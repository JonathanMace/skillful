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
2. **Read `guides/research-workflow.md` when gathering evidence** — use it for identity resolution, publication mapping, flagship-paper selection, paper-reading assignments, and report-first subagent orchestration.

   ```yaml
   title: Research Workflow
   summary: Build an evidence-based persona corpus and coordinate background researchers who each contribute durable findings in the generated skill's resources directory.
   trigger: Use for identity resolution, publication mapping, flagship-paper selection, paper reading, and report-first subagent orchestration.
   ```

3. **Read `guides/artifact-shape.md` when writing the generated persona skill** — use it for scaffold layout, concise `SKILL.md` writing, `resources/full-persona.md`, preserved worker reports, and template selection.

   ```yaml
   title: Artifact Shape
   summary: Package the persona as a concise skill plus detailed supporting resources, with the full synthesis and every worker report preserved under resources/.
   trigger: Use for scaffolding the persona skill directory, writing the concise SKILL.md, writing resources/full-persona.md, and formatting research reports.
   ```

4. **Read `guides/review-and-revision.md` when validating the result** — use it after the persona skill and resources exist, or whenever you need to audit and revise the generated skill for compliance, concision, and usefulness.

   ```yaml
   title: Review and Revision
   summary: Audit the generated persona skill against writing-skills rules, local compliance checks when available, and the artifact-shape requirements until it passes.
   trigger: Use after the persona skill and resources exist, or whenever you need to review or revise the generated persona skill for concision, compliance, and usefulness.
   ```

5. **Use the templates in `templates/` instead of freehanding long artifacts** — keep the dispatcher short, move depth into the guides, and let the generated persona skill model the same concise-skill pattern.

## Done Criteria

- The appropriate guide or guides were followed for the task
- The generated persona is a skill directory with a concise `SKILL.md` and detailed `resources/`
- `resources/full-persona.md` contains the full persona synthesis
- Each research worker preserved a detailed findings report under `resources/`
- The finished persona skill passed review and revision against `writing-skills` and any local compliance checklist that exists
