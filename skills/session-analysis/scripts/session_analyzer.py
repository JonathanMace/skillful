#!/usr/bin/env python3
"""Streaming analyser for Copilot CLI session event logs (events.jsonl).

Designed for large files (100+ MB). Uses a single-pass collector
architecture — the file is read once and each event is dispatched
to all active collectors simultaneously.

Install optional dependencies for faster analysis of large logs::

    pip install -r requirements.txt   # (from the scripts/ directory)

The script works without them — stdlib ``json`` is used as a fallback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator, Optional

# ---------------------------------------------------------------------------
# Optional fast JSON backend — falls back to stdlib json transparently.
# Install with:  pip install orjson
# ---------------------------------------------------------------------------
try:
    import orjson

    _loads = orjson.loads  # accepts both str and bytes
    _dumps = lambda obj, **kw: orjson.dumps(obj).decode("utf-8")
    _HAS_ORJSON = True
except ImportError:
    _loads = json.loads
    _dumps = lambda obj, **kw: json.dumps(obj, ensure_ascii=True)
    _HAS_ORJSON = False

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
    """Truncate *text* to *max_len* chars, appending '...' if trimmed."""
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\r", "")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _parse_ts(ts: str) -> Optional[datetime]:
    """Parse an ISO 8601 timestamp string to a timezone-aware datetime."""
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
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
        self._event_ids: list[str] = []

    def wants_all(self) -> bool:
        return False

    def wanted_types(self) -> set[str]:
        return TIMELINE_TYPES

    def process(self, evt: dict[str, Any]) -> None:
        ts = evt.get("timestamp", "")
        summary = _timeline_summary(evt)
        self.timeline.append((ts, evt["type"], summary))
        self._event_ids.append(evt.get("id", ""))

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
# V2 Shared Infrastructure
# ---------------------------------------------------------------------------

class AncestryIndex(Collector):
    """Shared index for resolving parentId chains and subagent ownership."""

    def __init__(self):
        self.parent_map: dict[str, str] = {}
        self.task_args: dict[str, dict] = {}
        self.task_call_eids: dict[str, str] = {}  # toolCallId -> event_id of task tool call
        self.subagent_starts: dict[str, dict] = {}
        self.subagent_start_by_tcid: dict[str, str] = {}
        self.subagent_completions: dict[str, dict] = {}
        self._resolve_cache: dict[str, Optional[tuple[str, str]]] = {}
        self._children_map: Optional[dict[str, list[str]]] = None

    def wants_all(self) -> bool:
        return True

    def wanted_types(self) -> set[str]:
        return set()

    def process(self, evt: dict[str, Any]) -> None:
        eid = evt.get("id", "")
        pid = evt.get("parentId", "")
        if eid:
            self.parent_map[eid] = pid

        etype = evt.get("type", "")
        data = evt.get("data", {})

        if etype == "tool.execution_start" and data.get("toolName") == "task":
            tcid = data.get("toolCallId", "")
            if tcid:
                self.task_args[tcid] = data.get("arguments", {})
                if eid:
                    self.task_call_eids[tcid] = eid
        elif etype == "subagent.started":
            tcid = data.get("toolCallId", "")
            if eid:
                self.subagent_starts[eid] = data
                if tcid:
                    self.subagent_start_by_tcid[tcid] = eid
        elif etype == "subagent.completed":
            tcid = data.get("toolCallId", "")
            if tcid:
                self.subagent_completions[tcid] = data

    def resolve_subagent(self, event_id: str) -> Optional[tuple[str, str]]:
        """Walk parentId chain to nearest subagent.started.
        Returns (task_name, toolCallId) or None for root-level events."""
        if event_id in self._resolve_cache:
            return self._resolve_cache[event_id]

        visited: list[str] = []
        current = event_id
        result = None

        while current:
            if current in self._resolve_cache:
                result = self._resolve_cache[current]
                break
            visited.append(current)
            if current in self.subagent_starts:
                data = self.subagent_starts[current]
                tcid = data.get("toolCallId", "")
                name = self.task_args.get(tcid, {}).get(
                    "name", data.get("agentName", "?")
                )
                result = (name, tcid)
                break
            current = self.parent_map.get(current, "")
            if not current:
                break

        for v in visited:
            self._resolve_cache[v] = result
        return result

    def resolve_parent_subagent(
        self, subagent_event_id: str
    ) -> Optional[tuple[str, str]]:
        """For a subagent.started event, find the parent subagent (if any).

        Uses the tool.execution_start event that spawned this subagent
        to determine the correct parent context, avoiding sibling
        subagent.started events in the parentId chain.
        """
        data = self.subagent_starts.get(subagent_event_id, {})
        tcid = data.get("toolCallId", "")
        if not tcid:
            return None

        # Find the tool.execution_start that called the task tool
        task_eid = self.task_call_eids.get(tcid, "")
        if not task_eid:
            return None

        return self.resolve_subagent(task_eid)

    def _build_children_map(self) -> None:
        if self._children_map is not None:
            return
        self._children_map = defaultdict(list)
        for eid, pid in self.parent_map.items():
            if pid:
                self._children_map[pid].append(eid)

    def descendants_of(self, event_id: str) -> set[str]:
        """Return set of all event IDs that are descendants of event_id."""
        self._build_children_map()
        result: set[str] = set()
        queue = [event_id]
        while queue:
            current = queue.pop()
            for child in self._children_map.get(current, []):
                if child not in result:
                    result.add(child)
                    queue.append(child)
        return result

    def subagent_name(self, event_id: str) -> str:
        """Resolve the human-readable subagent name for an event, or 'root'."""
        info = self.resolve_subagent(event_id)
        return info[0] if info else "root"

    def subagent_depth(self, event_id: str) -> int:
        """Compute nesting depth of an event in the subagent tree."""
        depth = 0
        info = self.resolve_subagent(event_id)
        seen: set[str] = set()
        while info:
            depth += 1
            tcid = info[1]
            if tcid in seen:
                break
            seen.add(tcid)
            sa_eid = self.subagent_start_by_tcid.get(tcid, "")
            if not sa_eid:
                break
            info = self.resolve_parent_subagent(sa_eid)
        return depth

    def result(self) -> "AncestryIndex":
        return self


class EventStore(Collector):
    """Stores all events for post-pass filtering."""

    def __init__(self):
        self.events: list[dict[str, Any]] = []

    def wants_all(self) -> bool:
        return True

    def wanted_types(self) -> set[str]:
        return set()

    def process(self, evt: dict[str, Any]) -> None:
        self.events.append(evt)

    def result(self) -> list[dict[str, Any]]:
        return self.events


# ---------------------------------------------------------------------------
# V2 External Access Patterns
# ---------------------------------------------------------------------------

_EXTERNAL_CMD_RE = re.compile(
    r"\b(curl|Invoke-WebRequest|Invoke-RestMethod|wget"
    r"|pip\s+install|npm\s+install|gem\s+install"
    r"|cargo\s+install|go\s+install|apt\s+install"
    r"|brew\s+install|choco\s+install|winget\s+install)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# V2 Cost Grouping Helpers
# ---------------------------------------------------------------------------

_COST_NAME_RE = re.compile(r"^(.+?)-\d+(?:-\d+)*$")


def _cost_group_name(name: str) -> str:
    """Derive a group name from a task name (strip trailing -N/-N-M)."""
    m = _COST_NAME_RE.match(name)
    if m:
        return m.group(1)
    return name


def _merge_cost_groups(
    groups: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Merge single-member groups that share a common hyphenated prefix."""
    singles = {k: v for k, v in groups.items() if v["count"] == 1}
    multi = {k: v for k, v in groups.items() if v["count"] > 1}

    prefix_buckets: dict[str, list[str]] = defaultdict(list)
    for name in singles:
        parts = name.split("-")
        if len(parts) > 1:
            prefix_buckets[parts[0]].append(name)
        else:
            multi[name] = singles[name]

    for prefix, names in prefix_buckets.items():
        if len(names) >= 2:
            merged: dict[str, Any] = {
                "count": 0,
                "tokens": 0,
                "duration_ms": 0,
                "names": [],
            }
            for n in names:
                d = singles[n]
                merged["count"] += d["count"]
                merged["tokens"] += d["tokens"]
                merged["duration_ms"] += d["duration_ms"]
                merged["names"].extend(d["names"])
            multi[prefix + "-*"] = merged
        else:
            multi[names[0]] = singles[names[0]]

    return multi


