---
title: Compensating Workflow (Saga)
summary: >-
  Each forward step in a multi-step workflow is paired with a compensating
  action that undoes its effects. On failure, compensating actions execute in
  reverse order, restoring the system to a clean state instead of leaving
  orphaned resources, partial reservations, and dangling artifacts.
trigger: >-
  Multi-step agent workflows that modify external state — files, branches,
  API calls, bookings, registrations, notifications, procurement orders,
  deployments — where partial failure would leave the system in an
  inconsistent state requiring manual cleanup.
---

# Compensating Workflow (Saga)

## What It Is

A structuring pattern for multi-step workflows where each forward step that modifies state is **paired with a compensating action** that reverses it. Steps execute sequentially, recording their completion in an execution log. If any step fails, the workflow halts forward progress and runs compensating actions **in reverse order** from the last completed step back to the first, restoring the system to the state it was in before the workflow began.

The name comes from the **Saga pattern** in distributed systems — a technique for managing long-lived transactions across multiple services where a traditional atomic rollback isn't available. The adaptation for agent workflows is direct: agents modify state across multiple systems (file systems, remote APIs, booking platforms, notification services) with no global transaction boundary. Each system must be rolled back independently, in the right order, using explicit undo operations. There is no "rollback" button — compensation must be designed, not assumed.

What distinguishes this from simple error handling is **intentional symmetry**: you don't write the forward steps and hope you'll figure out cleanup later. Every forward step is authored alongside its compensating action at design time. The two are a pair — if you can't define a compensating action for a step, that step is either irreversible (and must be positioned last in the workflow) or the workflow needs restructuring.

## Why It Works

- **Explicit cleanup eliminates orphaned state** — agents can't "undo" by default. Without predefined compensating actions, a failure at step 3 of 5 leaves steps 1–2's side effects permanently in place. Pairing each step with its reverse makes cleanup deterministic rather than ad-hoc.
- **Reverse-order execution respects dependencies** — steps are sequenced because later steps depend on earlier ones. Compensation must run in reverse for the same reason: you can't release an allocated resource (compensate step 1) before removing the records that reference it (compensate step 4). Reverse order ensures each compensation step operates against valid state.
- **The execution log makes recovery resumable** — recording each step's outcome to a persistent log means compensation can resume even if the compensating workflow itself is interrupted. A new session can read the log, determine which steps completed, and run the remaining compensations.
- **Design-time pairing catches irreversibility early** — when you must define the compensating action at the same time as the forward step, you discover irreversible operations (sent notifications, published releases, signed contracts, filed regulatory submissions, physical shipments) before they're buried in the middle of a workflow. This forces you to sequence irreversible steps last or add confirmation gates before them.
- **Scope control prevents over-engineering** — the pattern applies at the workflow level, not the operation level. You don't saga-wrap every individual edit; you saga-wrap the workflow that allocates resources, produces artifacts, validates results, and publishes outcomes. This keeps the overhead proportional to the risk.

## How to Implement

### 1. Define Step-Compensation Pairs

For each step in the workflow that modifies external state, define its compensating action. Steps that don't modify state (running validations, reading records, computing values) don't need compensation.

**General categories of step-compensation pairs:**

| Category | Forward action (example) | Compensating action (example) |
|----------|-------------------------|-------------------------------|
| Resource allocation / deallocation | Reserve a venue, allocate a server, open a work stream | Release the venue, deallocate the server, close the work stream |
| Artifact creation / deletion | Generate files, create records, produce reports | Delete the files, remove the records, retract the reports |
| Registration / withdrawal | Register a participant, enrol in a programme, add to a roster | Withdraw the participant, cancel the enrolment, remove from the roster |
| Notification / retraction | Send an invitation, publish an announcement, issue a confirmation | Send a cancellation notice, retract the announcement, revoke the confirmation |
| Procurement / cancellation | Place an order, book a service, request a shipment | Cancel the order, cancel the booking, cancel the shipment |
| Publication / unpublication | Publish a release, push to a remote, deploy an update | Unpublish the release, remove the remote reference, roll back the deployment |

These categories apply across domains. A git feature-branch workflow, a conference organisation workflow, and an infrastructure provisioning workflow all use the same structural pattern — only the specific forward and compensating actions differ.

**Example: Git feature-branch workflow**

