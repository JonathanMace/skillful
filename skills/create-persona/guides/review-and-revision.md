---
title: Review and Revision
summary: Audit the generated persona skill against writing-skills rules, local compliance checks when available, and the artifact-shape requirements until it passes.
trigger: Use after the persona skill and resources exist, or whenever you need to review or revise the generated persona skill for concision, compliance, and usefulness.
---

# Review and Revision

This guide covers the final quality pass. The generated persona skill should read like a good skill, not like a research memo.

## Procedure

1. **Inspect First** — read the generated `SKILL.md`, `resources/full-persona.md`, the worker reports in `resources/`, `writing-skills`, and any local skill-compliance checklist if the repo has one.
2. **Run a full structural audit** — if `tests/skill-compliance/checklist.md` or an equivalent local checklist exists, use it as the authoritative rubric. Otherwise derive the review from `writing-skills`. Check the full surface, not just a small subset:
   - frontmatter fields and naming
   - description length, trigger quality, and purpose-first wording
   - numbered procedure and inspect-first opening step
   - examples where appropriate
   - done criteria
   - repository conventions and tone
   - duplication vs. resource references
3. **Audit artifact behavior** — verify that:
   - the main `SKILL.md` stays concise and factual
   - the full persona lives in `resources/full-persona.md`
   - each research worker preserved a detailed findings report under `resources/`
   - worker reports read like durable findings rather than process logs
   - the resources include concrete cited examples that make the persona usable in later writing tasks
4. **Use a dedicated reviewer subagent** — dispatch a fresh reviewer in a separate context window with an explicit model. Have the reviewer write findings to `resources/review-and-revision.md`.
5. **Revise the generated skill and re-audit** — fix every meaningful issue, then re-run the same checklist until the generated persona skill passes cleanly.

## Prompt Template for the Persona Reviewer

```markdown
Generated skill path: <path-to-generated-persona-skill-directory>

Read the generated persona skill at `<path-to-generated-persona-skill-directory>/SKILL.md`
and the detailed synthesis at
`<path-to-generated-persona-skill-directory>/resources/full-persona.md`.

Also read the worker reports under
`<path-to-generated-persona-skill-directory>/resources/`.

Evaluate the generated skill against `writing-skills`. If the repository has a
local checklist such as `tests/skill-compliance/checklist.md`, use that as the
authoritative rubric and record PASS / NEEDS WORK / FAIL findings.

Check specifically for:
- purpose-first description
- trigger quality and description scope
- numbered procedure
- inspect-first opening step
- resource references instead of duplicated evidence
- done criteria
- concise, factual main `SKILL.md`
- `resources/full-persona.md` as the home of the full synthesis
- preserved worker reports under `resources/`
- reports written as durable findings rather than process logs
- concrete cited examples in the resources that make the persona operational

Write the findings and required revisions to
`resources/review-and-revision.md`.
```

## Rules and Constraints

- Do **not** treat a partial spot-check as enough; review the full checklist surface.
- Do **not** approve a verbose main `SKILL.md` just because the content is good.
- Do **not** ignore missing worker reports or missing concrete examples in the resources.
- Do **not** stop after critique alone; revise and re-audit until the generated skill passes.

## Done Criteria

- A dedicated reviewer subagent critiqued the generated persona skill
- The review used `writing-skills` and any local checklist that exists
- `resources/review-and-revision.md` records the findings and required fixes
- The generated skill was revised until no meaningful compliance or artifact-shape gaps remained
