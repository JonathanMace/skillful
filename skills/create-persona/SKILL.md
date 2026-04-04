---
name: create-persona
description: >-
  Construct a research-writing persona by deeply studying a specific person's
  publication record, flagship papers, venues, and stylistic patterns, then
  encoding the findings into a reusable repository artifact. Use when creating
  a persona for the user, a recurring author, an advisor, or another researcher
  whose voice should shape future writing in the repo.
license: MIT
---

# Creating a Meaningful Research Persona

Use this skill when the repository should learn how a specific researcher tends to think, argue, structure papers, and sound on the page. This is not a shallow "write like X" exercise. The goal is to build a high-quality persona from primary evidence across that person's research career, then encode it into a reusable repository artifact that improves future writing tasks.

For literature-search methodology, see `related-work`. For multi-agent orchestration, see `agent-design-patterns` and its `research-team` pattern. For final critique of the persona artifact, see `review-document`. For repo-wide identity guidance, see `writing-custom-instructions`.

## Procedure

1. **Inspect First** — read the request carefully and identify:
   - the target person's full name and any aliases
   - whether this is the user, a named advisor, a lab lead, or another researcher
   - whether the resulting persona should represent the repository as a whole
   - any existing persona files, author notes, drafts, or house-style instructions
   - whether the user explicitly wants a flat file such as `.github/skills/surname-firstname-persona.md` or a standard skill directory
2. **Create a research plan with background agents** — this is a deep research task, so do not do it in one context window. Dispatch multiple **background** subagents with explicit models. At minimum, use:
   - a **bibliography scout** to gather canonical identity sources
   - a **publication historian** to reconstruct the research timeline
   - a **flagship-paper selector** to identify the most representative papers
   - one or more **full-paper readers** to read candidate papers in depth
   - a **style synthesiser** to turn paper-level observations into writing patterns
   - an optional **persona reviewer** for an independent final pass
3. **Gather canonical identity sources** — locate the strongest sources first:
   - professional or personal website
   - lab homepage or faculty page
   - CV or publication list
   - DBLP profile
   - Google Scholar profile
   - ORCID, Semantic Scholar, or other publication indexes when useful

   Resolve name ambiguity early. If multiple people share the name, use affiliation, coauthors, venues, topics, and homepage evidence to lock onto the correct person.
4. **Reconstruct the publication trajectory** — build a working map of the person's research career:
   - publication years and career phases
   - recurring topics and problem domains
   - repeated coauthors, labs, or collaborations
   - common venues and venue tiers
   - shifts in research direction over time

   This step prevents the persona from overfitting to one paper or one era.
5. **Identify flagship papers deliberately** — do not just pick the most cited papers blindly. A "flagship" paper is one that is both representative and likely to reflect the author's real voice and agenda. Consider:
   - high citation count or strong influence
   - publication in prestigious or central venues
   - close fit to the author's recurring research interests
   - signs of major involvement such as first authorship, senior authorship, repeated themes, talks, or close continuity with surrounding work
   - whether the paper is frequently referenced from the author's own site, talks, bios, or publication list

   Select several flagship papers and several additional papers spanning early, middle, and recent career phases.
6. **Build a representative reading set** — read numerous papers, not just one cluster. Prefer a set that spans:
   - multiple years
   - multiple venues
   - core themes and adjacent themes
   - flagship papers plus supporting papers

   For most personas, aim to read at least **8-12 papers in full** unless the corpus is genuinely small.
7. **Read the papers in full** — do not infer voice from abstracts alone. For each selected paper, read enough to understand:
   - how the paper frames the problem
   - how contributions are stated
   - how related work is positioned
   - how claims are hedged or sharpened
   - how experiments, methodology, or theory are narrated
   - how the conclusion leaves the reader

   Look at sentence-level style, paragraph structure, section transitions, figure/table narration, and rhetorical pacing.
8. **Separate author signal from venue and coauthor noise** — some stylistic traits come from the venue template, lab norms, or dominant coauthors rather than the target person. Prefer patterns that recur across multiple papers, years, and coauthor sets. If a trait appears only once, treat it as tentative.
9. **Extract the persona dimensions explicitly** — synthesise concrete observations about:
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
10. **Write the persona artifact** — create a repo-local artifact in `.github/skills/` that captures the writing persona in detail.

    - If the user explicitly asked for a flat file, create `.github/skills/surname-firstname-persona.md`.
    - Otherwise, if the repository wants a standard repo-local skill layout, create `.github/skills/<surname-firstname-persona>/SKILL.md` following `writing-skills` conventions.

    The artifact should explain the author's preferred research-writing style, not just biographical facts.