# ---------------------------------------------------------------------------
# V2 Token Formatting Helper
# ---------------------------------------------------------------------------

def _fmt_tokens(n: int) -> str:
    """Format a token count to a human-readable string."""
    if not n:
        return "0"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


# ---------------------------------------------------------------------------
# V2 Output Formatters
# ---------------------------------------------------------------------------

def _output_subagent_transcript(
    name: str,
    ancestry: AncestryIndex,
    store: EventStore,
) -> None:
    """Print chronological transcript of a named subagent."""
    tcid = None
    for tc, args in ancestry.task_args.items():
        if args.get("name") == name:
            tcid = tc
            break

    if not tcid:
        print(f"No subagent found with name '{name}'")
        return

    sa_eid = ancestry.subagent_start_by_tcid.get(tcid)
    if not sa_eid:
        print(f"No subagent.started event found for '{name}'")
        return

    descendants = ancestry.descendants_of(sa_eid)
    descendants.add(sa_eid)

    relevant_types = {
        "assistant.message",
        "tool.execution_start",
        "tool.execution_complete",
        "subagent.started",
        "subagent.completed",
        "user.message",
    }

    transcript = [
        evt
        for evt in store.events
        if evt.get("id", "") in descendants and evt.get("type") in relevant_types
    ]

    print(f"\nSUBAGENT TRANSCRIPT: {name} ({len(transcript)} events)")
    print("=" * 80)

    for evt in transcript:
        ts = evt.get("timestamp", "")[:19].replace("T", " ")
        etype = evt["type"]
        data = evt.get("data", {})

        if etype == "assistant.message":
            content = data.get("content", "")
            if content and content.strip():
                print(f"\n  [{ts}] ASSISTANT:")
                lines = content.split("\n")
                for line in lines[:20]:
                    print(f"    {line[:200]}")
                if len(lines) > 20:
                    print(f"    ... ({len(content)} chars total)")

        elif etype == "tool.execution_start":
            tool = data.get("toolName", "?")
            args = data.get("arguments", {})
            args_str = _dumps(args)[:200]
            print(f"\n  [{ts}] TOOL CALL: {tool}")
            print(f"    Args: {args_str}")

        elif etype == "tool.execution_complete":
            result = data.get("result", {})
            text = (
                result.get("content", "")
                if isinstance(result, dict)
                else str(result)
            )
            print(f"  [{ts}] TOOL RESULT: {_truncate(text, 300)}")

        elif etype == "subagent.started":
            sa_name = data.get("agentName", "?")
            print(f"\n  [{ts}] SUBAGENT STARTED: {sa_name}")

        elif etype == "subagent.completed":
            sa_name = data.get("agentName", "?")
            tokens = data.get("totalTokens", "?")
            dur = data.get("durationMs")
            dur_str = _fmt_duration(dur / 1000) if dur else "?"
            print(
                f"  [{ts}] SUBAGENT COMPLETED: {sa_name}"
                f" ({dur_str}, {tokens} tokens)"
            )

        elif etype == "user.message":
            content = data.get("content", "")
            print(f"\n  [{ts}] USER: {_truncate(content, 300)}")


