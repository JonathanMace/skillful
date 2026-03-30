---
title: Research Team
summary: >-
  A coordinator agent that delegates all substantive work to team member
  subagents — recruiting, briefing, and dispatching specialists dynamically.
  The coordinator orchestrates and synthesises but never performs the work
  itself.
trigger: >-
  Multi-step investigative, creative, or development projects where the work
  spans multiple domains, benefits from parallel specialist effort, and evolves
  as new questions emerge.
---

# Research Team

## What It Is

A **coordinator agent** that functions as the head of a dynamic team. The coordinator never performs substantive work itself — it assesses the task, reviews which team members are available, recruits new specialists when gaps exist, dispatches work to team members in parallel, and synthesises their results into a coherent deliverable.

The coordinator role is sometimes called a **principal investigator (PI)** — a metaphor borrowed from academic research, but the pattern applies equally to product development, R&D, investigative analysis, strategic planning, creative production, security audits, or any endeavour where work decomposes into specialist domains. What matters is the separation between orchestration and execution, not the domain.

Team members are **embedded subagent instruction files** stored in a subdirectory beneath the coordinator's agent profile. Each file defines a specialist role — its expertise, responsibilities, constraints, and output format. The coordinator spawns subagents via the `task` tool, instructing each to read and follow a specific instruction file. Because these files live in a subdirectory (not as `.agent.md` files in `.github/agents/`), they are invisible to agent discovery and cannot be invoked directly by users.

What distinguishes this pattern from the Multi-Reviewer Panel or Mentor Constellation is **dynamism**: the coordinator can create new team members on the fly by authoring new instruction files. The team evolves as the work evolves.

## When to Use — and When Not To

**Use this pattern when:**
- The work spans multiple domains that benefit from specialist focus
- Parallel effort accelerates the outcome
- The project evolves — new questions emerge that require new expertise
- Quality benefits from separation between doing work and reviewing work

