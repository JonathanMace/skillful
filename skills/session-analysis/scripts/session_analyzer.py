#!/usr/bin/env python3
"""Streaming analyser for Copilot CLI session event logs (events.jsonl).

Designed for large files (100+ MB). Uses a single-pass collector
architecture — the file is read once and each event is dispatched
to all active collectors simultaneously.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator, Optional

# Default session log path
DEFAULT_PATH = (
    Path.home()
    / ".copilot"
    / "session-state"
    / "4ecd4bf8-106a-471b-af85-d3134005fe36"
    / "events.jsonl"
)

# Event types considered "key" for timeline extraction
TIMELINE_TYPES = {
    "user.message",
    "subagent.started",
    "subagent.completed",
    "skill.invoked",
    "session.compaction_start",
    "session.compaction_complete",
    "session.shutdown",
    "session.resume",
    "session.task_complete",
    "session.start",
    "session.error",
    "abort",
}

# Pre-compiled regexes for git activity tracking
_RE_GIT = re.compile(r"\bgit\b", re.IGNORECASE)
_RE_GH = re.compile(r"\bgh\b", re.IGNORECASE)

_GIT_PATTERNS = {
    "commit": re.compile(r"git\s+commit", re.IGNORECASE),
    "push": re.compile(r"git\s+push", re.IGNORECASE),
    "pr_create": re.compile(r"gh\s+pr\s+create", re.IGNORECASE),
    "pr_merge": re.compile(r"gh\s+pr\s+merge", re.IGNORECASE),
    "branch_create": re.compile(r"git\s+checkout\s+-b\s+([A-Za-z0-9][\w./-]+)", re.IGNORECASE),
    "branch_checkout": re.compile(r"git\s+checkout\s+(?!-b\b)(?!--)([A-Za-z0-9][\w./-]+)", re.IGNORECASE),
}

_RESULT_PATTERNS = {
    "pr_url": re.compile(r"https://github\.com/[^\s]+/pull/\d+"),
    "commit_sha": re.compile(r"\b[0-9a-f]{7,40}\b"),
}


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def _truncate(text: str, max_len: int = 200) -> str:
    """Truncate *text* to *max_len* chars, appending '…' if trimmed."""
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\r", "")
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def _parse_ts(ts: str) -> Optional[datetime]:
    """Parse an ISO 8601 timestamp string to a datetime."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _fmt_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    if seconds < 3600:
        return f"{seconds / 60:.1f}m"
    return f"{seconds / 3600:.1f}h"


def _timeline_summary(evt: dict) -> str:
    """Produce a short summary string for a timeline event."""
    etype = evt["type"]
    data = evt.get("data", {})

    if etype == "user.message":
        content = data.get("content", "")
        return _truncate(content, 120)

    if etype == "subagent.started":
        name = data.get("agentName", "?")
        return f"Launched {name}"

    if etype == "subagent.completed":
        name = data.get("agentName", "?")
        model = data.get("model", "")
        dur = data.get("durationMs")
        dur_str = _fmt_duration(dur / 1000) if dur else "?"
        tools = data.get("totalToolCalls", "?")
        return f"Completed {name} ({model}, {dur_str}, {tools} tools)"

    if etype == "skill.invoked":
        return f"Skill: {data.get('name', '?')}"

    if etype == "session.compaction_start":
        tokens = data.get("conversationTokens", "?")
        return f"Compaction start ({tokens} tokens)"

    if etype == "session.compaction_complete":
        pre = data.get("preCompactionTokens", "?")
        return f"Compaction complete (was {pre} tokens)"

    if etype == "session.shutdown":
        st = data.get("shutdownType", "?")
        reqs = data.get("totalPremiumRequests", "?")
        return f"Shutdown ({st}, {reqs} requests)"

    if etype == "session.resume":
        branch = data.get("context", {}).get("branch", "?")
        return f"Resume on {branch}"

    if etype == "session.start":
        ver = data.get("copilotVersion", "?")
        return f"Session start (v{ver})"

    if etype == "session.task_complete":
        return _truncate(data.get("summary", ""), 120)

    if etype == "session.error":
        return _truncate(data.get("message", ""), 120)

    if etype == "abort":
        return data.get("reason", "")

    return ""


# ---------------------------------------------------------------------------
# Collector Base Class
# ---------------------------------------------------------------------------

