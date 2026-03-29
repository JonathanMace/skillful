# Repository Initialization Checklist

Things to do when setting up a new project or repository.

- [ ] **Protect the main branch** — Configure branch protection rules so that all changes must be merged via pull requests. No direct commits to `main`.
- [ ] **Add or update copilot instructions** — Ensure `.github/copilot-instructions.md` exists and incorporates the conventions from this repository's instructions (worktree rules, subagent model requirements, default execution strategy, skill discovery, purpose-first descriptions).
- [ ] **Set up a git-checkpoint workflow** — Either install the `git-checkpoint` skill or define equivalent branch → PR → merge → cleanup conventions so agents follow a consistent git lifecycle.
- [ ] **Define structured output expectations** — Agents should specify their output format. Add output template requirements to any custom agents.
- [ ] **Add a self-updating clause to instructions** — Include a rule like "If you discover a useful pattern, add it to this file immediately" so instruction files grow organically from real usage.
