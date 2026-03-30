---
title: Escalation Ladder
summary: >-
  A chain of agent tiers from cheapest/fastest to most expensive/capable, where
  each tier attempts the task with explicit self-assessment criteria and
  escalates to the next tier only when it detects it cannot handle the task
  confidently — passing partial work, observations, and escalation reason as
  enriched context.
trigger: >-
  Tasks that vary in difficulty but where you don't know upfront which
  capability tier is needed, and using the most expensive agent for everything
  is wasteful.
---

# Escalation Ladder

## What It Is

A **sequential chain of agent tiers** ordered from cheapest/fastest to most expensive/capable. When a task arrives, it enters at the bottom rung. The agent at that tier attempts the task with explicit self-assessment criteria — confidence thresholds, failure signals, and scope boundaries. If the agent determines it can handle the task, it completes it and returns the result. If it detects that it cannot handle the task confidently, it **escalates** to the next tier, passing its partial work, observations, and a specific reason for escalation. The next tier picks up where the previous one left off, enriched by the lower tier's analysis rather than starting from scratch.

This is distinct from the Research Team pattern, which dispatches work to parallel specialists by **domain**. The Escalation Ladder dispatches by **difficulty** — the same task moves through sequential tiers of increasing capability. It is also distinct from the Multi-Reviewer Panel, which evaluates quality **after** production. The Escalation Ladder routes **during** production based on the agent's own assessment of whether it can complete the work. And unlike the Mentor Constellation, where agents are read-only advisors, every tier in the Escalation Ladder **actively produces work**.

The core economic insight is that most tasks are easy. If 80% of tasks can be handled by the cheapest tier, running the expensive tier on everything wastes 80% of your budget on tasks that didn't need it. The ladder exploits this distribution — paying the escalation overhead on the 20% of hard tasks to avoid overpaying on the 80% of easy ones.

> **Validate the 80/20 assumption.** The 80% figure is an illustrative heuristic, not a universal truth. Measure your actual task difficulty distribution before committing to a ladder design. Some domains (e.g., security audits, legal review, clinical decision support) may have 50%+ hard tasks, which shifts the cost calculus — the escalation overhead may not be worth it if most tasks reach the top tier anyway. If your distribution is skewed toward difficulty, consider fewer tiers or a higher-capability base tier.

## Why It Works

- **Cost scales with difficulty, not volume** — simple tasks (typo fixes, straightforward lookups, routine formatting) resolve at the cheapest tier. Only tasks that genuinely require stronger reasoning, larger context, or more sophisticated tool use escalate to expensive tiers. Total cost tracks task difficulty distribution rather than task count.
- **Escalation enriches context** — when a lower tier escalates, it doesn't just say "I failed." It passes partial work, specific observations, and the reason it couldn't proceed. The higher tier receives a pre-analysed problem — the easy parts already handled, the hard parts identified and described. This makes the higher tier more effective than if it had started cold.
- **Fast path for common cases** — the cheapest tier has the lowest latency. If most tasks resolve there, the average response time across all tasks drops significantly compared to always invoking the most capable (and slowest) tier.
- **Graceful degradation under load** — when the system is busy or budget-constrained, you can cap escalation at a lower tier. Tasks that would have escalated to the top tier instead return a "best effort" result from a lower tier with an explicit note about what wasn't handled. This is better than queueing everything for the top tier or failing outright.
- **Self-documenting difficulty** — the escalation history across many tasks reveals which categories of work are genuinely hard (always escalate) vs deceptively simple (rarely escalate). This data feeds back into tier definition and self-assessment criteria tuning.

## How to Implement

### 1. Define the Tier Chain

Each tier is a combination of **model**, **tool access**, and **context budget**. The tiers should represent meaningful capability jumps, not incremental upgrades.

| Rung | Model class | General description | Context budget | Cost | Latency |
|------|-------------|---------------------|----------------|------|---------|
| **Tier 0** | Fast/cheap (Haiku, GPT-4.1) | Routine, well-defined tasks with clear scope and low ambiguity | Small | Lowest | Fastest |
| **Tier 1** | Standard (Sonnet, GPT-5.1) | Multi-step tasks requiring moderate analysis, coordination across artifacts, or domain judgment | Medium | Moderate | Moderate |
| **Tier 2** | Premium (Opus, GPT-5.4) | Complex tasks requiring deep reasoning, novel problem-solving, or high-stakes decisions | Large | Highest | Slowest |

