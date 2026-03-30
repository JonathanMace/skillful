---
title: Mentor Constellation with Referral Graph
summary: >-
  Read-only advisory agents forming a referral network — each knows its limits
  and explicitly routes to the right specialist. Provides diverse perspectives
  without any single agent trying to be everything.
trigger: >-
  Advisory support where users need guidance from different domains but
  shouldn't have to know which specialist to ask.
---

# Mentor Constellation with Referral Graph

## What It Is

A set of advisory agents (typically 2–4) that form a **referral network** — each has a distinct expertise domain, a distinct communication style, and explicit knowledge of when to route the user to a different mentor. Critically, mentors are **read-only**: they can search and read files but cannot edit, execute, or modify anything. They advise; they do not act.

The referral graph is what distinguishes this from simply having multiple unrelated advisors. Each mentor's prompt explicitly names the other mentors and specifies when to refer: "If the user needs X, suggest they talk to @other-mentor." The graph should be connected — every mentor can route to every other mentor, directly or transitively.

## Why It Works

- **Diverse perspectives without overreach** — each mentor stays in its lane because it knows its blind spots and has a named colleague to defer to.
- **Structural safety via tool constraints** — advisory agents constrained to `[read, search]` or `[read, search, web]` are physically prevented from causing side effects, regardless of how persuasive their advice is. This is not a prompt convention; it is an architectural guarantee.
- **Memorable personas** — giving each mentor a distinct voice (formal academic, blunt practitioner, empathetic listener) makes them memorable and helps users learn when to invoke each one. Voice is not decoration; it is a UX mechanism.
- **Self-organising routing** — users don't need to know which mentor to ask. Any mentor will either answer within its domain or explicitly refer to the right one.

## How to Implement

### 1. Define Mentor Domains and Blind Spots

Map out 2–4 complementary areas of expertise. For each mentor, identify:

- **What it knows** — the domain it advises on
- **What it doesn't know** — its explicit blind spots
- **Who to refer to** — which mentor covers the blind spot

| Mentor | Domain | Blind spots | Refers to |
|--------|--------|-------------|-----------|
| **Academic** | Theory, literature, formal methods | Practical implementation, emotional support | Practitioner, Supporter |
| **Practitioner** | Implementation, shipping, pragmatics | Deep theory, emotional wellbeing | Academic, Supporter |
| **Supporter** | Morale, decision fatigue, overwhelm | All technical questions | Academic, Practitioner |

### 2. Constrain Tools Structurally

This is the most important implementation detail: **advisory agents must never have `edit` or `execute` tools.**

```yaml
# Correct — read-only advisory agent
tools: ["read", "search"]

# Also acceptable — adds web research capability
tools: ["read", "search", "web"]

# WRONG — advisory agent with edit capability
tools: ["read", "search", "edit"]  # Will edit files, guaranteed
```

The tool constraint is a safety boundary, not a suggestion. An advisory agent that can edit files **will** edit files — models are helpful by default and will act on their own advice if they have the tools to do so.

### 3. Author Mentor Prompts with Referral Instructions

Each mentor's prompt must include:

- A **role statement** with a distinct voice/persona
- An **expertise scope** defining what it advises on
- An **explicit referral section** naming other mentors and when to refer
- A **constraint reminder** that it advises but does not implement

Example structure:

```markdown
---
name: domain-expert
description: >-
  Senior domain expert who provides theoretical guidance, literature context,
  and formal analysis. Refers practical implementation questions to the
  practitioner agent and emotional/motivational questions to the supporter agent.
tools: ["read", "search", "web"]
---

You are a senior domain expert with deep theoretical knowledge. You communicate
in a formal, precise style — thorough and well-referenced.

## What You Advise On
- Theoretical foundations and formal methods
- Literature review and related work positioning
- Analytical approaches and mathematical frameworks

## What You Do NOT Advise On
- Practical implementation details — refer the user to @practitioner
- Emotional support or decision fatigue — refer the user to @supporter

## Referral Protocol
When a question falls outside your expertise, say so explicitly and name the
appropriate mentor. Example: "That's an implementation question — I'd suggest
talking to @practitioner, who can advise on the pragmatics of shipping this."

## Constraints
You are an advisor. You read and analyse but you do not modify files, run
commands, or implement changes. If the user needs something done, refer them
to an operational agent.
```

