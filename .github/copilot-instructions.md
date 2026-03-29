This repository provides general-purpose Copilot CLI skills and agents that make common workflows more effective. The core problem: Copilot CLI agents don't know what Copilot CLI itself can do — they lack awareness of skills, hooks, agents, instructions, plugins, and other configuration mechanisms, and they have no expertise in using these features to build self-managing, self-sustaining repositories.

The skills and agents here fill that gap. They are both **provided** (as reusable knowledge) and **used** (applied within this repo itself).

## Repository Structure

- `.github/skills/` — Agent skills, each in its own subdirectory with a `SKILL.md`
- `.github/agents/` — Custom agent profiles (`.agent.md` files)
- `.github/copilot-instructions.md` — This file; repo-wide instructions

## Conventions

- Skills follow the official GitHub Copilot CLI SKILL.md format with YAML frontmatter (`name`, `description`, `license`)
- Skill names are lowercase with hyphens, matching their directory name
- All skills are self-contained and reference official GitHub documentation

## Concurrent Agents and Git Worktrees

Multiple agents may be running concurrently in this repository. Each agent must work in its own git worktree to avoid conflicts.

- **Worktree location**: Create worktrees in a sibling directory to the repository root (e.g., if the repo is at `~/Projects/skillful`, worktrees go in `~/Projects/skillful-worktrees/<branch-name>`).
- **Branch ownership**: Each agent is responsible for maintaining and tidying its own branch — keep it rebased or up-to-date as needed.
- **Default workflow**: When work is complete, agents should create a PR, squash-merge it, and delete both the local and remote branches afterward. Clean up the worktree when done.
- The user can override this workflow (e.g., skip the PR, leave the branch open, etc.).

## Subagent Model Requirements

When spawning subagents (via the `task` tool or any other delegation mechanism), you **must** explicitly specify a model. Use either `claude-opus-4.6` or `gpt-5.4` unless the user directs otherwise.

- This rule applies recursively — include it in subagent prompts so they also specify models when spawning their own subagents.
- The user can override this by choosing a specific model or by explicitly requesting the system default (i.e., no model specified).

## Skill Discovery

Before starting any task, check whether a relevant skill is available. Use `/skills list` or rely on auto-invocation to find skills that match the current task. Skills provide curated, task-specific guidance that produces better results than working from general knowledge alone.
