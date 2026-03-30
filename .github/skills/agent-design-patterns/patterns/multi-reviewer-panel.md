# Multi-Reviewer Panel

## What It Is

A set of N agents (typically 2–4) that review the same artifact from **non-overlapping perspectives**, invoked in parallel. Each reviewer has a clear mandate — a defined scope of what it reviews and an explicit statement of what it does NOT review. A parent orchestrator spawns all reviewers simultaneously and synthesises their results into a unified assessment.

This is distinct from running one general-purpose reviewer multiple times. The power comes from **structural diversity**: each reviewer is blind to the others' concerns, which prevents groupthink and ensures coverage of dimensions that a single reviewer would trade off against each other (e.g., narrative quality vs technical correctness).

## Why It Works

- **Coverage without redundancy** — each reviewer owns a distinct slice of the quality surface. No two reviewers comment on the same issue, because their scopes are explicitly partitioned.
- **Parallel execution** — reviewers run in separate context windows with no shared state, so they execute simultaneously. A three-reviewer panel takes the same wall-clock time as one reviewer.
- **Calibrated intensity** — you can invoke the full panel for major milestones and a single lightweight reviewer for minor changes, matching review cost to change significance.
- **Consistent output** — structured output templates make it straightforward for the orchestrator to synthesise results, and for humans to scan findings quickly.

## How to Implement

### 1. Define Reviewer Scopes

Partition the quality surface into 2–4 non-overlapping domains. Common partitions:

| Reviewer | Focus | Example concerns |
|----------|-------|-----------------|
| **Domain / Significance** | Novelty, narrative, audience fit | "Does this solve a real problem?", "Who would use this?" |
| **Correctness / Rigour** | Technical accuracy, edge cases, flaws | "Is this logic sound?", "What breaks under load?" |
| **Methodology / Reproducibility** | Process quality, verifiability | "Can someone else reproduce this?", "Are assumptions documented?" |
| **Style / Conventions** | Formatting, consistency, standards compliance | "Does this follow project conventions?" |

Three reviewers is the sweet spot for most projects. Four is justified when style/convention checking is complex enough to warrant a dedicated reviewer.

### 2. Author Reviewer Instructions

Each reviewer needs:

- A **role statement** defining its expertise and perspective
- A **scope section** listing what it reviews
- A **"What You Do NOT Focus On" section** explicitly naming the other reviewers and their domains
- A **structured output template** with consistent sections (severity, finding, recommendation)
- A **severity scale** shared across all reviewers (e.g., critical / major / minor / nit)

Example structure for a reviewer instruction file:

```markdown
# Reviewer A — Domain and Significance

You are a senior domain expert. You assess whether the work is novel,
significant, and well-positioned for its intended audience.

## What You Review
- Novelty and contribution relative to prior work
- Narrative clarity and logical flow
- Audience fit and framing

## What You Do NOT Focus On
- Technical correctness and edge cases (Reviewer B handles this)
- Methodology, reproducibility, and process (Reviewer C handles this)

## Output Format
For each finding, report:

### [SEVERITY] Brief title
**Finding**: What you observed.
**Recommendation**: What should change.
```

### 3. Build the Orchestrator

The parent agent (or skill) spawns all reviewers in parallel using the `task` tool. Each reviewer runs in its own context window, reads its instruction file, and produces structured output.

```markdown
# In the parent agent's prompt:

When asked to review, spawn reviewers in parallel using the `task` tool:

1. **Reviewer A** (domain/significance) — agent_type: "general-purpose",
   prompt: "Read `.github/agents/reviewer-panel/reviewers/domain.md`.
   Then review this artifact: {artifact}"
2. **Reviewer B** (correctness/rigour) — agent_type: "general-purpose",
   prompt: "Read `.github/agents/reviewer-panel/reviewers/correctness.md`.
   Then review this artifact: {artifact}"
3. **Reviewer C** (methodology) — agent_type: "general-purpose",
   prompt: "Read `.github/agents/reviewer-panel/reviewers/methodology.md`.
   Then review this artifact: {artifact}"

After all reviewers complete, synthesise a unified report:
- Group findings by severity (critical first)
- Note any cross-cutting themes
- Provide a summary recommendation (accept / revise / reject)
```

### 4. Implement Graduated Intensity

Not every change warrants the full panel. Define escalation tiers:

| Change size | Review approach |
|-------------|----------------|
| Trivial (typos, formatting) | No review, or a single lightweight check |
| Minor (small feature, bug fix) | One reviewer — pick the most relevant |
| Major (new module, architecture change) | Full panel |
| Milestone (release, submission, major decision) | Full panel + synthesis discussion |

The orchestrator should assess change significance before deciding which tier to invoke.

## Gotchas

- **Without explicit exclusion boundaries, reviewers overlap.** If you don't tell Reviewer A to ignore correctness, it will comment on correctness — producing duplicate findings that waste synthesis effort and confuse the reader.
- **Too many reviewers cause diminishing returns.** Beyond 4 reviewers, the synthesis overhead exceeds the marginal coverage gain. If you need more perspectives, nest them (e.g., Reviewer B spawns sub-reviewers for security vs logic).
- **Graduated intensity matters.** Invoking a 3-reviewer panel for a one-line typo fix is wasteful and trains users to ignore review output. Match panel size to change significance.
- **Shared severity scales are essential.** If Reviewer A's "critical" means "important to address" but Reviewer B's "critical" means "blocks release", the synthesised report is incoherent. Define the scale once and reference it from all reviewers.
- **The orchestrator must add value.** Don't just concatenate reviewer outputs. The synthesis should identify cross-cutting themes, resolve contradictions, and produce a clear overall recommendation.

## Example

A documentation review panel for a technical blog:

- **Reviewer A (Audience)**: Assesses whether the post is clear, engaging, and pitched at the right level. Does NOT check technical accuracy.
- **Reviewer B (Technical)**: Verifies all code samples work, all claims are accurate, and all links resolve. Does NOT comment on writing style.
- **Reviewer C (Standards)**: Checks formatting, accessibility, SEO metadata, and house style compliance. Does NOT assess content quality.

The orchestrator spawns all three in parallel, collects structured findings, groups them by severity, and produces a single report with a publish/revise/hold recommendation.
