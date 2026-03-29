---
name: writing-hooks
description: >-
  Guide for authoring Copilot CLI hooks (hooks.json lifecycle event handlers).
  Use when asked to author hooks, create lifecycle hooks, configure
  session hooks, add pre/post tool hooks, or set up .github/hooks.
license: MIT
---

# Authoring Hooks for GitHub Copilot CLI

Hooks let you execute custom shell commands at specific points during a Copilot CLI session lifecycle. They provide programmable control and observability around Copilot's behavior — enforcing guardrails, logging activity, and automating responses to events.

## Procedure: Authoring a Hook

1. **Decide whether a hook is the right mechanism** — for workflow instructions, author a skill instead. For persistent preferences, author custom instructions instead. For new external capabilities, add an MCP server. See the `writing-skills` and `writing-custom-instructions` skills.
2. **Choose the trigger** — identify which lifecycle event should fire the hook (see [Available Hook Triggers](#available-hook-triggers) below).
3. **Create or edit a hook JSON file** in `.github/hooks/` — you can have multiple files with any name.
4. **Author the hook entry** — define the command for `bash` and/or `powershell`, set a working directory and timeout.
5. **Author supporting scripts** (if needed) — for complex logic, reference external scripts rather than inline commands.
6. **Test the hook in isolation** — pipe sample JSON into your script and verify exit code and output before deploying.
7. **Test in a live session** — start a Copilot CLI session and trigger the lifecycle event. Verify the hook fires and behaves as expected.

## When to Author Hooks (vs Other Customization)

- **Author hooks** for programmable guardrails, logging, automation, or policy enforcement around tool use and session events.
- **Author skills** for workflow instructions and task-specific procedures.
- **Author custom instructions** for persistent preferences and coding standards.
- **Add MCP servers** for new external capabilities and tool integrations.

## File Location

```
.github/hooks/
├── my-hooks.json       # Any name ending in .json
└── security-hooks.json # Multiple hook files are supported
```

Hook files must be on the repository's **default branch** for the coding agent to use them. Copilot CLI loads hooks from the `.github/hooks/` directory in the current working directory.

## Configuration Format

Hooks are defined in a JSON file with `version: 1`:

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [],
    "sessionEnd": [],
    "userPromptSubmitted": [],
    "preToolUse": [],
    "postToolUse": [],
    "errorOccurred": [],
    "agentStop": [],
    "subagentStop": []
  }
}
```

## Available Hook Triggers

| Hook | Fires When |
|------|-----------|
| `sessionStart` | A CLI session begins |
| `sessionEnd` | A CLI session ends |
| `userPromptSubmitted` | A user submits a prompt |
| `preToolUse` | Before a tool is executed |
| `postToolUse` | After a tool finishes executing |
| `errorOccurred` | An error occurs during execution |
| `agentStop` | The main agent stops without an error |
| `subagentStop` | A subagent completes its task |

## Hook Command Syntax

Each hook entry specifies commands for `bash` and/or `powershell`:

```json
{
  "type": "command",
  "bash": "echo \"Session started: $(date)\" >> logs/session.log",
  "powershell": "Add-Content -Path logs/session.log -Value \"Session started: $(Get-Date)\"",
  "cwd": ".",
  "timeoutSec": 10,
  "env": {
    "LOG_LEVEL": "INFO"
  }
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | Yes | Must be `"command"` |
| `bash` | string | No* | Shell command for Unix/macOS |
| `powershell` | string | No* | Shell command for Windows |
| `cwd` | string | No | Working directory for the command |
| `timeoutSec` | number | No | Timeout in seconds (default: 30) |
| `env` | object | No | Additional environment variables |

*At least one of `bash` or `powershell` should be provided.

## Examples

### Session Logging

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "type": "command",
        "bash": "echo \"Session started: $(date)\" >> logs/session.log",
        "powershell": "Add-Content -Path logs/session.log -Value \"Session started: $(Get-Date)\"",
        "cwd": ".",
        "timeoutSec": 10
      }
    ],
    "sessionEnd": [
      {
        "type": "command",
        "bash": "echo \"Session ended: $(date)\" >> logs/session.log",
        "powershell": "Add-Content -Path logs/session.log -Value \"Session ended: $(Get-Date)\"",
        "cwd": ".",
        "timeoutSec": 10
      }
    ]
  }
}
```

### Prompt Logging with External Script

```json
{
  "version": 1,
  "hooks": {
    "userPromptSubmitted": [
      {
        "type": "command",
        "bash": "./scripts/log-prompt.sh",
        "powershell": "./scripts/log-prompt.ps1",
        "cwd": "scripts",
        "env": {
          "LOG_LEVEL": "INFO"
        }
      }
    ]
  }
}
```

### Pre-Tool Guard (Block Dangerous Commands)

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": "./scripts/validate-tool.sh",
        "powershell": "./scripts/validate-tool.ps1",
        "cwd": ".",
        "timeoutSec": 5
      }
    ]
  }
}
```

The hook script receives a JSON payload on stdin with context about the tool being invoked (tool name, arguments, etc.). The script can output JSON to modify behavior (e.g., block execution).

## Hook Input and Output

### Input

Hook scripts receive a JSON object on stdin containing context about the triggering event. The payload varies by hook type but commonly includes:

- `timestamp` — when the event occurred
- `cwd` — current working directory
- `toolName` — (for tool hooks) the tool being invoked
- `toolArgs` — (for tool hooks) the tool's arguments as a JSON string

### Output

Hook scripts can output JSON to influence agent behavior. The output must be **compact JSON on a single line**.

## Debugging Hooks

### Enable debug mode in scripts

```bash
#!/bin/bash
set -x  # Enable bash debug mode
INPUT=$(cat)
echo "DEBUG: Received input" >&2
echo "$INPUT" >&2
# ... rest of script
```

### Test hooks locally

```bash
# Pipe test input into your hook script
echo '{"timestamp":1704614400000,"cwd":"/tmp","toolName":"bash","toolArgs":"{\"command\":\"ls\"}"}' | ./my-hook.sh

# Check exit code
echo $?

# Validate output is valid JSON
./my-hook.sh < test-input.json | jq .
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hooks not executing | Verify JSON is in `.github/hooks/`, check for valid JSON syntax, ensure `version: 1` is set |
| Hooks timing out | Increase `timeoutSec`, optimize script performance |
| Invalid JSON output | Ensure output is on a single line; use `jq -c` (Unix) or `ConvertTo-Json -Compress` (Windows) |
| Script not found | Check `cwd` is correct, ensure script is executable (`chmod +x`) |

## Best Practices for Authoring Hooks

1. **Keep hooks fast** — hooks run synchronously and block the agent. Use reasonable timeouts.
2. **Provide both `bash` and `powershell`** — ensures cross-platform compatibility.
3. **Log to stderr for debugging** — stdout is parsed as the hook's response; diagnostic output should go to stderr.
4. **Use scripts for complex logic** — inline commands get unwieldy; reference external scripts.
5. **Test hooks in isolation** — pipe sample JSON into your scripts before deploying.
6. **Set appropriate timeouts** — the default 30 seconds is generous; most hooks should complete in under 5 seconds.
7. **Don't block unnecessarily** — hooks that block tool use should have clear, documented reasons.