**Domain-specific examples:**

- **Software engineering**: Tier 0 = typo fixes, simple lookups, formatting, dependency bumps. Tier 1 = refactoring, test writing, multi-file edits. Tier 2 = architecture decisions, security audits, complex debugging.
- **Document review**: Tier 0 = formatting, citation checks, boilerplate sections. Tier 1 = substantive editing, cross-reference verification, consistency analysis. Tier 2 = strategic recommendations, regulatory compliance assessment, novel legal questions.

Three tiers is the sweet spot for most workflows. Two tiers (fast vs premium) works when the task distribution is bimodal. Four or more tiers add escalation overhead without proportional benefit — the self-assessment boundaries between adjacent tiers become too subtle for agents to distinguish reliably.

Each tier is invoked via the `task` tool with an explicit `model` parameter:

```markdown
Use the `task` tool with agent_type: "general-purpose" and model: "<tier model>".

Tier 0: model: "claude-haiku-4.5" or model: "gpt-4.1"
Tier 1: model: "claude-sonnet-4" or model: "gpt-5.1"
Tier 2: model: "claude-opus-4.6" or model: "gpt-5.4"
```

### 2. Define Self-Assessment Criteria

Each tier needs explicit criteria for deciding whether to complete the task or escalate. Self-assessment is the hardest part of this pattern — weaker models are notoriously poor at knowing what they don't know. Mitigate this by making criteria **concrete and observable**, not introspective.

**Escalation signals** (concrete, observable):

| Signal | What it means | Example |
|--------|--------------|---------|
| **Search failure** | Can't find the information needed to proceed | "I searched for the authentication logic but found no relevant files" |
| **Conflicting evidence** | Found contradictory information with no clear resolution | "Module A assumes sync access, Module B assumes async — I can't determine which is canonical" |
| **Scope explosion** | Task requires touching significantly more files/systems than expected | "This 'simple rename' requires changes across 15 files and 3 config systems" |
| **Confidence hedge** | The agent qualifies its answer with uncertainty markers | "I think this is correct but I'm not sure about the edge case where..." |
| **Repeated failure** | The agent's approach isn't working after 2+ attempts | "I've tried two approaches to fix this test and both produce new failures" |
| **Domain boundary** | The task requires reasoning the agent knows it's not suited for | "This requires security threat modelling, which is beyond routine code changes" |

**Do NOT rely on** the agent self-reporting "I'm not confident" — weaker models often report high confidence on wrong answers. Instead, structure the prompt so escalation triggers are based on observable outcomes:

```markdown
## Self-Assessment Protocol

After attempting the task, evaluate these criteria:

1. Did you find all the information you needed? If you had to guess at any
   fact, escalate.
2. Does your solution require changes to more than 5 artifacts? If so,
   escalate — multi-artifact coordination benefits from stronger reasoning.
3. Did you encounter any contradictions in the source material that you
   couldn't resolve? If so, escalate with the specific contradictions
   documented.
4. Did your solution pass on the first attempt, or did you need multiple
   iterations? If you needed 3+ iterations, escalate — the problem is
   harder than this tier handles well.
5. Does the task involve a high-stakes or high-consequence domain (e.g.,
   security, financial calculations, legal compliance, medical advice)?
   Escalate unconditionally — these domains warrant premium reasoning
   regardless of apparent simplicity.
```

**Example: software engineering criteria**
- "More than 5 artifacts" → more than 5 files touched
- "Contradictions in source material" → conflicting type signatures, inconsistent API contracts
- "High-stakes domain" → security, authentication, data integrity

**Example: document review criteria**
- "More than 5 artifacts" → more than 5 sections or cross-referenced documents
- "Contradictions in source material" → conflicting clauses, inconsistent definitions across exhibits
- "High-stakes domain" → regulatory filings, binding legal language, public-facing disclosures

