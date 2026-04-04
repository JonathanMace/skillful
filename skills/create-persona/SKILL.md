---
name: create-persona
description: >-
  Create a research-writing persona skill by deeply studying a specific
  person's publication record, flagship papers, venues, and stylistic patterns,
  then packaging the findings as a concise reusable skill with detailed
  supporting resources. Use when creating a persona for the user, a recurring
  author, an advisor, or another researcher whose voice should shape future
  writing in the repo.
license: MIT
---

# Creating a Research Persona Skill

Use this skill when the repository should learn how a specific researcher tends to think, argue, structure papers, and sound on the page. This is not a shallow "write like X" exercise. The goal is to build a high-quality persona from primary evidence across that person's research career, then encode it as a **concise persona skill** backed by a **detailed `resources/` directory** that preserves the evidence and full synthesis.

For literature-search methodology, see `related-work`. For multi-agent orchestration, see `agent-design-patterns` and its `research-team` pattern. For final critique of the generated artifact, see `review-document`. For the rules the generated persona skill must satisfy, see `writing-skills`.

## Procedure

1. **Inspect First** — read the request carefully and identify:
    - the target person's full name and any aliases
    - whether this is the user, a named advisor, a lab lead, or another researcher
    - whether the resulting persona should represent the repository as a whole
    - any existing persona files, author notes, drafts, or house-style instructions
    - where the generated skill should live; default to a standard skill directory rather than a flat file
 2. **Default to a standard skill directory** — create a skill directory such as `.github/skills/<surname-firstname-persona>/` unless the user explicitly requires another location. Prefer a skill directory over a flat file so the persona can carry a `resources/` directory with durable evidence and detailed reports.
 3. **Create the scaffold before deep research** — create the target persona skill directory up front with:
    - `SKILL.md` for the concise reusable persona instructions
    - `resources/full-persona.md` for the detailed synthesis
    - additional `resources/*.md` reports for each research worker
 4. **Create a research plan with background agents** — this is a deep research task, so do not do it in one context window. Dispatch multiple **background** subagents with explicit models. At minimum, use:
    - a **bibliography scout** to gather canonical identity sources
    - a **publication historian** to reconstruct the research timeline
    - a **flagship-paper selector** to identify the most representative papers
    - one or more **full-paper readers** to read candidate papers in depth
    - a **style synthesiser** to turn paper-level observations into writing patterns
    - a **persona reviewer** for the final skill-compliance and quality pass
 5. **Require report-first outputs from every researcher** — each research subagent should write a detailed report into the generated skill's `resources/` directory. These reports should preserve findings, not process logs. Prefer proposition-first language such as "the persona consistently frames..." rather than "I searched..." or "I read...".
 6. **Gather canonical identity sources** — locate the strongest sources first:
    - professional or personal website
    - lab homepage or faculty page
    - CV or publication list
    - DBLP profile
    - Google Scholar profile
    - ORCID, Semantic Scholar, or other publication indexes when useful

    Resolve name ambiguity early. If multiple people share the name, use affiliation, coauthors, venues, topics, and homepage evidence to lock onto the correct person.
 7. **Reconstruct the publication trajectory** — build a working map of the person's research career:
    - publication years and career phases
    - recurring topics and problem domains
    - repeated coauthors, labs, or collaborations
    - common venues and venue tiers
    - shifts in research direction over time

    This step prevents the persona from overfitting to one paper or one era.
 8. **Identify flagship papers deliberately** — do not just pick the most cited papers blindly. A "flagship" paper is one that is both representative and likely to reflect the author's real voice and agenda. Consider:
    - high citation count or strong influence
    - publication in prestigious or central venues
    - close fit to the author's recurring research interests
    - signs of major involvement such as first authorship, senior authorship, repeated themes, talks, or close continuity with surrounding work
    - whether the paper is frequently referenced from the author's own site, talks, bios, or publication list

    Select several flagship papers and several additional papers spanning early, middle, and recent career phases.
 9. **Build a representative reading set** — read numerous papers, not just one cluster. Prefer a set that spans:
    - multiple years
    - multiple venues
    - core themes and adjacent themes
    - flagship papers plus supporting papers

    For most personas, aim to read at least **8-12 papers in full** unless the corpus is genuinely small.
 10. **Read the papers in full** — do not infer voice from abstracts alone. For each selected paper, read enough to understand:
    - how the paper frames the problem
    - how contributions are stated
    - how related work is positioned
    - how claims are hedged or sharpened
    - how experiments, methodology, or theory are narrated
    - how the conclusion leaves the reader

    Look at sentence-level style, paragraph structure, section transitions, figure/table narration, and rhetorical pacing.
 11. **Separate author signal from venue and coauthor noise** — some stylistic traits come from the venue template, lab norms, or dominant coauthors rather than the target person. Prefer patterns that recur across multiple papers, years, and coauthor sets. If a trait appears only once, treat it as tentative.
 12. **Extract the persona dimensions explicitly** — synthesise concrete observations about:
    - preferred paper structure and flow
    - opening move in abstracts and introductions
    - how motivation and problem framing are handled
    - how novelty is claimed
    - how related work is discussed
    - level of directness, confidence, and hedging
    - typical tone: crisp, skeptical, expansive, formal, punchy, measured, etc.
    - sentence length, paragraph density, and use of signposting
    - favored kinds of evidence, evaluation, or argumentation
    - common lexical habits and recurring turns of phrase
    - limitations, future work, and conclusion style
 13. **Write the detailed resource set first** — turn the evidence into detailed supporting files under `resources/`. At minimum include:

     - `resources/full-persona.md` — the complete synthesis of research areas, argument habits, and writing style
     - `resources/identity-and-bibliography.md` — identity resolution and canonical source map
     - `resources/publication-history.md` — career phases, topic shifts, venue patterns, and recurring collaborations
     - `resources/flagship-papers.md` — representative paper set with rationale
     - one or more paper-reading reports such as `resources/paper-01.md`, `resources/paper-02.md`, and `resources/paper-03.md`
     - `resources/review-and-revision.md` — the final critique and the revisions it required

     These reports should be rich, evidence-based, and useful on their own. They are not scratch notes.
 14. **Write the concise persona `SKILL.md`** — keep the generated persona skill short and factual. Its job is to help future agents think like and write like the researcher while pointing them to the deeper resources. The main `SKILL.md` should primarily capture:

     - core research interests and recurring problem areas
     - the author's characteristic ways of framing problems, novelty, evidence, and significance
     - the author's writing style, tone, structure, and section-level habits
     - clear do / don't guidance for future writing tasks
     - a resource map pointing to `resources/full-persona.md` and the supporting reports

     If a detail is explanatory evidence rather than operational guidance, move it into `resources/` rather than bloating the main skill file.
 15. **Update repository instructions only when the persona is explicitly central** — if this person is meant to represent the repository as a whole, or is the user whose voice should guide future work broadly, add a brief repo-wide pointer to the generated skill. Do not do this by default.
 16. **Review and revise against skill-writing rules** — run an independent reviewer against the generated `SKILL.md` after the skill and resources exist. The reviewer should verify that the generated skill follows `writing-skills`: purpose-first description, concise scope, numbered procedure, inspect-first opening step, resource references, and done criteria. Revise until the generated skill reads like a good skill rather than a long persona memo.

