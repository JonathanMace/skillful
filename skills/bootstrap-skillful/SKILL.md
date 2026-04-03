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

### 3. Add Project Header to `copilot-instructions.md`

If `.github/copilot-instructions.md` does not exist, or exists but does not start with a project title and description, add a header at the top of the file:

```markdown
# <project name>

<one-line description of what the project does>
```

Derive the project name from the repository name and the description from the repo's GitHub description (or a sensible default). If the file already starts with a heading and description, leave them as-is.

### 4. Create or Update Skillful Rules in `copilot-instructions.md`

The template at `templates/copilot-instructions.md` (relative to this skill's directory) contains the managed rules wrapped in guard comments:

```html
<!-- BEGIN SKILLFUL MANAGED SECTION -->
...rules...
<!-- END SKILLFUL MANAGED SECTION -->
```

**If `.github/copilot-instructions.md` does not exist:**

Create it with the project header from Step 3 followed by the full template contents.

**If the file exists but has no guard comments:**

This means it was created manually or by an older version of skillful. Append the full template contents (including guard comments) after the existing content. Do **not** remove or rewrite existing content.

**If the file exists and already has guard comments:**

Replace everything between `<!-- BEGIN SKILLFUL MANAGED SECTION -->` and `<!-- END SKILLFUL MANAGED SECTION -->` (inclusive) with the current template contents. This upgrades the managed rules in place while preserving all user-authored content outside the markers.

The managed section contains these four rules:

1. **Self-Updating Instructions** — agents must add discovered patterns and anti-patterns to this file immediately
2. **Work Tracking** — subagents doing coding tasks must use dedicated git worktrees via the `git-checkpoint` skill
3. **Subagent Model Specification** — always specify the model when spawning subagents
4. **README Maintenance** — keep the README up to date when creating new artifacts

The **Anti-Patterns** section lives outside the managed markers (after them) so user-added entries are never overwritten. If no Anti-Patterns section exists, append one after the closing marker.

### 5. Create `README.md` (if missing)

If no `README.md` exists at the repository root, create one with:

- Project name (derived from the repo name)
- A placeholder description
- A "Getting Started" section
- A note that this repo is managed with Copilot CLI

If a `README.md` already exists, leave it as-is.

### 6. Create `AGENTS.md` (if missing)

If no `AGENTS.md` exists at the repository root, create one using the template at `templates/AGENTS.md` (relative to this skill's directory). Customize the placeholders based on the repository.

If `AGENTS.md` already exists, leave it as-is.

### 7. Create `.gitignore` (if missing)

If no `.gitignore` exists at the repository root, create one with sensible defaults for the project. Inspect the repository to determine the primary language/framework and generate appropriate ignore patterns. At minimum, include:

```
# OS files
.DS_Store
Thumbs.db

# Editor files
*.swp
*.swo
*~
.idea/
.vscode/
*.code-workspace
```

Add language-specific patterns based on what you find in the repo (e.g., `node_modules/` for Node.js, `__pycache__/` for Python, `bin/` and `obj/` for .NET).

If a `.gitignore` already exists, leave it as-is.

### 8. Protect the Default Branch

Configure branch protection so that the default branch (typically `main`) only accepts changes via pull requests, with self-approval allowed.

**Desired state:**

- Direct pushes to the default branch are **blocked**
- All changes must come through pull requests
- **No required approvals** — the PR author can merge their own PR (self-approval)
- No required status checks (the user can add these later)

**Using GitHub repository rulesets** (preferred):

First, check if a ruleset already protects the default branch:

```
gh api repos/{owner}/{repo}/rulesets
```

If no ruleset covers the default branch, create one. Write the JSON body to a temporary file, pass it to `gh api`, then delete the file:

```
# Write the ruleset JSON to a temp file
# (Use your shell's temp-file mechanism — the JSON content is what matters)
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

gh api repos/{owner}/{repo}/rulesets -X POST --input <temp-file>
```

Replace `main` with the actual default branch name if different.

If the rulesets API is unavailable (e.g., older GitHub plan), fall back to classic branch protection using this JSON body:

```
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "restrictions": null
}

gh api repos/{owner}/{repo}/branches/main/protection -X PUT --input <temp-file>
```

**If branch protection already exists**, verify it matches the desired state. Do not weaken existing protections — only add the PR requirement if it is missing.

### 9. Configure Repository Merge Settings

Set the repository to default to **squash merging** and to **automatically delete head branches** after merge using this JSON body:

```
{
  "allow_squash_merge": true,
  "allow_merge_commit": true,
  "allow_rebase_merge": true,
  "squash_merge_commit_title": "PR_TITLE",
  "squash_merge_commit_message": "PR_BODY",
  "delete_branch_on_merge": true
}

gh api repos/{owner}/{repo} -X PATCH --input <temp-file>
```

This ensures:

- **Squash merge** is available and produces clean single-commit history
- Other merge strategies remain available (the user can disable them later)
- **Head branches are automatically deleted** after merging a PR, preventing stale branch accumulation

If the API call fails due to insufficient permissions, note it in the output and continue — these are non-blocking settings.

### 10. Commit and Open a PR

All file changes from steps 2–7 should be committed together on a feature branch and submitted as a single pull request.

**Important — shell compatibility:** Do not pass multi-line strings or strings with special characters (backticks, quotes, angle brackets) directly on the command line. PowerShell and other shells mangle them. Instead, write message bodies to a temporary file and use file-based flags (`--body-file`, `--file`).

```
git checkout -b bootstrap-skillful origin/main
git add -A
```

Write the commit message to a temp file, then commit using `--file`:

```
git commit --file <temp-commit-msg-file>
```

Commit message contents:

```
chore: bootstrap Copilot CLI infrastructure

Add copilot-instructions.md, directory scaffolding, README, and AGENTS.md.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

Push and create the PR using `--body-file`:

```
git push -u origin bootstrap-skillful
gh pr create --title "Bootstrap skillful" --body-file <temp-pr-body-file> --base main
```

PR body contents:

```
Set up Copilot CLI infrastructure:

- Directory scaffolding (.github/agents, skills, instructions, hooks)
- copilot-instructions.md with managed rules
- README.md (if missing)
- AGENTS.md (if missing)

Branch protection and merge settings are configured via API separately.
```

Then squash-merge the PR and clean up:

```
gh pr merge --squash --delete-branch
```

Delete any temporary files after the PR is merged.

**Note:** Steps 8 (branch protection) and 9 (merge settings) are API-only operations that don't produce file changes — they run independently and do not need to be part of the PR.

## Re-bootstrapping (Upgrading)

When re-running this skill on a previously bootstrapped repo:

- **Directories**: already exist → skip
- **Project header**: exists → skip (Step 3)
- **copilot-instructions.md managed section**: has guard comments → replace in place (Step 4); no guard comments → append template
- **Anti-Patterns section**: preserved outside managed markers — never overwritten
- **README.md / AGENTS.md / .gitignore**: exist → skip
- **Branch protection**: exists → verify, don't weaken
- **Merge settings**: re-applied (idempotent API call)

The skill is designed to be safe to re-run at any time.

## Done Criteria

- [ ] `.github/agents/`, `.github/skills/`, `.github/instructions/`, `.github/hooks/` all exist
- [ ] `.github/copilot-instructions.md` exists and contains all four core rules plus build artifact rule
- [ ] `.gitignore` exists at the repo root
- [ ] `README.md` exists at the repo root
- [ ] `AGENTS.md` exists at the repo root
- [ ] Default branch requires PRs (no direct pushes)
- [ ] Self-approval is allowed (0 required approving reviews)
- [ ] Repository defaults to squash merge with PR title/body
- [ ] Head branches are automatically deleted after merge
- [ ] All changes are committed and pushed (or in a PR if branch protection is active)
