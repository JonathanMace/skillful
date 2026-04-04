---
title: Artifact Shape
summary: Package the persona as a concise skill plus detailed supporting resources, with the full synthesis and every worker report preserved under resources/.
trigger: Use for scaffolding the persona skill directory, writing the concise SKILL.md, writing resources/full-persona.md, and formatting research reports.
---

# Artifact Shape

This guide defines what the generated persona skill should look like. The pattern is simple: **concise main skill, detailed resources beside it**.

## Procedure

1. **Inspect First** — read the surrounding repo's existing skill conventions, nearby skills, and any local style expectations before creating the persona skill.
2. **Default to a standard skill directory** — create a directory such as `.github/skills/<surname-firstname-persona>/` unless the user explicitly requires another location. Prefer a skill directory over a flat file so you can preserve `resources/`.
3. **Use this layout**:

   ```text
   .github/skills/
   └── <surname-firstname-persona>/
       ├── SKILL.md
       └── resources/
           ├── full-persona.md
           ├── identity-and-bibliography.md
           ├── publication-history.md
           ├── flagship-papers.md
           ├── paper-01.md
           ├── paper-02.md
           └── review-and-revision.md
   ```

4. **Write `resources/full-persona.md` before the main skill** — use `templates/full-persona-template.md` for the full synthesis of research interests, framing habits, voice, section moves, and limits.
5. **Preserve every research worker report under `resources/`** — use `templates/research-report-template.md` so each report captures durable findings rather than chat-only notes.
6. **Write the main `SKILL.md` last, and keep it concise** — use `templates/persona-skill-template.md`. The main skill should primarily capture:
   - core research interests and recurring problem areas
   - characteristic ways of framing problems, novelty, evidence, and significance
   - writing style, tone, structure, and section-level habits
   - clear do / don't guidance for future writing tasks
   - a resource map pointing to `resources/full-persona.md` and supporting reports

   If a detail is explanatory evidence rather than operational guidance, move it into `resources/` instead of bloating the main skill file.
7. **Make the resources operational, not merely descriptive** — include concrete cited examples of openings, significance claims, related-work moves, transition habits, and lexical patterns in `resources/full-persona.md` or the paper-reading reports. Keep those examples in the resources, not in the main `SKILL.md`.
8. **Update repo-wide instructions only when the persona is explicitly central** — if the persona is meant to represent the repository as a whole or the user's standing voice, add a brief pointer to the generated skill. Do not do this by default.

## Template Map

- `templates/persona-skill-template.md` — concise generated persona skill
- `templates/full-persona-template.md` — detailed synthesis for `resources/full-persona.md`
- `templates/research-report-template.md` — worker reports in `resources/`

## Rules and Constraints

- Do **not** let the generated `SKILL.md` turn into a long biographical memo.
- Do **not** bury the full persona in chat history instead of `resources/full-persona.md`.
- Do **not** omit the individual worker reports; preserving them is part of the artifact.
- Do **not** leave the persona abstract; concrete cited examples belong in the resources.
- Do **not** update `.github/copilot-instructions.md` unless the persona is intended to represent the user or repository more broadly.

## Done Criteria

- A generated skill directory was created with a concise `SKILL.md` and detailed `resources/`
- `resources/full-persona.md` captures the full synthesis of interests, framing, and writing style
- Each research worker produced a detailed report in `resources/`
- The main `SKILL.md` stays concise and factual, and points to the detailed resources
- The resources include concrete cited examples that make the persona operational