def _output_search_tools(
    regex: str,
    tool_name_filter: Optional[str],
    ancestry: AncestryIndex,
    store: EventStore,
) -> None:
    """Search tool arguments and results with a regex."""
    pattern = re.compile(regex, re.IGNORECASE)

    starts: dict[str, dict] = {}
    completes: dict[str, dict] = {}
    for evt in store.events:
        etype = evt.get("type", "")
        data = evt.get("data", {})
        tcid = data.get("toolCallId", "")
        if etype == "tool.execution_start" and tcid:
            starts[tcid] = evt
        elif etype == "tool.execution_complete" and tcid:
            completes[tcid] = evt

    rows: list[list] = []
    for tcid, start_evt in starts.items():
        data = start_evt.get("data", {})
        tool = data.get("toolName", "")

        if tool_name_filter and tool != tool_name_filter:
            continue

        args = data.get("arguments", {})
        args_str = _dumps(args)

        complete_evt = completes.get(tcid, {})
        result_data = complete_evt.get("data", {}).get("result", {})
        result_str = (
            result_data.get("content", "")
            if isinstance(result_data, dict)
            else str(result_data)
        )

        args_match = pattern.search(args_str)
        result_match = pattern.search(result_str)

        if args_match or result_match:
            ts = start_evt.get("timestamp", "")[:19]
            eid = start_evt.get("id", "")
            subagent = ancestry.subagent_name(eid)
            match = args_match or result_match
            full_text = args_str if args_match else result_str
            s = max(0, match.start() - 40)
            e = min(len(full_text), match.end() + 40)
            context = full_text[s:e].replace("\n", " ")
            rows.append([ts, subagent, tool, _truncate(context, 80)])

    print(f"\nSEARCH TOOLS: /{regex}/ ({len(rows)} matches)")
    if tool_name_filter:
        print(f"  Filtered by tool: {tool_name_filter}")
    print("-" * 100)
    _print_table(["Timestamp", "Subagent", "Tool", "Match Context"], rows)


