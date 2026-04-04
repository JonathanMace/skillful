---
name: create-persona
description: >-
  Create a research-writing persona skill by deeply studying a specific
  person's publication record, flagship papers, venues, and stylistic patterns,
  then packaging the findings as a concise reusable skill with detailed
  supporting resources. Use when creating a persona for the user, a recurring
  author, an advisor, or another researcher whose voice should shape future
  writing in the repo.
license: MIT
---

# Creating a Research Persona Skill

Use this skill when the repository should learn how a specific researcher tends to think, argue, structure papers, and sound on the page. The deliverable is a **concise persona skill** backed by a **detailed `resources/` directory**, not a long memo stuffed into one `SKILL.md`.

For literature-search methodology, see `related-work`. For multi-agent orchestration, see `agent-design-patterns` and its `research-team` pattern. For final critique of the generated artifact, see `review-document`. For the rules the generated persona skill must satisfy, see `writing-skills`.

## Procedure

1. **Inspect First** — read the request and identify the target person, scope, existing persona materials, intended skill location, and whether the persona is meant for broad repo identity or narrower task-specific use.
2. **Use `guides/research-workflow.md` for evidence gathering** — it covers identity resolution, publication mapping, flagship-paper selection, paper-reading assignments, and report-first subagent orchestration.
3. **Use `guides/artifact-shape.md` for the generated deliverable** — it defines the scaffold, the concise generated `SKILL.md`, `resources/full-persona.md`, preserved worker reports, and the templates that shape those files.
4. **Use `guides/review-and-revision.md` for the final quality pass** — it covers the checklist-driven audit, reviewer-subagent prompt, and revision loop for the generated persona skill.

## Companion Files

| File | Use it for |
|------|------------|
| `guides/research-workflow.md` | Evidence gathering, paper reading, and research subagent coordination |
| `guides/artifact-shape.md` | Final persona skill layout, `resources/` contents, and template selection |
| `guides/review-and-revision.md` | Checklist-driven audit, reviewer prompt, and revision loop |
| `templates/persona-skill-template.md` | Concise generated persona `SKILL.md` |
| `templates/full-persona-template.md` | Detailed `resources/full-persona.md` synthesis |
| `templates/research-report-template.md` | Individual research-worker reports under `resources/` |

## Done Criteria

- The relevant guide or guides were followed for the task
- The generated persona is a skill directory with a concise `SKILL.md` and detailed `resources/`
- `resources/full-persona.md` contains the full persona synthesis
- Each research worker preserved a detailed findings report under `resources/`
- The finished persona skill passed review and revision against `writing-skills` and any local compliance checklist that exists