class Collector(ABC):
    """Base class for single-pass event collectors."""

    @abstractmethod
    def wants_all(self) -> bool:
        """Return True if this collector needs every event type."""
        ...

    @abstractmethod
    def wanted_types(self) -> set[str]:
        """Event types this collector processes (ignored if wants_all)."""
        ...

    @abstractmethod
    def process(self, evt: dict[str, Any]) -> None:
        """Process a single event."""
        ...

    @abstractmethod
    def result(self) -> Any:
        """Return the collected result."""
        ...


# ---------------------------------------------------------------------------
# Collector Implementations
# ---------------------------------------------------------------------------

class SummaryCollector(Collector):
    def __init__(self):
        self.counts: dict[str, int] = defaultdict(int)
        self.models: set[str] = set()
        self.first_ts: Optional[str] = None
        self.last_ts: Optional[str] = None
        self.tool_names: set[str] = set()
        self.agent_types: set[str] = set()
        self.skill_names: list[str] = []
        self.total_tokens: int = 0
        self.total_premium: int = 0
        self.lines_added: int = 0
        self.lines_removed: int = 0

    def wants_all(self) -> bool:
        return True

    def wanted_types(self) -> set[str]:
        return set()

    def process(self, evt: dict[str, Any]) -> None:
        etype = evt["type"]
        data = evt.get("data", {})
        ts = evt.get("timestamp", "")
        self.counts[etype] += 1

        if self.first_ts is None:
            self.first_ts = ts
        self.last_ts = ts

        if etype == "tool.execution_start":
            self.tool_names.add(data.get("toolName", ""))
        elif etype == "tool.execution_complete":
            model = data.get("model", "")
            if model:
                self.models.add(model)
        elif etype == "subagent.started":
            self.agent_types.add(data.get("agentName", ""))
        elif etype == "subagent.completed":
            tok = data.get("totalTokens", 0)
            if tok:
                self.total_tokens += tok
            model = data.get("model", "")
            if model:
                self.models.add(model)
        elif etype == "skill.invoked":
            self.skill_names.append(data.get("name", "?"))
        elif etype == "session.shutdown":
            reqs = data.get("totalPremiumRequests", 0)
            if reqs:
                self.total_premium += reqs
            changes = data.get("codeChanges", {})
            self.lines_added += changes.get("linesAdded", 0)
            self.lines_removed += changes.get("linesRemoved", 0)

    def result(self) -> dict[str, Any]:
        start = _parse_ts(self.first_ts) if self.first_ts else None
        end = _parse_ts(self.last_ts) if self.last_ts else None
        duration = (end - start).total_seconds() if (start and end) else 0
        counts = self.counts

        return {
            "duration": _fmt_duration(duration),
            "duration_seconds": duration,
            "start_time": self.first_ts or "",
            "end_time": self.last_ts or "",
            "total_events": sum(counts.values()),
            "user_messages": counts.get("user.message", 0),
            "assistant_turns": counts.get("assistant.turn_start", 0),
            "assistant_messages": counts.get("assistant.message", 0),
            "tool_calls_started": counts.get("tool.execution_start", 0),
            "tool_calls_completed": counts.get("tool.execution_complete", 0),
            "unique_tools": sorted(self.tool_names),
            "subagents_launched": counts.get("subagent.started", 0),
            "subagents_completed": counts.get("subagent.completed", 0),
            "unique_agent_types": sorted(self.agent_types),
            "skills_invoked": counts.get("skill.invoked", 0),
            "skill_names": self.skill_names,
            "compactions": counts.get("session.compaction_start", 0),
            "shutdowns": counts.get("session.shutdown", 0),
            "resumes": counts.get("session.resume", 0),
            "aborts": counts.get("abort", 0),
            "errors": counts.get("session.error", 0),
            "models_used": sorted(self.models),
            "total_subagent_tokens": self.total_tokens,
            "total_premium_requests": self.total_premium,
            "lines_added": self.lines_added,
            "lines_removed": self.lines_removed,
            "event_type_counts": dict(sorted(counts.items(), key=lambda x: -x[1])),
        }