def _output_audit_external(
    ancestry: AncestryIndex,
    store: EventStore,
) -> None:
    """Audit external network and package-install access."""
    starts: dict[str, dict] = {}
    completes: dict[str, dict] = {}
    for evt in store.events:
        etype = evt.get("type", "")
        data = evt.get("data", {})
        tcid = data.get("toolCallId", "")
        if etype == "tool.execution_start" and tcid:
            starts[tcid] = evt
        elif etype == "tool.execution_complete" and tcid:
            completes[tcid] = evt

    rows: list[list] = []
    for tcid, start_evt in starts.items():
        data = start_evt.get("data", {})
        tool = data.get("toolName", "")
        args = data.get("arguments", {})

        is_external = False
        detail = ""

        if tool in ("web_fetch", "web_search"):
            is_external = True
            detail = args.get("url", args.get("query", str(args)[:100]))
        elif tool == "powershell":
            cmd = args.get("command", "")
            if _EXTERNAL_CMD_RE.search(cmd):
                is_external = True
                detail = cmd

        if is_external:
            ts = start_evt.get("timestamp", "")[:19]
            eid = start_evt.get("id", "")
            subagent = ancestry.subagent_name(eid)

            complete_evt = completes.get(tcid, {})
            result_data = complete_evt.get("data", {}).get("result", {})
            result_str = (
                result_data.get("content", "")
                if isinstance(result_data, dict)
                else str(result_data)
            )

            rows.append([
                ts,
                subagent[:25],
                tool,
                _truncate(detail, 60),
                _truncate(result_str, 60),
            ])

    print(f"\nEXTERNAL ACCESS AUDIT ({len(rows)} events)")
    print("-" * 120)
    _print_table(
        ["Timestamp", "Subagent", "Tool", "URL/Command", "Result"],
        rows,
    )


def _output_search(
    regex: str,
    event_type_filter: Optional[str],
    ancestry: AncestryIndex,
    store: EventStore,
) -> None:
    """Full-text search across all events with deduplication."""
    pattern = re.compile(regex, re.IGNORECASE)
    seen_hashes: set[str] = set()
    rows: list[list] = []

    for evt in store.events:
        etype = evt.get("type", "")
        if event_type_filter and etype != event_type_filter:
            continue

        data = evt.get("data", {})
        searchable = ""

        if etype in ("assistant.message", "user.message"):
            searchable = data.get("content", "")
        elif etype == "tool.execution_start":
            args = data.get("arguments", {})
            searchable = _dumps(args)
        elif etype == "tool.execution_complete":
            result = data.get("result", {})
            searchable = (
                result.get("content", "")
                if isinstance(result, dict)
                else str(result)
            )
        elif etype == "subagent.completed":
            searchable = _dumps(data)
        else:
            searchable = _dumps(data)

        m = pattern.search(searchable)
        if m:
            content_hash = hashlib.md5(
                searchable.encode("utf-8", errors="replace")
            ).hexdigest()
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)

            ts = evt.get("timestamp", "")[:19]
            eid = evt.get("id", "")
            subagent = ancestry.subagent_name(eid)

            s = max(0, m.start() - 40)
            e = min(len(searchable), m.end() + 40)
            snippet = searchable[s:e].replace("\n", " ")
            rows.append([ts, etype, subagent, _truncate(snippet, 80)])

    print(f"\nSEARCH: /{regex}/ ({len(rows)} matches)")
    if event_type_filter:
        print(f"  Filtered by type: {event_type_filter}")
    print("-" * 120)
    _print_table(["Timestamp", "Event Type", "Subagent", "Context"], rows)


