---
name: writing-skills
description: >-
  Skills give agents reusable, on-demand expertise they can invoke by name
  or that auto-activate from context.  Use this skill to author a SKILL.md,
  add agent skills, set up a .github/skills directory, or write skill
  instructions.
license: MIT
---

# Authoring Agent Skills for GitHub Copilot CLI

Agent skills are folders of instructions, scripts, and resources that Copilot loads on-demand to improve its performance on specialized tasks. Each skill is a self-contained directory with a `SKILL.md` file and optional supporting assets.

A well-authored skill should let a future contributor repeat the same workflow without relying on session history or tribal knowledge.

## Procedure: Authoring a Skill

1. **Decide whether a skill is the right mechanism** (see [When to Author a Skill](#when-to-author-a-skill-vs-other-customization) below).
2. **Inspect neighboring skills first** — if the repository already has skills in `.github/skills/`, match their frontmatter shape, tone, and structural conventions for consistency.
3. **Define the trigger before authoring** — articulate the kind of request or task that should cause Copilot to load this skill. This becomes your `description` field and sets the scope boundary for the entire skill.
4. **Choose a placement** — for Copilot CLI, prefer project-level (`.github/skills/`) or personal (`~/.copilot/skills/`).
5. **Create a directory** named in lowercase with hyphens (e.g., `github-actions-debugging`).
6. **Author the `SKILL.md`** — author YAML frontmatter (`name`, `description`, optional `license`) followed by a Markdown body with instructions. Keep the body narrowly scoped to the trigger you defined in step 3.
7. **Add supporting files** (optional) — scripts, templates, or examples in the skill directory.
8. **Review as if new to the repo** — re-read the skill from the perspective of someone who has never seen the repository. It should clearly explain when to use it, what steps to follow, what "done" looks like, and which related docs or validations must accompany the change.
9. **Test the skill** — run `/skills reload`, then prompt Copilot with a task that should trigger it. Verify it activates and produces good results.

## When to Author a Skill (vs Other Customization)

- **Author a skill** for repeatable, task-specific instructions that Copilot should only load when relevant (e.g., debugging CI failures, generating tests, reviewing PRs).
- **Author custom instructions** (`.github/copilot-instructions.md`) for broad, always-on guidance like coding standards that apply to every task (see the `writing-custom-instructions` skill).
- **Author a custom agent** (`.agent.md`) when you need a specialized persona with constrained tools or a distinct approach (see the `writing-custom-agents` skill).

Skills are the right choice when you want "just-in-time" expertise without permanently enlarging the context window.

## Directory Structure

```
.github/skills/
└── my-skill-name/
    ├── SKILL.md              # Required — skill definition
    ├── scripts/              # Optional — helper scripts
    │   └── run-checks.sh
    └── templates/            # Optional — templates, examples
        └── checklist.md
```

### Placement Options

| Scope | Location |
|-------|----------|
| **Project skills** (single repo) | `.github/skills/` in repo root |
| **Personal skills** (all repos) | `~/.copilot/skills/` in your home directory |

Copilot CLI can also read `.claude/skills/`, `.agents/skills/`, and their home-directory equivalents for compatibility. For Copilot-focused repositories, prefer `.github/skills/` and `~/.copilot/skills/`.

### Naming Rules

- Directory name: **lowercase, hyphens for spaces** (e.g., `github-actions-debugging`)
- The directory name should match the `name` field in the YAML frontmatter
- Use descriptive, specific names that convey the skill's purpose

## SKILL.md Format

Every skill requires a `SKILL.md` file (the filename must be exactly `SKILL.md`). It consists of **YAML frontmatter** followed by a **Markdown body**.

### YAML Frontmatter

```yaml
---
name: my-skill-name
description: >-
  Guide for authoring release notes with a consistent structure and
  repository-specific checks. Use when drafting release notes, changelog
  entries, or release summaries.
license: MIT
---
```

Include `license` only when you want to declare the license for the skill; otherwise omit it.

| Property | Required | Description |
|----------|----------|-------------|
| `name` | **Yes** | Unique identifier. Lowercase, hyphens for spaces. It should match the directory name, and in this repo you should keep them identical. |
| `description` | **Yes** | Explains what the skill does AND when to use it. This is critical — Copilot matches user prompts against this text to decide whether to load the skill. |
| `license` | No | License that applies to the skill. |

### Writing an Effective Description

The `description` is the single most important field. Copilot uses it to decide when to auto-invoke the skill. Follow these guidelines:

1. **Lead with the outcome** — say what the skill helps Copilot accomplish, not what skills are in general.
2. **State when to use it** — include trigger phrases and keywords that users would naturally type.
3. **Be specific** — vague descriptions cause false matches or missed invocations.
4. **Keep it concise** — 1–3 short sentences is usually enough.

**Good examples:**

```yaml
description: >-
  Guide for debugging failing GitHub Actions workflows. Use when asked
  to debug, fix, or investigate CI/CD failures, broken builds, or
  failing GitHub Actions.
```

```yaml
description: >-
  Guide for authoring and reviewing pull request descriptions.
  Use when creating PRs, drafting PR summaries, or improving
  PR documentation.
```

**Bad examples:**

```yaml
# Too vague — when would Copilot use this?
description: Helps with code stuff.

# Too narrow — misses many valid prompts
description: Use only when user types exactly "run the test helper".
```

### Markdown Body

The body contains the actual instructions Copilot will follow when the skill is loaded. Author these instructions as if you are onboarding a skilled developer who has never seen your project.

**Structure your instructions with:**

1. **Context** — brief background on what the skill addresses
2. **Step-by-step procedure** — numbered steps Copilot should follow
3. **Rules and constraints** — what to do and what to avoid
4. **Cross-references** — call out related agents, docs, hooks, or other skills rather than duplicating their content
5. **Examples** — concrete input/output samples when helpful
6. **Done criteria** — what "done" looks like, including any validation or documentation steps

The instructions should tell Copilot what to do, when to use supporting files, and how to recognize completion without relying on session history.

For **procedural skills** (e.g., "debug CI failures"), use a numbered step-by-step workflow. For **reference skills** (e.g., "how to author X"), organize by topic with sections and tables, but still include a top-level procedure summarizing the authoring workflow.

Prefer cross-references over duplication — link to the durable doc, agent, or skill that owns deeper context instead of embedding long background sections.

```markdown
---
name: github-actions-failure-debugging
description: >-
  Guide for debugging failing GitHub Actions workflows. Use when asked
  to debug failing GitHub Actions workflows.
---

To debug failing GitHub Actions workflows, follow this process:

1. Use `list_workflow_runs` to look up recent workflow runs and their status
2. Use `summarize_job_log_failures` to get an AI summary of the failure logs
3. If more detail is needed, use `get_job_logs` for full logs
4. Try to reproduce the failure locally
5. Fix the failing build and verify the fix before committing
```

## Referencing Supporting Files

You can include scripts, templates, and other assets in the skill directory and reference them in the instructions. Reference them by relative path and explain when Copilot should use them:

```markdown
When creating a new test file, use the template at `templates/test-template.md`
as a starting point.

To run the validation checks, execute `scripts/validate.sh` from the skill
directory.
```

Copilot can read and execute files within the skill directory when instructed to do so.

## How Skills Are Invoked (Context for Authors)

Understanding how skills are invoked helps you author better descriptions and instructions.

### Automatic Invocation

Copilot automatically loads a skill when it determines the skill is relevant to the current task, based on the skill's `description` matching the user's prompt. When that happens, the `SKILL.md` body is added to the agent's context. This is why the `description` field is critical — it controls discoverability, while the body supplies the working instructions.

### Manual Invocation

Users can invoke a skill explicitly by prefixing its name with `/` in their prompt:

```
Use the /github-actions-failure-debugging skill to fix the CI failures.
```

### Skills Management Commands

| Command | Purpose |
|---------|---------|
| `/skills list` | List all available skills |
| `/skills` | Toggle skills on/off interactively |
| `/skills info` | View detailed info about a skill (including location) |
| `/skills reload` | Reload skills without restarting the CLI |
| `/skills add` | Add an alternative skills directory |
| `/skills remove SKILL-DIR` | Remove a directly-added skill |

## Best Practices for Authoring Skills

1. **One skill per task domain** — keep skills focused and modular.
2. **Define the trigger first** — articulate what kind of request should load this skill before writing the body. The body should be narrowly scoped to that trigger.
3. **Author for auto-discovery** — invest effort in the `description` field so Copilot reliably finds your skill when needed.
4. **Prefer cross-references over duplication** — link to related agents, docs, hooks, or other skills that own deeper context rather than embedding long background sections.
5. **Prefer skills over bloated instructions** — move task-specific guidance out of `copilot-instructions.md` and into skills to keep the base context lean.
6. **Include concrete examples** — Copilot performs better when instructions include examples of expected behavior.
7. **Test your skill** — after authoring a skill, run `/skills reload`, then try both a natural prompt that should auto-invoke the skill and an explicit `/skill-name` prompt. Verify it activates and produces good results.
8. **Keep instructions actionable** — author numbered steps, not vague aspirations. Tell Copilot what to do, what to check, and when to use supporting files.
9. **Match existing conventions** — if the repository already has skills, match their tone, frontmatter shape, and structural patterns.
10. **Reference scripts for complex logic** — if a procedure involves complex shell commands or multi-step automation, include a script in the skill directory rather than embedding long code blocks in the Markdown.
11. **Consider packaging as a plugin** — if you want to distribute a collection of skills (plus agents, hooks, and MCP configs), package them as a plugin for easy installation via `/plugin install`.
