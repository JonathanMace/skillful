# Skill Compliance Checklist

This is the authoritative checklist for evaluating skills in this repository. Every rule here is extracted from [`skills/writing-skills/SKILL.md`](../../skills/writing-skills/SKILL.md) and the repository's [`copilot-instructions.md`](../../.github/copilot-instructions.md).

When auditing a skill, evaluate every item below. Mark each as **PASS**, **NEEDS WORK**, or **FAIL**.

---

## 1. Frontmatter

| # | Check | Rule |
|---|-------|------|
| F1 | Has YAML frontmatter | File starts with `---` delimited YAML block |
| F2 | Has `name` field | Required. Present and non-empty |
| F3 | Has `description` field | Required. Present and non-empty |
| F4 | `license` is optional | If present, it declares the license. Not required |
| F5 | `name` is lowercase with hyphens | Only lowercase letters, digits, and hyphens. No underscores, spaces, or uppercase |
| F6 | `name` matches directory name | The `name` field value is identical to the skill's parent directory name |
| F7 | `description` is 1–3 sentences | Concise: 1 to 3 short sentences. Not a paragraph or a single fragment |

## 2. Description Quality

| # | Check | Rule |
|---|-------|------|
| D1 | First sentence is purpose-first | Leads with what the artifact **achieves** — the capability or outcome — not what the skill "is" |
| D2 | First sentence is NOT tautological | Does NOT start with "Guide for…", "Skill for…", "How to…", "A skill that…", or similar self-referential phrasing |
| D3 | Includes trigger phrases | Contains keywords or phrases users would naturally type when they need this skill (e.g., "Use when…", "Use this skill to…") |
| D4 | Specific enough to avoid false matches | Description is precise enough that Copilot won't load the skill for unrelated tasks |
| D5 | Specific enough to avoid missed invocations | Description covers the skill's full scope so Copilot doesn't miss valid triggers |

## 3. Body Structure

| # | Check | Rule |
|---|-------|------|
| B1 | Has a numbered procedure | Body contains a numbered step-by-step workflow (for procedural skills) or a top-level procedure summarizing the authoring workflow (for reference skills) |
| B2 | Procedure opens with an "Inspect First" step | The first (or early) step instructs the agent to read existing files, configs, or state before making changes |
| B3 | Has cross-references to related skills/docs | References related agents, docs, hooks, or other skills rather than duplicating their content |
| B4 | Has examples where appropriate | Includes concrete input/output samples, code blocks, or templates when they would help the agent |
| B5 | Has a "Done Criteria" section | Explicitly defines what "done" looks like — a checklist, exit conditions, or validation steps |
| B6 | Instructions are actionable | Uses numbered steps, specific commands, or concrete guidance — not vague aspirations like "make it good" |

## 4. Conventions

| # | Check | Rule |
|---|-------|------|
| C1 | Directory name is lowercase with hyphens | The skill's directory name uses only lowercase letters, digits, and hyphens |
| C2 | File is named exactly `SKILL.md` | The main skill file is `SKILL.md` (uppercase), not `skill.md`, `Skill.md`, etc. |
| C3 | Tone matches sibling skills | Writing style, formality level, and structural patterns are consistent with other skills in the repo |
| C4 | No unnecessary duplication | Does not embed long sections that belong to another skill — uses cross-references instead |

---

## Scoring

| Rating | Meaning |
|--------|---------|
| **PASS** | Fully satisfies the check |
| **NEEDS WORK** | Partially satisfies or could be improved, but not broken |
| **FAIL** | Missing, incorrect, or violates the rule |

A skill's overall rating:
- **PASS** — all checks pass, or only minor NEEDS WORK items
- **NEEDS WORK** — multiple NEEDS WORK items, or one FAIL in a non-critical area
- **FAIL** — any FAIL in Frontmatter (F1–F6) or Description Quality (D1–D2), or multiple FAILs elsewhere