def _output_file_history(
    path_filter: str,
    ancestry: AncestryIndex,
    store: EventStore,
) -> None:
    """Show history of file operations matching a path substring."""
    path_lower = path_filter.lower()
    rows: list[list] = []

    for evt in store.events:
        if evt.get("type") != "tool.execution_start":
            continue
        data = evt.get("data", {})
        tool = data.get("toolName", "")
        if tool not in ("create", "edit", "view"):
            continue

        args = data.get("arguments", {})
        file_path = args.get("path", "")
        if not file_path or path_lower not in file_path.lower():
            continue

        ts = evt.get("timestamp", "")[:19]
        eid = evt.get("id", "")
        subagent = ancestry.subagent_name(eid)

        detail = ""
        if tool == "create":
            text = args.get("file_text", "")
            detail = _truncate(text, 200)
        elif tool == "edit":
            old = args.get("old_str", "")
            new = args.get("new_str", "")
            detail = f"old: {_truncate(old, 100)} -> new: {_truncate(new, 100)}"

        rows.append([ts, tool, subagent[:25], file_path, _truncate(detail, 60)])

    print(f"\nFILE HISTORY: *{path_filter}* ({len(rows)} operations)")
    print("-" * 120)
    _print_table(
        ["Timestamp", "Operation", "Subagent", "Path", "Detail"],
        rows,
    )


def _output_trace_claim(
    claim: str,
    ancestry: AncestryIndex,
    store: EventStore,
) -> None:
    """Trace propagation of a string/regex through the session."""
    try:
        pattern = re.compile(claim, re.IGNORECASE)
    except re.error:
        pattern = re.compile(re.escape(claim), re.IGNORECASE)

    hits: list[dict[str, str]] = []

    for evt in store.events:
        etype = evt.get("type", "")
        data = evt.get("data", {})

        searchable = ""
        source_desc = ""

        if etype == "assistant.message":
            searchable = data.get("content", "")
            source_desc = "assistant message"
        elif etype == "tool.execution_start":
            tool = data.get("toolName", "")
            args = data.get("arguments", {})
            searchable = _dumps(args)
            source_desc = f"tool call ({tool})"
        elif etype == "tool.execution_complete":
            result = data.get("result", {})
            searchable = (
                result.get("content", "")
                if isinstance(result, dict)
                else str(result)
            )
            source_desc = "tool result"
        else:
            continue

        m = pattern.search(searchable)
        if m:
            ts = evt.get("timestamp", "")
            eid = evt.get("id", "")
            subagent = ancestry.subagent_name(eid)

            s = max(0, m.start() - 40)
            e = min(len(searchable), m.end() + 40)
            snippet = searchable[s:e].replace("\n", " ")

            hits.append({
                "timestamp": ts,
                "subagent": subagent,
                "event_type": source_desc,
                "snippet": _truncate(snippet, 100),
            })

    print(f"\nTRACE CLAIM: '{claim}' ({len(hits)} appearances)")
    print("=" * 100)

    if not hits:
        print("  No matches found.")
        return

    first = hits[0]
    print(f"\n  First appearance:")
    print(f"    Time:     {first['timestamp'][:19]}")
    print(f"    Subagent: {first['subagent']}")
    print(f"    Source:   {first['event_type']}")
    print(f"    Context:  {first['snippet']}")

    by_subagent: dict[str, list[dict]] = defaultdict(list)
    for h in hits[1:]:
        by_subagent[h["subagent"]].append(h)

    if by_subagent:
        print(f"\n  Propagation ({len(hits) - 1} subsequent appearances):")
        for sa, sa_hits in sorted(by_subagent.items()):
            print(f"\n    {sa} ({len(sa_hits)} hits):")
            for h in sa_hits[:5]:
                print(
                    f"      [{h['timestamp'][:19]}]"
                    f" {h['event_type']}: {h['snippet']}"
                )
            if len(sa_hits) > 5:
                print(f"      ... and {len(sa_hits) - 5} more")


