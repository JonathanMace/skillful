---
name: review-document
description: >-
  Produce a critical second-pass review of a finished document by dispatching a
  fresh reviewer subagent with a task-specific identity and explicit feedback
  criteria. Use when reviewing Markdown, LaTeX, reports, proposals, READMEs,
  specifications, design docs, blog posts, or other written artifacts after
  drafting is complete.
license: MIT
---

# Reviewing a Finished Document Critically

Use this skill after a document already exists and you want a genuinely independent critique. The core idea is simple: do **not** review the document in the same context window that wrote it. Spawn a fresh subagent so the reviewer is not contaminated by the parent agent's drafting history, hidden assumptions, or intent.

For broader multi-angle review systems, see the `agent-design-patterns` skill and its `multi-reviewer-panel` pattern. For reusable reviewer personas, see `writing-custom-agents`. If a persona artifact exists for the target audience or domain expert, see `create-persona` — persona-informed identities produce sharper reviewers.

## Procedure

1. **Inspect First** — read the finished document and any nearby rubric, brief, style guide, or acceptance criteria. Identify:
   - the document type and format (Markdown, LaTeX, prose, structured reference)
   - the intended audience and their assumed background
   - the stakes (internal note vs. published paper vs. public README)
   - the kind of criticism that matters most for this document
   - any existing persona artifacts, style guides, or checklists that should inform the review
