---
title: Research Workflow
summary: Build an evidence-based persona corpus and coordinate background researchers who each contribute durable findings in the generated skill's resources directory.
trigger: Use for identity resolution, publication mapping, flagship-paper selection, paper reading, and report-first subagent orchestration.
---

# Research Workflow

This guide covers the evidence-gathering side of persona creation. The goal is to build a reliable corpus, assign the right reading work to background researchers, and preserve each researcher's findings as durable resources inside the generated persona skill.

## Procedure

1. **Inspect First** — confirm the target person's name, aliases, affiliations, scope, expected skill location, and any existing persona notes or house-style instructions.
2. **Create the persona skill scaffold before deep research** — create the target skill directory and a `resources/` subdirectory up front so every researcher has a stable place to write findings.
3. **Create a research plan with background subagents** — this is a deep research task, so dispatch multiple **background** subagents with explicit models. At minimum, use:
   - a **bibliography scout** for identity resolution and canonical sources
   - a **publication historian** for career phases and topic shifts
   - a **flagship-paper selector** for representative paper choice
   - one or more **full-paper readers** for close reading
   - a **style synthesiser** for the final merge
4. **Gather canonical identity sources** — prioritize the strongest sources first:
   - professional or personal website
   - lab homepage or faculty page
   - CV or publication list
   - DBLP profile
   - Google Scholar profile
   - ORCID, Semantic Scholar, or other publication indexes when useful

   Resolve ambiguity early. If multiple people share the name, use affiliation, coauthors, venues, topics, and homepage evidence to lock onto the correct person.
5. **Reconstruct the publication trajectory** — map the person's research career across years, topic clusters, venue patterns, collaborations, and major shifts. This prevents the persona from overfitting to one paper or one era.
6. **Identify flagship papers deliberately** — choose papers that are both influential and representative of the author's recurring agenda. Do not just sort by citation count.
7. **Build a representative reading set** — span multiple years, venues, themes, and collaboration contexts. For most personas, aim to read at least **8-12 papers in full** unless the corpus is genuinely small.
8. **Read the papers in full** — do not infer voice from abstracts alone. Study problem framing, contribution statements, related-work positioning, claim strength, narrative pacing, section transitions, results discussion, and conclusion style.
9. **Require report-first outputs from every researcher** — each research subagent should write a detailed report into the generated skill's `resources/` directory using `templates/research-report-template.md`. These reports should preserve findings, not process logs.
10. **Separate author signal from venue and coauthor noise** — prefer traits that recur across papers, years, and coauthor sets. If a trait appears once, treat it as tentative.
11. **Extract persona dimensions explicitly** — synthesise observations about:
    - research areas and recurring problem domains
    - preferred paper structure and flow
    - opening move in abstracts and introductions
    - how motivation, novelty, and significance are framed
    - how related work is positioned
    - level of directness, confidence, and hedging
    - sentence rhythm, paragraph density, and signposting habits
    - favored evidence styles and argumentative moves
    - recurring lexical habits or turns of phrase
    - limitations, future work, and conclusion style
12. **Hand off to `guides/artifact-shape.md`** — once the evidence base is stable, switch to shaping the final generated persona skill and resources.

## Recommended Team Shape

| Role | Purpose | Typical output |
|------|---------|----------------|
| **Bibliography scout** | Find canonical identity and publication sources | `resources/identity-and-bibliography.md` |
| **Publication historian** | Map the research trajectory over time | `resources/publication-history.md` |
| **Flagship-paper selector** | Choose representative high-signal papers | `resources/flagship-papers.md` |
| **Full-paper reader** | Read papers deeply and extract stylistic evidence | `resources/paper-0N.md` |
| **Style synthesiser** | Merge evidence into the final persona guidance | `resources/full-persona.md` |

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
Use `templates/research-report-template.md` as the output shape.

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

## Rules and Constraints

- Do **not** infer a persona from one or two famous papers alone.
- Do **not** confuse topical similarity with stylistic similarity.
- Do **not** assume the most cited paper is automatically the most representative.
- Do **not** rely solely on DBLP or Google Scholar metadata; read the actual papers.
- Do **not** overstate confidence when the corpus is noisy or highly collaborative.
- Do **not** let research worker outputs vanish into chat history; preserve them under `resources/`.
- Do **not** write research reports as process diaries; write them as durable findings about the persona.

## Done Criteria

- Canonical identity sources were gathered and disambiguated
- Publication history was mapped across the research career
- Flagship papers were selected intentionally rather than mechanically
- Numerous papers spanning the career were read in full
- The persona distinguishes stable author traits from venue or coauthor artifacts
- Each research worker produced a detailed report in the generated skill's `resources/` directory