11. **Update repository instructions when the persona is central** — if this person is meant to represent the repository as a whole, or is the user whose voice should guide future work, add a brief paragraph to `.github/copilot-instructions.md` describing that identity and pointing future agents to the persona artifact.
12. **Review and refine the persona** — run an independent reviewer against the artifact. The reviewer should check whether the persona is evidence-based, non-generic, and specific enough to change future writing behavior in meaningful ways.

## Recommended Team Shape

| Role | Purpose | Typical output |
|------|---------|----------------|
| **Bibliography scout** | Find canonical identity and publication sources | Clean source list, resolved identity, seed corpus |
| **Publication historian** | Map the research trajectory over time | Timeline, topic clusters, venue patterns |
| **Flagship-paper selector** | Choose representative high-signal papers | Ranked flagship set with rationale |
| **Full-paper reader** | Read papers deeply and extract stylistic evidence | Structured annotations on voice, framing, and structure |
| **Style synthesiser** | Merge evidence into persona guidance | Draft persona artifact with patterns and rules |
| **Persona reviewer** | Critique overreach, vagueness, or unsupported claims | Revision notes and confidence checks |

## What the Persona Artifact Should Contain

The persona artifact should usually include these sections:

1. **Who this persona represents** — name, role, scope, and why this persona matters in the repository
2. **Evidence base** — websites, profiles, and the set of papers read
3. **Career-phase overview** — how the style evolved over time, if relevant
4. **Core writing patterns** — recurring structural and rhetorical habits
5. **Voice and tone** — how the author sounds on the page
6. **Research style** — how the author frames contributions, evidence, and significance
7. **Preferred moves by section** — abstract, introduction, related work, method, results, conclusion
8. **Do / Don't guidance** — actionable instructions for future agents trying to write in this style
9. **Limits of the persona** — where the evidence is thin, mixed, or uncertain

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
5. an output format with findings, citations, and confidence notes

## Prompt Template for a Full-Paper Reader

```markdown
You are reading papers to infer an author's research-writing persona.

Target person: <name>
Assigned papers:
- paper 1
- paper 2
- paper 3

Read the papers in full. Do not rely only on titles or abstracts.

Extract evidence about:
- abstract structure
- introduction style
- claim strength and hedging
- related-work positioning
- paragraph and sentence rhythm
- tone, voice, and argumentative style
- how results and limitations are discussed

Return:
1. Paper-by-paper observations
2. Recurring style patterns across the set
3. Traits that seem venue-driven or coauthor-driven rather than author-driven
4. High-confidence and low-confidence inferences
```

## Persona Artifact Template

```markdown
# <Surname, Firstname> Persona

## Overview
Who this person is and why this persona exists in the repository.

## Evidence Base
- Website / profile links
- Publication indexes consulted
- Papers read in full

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

## Do / Don't
### Do
- ...

### Don't
- ...

## Limits and Confidence
- ...
```

## Rules and Constraints

- Do **not** infer a persona from one or two famous papers alone.
- Do **not** confuse topical similarity with stylistic similarity.
- Do **not** assume the most cited paper is automatically the most representative.
- Do **not** rely solely on DBLP or Google Scholar metadata; read the actual papers.
- Do **not** overstate confidence when the corpus is noisy or highly collaborative.
- Do **not** imitate superficial quirks while missing deeper argumentative structure.
- Do **not** update `.github/copilot-instructions.md` unless the persona is intended to represent the user or repository more broadly.

## Done Criteria

- Canonical identity sources were gathered and disambiguated
- Publication history was mapped across the research career
- Flagship papers were selected intentionally rather than mechanically
- Numerous papers spanning the career were read in full
- The persona distinguishes stable author traits from venue or coauthor artifacts
- A detailed persona artifact was created in `.github/skills/`
- `.github/copilot-instructions.md` was updated when the persona represents the repository or user broadly
- An independent reviewer checked the persona for specificity and evidence quality
