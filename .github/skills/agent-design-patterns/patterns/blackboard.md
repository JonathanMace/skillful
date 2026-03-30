---
title: Blackboard (Shared Scratchpad)
summary: >-
  Multiple agents collaborate on a single evolving artifact through a structured
  shared file — the blackboard. Agents read the current state, contribute to
  their assigned section, and write back. The file's schema prevents conflicts,
  and git provides an audit trail. No coordinator synthesises; the artifact
  assembles itself through structured contributions.
trigger: >-
  Multi-agent collaboration on a single document or artifact where contributions
  span different domains and no single agent has the full picture, but a
  coordinator bottleneck is undesirable.
---

# Blackboard (Shared Scratchpad)

## What It Is

A **structured file** — the blackboard — that serves as the sole coordination mechanism between multiple agents collaborating on a single artifact. Each agent reads the current state of the blackboard, contributes to a designated section, and writes the file back. The blackboard's schema divides the artifact into sections with clear ownership conventions, so agents can contribute concurrently (or in sequenced turns) without overwriting each other's work. Git versioning provides a full audit trail of who wrote what and when.

The critical distinction from coordinator-based patterns (like the Research Team) is that **no agent synthesises**. In the Research Team, the coordinator receives all outputs, resolves conflicts, and produces a unified deliverable. The blackboard inverts this: the artifact *is* the deliverable, and it assembles itself through the cumulative contributions of specialist agents. An orchestrator still exists, but its role is thin — it dispatches agents and monitors convergence, not read and rewrite contributions. If the orchestrator starts rewriting sections, the pattern has collapsed into a coordinator pattern with extra file I/O.

What distinguishes the blackboard from the Multi-Reviewer Panel or Mentor Constellation is **read-write collaboration on a shared mutable artifact**. Reviewers produce independent assessments that a coordinator merges. Mentors route questions between each other. Blackboard agents directly modify a shared document — each contribution builds on and responds to the contributions already present.

## Why It Works