def _output_subagent_tree(ancestry: AncestryIndex) -> None:
    """Print an indented tree of subagent relationships."""
    tree: dict[str, dict[str, Any]] = {}
    roots: list[str] = []

    for tcid, eid in ancestry.subagent_start_by_tcid.items():
        data = ancestry.subagent_starts.get(eid, {})
        args = ancestry.task_args.get(tcid, {})
        completion = ancestry.subagent_completions.get(tcid, {})

        name = args.get("name", data.get("agentName", "?"))
        agent_type = args.get("agent_type", data.get("agentName", "?"))
        tokens = completion.get("totalTokens", 0)
        dur_ms = completion.get("durationMs", 0)

        tree[tcid] = {
            "name": name,
            "agent_type": agent_type,
            "tokens": tokens or 0,
            "duration_ms": dur_ms or 0,
            "children": [],
            "parent_tcid": None,
            "timestamp": data.get("timestamp", ""),
        }

        parent_info = ancestry.resolve_parent_subagent(eid)
        if parent_info:
            tree[tcid]["parent_tcid"] = parent_info[1]
        else:
            roots.append(tcid)

    # Build children lists
    for tcid, node in tree.items():
        ptcid = node["parent_tcid"]
        if ptcid and ptcid in tree:
            tree[ptcid]["children"].append(tcid)
        elif ptcid and ptcid not in tree and tcid not in roots:
            roots.append(tcid)

    # Sort by timestamp
    for node in tree.values():
        node["children"].sort(key=lambda c: tree[c].get("timestamp", ""))
    roots.sort(key=lambda c: tree[c].get("timestamp", ""))

    print(f"\nSUBAGENT TREE ({len(tree)} subagents)")
    print("=" * 80)

    def _node_label(tcid: str) -> str:
        n = tree[tcid]
        dur = _fmt_duration(n["duration_ms"] / 1000) if n["duration_ms"] else "?"
        tok = _fmt_tokens(n["tokens"])
        return f"{n['name']} ({n['agent_type']}, {dur}, {tok} tok)"

    def _print_subtree(tcid: str, prefix: str) -> None:
        children = tree[tcid]["children"]
        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            print(f"{prefix}+-- {_node_label(child)}")
            extension = "    " if is_last else "|   "
            _print_subtree(child, prefix + extension)

    for root_tcid in roots:
        print(f"  {_node_label(root_tcid)}")
        _print_subtree(root_tcid, "  ")


def _output_cost_by_issue(ancestry: AncestryIndex) -> None:
    """Group subagents by issue/task pattern and show token costs."""
    groups: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "tokens": 0, "duration_ms": 0, "names": []}
    )

    for tcid in ancestry.subagent_start_by_tcid:
        args = ancestry.task_args.get(tcid, {})
        sa_eid = ancestry.subagent_start_by_tcid[tcid]
        data = ancestry.subagent_starts.get(sa_eid, {})
        completion = ancestry.subagent_completions.get(tcid, {})

        name = args.get("name", data.get("agentName", "?"))
        group = _cost_group_name(name)

        groups[group]["count"] += 1
        groups[group]["tokens"] += completion.get("totalTokens", 0) or 0
        groups[group]["duration_ms"] += completion.get("durationMs", 0) or 0
        groups[group]["names"].append(name)

    final_groups = _merge_cost_groups(dict(groups))

    sorted_groups = sorted(final_groups.items(), key=lambda x: -x[1]["tokens"])

    rows: list[list] = []
    for gname, data in sorted_groups:
        dur = (
            _fmt_duration(data["duration_ms"] / 1000)
            if data["duration_ms"]
            else "?"
        )
        rows.append([gname, data["count"], f"{data['tokens']:,}", dur])

    total_tokens = sum(g["tokens"] for g in final_groups.values())
    total_dur = sum(g["duration_ms"] for g in final_groups.values())

    print(
        f"\nCOST BY ISSUE ({len(final_groups)} groups,"
        f" {total_tokens:,} total tokens,"
        f" {_fmt_duration(total_dur / 1000) if total_dur else '?'} total)"
    )
    print("-" * 80)
    _print_table(
        ["Group", "Count", "Total Tokens", "Total Duration"],
        rows,
    )


def _output_enhanced_timeline(
    timeline_c: TimelineCollector,
    ancestry: AncestryIndex,
    from_ts: Optional[str],
    to_ts: Optional[str],
) -> None:
    """Print timeline with timestamp filtering and nesting visualization."""
    tl = timeline_c.result()
    event_ids = timeline_c._event_ids

    from_dt = _parse_ts(from_ts) if from_ts else None
    to_dt = _parse_ts(to_ts) if to_ts else None

    filtered: list[tuple[int, str, str, str, str]] = []
    for i, (ts, etype, summary) in enumerate(tl):
        dt = _parse_ts(ts)
        if from_dt and dt and dt < from_dt:
            continue
        if to_dt and dt and dt > to_dt:
            continue
        eid = event_ids[i] if i < len(event_ids) else ""
        filtered.append((i, ts, etype, summary, eid))

    range_label = ""
    if from_ts or to_ts:
        f = from_ts[:19] if from_ts else "start"
        t = to_ts[:19] if to_ts else "end"
        range_label = f", filtered {f} -> {t}"

    print(f"\nTIMELINE ({len(filtered)} key events{range_label})")
    print("-" * 80)

    for _, ts, etype, summary, eid in filtered:
        short_ts = ts[:19].replace("T", " ") if ts else "?"
        tag = etype.split(".")[-1]
        depth = ancestry.subagent_depth(eid) if eid else 0

        # Enhanced labels for subagent events (shown at parent level)
        if etype == "subagent.started":
            depth = max(0, depth - 1)
            sa_name = _resolve_task_name_for_event(eid, ancestry)
            label = f"▶ START {sa_name}"
        elif etype == "subagent.completed":
            sa_name = _resolve_task_name_for_completed(eid, ancestry)
            label = f"■ DONE  {summary}" if not sa_name else f"■ DONE  {sa_name}"
        else:
            label = summary

        indent = "  " * depth
        print(f"  {indent}{short_ts}  [{tag:<20}] {label}")