### 4. Design the Referral Graph

The referral relationships should form a **connected graph**: every mentor can reach every other mentor through at most one hop. This ensures users are never stuck in a dead-end conversation.

```
Academic ←→ Practitioner
   ↕              ↕
      Supporter
```

In practice, a fully connected graph (every mentor refers to every other mentor) works well for small constellations (2–4 mentors). For larger groups, ensure transitivity — if Mentor A only refers to Mentor B, and Mentor B refers to Mentor C, then A can still reach C through B.

### 5. Give Each Mentor a Distinct Voice

Voice is not cosmetic — it serves three purposes:

1. **Recognition**: Users learn to identify mentors by how they communicate, making it natural to invoke the right one.
2. **Expectation setting**: A blunt, informal voice signals "I'll give you the pragmatic answer." A formal, thorough voice signals "I'll give you the rigorous answer."
3. **Diversity of thought**: Different communication styles naturally produce different kinds of advice, even on overlapping topics.

| Voice | Characteristics | Suitable for |
|-------|----------------|-------------|
| **Formal academic** | Precise, well-referenced, thorough, cautious | Theory, analysis, literature |
| **Blunt practitioner** | Direct, opinionated, action-oriented | Implementation, pragmatics, shipping |
| **Empathetic listener** | Warm, patient, non-technical, validating | Overwhelm, indecision, morale |
| **Socratic questioner** | Question-driven, clarifying, never gives direct answers | Problem framing, assumption testing |

## Gotchas

- **Without explicit referral instructions, mentors try to answer everything.** Models are helpful by default. If you don't tell a mentor "refer implementation questions to @practitioner", it will attempt a mediocre answer instead of routing correctly. The referral instruction must be specific and name the other agent.
- **The read-only tool constraint is structural, not advisory.** Don't rely on prompt instructions like "you should not edit files" — models sometimes ignore soft constraints under pressure. Omit `edit` and `execute` from the tool list entirely. A mentor without those tools **cannot** cause side effects, full stop.
- **Don't create mentors for operational problems.** A mentor can advise "you should refactor module X into smaller functions" but it should not do the refactoring. If you need an agent that acts on advice, that's an operational agent, not a mentor. Keep the boundary clean.
- **Voice and persona require iteration.** The first draft of a mentor's voice will be generic. Test it with real prompts and refine until the voice is distinctive enough that you can identify the mentor from a blind response. If two mentors sound interchangeable, their voices need more differentiation.
- **Don't over-populate the constellation.** Each additional mentor adds referral complexity (every existing mentor needs to know about the new one) and selection overhead (users must learn when to invoke each one). Start with 2–3 and add only when a clear gap emerges.

## Example

A project advisory constellation for a software team:

- **Architect** (formal, theoretical): Advises on system design, trade-off analysis, and technical debt. Speaks in precise, structured paragraphs. Refers implementation questions to Pragmatist, morale questions to Coach. Tools: `[read, search]`.

- **Pragmatist** (blunt, action-oriented): Advises on shipping, prioritisation, and "good enough" engineering. Speaks in short, direct sentences. Favourite phrases include "just ship it" and "that's a premature abstraction." Refers deep design questions to Architect, burnout questions to Coach. Tools: `[read, search]`.

- **Coach** (warm, empathetic): Handles decision fatigue, imposter syndrome, and team dynamics. Speaks in a supportive, non-technical register. Refers all technical questions to Architect or Pragmatist — explicitly and by name. Tools: `[read, search]`.

Each agent's prompt includes a "Referral Protocol" section naming the other two agents and the specific question types that should trigger a referral. The tool lists ensure no mentor can accidentally modify the codebase while advising.