## Recommended Team Shape

| Role | Purpose | Typical output |
|------|---------|----------------|
| **Bibliography scout** | Find canonical identity and publication sources | `resources/identity-and-bibliography.md` |
| **Publication historian** | Map the research trajectory over time | `resources/publication-history.md` |
| **Flagship-paper selector** | Choose representative high-signal papers | `resources/flagship-papers.md` |
| **Full-paper reader** | Read papers deeply and extract stylistic evidence | `resources/paper-0N.md` reports with persona findings and evidence |
| **Style synthesiser** | Merge evidence into the final persona guidance | `resources/full-persona.md` |
| **Persona reviewer** | Critique overreach, verbosity, and skill-rule violations | `resources/review-and-revision.md` |

## Generated Skill Layout

The default output should be a skill directory like this:

```text
.github/skills/
└── <surname-firstname-persona>/
    ├── SKILL.md
    └── resources/
        ├── full-persona.md
        ├── identity-and-bibliography.md
        ├── publication-history.md
        ├── flagship-papers.md
        ├── paper-01.md
        ├── paper-02.md
        ├── style-synthesis.md
        └── review-and-revision.md
```

The exact filenames can vary, but the pattern should not: **concise main skill, detailed resources beside it**.

## Example Dispatch Pattern

```text
Use the task tool in background mode with explicit models.

Wave 1:
- Bibliography scout — model: gpt-5.4
- Publication historian — model: gpt-5.4
- Flagship-paper selector — model: claude-opus-4.6

Wave 2:
- Full-paper reader A — model: claude-opus-4.6
- Full-paper reader B — model: claude-opus-4.6
- Full-paper reader C — model: claude-opus-4.6

Wave 3:
- Style synthesiser — model: claude-opus-4.6
- Persona reviewer — model: gpt-5.4
```

