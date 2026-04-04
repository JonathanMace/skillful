# Skill Compliance Audit — Prompt Template

> **Purpose:** Give this entire file as a prompt to a subagent. It will read every skill, evaluate it against the checklist, and produce a structured report.

---

## Instructions

You are auditing all skills in this repository for compliance with the authoring rules defined in the `writing-skills` skill.

### Step 1: Read the Checklist

Read `tests/skill-compliance/checklist.md`. This is the authoritative set of checks. Do not invent additional criteria — use exactly the checks listed there.

### Step 2: Read Every Skill

Read each `SKILL.md` file listed below:

| Skill | Path |
|-------|------|
| agent-design-patterns | `skills/agent-design-patterns/SKILL.md` |
| bootstrap-skillful | `skills/bootstrap-skillful/SKILL.md` |
| create-persona | `skills/create-persona/SKILL.md` |
| git-checkpoint | `skills/git-checkpoint/SKILL.md` |
| latex-report | `skills/latex-report/SKILL.md` |
| related-work | `skills/related-work/SKILL.md` |
| review-document | `skills/review-document/SKILL.md` |
| session-analysis | `skills/session-analysis/SKILL.md` |
| writing-plugins | `skills/writing-plugins/SKILL.md` |
| writing-custom-agents | `skills/writing-custom-agents/SKILL.md` |
| writing-custom-instructions | `skills/writing-custom-instructions/SKILL.md` |
| writing-hooks | `skills/writing-hooks/SKILL.md` |
| writing-skills | `skills/writing-skills/SKILL.md` |

### Step 3: Evaluate Each Skill

For each skill, evaluate every check in the checklist (F1–F7, D1–D5, B1–B6, C1–C4). Assign a rating of **PASS**, **NEEDS WORK**, or **FAIL** to each check.

### Step 4: Produce the Report

#### Per-Skill Report Card

For each skill, output a report card in this format:

```
## <skill-name>

| Check | Rating | Notes |
|-------|--------|-------|
| F1 | PASS | |
| F2 | PASS | |
| ... | ... | ... |

**Overall: PASS / NEEDS WORK / FAIL**
**Summary:** <1-2 sentence summary of the skill's compliance>
```

Include notes only when the rating is NEEDS WORK or FAIL — explain what is missing or incorrect.

#### Summary Table

After all per-skill report cards, output a summary table:

```
## Summary

| Skill | Frontmatter | Description | Body | Conventions | Overall |
|-------|-------------|-------------|------|-------------|---------|
| git-checkpoint | PASS | PASS | NEEDS WORK | PASS | NEEDS WORK |
| ... | ... | ... | ... | ... | ... |
```

Each category rating is the worst rating among its checks (e.g., if any check in "Body" is FAIL, the category is FAIL).

#### Recommendations

After the summary table, list the top 3–5 concrete improvements that would have the highest impact across all skills. Be specific — reference the skill name and check ID.

### Scoring Rules

Use these rules to assign overall ratings:

- **PASS** — all checks pass, or only minor NEEDS WORK items (cosmetic, not structural)
- **NEEDS WORK** — multiple NEEDS WORK items, or one FAIL in a non-critical area (B4, C3, C4)
- **FAIL** — any FAIL in Frontmatter required fields (F1–F6) or Description Quality core rules (D1–D2), or 3+ FAILs in any category

### Important Notes

- Evaluate `writing-skills` itself — it must follow its own rules.
- Be objective. Don't give PASS just because a skill is well-written overall — check each item independently.
- For D1 (purpose-first), the test is: does the first sentence describe an **outcome or capability**, or does it describe **the skill itself**? "Skills teach agents reusable procedures…" passes because it leads with the capability. "A guide for writing skills" would fail.
- For B2 (inspect first), the step doesn't need to be literally named "Inspect First" — it just needs to instruct the agent to read existing state before acting.
- For C3 (tone), compare across all skills. Minor differences are acceptable; major stylistic divergence is NEEDS WORK.
