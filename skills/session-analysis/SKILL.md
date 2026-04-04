---
name: session-analysis
description: >-
  Understand what happened in a Copilot CLI session — review agent behavior,
  audit tool usage and external access, trace subagent hierarchies, search
  events and tool calls, track file provenance, and trace claim propagation.
  Use when asked to analyze a session, review past work, debug agent
  performance, investigate what went wrong, audit security, or extract
  insights from session logs.
license: MIT
---

# Analyzing Copilot CLI Sessions

Copilot CLI records every event in a session to `~/.copilot/session-state/<session-id>/events.jsonl`. This skill uses an analyzer script to perform retrospective forensic analysis of those logs — understanding what an agent did, how its subagents coordinated, what external resources were accessed, and how information propagated through the agent tree.

## Quick Reference: Task → Flag

| I want to… | Use |
|-------------|-----|
| Get a session overview | `--summary` |
| See what happened chronologically | `--timeline` |
| Read what the user asked | `--messages` |
| Replay the full conversation | `--conversation` |
| Replay around a specific exchange | `--conversation N` |
| List all subagents with stats | `--subagents` |
| Visualize subagent hierarchy | `--subagent-tree` |
| Read a specific subagent's full transcript | `--subagent-transcript NAME` |
| Compare token costs across task groups | `--cost-by-issue` |
| Search all events for a string | `--search REGEX` |
| Search tool calls specifically | `--search-tools REGEX` |
| Trace how a claim propagated | `--trace-claim STRING` |
| Audit external network access | `--audit-external` |
| See who created/edited a file | `--file-history PATH` |
| Review tool usage statistics | `--tools` |
| Audit git activity | `--git` |
| Export data as JSON | `--export FILE` |

## Prerequisites

- Python 3.9+ (uses only stdlib — no dependencies)
- Access to the session's `events.jsonl` file

## Procedure: Analyzing a Session

1. **Inspect first — locate the session log.** Session logs live at `~/.copilot/session-state/<session-id>/events.jsonl`.
   - If the user provides a session ID or path, use it directly.
   - To find the most recent sessions:
     ```
     Get-ChildItem ~/.copilot/session-state -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 5   # Windows
     ls -lt ~/.copilot/session-state/ | head -5   # Unix/macOS
     ```
   - To search past sessions by keyword, use the `session_store` SQL database:
     ```sql
     SELECT id, summary, created_at FROM sessions ORDER BY created_at DESC LIMIT 10;
     ```
   - **Always provide the path explicitly** when invoking the script — do not rely on its default path argument.

2. **Start with the summary** to get an overview of the session scope and scale:
   ```
   python scripts/session_analyzer.py <path-to-events.jsonl> --summary
   ```

3. **Visualize the subagent tree** if the session has subagents — this reveals the coordination structure:
   ```
   python scripts/session_analyzer.py <path-to-events.jsonl> --subagent-tree
   ```

4. **Drill into specific areas** based on what the summary reveals or what the user asks about — use the flags documented below.

