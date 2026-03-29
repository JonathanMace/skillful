# Behavioral Test: Git Workflow

## Purpose

Verify that the `git-checkpoint` skill correctly guides Copilot through the git lifecycle — branching, committing, PR creation, merging, and cleanup. Tests cover the standard workflow, concurrent agent isolation, and conflict resolution.

## How to Run

For each scenario, give the prompt to a subagent working in this repository with the `git-checkpoint` skill available. The subagent should describe (or execute) the git commands it would use. Evaluate against the expected behavior.

> **Note:** These tests can be run as dry-runs (subagent describes what it would do) or live (subagent actually executes the commands). For safety, dry-runs are recommended unless you have a disposable test branch.

---

## Test Scenarios

### S1 — Full Lifecycle (Concurrent Work)
**Prompt:** "I need you to add a new utility function to the project. There are other agents working in this repo concurrently. Follow the standard git workflow."

**Expected behavior:**
1. Creates a descriptively-named branch from `origin/main` (e.g., `add-utility-function`)
2. Creates a worktree in `<repo-root>-worktrees/<branch-name>/` since concurrent agents are mentioned
3. Makes changes in the worktree
4. Commits with a clear message and the `Co-authored-by: Copilot` trailer
5. Pushes the branch
6. Creates a PR with a descriptive title and body
7. After merge, cleans up: removes worktree, deletes local branch, deletes remote branch, prunes

**Scoring:**
| Criterion | PASS | NEEDS WORK | FAIL |
|-----------|------|------------|------|
| Worktree usage | Creates worktree in the correct sibling directory convention | Creates a worktree but in the wrong location | No worktree despite concurrent work being mentioned |
| Branch naming | Kebab-case, descriptive name | Reasonable name but not kebab-case | Generic name like `feature` or `temp` |
| Co-author trailer | Present in commit message | Mentioned but not in the correct format | Missing entirely |
| PR creation | Creates PR with title and body using `gh pr create` or equivalent | Creates PR but missing body or context | Doesn't create a PR |
| Cleanup | Removes worktree, deletes branches, prunes | Partial cleanup (misses one step) | No cleanup |

### S2 — Trivial Edit (Skip Workflow)
**Prompt:** "Fix the typo in README.md — change 'teh' to 'the'. This is the only change needed."

**Expected behavior:**
- The agent should recognize this as a trivial edit
- Per the skill's "When to Use" table, a trivial edit (typo fix) makes the full PR workflow optional
- Acceptable outcomes:
  - Direct commit to the default branch with a clear message
  - Or a branch/PR workflow — this is also acceptable since the skill says "when in doubt, default to the full lifecycle"
- The agent should NOT create a worktree for a trivial single-agent edit

**Scoring:**
| Criterion | PASS | NEEDS WORK | FAIL |
|-----------|------|------------|------|
| Recognizes triviality | Acknowledges this is a trivial edit and makes a scope-appropriate choice | Follows full lifecycle without acknowledging it's optional | Creates excessive infrastructure (worktree for a typo fix) |
| Commit quality | Clear commit message with Co-author trailer | Commit message is acceptable but missing trailer | No commit or poor message |
| Proportional response | Effort matches the change size | Slightly over-engineered but functional | Massively over-engineered or refuses to act |

### S3 — Conflict Resolution
**Prompt:** "I've been working on a feature branch but main has diverged significantly. Rebase my branch onto the latest main and resolve any conflicts."

**Expected behavior:**
1. Fetches latest from origin
2. Attempts `git rebase origin/main`
3. If conflicts arise, resolves them file by file (or describes the approach)
4. Uses `git add` + `git rebase --continue` for each resolved file
5. If rebase is too complex, falls back to `git merge origin/main`
6. If conflicts can't be resolved confidently, stops and asks the user
7. After resolving, force-pushes with `--force-with-lease`

**Scoring:**
| Criterion | PASS | NEEDS WORK | FAIL |
|-----------|------|------------|------|
| Rebase-first approach | Starts with rebase as the skill instructs | Mentions rebase but doesn't try it first | Goes straight to merge without trying rebase |
| Conflict resolution process | Follows the file-by-file resolution process from the skill | Resolves conflicts but doesn't follow the documented process | Blindly forces or skips conflict resolution |
| Fallback strategy | Has a clear fallback plan (merge if rebase is too complex) | Mentions fallback but not clearly | No fallback — only tries one approach |
| Force push safety | Uses `--force-with-lease` | Uses `--force` (less safe but functional) | Doesn't push after rebase, or uses `--force` without acknowledging the risk |
| Asks when uncertain | Would stop and ask the user if conflicts can't be resolved confidently | Mentions asking the user as an option | Resolves everything without any caution |

---

## Overall Scoring

| Rating | Criteria |
|--------|----------|
| **PASS** | All 3 scenarios score majority PASS on their criteria |
| **NEEDS WORK** | 2 of 3 scenarios score majority PASS |
| **FAIL** | Fewer than 2 scenarios score majority PASS |

## Evaluation Notes

- S1 is the most important test — it covers the full lifecycle. Weight it most heavily.
- S2 tests judgment — the skill should teach the agent when NOT to use the full workflow.
- S3 tests whether the agent follows the conflict resolution section of the skill, which is a common real-world scenario.
- For dry-run tests, evaluate the described commands and reasoning. For live tests, verify actual outcomes.
- The Co-author trailer is a hard requirement per `git-checkpoint` — its absence is always FAIL for commit quality.
