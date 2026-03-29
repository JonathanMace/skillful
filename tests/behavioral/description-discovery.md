# Behavioral Test: Description Discovery

## Purpose

Verify that skill descriptions lead to correct auto-invocation. Good descriptions cause Copilot to load the right skill for matching prompts and avoid loading skills for unrelated prompts.

This test covers all 6 skills via their `description` fields.

## How to Run

Give each prompt below to a fresh Copilot CLI session (or a subagent) working in this repository. Observe which skill(s) Copilot auto-invokes. Compare against the expected outcome.

---

## Positive Prompts (SHOULD trigger a specific skill)

These prompts should cause Copilot to auto-invoke the indicated skill.

### P1 — git-checkpoint
**Prompt:** "I need to create a branch, make some changes, open a PR, and clean up after merging."
**Expected skill:** `git-checkpoint`
**Why:** Directly describes the git lifecycle the skill covers.

### P2 — writing-skills
**Prompt:** "Create a new SKILL.md for a code review workflow."
**Expected skill:** `writing-skills`
**Why:** Explicitly mentions SKILL.md authoring.

### P3 — writing-custom-instructions
**Prompt:** "Add a rule to copilot-instructions.md that enforces consistent error handling."
**Expected skill:** `writing-custom-instructions`
**Why:** Mentions copilot-instructions.md directly.

### P4 — writing-hooks
**Prompt:** "Set up a pre-tool hook that blocks any shell command containing rm -rf."
**Expected skill:** `writing-hooks`
**Why:** Describes hook authoring with a pre-tool guard.

### P5 — writing-custom-agents
**Prompt:** "I want to create a specialized Copilot persona for database migrations that only has read and execute access."
**Expected skill:** `writing-custom-agents`
**Why:** Describes creating a custom agent with constrained tools.

### P6 — session-analysis
**Prompt:** "What happened in my last Copilot session? Show me a summary of tool usage and token consumption."
**Expected skill:** `session-analysis`
**Why:** Asks for session review and analysis.

### P7 — writing-custom-instructions (path-specific)
**Prompt:** "Create path-specific instructions for all Python files in the src/ directory."
**Expected skill:** `writing-custom-instructions`
**Why:** Path-specific instructions are a core topic of this skill.

### P8 — writing-skills (indirect)
**Prompt:** "Package our deployment checklist as reusable knowledge that Copilot can load on demand."
**Expected skill:** `writing-skills`
**Why:** Describes the purpose of a skill without using the word "skill." Tests purpose-first discovery.

---

## Negative Prompts (SHOULD NOT trigger a specific skill)

These prompts should NOT cause Copilot to auto-invoke the indicated skill (or any skill from this repo).

### N1 — Not git-checkpoint
**Prompt:** "Fix the failing unit test in src/auth/login.test.ts."
**Should NOT trigger:** `git-checkpoint`
**Why:** Fixing a test is a coding task, not a git workflow task.

### N2 — Not writing-skills
**Prompt:** "Review my Python code for security vulnerabilities."
**Should NOT trigger:** `writing-skills`
**Why:** Code review has nothing to do with skill authoring.

### N3 — Not writing-hooks
**Prompt:** "Set up a GitHub Actions workflow that runs on every push."
**Should NOT trigger:** `writing-hooks`
**Why:** GitHub Actions workflows are not Copilot CLI hooks. A false match here would indicate the description is too broad.

### N4 — Not writing-custom-agents
**Prompt:** "Refactor the UserService class to use dependency injection."
**Should NOT trigger:** `writing-custom-agents`
**Why:** Code refactoring is unrelated to agent authoring.

### N5 — Not session-analysis
**Prompt:** "Analyze the performance of our REST API endpoints."
**Should NOT trigger:** `session-analysis`
**Why:** API performance analysis is different from Copilot session analysis. The word "analyze" alone should not trigger it.

### N6 — Not writing-custom-instructions
**Prompt:** "Write documentation for the API module."
**Should NOT trigger:** `writing-custom-instructions`
**Why:** Writing documentation is not the same as writing Copilot instructions.

### N7 — Not writing-skills (edge case)
**Prompt:** "Help me improve my programming skills."
**Should NOT trigger:** `writing-skills`
**Why:** The word "skills" here refers to personal abilities, not Copilot skills. Tests specificity.

### N8 — Not git-checkpoint
**Prompt:** "Show me the git log for the last 10 commits."
**Should NOT trigger:** `git-checkpoint`
**Why:** Viewing git history is a simple command, not a lifecycle workflow.

---

## Scoring Criteria

### Per-Prompt Scoring

| Rating | Positive Prompts | Negative Prompts |
|--------|-----------------|-----------------|
| **PASS** | Correct skill auto-invoked | Indicated skill NOT invoked |
| **NEEDS WORK** | Correct skill invoked along with unrelated skills | Indicated skill invoked but alongside the correct one |
| **FAIL** | Wrong skill invoked, or no skill invoked | Indicated skill was the primary invocation |

### Overall Scoring

| Rating | Criteria |
|--------|----------|
| **PASS** | 12+ of 16 prompts score PASS |
| **NEEDS WORK** | 8–11 prompts score PASS |
| **FAIL** | Fewer than 8 prompts score PASS |

### Notes

- Auto-invocation behavior depends on the Copilot model and context. Some variation is expected.
- If a skill is invoked but not used (loaded but not followed), still count it as invoked for scoring purposes.
- Record which skill(s) were invoked for each prompt to help diagnose description issues.