def _resolve_task_name_for_event(eid: str, ancestry: AncestryIndex) -> str:
    """Resolve the task name for a subagent.started event."""
    data = ancestry.subagent_starts.get(eid, {})
    tcid = data.get("toolCallId", "")
    if tcid:
        args = ancestry.task_args.get(tcid, {})
        name = args.get("name", "")
        if name:
            agent_type = args.get("agent_type", data.get("agentName", "?"))
            return f"{name} ({agent_type})"
    return data.get("agentName", "?")


def _resolve_task_name_for_completed(eid: str, ancestry: AncestryIndex) -> str:
    """Resolve the task name for a subagent.completed event."""
    # Walk parentId chain to find which subagent this completion belongs to
    resolved = ancestry.resolve_subagent(eid)
    if resolved:
        name = resolved[0]
        tcid = resolved[1]
        comp = ancestry.subagent_completions.get(tcid, {})
        model = comp.get("model", "")
        dur_ms = comp.get("durationMs", 0)
        dur_str = _fmt_duration(dur_ms / 1000) if dur_ms else "?"
        tokens = comp.get("totalTokens", "?")
        parts = [name]
        if model:
            parts.append(model)
        parts.append(dur_str)
        parts.append(f"{tokens} tok")
        return f"{name} ({', '.join(parts[1:])})"
    return ""


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

    if _HAS_ORJSON:
        fh = open(path, "rb", buffering=1_048_576)
    else:
        fh = open(path, encoding="utf-8", buffering=1_048_576)

    try:
        for lineno, line in enumerate(fh, 1):
            stripped = line.strip() if isinstance(line, str) else line.strip()
            if not stripped:
                continue
            try:
                evt = _loads(stripped)
            except (json.JSONDecodeError, ValueError):
                print(f"[WARN] Malformed JSON on line {lineno}, skipping", file=sys.stderr)
                continue

            etype = evt.get("type", "")

            for c in wants_all:
                c.process(evt)

            if etype in type_dispatch:
                for c in type_dispatch[etype]:
                    c.process(evt)
    finally:
        fh.close()


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
    if _HAS_ORJSON:
        fh = open(path, "rb", buffering=1_048_576)
    else:
        fh = open(path, encoding="utf-8", buffering=1_048_576)
    try:
        for lineno, line in enumerate(fh, 1):
            stripped = line.strip() if isinstance(line, str) else line.strip()
            if not stripped:
                continue
            try:
                evt = _loads(stripped)
            except (json.JSONDecodeError, ValueError):
                print(f"[WARN] Malformed JSON on line {lineno}, skipping", file=sys.stderr)
                continue
            if type_filter is None or evt.get("type") in type_filter:
                yield evt
    finally:
        fh.close()


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


def build_ancestry_index(path: str | Path) -> AncestryIndex:
    """Build an AncestryIndex from an event log."""
    c = AncestryIndex()
    run_collectors(path, [c])
    return c


def build_subagent_tree(path: str | Path) -> None:
    """Print the subagent tree for a session log."""
    c = AncestryIndex()
    run_collectors(path, [c])
    _output_subagent_tree(c)


