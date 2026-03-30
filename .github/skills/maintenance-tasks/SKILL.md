---
name: maintenance-tasks
description: >-
  Schedule, track, and execute recurring maintenance procedures — stale reference
  audits, documentation drift checks, terminology consistency, and convention
  hygiene. Use when a project needs systematic upkeep that should happen
  automatically rather than relying on human memory.
license: MIT
---

# Maintenance Tasks

A framework for defining, scheduling, and executing recurring maintenance procedures in any project managed by Copilot CLI agents. Each procedure is a self-contained **task file** with its own trigger conditions, execution steps, and verification criteria.

Projects accumulate entropy — stale references, outdated docs, orphaned branches, drifting conventions. Humans forget to check; agents don't know when to check unless told. This skill provides the "when" and "how."

The framework is domain-agnostic in *what* it maintains, while assuming git-based project infrastructure (matching the Copilot CLI platform). A software repository might audit cross-references and prune branches; a writing project might check source freshness and terminology consistency; a strategic planning project might validate stakeholder maps and assumption currency. The scheduling and execution machinery is the same.

## Architecture

The maintenance system has three layers:

```
┌─────────────────────────────────────┐
│  Trigger Layer (when to run)        │  ← copilot-instructions.md or hooks
├─────────────────────────────────────┤
│  Framework Layer (what's due)       │  ← this SKILL.md + state file
├─────────────────────────────────────┤
│  Task Layer (how to do it)          │  ← individual task files in tasks/
└─────────────────────────────────────┘
```

**Trigger Layer** — defines *when* maintenance gets checked. The **recommended default** is instruction-based: add a line to `copilot-instructions.md` such as "at the start of each session, check if any maintenance tasks are due by reading `.github/skills/maintenance-tasks/SKILL.md` and the state file." Other options:
- **Hook-based**: a `sessionStart` hook that checks the state file and emits a reminder
- **Manual**: a human or coordinator agent explicitly invokes maintenance
- **Ritual-cadence**: the MAINTAIN phase of a ritual cadence cycle checks the maintenance registry

At least one concrete trigger must be wired up when adopting this skill — without one, the system is inert.

**Framework Layer** — this skill. Evaluates which tasks are due based on their trigger conditions and the state file, then dispatches them.

**Task Layer** — individual procedure files in `tasks/`. Each is self-contained and can be executed independently.

## State File

Maintenance state is tracked in `.github/maintenance-state.md` — a markdown file (not JSON) so it's human-readable and diff-friendly in version control. Teams that prefer structured data may use YAML or JSON if they update the runner's parsing logic accordingly.

### Format

```markdown
# Maintenance State

<!-- Auto-updated by maintenance-runner. Manual edits are safe. -->
<!-- If this file becomes malformed, delete it — the runner will regenerate it
     with all tasks marked overdue. -->

| Task | Last Run | Trigger | Next Due | Last Result | Consecutive Clean |
|------|----------|---------|----------|-------------|-------------------|
| stale-reference-audit | 2026-03-30 (ae38613) | every 20 commits | ~20 commits from ae38613 | ✅ 3 fixes | 0 |
| doc-drift-check | 2026-03-28 | weekly | 2026-04-04 | ✅ clean | 4 |
| branch-hygiene | 2026-03-30 (ae38613) | every 10 commits | ~10 commits from ae38613 | ✅ pruned 3 | 0 |
```

### Rules

- **Commit-counted triggers** store the commit SHA at last run; the runner counts commits since that SHA using `git rev-list --count <sha>..HEAD`. If the SHA is unreachable (force-push, rebase, garbage collection), treat the task as overdue and log "⚠️ recorded SHA unreachable — treating as due."
- **Time-based triggers** store a date; the runner compares to current date.
- **Event-based triggers** store the event that last triggered them; re-trigger on next matching event.
- If the state file doesn't exist, all tasks are considered overdue and the runner creates it.
- If the state file exists but is malformed (unparseable table), back it up as `maintenance-state.md.bak`, regenerate from the task directory with all tasks marked overdue, and log the recovery.
- The state file is committed to the repository so it persists across sessions.
- In environments without persistent storage (ephemeral CI containers, sandbox sessions), the state file resets each session. Consider using only `time-interval` triggers with conservative thresholds, or storing state externally (e.g., a GitHub Issue or project board).
- **Trigger type sync**: the runner re-reads each task file's frontmatter on every evaluation. If a task's trigger type/value changed since the last state entry, the runner updates the state file row to match and recalculates "Next Due."

### Frequency Calibration

Trigger thresholds are starting points, not permanent values. The state file tracks a **Consecutive Clean** counter — the number of consecutive runs where the task found zero issues.

- If a task reaches **5 consecutive clean** runs, the runner logs a suggestion: "consider doubling the trigger interval for [task]." It does not change the interval automatically — that requires editing the task file.
- If a task finds **>10 issues** in a single run, the runner logs: "consider halving the trigger interval for [task]."
- Suggestions are persisted in a **Pending Suggestions** section at the bottom of the state file so they survive across sessions. If the same suggestion has been emitted 3+ consecutive times without the trigger value changing, the runner escalates: "📊 calibration suggestion ignored for 3 runs — creating issue."

This makes frequencies empirically observable rather than static guesses.

## Task File Format

Each task lives in `.github/skills/maintenance-tasks/tasks/<task-name>.md` and follows this structure:

```markdown
---
name: <task-name>
summary: One-line description of what this task does
trigger:
  type: commit-count | time-interval | event
  value: 20 | weekly | on-session-start
severity: routine | important | critical
estimated-effort: small | medium | large
---

# <Task Name>

## Purpose
Why this task exists — what entropy it prevents.

## Trigger Conditions
When this task should run. Repeat the frontmatter trigger in prose,
plus any concrete skip conditions with mechanically evaluable criteria.

## Procedure
Numbered steps. Each step should be concrete and verifiable.
1. ...
2. ...
3. ...

## Verification
How to confirm the task completed successfully.
- [ ] Check 1
- [ ] Check 2

## Logging
What to record in the maintenance state file after execution.
```

### Effort Tiers

Effort estimates ground expectations for context-window and time budgets:
- **small**: scans <50 files or makes <10 changes
- **medium**: scans 50–200 files or makes 10–50 changes
- **large**: scans 200+ files or makes 50+ changes

The runner logs actual files-scanned and changes-made counts per task. If actual effort consistently exceeds the declared tier across 3 runs, it logs a suggestion to update the task's `estimated-effort`.

## Execution Model

Maintenance tasks can be executed by:

1. **Any agent** — an agent reads this skill, checks the state file, and runs overdue tasks inline. Best for lightweight tasks during normal work.

2. **A dedicated maintenance-runner agent** — a purpose-built agent that systematically evaluates and runs all overdue tasks. Best for comprehensive sweeps.

3. **A coordinator's MAINTAIN phase** — the research-team coordinator (or any agent following the ritual-cadence pattern) checks the maintenance registry during its maintenance phase.

### Execution Protocol

Regardless of who runs the task:

1. **Lock** — write a `<!-- 🔒 maintenance in progress — [timestamp] -->` comment to the state file and commit it. Other runners seeing this comment within 30 minutes should skip execution. Locks older than 30 minutes are considered stale and may be overridden.
2. **Check** — read the state file; identify tasks whose trigger conditions are met
3. **Prioritise** — sort by severity (critical > important > routine), then by how overdue
4. **Execute** — for each due task, read its task file and follow the procedure
5. **Verify** — run the task's verification checks
6. **Update state** — write the result, new "last run," and updated Consecutive Clean counter to the state file
7. **Unlock and commit** — remove the lock comment; commit the state file update (may be batched with the task's own changes)

### Partial Execution

If time or context is limited:
- Run only critical/important tasks; defer routine ones
- Run the single most overdue task
- Log deferred tasks as "skipped (reason)" in the state file — do NOT silently ignore them

## Adding New Tasks

1. Create a new file in `tasks/` following the task file format
2. The task is automatically discoverable — the runner scans the `tasks/` directory
3. On first encounter, the runner adds it to the state file with "never" as last run, making it immediately due
4. No changes to this SKILL.md or any other file are needed

## Removing Tasks

1. Delete the task file from `tasks/`
2. Optionally remove its row from the state file (the runner will ignore orphaned rows)
3. No other changes needed

## Error Handling

- If a task's procedure fails partway through, record "❌ failed at step N: <error>" in the state file. Revert partial changes from the failed task. Continue with the next task.
- **Consecutive failure escalation**: track consecutive failures per task. After 3 consecutive failures, mark the task as "⚠️ needs attention — 3 consecutive failures" and stop attempting it until the task file's content changes (detected via file modification).
- **Abort threshold**: if ≥2 tasks fail AND >50% of tasks in the current run fail, stop the run and log "⚠️ maintenance sweep aborted — majority failure." This prevents a single flaky failure in a small task set from triggering an abort.

## Known Limitations

- **False-negative results**: a task that runs successfully but misses actual issues (e.g., a stale-reference audit that doesn't recognise a particular link syntax) will report "✅ clean" and increment Consecutive Clean, potentially triggering a suggestion to run *less* often. There is no built-in cross-validation. For high-stakes tasks, consider periodically injecting a known-broken canary to verify detection accuracy.
- **Lock race condition**: if two runners read the state file simultaneously before either writes a lock, both may proceed. The 30-minute lock timeout bounds the damage to duplicate execution. This is acceptable at typical maintenance frequencies but could cause issues in heavily concurrent environments.
- **Git infrastructure dependency**: the runner assumes a git-backed repository. Commit-count triggers, SHA-based state, and `git checkout` rollbacks are git-specific. Non-git projects should rely on `time-interval` and `event` triggers instead.

## Integration with Other Patterns

- **Ritual Cadence**: the MAINTAIN phase naturally integrates with this skill. Add "check maintenance-tasks registry" to the tidy procedure.
- **Research Team**: the coordinator's MAINTAIN phase should check for due maintenance tasks and dispatch an operations member to handle them.
- **Hooks**: a `sessionStart` hook can check the state file and emit a reminder if critical tasks are overdue.

## Example Tasks for Other Domains

The task format works for any project type. Some examples beyond software maintenance:

- **Source freshness check** — verify that cited URLs and references are still accessible and current (research, journalism, documentation projects)
- **Terminology consistency audit** — scan for vocabulary drift across documents; flag synonyms that should be standardised (writing, legal, policy projects)
- **Stakeholder reference validation** — confirm that named contacts, roles, and organisational references are still accurate (planning, governance projects)
- **Continuity audit** — check for contradictions in character names, timelines, or world-building details (creative writing projects)

## Tasks

<!-- Task index — auto-discoverable from tasks/ directory, listed here for convenience.
     The stale-reference-audit below is specific to repositories with Copilot CLI
     infrastructure. Your project's tasks will target your own reference types. -->

### Stale Reference Audit

> Scan the repository for internal cross-references (file paths, section links,
> skill/agent names) that point to renamed, moved, or deleted targets. Fix or
> flag each one.

**Trigger**: every 20 commits (starting point — calibrate based on observed results)
**Severity**: routine

→ Read `.github/skills/maintenance-tasks/tasks/stale-reference-audit.md` for the full procedure.