5. **Interpret the results** using the guidance in [Interpretation: What to Look For](#interpretation-what-to-look-for).

6. **Report findings** — summarize the key insights concisely. Lead with the most important or surprising findings.

## Common Analysis Workflows

### "What happened in this session?"
```
python scripts/session_analyzer.py <path> --summary --timeline
```
Start with summary for scope metrics, then timeline for the chronological narrative.

### "Why did this subagent fail?"
```
python scripts/session_analyzer.py <path> --subagent-tree
python scripts/session_analyzer.py <path> --subagent-transcript <name-from-tree>
```
Identify the agent in the tree, then pull its full transcript to see where it went wrong.

### "Did the agent access anything it shouldn't have?"
```
python scripts/session_analyzer.py <path> --audit-external
```
Review the table of external accesses. Verify flagged shell commands manually — regex matching may produce false positives on string literals.

### "Which agent created or modified this file?"
```
python scripts/session_analyzer.py <path> --file-history src/auth.ts
python scripts/session_analyzer.py <path> --subagent-transcript <owning-agent>
```
Find which subagent touched the file, then review its transcript for context.

### "Where did this hallucinated claim come from?"
```
python scripts/session_analyzer.py <path> --trace-claim "incorrect claim text"
```
Shows first appearance and propagation path across subagents — trace it back to the source.

## The Analyzer Script

The script is at `scripts/session_analyzer.py` (relative to this skill directory). It uses a single-pass collector architecture — the file is read once and events are dispatched to active collectors, so it handles 100+ MB logs efficiently. Forensic features that need ancestry resolution (attributing events to their owning subagent) use an in-memory index built during the pass.

### Flags

All flags take the path to `events.jsonl` as the first positional argument. If no flags are specified, `--summary` is the default. Multiple flags can be combined in a single invocation.

```
python scripts/session_analyzer.py <path> --summary --subagent-tree --audit-external
```

#### Overview Flags

##### `--summary` — Session Overview

Prints high-level statistics: duration, event counts, user messages, tool calls, subagents, skills, compactions, models, token totals, premium requests, and code changes (lines added/removed). Use this first to understand the shape of a session.

##### `--timeline` — Key Event Timeline

Prints key events in chronological order: user messages, subagent start/complete, skill invocations, compactions, shutdowns, resumes, errors, and aborts. Each entry shows timestamp, event type tag, and a short summary.

- `--from TIMESTAMP` — filter events after this ISO 8601 timestamp
- `--to TIMESTAMP` — filter events before this ISO 8601 timestamp

When forensic features are enabled, shows nesting depth based on the subagent tree.

##### `--messages` — User Messages

Lists every user message with its index number and timestamp. Message indices can be passed to `--conversation N` to focus on a specific exchange.

##### `--tools` — Tool Usage Statistics

Prints per-tool statistics: invocation count, success rate (%), and average duration. Use to identify tool failures, hot tools, or slow tools.

##### `--git` — Git Activity

Summarizes git/gh commands: commit count, PRs created/merged, branches seen, and detailed command logs.

##### `--conversation [N]` — Conversation Flow

Without `N`, prints the full user/assistant/system conversation flow. With `N`, focuses on a window around user message `N` (3 messages before, 10 after).

#### Subagent Flags

##### `--subagents` — Subagent Summary Table

Prints a table of all subagents: name, type, model, duration, tool call count, and token count. Use to audit subagent efficiency.

##### `--subagent-tree` — Subagent Hierarchy

Prints an indented tree showing parent-child relationships between subagents, annotated with agent type, duration, and token count from each subagent's completion data:

```
SUBAGENT TREE (12 subagents)
  convert-docs-skill-editor (general-purpose, 5.2m, 120K tok)
  +-- persona-skill-auditor (general-purpose, 3.1m, 80K tok)
  |   +-- paper-reader-1 (explore, 1.2m, 30K tok)
  |   +-- paper-reader-2 (explore, 0.9m, 25K tok)
  +-- style-synthesiser (general-purpose, 2.4m, 60K tok)
```

Use this to understand coordination structure — which agents spawned which, and where time and tokens were spent.

##### `--subagent-transcript NAME` — Full Subagent Transcript

Extracts the complete conversation for a named subagent — every assistant message, tool call (with arguments and results), and the completion outcome, formatted chronologically.

The `NAME` argument matches the `arguments.name` field from the `task` tool call that launched the subagent (visible in `--subagent-tree` output). Includes all events owned by that subagent and its descendants.

##### `--cost-by-issue` — Cost Grouping

Groups subagents by common task-name prefix and aggregates token counts and durations per group. Useful for sessions where subagents follow a naming convention (e.g., `runner-6`, `executor-6`, `validator-6-1` all group under issue `6`).

#### Search and Audit Flags

##### `--search REGEX` — Full-Text Event Search

Searches across all events: `data.content` on messages, `data.arguments` and `data.result` on tool events, `data.result` on subagent completions. Results are deduplicated by content hash and attributed to their owning subagent.

Supports `--event-type TYPE` to filter by event type (e.g., `--event-type tool.execution_complete`).

##### `--search-tools REGEX` — Tool Call Search

Searches tool call arguments and results with a regex. Each match shows timestamp, owning subagent, tool name, and a context snippet.

Supports `--tool-name NAME` to restrict search to a specific tool (e.g., `--tool-name web_fetch`).

##### `--trace-claim STRING` — Claim Propagation Trace

Traces how a specific string or regex pattern propagates through the session. Shows the first appearance (timestamp, subagent, event type) and then all subsequent appearances grouped by subagent. Use this to understand how information flows — e.g., a claim first appears in one subagent's output, then gets picked up by a validator, then appears in the coordinator's status update.

##### `--audit-external` — External Access Audit

Lists all external network access events and shell commands with network-access patterns.

**Note:** Shell command detection uses regex matching, which may flag false positives when tool names appear in string literals (e.g., a CI config containing `pip install`). Verify flagged shell commands manually.

Detected patterns include: `web_fetch`, `web_search` tool calls, and shell commands containing `curl`, `Invoke-WebRequest`, `wget`, `pip install`, `npm install`, or similar. Each entry shows timestamp, owning subagent, tool, URL or command, and a result snippet.

##### `--file-history PATH` — File Provenance

Shows all `create`, `edit`, and `view` operations on files matching a path substring (case-insensitive). Each entry shows timestamp, operation type, owning subagent, full path, and a content snippet (file text for creates, old/new strings for edits).

#### Export

##### `--export FILE` — JSON Export

Exports the timeline to a JSON file for external analysis or further processing.

## Understanding events.jsonl (Reference)

> Most analysis tasks use the script, which handles event parsing. This section is useful when interpreting raw events or troubleshooting unexpected output.

Each line is a JSON object with at minimum `type`, `timestamp`, `id`, and `parentId` fields.

### Event Types

| Event Type | Description |
|---|---|
| `user.message` | User prompt (content in `data.content`) |
| `assistant.message` | Assistant text response |
| `assistant.turn_start` / `assistant.turn_end` | Boundaries of an assistant reasoning turn |
| `tool.execution_start` | Tool invocation (tool name, arguments in `data`) |
| `tool.execution_complete` | Tool result (success flag, result content) |
| `subagent.started` | Subagent launched (agent name, `toolCallId`) |
| `subagent.completed` | Subagent finished (model, duration, tokens, tool calls) |
| `skill.invoked` | Skill activated (name in `data.name`) |
| `session.compaction_start` / `session.compaction_complete` | Context compaction (pre/post token counts) |
| `session.shutdown` | Session ended (shutdown type, premium requests, code changes) |
| `session.resume` | Session resumed (branch context) |
| `session.error` | Error occurred (message) |
| `abort` | User abort (reason) |

### Event Linking

Events are linked in two ways:

1. **`parentId` chains** — every event's `parentId` points to the immediately preceding event in its execution context, forming a linked list. To attribute an event to its owning subagent, walk the `parentId` chain upward until reaching a `subagent.started` event. Chains can be 0–50+ hops deep, passing through assistant messages, tool calls, and turn boundaries.

2. **`toolCallId`** — a `tool.execution_start` and its corresponding `tool.execution_complete` share the same `toolCallId`. A `subagent.started` event's `toolCallId` matches the `tool.execution_start` where `toolName == "task"`, linking the subagent to the task tool call whose `arguments.name` gives the human-readable subagent name.

## Interpretation: What to Look For

### Session Health
- **High compaction count** — the session hit context limits repeatedly; consider breaking work into smaller sessions or using more subagents
- **Errors or aborts** — check the timeline for `session.error` and `abort` events to understand failure modes
- **Shutdown type** — `session.shutdown` data includes `shutdownType` (normal, timeout, error)

### Efficiency
- **Tool success rate below 90%** — investigate which tools are failing and why
- **Subagents with high token counts but few tool calls** — may indicate verbose prompts or unnecessary context
- **Long subagent durations** — compare similar subagents via `--subagent-tree` to spot outliers
- **Deep subagent nesting** — deeply nested trees may indicate over-delegation; compare with flat structures

### Forensic Patterns
- **Claim propagation** — use `--trace-claim` to verify whether information flowed correctly between agents, or to find where a hallucinated claim originated
- **Unauthorized external access** — use `--audit-external` to verify all network access was intentional and appropriate
- **File ownership** — use `--file-history` to determine which subagent introduced a particular change
- **Subagent coordination** — use `--subagent-tree` combined with `--subagent-transcript` to understand how a parent agent delegated work and whether subagents duplicated effort

### Code Impact
- **Lines added vs removed** — large net additions may warrant review; high churn may indicate iteration
- **Commit frequency** — many small commits suggests incremental work; few large commits may indicate batch operations
- **Git activity without user prompts** — autonomous commits or PR operations should be reviewed

## Done Criteria

- Session log located and confirmed readable (script runs without errors)
- `--summary` output produced and key metrics reported to the user (duration, event count, tool calls, token usage, subagent count)
- User's specific questions answered with evidence — cite timestamps, subagent names, or event counts from the output
- If `--summary` reveals potential issues (tool success rate < 90%, high compaction count, errors/aborts), these are flagged with explanation
- Actionable recommendations provided when analysis reveals inefficiencies or failures

## Cross-References

- **Session store SQL database** — for cross-session queries (finding sessions by summary, file, or ref), use the `session_store` database via the `sql` tool. This skill analyzes a single session's raw events in depth; the session store provides breadth across all sessions.
- `writing-skills` — skill invocation events (`skill.invoked`) in session logs correspond to skills authored with that guidance
- `writing-hooks` — hook execution events map to hooks authored with that skill
- `writing-custom-agents` — subagent lifecycle events (`subagent.started`, `subagent.completed`) correspond to agents and embedded subagent instructions authored with that skill