- **The file is the coordination mechanism** — agents don't need to communicate with each other or through a coordinator. They communicate through the artifact itself. Each agent reads the latest state, sees what others have contributed, and writes in context. This is how collaborative documents work in the real world — coauthors don't pass messages through an editor, they write into the shared document. To validate this claim, compare blackboard output quality to coordinator-synthesised output on the same task. If the blackboard produces equivalent or better artifacts with fewer coordinator interventions, the mechanism is working.
- **Section-level ownership prevents conflicts** — by assigning each agent to a specific section (or set of sections), the schema eliminates write conflicts without requiring distributed locking. Two agents can contribute to the same blackboard simultaneously if they write to different sections, or sequentially if they need to read each other's work.
- **Git provides a free audit trail** — every contribution is a commit. You can see which agent wrote which section, when it was written, and what changed between passes. If a contribution degrades the artifact, `git diff` reveals exactly what happened and `git revert` undoes it.
- **The artifact converges incrementally** — each pass brings the blackboard closer to completion. Early passes fill in skeletal content; later passes refine, cross-reference, and polish. The orchestrator can monitor convergence by checking whether sections are still changing — when the diff between passes falls below a concrete threshold (e.g., fewer than 5% of the document's words changed), the artifact is done.
- **Contributions are persistent across sessions** — because the blackboard is a file, it survives session boundaries. An agent that contributed in session 1 can be re-dispatched in session 2 to refine its section, and it will find its prior work intact.

## How to Implement

### 1. Design the Blackboard Schema

The blackboard file must have a **predictable structure** that agents can parse and modify without corrupting each other's sections. Use clear section delimiters — Markdown headings are the simplest choice.

Every blackboard needs three structural elements:

1. **A metadata header** — tracks the artifact's state (current pass number, which sections are complete, outstanding flags)
2. **Owned sections** — one per contributing agent, clearly delimited and labelled with the owner
3. **A cross-cutting section** — for observations that span multiple sections (contradictions, dependencies, open questions)

Example blackboard template:

```markdown
# Design Document: [Title]

## Metadata
- **Pass**: 1
- **Status**: In progress
- **Sections awaiting input**: Risk Analysis, Testing Strategy
- **Open flags**: None

## Problem Statement
<!-- Owner: problem-analyst -->
<!-- Status: draft | review | final -->

[Content contributed by the problem-analyst agent]

## Technical Approach
<!-- Owner: architect -->
<!-- Status: draft | review | final -->

[Content contributed by the architect agent]

## Risk Analysis
<!-- Owner: risk-analyst -->
<!-- Status: empty | draft | review | final -->

[Content contributed by the risk-analyst agent]

## Testing Strategy
<!-- Owner: test-strategist -->
<!-- Status: empty | draft | review | final -->

## Cross-Cutting Concerns
<!-- Owner: any (append-only) -->

- [Observations that span multiple sections]
- [Contradictions between sections]
- [Dependencies: "Section X assumes Y, but Section Z contradicts this"]
```

The template above uses software design sections and roles, but the pattern is domain-agnostic. **Roles depend on the task**: for a marketing campaign, the agents might be "audience-analyst", "creative-director", "budget-analyst", and "channel-strategist"; for event planning: "venue-coordinator", "logistics-planner", "budget-manager", and "communications-lead". Choose roles that map to the natural divisions of expertise in your domain.

Here is a domain-neutral template that works outside software:

```markdown
# Blackboard: [Title]

## Metadata
- **Pass**: 1
- **Status**: In progress
- **Sections awaiting input**: [list]
- **Open flags**: None

## Situation Assessment
<!-- Owner: [analyst-role] -->
<!-- Status: empty | draft | review | final -->

[Current state of affairs, constraints, and objectives]

## Proposed Response
<!-- Owner: [strategist-role] -->
<!-- Status: empty | draft | review | final -->

[Recommended plan of action]

## Risk Factors
<!-- Owner: [risk-role] -->
<!-- Status: empty | draft | review | final -->

[Threats, uncertainties, and mitigations]

## Validation Criteria
<!-- Owner: [evaluator-role] -->
<!-- Status: empty | draft | review | final -->

[How we will know the response succeeded]

## Cross-Cutting Concerns
<!-- Owner: any (append-only) -->

- [Observations that span multiple sections]
```

**Schema enforcement is the orchestrator's responsibility.** After each agent writes back, the orchestrator (or a validation step) must perform a structural check:

1. **All expected headings present** — no sections were deleted
2. **Headings in expected order** — no sections were reordered
3. **Content confined to assigned sections** — diff shows changes only between the agent's heading and the next heading
4. **Metadata status fields updated** — the contributing agent set its section's status comment

If any check fails, revert the commit and re-dispatch with a stricter prompt. **Validate that section ownership actually prevents conflicts** by tracking ownership violations across passes: if violations occur in more than 10% of passes, section boundaries need stronger enforcement (more explicit prompts, structural guards, or switching from concurrent to sequential dispatch).

### 2. Define the Turn Protocol

Agents can contribute to the blackboard either **sequentially** (one at a time, each reading the latest state) or **concurrently** (multiple agents writing to different sections simultaneously). Each approach has trade-offs:

| Protocol | How it works | Strengths | Risks |
|----------|-------------|-----------|-------|
| **Sequential turns** | Dispatch one agent at a time; each reads the full blackboard before writing | Zero conflict risk; each agent builds on all prior contributions | Slow — N agents require N serial dispatches |
| **Concurrent with section ownership** | Dispatch multiple agents simultaneously; each writes only to its owned section | Fast — parallel execution | Agents can't read each other's in-progress work; cross-references are stale |
| **Phased** | Concurrent within a phase, sequential between phases | Balances speed and coherence | Requires careful phase design |

**Sequential turns** are the safest default for Copilot CLI. Each dispatch uses the `task` tool synchronously — the agent reads the blackboard, writes its section, and returns. The orchestrator then dispatches the next agent.

**Phased execution** is the practical sweet spot for most blackboard collaborations:

```
Phase 1 (parallel): Problem Statement + Technical Approach
  → both agents write independently
Phase 2 (parallel): Risk Analysis + Testing Strategy
  → both agents read Phase 1 content before writing
Phase 3 (sequential): Cross-cutting review pass
  → one agent reads everything and populates the cross-cutting section
```

### 3. Establish Contribution Conventions

Every contribution must follow conventions that make the blackboard coherent rather than a pile of disconnected fragments. Define these in the blackboard template or in a separate conventions file:

**Attribution** — each contribution is marked with the contributing agent's identifier and the pass number:

```markdown
## Technical Approach
<!-- Owner: architect -->
<!-- Status: draft -->
<!-- Last modified: Pass 2 by architect -->
```

**Contribution modes** — agents must know whether they are expected to:
- **Fill** — write new content into an empty section
- **Refine** — improve existing content in their own section based on what other sections now say
- **Respond** — add content to the cross-cutting section in response to another agent's work
- **Flag** — mark a dependency or contradiction without resolving it

**The "needs input from" flag** — when an agent discovers that its section depends on information from another section that hasn't been written yet, it inserts a flag rather than guessing:

```markdown
## Risk Analysis
<!-- Owner: risk-analyst -->
<!-- Status: draft -->

### Technical Risks
- Latency under load depends on architecture choice.
  **[NEEDS INPUT: architect]** — Cannot assess scaling risk until
  Technical Approach specifies the data flow architecture.

### Business Risks
- Market timing risk is moderate given current competitive landscape.
```

The orchestrator scans for `[NEEDS INPUT: X]` flags after each pass and dispatches the named agent to address the dependency before the next pass.

### 4. Implement the Orchestrator as a Thin Scheduler

The orchestrator is **not a coordinator**. It does not read contributions, assess quality, resolve conflicts, or rewrite content. Its job is limited to:

1. **Initialise** — create the blackboard file from the template, filling in the title and section structure
2. **Dispatch** — send agents to contribute, providing the blackboard file path and their assignment
3. **Validate** — after each write-back, verify the schema is intact (expected headings present, no sections deleted)
4. **Monitor flags** — scan for `[NEEDS INPUT: X]` and `[CONTRADICTION]` markers; dispatch the appropriate agent
5. **Detect convergence** — compare the blackboard before and after a pass; when the diff is below a threshold, declare the artifact complete
6. **Commit** — after each pass, commit the blackboard to git with a message identifying the pass and contributing agents

```markdown
# In the orchestrator's prompt:

## Blackboard Protocol

You manage a shared blackboard file. You do NOT write content into the
blackboard yourself — you dispatch specialist agents who read and write it.

### Dispatch Template
For each agent, use the `task` tool:
  prompt: "Read the blackboard file at {path}. You own the '{section}' section.
  Read ALL other sections to understand the current state of the document.
  Then write your contribution to your section. Do not modify any other section.
  If you depend on information from another section that is missing, insert a
  [NEEDS INPUT: owner-name] flag. Write the updated file back to {path}."

### After Each Pass
1. Verify the blackboard schema is intact (structural check: headings present, ordered, content confined)
2. Commit the file: git add {path} && git commit -m "Pass N: {agents}"
3. Scan for [NEEDS INPUT] flags — dispatch the named agent next
4. Scan for [CONTRADICTION] flags — dispatch a resolution pass
5. Check the Cross-Cutting Concerns section — if the same concern has
   appeared for 2+ passes without being addressed, dispatch a dedicated
   resolution agent or escalate to the human
6. Compare with previous pass — if diff is minimal, consider convergence

### Convergence Criteria
The artifact is complete when:
- All sections have status "draft" or better (none are "empty")
- No [NEEDS INPUT] flags remain unresolved
- The diff between the last two passes is cosmetic only (formatting, not substance)
- OR a maximum pass count (default: 5) has been reached
```

### 5. Handle Conflicts and Corruption

Even with section-level ownership, things can go wrong. Plan for these failure modes:

**Schema corruption** — an agent rewrites the entire file instead of just its section. Mitigation: the orchestrator validates the schema after each write-back. If headings are missing or reordered, revert the commit (`git checkout HEAD~1 -- {path}`) and re-dispatch with a more explicit prompt emphasising "modify ONLY your section."

**Section boundary violation** — an agent edits a section it doesn't own. Mitigation: use `git diff` after each write-back to verify changes are confined to the expected section. If changes leak into other sections, revert and re-dispatch. Include a stern constraint in the dispatch prompt:

```markdown
CONSTRAINT: You own ONLY the "{section}" section. Do not modify any text
outside the "{section}" heading and the next heading. If you see problems
in other sections, note them in the Cross-Cutting Concerns section — do
not fix them directly.
```

**Stale reads under concurrent dispatch** — two agents dispatched concurrently both read the same blackboard state; the second to write back doesn't see the first's contributions. Mitigation: this is acceptable for owned sections (they write to different sections). For the cross-cutting section, use append-only semantics — agents add bullets, never delete or rewrite existing ones.

**Divergent contributions** — two agents in different sections make incompatible assumptions. Mitigation: this is not a bug — it's the pattern working correctly. The cross-cutting section exists precisely to surface these. A later pass dispatches an agent to resolve the contradiction, or the orchestrator flags it for human review.

### 6. Detect Convergence

The blackboard is "done" when further passes stop producing meaningful changes. Implement convergence detection with a combination of signals:

**Quantitative signals:**
- Section status: all sections are "draft" or "final" (none "empty")
- Flag count: zero unresolved `[NEEDS INPUT]` flags
- Diff size: the diff between pass N and pass N-1 is below a threshold (e.g., fewer than 10 changed lines, all formatting)
- **Word-count delta**: track the number of words changed per pass. Convergence threshold: if a pass changes fewer than 5% of the document's total words, consider the artifact converged
- Pass count: a maximum pass count (default: 5) prevents infinite refinement
- **Oscillation detection**: if word-count deltas are not monotonically decreasing after 3+ passes, the blackboard may be oscillating — agents are rewriting each other's contributions. Log a warning and consider switching to sequential dispatch or escalating to human review

**Qualitative signals (optional):**
- Dispatch a "convergence assessor" agent that reads the entire blackboard and reports whether it reads as a coherent document or a collection of disconnected fragments
- Check whether the cross-cutting section is growing (new contradictions being found) or stable (no new issues)

**Automated convergence protocol:**

The orchestrator should automate the stop decision rather than requiring human monitoring:

```
After each pass:
  1. Count unresolved flags → if > 0, dispatch resolution pass
  2. Compute diff from previous pass → measure word-count delta
  3. If 3 consecutive passes produce <5% content change AND flags are zero
     → auto-declare convergence and stop dispatching
  4. If passes oscillate (same sections change back and forth between passes)
     → log a warning and escalate to human review
  5. If pass count exceeds maximum → declare convergence with caveat
     ("Maximum passes reached; artifact may benefit from further refinement")
```

## Gotchas

- **Without section-level structure, agents overwrite each other's work.** A blackboard that is just a flat document with no section delimiters is a race condition. The first agent to write back wins; subsequent agents obliterate prior contributions. Section headings with ownership markers are not optional — they are the locking mechanism.
- **Agents that write without reading produce incoherent documents.** If the dispatch prompt says "write the Risk Analysis section" without saying "read ALL other sections first," the agent will produce a generic risk analysis disconnected from the problem statement and technical approach. The dispatch prompt must explicitly instruct agents to read the entire blackboard before writing their section.
- **The blackboard becomes a kitchen sink without schema enforcement.** Agents are helpful — they will add content wherever they think it belongs. Without a fixed schema that the orchestrator validates after each write-back, sections proliferate, headings mutate, and the structure degrades. Validate after every write.
- **Sequential dispatch is safe but slow; concurrent dispatch risks incoherence.** Pure sequential dispatch means N agents require N serial `task` calls — fine for 3 agents, painful for 8. Pure concurrent dispatch means agents can't reference each other's contributions. The phased approach (concurrent within a phase, sequential between phases) is almost always the right compromise.
- **An agent that modifies sections outside its assignment corrupts others' work.** Models want to be helpful. If the architect agent sees a problem in the risk analysis section, it will fix it — rewriting content the risk analyst hasn't contributed yet or contradicting the risk analyst's planned approach. The "do not modify other sections" constraint must be in the dispatch prompt, and the orchestrator must verify with `git diff` that changes are confined.
- **The pattern degrades to "coordinator with extra steps" if one agent does all the synthesis.** If the orchestrator starts reading contributions, judging quality, and rewriting sections, it has become a coordinator — and a slow one, because it's also managing file I/O. The orchestrator's job is dispatch, validate, and detect convergence. If synthesis is needed, dispatch a synthesis agent that contributes to the cross-cutting section, subject to the same rules as every other agent.
- **The cross-cutting section becomes a dumping ground without append-only discipline.** If agents can rewrite the cross-cutting section (deleting others' observations), it loses its value as a shared record. Make it append-only: agents add new bullets, never delete existing ones. The orchestrator can clean it up between passes if needed.
- **Convergence detection based on diff size alone misses semantic stagnation.** An agent that rewrites its section with different words but the same meaning produces a large diff that looks like progress. Combine diff-based detection with flag counting and, for important artifacts, a qualitative convergence assessment from a dedicated agent.
- **The blackboard file grows unwieldy after many passes.** Each pass may add content, flags, and cross-cutting observations. Without periodic cleanup, the file becomes too large for agents' context windows to handle effectively. The orchestrator should resolve and remove flags between passes, and compress the cross-cutting section when observations have been addressed.

## Example

A design document for a new API versioning strategy, assembled by four specialist agents contributing to a shared blackboard:

**Setup** — the orchestrator creates `docs/api-versioning-design.md` from the blackboard template with sections: Problem Statement, Technical Approach, Risk Analysis, Testing Strategy, and Cross-Cutting Concerns. It commits the empty template.

**Phase 1 (parallel):**
- **Problem Analyst** reads the (empty) blackboard. Writes the Problem Statement section: describes the current pain points, customer impact, and constraints. Sets section status to "draft."
- **Architect** reads the (empty) blackboard. Writes the Technical Approach section: proposes URL-based versioning with header negotiation fallback. Sets section status to "draft."
- Both agents are dispatched concurrently — they write to different sections, so no conflict.

**Phase 2 (parallel):**
- **Risk Analyst** reads the full blackboard (now has Problem Statement and Technical Approach). Writes the Risk Analysis section, noting: "URL-based versioning creates combinatorial explosion if more than 3 versions are active simultaneously." Inserts flag: `[NEEDS INPUT: architect]` — "What is the version retirement policy?" Sets section status to "draft."
- **Test Strategist** reads the full blackboard. Writes the Testing Strategy section, describing contract testing across version boundaries. Adds to Cross-Cutting Concerns: "Problem Statement mentions backward compatibility as a hard requirement, but Technical Approach doesn't address how breaking changes are communicated to consumers."

**Resolution pass (sequential):**
- Orchestrator detects `[NEEDS INPUT: architect]` in Risk Analysis. Re-dispatches the **Architect** to read the flag and add the version retirement policy to the Technical Approach section. The architect also reads the Cross-Cutting Concerns bullet and adds a "Breaking Change Protocol" subsection.

**Convergence pass (sequential):**
- Orchestrator re-dispatches all four agents for a refinement pass. Each reads the now-complete blackboard and refines their section in light of all other sections. The Risk Analyst removes the `[NEEDS INPUT]` flag (now resolved). The Test Strategist updates the contract testing approach to account for the retirement policy.
- Orchestrator compares the diff: changes are refinements (wording, cross-references), not structural. No flags remain. Declares convergence.

**Result**: a coherent design document where each section was written by a specialist, each specialist read and responded to the others' contributions, and the document assembled itself through structured collaboration — with no coordinator rewriting anyone's work.

---

### Event Planning Example (Non-Software)

A conference planning document assembled by four specialist agents contributing to a shared blackboard:

**Setup** — the orchestrator creates `plans/annual-conference.md` from the domain-neutral template with sections: Situation Assessment, Proposed Response, Risk Factors, Validation Criteria, and Cross-Cutting Concerns.

**Phase 1 (parallel):**
- **Venue Coordinator** writes the Situation Assessment: expected attendance of 500, three candidate cities, AV requirements, accessibility constraints. Status: "draft."
- **Logistics Planner** writes the Proposed Response: two-day agenda with keynotes, breakout sessions, and networking events. Includes catering and transport logistics. Status: "draft."

**Phase 2 (parallel):**
- **Budget Manager** reads the full blackboard. Writes Risk Factors: venue deposit timelines create cash-flow risk; catering costs exceed budget if attendance exceeds 450. Inserts flag: `[NEEDS INPUT: venue-coordinator]` — "What are cancellation penalties for each candidate city?"
- **Communications Lead** writes Validation Criteria: registration targets by milestone dates, speaker confirmation rate, sponsor commitment levels. Adds to Cross-Cutting Concerns: "Proposed Response assumes 500 attendees, but Situation Assessment lists this as an upper bound — planning should account for 350–500 range."

**Resolution and convergence** follow the same protocol as the software example: the orchestrator resolves flags, dispatches refinement passes, and declares convergence when the diff between passes becomes minimal.

The blackboard pattern works identically — only the section names, agent roles, and domain expertise change.
