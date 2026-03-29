# Behavioral Test: Instruction Placement

## Purpose

Verify that the `writing-custom-instructions` skill correctly guides Copilot to place instructions in the right file type (repository-wide, path-specific, or local) based on the nature of the rule being authored.

## How to Run

For each test prompt below, give it to a subagent working in this repository with the `writing-custom-instructions` skill available. The subagent should determine where to place the instruction and create (or describe creating) the appropriate file. Evaluate whether it chose the correct file type and location.

---

## Test Prompts

### T1 — American English Spelling
**Prompt:** "Add an instruction that all code comments and documentation must use American English spelling."
**Expected placement:** Repository-wide (`.github/copilot-instructions.md`)
**Rationale:** This is a broad convention that applies to all files and all tasks. It belongs in the global instruction file.

**Scoring:**
- **PASS**: Places in `.github/copilot-instructions.md`
- **NEEDS WORK**: Places in the right file but also creates an unnecessary path-specific file
- **FAIL**: Places in a path-specific file or local instructions only

### T2 — React Hooks Convention
**Prompt:** "Enforce that all React components in src/frontend/ must use hooks instead of class components."
**Expected placement:** Path-specific (`.github/instructions/*.instructions.md` with `applyTo: "src/frontend/**/*.tsx"` or similar)
**Rationale:** This rule is scoped to a specific directory and file type. It should be a path-specific instruction, not a global one.

**Scoring:**
- **PASS**: Creates a path-specific file with an appropriate `applyTo` glob matching `src/frontend/` and React file extensions
- **NEEDS WORK**: Creates a path-specific file but the glob is too broad (e.g., `**`) or too narrow
- **FAIL**: Places in `.github/copilot-instructions.md` without any path scoping

### T3 — Input Validation Rule
**Prompt:** "All API endpoint handlers must validate input parameters before processing. Add this as an instruction."
**Expected placement:** Path-specific (`.github/instructions/*.instructions.md` with `applyTo` matching API handler files) OR repository-wide if no clear API directory structure exists
**Rationale:** If the repo has a clear API directory, this should be path-specific. If not, repository-wide is acceptable since it's a broad security convention.

**Scoring:**
- **PASS**: Creates a path-specific file targeting API handlers, OR places in `.github/copilot-instructions.md` with a brief justification for the scope choice
- **NEEDS WORK**: Places correctly but doesn't consider scope — no mention of why global vs. path-specific
- **FAIL**: Places in local/personal instructions (`~/.copilot/copilot-instructions.md`) — this is a project rule, not a personal preference

### T4 — npm Test Command
**Prompt:** "Configure instructions so that Copilot always uses `npm test -- --coverage` when running tests."
**Expected placement:** Repository-wide (`.github/copilot-instructions.md`)
**Rationale:** Build/test commands are project-wide conventions. They belong in global instructions.

**Scoring:**
- **PASS**: Places in `.github/copilot-instructions.md`
- **NEEDS WORK**: Places in a path-specific file scoped to test files — partially reasonable but over-scoped
- **FAIL**: Places in local instructions or doesn't create a file at all

### T5 — Mixed Rules (Multiple Scopes)
**Prompt:** "Add these rules: (1) Use TypeScript strict mode everywhere, (2) All GraphQL resolvers in src/graphql/ must include error handling, (3) I personally prefer verbose variable names in all my projects."
**Expected placement:**
- Rule 1: Repository-wide (`.github/copilot-instructions.md`)
- Rule 2: Path-specific (`.github/instructions/*.instructions.md` with `applyTo: "src/graphql/**"`)
- Rule 3: Local/personal (`~/.copilot/copilot-instructions.md`)
**Rationale:** This tests whether the skill correctly splits mixed-scope rules into the appropriate files.

**Scoring:**
- **PASS**: All three rules placed in the correct file type. Rule 1 is global, Rule 2 is path-specific, Rule 3 is local/personal
- **NEEDS WORK**: Two of three rules placed correctly
- **FAIL**: All rules dumped into a single file, or Rule 3 is placed in a repo-level file

---

## Overall Scoring

| Rating | Criteria |
|--------|----------|
| **PASS** | 4+ of 5 prompts score PASS |
| **NEEDS WORK** | 3 of 5 prompts score PASS |
| **FAIL** | Fewer than 3 prompts score PASS |

## Evaluation Notes

- The subagent should reference the skill's guidance on instruction types and scoping.
- Watch for the skill's "Inspect existing instructions" step — the subagent should check what already exists before creating new files.
- If the subagent explains its reasoning for the placement choice, that's a positive signal even if the choice is borderline.
- The `applyTo` glob doesn't need to be exact — it should be reasonable for the described scope.
