---
name: review-document
description: >-
  Produce a critical second-pass review of a finished document by dispatching a
  fresh reviewer subagent with a task-specific identity and explicit feedback
  criteria. Use when reviewing Markdown, LaTeX, reports, proposals, READMEs,
  blog posts, or other written artifacts after drafting is complete.
license: MIT
---

# Reviewing a Finished Document Critically

Use this skill after a document already exists and you want a genuinely independent critique. The core idea is simple: do **not** review the document in the same context window that wrote it. Spawn a fresh subagent so the reviewer is not contaminated by the parent agent's drafting history, hidden assumptions, or intent.

For broader multi-angle review systems, see the `agent-design-patterns` skill and its `multi-reviewer-panel` pattern. For reusable reviewer personas, see `writing-custom-agents`.

## Procedure

1. **Inspect First** — read the finished document and any nearby rubric, brief, style guide, or acceptance criteria. Identify the document type, intended audience, stakes, and the kind of criticism that matters most.
2. **Decide whether one reviewer is enough** — for most documents, one strong reviewer subagent is the right default. If you need clearly separated perspectives such as audience fit, technical correctness, and standards compliance, switch to the `multi-reviewer-panel` pattern instead of asking one reviewer to do everything.
3. **Define the reviewer's identity** — give the subagent a concrete role tied to the document's domain and audience. Good identities are specific and slightly opinionated: "expert in FizzBuzz pedagogy," "skeptical conference reviewer for a LaTeX paper," "maintainer reviewing a README for first-time contributors," or "technical editor for an internal design memo." Avoid generic roles like "helpful reviewer."
4. **State the feedback you want** — tell the subagent exactly what to critique and how hard to push. Examples: factual errors, weak arguments, missing assumptions, confusing structure, unsupported claims, audience mismatch, missing examples, or overclaiming. Also state what the reviewer should *not* spend time on if you want focused feedback.
5. **Spawn a fresh subagent with explicit instructions** — use the `task` tool so the review happens in a separate context window, and specify the model explicitly. Tell the subagent that it did not write the document and should behave like an external critic, not a co-author trying to defend prior choices.
6. **Require a structured review** — ask for a review format that is easy to act on, such as overall verdict, major issues, minor issues, open questions, and recommended revisions. Prefer specific findings with evidence over vague impressions.
7. **Apply changes and re-review if needed** — revise the document based on the findings, then run the same reviewer again or a narrower follow-up reviewer if the first pass exposed a specific weakness.

## Reviewer Identity Patterns

Borrow the same kind of sharply scoped identities used in the `multi-reviewer-panel` pattern:

| Situation | Strong reviewer identity | Primary focus |
|-----------|--------------------------|---------------|
| Beginner tutorial | **Expert in FizzBuzz pedagogy** | Where novices will get lost, missing steps, misleading examples |
| Technical paper | **Skeptical LaTeX conference reviewer** | Claims, rigor, evidence, structure, missing citations |
| Project README | **Maintainer reviewing onboarding docs for first-time contributors** | Setup gaps, assumption leaks, task flow, user friction |
| Internal proposal | **Staff engineer pressure-testing a design memo** | Hidden assumptions, tradeoffs, operational risk |

The identity should change the reviewer's instincts. A good reviewer persona naturally notices the kinds of problems you care about.

## Prompt Template

Use a prompt shaped like this when dispatching the reviewer:

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
1. Overall verdict
2. Major issues
3. Minor issues
4. Specific revision recommendations
```

## Example Task Dispatch

```text
Use the task tool with:
- agent_type: general-purpose
- model: gpt-5.4
- description: "Reviewing document"

Prompt:
"Read `docs/fizzbuzz-tutorial.md`. You are an expert in FizzBuzz pedagogy
reviewing a completed tutorial for beginners. You did not help write it.
Give a critical review focused on conceptual correctness, missing steps,
confusing explanations, and weak examples. Do not spend time on superficial
copy edits. Return an overall verdict, major issues, minor issues, and
concrete revision recommendations."
```

For higher-stakes technical documents, use a stronger reviewer identity and a stronger model such as `claude-opus-4.6`.

## Rules and Constraints

- Do **not** ask the same context window that authored the document to "self-review" and treat that as independent critique.
- Do **not** give the reviewer a bland identity; specificity produces sharper feedback.
- Do **not** ask for "any feedback" with no focus. The quality of the review depends heavily on the scope you define.
- Do **not** mix critique and rewriting in the first pass unless the task explicitly calls for both. A reviewer who immediately rewrites often softens or skips the criticism you actually needed.
- If the document needs multiple non-overlapping perspectives, use separate reviewers rather than one overloaded generalist.

## Done Criteria

- The document has been read in its finished form
- A fresh subagent was used for the review
- The subagent had a task-specific identity tied to the document domain
- The prompt specified the kind of feedback desired and any out-of-scope areas
- The review output was structured enough to drive revisions
- Follow-up review was run if major issues were addressed