class TimelineCollector(Collector):
    def __init__(self):
        self.timeline: list[tuple[str, str, str]] = []

    def wants_all(self) -> bool:
        return False

    def wanted_types(self) -> set[str]:
        return TIMELINE_TYPES

    def process(self, evt: dict[str, Any]) -> None:
        ts = evt.get("timestamp", "")
        summary = _timeline_summary(evt)
        self.timeline.append((ts, evt["type"], summary))

    def result(self) -> list[tuple[str, str, str]]:
        return self.timeline


class UserMessageCollector(Collector):
    def __init__(self):
        self.messages: list[tuple[int, str, str]] = []
        self._idx = 0

    def wants_all(self) -> bool:
        return False

    def wanted_types(self) -> set[str]:
        return {"user.message"}

    def process(self, evt: dict[str, Any]) -> None:
        content = evt.get("data", {}).get("content", "")
        ts = evt.get("timestamp", "")
        self.messages.append((self._idx, ts, content))
        self._idx += 1

    def result(self) -> list[tuple[int, str, str]]:
        return self.messages


class SubagentCollector(Collector):
    def __init__(self):
        self.task_args: dict[str, dict] = {}
        self.starts: dict[str, dict] = {}
        self.completions: dict[str, dict] = {}

    def wants_all(self) -> bool:
        return False

    def wanted_types(self) -> set[str]:
        return {"tool.execution_start", "subagent.started", "subagent.completed"}

    def process(self, evt: dict[str, Any]) -> None:
        etype = evt["type"]
        data = evt.get("data", {})

        if etype == "tool.execution_start" and data.get("toolName") == "task":
            self.task_args[data["toolCallId"]] = data.get("arguments", {})
        elif etype == "subagent.started":
            tcid = data.get("toolCallId", "")
            self.starts[tcid] = {
                "agent_name": data.get("agentName", ""),
                "agent_display": data.get("agentDisplayName", ""),
                "timestamp": evt.get("timestamp", ""),
            }
        elif etype == "subagent.completed":
            tcid = data.get("toolCallId", "")
            self.completions[tcid] = {
                "agent_name": data.get("agentName", ""),
                "model": data.get("model", ""),
                "total_tool_calls": data.get("totalToolCalls"),
                "total_tokens": data.get("totalTokens"),
                "duration_ms": data.get("durationMs"),
                "timestamp": evt.get("timestamp", ""),
            }

    def result(self) -> list[dict[str, Any]]:
        all_ids = sorted(
            self.starts.keys() | self.completions.keys(),
            key=lambda k: self.starts.get(k, {}).get("timestamp", ""),
        )

        results: list[dict[str, Any]] = []
        for tcid in all_ids:
            s = self.starts.get(tcid, {})
            c = self.completions.get(tcid, {})
            args = self.task_args.get(tcid, {})

            start_time = s.get("timestamp", "")
            end_time = c.get("timestamp", "")
            dur_ms = c.get("duration_ms")
            duration = _fmt_duration(dur_ms / 1000) if dur_ms else "?"

            results.append({
                "name": args.get("name", s.get("agent_name", "?")),
                "agent_type": args.get("agent_type", s.get("agent_name", "?")),
                "model": args.get("model", c.get("model", "")),
                "prompt": _truncate(args.get("prompt", ""), 200),
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
                "tool_calls": c.get("total_tool_calls", "?"),
                "tokens": c.get("total_tokens", "?"),
                "result_summary": f"{c.get('total_tool_calls', '?')} tools, {c.get('total_tokens', '?')} tokens",
            })

        return results


class ToolUsageCollector(Collector):
    def __init__(self):
        self.start_times: dict[str, datetime] = {}
        self.counts: dict[str, int] = defaultdict(int)
        self.successes: dict[str, int] = defaultdict(int)
        self.durations: dict[str, list[float]] = defaultdict(list)
        self.tool_names: dict[str, str] = {}

    def wants_all(self) -> bool:
        return False

    def wanted_types(self) -> set[str]:
        return {"tool.execution_start", "tool.execution_complete"}

    def process(self, evt: dict[str, Any]) -> None:
        data = evt.get("data", {})
        tcid = data.get("toolCallId", "")

        if evt["type"] == "tool.execution_start":
            name = data.get("toolName", "unknown")
            self.tool_names[tcid] = name
            self.counts[name] += 1
            ts = _parse_ts(evt.get("timestamp", ""))
            if ts:
                self.start_times[tcid] = ts

        elif evt["type"] == "tool.execution_complete":
            name = self.tool_names.pop(tcid, data.get("toolName", "unknown"))
            if data.get("success"):
                self.successes[name] += 1
            end_ts = _parse_ts(evt.get("timestamp", ""))
            start_ts = self.start_times.pop(tcid, None)
            if start_ts and end_ts:
                dur = (end_ts - start_ts).total_seconds()
                if dur >= 0:
                    self.durations[name].append(dur)

    def result(self) -> dict[str, dict[str, Any]]:
        stats: dict[str, dict[str, Any]] = {}
        for name in sorted(self.counts):
            total = self.counts[name]
            succ = self.successes.get(name, 0)
            durs = self.durations.get(name, [])
            stats[name] = {
                "count": total,
                "success_rate": round(succ / total * 100, 1) if total else 0,
                "avg_duration": round(sum(durs) / len(durs), 2) if durs else None,
            }
        return stats


