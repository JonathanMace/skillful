# AGENTS.md

## Overview

This repository provides general-purpose Copilot CLI skills and agents — packaged as the [skillful](https://github.com/JonathanMace/skillful) plugin — that teach agents how to build self-managing, self-sustaining repositories.

## Agent Infrastructure

| Directory | Purpose |
|-----------|---------|
| `.github/agents/` | Custom agent profiles (`.agent.md` files) |
| `.github/skills/` | Reusable procedural knowledge (`SKILL.md` files) |
| `.github/instructions/` | Path-specific instruction files |
| `.github/hooks/` | Event hooks for agent actions |
| `.github/copilot-instructions.md` | Repository-wide instructions loaded in every session |

## Working with Agents

- Agents work in **dedicated git worktrees** to avoid conflicts when running concurrently
- All changes to the default branch must come through **pull requests**
- Agents must always specify the **model** when spawning subagents
- The `copilot-instructions.md` file serves as persistent cross-session memory — agents update it as they learn

## Getting Started

To work on this repository with Copilot CLI:

1. Install the skillful plugin: `/plugin install JonathanMace/skillful`
2. Check available skills: `/skills list`
3. Check available agents: `/agents list`