**Validating self-assessment reliability.** Observable criteria are better than introspection, but you should verify they actually catch the cases they should. Run a calibration exercise: dispatch 20 representative tasks through the ladder, then have a human expert independently assign each task to a tier. If more than 30% of escalations are unnecessary (the expert says Tier 0 could have handled it), the self-assessment criteria need tightening — raise thresholds or remove over-sensitive signals. If more than 10% of Tier 0 completions should have escalated, the criteria need loosening.

### 3. Design the Escalation Protocol

When a tier escalates, it must pass a structured handoff to the next tier. The handoff is the mechanism that makes escalation productive rather than wasteful — without it, the higher tier starts from scratch and the lower tier's work is lost.

**Escalation handoff structure:**

```markdown
## Escalation Handoff

**Original task**: [The task as originally received]
**Tier attempted**: [Which tier is escalating]
**Work completed**: [What the lower tier accomplished — partial results,
  files read, searches performed, changes made]
**Escalation reason**: [Specific signal that triggered escalation — not
  "I couldn't do it" but "I found conflicting type signatures in auth.ts
  and session.ts that I cannot reconcile"]
**Observations**: [Anything the lower tier learned that the higher tier
  should know — relevant files, dead ends already explored, context
  gathered]
**Suggested approach**: [If the lower tier has a hypothesis about how to
  proceed, include it — the higher tier can accept or discard it]
```

In Copilot CLI, the handoff is passed as part of the `task` tool's `prompt` parameter. The shared filesystem means any files the lower tier created or modified are already visible to the higher tier — the handoff only needs to describe what was done, not transfer the artifacts.

```markdown
# Orchestrator prompt for escalation:

When a tier escalates, invoke the next tier using the `task` tool:

prompt: "You are Tier {N} in an escalation ladder. A lower tier attempted
this task and escalated to you. Read the escalation handoff below, then
continue the work.

{escalation handoff content}

You have access to all files the previous tier read or modified. Build on
their work — do not start from scratch unless their approach was
fundamentally wrong.

Apply the same self-assessment protocol. If you also cannot complete this
task confidently, produce an escalation handoff for the next tier."
```

### 4. Build the Orchestrator

The orchestrator is the entry point that receives tasks, dispatches them to Tier 0, and handles escalation responses. It can be a parent agent, a skill, or a section of your project's instructions.

```markdown
# Escalation Ladder Orchestrator

## Dispatch Protocol

1. Receive the task.
2. Dispatch to Tier 0 (cheapest/fastest model) with the self-assessment
   protocol included in the prompt.
3. Read the Tier 0 result.
   - If the result is a completed task: return it. Done.
   - If the result is an escalation handoff: proceed to step 4.
4. Dispatch to Tier 1 (standard model) with the escalation handoff
   prepended to the prompt.
5. Read the Tier 1 result.
   - If completed: return it. Done.
   - If escalation handoff: proceed to step 6.
6. Dispatch to Tier 2 (premium model) with the accumulated escalation
   context from all previous tiers.
7. Read the Tier 2 result.
   - If completed: return it. Done.
   - If the top tier also cannot complete: invoke the circuit breaker
     (see below).
```

### 5. Implement the Circuit Breaker

When the top tier also fails, the ladder is exhausted. The circuit breaker prevents infinite loops and provides a structured failure response.

**Circuit breaker actions:**

1. **Collect all tier observations** — each tier's partial work and escalation reason form a comprehensive analysis of why the task is hard.
2. **Produce a structured failure report** — not "I failed" but a detailed description of what was attempted, what was learned, and where the blockage is.
3. **Flag for human review** — some tasks genuinely require human judgment, domain knowledge not present in the codebase, or access to systems the agents can't reach.
4. **Do NOT retry the full ladder** — if all tiers failed, retrying with the same context will produce the same result. Only retry if new information becomes available.