class ConversationCollector(Collector):
    def __init__(self, include_tool_results: bool = False, max_content: int = 200):
        self._include_tools = include_tool_results
        self._max = max_content
        self.conversation: list[tuple[str, str, str]] = []

    def wants_all(self) -> bool:
        return False

    def wanted_types(self) -> set[str]:
        types = {"user.message", "assistant.message", "system.notification"}
        if self._include_tools:
            types.add("tool.execution_complete")
        return types

    def process(self, evt: dict[str, Any]) -> None:
        ts = evt.get("timestamp", "")
        data = evt.get("data", {})
        etype = evt["type"]

        if etype == "user.message":
            self.conversation.append(("user", ts, _truncate(data.get("content", ""), self._max)))
        elif etype == "assistant.message":
            content = data.get("content", "")
            if content and content.strip():
                self.conversation.append(("assistant", ts, _truncate(content, self._max)))
        elif etype == "system.notification":
            self.conversation.append(("system", ts, _truncate(data.get("content", ""), self._max)))
        elif etype == "tool.execution_complete":
            result = data.get("result", {})
            text = result.get("content", "") if isinstance(result, dict) else str(result)
            self.conversation.append(("tool", ts, _truncate(text, self._max)))

    def result(self) -> list[tuple[str, str, str]]:
        return self.conversation


class GitActivityCollector(Collector):
    def __init__(self):
        self.commits: list[dict] = []
        self.prs_created: list[dict] = []
        self.prs_merged: list[dict] = []
        self.branches: set[str] = set()
        self.git_commands: list[dict] = []
        self.pending_git: dict[str, dict] = {}

    def wants_all(self) -> bool:
        return False

    def wanted_types(self) -> set[str]:
        return {"tool.execution_start", "tool.execution_complete", "session.context_changed"}

    def process(self, evt: dict[str, Any]) -> None:
        etype = evt["type"]
        data = evt.get("data", {})
        tcid = data.get("toolCallId", "")
        ts = evt.get("timestamp", "")

        if etype == "tool.execution_start":
            tool = data.get("toolName", "")
            args = data.get("arguments", {})

            if tool == "powershell":
                cmd = args.get("command", "")
                if not (_RE_GIT.search(cmd) or _RE_GH.search(cmd)):
                    return
                self.pending_git[tcid] = {"command": cmd, "timestamp": ts}
                self.git_commands.append({"timestamp": ts, "command": _truncate(cmd, 300)})

                for label, pat in _GIT_PATTERNS.items():
                    m = pat.search(cmd)
                    if not m:
                        continue
                    if label == "commit":
                        self.commits.append({"timestamp": ts, "command": _truncate(cmd, 300)})
                    elif label == "pr_create":
                        self.prs_created.append({"timestamp": ts, "command": _truncate(cmd, 300)})
                    elif label == "pr_merge":
                        self.prs_merged.append({"timestamp": ts, "command": _truncate(cmd, 300)})
                    elif label in ("branch_create", "branch_checkout"):
                        self.branches.add(m.group(1))

            elif tool.startswith("github-mcp-server"):
                if "pull_request" in tool or "list_pull" in tool:
                    self.git_commands.append({"timestamp": ts, "tool": tool, "args": str(args)[:200]})

        elif etype == "tool.execution_complete":
            if tcid in self.pending_git:
                result = data.get("result", {})
                text = result.get("content", "") if isinstance(result, dict) else str(result)
                pr_match = _RESULT_PATTERNS["pr_url"].search(text)
                if pr_match:
                    url = pr_match.group(0)
                    cmd_info = self.pending_git[tcid]
                    if "pr create" in cmd_info.get("command", "").lower():
                        self.prs_created.append({"timestamp": ts, "url": url})
                    elif "pr merge" in cmd_info.get("command", "").lower():
                        self.prs_merged.append({"timestamp": ts, "url": url})
                del self.pending_git[tcid]

        elif etype == "session.context_changed":
            branch = data.get("branch", "")
            if branch:
                self.branches.add(branch)

    def result(self) -> dict[str, Any]:
        return {
            "commits": len(self.commits),
            "commit_details": self.commits,
            "prs_created": len(self.prs_created),
            "pr_create_details": self.prs_created,
            "prs_merged": len(self.prs_merged),
            "pr_merge_details": self.prs_merged,
            "branches": sorted(self.branches),
            "git_commands_total": len(self.git_commands),
        }