Each dispatched agent should receive:

1. the exact target person
2. any known aliases, institutions, or websites
3. a clear scope boundary
4. an evidence requirement
5. an output path under the generated skill's `resources/` directory
6. an output format with findings, citations, and confidence notes

## How Research Reports Should Read

Every report written into `resources/` should be detailed and evidence-based, but it should read like a stable finding rather than a work log.

- Prefer **persona findings** over process narration
- Write **what the persona is like**, not **what you did to learn it**
- Separate **high-confidence** patterns from **tentative** ones
- Distinguish **author-driven** traits from **venue-driven** or **coauthor-driven** artifacts
- Cite the papers, profiles, or other sources that support each major claim

Good:

```text
The persona consistently opens introductions by broadening from a systems-level
problem to a sharply defined technical bottleneck, then claims significance in
terms of reliability and scale rather than novelty for novelty's sake.
```

Bad:

```text
I read three papers and noticed that the introductions were pretty similar.
Then I checked the author's webpage and found more evidence.
```

## Prompt Template for a Full-Paper Reader

```markdown
You are reading papers to infer an author's research-writing persona.

Target person: <name>
Assigned papers:
- paper 1
- paper 2
- paper 3

Read the papers in full. Do not rely only on titles or abstracts.

Write your findings to `resources/paper-01.md` in the generated persona skill.

Extract evidence about:
- abstract structure
- introduction style
- claim strength and hedging
- related-work positioning
- paragraph and sentence rhythm
- tone, voice, and argumentative style
- how results and limitations are discussed

Return:
1. Persona findings stated as claims about the author's style
2. Paper-by-paper evidence supporting those findings
3. Traits that seem venue-driven or coauthor-driven rather than author-driven
4. High-confidence and low-confidence inferences
5. Open questions that the style synthesiser should resolve
```

## Prompt Template for the Persona Reviewer

```markdown
Read the generated persona skill at `.github/skills/<surname-firstname-persona>/SKILL.md`
and the detailed synthesis at
`.github/skills/<surname-firstname-persona>/resources/full-persona.md`.

Evaluate the generated `SKILL.md` against the `writing-skills` rules.

Check specifically for:
- purpose-first description
- concise scope and non-verbose body
- numbered procedure
- inspect-first opening step
- resource references instead of duplicated evidence
- done criteria
- factual guidance about research interests, framing habits, and writing style

If the skill fails any check, propose concrete revisions and update
`resources/review-and-revision.md` with the findings.
```

## Generated Persona `SKILL.md` Template