**Do NOT use this pattern when:**
- The work is irreducibly singular (e.g., a single creative act that can't be decomposed)
- Time pressure demands immediate action with no recruitment overhead — dispatch an existing generalist directly
- The project is small enough that one agent can handle it in a single pass
- Regulatory or compliance requirements prescribe a fixed team composition (the pattern's dynamism may conflict with mandated roles)

For urgent work within an otherwise research-team-structured project, the coordinator should have a **fast path**: dispatch an existing member with an ad-hoc prompt rather than recruiting a new specialist.

## Why It Works

- **Separation of strategy from execution** — the coordinator focuses on what to investigate and who should investigate it. Team members focus on doing the work. This prevents the coordinator from getting lost in details and prevents specialists from losing sight of the big picture.
- **Dynamic team composition** — unlike static patterns where the cast is fixed at design time, the coordinator can recruit new specialists as questions emerge. The team grows to fit the problem.
- **Parallel specialist execution** — team members run in separate context windows with no shared state, so multiple investigations happen simultaneously. The coordinator's synthesis step is the only sequential bottleneck.
- **Persistent expertise via instruction files** — each team member's instruction file persists across sessions. When a specialist is recruited for one task, it remains available for future tasks. The team accumulates capability over time — provided the coordinator maintains and refines member files based on observed performance (see "Feedback Loops" below).
- **Self-improving infrastructure** — rules and conventions sediment from experience rather than being prescribed upfront. The coordinator updates instruction files based on observed failures, and each update takes effect on the next dispatch.
- **Review gates prevent fire-and-forget** — draft artifacts pass through a review panel before being finalised. This catches domain assumptions, untestable claims, and hidden human dependencies before they calcify into infrastructure.

## The Agent Taxonomy

Teams naturally develop five categories of members. Not every team needs all five, but knowing the categories helps the coordinator identify gaps:

| Category | Purpose | Tool profile | Example members |
|----------|---------|-------------|-----------------|
| **Production** | Do the substantive work | Full tools (read, search, edit, execute) | Writer, analyst, engineer, designer |
| **Review** | Attack the work for quality | Read-only + execute where needed | Reviewer panel, consistency auditor, editor |
| **Strategic** | Challenge direction and assumptions | Read-only + web | Provocateur, scout, landscape analyst |
| **Advisory** | Prevent pathological patterns | Read-only (no edit, no execute) | Mentor figures, anti-perfectionism roles |
| **Operations** | Maintain infrastructure | Full tools, rigid SOP | Chief-of-staff, process steward |

**Tool constraints are safety boundaries, not suggestions.** A reviewer that can't edit files is *structurally* prevented from fixing the problems it finds — it must report them for the coordinator or a production member to address. An advisor that can't execute commands can't accidentally cause side effects. Design tool lists around least privilege.

**A note on enforcement:** For team members defined as `.agent.md` files, tool constraints are structural — the platform enforces them. For embedded subagent instruction files dispatched via the `task` tool, tool constraints are **prompt-level** — the instruction file says "you do not edit files" but the subagent technically has access. If a safety boundary is critical (e.g., an advisory member must never edit), consider promoting it to a `.agent.md` file with `user-invocable: false` and `disable-model-invocation: true`. For most members, prompt-level constraints are sufficient — but be aware of the distinction. See the `writing-custom-agents` skill for detailed guidance on this trade-off.

## How to Implement

### 1. Create the Coordinator Agent

The coordinator is an `.agent.md` file in `.github/agents/`. Its prompt defines the orchestration workflow — never the work itself.

The coordinator's prompt should include:

- A **role statement** as a coordinator who delegates everything
- A **team roster protocol** — always inspect the team member directory before dispatching
- A **recruitment procedure** — how to create new team members when a gap exists
- A **dispatch procedure** — how to spawn subagents with explicit instruction-file references
- A **synthesis procedure** — how to combine results from multiple team members
- A **review-before-finalising gate** — drafts are reviewed before being made canonical
- A **constraint** that the coordinator never performs substantive work directly

```yaml
---
name: research-team
description: >-
  Coordinator who orchestrates a dynamic team. Delegates all work to
  specialist subagents, recruiting new team members as needed.
tools: ["*"]
---
```

### 2. Structure the Team Member Directory

Team member instruction files live in a subdirectory co-located with the coordinator agent:

```
.github/agents/
├── research-team.agent.md          # Coordinator agent
└── research-team/                  # Team member instructions
    └── members/
        ├── README.md               # Roster: lists all members and their roles
        ├── progress.md             # Session continuity state
        ├── log.md                  # Append-only cycle log
        └── (member files created dynamically by the coordinator)
```

The `README.md` serves as a roster — a living document that the coordinator updates whenever it recruits a new member. This is the coordinator's first read before any dispatch.

### 3. The Coordinator's Core Loop

The coordinator follows a consistent decision loop for every task:

1. **Bootstrap** — if a progress file exists (`members/progress.md`), read it to resume from the last cycle. If the file exists but is malformed (missing required sections), fall back to the log file's last `**Next**:` entry. If both are unusable, start fresh and log the data loss.
2. **Assess** — what domains of expertise does this require? What are the key questions?
3. **Review roster** — read `members/README.md` to see who's available
4. **Identify gaps** — which required domains lack a team member?
5. **Recruit** — for each gap, author a new instruction file and update the roster. After authoring, verify the file contains all required sections (Role, What You Do, What You Do NOT Do, Output Format, Working Method). For critical roles, dispatch the review panel against the member file before first use.
6. **Dispatch** — spawn subagents via the `task` tool, each reading its instruction file. Include an **expected-outcome statement** in each dispatch prompt. If more than half of dispatched members fail in the same wave, do NOT retry individually — log the collective failure, reduce the next wave size, and wait one cycle before full-scale dispatch.
7. **Triage results** — for each member result, verify it addresses the assigned task and contains substantive content. If a member failed (garbage, timeout, empty result): retry once with a more specific prompt. If it fails again, flag the gap in the synthesis as "not investigated — member failure."
8. **Synthesise** — collect results, resolve conflicts, produce a unified deliverable. Genuine synthesis means surfacing contradictions, identifying cross-cutting themes, and producing conclusions not present in any individual report — not concatenation with headers.
9. **Review** — before finalising artifacts, dispatch reviewers (see "Review Gates" below)
10. **Iterate** — refine based on review feedback; repeat until the review-pass criteria are met
11. **Retrospect** — note whether team members performed well; update instruction files if needed. Sample one existing rule and check whether the failure it was created to prevent has recurred.
12. **Update progress** — write the current state to `members/progress.md`. As the session ages and context pressure builds, write *more* detail — the progress file is the hand-off mechanism to the next session.

### 4. The Iteration Cycle

For sustained work (not one-off questions), the coordinator operates in cycles:

**DO → REVIEW → LOG → FINALISE → PLAN → MAINTAIN**

- **DO**: Dispatch multiple team members in parallel, each on independent work
- **REVIEW**: Run a review panel against the output (see "Review Gates" below)
- **LOG**: Append to `members/log.md` — see "Logging" below for format
- **FINALISE**: Make reviewed artifacts canonical. For repo-resident artifacts, this means branch → PR → merge → cleanup (using the `git-checkpoint` skill or equivalent). If merge fails due to conflict, rebase and retry once; if that also fails, leave the PR open and log it as blocked. For other deliverables, finalise however is appropriate.
- **PLAN**: Identify the next batch of work; update priorities in the progress file. **Re-read the original task description** and verify that planned next actions still serve the original objective. If drift is detected, log it and recalibrate.
- **MAINTAIN**: Audit team health — members not dispatched in the last 3 cycles are candidates for archival. Check for contradictory rules in member files. Update roster "Last Dispatched" column. If `log.md` exceeds 30 entries, summarise the oldest into a `## Summary of Cycles 1–N` block and keep only the last 10 cycles in full detail.

After MAINTAIN, the coordinator should **self-continue** to the next DO step unless a stopping condition is met:
- All planned work items are exhausted
- A maximum cycle count has been reached
- Three consecutive cycles rated "low significance" → pause and report to human
- A critical unresolved finding blocks progress
- An explicit stop instruction was given

**Platform constraint:** In Copilot CLI, the coordinator runs in response to user messages. Sustained autonomous operation across many cycles may be limited by context window size and session duration. The progress file mitigates this — each new session bootstraps from the last checkpoint.

### 5. Logging

Maintain a `members/log.md` file with append-only log entries. Each entry follows this format:

```markdown
## Cycle N — [date/time or session identifier]

**Dispatched**: [list of members and their tasks]
**Outcomes**: [specific results — numbers, decisions, artifacts produced]
**Review verdict**: [pass/fail, key findings]
**Decisions made**: [what the coordinator decided and why]
**Significance**: [high/medium/low — see criteria below]
**Next**: [what the next cycle should focus on]
```

**Significance levels:**
- **High** — produced or finalised a deliverable artifact
- **Medium** — advanced work items measurably (new findings, resolved blockers, substantive revisions)
- **Low** — cycle completed but no work items advanced, or all outputs were refinements of existing work

The log serves three purposes: (1) a returning human can understand what happened, (2) a new coordinator session can resume via the progress file, (3) the MAINTAIN step can detect diminishing returns (three consecutive "low" cycles → pause and report).

### 6. Session Continuity

Maintain a `members/progress.md` file that the coordinator updates at every cycle boundary:

```markdown
# Progress

## Current State
- **Cycle**: N
- **Phase**: [DO/REVIEW/LOG/FINALISE/PLAN/MAINTAIN]
- **Active work items**: [list]
- **Completed work items**: [list]
- **Open questions**: [list]
- **Original task**: [the user's initial request, preserved for drift detection]
- **Session-local rules**: [rules discovered this session that haven't been committed to member files yet]

## Next Actions
[What the next cycle should do first]
```

The coordinator's core loop begins with "read the progress file if it exists." This allows any session to resume where the last one stopped, regardless of whether the same human or the same model is driving.

**Self-update paradox:** Updates to team member instruction files take effect immediately (they're read fresh each dispatch). Updates to the coordinator's own `.agent.md` file do NOT take effect until a new session loads it. For coordinator-level rules discovered mid-session, write them to the "Session-local rules" section of the progress file and consult it at each cycle start.

### 7. Review Gates

**Never fire-and-forget.** Draft artifacts should pass through review before being finalised. The review panel is itself composed of team members — the coordinator dispatches them like any other work.

A minimal review panel covers three concerns:

| Reviewer | Focus | Key question |
|----------|-------|-------------|
| **Generalizability** | Domain assumptions | "Does this work for projects unlike ours?" |
| **Testability** | Empirical grounding | "How would you know if this is working?" |
| **Autonomy** | Self-sufficiency | "What breaks if the human walks away?" |

**Review-pass criteria:** An artifact passes review when:
1. No reviewer assigns its worst-category verdict (DOMAIN-LOCKED, UNTESTABLE, or HUMAN-DEPENDENT)
2. All findings rated as blockers have been addressed in a subsequent revision
3. Remaining non-blocking findings are logged for future improvement but do not prevent finalisation

**Maximum iterations:** If after 3 review rounds an artifact still has blocking findings, finalise it with an explicit "Unresolved Findings" appendix listing what remains. This prevents death-spiral perfectionism while maintaining transparency.

**Contradictory feedback:** When reviewers contradict each other: (1) determine whether the contradiction is real or apparent (different scopes may look contradictory), (2) if real, prefer the reviewer whose concern is most relevant to the artifact's primary purpose, (3) document the trade-off explicitly in the artifact.

Not every artifact needs a full panel. Match review intensity to significance:

| Artifact significance | Review approach |
|----------------------|----------------|
| Minor fix, typo, formatting | Skip review or quick spot-check |
| New team member, updated convention | At least one reviewer (pick the most relevant) |
| New pattern, foundational infrastructure | Full panel |
| Architectural change affecting multiple artifacts | Full panel + iteration |

### 8. Spawn Subagents with Explicit Instruction References

Because embedded subagent instructions are not registered agents, the coordinator must explicitly tell each subagent to read its instruction file:

```markdown
Use the `task` tool with `agent_type: "general-purpose"` for each team member.

Prompt template:
"Read and follow the instructions in `.github/agents/research-team/members/<member>.md`.
Then perform the following task: {specific task description with full context}
Expected outcome: {what the member should produce and at what specificity}"

Always specify a model explicitly.

For read-only members (Review, Strategic, Advisory categories), add to the prompt:
"You are operating in a read-only advisory capacity. Do not edit any files.
Do not execute commands that modify state. Report your findings for the
coordinator to act on."
```

Provide each member with all the context they need — they start with zero shared state. If they need to read project files, tell them which files. If they need conventions, state them or point to the file.

### 9. Author Team Member Instruction Files

Each team member file follows a consistent structure:

```markdown
# [Member Name]

## Role
Who this team member is and what they specialise in.

## What You Do
- Specific tasks this member performs
- Types of questions they can answer

## What You Do NOT Do
- Explicit exclusions naming who else handles them
- "Don't do X — that's Y's job"

## Output Format
How to structure results so the coordinator can synthesise them.

## Working Method
Step-by-step approach for common tasks.
```

The "What You Do NOT Do" section is critical. Without it, members overlap — a reviewer starts editing files, an advisor starts making decisions. Every exclusion should name the member who *does* handle that concern.

Members should be **self-contained** — a subagent reading the file should have everything it needs without context from the coordinator beyond the specific task description.

### 10. Self-Updating Rules

The coordinator's instructions and team member files should include a self-updating clause:

> When you discover a useful pattern, workflow improvement, or lesson learned, update the relevant instruction file immediately. Rules should sediment from experience — every rule should trace to a specific failure mode.

This means:
- Team members' instruction files are refined based on observed performance
- Anti-patterns are explicitly blacklisted with "what went wrong" context (not just "don't do X" but "don't do X because Y happened when Z was tried")
- The coordinator writes session-local rules to `members/progress.md` (since its own `.agent.md` won't reload mid-session)

**Feedback loop integrity:** To verify that self-updating is actually working (not just accumulating arbitrary edits), periodically audit member files for: (1) rules that include provenance ("because X happened"), (2) contradictions between rules, (3) files that have never been updated since creation. During MAINTAIN, sample one existing rule and check whether the failure it prevents has recurred — if so, the rule needs strengthening or the root cause was elsewhere.

### 11. Maintain the Roster

The `README.md` roster is the coordinator's index of available expertise:

```markdown
# Team Roster

| Member | File | Category | Domain | Recruited For | Last Dispatched |
|--------|------|----------|--------|--------------|-----------------|
| Generalizability Reviewer | `generalizability-reviewer.md` | Review | Domain assumption critique | Artifact review panel | Cycle 3 |
```

The coordinator updates this file whenever it recruits a new member or dispatches an existing one. The "Last Dispatched" column enables staleness detection: if a member hasn't been dispatched in 3+ cycles, it's a candidate for archival.

**Archival procedure:** Remove the member from the roster's active table. Move the row to an "Archived" section in the README with a note on when and why. Leave the instruction file in place — it can be re-activated by moving it back to the active table. Do not delete instruction files; they represent institutional knowledge.

**Recruit-vs-reuse decision:** Before creating a new member, ask: "Could an existing member handle this with a tailored dispatch prompt?" If an existing member covers most of the need, dispatch it with specific instructions. Only recruit when the gap represents a fundamentally different specialism you expect to reuse.

## Gotchas

- **The coordinator must never do the work itself.** The strongest temptation is to "just quickly check this one thing." If no suitable team member exists, recruit one — don't fill the gap yourself. The only exception is trivially small coordination tasks (reading the roster, dispatching).
- **Never fire-and-forget artifacts.** A first draft is never the final version. Route drafts through review before finalising. This applies recursively — team member instruction files themselves should be reviewed before being relied upon for critical work.
- **Team members must be self-contained.** A subagent starts with no context. If a member's instruction file says "follow the project's conventions" without specifying what those are, the subagent will improvise. Include everything needed, or tell it which files to read.
- **Tool constraints for embedded members are prompt-level, not structural.** For `.agent.md` files, tool restrictions are enforced by the platform. For instruction files dispatched via `task`, the constraint exists only in the prompt. If a safety boundary is critical, promote the member to an `.agent.md` file. For most members, prompt-level constraints are sufficient.
- **Every rule should trace to a failure.** Don't prescribe rules prophylactically. When something goes wrong, codify the fix as a rule with context ("don't do X because Y happened"). Rules without provenance will be ignored or misapplied. Periodically audit for provenance — rules that can't explain themselves are candidates for removal.
- **Recruitment has overhead — don't over-recruit.** For a one-off question an existing member can answer, dispatch with a specific prompt rather than creating a hyper-specialised new member. If the roster exceeds ~15 members or more than 30% are unused in the last 3 cycles, consolidate or archive.
- **The roster can grow stale.** Periodically review and archive unused members during the MAINTAIN step. Members that haven't been dispatched in 3+ cycles are candidates. This isn't bureaucracy — a bloated roster slows every dispatch by forcing the coordinator to read more member summaries.
- **Synthesis is the coordinator's core value-add.** If the coordinator merely concatenates member outputs, it's not adding value. Genuine synthesis means: surfacing buried contradictions, identifying cross-cutting themes, producing conclusions not present in any individual report. Test this by asking: "Does the synthesis contain insights that no single member provided?"
- **Anti-perfectionism roles are load-bearing.** Advisory members that say "stop polishing, ship it" sound frivolous but prevent the "just one more revision" death spiral. Don't dismiss them.
- **Model selection matters per dispatch.** Deep analysis benefits from stronger reasoning models; routine tasks work with fast, cheap ones. The coordinator should make deliberate choices, not use the same model for everything.
- **Session boundaries are real.** The coordinator's `.agent.md` file is loaded at session start and doesn't change mid-session. Team member files are read fresh each dispatch and can be updated mid-session. Use the progress file for session-local coordinator rules that need to take effect immediately.

## Example

A product development team evaluating a new feature:

**Coordinator agent** receives: "Should we build a real-time collaboration feature?"

1. **Bootstraps** — no progress file; this is a fresh investigation
2. **Assesses** — needs expertise in market analysis, technical feasibility, user research, and competitive landscape
3. **Reviews roster** — empty or minimal; this is a new project area
4. **Recruits** — authors `market-analyst.md` (Strategic), `technical-feasibility.md` (Production), `user-researcher.md` (Production), `competitive-analyst.md` (Strategic). Verifies each file has required sections before proceeding.
5. **Dispatches** all four in parallel, each with an expected-outcome statement:
   - Market Analyst: "Analyse market demand for real-time collaboration in our product category. Expected outcome: demand assessment with supporting data, 3-5 key findings."
   - Technical Feasibility: "Assess engineering effort, architecture changes, and risks. Expected outcome: effort estimate (T-shirt size), risk inventory, go/no-go recommendation."
   - User Researcher: "Synthesise user feedback and support tickets related to collaboration pain points. Expected outcome: top 5 pain points ranked by frequency, with representative quotes."
   - Competitive Analyst: "Map competitors offering real-time collaboration. Expected outcome: feature comparison matrix, positioning implications."
6. **Triages results** — verifies all four produced substantive content addressing the assigned task
7. **Dispatches review panel** against the four reports — the Testability reviewer flags that the market analyst's demand claims lack evidence paths
8. **Synthesises** — produces a unified recommendation noting agreement (strong user demand, moderate engineering effort) and conflict (competitive analyst says "table stakes" while market analyst says "differentiator"), explicitly surfacing the contradiction
9. **Logs** — records cycle outcomes, decisions, and significance to `members/log.md`
10. **Retrospects** — notes the competitive analyst's instructions were too vague about how to assess positioning; refines the instruction file with "always assess whether the feature is a differentiator, table stakes, or irrelevant in each competitor's strategy"
