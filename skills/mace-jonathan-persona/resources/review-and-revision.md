# Persona Skill Review — mace-jonathan-persona

## Compliance Checklist Results

### 1. Frontmatter

| # | Check | Result | Notes |
|---|-------|--------|-------|
| F1 | Has YAML frontmatter | PASS | Opens with `---` delimited YAML block (lines 1–8) |
| F2 | Has `name` field | PASS | `name: mace-jonathan-persona` |
| F3 | Has `description` field | PASS | Two well-formed sentences using YAML `>-` block scalar |
| F4 | `license` is optional | PASS | Not present; not required |
| F5 | `name` is lowercase with hyphens | PASS | `mace-jonathan-persona` — only lowercase, digits, and hyphens |
| F6 | `name` matches directory name | PASS | Both are `mace-jonathan-persona` |
| F7 | `description` is 1–3 sentences | PASS | Two sentences: one stating the capability, one stating when to use it |

### 2. Description Quality

| # | Check | Result | Notes |
|---|-------|--------|-------|
| D1 | First sentence is purpose-first | PASS | "Write research prose in the style of Jonathan Mace by following his recurring research interests, problem-framing habits, and characteristic rhetorical moves." — leads with the capability |
| D2 | First sentence is NOT tautological | PASS | Does not begin with "Guide for…", "Skill for…", or similar self-referential phrasing |
| D3 | Includes trigger phrases | PASS | "Use when drafting or revising abstracts, introductions, related work, papers, proposals, or reviews that should sound like this researcher." — explicit trigger with broad keyword coverage |
| D4 | Specific enough to avoid false matches | PASS | Scoped to writing in a specific researcher's voice; unlikely to fire for unrelated tasks |
| D5 | Specific enough to avoid missed invocations | PASS | Covers "drafting," "revising," multiple section types, and "reviews" — broad trigger surface for research-writing tasks involving this persona |

### 3. Body Structure

| # | Check | Result | Notes |
|---|-------|--------|-------|
| B1 | Has a numbered procedure | PASS | Five numbered steps under "## Procedure" |
| B2 | Procedure opens with "Inspect First" step | PASS | Step 1 is explicitly "**Inspect First**" — reads the task, venue rules, and source material |
| B3 | Has cross-references to related skills/docs | NEEDS WORK | Extensively cross-references its own `resources/` directory (8 files listed in the Resources section). However, it has **no external cross-references** to sibling skills. Every comparable sibling skill cross-references related skills: `create-persona` links to `related-work`, `agent-design-patterns`, `review-document`, and `writing-skills`; `review-document` links to `agent-design-patterns`, `writing-custom-agents`, and `create-persona`. This skill should reference at least `create-persona` (for regeneration/updates) and `writing-skills` (the compliance rules that govern its shape). |
| B4 | Has examples where appropriate | PASS | Core Writing Patterns section includes 10 patterns each with concrete cited paper examples; Signature Lexicon provides frequency-categorized vocabulary; Do/Don't section gives 19 specific directives. Full-persona.md adds dozens more cited examples. |
| B5 | Has a "Done Criteria" section | PASS | Four exit conditions under "## Done Criteria" covering persona fidelity, style representation, venue-override precedence, and confidence bounds |
| B6 | Instructions are actionable | PASS | Numbered procedure steps with specific actions; the 10 core writing patterns are concrete enough to follow directly; Do/Don't items are specific (e.g., "Don't use 'argue' as a primary verb — prefer 'show'") |

### 4. Conventions

| # | Check | Result | Notes |
|---|-------|--------|-------|
| C1 | Directory name is lowercase with hyphens | PASS | `mace-jonathan-persona` |
| C2 | File is named exactly `SKILL.md` | PASS | Confirmed |
| C3 | Tone matches sibling skills | PASS | Professional, instructional, declarative. Uses the same structural conventions as `git-checkpoint`, `create-persona`, and `review-document`: heading hierarchy, bold-face terms, bulleted/numbered lists, dedicated Done Criteria section. Appropriately more content-dense than process skills, since it serves as a quick-reference persona card. |
| C4 | No unnecessary duplication | PASS | The SKILL.md contains a compressed summary (~124 lines) that is deliberately designed for fast in-context use, while deferring all evidence, citations, and nuance to `resources/full-persona.md` (420 lines). The overlap between the two is intentional and appropriate — the SKILL.md provides just enough for an agent to write correctly without reading the full synthesis, while the full synthesis provides the evidentiary depth for ambiguous or high-stakes tasks. |