def search_events(
    path: str | Path,
    regex: str,
    event_type: Optional[str] = None,
) -> None:
    """Search all events in a session log for a regex pattern."""
    ancestry = AncestryIndex()
    store = EventStore()
    run_collectors(path, [ancestry, store])
    _output_search(regex, event_type, ancestry, store)


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
    # --- Existing flags ---
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

    # --- V2 flags ---
    parser.add_argument(
        "--subagent-transcript",
        metavar="NAME",
        help="Print chronological transcript of a named subagent",
    )
    parser.add_argument(
        "--search-tools",
        metavar="REGEX",
        help="Search tool arguments and results with a regex",
    )
    parser.add_argument(
        "--tool-name",
        metavar="NAME",
        help="Filter --search-tools by tool name",
    )
    parser.add_argument(
        "--audit-external",
        action="store_true",
        help="Audit external network and package-install access",
    )
    parser.add_argument(
        "--search",
        metavar="REGEX",
        help="Full-text search across all events",
    )
    parser.add_argument(
        "--event-type",
        metavar="TYPE",
        help="Filter --search by event type",
    )
    parser.add_argument(
        "--file-history",
        metavar="PATH",
        help="Show history of create/edit/view operations on a file path",
    )
    parser.add_argument(
        "--trace-claim",
        metavar="STRING",
        help="Trace propagation of a string/regex through the session",
    )
    parser.add_argument(
        "--subagent-tree",
        action="store_true",
        help="Print indented tree of subagent relationships",
    )
    parser.add_argument(
        "--cost-by-issue",
        action="store_true",
        help="Group subagents by issue/task pattern and show token costs",
    )
    parser.add_argument(
        "--from",
        dest="from_ts",
        metavar="TIMESTAMP",
        help="Filter --timeline from this ISO 8601 timestamp",
    )
    parser.add_argument(
        "--to",
        dest="to_ts",
        metavar="TIMESTAMP",
        help="Filter --timeline up to this ISO 8601 timestamp",
    )

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    # Detect which v2 features are requested
    v2_needs_ancestry = any([
        args.subagent_transcript,
        args.search_tools,
        args.audit_external,
        args.search,
        args.file_history,
        args.trace_claim,
        args.subagent_tree,
        args.cost_by_issue,
        args.from_ts or args.to_ts,
        args.timeline,
    ])
    v2_needs_store = any([
        args.subagent_transcript,
        args.search_tools,
        args.audit_external,
        args.search,
        args.file_history,
        args.trace_claim,
    ])

    any_flag = any([
        args.summary, args.timeline, args.messages, args.subagents,
        args.tools, args.conversation is not None, args.git, args.export,
        args.subagent_transcript, args.search_tools, args.audit_external,
        args.search, args.file_history, args.trace_claim,
        args.subagent_tree, args.cost_by_issue,
    ])

    # Default to --summary if nothing specified
    if not any_flag:
        args.summary = True

    # Build collectors for all requested analyses
    collectors: list[Collector] = []
    summary_c = timeline_c = messages_c = subagents_c = None
    tools_c = conversation_c = git_c = None
    ancestry_c: Optional[AncestryIndex] = None
    store_c: Optional[EventStore] = None

    # V2 shared infrastructure
    if v2_needs_ancestry:
        ancestry_c = AncestryIndex()
        collectors.append(ancestry_c)
    if v2_needs_store:
        store_c = EventStore()
        collectors.append(store_c)

    if args.summary:
        summary_c = SummaryCollector()
        collectors.append(summary_c)
    if args.timeline or args.export or args.from_ts or args.to_ts:
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

    # -----------------------------------------------------------------------
    # Format and print results
    # -----------------------------------------------------------------------

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

    # Enhanced timeline (always shows nesting + START/DONE markers)
    if timeline_c is not None and args.timeline:
        if ancestry_c is not None:
            _output_enhanced_timeline(
                timeline_c, ancestry_c, args.from_ts, args.to_ts
            )
        else:
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

    # -----------------------------------------------------------------------
    # V2 feature output
    # -----------------------------------------------------------------------

    if args.subagent_tree and ancestry_c is not None:
        _output_subagent_tree(ancestry_c)

    if args.cost_by_issue and ancestry_c is not None:
        _output_cost_by_issue(ancestry_c)

    if args.subagent_transcript and ancestry_c is not None and store_c is not None:
        _output_subagent_transcript(args.subagent_transcript, ancestry_c, store_c)

    if args.search_tools and ancestry_c is not None and store_c is not None:
        _output_search_tools(
            args.search_tools, args.tool_name, ancestry_c, store_c
        )

    if args.audit_external and ancestry_c is not None and store_c is not None:
        _output_audit_external(ancestry_c, store_c)

    if args.search and ancestry_c is not None and store_c is not None:
        _output_search(args.search, args.event_type, ancestry_c, store_c)

    if args.file_history and ancestry_c is not None and store_c is not None:
        _output_file_history(args.file_history, ancestry_c, store_c)

    if args.trace_claim and ancestry_c is not None and store_c is not None:
        _output_trace_claim(args.trace_claim, ancestry_c, store_c)


if __name__ == "__main__":
    main()
