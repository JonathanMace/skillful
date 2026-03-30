---
name: stale-reference-audit
summary: Find and fix internal cross-references that point to renamed, moved, or deleted targets
trigger:
  type: commit-count
  value: 20
severity: routine
estimated-effort: small
---

# Stale Reference Audit

## Purpose

Projects that use cross-references — file paths in markdown, skill/agent names in instructions, section anchors in docs — accumulate broken links as files move, rename, or get deleted. Left unchecked, these stale references erode trust in documentation and cause agent failures: an agent told to "read file X" that doesn't exist wastes tool calls recovering (or silently proceeds with incomplete information, producing incorrect output).

This task was created after a critical self-review found 3 stale vocabulary references and an incomplete repository structure description that had drifted from reality.

## Trigger Conditions

- **Primary**: every 20 commits since last run (starting point — see Calibration below)
- **Additional**: should also run after any bulk rename, directory restructure, or skill/agent addition/removal
- **Skip condition**: if the only files changed since last run match the ignore pattern below, defer one cycle. To evaluate: run `git diff --name-only <last-sha>..HEAD` and check if ALL changed files match `*.png`, `*.jpg`, `*.gif`, `*.svg`, `*.ico`, `*.woff*`, `*.ttf`, or paths under `assets/` or `vendor/`. If any file falls outside these patterns, the skip condition is NOT met and the audit must run.

## Procedure

1. **Inventory reference sources** — identify all files that contain internal cross-references. In this repository, that means:
   - Markdown files (`.md`) — relative paths, `Read .github/...` instructions, section anchors
   - Agent files (`.agent.md`) — file paths in instructions, skill references
   - Instruction files (`copilot-instructions.md`, embedded member files) — directory descriptions, file paths
   - YAML frontmatter — referenced paths
   
   For non-Copilot projects, adapt step 1 to your project's reference types (e.g., import statements, URL references, bibliography entries).

2. **Extract references** — for each source file, extract all internal references:
   - File paths (e.g., `.github/skills/foo/SKILL.md`)
   - Directory references (e.g., "files live in `.github/agents/`")
   - Skill/agent name references (e.g., "see the `writing-custom-agents` skill")
   - Section anchors (e.g., `#how-to-implement`)

3. **Validate each reference**:
   - **File paths**: verify the target file exists at the referenced path
   - **Directory references**: verify the directory exists and the description matches its actual contents
   - **Skill/agent names**: verify a matching skill directory or agent file exists
   - **Section anchors**: verify the target section heading exists in the referenced file

4. **Categorise findings**:
   - **Broken**: target doesn't exist at all → must fix
   - **Stale**: target exists but description/context is outdated → should fix
   - **Ambiguous**: reference is vague enough that correctness can't be verified → flag for escalation

5. **Fix broken and stale references**:
   - For broken paths: find the correct new path (check `git log --diff-filter=R --summary` for renames) or remove the reference
   - For stale descriptions: update to match current reality
   - For ambiguous references: log them. If >3 ambiguous findings have accumulated across runs (check state file history), create a GitHub Issue to escalate to the human.

6. **Report findings** — produce a summary:
   ```
   ## Stale Reference Audit — [date]
   - Files scanned: N
   - References checked: N
   - Broken: N (fixed: N)
   - Stale: N (fixed: N)
   - Ambiguous: N (flagged/escalated)
   ```

## Verification

- [ ] All file path references in markdown files resolve to existing files
- [ ] All directory descriptions match their actual contents
- [ ] All skill/agent name references match existing skills/agents
- [ ] No broken section anchors remain
- [ ] Changes committed with descriptive message

## Calibration

The 20-commit trigger is a starting point. After 5 runs:
- If ≥3 consecutive runs find 0 issues, the runner will suggest doubling the interval
- If any run finds >10 issues, the runner will suggest halving the interval
- Adjust the `trigger.value` in this file's frontmatter based on the suggestion

## Logging

Update the maintenance state file with:
- Last run date and current HEAD commit SHA
- Result summary (e.g., "✅ 3 fixes" or "✅ clean" or "⚠️ 2 ambiguous flagged")
- Reset Consecutive Clean counter to 0 if any issues found; increment if clean
