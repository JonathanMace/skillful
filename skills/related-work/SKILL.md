---
name: related-work
description: >-
  Find and evaluate academic and practitioner related work by decomposing a
  subject into orthogonal topic areas, dispatching parallel background
  researchers, and synthesising a balanced set of recent and foundational
  sources. Use when preparing a related-work section, literature review,
  research memo, prior-art scan, or technical landscape analysis.
license: MIT
---

# Finding Related Work Thoroughly

Use this skill when the goal is not just to "find some papers," but to build a credible map of the field. The core method is to break the subject into multiple orthogonal slices, assign those slices to background researchers, read actual candidate sources rather than citing from titles alone, and synthesise a balanced set of recent and classic work.

For broader multi-agent orchestration, see the `agent-design-patterns` skill and its `research-team` pattern. For a final critical pass on the written related-work section, see `review-document`.

## Procedure

1. **Inspect First** — read the problem statement, draft, abstract, proposal, or prompt that motivated the search. Identify:
   - the central claim or topic
   - named authors, advisors, labs, or institutions to prioritise
   - target venues, conferences, or communities if known
   - any existing bibliography, seed papers, or keywords
   - whether the deliverable is a research paper, survey, memo, grant, or product landscape
2. **Build a topic decomposition** — split the subject into 4-8 orthogonal areas of related work. These should represent distinct lenses rather than synonyms. Typical buckets include:
   - direct technical approaches
   - adjacent problem formulations
   - enabling methods or infrastructure
   - evaluation methods or benchmarks
   - application domains
   - practitioner/industry discussion
3. **Create a search plan with background agents** — do not run the whole search serially in one context window. Dispatch multiple background agents, each with an explicit model and mandate. At minimum:
   - one academic-search agent per topic area
   - one citation-graph chaser for the strongest seed papers
   - one practitioner-landscape agent for blogs, newsletters, open-source projects, discussions, and industrial writeups
4. **Search each academic area thoroughly** — start with Google Scholar for every topic area. Use multiple query phrasings, not just one keyword string. Search:
   - the exact terms from the problem statement
   - nearby terminology and older names for the same idea
   - broader framing terms
   - author names, lab names, and venue names when relevant
   - "survey", "benchmark", "review", or "system" variants when useful
5. **Balance recent and foundational work explicitly** — for each topic area, collect both:
   - **recent work** from the last 3 years
   - **foundational older work** that the field still builds on

   Do not let the bibliography drift into only classic papers. If a topic area has no recent work, say so explicitly rather than silently backfilling with old citations.
6. **Rank candidates with clear preferences** — prefer sources that are both relevant and credible. In rough order:
   - direct relevance to the topic area
   - strong fit to the intended audience and target venue
   - papers from top-tier venues
   - papers from venues where the user or named authors have published before
   - highly cited papers, especially for foundational coverage
   - strong recent papers even if citation counts are still low
   - work from respected labs, universities, and research groups

   Venue prestige and citation count are tie-breakers, not substitutes for relevance.
7. **Read actual candidate papers** — download or otherwise access the paper itself whenever possible. Read enough of the real source to verify what it actually contributes:
   - abstract and introduction for framing
   - problem setup and method section for technical fit
   - experiments, evaluation, or case studies for evidence
   - conclusion and limitations for scope boundaries

   Do **not** cite papers based only on title matches or shallow snippets when the actual paper is accessible.
8. **Follow the citation graph in both directions** — when a paper is highly relevant:
   - look backward at its references to find the foundational work it builds on
   - look forward at "cited by" results to find newer papers on the same theme
   - prioritise the forward citation graph for papers from the last 3 years, since that is where recent follow-on work appears
9. **Run the practitioner track separately** — treat non-academic material as a first-class workstream, not an afterthought. Use a separate expert to search for:
   - blog posts and technical essays
   - industrial newsletters
   - conference talks, workshops, and discussion threads
   - open-source projects and their issue trackers
   - standards efforts, benchmarks, and tooling ecosystems

   This track should surface what practitioners argue about, what tools exist, and where the field is moving outside formal publications.
10. **Saturate the bibliography before stopping** — for research-paper workflows, aim for at least **30 relevant citations** spread across the topic areas, not 30 variants of the same paper cluster. Keep going until:
   - every topic area has representative sources
   - the recent-work coverage is credible
   - the foundational lineage is clear
   - the practitioner landscape has been checked separately