```markdown
---
name: <surname-firstname-persona>
description: >-
  Write research prose in the style of <Full Name> by following their recurring
  research interests, problem framing habits, and characteristic rhetorical
  moves. Use when drafting or revising abstracts, introductions, related work,
  papers, proposals, or reviews that should sound like this researcher.
---

# <Full Name> Persona

## Overview
Use this skill when the task should reflect <Full Name>'s research priorities,
argument style, and writing voice. Keep the writing grounded in the documented
patterns below, and open the files in `resources/` when you need the full
evidence base or more nuance.

## Procedure
1. **Inspect First** — read the current writing task, venue rules, repository
   style guidance, and any nearby source material. Venue or task requirements
   override persona preferences.
2. **Read the detailed synthesis** — open `resources/full-persona.md` and any
   task-relevant supporting reports before drafting.
3. **Match the research lens** — stay close to the author's recurring interests,
   favored problem framing, and preferred significance claims.
4. **Match the writing style** — follow the documented tone, section flow,
   evidence habits, and claim strength. Do not imitate superficial quirks.
5. **Respect the limits** — if the evidence is mixed or the task is far outside
   the researcher's usual domain, use the closest high-confidence patterns and
   avoid overclaiming.

## Core Persona Guidance
- Research areas and recurring interests
- Problem framing habits
- Writing tone and structure
- Do / don't guidance for future drafts

## Resources
- `resources/full-persona.md` — complete persona synthesis
- `resources/flagship-papers.md` — representative paper set
- `resources/review-and-revision.md` — final critique and fixes

## Done Criteria
- The response reflects the documented persona rather than generic academic prose
- Research interests, framing habits, and writing style are all represented
- Venue or task-specific requirements still take priority where they conflict
- The draft stays within the high-confidence bounds documented in `resources/`
```

## Detailed Persona Resource Template

Use `resources/full-persona.md` for the full synthesis:

```markdown
# <Full Name> Full Persona

## Who This Persona Represents
Name, role, scope, and why this persona exists in the repository.

## Evidence Base
- Canonical websites and profiles
- Publication indexes consulted
- Papers read in full

## Research Areas and Recurring Interests
- ...

## Career-Phase Overview
- ...

## Core Writing Patterns
- ...

## Voice and Tone
- ...

## Section-by-Section Preferences
### Abstract
### Introduction
### Related Work
### Method / Approach
### Results / Evaluation
### Conclusion

## Do / Don't Guidance
### Do
- ...

### Don't
- ...

## Limits and Confidence
- ...
```

## Research Report Template

Use a structure like this for reports in `resources/`:

```markdown
# <Report Title>

## Persona Findings
- Evidence-backed claims about the author's research interests, framing habits,
  or writing style

## Evidence
- Specific papers, profiles, quotes, or recurring patterns that support each
  finding

## Author vs. Venue / Coauthor Signal
- Which traits appear stable across contexts, and which may be inherited from
  collaborators or venue norms

## Confidence and Limits
- High-confidence findings
- Tentative findings
- Open questions
```

## Rules and Constraints

- Do **not** infer a persona from one or two famous papers alone.
- Do **not** confuse topical similarity with stylistic similarity.
- Do **not** assume the most cited paper is automatically the most representative.
- Do **not** rely solely on DBLP or Google Scholar metadata; read the actual papers.
- Do **not** overstate confidence when the corpus is noisy or highly collaborative.
- Do **not** imitate superficial quirks while missing deeper argumentative structure.
- Do **not** let the generated `SKILL.md` turn into a long biographical memo; move depth into `resources/`.
- Do **not** let research worker outputs vanish into chat history; preserve them as detailed reports under `resources/`.
- Do **not** write research reports as process diaries; write them as durable findings about the persona.
- Do **not** update `.github/copilot-instructions.md` unless the persona is intended to represent the user or repository more broadly.

## Done Criteria

- Canonical identity sources were gathered and disambiguated
- Publication history was mapped across the research career
- Flagship papers were selected intentionally rather than mechanically
- Numerous papers spanning the career were read in full
- The persona distinguishes stable author traits from venue or coauthor artifacts
- A generated skill directory was created with a concise `SKILL.md` and detailed `resources/`
- Each research worker produced a detailed report in the generated skill's `resources/` directory
- `resources/full-persona.md` captures the full synthesis of interests, framing, and writing style
- The main `SKILL.md` stays concise and factual, and points to the detailed resources
- `.github/copilot-instructions.md` was updated when the persona represents the repository or user broadly
- An independent reviewer checked the generated `SKILL.md` for specificity, evidence quality, and compliance with `writing-skills`