```markdown
## Circuit Breaker Report

**Task**: [Original task]
**Tiers attempted**: [All tiers, with brief outcome of each]
**Cumulative observations**: [What was learned across all tiers]
**Blocking issue**: [The specific reason no tier could complete the task]
**Recommendation**: [What a human or future agent with new context should
  try — e.g., "needs access to the production database schema" or "requires
  a design decision about whether to use sync or async"]
```

### 6. Track Cost and Effectiveness

The ladder is only valuable if it actually saves resources compared to always using the top tier. Without measurement, you can't tell. Track these metrics per task:

| Metric | How to measure | What it tells you |
|--------|---------------|-------------------|
| **Resolution tier** | Which tier completed the task | Distribution of difficulty across your workload |
| **Escalation rate** | % of tasks that escalate past Tier 0 | Whether Tier 0 criteria are too aggressive (too many escalations) or too permissive (catching errors late) |
| **Wasted work** | How much of a lower tier's output the higher tier discarded | Whether escalation handoffs are useful or just noise |
| **Cost ratio** | Actual cost ÷ cost if all tasks used top tier | The ladder's economic value — if this approaches 1.0, the ladder isn't saving anything |
| **Correctness by tier** | Error rate of tasks completed at each tier | Whether lower tiers are completing tasks they shouldn't be |
| **Ladder savings** | (sum of top-tier cost per task) − (actual cost with ladder) | Net economic value of the ladder — if negative, the ladder adds overhead and you should consider fewer tiers or fewer escalation criteria |

**Non-software example metrics**: For a customer support escalation ladder, "resolution tier" maps to which support level resolved the ticket, "escalation rate" is the percentage of tickets that leave the FAQ bot, "wasted work" is the fraction of bot-gathered context the specialist ignored, and "cost ratio" compares actual agent-hours to the cost of routing every ticket to a senior advisor.

**Calculating ladder savings.** `Savings = (sum of top-tier-cost per task) − (actual cost with ladder)`. The top-tier-cost-per-task is what each task would have cost if dispatched directly to the highest tier. Actual cost is the sum of all tier invocations including escalation overhead. If savings ≤ 0, the ladder is not paying for itself — consider collapsing tiers or relaxing escalation criteria.

In practice, append a one-line entry to a tracking file after each task:

```markdown
# In escalation-metrics.md (append-only):
| Task | Tier 0 | Tier 1 | Tier 2 | Resolved at | Notes |
|------|--------|--------|--------|-------------|-------|
| Fix typo in README | ✅ done | — | — | Tier 0 | |
| Refactor auth module | ❌ scope explosion | ✅ done | — | Tier 1 | 12 files touched |
| Security audit of API | ❌ domain boundary | ❌ low confidence | ✅ done | Tier 2 | Unconditional escalation was correct |
```

### 7. Handle De-Escalation

Sometimes a higher tier determines the task was simpler than the lower tier thought. This happens when the lower tier's self-assessment was wrong — it escalated due to a perceived difficulty that wasn't real.

**Do NOT dispatch the task back down.** The higher tier is already running; having it complete the simple task wastes a small amount of budget but avoids the round-trip cost and latency of de-escalation. Instead, use the observation to **tune the lower tier's self-assessment criteria**:

1. Log the false escalation with the specific signal that misfired.
2. After accumulating 3+ false escalations with the same signal, adjust the threshold — make the criterion less sensitive or add an exception.
3. If a particular task category consistently false-escalates, add it to the lower tier's "handle unconditionally" list.

De-escalation is a feedback mechanism, not a runtime routing decision. The ladder always moves upward during execution; downward adjustments happen between tasks as criteria tuning.

## Gotchas