2. **Decide whether one reviewer is enough** — for most documents, one strong reviewer subagent is the right default. Switch to the `multi-reviewer-panel` pattern from `agent-design-patterns` when you need clearly separated perspectives such as audience fit, technical correctness, and standards compliance rather than asking one reviewer to cover everything.
3. **Define the reviewer's identity** — give the subagent a concrete role tied to the document's domain and audience. Good identities are specific and slightly opinionated: "expert in FizzBuzz pedagogy," "skeptical conference reviewer for a LaTeX paper," "maintainer reviewing a README for first-time contributors," or "technical editor for an internal design memo." Avoid generic roles like "helpful reviewer." If a persona artifact exists for a relevant domain expert, use it to ground the reviewer identity.
4. **State the feedback you want** — tell the subagent exactly what to critique and how hard to push. Examples: factual errors, weak arguments, missing assumptions, confusing structure, unsupported claims, audience mismatch, missing examples, or overclaiming. Also state what the reviewer should *not* spend time on if you want focused feedback.
5. **Spawn a fresh subagent with explicit instructions** — use the `task` tool so the review happens in a separate context window. Always specify the model explicitly (see [Model Selection](#model-selection) below). The prompt must:
   - state the reviewer's identity and domain
   - declare that the reviewer did not write the document and should behave as an external critic
   - list the focus areas and any out-of-scope exclusions
   - specify the file path(s) to read
   - require a structured output format
6. **Require a structured review** — ask for a review format that is easy to act on:
   1. Overall verdict (accept / revise / rethink)
   2. Major issues (with evidence from the document)
   3. Minor issues
   4. Open questions the reviewer cannot resolve alone
   5. Specific revision recommendations

   Prefer specific findings with evidence over vague impressions. A review that says "the argument in §3 is weak because X is unsupported" is actionable; "could be improved" is not.
7. **Apply changes and re-review if needed** — revise the document based on the findings. Then decide:
   - **No major issues found** — done.
   - **Major issues addressed** — run the same reviewer again to verify the fixes landed.
   - **First pass exposed a specific weakness** — spawn a narrower follow-up reviewer scoped to that weakness (e.g., a technical-accuracy reviewer after a structural review).
   - **Diminishing returns** — stop iterating when the reviewer finds only minor issues or repeats previous feedback.

## Reviewer Identity Patterns

Borrow the same kind of sharply scoped identities used in `agent-design-patterns`:

| Situation | Strong reviewer identity | Primary focus |
|-----------|--------------------------|---------------|
| Beginner tutorial | **Expert in FizzBuzz pedagogy** | Where novices will get lost, missing steps, misleading examples |
| Technical paper | **Skeptical LaTeX conference reviewer** | Claims, rigor, evidence, structure, missing citations |
| Project README | **Maintainer reviewing onboarding docs for first-time contributors** | Setup gaps, assumption leaks, task flow, user friction |
| Internal proposal | **Staff engineer pressure-testing a design memo** | Hidden assumptions, tradeoffs, operational risk |
| Skill or agent definition | **Copilot CLI power user auditing a SKILL.md** | Compliance, trigger coverage, procedure clarity, done criteria |

The identity should change the reviewer's instincts. A good reviewer persona naturally notices the kinds of problems you care about.

## Model Selection

Choose the reviewer model based on the document's complexity and stakes:

| Document stakes | Recommended model | Rationale |
|-----------------|-------------------|-----------|
| Routine (internal notes, changelogs) | `gpt-5.4` | Fast, cost-effective, sufficient for structural review |
| Standard (READMEs, tutorials, proposals) | `gpt-5.4` or `claude-sonnet-4.6` | Good balance of depth and speed |
| High-stakes (papers, public reports, specs) | `claude-opus-4.6` | Strongest reasoning for nuanced critique |

Always specify the model explicitly when dispatching the reviewer subagent.

## Prompt Template

Use a prompt shaped like this when dispatching the reviewer. The template has five required components: identity, independence declaration, focus areas, exclusions, and structured output format.

```markdown
You are an expert in FizzBuzz pedagogy reviewing a completed Markdown tutorial.

You did not help write this document. Review it as an external critic.

Focus on:
- conceptual correctness
- where a beginner will get confused
- missing prerequisites or skipped steps
- whether the examples actually teach the concept

Do not focus on:
- minor copy edits that do not affect comprehension
- formatting nits unless they block understanding

Read `docs/fizzbuzz-tutorial.md` and produce:
1. Overall verdict (accept / revise / rethink)
2. Major issues (with evidence)
3. Minor issues
4. Open questions
5. Specific revision recommendations
```

## Example Task Dispatch

```text
Use the task tool in sync mode with explicit model:

  agent_type: general-purpose
  model:       gpt-5.4
  description: "Review fizzbuzz tutorial"
  prompt:      <see below>
```

```markdown
Read `docs/fizzbuzz-tutorial.md`. You are an expert in FizzBuzz pedagogy
reviewing a completed tutorial for beginners. You did not help write it.

Give a critical review focused on conceptual correctness, missing steps,
confusing explanations, and weak examples. Do not spend time on superficial
copy edits.

Return:
1. Overall verdict (accept / revise / rethink)
2. Major issues (cite specific sections or lines)
3. Minor issues
4. Open questions
5. Concrete revision recommendations
```

For higher-stakes technical documents, use a stronger reviewer identity and a stronger model such as `claude-opus-4.6`.

## Rules and Constraints

- Do **not** ask the same context window that authored the document to "self-review" and treat that as independent critique.
- Do **not** give the reviewer a bland identity; specificity produces sharper feedback.
- Do **not** ask for "any feedback" with no focus. The quality of the review depends heavily on the scope you define.
- Do **not** mix critique and rewriting in the first pass unless the task explicitly calls for both. A reviewer who immediately rewrites often softens or skips the criticism you actually needed.
- Do **not** omit the model when spawning the reviewer subagent.
- If the document needs multiple non-overlapping perspectives, use separate reviewers rather than one overloaded generalist.

## Done Criteria

- The document was read in its finished form before dispatching the reviewer
- A fresh subagent in a separate context window was used for the review
- The reviewer model was specified explicitly
- The subagent had a task-specific identity tied to the document domain
- The prompt specified focus areas, exclusions, and a structured output format
- The review output included an overall verdict, major issues, minor issues, open questions, and revision recommendations
- Revisions were applied based on review findings
- A follow-up review was run when major issues were addressed in revisions