# ---------------------------------------------------------------------------
# Single-Pass Engine
# ---------------------------------------------------------------------------

def run_collectors(
    path: str | Path,
    collectors: list[Collector],
) -> None:
    """Read *path* once and dispatch each event to all active collectors."""
    if not collectors:
        return

    wants_all = [c for c in collectors if c.wants_all()]
    type_filtered = [c for c in collectors if not c.wants_all()]

    # Build dispatch table: event_type -> list of collectors
    type_dispatch: dict[str, list[Collector]] = defaultdict(list)
    for c in type_filtered:
        for t in c.wanted_types():
            type_dispatch[t].append(c)

    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                print(f"[WARN] Malformed JSON on line {lineno}, skipping", file=sys.stderr)
                continue

            etype = evt.get("type", "")

            for c in wants_all:
                c.process(evt)

            if etype in type_dispatch:
                for c in type_dispatch[etype]:
                    c.process(evt)


# ---------------------------------------------------------------------------
# Legacy Wrapper Functions (backward-compatible standalone API)
# ---------------------------------------------------------------------------

def iter_events(
    path: str | Path,
    type_filter: Optional[str | set[str]] = None,
) -> Generator[dict[str, Any], None, None]:
    """Yield events one at a time from *path*, optionally filtering by type."""
    if isinstance(type_filter, str):
        type_filter = {type_filter}
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                print(f"[WARN] Malformed JSON on line {lineno}, skipping", file=sys.stderr)
                continue
            if type_filter is None or evt.get("type") in type_filter:
                yield evt


def extract_timeline(path: str | Path) -> list[tuple[str, str, str]]:
    """Return ``(timestamp, event_type, summary)`` for key events."""
    c = TimelineCollector()
    run_collectors(path, [c])
    return c.result()


def extract_user_messages(path: str | Path) -> list[tuple[int, str, str]]:
    """Return ``(index, timestamp, content)`` for every user message."""
    c = UserMessageCollector()
    run_collectors(path, [c])
    return c.result()


def extract_subagents(path: str | Path) -> list[dict[str, Any]]:
    """Return a list of dicts describing each subagent lifecycle."""
    c = SubagentCollector()
    run_collectors(path, [c])
    return c.result()


def tool_usage_stats(path: str | Path) -> dict[str, dict[str, Any]]:
    """Return ``{tool_name: {count, success_rate, avg_duration}}``."""
    c = ToolUsageCollector()
    run_collectors(path, [c])
    return c.result()


def extract_conversation(
    path: str | Path,
    include_tool_results: bool = False,
    max_content: int = 200,
) -> list[tuple[str, str, str]]:
    """Return ``(role, timestamp, content)`` for the conversation flow."""
    c = ConversationCollector(include_tool_results=include_tool_results, max_content=max_content)
    run_collectors(path, [c])
    return c.result()


def extract_git_activity(path: str | Path) -> dict[str, Any]:
    """Scan tool executions for git/gh commands."""
    c = GitActivityCollector()
    run_collectors(path, [c])
    return c.result()


def session_summary(path: str | Path) -> dict[str, Any]:
    """Return a dict of high-level session statistics."""
    c = SummaryCollector()
    run_collectors(path, [c])
    return c.result()


# ---------------------------------------------------------------------------
# CLI Formatting Helpers
# ---------------------------------------------------------------------------

