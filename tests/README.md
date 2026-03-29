# Skill Test Framework

This directory contains a structured, repeatable test framework for validating skills in this repository. Tests verify that skills adhere to the rules defined in the [`writing-skills` skill](../.github/skills/writing-skills/SKILL.md).

## Test Categories

### 1. Structural Compliance (`skill-compliance/`)

Automated-style checks that verify every skill follows the required format, naming conventions, description quality rules, and body structure defined by `writing-skills`. These are deterministic — a skill either passes or it doesn't.

- **[`checklist.md`](skill-compliance/checklist.md)** — the authoritative checklist every skill is tested against, extracted from `writing-skills/SKILL.md`
- **[`run-audit.md`](skill-compliance/run-audit.md)** — a self-contained prompt template you give to a subagent to run the full audit

### 2. Behavioral Tests (`behavioral/`)

Prompt-based tests that verify skills work correctly when invoked by Copilot. Each test file contains prompts, expected outcomes, and scoring criteria. Results require human or reviewer-agent judgment.

- **[`description-discovery.md`](behavioral/description-discovery.md)** — tests that skill descriptions lead to correct auto-invocation
- **[`instruction-placement.md`](behavioral/instruction-placement.md)** — tests for the `writing-custom-instructions` skill
- **[`skill-authoring.md`](behavioral/skill-authoring.md)** — tests for the `writing-skills` skill
- **[`git-workflow.md`](behavioral/git-workflow.md)** — tests for the `git-checkpoint` skill

## How to Run Tests

### Structural Compliance Audit

Give the prompt in `skill-compliance/run-audit.md` to a subagent (or paste it into a Copilot CLI session):

```
Run the skill compliance audit described in tests/skill-compliance/run-audit.md
```

The subagent will read every skill, evaluate it against the checklist, and produce a per-skill report card plus a summary table.

### Behavioral Tests

Run a specific behavioral test file by telling a subagent to execute it:

```
Run the behavioral test described in tests/behavioral/description-discovery.md
```

Or run all behavioral tests:

```
Run all behavioral tests in tests/behavioral/
```

Each behavioral test file is self-contained — it includes the prompts, expected outcomes, and scoring criteria.

### Capturing Results

Test results can optionally be written to `tests/LAST-RUN.md` by the agent running the tests. This file is not checked in — it captures the most recent run for review.

## How to Add New Tests

### Adding a Structural Check

1. Add the check to `skill-compliance/checklist.md` under the appropriate category.
2. Update `skill-compliance/run-audit.md` if the check requires special evaluation instructions.

### Adding a Behavioral Test

1. Create a new `.md` file in `behavioral/`.
2. Follow the format used by existing test files:
   - **Purpose** — what the test validates
   - **Prompts** — the exact prompts to give to a subagent
   - **Expected Outcome** — what correct behavior looks like
   - **Scoring Criteria** — how to grade the result (PASS / NEEDS WORK / FAIL)
3. Add the test to this README under the behavioral tests list.

## Design Principles

- **LLM-native**: tests are prompt files, not scripts. The "test runner" is a subagent given a prompt.
- **Self-contained**: each test file includes everything needed to run it — no external context required.
- **Repeatable**: anyone can re-run the same tests and compare results across runs.
- **Practical**: the framework is lightweight. Don't over-engineer what is fundamentally an LLM evaluation task.
