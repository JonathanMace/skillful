---
name: agent-design-patterns
description: >-
  Named design patterns for structuring multi-agent systems — reviewer panels,
  mentor constellations, ritual cadences, and dynamic research teams. Use when
  authoring agents that need to work together as a coordinated system rather
  than as isolated helpers.
license: MIT
---

# Agent Design Patterns

This skill collects reusable architecture patterns for multi-agent systems built with GitHub Copilot CLI. Each pattern addresses a recurring coordination problem — how to review work from multiple angles, how to provide advisory support without operational risk, or how to prevent long-running autonomous sessions from drifting.

These patterns are **optional**. They represent proven approaches distilled from real projects, not requirements. Apply them when your agent system faces the problem they solve; don't adopt them preemptively.

For the mechanics of authoring individual agents, see the `writing-custom-agents` skill. The patterns here address how agents work **together**.

## Patterns

<!-- Each entry below is a verbatim copy of the pattern file's frontmatter.
     When adding or editing patterns, update the file's frontmatter first,
     then copy it here exactly. The dispatcher is an index, not a paraphrase. -->

### Multi-Reviewer Panel

> N agents review the same artifact from non-overlapping perspectives, invoked
> in parallel. Each reviewer has a clear mandate and explicitly states what it
> does NOT review, eliminating redundancy while maximising coverage.

**When to use**: Quality gates for documents, code, designs, or any artifact that benefits from diverse expert scrutiny.

→ Read `.github/skills/agent-design-patterns/patterns/multi-reviewer-panel.md` for full implementation guidance.

### Mentor Constellation with Referral Graph

> Read-only advisory agents forming a referral network — each knows its limits
> and explicitly routes to the right specialist. Provides diverse perspectives
> without any single agent trying to be everything.

**When to use**: Advisory support where users need guidance from different domains but shouldn't have to know which specialist to ask.

→ Read `.github/skills/agent-design-patterns/patterns/mentor-constellation.md` for full implementation guidance.

### Ritual Cadence

> A skill that enforces periodic maintenance and reflection ceremonies,
> preventing autonomous agent systems from drifting indefinitely without
> cleanup. Divides long-running sessions into bounded cycles with structured
> pauses.

**When to use**: Long-running autonomous sessions where agents accumulate stale state, unfinished work, or strategic drift.

→ Read `.github/skills/agent-design-patterns/patterns/ritual-cadence.md` for full implementation guidance.

### Research Team

> A coordinator agent that delegates all substantive work to team member
> subagents — recruiting, briefing, and dispatching specialists dynamically.
> The coordinator orchestrates and synthesises but never performs the work
> itself.

**When to use**: Multi-step investigative, creative, or development projects where the work spans multiple domains, benefits from parallel specialist effort, and evolves as new questions emerge.

→ Read `.github/skills/agent-design-patterns/patterns/research-team.md` for full implementation guidance.