- **Self-assessment is the weakest link.** Weaker models are notoriously bad at knowing what they don't know — they produce confident wrong answers rather than escalating. Mitigate this by using **observable criteria** (search failures, iteration count, artifact count) rather than introspective ones ("am I confident?"). Even with observable criteria, expect Tier 0 to occasionally complete tasks it should have escalated. Periodic spot-checks of Tier 0 completions are essential. To reduce the human cost of spot-checks, designate a periodic automated review: dispatch a higher-tier agent to re-evaluate a random sample of Tier 0 completions (e.g., 10% per batch). If the re-evaluation finds significant quality gaps, tighten Tier 0's escalation criteria.
- **Escalation context bloat wastes the higher tier's budget.** If Tier 0 dumps its entire chain of thought into the handoff, the higher tier burns context tokens re-reading irrelevant details. Keep handoffs structured and concise — the higher tier needs to know what was tried, what was found, and why escalation happened, not every intermediate reasoning step. Cap handoffs at a fixed length (e.g., 500 words) and let the higher tier re-read source files directly if it needs more detail.
- **Tier boundaries are domain-specific.** A model that handles refactoring well might struggle with security analysis at the same tier. The ladder's tier definitions should account for task type, not just abstract "difficulty." Consider maintaining separate escalation criteria for different task categories (code changes, documentation, security, architecture) rather than one universal set.
- **If everything escalates to the top, the ladder is theatre.** Track your escalation rate. If more than 40% of tasks reach the highest tier, either your Tier 0 criteria are too aggressive, your task distribution is harder than expected, or the lower-tier model genuinely can't handle your workload. Diagnose which case applies — the fix is different for each (relax criteria, add an intermediate tier, or upgrade the base model, respectively).
- **Without metrics, you can't justify the ladder.** The overhead of escalation (extra latency, handoff composition, orchestrator complexity) is real. If you're not measuring resolution-tier distribution and cost ratio, you have no evidence the ladder is saving money. It might be cheaper to run everything at Tier 1 and skip the orchestration entirely. Measure before you commit. The orchestrator should also include automated cost alerts: if Tier 2 usage exceeds a configurable threshold (e.g., 30%) of total dispatches over the last 50 tasks, log a warning suggesting criteria recalibration. This prevents slow drift toward top-heavy routing from going unnoticed.
- **Unconditional escalation rules are necessary.** Some task categories should skip lower tiers entirely — security-sensitive changes, data migrations, anything touching authentication. Routing these through a cheap model "just to check" risks a confident wrong answer that passes self-assessment. Define a short list of categories that enter the ladder at Tier 1 or Tier 2 directly.
- **The ladder adds latency on hard tasks.** A task that escalates through all three tiers takes the cumulative time of all three attempts. If latency matters more than cost, consider starting at a higher tier for time-sensitive tasks or running tiers in parallel (speculative execution) — though parallel execution sacrifices the context-enrichment benefit that makes escalation valuable.
- **Don't confuse escalation with retry.** Escalation means a qualitatively different agent attempts the task with enriched context. Retry means the same agent attempts the same task again. If a tier fails due to a transient error (timeout, tool failure), retry at the same tier. If it fails due to a capability gap, escalate. Conflating the two wastes budget on retries that won't help and delays escalation that would.

## Example

A codebase maintenance workflow with three tiers:

**Tier 0 — Fast triage (Haiku / GPT-4.1):**
Handles simple, well-scoped tasks. Self-assessment criteria: task touches ≤3 files, no security implications, no ambiguous requirements, solution works on first attempt.

```markdown
# Dispatch to Tier 0:
prompt: "You are a fast-pass agent for routine maintenance tasks. Attempt
the following task. If you can complete it confidently within these
constraints, do so and return the result. If any escalation signal fires,
stop work and produce an escalation handoff instead.

Task: Update the lodash dependency from 4.17.20 to 4.17.21 across all
package.json files.

## Self-Assessment — Escalate if:
- More than 3 files need changes
- Any breaking change is noted in the changelog
- You encounter version conflicts with other dependencies
- The update requires code changes beyond the version number"

model: "claude-haiku-4.5"
```

Tier 0 finds two `package.json` files, updates both, and returns the result. No escalation needed. Cost: minimal. Latency: seconds.

**Tier 1 — Standard work (Sonnet / GPT-5.1):**
A different task arrives: "Refactor the authentication middleware to support both JWT and session-based auth."

Tier 0 attempts it, finds it requires changes to 8 files and involves security-adjacent logic. It escalates:

```markdown
## Escalation Handoff

**Original task**: Refactor auth middleware to support JWT and session auth
**Tier attempted**: Tier 0
**Work completed**: Identified all files importing auth middleware (8 files).
  Read the current middleware implementation in src/middleware/auth.ts.
  Listed the two auth strategies mentioned in existing comments.
**Escalation reason**: Scope explosion (8 files) and security-adjacent domain.
**Observations**: The current middleware assumes JWT only. Session support
  would require a strategy pattern. Tests exist in auth.test.ts but only
  cover JWT paths.
**Suggested approach**: Introduce an AuthStrategy interface, implement
  JwtStrategy and SessionStrategy, update middleware to accept either.
```

Tier 1 receives this handoff, builds on Tier 0's file discovery and analysis, implements the strategy pattern, updates all 8 files, and adds session-auth test cases. No further escalation needed.

**Tier 2 — Premium reasoning (Opus / GPT-5.4):**
A third task arrives: "Audit the API for authorization bypass vulnerabilities."

Tier 0 escalates unconditionally (security domain). Tier 1 attempts the audit, identifies three potential issues but flags low confidence on two of them — it can't determine whether certain middleware ordering is intentional or a bug. It escalates:

```markdown
## Escalation Handoff

**Original task**: Audit API for authorization bypass vulnerabilities
**Tier attempted**: Tier 1 (Tier 0 skipped — unconditional security escalation)
**Work completed**: Mapped all API routes and their middleware chains.
  Identified 3 potential issues: (1) /admin/config has no auth middleware
  — confirmed vulnerability, (2) /api/users uses auth but not role-check
  — unclear if intentional, (3) middleware ordering in /api/payments
  applies rate-limit before auth — unclear if this enables pre-auth
  enumeration.
**Escalation reason**: Low confidence on issues 2 and 3. Cannot determine
  design intent from code alone.
**Observations**: No security documentation exists. Middleware ordering
  varies across routes with no apparent convention. Issue 1 is confirmed
  and should be fixed regardless of other findings.
**Suggested approach**: Review git history for intentional middleware
  ordering decisions. Check for security-related comments or ADRs.
```

Tier 2 receives the accumulated context from both lower tiers, performs deep analysis including git history review, confirms issue 1, determines issue 2 was intentional (role-check is handled at the database layer), and confirms issue 3 as a real vulnerability. It produces a comprehensive security report without duplicating the route-mapping work that Tier 1 already completed.

**Result**: Three tasks, three different resolution tiers. The dependency update cost pennies at Tier 0. The refactoring used a standard model at Tier 1. Only the security audit — which genuinely needed premium reasoning — reached Tier 2. Total cost: a fraction of running all three tasks at the premium tier.

---

### Non-Software Example: Customer Support Escalation

A customer support workflow with three tiers:

**Tier 0 — FAQ Bot (fast/cheap model):**
Handles routine, well-scoped inquiries. Self-assessment criteria: question matches a known FAQ entry, no account-specific investigation needed, answer is a single factual statement.

A customer asks: "What are your return policy timeframes?" Tier 0 retrieves the FAQ entry, returns the answer. No escalation. Cost: minimal.

**Tier 1 — Specialist Agent (standard model):**
A customer writes: "I returned my order 45 days ago and haven't received a refund, but I also used a promotional credit on the order."

Tier 0 recognizes this requires account-specific investigation and multiple policy interactions (return windows, refund processing, promotional credit rules). It escalates with observations: "Customer is past the standard 30-day refund window. Promotional credit complicates the refund calculation. I identified the relevant policies but cannot determine the correct resolution."

Tier 1 reviews the account history, applies the policies, and resolves the ticket.

**Tier 2 — Senior Advisor (premium model):**
A customer submits a complaint involving a disputed charge, a regulatory reference, and a threat of legal action.

Tier 0 escalates unconditionally (high-stakes). Tier 1 gathers account history and relevant policies but flags low confidence on the regulatory claim and the legal exposure. It escalates with detailed observations.

Tier 2 performs deep analysis, cross-references the regulatory claim, drafts a resolution that addresses both the customer's complaint and the company's legal obligations.

**Result**: Routine questions resolve instantly at Tier 0. Policy-complex issues get specialist attention at Tier 1. Only genuinely high-stakes situations reach Tier 2.