| Step | Forward action | Compensating action | Notes |
|------|---------------|---------------------|-------|
| 1 | Create feature branch | Delete branch (`git branch -D`) | Branch must not be the current checkout when deleted |
| 2 | Generate/edit code files | Restore originals or delete created files | Use `git checkout -- .` if on a branch; otherwise track created files |
| 3 | Run tests | *(none — read-only)* | Tests don't modify state; no compensation needed |
| 4 | Commit and push | Delete remote branch (`git push origin --delete`) | Force-push or branch delete; local commit is handled by branch deletion in step 1's compensation |
| 5 | Create pull request | Close PR via API | Must handle "PR already merged" case gracefully |

**Example: Conference presentation workflow**

| Step | Forward action | Compensating action | Notes |
|------|---------------|---------------------|-------|
| 1 | Reserve speaking slot | Cancel reservation with organiser | Must respect cancellation deadline |
| 2 | Book travel and accommodation | Cancel travel booking | Check cancellation policy; some bookings become non-refundable |
| 3 | Prepare presentation slides | *(none — local artifact, no external state)* | No compensation needed unless slides were uploaded to a shared system |
| 4 | Submit slides to organiser | Request slide withdrawal | Must handle "slides already published in programme" case |
| 5 | Send attendance confirmation to co-presenters | Send cancellation notice | Notification is partially irreversible — recipients have already seen it |

**Design rules:**

- Every state-modifying step **must** have a compensating action defined before the workflow executes. If you can't define one, the step is irreversible — move it to the end or gate it with human confirmation.
- Compensating actions should be **narrower** than their forward actions. The forward step might create 15 files or book 3 services; the compensating action should delete exactly those 15 files or cancel exactly those 3 bookings, not wipe the directory or cancel all active bookings.
- Store the pair definitions in a structure the workflow can traverse. In an agent context, this is typically a list in the prompt or a section in a skill file:

```markdown
## Workflow Steps

### Step 1: Create feature branch
- **Action**: `git checkout -b feature/saga-example`
- **Compensate**: `git checkout main && git branch -D feature/saga-example`
- **Modifies state**: yes

### Step 2: Generate code
- **Action**: Create files per specification
- **Compensate**: `git checkout -- . && git clean -fd`
- **Modifies state**: yes

### Step 3: Run tests
- **Action**: Execute test suite
- **Compensate**: *(none)*
- **Modifies state**: no
```

### 2. Create the Execution Log

The execution log is a persistent record of which steps have been attempted and their outcomes. It serves two purposes: (1) the compensation chain reads it to know where to start rolling back, and (2) a returning session can resume compensation if the agent was interrupted mid-rollback.

Store the log as a file in a predictable location. For agent workflows, co-locate it with the workflow's other state:

```markdown
# Execution Log — [workflow name]

| Step | Action | Status | Timestamp | Detail |
|------|--------|--------|-----------|--------|
| 1 | Create branch `feature/saga-example` | ✅ completed | 2025-01-15T10:00:00Z | Branch created from `main` at `abc1234` |
| 2 | Generate code | ✅ completed | 2025-01-15T10:01:30Z | Created 3 files: `src/a.ts`, `src/b.ts`, `test/a.test.ts` |
| 3 | Run tests | ❌ failed | 2025-01-15T10:02:45Z | 2 of 8 tests failed — `TypeError` in `src/a.ts:42` |
| 4 | Commit and push | ⏭ skipped | — | Not attempted (step 3 failed) |
| 5 | Create PR | ⏭ skipped | — | Not attempted (step 3 failed) |
```

**Log management rules:**

- Write the log entry **after** each step completes (success or failure), not before.
- Include enough detail to support compensation: resource identifiers, file paths, confirmation numbers, record IDs. The compensating action will need this information.
- Status values: `✅ completed`, `❌ failed`, `⏭ skipped`, `🔄 compensated`, `⚠️ compensation-failed`.
- After successful compensation of all steps, append a summary line: `Compensation complete — system restored to pre-workflow state.`
- Clean up the log file after a fully successful workflow or a fully successful compensation. A log that persists means something is unresolved.

### 3. Execute Forward Steps

Run steps sequentially. After each step, update the execution log. If a step fails, immediately stop forward execution and transition to the compensation protocol.

```
for each step in workflow_steps:
    log step as "in progress"
    try:
        execute step.forward_action
        log step as "completed" with detail
    on failure:
        log step as "failed" with error detail
        log remaining steps as "skipped"
        begin compensation from last completed step
        return
log workflow as "completed"
clean up execution log
```

**Critical implementation detail for agents:** In Copilot CLI, "sequential execution" means the coordinator dispatches one subagent at a time (or executes steps inline) and checks the result before proceeding. Do **not** dispatch all steps in parallel — the entire point of the saga is that step N+1 only executes if step N succeeded.