## Persona-Specific Quality

| Check | Result | Notes |
|-------|--------|-------|
| SKILL.md is concise, not biographical | PASS | The Overview is two short paragraphs (identity + purpose). The rest of the 124-line body is operational: writing patterns, voice guidance, lexicon, and do/don't rules. No biographical narrative, timeline, or publication list appears in the SKILL.md itself. |
| full-persona.md contains full synthesis | PASS | 420 lines covering: evidence base, research areas, career-phase overview, 10 core writing patterns with cited examples, voice and tone analysis, lexical habits, section-by-section preferences (abstract through conclusion), concrete cited examples, do/don't guidance, and confidence limits. This is a comprehensive, well-organized synthesis document. |
| Worker reports preserved | PASS | All 7 worker reports are preserved under `resources/`: `paper-01.md` through `paper-04.md` (deep readings of 10 papers across 4 batches), `identity-and-bibliography.md`, `publication-history.md`, and `flagship-papers.md`. |
| Reports are findings, not process logs | PASS | Each report opens with a "## Persona Findings" section containing numbered observations about the researcher's patterns, then a "## Evidence" section with detailed per-paper analysis. The language is "Mace consistently opens with…" and "This pattern recurs across…" — durable characterizations, not "I searched for X and found Y" process narration. |
| Concrete cited examples in resources | PASS | Extensive. `full-persona.md` §"Concrete Cited Examples" provides 8 sub-categories of examples, each with 3–6 direct quotes keyed to specific papers and sections (e.g., "Pivot Tracing (SOSP 2015): 'there is a mismatch between the expectations and incentives…'"). Worker reports add further evidence with paper-specific quotes and structural observations. |
| Do/Don't guidance is actionable | PASS | The SKILL.md provides 11 Do items and 8 Don't items, each as a bold directive followed by one-sentence explanation. The full-persona.md expands these to 14 Do and 12 Don't items with cited justifications. All are specific enough to apply during drafting (e.g., "Don't use 'argue' as a primary verb — prefer 'show'"; "Use 'In practice' frequently to contrast theory with operational reality"). |
| Resource map is complete and accurate | PASS | The Resources section lists all 8 files with descriptions. Every listed file exists in the `resources/` directory. Every file in the directory is listed. The descriptions accurately characterize the file contents (verified by reading each). The "420 lines" claim for full-persona.md is accurate. |

## Overall Assessment

- **Overall rating: PASS**

### Strengths

1. **Excellent frontmatter and description quality.** The description is purpose-first, non-tautological, trigger-rich, and precisely scoped — one of the better descriptions in the repository.
2. **Comprehensive evidence base.** The resources directory contains 7 worker reports plus a 420-line synthesis document, totaling over 180 KB of detailed, cited findings. This is an unusually thorough evidence base for a persona skill.
3. **Operational rather than biographical.** The SKILL.md resists the temptation to become a biography. It stays focused on what an agent needs to write correctly: patterns, lexicon, voice, and do/don't rules.
4. **Strong confidence calibration.** The full-persona.md explicitly categorizes patterns into high-confidence, medium-confidence, and low-confidence tiers, and includes a "What We Don't Know" section. This is valuable — it tells the agent where to push hard and where to tread carefully.
5. **Concrete cited examples make the persona operational.** The examples aren't paraphrased — they're direct quotes keyed to specific papers, sections, and years. An agent can match these patterns without having read the source papers.
6. **Worker reports read as durable reference documents.** Each paper-batch report is structured as numbered findings with an evidence section — usable as standalone reference material, not disposable process artifacts.

### Issues Requiring Revision

The only compliance gap is minor:

## Required Revisions

1. **Add external cross-references (B3).** Add a brief "Cross-References" or "See Also" section (or incorporate references into the Overview or Procedure) that points to:
   - `create-persona` — the skill that defines the process for generating and updating persona skills like this one
   - `writing-skills` — the compliance standard this skill was built to satisfy
   - Optionally, `review-document` — useful when reviewing prose drafted with this persona

   A minimal addition to the end of the Overview or after the Resources section would suffice, e.g.:

   ```markdown
   ## See Also

   - `create-persona` — the skill that generates and updates persona skills like this one
   - `writing-skills` — the compliance rules governing skill structure and frontmatter
   - `review-document` — for independent review of prose drafted using this persona
   ```
