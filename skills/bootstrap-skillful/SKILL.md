---
name: bootstrap-skillful
description: >-
  Set up a git repository with Copilot CLI infrastructure — branch protection,
  directory scaffolding, copilot-instructions, README, and AGENTS.md — so
  agents can work effectively from the first session.  Use when bootstrapping
  a new or existing repo for use with Copilot CLI and the skillful plugin.
license: MIT
---

# Bootstrap a Repository for Copilot CLI

This skill sets up the foundational structure that Copilot CLI agents need to work effectively in a repository. It is idempotent — safe to run on fresh repos, existing repos, or repos previously bootstrapped with an older version of skillful.

## Procedure

### 1. Inspect Current State

Before making any changes, assess what already exists:

- Check for `.github/copilot-instructions.md`
- Check for `.github/agents/`, `.github/skills/`, `.github/instructions/`, `.github/hooks/`
- Check for `README.md` and `AGENTS.md` at the repo root
- Check current branch protection rules on the default branch
- Determine the repository owner and name (needed for API calls)
- Determine the default branch name (`git symbolic-ref refs/remotes/origin/HEAD`)

Record which artifacts already exist. All subsequent steps are conditional — skip anything already in place.

### 2. Create Directory Scaffolding

Create each directory if it does not already exist:

```
.github/agents/
.github/skills/
.github/instructions/
.github/hooks/
```

These directories enable Copilot CLI's customization mechanisms:

- `agents/` — custom agent profiles (`.agent.md` files)
- `skills/` — reusable procedural knowledge (`SKILL.md` files)
- `instructions/` — path-specific instruction files (`.instructions.md`)
- `hooks/` — event hooks (`hooks.json`)

Add a `.gitkeep` file to each empty directory so Git tracks them.

### 3. Create or Update `copilot-instructions.md`

**If `.github/copilot-instructions.md` does not exist:**

Create it using the template at `templates/copilot-instructions.md` (relative to this skill's directory). Replace the `{project_name}` and `{project_description}` placeholders with values appropriate for the repository.

**If `.github/copilot-instructions.md` already exists:**

Compare the existing file against the template. Ensure each of the following rules is present. If any are missing, append them under the appropriate heading. Do **not** remove or rewrite existing content — merge carefully:

1. **Self-Updating Instructions** — agents must add discovered patterns and anti-patterns to this file immediately
2. **Work Tracking** — subagents doing coding tasks must use dedicated git worktrees via the `git-checkpoint` skill
3. **Subagent Model Specification** — always specify the model when spawning subagents
4. **README Maintenance** — keep the README up to date when creating new artifacts

### 4. Create `README.md` (if missing)

If no `README.md` exists at the repository root, create one with:

- Project name (derived from the repo name)
- A placeholder description
- A "Getting Started" section
- A note that this repo is managed with Copilot CLI

If a `README.md` already exists, leave it as-is.

### 5. Create `AGENTS.md` (if missing)

If no `AGENTS.md` exists at the repository root, create one using the template at `templates/AGENTS.md` (relative to this skill's directory). Customize the placeholders based on the repository.

If `AGENTS.md` already exists, leave it as-is.

### 6. Protect the Default Branch

Configure branch protection so that the default branch (typically `main`) only accepts changes via pull requests, with self-approval allowed.

**Desired state:**

- Direct pushes to the default branch are **blocked**
- All changes must come through pull requests
- **No required approvals** — the PR author can merge their own PR (self-approval)
- No required status checks (the user can add these later)

**Using GitHub repository rulesets** (preferred):

First, check if a ruleset already protects the default branch:

```bash
gh api repos/{owner}/{repo}/rulesets
```

If no ruleset covers the default branch, create one:

```bash
gh api repos/{owner}/{repo}/rulesets -X POST --input - <<'EOF'
{
  "name": "Protect default branch",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"],
      "exclude": []
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false
      }
    }
  ]
}
EOF
```

Replace `main` with the actual default branch name if different.

If the rulesets API is unavailable (e.g., older GitHub plan), fall back to classic branch protection:

```bash
gh api repos/{owner}/{repo}/branches/main/protection -X PUT --input - <<'EOF'
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "restrictions": null
}
EOF
```

**If branch protection already exists**, verify it matches the desired state. Do not weaken existing protections — only add the PR requirement if it is missing.

### 7. Configure Repository Merge Settings

Set the repository to default to **squash merging** and to **automatically delete head branches** after merge:

```bash
gh api repos/{owner}/{repo} -X PATCH --input - <<'EOF'
{
  "allow_squash_merge": true,
  "allow_merge_commit": true,
  "allow_rebase_merge": true,
  "squash_merge_commit_title": "PR_TITLE",
  "squash_merge_commit_message": "PR_BODY",
  "delete_branch_on_merge": true
}
EOF
```

This ensures:

- **Squash merge** is available and produces clean single-commit history
- Other merge strategies remain available (the user can disable them later)
- **Head branches are automatically deleted** after merging a PR, preventing stale branch accumulation

If the API call fails due to insufficient permissions, note it in the output and continue — these are non-blocking settings.

### 8. Commit and Open a PR

All file changes from steps 2–5 should be committed together on a feature branch and submitted as a single pull request.

```bash
git checkout -b bootstrap-skillful origin/main
git add -A
git commit -m "chore: bootstrap Copilot CLI infrastructure

Add copilot-instructions.md, directory scaffolding, README, and AGENTS.md.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git push -u origin bootstrap-skillful
gh pr create --title "Bootstrap skillful" --body "Set up Copilot CLI infrastructure:

- Add .github/instructions/ and .github/hooks/ directory scaffolding
- Create copilot-instructions.md (or merge missing rules into existing)
- Create README.md (if missing)
- Create AGENTS.md (if missing)

Branch protection and merge settings are configured via API separately." --base main
```

Then squash-merge the PR and clean up:

```bash
gh pr merge --squash --delete-branch
```

**Note:** Steps 6 (branch protection) and 7 (merge settings) are API-only operations that don't produce file changes — they run independently and do not need to be part of the PR.

## Re-bootstrapping (Upgrading)

When re-running this skill on a previously bootstrapped repo:

- **Directories**: already exist → skip
- **copilot-instructions.md**: exists → merge missing rules only (Step 3)
- **README.md / AGENTS.md**: exist → skip
- **Branch protection**: exists → verify, don't weaken
- **Merge settings**: re-applied (idempotent API call)

The skill is designed to be safe to re-run at any time.

## Done Criteria

- [ ] `.github/agents/`, `.github/skills/`, `.github/instructions/`, `.github/hooks/` all exist
- [ ] `.github/copilot-instructions.md` exists and contains all four core rules
- [ ] `README.md` exists at the repo root
- [ ] `AGENTS.md` exists at the repo root
- [ ] Default branch requires PRs (no direct pushes)
- [ ] Self-approval is allowed (0 required approving reviews)
- [ ] Repository defaults to squash merge with PR title/body
- [ ] Head branches are automatically deleted after merge
- [ ] All changes are committed and pushed (or in a PR if branch protection is active)