This is where the pattern diverges from patterns like Research Team, which maximises parallelism. A saga is inherently sequential for forward steps. The trade-off is intentional: you sacrifice speed for the ability to halt cleanly.

### 4. Execute Compensation on Failure

When a step fails, iterate backwards through the execution log from the last `✅ completed` step to the first, executing each step's compensating action.

```
failed_at = index of failed step
for i from (failed_at - 1) down to 0:
    if execution_log[i].status == "completed":
        try:
            execute step[i].compensating_action
            update execution_log[i].status to "compensated"
        on failure:
            update execution_log[i].status to "compensation-failed"
            log the failure detail
            continue  # attempt remaining compensations
```

**Do not stop compensation on a single compensation failure.** If compensating step 3 fails, still attempt to compensate steps 2 and 1. Partial rollback is bad, but rolling back everything you can is strictly better than stopping at the first compensation failure. Log which compensations failed so a human can address the remainder.

**After compensation completes**, report the final state: which steps were compensated, which compensations failed, and what manual intervention is needed (if any).

### 5. Make Compensating Actions Idempotent

Compensating actions must be safe to run multiple times. This is non-negotiable — compensation can be interrupted and retried, or a human might manually fix something and then re-run the compensation chain. If a compensating action fails when the state is already clean, the workflow breaks for no reason.