11. **Produce a structured synthesis** — organise the result by topic area, not by the order you found papers. For each source, note:
   - why it is relevant
   - whether it is recent, foundational, or practitioner-facing
   - what distinct contribution it makes
   - how it connects to nearby papers
   - whether it should likely appear in the final related-work section
12. **Identify absences and open questions** — explicitly record where evidence is weak, where the recent literature is thin, where terminology is fragmented, or where a practitioner conversation exists without strong academic treatment.

## Recommended Team Shape

| Role | Purpose | Typical output |
|------|---------|----------------|
| **Topic-area researcher** | Search one orthogonal academic slice deeply | Ranked papers with notes and gaps |
| **Citation-graph chaser** | Expand from the strongest seed papers | Older foundations plus newer descendants |
| **Venue and author scout** | Identify preferred venues and author-specific publication history | Venue priority list and author-relevant leads |
| **Practitioner landscape analyst** | Cover non-paper materials separately | Blogs, OSS projects, discussions, and industry signals |
| **Synthesis lead** | Merge all streams into one related-work map | Grouped bibliography and recommendations |

If the user names authors or advisors, the venue-and-author scout should inspect their Google Scholar profiles, CVs, homepages, or publication lists and bias the venue scan accordingly.

## Example Dispatch Pattern

```text
Use the task tool in background mode with explicit models.

Wave 1:
- Topic-area researcher A — model: gpt-5.4
- Topic-area researcher B — model: gpt-5.4
- Topic-area researcher C — model: gpt-5.4
- Practitioner landscape analyst — model: gpt-5.4

Wave 2:
- Citation-graph chaser — model: claude-opus-4.6
- Synthesis lead — model: claude-opus-4.6
```

Each background agent should get:

1. the exact topic area it owns
2. the recency requirement (last 3 years plus classics)
3. the venue and citation preferences
4. a requirement to read actual candidate papers
5. an output format that includes ranked sources, short annotations, and unresolved gaps

## Prompt Template for an Academic Topic-Area Agent

```markdown
You are a literature researcher covering one slice of a related-work search.

Topic area: retrieval-augmented code generation for software engineering

Search thoroughly using Google Scholar and related web sources. Find both:
- strong recent papers from the last 3 years
- foundational older papers still relevant to the topic

Prefer:
- top-tier venues
- venues where the named authors have published before
- highly cited foundational papers
- strong recent papers even when citation counts are still maturing

Read actual candidate papers, not just titles or snippets. Follow citation
links from the strongest papers to find older foundations and newer follow-ons.

Return:
1. Top candidate papers
2. Why each paper matters
3. Which are recent vs foundational
4. Missing areas or ambiguous terminology
5. Suggested next searches
```

## Prompt Template for the Practitioner Track

```markdown
You are a practitioner landscape analyst working in parallel with academic
paper searchers.

Investigate non-academic related work on the topic:
- blogs and essays
- industrial newsletters
- open-source projects
- talks, discussions, benchmarks, and tooling

Focus on what practitioners are actually building, debating, and adopting.
Treat this as a separate workstream, not a supplement to the paper list.

Return:
1. Important non-paper sources
2. What themes they emphasise
3. Which open-source projects or communities matter most
4. Where practitioner discussion diverges from the academic literature
```

## Rules and Constraints

- Do **not** search only one phrasing of the topic; reformulate the search space.
- Do **not** stop after finding a few canonical old papers; make recent coverage explicit.
- Do **not** rely on title matching alone when full texts are accessible.
- Do **not** treat citation count as a proxy for relevance.
- Do **not** collapse practitioner materials into the academic track; pursue them as a separate expert.
- Do **not** produce one undifferentiated bibliography; organise by orthogonal topic area.
- When the deliverable is a research paper, **30 relevant citations is a floor, not a ceiling**, unless the field is genuinely tiny.

## Done Criteria

- The topic has been decomposed into multiple orthogonal related-work areas
- Parallel background agents were used rather than one serial search pass
- Google Scholar searches were run for each academic area
- Recent work from the last 3 years and older foundational work are both represented
- Actual candidate papers were read closely enough to verify relevance
- Citation graphs were followed for the strongest papers
- Venue, citation, and author-history preferences were used appropriately
- Non-academic related work was pursued by a separate expert
- For research-paper workflows, the result includes at least 30 relevant citations across the topic areas
- The final output groups sources by area and explains why each source matters
