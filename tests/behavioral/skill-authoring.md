# Behavioral Test: Skill Authoring

## Purpose

Verify that the `writing-skills` skill correctly guides Copilot to author new skills that follow all the rules defined in `writing-skills/SKILL.md`. This tests the skill's ability to produce compliant output, not just contain correct instructions.

## How to Run

For each test prompt, give it to a subagent working in this repository with the `writing-skills` skill available. The subagent should author a complete `SKILL.md` file. Evaluate the output against the scoring criteria.

---

## Test Prompts

### T1 — Straightforward Domain
**Prompt:** "Create a skill for debugging GitHub Actions CI failures. It should help agents diagnose why a workflow failed, find the relevant logs, and fix the issue."

**Expected output characteristics:**
- Directory: `skills/github-actions-debugging/` (or similar kebab-case name)
- Frontmatter: `name` matches directory, `description` is purpose-first, 1–3 sentences
- Description: Leads with the capability ("Diagnose and fix failing GitHub Actions workflows…"), not "A skill for…" or "Guide for…"
- Description: Includes trigger phrases ("Use when asked to debug, fix, or investigate CI/CD failures")
- Body: Numbered procedure starting with an inspect/discovery step (e.g., "List recent workflow runs")
- Body: Cross-references to related skills or docs (e.g., mentions `git-checkpoint` for committing fixes)
- Body: Done criteria section
- Body: Examples of commands or tool usage

**Scoring:**
| Criterion | PASS | NEEDS WORK | FAIL |
|-----------|------|------------|------|
| Description is purpose-first | First sentence describes the outcome | First sentence is borderline but close | Tautological ("Guide for…", "Skill for…") |
| Has trigger phrases | Clear "Use when…" clause | Trigger phrases are present but vague | No trigger phrases |
| Procedure starts with inspect step | First step reads existing state (logs, runs) | Inspect step exists but not first | No inspect step |
| Has done criteria | Explicit "Done Criteria" section with checklist | Done criteria mentioned but not structured | No done criteria |
| Has cross-references | References related skills or docs | Mentions related topics but no explicit reference | No cross-references |
| Frontmatter is correct | name, description, correct format | Minor formatting issues | Missing required fields |

### T2 — Abstract/Vague Request
**Prompt:** "Make a skill that helps with database stuff."

**Expected behavior:** The subagent should NOT just create a vague skill. It should:
1. Ask clarifying questions or make a specific scoping decision
2. Define a clear trigger (e.g., "database schema migrations" or "query optimization")
3. Author a focused skill, not a catch-all

**Expected output characteristics:**
- The skill should be scoped to a specific database task, not "all database things"
- Description should be specific enough to avoid false matches
- If the subagent narrows the scope itself, the chosen scope should be reasonable and well-justified

**Scoring:**
| Criterion | PASS | NEEDS WORK | FAIL |
|-----------|------|------------|------|
| Scoping | Narrows to a specific domain with justification | Narrows somewhat but still broad | Creates a vague "database stuff" skill |
| Description specificity | Description targets a clear use case | Description is reasonable but could trigger falsely | Description is vague ("Helps with database stuff") |
| Follows writing-skills procedure | Evidence of following the authoring procedure (inspect, define trigger first) | Partial adherence | No evidence of following the procedure |

### T3 — Skill with Supporting Files
**Prompt:** "Create a skill for generating API documentation. It should include a template for the documentation format and a script that validates the generated docs have all required sections."

**Expected output characteristics:**
- Main `SKILL.md` with proper frontmatter and body
- A `templates/` subdirectory with a documentation template
- A `scripts/` subdirectory with a validation script
- The `SKILL.md` body references both supporting files with relative paths and explains when to use them
- Uses the directory structure pattern from `writing-skills` (SKILL.md + optional scripts/ and templates/)

**Scoring:**
| Criterion | PASS | NEEDS WORK | FAIL |
|-----------|------|------------|------|
| Supporting files created | Both template and script exist | One of the two exists | Neither exists |
| Files are referenced in SKILL.md | Clear references with relative paths and usage context | Referenced but not clearly explained | Not referenced |
| Directory structure follows convention | Matches `skills/<name>/` pattern with scripts/ and templates/ | Correct location but unusual structure | Wrong location or flat structure |
| SKILL.md body is thin | Body focuses on procedure, references files for details | Body is slightly bloated but functional | Body embeds all content inline, ignoring supporting files |

---

## Overall Scoring

| Rating | Criteria |
|--------|----------|
| **PASS** | All 3 tests score majority PASS on their criteria |
| **NEEDS WORK** | 2 of 3 tests score majority PASS |
| **FAIL** | Fewer than 2 tests score majority PASS |

## Evaluation Notes

- The subagent should demonstrate that it read and followed the `writing-skills` procedure (inspect neighbors, define trigger first, etc.).
- Pay special attention to description quality — this is the single most important output.
- T2 is deliberately vague to test whether the skill teaches the agent to scope properly.
- T3 tests the dispatcher/supporting-files pattern from `writing-skills`.
- Don't penalize minor stylistic differences — focus on structural compliance and description quality.
