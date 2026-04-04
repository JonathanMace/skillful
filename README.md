# Skillful

A [Copilot CLI plugin](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-cli-plugins) that teaches agents how to build self-managing repositories using Copilot CLI's own extension points — skills, agents, hooks, instructions, and more.

## Install

```sh
copilot plugin install JonathanMace/skillful
```

Or install from a local clone:

```sh
copilot plugin install ./path/to/skillful
```

Verify it loaded:

```sh
copilot plugin list
```

## Skills

| Skill | What it does |
|---|---|
| **writing-skills** | Author reusable `SKILL.md` files that teach agents repeatable procedures and domain expertise. |
| **latex-report** | Produce LaTeX reports and PDF writeups with appropriate templates, modern fonts, and committed compiled PDFs. |
| **writing-plugins** | Package reusable skills, agents, hooks, and integrations into an installable Copilot CLI plugin. |
| **writing-custom-agents** | Author `.agent.md` profiles that give agents a focused role, model, and tool access — including orchestrating parallel subagents. |
| **writing-custom-instructions** | Author instruction files that enforce coding standards and workflow rules across all Copilot sessions. |
| **writing-hooks** | Author `hooks.json` files that run commands before or after agent actions for logging, guardrails, and automation. |
| **git-checkpoint** | Standardize a conflict-free git workflow for concurrent agents — branches, worktrees, commits, PRs, merges, and cleanup. |
| **agent-design-patterns** | Named design patterns for multi-agent coordination — reviewer panels, mentor constellations, ritual cadences, escalation ladders, and more. |
| **session-analysis** | Analyze Copilot CLI sessions — review agent behavior, audit tool usage, trace subagent lifecycles, and inspect token consumption. |

## Usage

Once installed, skills are automatically discovered by Copilot CLI. Ask the agent to perform a task that matches a skill and it will activate, or invoke one explicitly:

```
/skills list
/skills invoke writing-skills
```

## Structure

```
skillful/
├── plugin.json                        # Plugin manifest
└── skills/
    ├── agent-design-patterns/         # Multi-agent coordination patterns
    │   ├── SKILL.md
    │   └── patterns/*.md
    ├── git-checkpoint/                # Conflict-free git workflow
    │   └── SKILL.md
    ├── latex-report/                  # Author LaTeX reports and PDF writeups
    │   └── SKILL.md
    ├── session-analysis/              # Session retrospective analysis
    │   ├── SKILL.md
    │   └── scripts/session_analyzer.py
    ├── writing-plugins/               # Author plugin.json-based CLI plugins
    │   └── SKILL.md
    ├── writing-custom-agents/         # Author .agent.md files
    │   └── SKILL.md
    ├── writing-custom-instructions/   # Author copilot-instructions.md
    │   └── SKILL.md
    ├── writing-hooks/                 # Author hooks.json
    │   └── SKILL.md
    └── writing-skills/                # Author SKILL.md files
        └── SKILL.md
```

## Development

Most reusable authoring skills have a canonical source in `.github/skills/`, and the `skills/` directory at the repo root is the plugin-distributable copy. Some skills are intentionally maintained only in `skills/` when they belong to the distributable plugin surface rather than the repository's mirrored internal skill set (for example, `bootstrap-skillful` and `writing-plugins`). When updating a mirrored skill, edit the `.github/skills/` version and copy it to `skills/`.