def _print_table(headers: list[str], rows: list[list], max_col: int = 60) -> None:
    """Print a simple ASCII table."""
    # Compute column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            text = str(cell)[:max_col]
            if i < len(widths):
                widths[i] = max(widths[i], len(text))

    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print(fmt.format(*("-" * w for w in widths)))
    for row in rows:
        cells = [str(c)[:max_col] for c in row]
        # Pad if needed
        while len(cells) < len(headers):
            cells.append("")
        print(fmt.format(*cells))


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    # Ensure stdout can handle Unicode on Windows
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Analyse a Copilot CLI session event log.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_PATH),
        help="Path to events.jsonl (default: most recent session)",
    )
    parser.add_argument("--summary", action="store_true", help="Print session summary stats")
    parser.add_argument("--timeline", action="store_true", help="Print key event timeline")
    parser.add_argument("--messages", action="store_true", help="Print all user messages")
    parser.add_argument("--subagents", action="store_true", help="Print subagent summary table")
    parser.add_argument("--tools", action="store_true", help="Print tool usage stats")
    parser.add_argument(
        "--conversation",
        nargs="?",
        const=-1,
        type=int,
        metavar="N",
        help="Print conversation flow (optionally around user message N)",
    )
    parser.add_argument("--git", action="store_true", help="Print git activity summary")
    parser.add_argument("--export", metavar="FILE", help="Export full timeline to JSON file")

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    # Default to --summary if nothing specified
    if not any([
        args.summary, args.timeline, args.messages, args.subagents,
        args.tools, args.conversation is not None, args.git, args.export,
    ]):
        args.summary = True

    # Build collectors for all requested analyses
    collectors: list[Collector] = []
    summary_c = timeline_c = messages_c = subagents_c = None
    tools_c = conversation_c = git_c = None

    if args.summary:
        summary_c = SummaryCollector()
        collectors.append(summary_c)
    if args.timeline or args.export:
        timeline_c = TimelineCollector()
        collectors.append(timeline_c)
    if args.messages:
        messages_c = UserMessageCollector()
        collectors.append(messages_c)
    if args.subagents:
        subagents_c = SubagentCollector()
        collectors.append(subagents_c)
    if args.tools:
        tools_c = ToolUsageCollector()
        collectors.append(tools_c)
    if args.conversation is not None:
        conversation_c = ConversationCollector(include_tool_results=False, max_content=300)
        collectors.append(conversation_c)
    if args.git:
        git_c = GitActivityCollector()
        collectors.append(git_c)

    # Single pass over the file
    run_collectors(path, collectors)

    # Format and print results
    if summary_c is not None:
        s = summary_c.result()
        print("=" * 60)
        print("SESSION SUMMARY")
        print("=" * 60)
        print(f"  Duration:            {s['duration']} ({s['start_time'][:19]} -> {s['end_time'][:19]})")
        print(f"  Total events:        {s['total_events']:,}")
        print(f"  User messages:       {s['user_messages']}")
        print(f"  Assistant turns:     {s['assistant_turns']}")
        print(f"  Tool calls:          {s['tool_calls_started']:,} started, {s['tool_calls_completed']:,} completed")
        print(f"  Unique tools:        {len(s['unique_tools'])}")
        print(f"  Subagents:           {s['subagents_launched']} launched, {s['subagents_completed']} completed")
        print(f"  Agent types:         {', '.join(s['unique_agent_types'])}")
        print(f"  Skills invoked:      {s['skills_invoked']} ({', '.join(s['skill_names'])})")
        print(f"  Compactions:         {s['compactions']}")
        print(f"  Shutdowns/Resumes:   {s['shutdowns']} / {s['resumes']}")
        print(f"  Aborts:              {s['aborts']}")
        print(f"  Errors:              {s['errors']}")
        print(f"  Models used:         {', '.join(s['models_used'])}")
        print(f"  Subagent tokens:     {s['total_subagent_tokens']:,}")
        print(f"  Premium requests:    {s['total_premium_requests']}")
        print(f"  Code changes:        +{s['lines_added']:,} / -{s['lines_removed']:,} lines")
        print()
        print("Event type breakdown:")
        for etype, cnt in s["event_type_counts"].items():
            print(f"  {cnt:>6,}  {etype}")

    if timeline_c is not None and args.timeline:
        tl = timeline_c.result()
        print(f"\nTIMELINE ({len(tl)} key events)")
        print("-" * 80)
        for ts, etype, summary in tl:
            short_ts = ts[:19].replace("T", " ") if ts else "?"
            tag = etype.split(".")[-1]
            print(f"  {short_ts}  [{tag:<20}] {summary}")

    if messages_c is not None:
        msgs = messages_c.result()
        print(f"\nUSER MESSAGES ({len(msgs)} total)")
        print("-" * 80)
        for idx, ts, content in msgs:
            short_ts = ts[:19].replace("T", " ") if ts else "?"
            first_line = content.split("\n")[0][:120] if content else ""
            print(f"  [{idx:>3}] {short_ts}  {first_line}")

    if subagents_c is not None:
        agents = subagents_c.result()
        print(f"\nSUBAGENTS ({len(agents)} total)")
        print("-" * 100)
        headers = ["#", "Name", "Type", "Model", "Duration", "Tools", "Tokens"]
        rows = []
        for i, a in enumerate(agents):
            rows.append([
                i,
                a["name"][:25],
                a["agent_type"][:18],
                a["model"][:20] if a["model"] else "",
                a["duration"],
                a["tool_calls"],
                a["tokens"],
            ])
        _print_table(headers, rows)

    if tools_c is not None:
        stats = tools_c.result()
        print(f"\nTOOL USAGE ({len(stats)} tools)")
        print("-" * 70)
        headers = ["Tool", "Count", "Success %", "Avg Duration"]
        rows = []
        for name, s in sorted(stats.items(), key=lambda x: -x[1]["count"]):
            dur = f"{s['avg_duration']:.2f}s" if s["avg_duration"] is not None else "N/A"
            rows.append([name, s["count"], f"{s['success_rate']}%", dur])
        _print_table(headers, rows)

    if conversation_c is not None:
        n = args.conversation
        conv = conversation_c.result()
        if n >= 0:
            user_indices = [i for i, (role, _, _) in enumerate(conv) if role == "user"]
            if n < len(user_indices):
                center = user_indices[n]
                start = max(0, center - 3)
                end = min(len(conv), center + 10)
                conv = conv[start:end]
                print(f"\nCONVERSATION around user message {n}")
            else:
                print(f"User message {n} not found (max {len(user_indices) - 1})")
                return
        else:
            print(f"\nFULL CONVERSATION ({len(conv)} entries)")

        print("-" * 80)
        for role, ts, content in conv:
            short_ts = ts[:19].replace("T", " ") if ts else "?"
            prefix = {"user": "[user]", "assistant": "[asst]", "tool": "[tool]", "system": "[sys]"}.get(role, "[?]")
            print(f"  {prefix} [{short_ts}] {content[:200]}")

    if git_c is not None:
        g = git_c.result()
        print("\nGIT ACTIVITY")
        print("-" * 60)
        print(f"  Total git/gh commands:  {g['git_commands_total']}")
        print(f"  Commits:                {g['commits']}")
        print(f"  PRs created:            {g['prs_created']}")
        print(f"  PRs merged:             {g['prs_merged']}")
        print(f"  Branches seen:          {len(g['branches'])}")
        if g["branches"]:
            for b in g["branches"]:
                print(f"    - {b}")
        if g["pr_create_details"]:
            print("\n  PR Create Details:")
            for pr in g["pr_create_details"][:20]:
                ts = pr.get("timestamp", "")[:19]
                cmd = pr.get("command", pr.get("url", ""))
                print(f"    {ts}  {_truncate(cmd, 120)}")
        if g["pr_merge_details"]:
            print("\n  PR Merge Details:")
            for pr in g["pr_merge_details"][:20]:
                ts = pr.get("timestamp", "")[:19]
                cmd = pr.get("command", pr.get("url", ""))
                print(f"    {ts}  {_truncate(cmd, 120)}")

    if timeline_c is not None and args.export:
        tl = timeline_c.result()
        export_data = [
            {"timestamp": ts, "event_type": etype, "summary": summary}
            for ts, etype, summary in tl
        ]
        out_path = Path(args.export)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(export_data, fh, indent=2, ensure_ascii=False)
        print(f"\nExported {len(export_data)} timeline events to {out_path}")


if __name__ == "__main__":
    main()
