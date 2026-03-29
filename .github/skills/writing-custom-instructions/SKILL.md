---
name: writing-custom-instructions
description: >-
  Guide for authoring Copilot CLI custom instruction files including
  copilot-instructions.md, path-specific *.instructions.md files, and
  AGENTS.md. Use when asked to author custom instructions, configure
  copilot-instructions, set up repo instructions, or create AGENTS.md.
license: MIT
---

# Authoring Custom Instructions for GitHub Copilot CLI

Custom instructions are persistent natural-language guidance that Copilot CLI loads automatically at the start of every session. They tell Copilot **how to behave** — coding conventions, project context, communication preferences — without you repeating them in every prompt.

## Procedure: Authoring Custom Instructions

1. **Decide the instruction scope** — does this guidance apply to every task (repository-wide), only certain files (path-specific), or all agent-powered work (AGENTS.md)?
2. **Inspect existing instructions** — check for `.github/copilot-instructions.md`, `.github/instructions/`, and `AGENTS.md` to avoid contradictions.
3. **Choose the right file type** (see [Instruction Types](#instruction-types) below).
4. **Author the file** — write short, self-contained statements in Markdown. For path-specific files, add `applyTo` frontmatter.
5. **Prioritize critical rules first** — Copilot code review only reads the first 4,000 characters of instruction files.
6. **Review as if new to the repo** — re-read your instructions from the perspective of someone unfamiliar with the project. Each statement should stand alone without requiring external context.
7. **Test your instructions** — start a new CLI session (or use `/instructions` to verify they are active) and submit a prompt to confirm Copilot follows the guidance. If a rule is too specific for general use, extract it into a skill instead (see the `writing-skills` skill).

## Instruction Types

| Type | File Location | Scope |
|------|--------------|-------|
| **Repository-wide** | `.github/copilot-instructions.md` | All tasks in this repo |
| **Path-specific** | `.github/instructions/**/*.instructions.md` | Tasks involving files matching a glob pattern |
| **Agent instructions** | `AGENTS.md` at repo root | All agent tasks in this repo |
| **Local/personal** | `$HOME/.copilot/copilot-instructions.md` | All repos for this user |
| **Environment dirs** | Dirs listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` env var | Custom locations |

Copilot CLI also reads `CLAUDE.md` and `GEMINI.md` at the repo root.

### Precedence (highest to lowest)

1. Path-specific instructions (`.github/instructions/**/*.instructions.md`)
2. Repository-wide instructions (`.github/copilot-instructions.md`)
3. Agent instructions (`AGENTS.md`)
4. Local/personal instructions

All matching instructions are combined and provided to Copilot. Avoid conflicts between levels — conflicting instructions produce non-deterministic behavior.

## Repository-Wide Instructions

### File: `.github/copilot-instructions.md`

This is the primary instruction file. Its contents are sent with every prompt in this repo.

```markdown
# Project Guidelines

- Language: TypeScript in strict mode
- Formatter: Prettier with default config
- Linter: ESLint with @typescript-eslint
- Tests: Jest with React Testing Library
- Use early returns; avoid deep nesting
- Prefer named exports over default exports
```

### What to Include

- **Project overview** — purpose, architecture, key components
- **Tech stack** — languages, frameworks, libraries, versions
- **Coding standards** — naming conventions, formatting rules, patterns to prefer/avoid
- **Build and test commands** — how to build, lint, test
- **Folder structure** — key directories and their purposes

### What to Avoid

- Task-specific procedures (author a **skill** instead)
- References to external documents Copilot cannot access
- Instructions so lengthy they crowd out the actual user prompt
- Overly prescriptive style rules that conflict with varied tasks

## Path-Specific Instructions

### Location: `.github/instructions/**/*.instructions.md`

These files provide targeted guidance for specific parts of the codebase. They activate when Copilot is working on files that match the `applyTo` glob pattern.

### Format

```markdown
---
applyTo: "src/frontend/**/*.tsx"
---

- Use React function components with hooks
- Use Tailwind CSS for styling; avoid inline styles
- All components must have PropTypes or TypeScript interfaces
- Prefer composition over inheritance
```

### `applyTo` Glob Syntax

| Pattern | Matches |
|---------|---------|
| `*` | All files in current directory |
| `**` or `**/*` | All files recursively |
| `*.py` | `.py` files in current directory |
| `**/*.py` | `.py` files at any depth |
| `src/**/*.ts` | `.ts` files anywhere under `src/` |
| `**/*.ts,**/*.tsx` | Multiple patterns, comma-separated |

### Optional: `excludeAgent`

Restrict which Copilot agent sees the instructions:

```markdown
---
applyTo: "**"
excludeAgent: "code-review"
---

These instructions are only used by the coding agent, not code review.
```

Valid values: `"code-review"`, `"coding-agent"`.

### Organization Tips

```
.github/instructions/
├── frontend.instructions.md     # applyTo: "src/frontend/**"
├── backend.instructions.md      # applyTo: "src/api/**"
├── testing.instructions.md      # applyTo: "**/*.test.*,**/*.spec.*"
└── database/
    └── migrations.instructions.md  # applyTo: "**/migrations/**"
```

Name files descriptively. Use subdirectories to organize by domain.

## Agent Instructions (AGENTS.md)

### Location: Repository root, cwd, or `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` paths

`AGENTS.md` at the repository root is treated as **primary** agent instructions. Files in other locations are **additional** instructions (lower priority).

```markdown
# AGENTS.md

## Development Workflow

- Always create a feature branch; never commit directly to main
- Run `npm test` before committing
- Include a changelog entry for user-facing changes

## Code Review Standards

- All PRs require at least one approval
- Check for security implications in dependency updates
```

### When to Use AGENTS.md vs copilot-instructions.md

Both are loaded by Copilot CLI for every request, but:

- **`copilot-instructions.md`** is the Copilot-native format — use it as the default choice.
- **`AGENTS.md`** is also loaded by Copilot CLI and provides an alternative location for agent-focused instructions. Use it when you want to keep agent-specific workflow rules separate from general coding conventions.
- If both exist, both are used. Avoid contradictions between them.

## Local Instructions

### File: `$HOME/.copilot/copilot-instructions.md`

Personal instructions that apply to all your Copilot CLI sessions, regardless of repository. Useful for individual preferences:

```markdown
- Prefer concise explanations
- Always show the file path when editing files
- Use American English spelling
```

## CLI Commands for Instructions

| Command | Purpose |
|---------|---------|
| `/instructions` | View active instruction files and toggle them on/off |
| `/init` | Initialize Copilot instructions for a repository (creates starter files) |

## Best Practices for Authoring Instructions

1. **Keep instructions lean** — every instruction consumes context tokens on every prompt. Only include what is broadly relevant.
2. **Use path-specific files for specialized rules** — don't put frontend rules in the global file if they only matter for `.tsx` files.
3. **Avoid contradictions** — conflicting instructions across files produce unpredictable results.
4. **Put the most important rules first** — especially within `copilot-instructions.md`, since code review only reads the first 4,000 characters.
5. **Extract procedures into skills** — if you find yourself writing step-by-step task procedures in instructions, author a skill instead (see the `writing-skills` skill).
6. **Test your instructions** — after authoring or editing, start a new CLI session and verify Copilot follows the guidance.
7. **Commit and share** — repository instructions are version-controlled and shared across the team. Review changes to instructions like code changes.
