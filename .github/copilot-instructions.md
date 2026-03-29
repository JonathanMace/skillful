This repository contains reusable Copilot CLI skills for authoring Copilot CLI customization artifacts — skills, custom instructions, custom agents, and hooks.

## Repository Structure

- `.github/skills/` — Agent skills, each in its own subdirectory with a `SKILL.md`
- `.github/copilot-instructions.md` — This file; repo-wide instructions

## Conventions

- Skills follow the official GitHub Copilot CLI SKILL.md format with YAML frontmatter (`name`, `description`, `license`)
- Skill names are lowercase with hyphens, matching their directory name
- All skills are self-contained and reference official GitHub documentation