| Action | Non-idempotent (fragile) | Idempotent (safe) |
|--------|--------------------------|-------------------|
| Delete branch | `git branch -D feature/x` (fails if branch doesn't exist) | `git branch -D feature/x 2>$null; $true` or check-then-delete |
| Delete remote branch | `git push origin --delete feature/x` (fails if already deleted) | Check remote branch existence first, skip if absent |
| Close PR | `gh pr close N` (fails if already closed) | `gh pr close N` (actually idempotent — GitHub API accepts this) |
| Remove created files | `Remove-Item src/a.ts` (fails if file doesn't exist) | `Remove-Item src/a.ts -ErrorAction SilentlyContinue` |
| Cancel vendor order | Call cancellation API (fails if already cancelled) | Check order status first; if already cancelled, treat as success |
| Cancel venue booking | Send cancellation request (fails if booking not found) | Query booking status; if not found or already cancelled, return success |

The general principle: **check whether the state you're trying to undo still exists before undoing it, and treat "already clean" as success.**

### 6. Handle the Stuck State

When compensation itself fails, the system is in the worst possible state: partially modified and partially rolled back. The execution log exists precisely for this scenario — it records which compensations succeeded and which failed, giving a human (or a future agent session) a precise inventory of what remains.

**Escalation protocol:**

1. **Log everything.** The execution log must record every compensation attempt and its outcome. Do not summarise; record verbatim.
2. **Report to the user.** Produce a clear summary: "Steps 1–3 completed. Step 4 failed. Compensation of step 3 succeeded. Compensation of step 2 failed (venue has a no-cancellation policy within 48 hours of the event). Compensation of step 1 skipped (depends on step 2). Manual action required: contact venue manager to negotiate cancellation, and send retraction to the 12 notified attendees."
3. **Leave the execution log in place.** A persistent log signals "this workflow is unresolved." Do not clean it up until all state is restored.
4. **Do not retry compensation indefinitely.** One automatic retry per compensation step is reasonable. Beyond that, the problem is likely environmental (permissions, network, conflicts) and requires human intervention.

### 7. Integrate with Existing Patterns

Any pattern that modifies external state can wrap its state-changing operations in a saga. The saga is not a competing pattern — it's a **safety layer** that any workflow can adopt.

| Pattern | Where sagas apply |
|---------|------------------|
| **Research Team** | Coordinator dispatches work that creates branches, writes files, opens PRs. Wrap the finalisation cycle (branch → commit → push → PR → merge) in a saga. |
| **Git-Checkpoint** | Already a specific instance of this pattern for git operations. The compensating workflow generalises it to non-git state changes. |
| **Ritual Cadence** | The tidy phase can use a saga when cleaning up multiple branches or worktrees — if deletion of worktree 3 fails, don't leave worktrees 1–2 in a half-cleaned state. |
| **Multi-Reviewer Panel** | Reviewers are read-only and don't need sagas. The orchestrator's synthesis step might write files — that step benefits from compensation if it's part of a larger workflow. |

**Integration is lightweight.** You don't need to restructure an existing workflow to add saga support. Identify the state-modifying steps, define their compensating actions, add an execution log, and wrap the execution in the forward/compensate protocol. The rest of the workflow stays unchanged.

## Gotchas

- **Not every workflow needs a saga.** A single action followed by one dependent action doesn't justify the overhead of step-compensation pairs and an execution log. Reserve sagas for workflows with three or more state-modifying steps where partial failure would cause meaningful damage. Over-engineering simple operations with saga infrastructure creates complexity without safety benefit.
- **Some actions are genuinely irreversible.** A sent notification, a published package, a signed contract, a filed regulatory submission, a physical shipment, a merged change that others have based work on — these cannot be undone by a compensating action. Design your workflow so irreversible steps come last, after all fallible steps have succeeded. If an irreversible step must come early, gate it with human confirmation or accept that compensation will be partial.
- **The execution log is itself state that must be managed.** If you store it in a file and the file write fails, your compensation chain has no data to work from. Write the log to the most reliable location available. For agent workflows, the working directory or the worktree root is appropriate. Don't store it in a temporary directory that might be cleaned up by the OS. Clean up successful logs; leave failed logs as unresolved markers.
- **Compensation that fails leaves the worst state.** A system that is fully forward (all steps succeeded) or fully rolled back (all compensations succeeded) is consistent. A system that is partially rolled back is inconsistent in an unpredictable way. This is why compensating actions must be idempotent and why compensation continues past individual failures — maximise rollback coverage even when perfection isn't achievable.
- **Agent context windows may not survive the full compensation chain.** A workflow with 8 steps that fails at step 7 needs to compensate 6 steps. If the agent's context window is exhausted, it may lose track of the execution log or the compensation sequence. Mitigation: keep the execution log in a file (not just in-context), and design the compensation protocol so a new session can resume from the log. The log is the hand-off mechanism.
- **Use native operations for compensation, not hand-rolled alternatives.** Every system has built-in mechanisms for undoing changes — git has `revert`, `reset`, and `branch -D`; booking platforms have cancellation APIs; cloud providers have resource deletion endpoints. Your compensating actions should use these native primitives. The saga pattern provides the *structure* (when to compensate, in what order); the target system provides the *primitives* (how to compensate).
- **Compensating actions need the same context as forward actions.** If step 2 created files and you need to delete them in compensation, the compensating action needs to know *which* files. This information must be recorded in the execution log at the time step 2 completes. A compensating action that says "delete created files" without a file list is useless. Log specifics, not intentions.
- **Parallel steps complicate compensation ordering.** If steps 2a and 2b execute in parallel and 2b fails, you need to compensate both 2a (which succeeded) and roll back any partial effects of 2b — but the ordering between parallel steps is ambiguous. Avoid parallelism within sagas. If you must parallelise, treat the parallel group as a single logical step with a single composite compensating action.

## Examples

### Example A: Git Feature Branch Workflow

An agent workflow that creates a feature branch, generates code, runs tests, commits, pushes, and opens a PR — with full saga compensation.

**Step-compensation pairs defined in the skill:**

```markdown
## Saga: Feature Branch Workflow

### Step 1: Create feature branch
- **Forward**: `git checkout -b feature/add-validation`
- **Compensate**: `git checkout main; git branch -D feature/add-validation`
- **Log detail**: branch name, base commit SHA

### Step 2: Generate code changes
- **Forward**: Create/edit files per specification
- **Compensate**: `git checkout -- .; git clean -fd`
- **Log detail**: list of created and modified file paths

### Step 3: Run tests
- **Forward**: `npm test`
- **Compensate**: *(none — tests are read-only)*
- **Log detail**: pass/fail, failure summary if applicable

### Step 4: Commit and push
- **Forward**: `git add -A; git commit -m "feat: add validation"; git push -u origin feature/add-validation`
- **Compensate**: `git push origin --delete feature/add-validation`
- **Log detail**: commit SHA, remote URL

### Step 5: Create pull request
- **Forward**: `gh pr create --title "feat: add validation" --body "..."`
- **Compensate**: `gh pr close {pr_number}`
- **Log detail**: PR number, PR URL
```

**Scenario A — tests fail at step 3:**

1. Step 1 completes: branch `feature/add-validation` created. Logged.
2. Step 2 completes: 4 files created, 2 modified. Logged with file paths.
3. Step 3 fails: 3 of 12 tests fail. Logged with failure details.
4. Steps 4–5 skipped. Logged.
5. **Compensation begins** — iterate backward from step 2 (step 3 has no compensation):
   - Compensate step 2: `git checkout -- . && git clean -fd` — file changes reverted. Logged as `🔄 compensated`.
   - Compensate step 1: `git checkout main && git branch -D feature/add-validation` — branch deleted. Logged as `🔄 compensated`.
6. Execution log updated: `Compensation complete — system restored to pre-workflow state.`
7. Log file cleaned up. Agent reports: "Tests failed (3/12). Workflow rolled back. No residual state."

### Example B: Conference Presentation Workflow

An agent workflow that organises a conference presentation: reserves a speaking slot, books travel, prepares materials, submits slides, and notifies co-presenters.

**Step-compensation pairs:**

| Step | Forward action | Compensating action | Notes |
|------|---------------|---------------------|-------|
| 1 | Reserve speaking slot with organiser | Cancel slot reservation | Must respect cancellation deadline |
| 2 | Book flights and hotel | Cancel travel booking | Check refund policy; some bookings become non-refundable after a deadline |
| 3 | Prepare presentation slides | *(none — local work, no external state)* | No compensation needed |
| 4 | Submit slides to conference platform | Request slide withdrawal from platform | Must handle "slides already published in programme" case |
| 5 | Send confirmation to co-presenters | Send cancellation notice to co-presenters | Partially irreversible — recipients have already seen the original |

**Scenario B — travel booking fails at step 2:**

1. Step 1 completes: speaking slot reserved for "Saga Patterns in Practice", confirmation #CP-2025-0442. Logged.
2. Step 2 fails: no available flights within budget on the conference dates. Logged with failure details.
3. Steps 3–5 skipped. Logged.
4. **Compensation begins** — iterate backward from step 1 (step 2 has no completed state to compensate):
   - Compensate step 1: cancel speaking slot reservation #CP-2025-0442. Confirmation of cancellation received. Logged as `🔄 compensated`.
5. Execution log updated: `Compensation complete — system restored to pre-workflow state.`
6. Log file cleaned up. Agent reports: "Travel booking failed (no flights within budget). Speaking slot reservation cancelled. No residual state."

### Scenario C — compensation itself fails (applicable to any domain)

This scenario illustrates the stuck state, where compensation partially succeeds. The specific domain doesn't matter — the protocol is the same.

**Git example:**

1. Steps 1–3 complete. Step 4 (push) fails due to a pre-push hook rejection.
2. Compensation of step 2 succeeds (files reverted).
3. Compensation of step 1 fails — the branch can't be deleted because a worktree is attached to it.
4. Execution log shows: step 2 `🔄 compensated`, step 1 `⚠️ compensation-failed`.
5. Agent reports: "Push failed (pre-push hook). Partial rollback: files reverted, but branch `feature/add-validation` could not be deleted (worktree attached). Manual action required: `git worktree remove <path> && git branch -D feature/add-validation`."
6. Execution log persists until the branch is manually cleaned up.

**Conference example:**

1. Steps 1–4 complete. Step 5 (send confirmation to co-presenters) fails due to a mail service outage.
2. Compensation of step 4 succeeds (slides withdrawn from platform).
3. Compensation of step 2 fails — the hotel booking has passed its free cancellation deadline and requires manual negotiation.
4. Compensation of step 1 succeeds (speaking slot released).
5. Execution log shows: step 4 `🔄 compensated`, step 2 `⚠️ compensation-failed`, step 1 `🔄 compensated`.
6. Agent reports: "Notification failed (mail service outage). Partial rollback: slides withdrawn, speaking slot released, but hotel booking (confirmation #HB-9981) could not be auto-cancelled (past free cancellation window). Manual action required: contact hotel to negotiate cancellation or transfer."
7. Execution log persists until the hotel booking is manually resolved.

## Validating Compensation

After compensation completes, verify that the system state matches the pre-workflow state. Automated verification catches cases where a compensating action reported success but left residual state.

**Validation approach:**

1. **Capture a pre-workflow state snapshot** before the first forward step. Record the relevant state inventory for your domain.
2. **After compensation completes**, capture the same state inventory and compare it to the snapshot.
3. **Report discrepancies** as compensation failures even if all compensating actions reported success.

**Domain-specific examples:**

- **Git workflows**: Compare `git status`, branch list (`git branch -a`), and remote refs to the pre-workflow snapshot. Any new branches, modified files, or remote refs that didn't exist before indicate incomplete compensation.
- **Booking/registration workflows**: Query the relevant systems (venue booking status, travel reservation status, participant roster) and confirm they match the pre-workflow state. A reservation that still appears as "active" after compensation indicates a failed rollback.
- **Infrastructure workflows**: List provisioned resources and compare to the pre-workflow inventory. Any resources that were created during the workflow and still exist indicate incomplete compensation.
