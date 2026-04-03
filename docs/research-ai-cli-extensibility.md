# AI Coding CLI Extensibility Research

> **Date**: July 2025
> **Researcher role**: Web Researcher (per `.github/agents/research-team/members/web-researcher.md`)
> **Methodology**: Web search → primary source verification via official docs, GitHub repos, and code search

---

## 1. Claude Code (Anthropic)

### Source: Official Anthropic documentation (docs.anthropic.com/en/docs/claude-code/*)
### Status: CONFIRMED — extremely comprehensive extensibility

### Evidence & Raw Findings

#### 1.1 Plugin System
**Status: CONFIRMED**
- Full unified plugin architecture with `.claude-plugin/plugin.json` manifest
- Plugins can bundle: skills, agents, hooks, MCP servers, LSP servers, slash commands, and settings
- Official Anthropic marketplace at `claude-plugins-official` (auto-available)
- Demo marketplace at `anthropics/claude-code` GitHub repo
- Plugin marketplaces can be: GitHub repos, Git URLs, local paths, or remote URLs
- Plugins namespaced as `/plugin-name:skill-name` to prevent conflicts
- Scopes: user, project, local, managed (enterprise)
- CLI management: `/plugin install`, `/plugin disable`, `/plugin enable`, `/plugin uninstall`
- Version management with semantic versioning
- Auto-update support for marketplaces
- URL: https://docs.anthropic.com/en/docs/claude-code/plugins

**Confirmed plugin categories in official marketplace:**
- Code intelligence (LSP): clangd, gopls, pyright, rust-analyzer, typescript, etc.
- External integrations: GitHub, GitLab, Atlassian, Asana, Linear, Notion, Figma, Vercel, Firebase, Supabase, Slack, Sentry
- Development workflows: commit-commands, pr-review-toolkit, agent-sdk-dev, plugin-dev
- Output styles: explanatory-output-style, learning-output-style

#### 1.2 Custom Instructions (CLAUDE.md)
**Status: CONFIRMED**
- `CLAUDE.md` files at multiple scopes: managed policy, project (`./CLAUDE.md` or `./.claude/CLAUDE.md`), user (`~/.claude/CLAUDE.md`)
- Directory-hierarchy traversal: walks up from CWD loading all ancestor CLAUDE.md files
- Subdirectory CLAUDE.md files loaded on-demand when Claude reads files in those dirs
- Import syntax: `@path/to/import` for pulling in other files (up to 5 hops deep)
- `.claude/rules/` directory for modular, topic-specific instruction files
- Path-scoped rules via YAML frontmatter `paths:` field (glob patterns)
- User-level rules in `~/.claude/rules/`
- AGENTS.md interop: can import AGENTS.md into CLAUDE.md
- Auto memory: Claude writes its own persistent notes across sessions
- HTML comments stripped from context (for human-only notes)
- URL: https://docs.anthropic.com/en/docs/claude-code/memory

#### 1.3 Hooks (Pre/Post-Action Triggers)
**Status: CONFIRMED — extremely mature**
- 25+ hook event types including:
  - `SessionStart`, `SessionEnd`
  - `UserPromptSubmit`
  - `PreToolUse`, `PostToolUse`, `PostToolUseFailure` (can block tool calls)
  - `PermissionRequest`, `PermissionDenied`
  - `SubagentStart`, `SubagentStop`
  - `TaskCreated`, `TaskCompleted`
  - `Stop`, `StopFailure`
  - `InstructionsLoaded`, `ConfigChange`
  - `CwdChanged`, `FileChanged`
  - `WorktreeCreate`, `WorktreeRemove`
  - `PreCompact`, `PostCompact`
  - `Elicitation`, `ElicitationResult`
  - `TeammateIdle`
  - `Notification`
- Four hook handler types:
  - **Command hooks** (`type: "command"`): shell commands, receive JSON on stdin
  - **HTTP hooks** (`type: "http"`): POST to URL endpoints
  - **Prompt hooks** (`type: "prompt"`): single-turn LLM evaluation
  - **Agent hooks** (`type: "agent"`): subagent with Read/Grep/Glob tools
- Matcher patterns: regex-based filtering on tool name, event type, etc.
- `if` field: permission-rule-syntax for granular matching (e.g., `"Bash(git *)"`, `"Edit(*.ts)"`)
- Hook scopes: user settings, project settings, local settings, managed policy, plugin hooks, skill/agent frontmatter
- Async hooks supported (run in background without blocking)
- URL: https://docs.anthropic.com/en/docs/claude-code/hooks

#### 1.4 MCP (Model Context Protocol) Support
**Status: CONFIRMED — first-class**
- Full MCP client with stdio, SSE, and HTTP transports
- Three installation scopes: local, project (`.mcp.json` in repo), user
- CLI management: `claude mcp add`, `claude mcp list`, `claude mcp get`, `claude mcp remove`
- OAuth 2.0 authentication support
- Dynamic tool updates via MCP `list_changed` notifications
- Plugin-provided MCP servers (auto-start with plugin)
- Environment variable expansion in `.mcp.json`
- Channels: MCP servers can push messages into sessions (Telegram, Discord, webhooks)
- URL: https://docs.anthropic.com/en/docs/claude-code/mcp

#### 1.5 Skills (Reusable Procedures)
**Status: CONFIRMED**
- `SKILL.md` files in `.claude/skills/<name>/` directories
- YAML frontmatter: name, description, allowed-tools, model, context, hooks, paths, etc.
- Skill scopes: enterprise, personal (`~/.claude/skills/`), project (`.claude/skills/`), plugin
- Supports `$ARGUMENTS` substitution, `$CLAUDE_SESSION_ID`, `$CLAUDE_SKILL_DIR`
- Can run in forked subagent context (`context: fork`)
- Invocation control: `disable-model-invocation`, `user-invocable`
- Bundled skills: `/batch`, `/claude-api`, `/debug`, `/loop`, `/simplify`
- Follows the [Agent Skills](https://agentskills.io) open standard
- URL: https://docs.anthropic.com/en/docs/claude-code/skills

#### 1.6 Custom Agents (Subagents)
**Status: CONFIRMED**
- Markdown files with YAML frontmatter in `.claude/agents/` or `~/.claude/agents/`
- Configurable: tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, isolation
- Built-in subagents: Explore, Plan, General-purpose, Bash, statusline-setup, Claude Code Guide
- Can run in isolated git worktrees (`isolation: "worktree"`)
- Persistent memory across sessions (`memory: user|project|local`)
- Background execution support
- Agent teams: teammates that inherit subagent definitions
- CLI-defined subagents via `--agents` JSON flag
- URL: https://docs.anthropic.com/en/docs/claude-code/sub-agents

#### 1.7 Automation Frameworks
**Status: CONFIRMED**
- Python scripting via Agent SDK
- `--message` flag for headless single-instruction mode
- GitHub Actions integration for PR reviews and issue triage
- GitLab CI/CD integration
- Slack integration for routing bug reports
- Scheduled tasks (cloud and desktop)
- Remote control for continuing sessions across devices

### Dead Ends
- None significant — Claude Code's documentation is comprehensive and well-organized

---

## 2. Aider (Aider-AI/aider)

### Source: aider.chat official docs, GitHub repo (Aider-AI/aider)
### Status: CONFIRMED — configuration-heavy, no formal plugin system

### Evidence & Raw Findings

#### 2.1 Plugin System
**Status: NOT FOUND — no formal plugin system exists**
- Aider has NO plugin architecture, no plugin marketplace, no plugin manifest format
- Extensibility is achieved through configuration files and conventions, not a plugin API
- The `/load` command can execute batched commands from a file, providing rudimentary scripting
- URL: https://aider.chat/docs/usage/commands.html

#### 2.2 Configuration / Customization
**Status: CONFIRMED — extensive config system**
- `.aider.conf.yml`: YAML config file searched in home dir, git root, and CWD (loaded in that order)
- `.env` file support for API keys and environment variables
- `AIDER_xxx` environment variables for all options
- 100+ configurable options covering: model selection, git behavior, output, caching, voice, analytics
- Model aliases and custom model metadata files
- `.aiderignore` file (like .gitignore for aider)
- URL: https://aider.chat/docs/config/aider_conf.html

#### 2.3 Custom Instructions / Conventions
**Status: CONFIRMED**
- `CONVENTIONS.md` (or any markdown file) loaded via `/read CONVENTIONS.md` or `--read CONVENTIONS.md`
- Read-only context: conventions are injected but not editable by the model
- Can auto-load via `.aider.conf.yml` `read:` key
- Community conventions repository: https://github.com/Aider-AI/conventions
- Custom system prompts via `--commit-prompt` for commit messages
- URL: https://aider.chat/docs/usage/conventions.html

#### 2.4 MCP Support
**Status: NOT FOUND in core Aider**
- GitHub code search and official docs show NO native MCP client in Aider
- Third-party community projects exist:
  - `disler/aider-mcp-server`: wraps Aider as an MCP *server* (so other MCP clients can use Aider)
  - `mcpm-aider`: CLI tool for managing MCP integrations with Aider
- These are **external wrappers**, not native Aider features
- Aider's README (verified on GitHub) makes no mention of MCP
- URL: https://github.com/Aider-AI/aider/blob/main/README.md

#### 2.5 Custom Tools / Commands
**Status: PARTIAL**
- Built-in slash commands only (not user-extensible)
- ~35 built-in commands: /add, /ask, /code, /commit, /lint, /test, /web, /voice, etc.
- `/load` command: executes commands from a file (basic scripting)
- `/run` command: runs arbitrary shell commands
- `/test` command: runs shell command and feeds output on failure
- No mechanism to define custom slash commands
- URL: https://aider.chat/docs/usage/commands.html

#### 2.6 Scripting / Automation API
**Status: CONFIRMED**
- CLI scripting: `aider --message "instruction" file.py` for headless single-shot mode
- Shell scripting: loop over files with `--message`
- Python API (unofficial/unsupported):
  ```python
  from aider.coders import Coder
  from aider.models import Model
  coder = Coder.create(main_model=Model("gpt-4-turbo"), fnames=["file.py"])
  coder.run("instruction")
  ```
- Flags for automation: `--yes`, `--auto-commits`, `--dry-run`, `--no-stream`
- NOTE: "The python scripting API is not officially supported or documented, and could change in future releases"
- URL: https://aider.chat/docs/scripting.html

#### 2.7 Hooks / Guards
**Status: NOT FOUND**
- No pre/post-action hook system
- `--lint-cmd`: run lint commands after changes (closest to a post-action hook)
- `--test-cmd`: run test commands after changes
- `--auto-lint` and `--auto-test` flags for automatic post-change validation
- `--git-commit-verify`: enable/disable git pre-commit hooks
- These are fixed integration points, not a general-purpose hook framework

### Dead Ends
- Searched for "plugin", "extension", "hook", "MCP" in Aider docs — no native extensibility framework
- The `.aider.conf.yml` sample file (downloaded from GitHub) has no plugin-related fields
- Community MCP integrations exist but are external wrappers, not core features

---

## 3. Open Interpreter (OpenInterpreter/open-interpreter)

### Source: docs.openinterpreter.com, GitHub repo (OpenInterpreter/open-interpreter)
### Status: CONFIRMED — Python-native extensibility, no formal plugin system

### Evidence & Raw Findings

#### 3.1 Plugin System
**Status: NOT FOUND — no formal plugin system**
- No plugin architecture, no plugin manifest, no marketplace
- Extensibility is through Python profiles and the Python API
- GitHub code search for "plugin" OR "extension" OR "hook" in their docs directory: **0 results**

#### 3.2 Profiles (Configuration System)
**Status: CONFIRMED**
- Python profiles: full Python scripts that configure the `interpreter` object
- YAML profiles: declarative configuration files
- Stored in profiles directory (accessible via `interpreter --profiles`)
- Switch profiles: `interpreter --profile <name>`
- Configurable: model, temperature, context_window, max_tokens, auto_run, custom_instructions, system_message, and more
- Template profile available on GitHub for creating custom profiles
- URL: https://docs.openinterpreter.com/guides/profiles

#### 3.3 Custom Instructions
**Status: CONFIRMED**
- `custom_instructions` setting: appends text to the system message
- `system_message` setting: full system message override (not recommended)
- `user_message_template`: template applied to user messages
- `code_message_template`: template applied to code outputs
- URL: https://docs.openinterpreter.com/settings/all-settings

#### 3.4 MCP Support
**Status: NOT FOUND in codebase**
- GitHub code search for "MCP" OR "model context protocol" in OpenInterpreter/open-interpreter: **0 results**
- No mention of MCP in official documentation at docs.openinterpreter.com
- No MCP client or server implementation in the codebase
- Web search results claiming MCP support appear to be **AI-generated hallucinations** conflating general MCP ecosystem trends with OI's actual features
- **IMPORTANT**: Earlier web search summaries claiming "Built-in MCP client support" for Open Interpreter are UNVERIFIED and contradicted by code search evidence

#### 3.5 Custom Tools
**Status: PARTIAL**
- Open Interpreter's core extensibility is through code execution (Python, JS, shell)
- `computer` API: provides programmatic access to display, keyboard, mouse, clipboard, etc.
- `import_computer_api: True` gives the model access to a Computer API
- No formal custom tool registration system
- Users can extend functionality by writing Python code that the interpreter executes

#### 3.6 Automation / Scripting
**Status: CONFIRMED**
- Python API: `interpreter.chat("instruction")` for programmatic control
- `messages` property for conversation state management/restoration
- `auto_run: True` for unattended execution
- `loop: True` for task completion enforcement
- `max_budget` for cost control in automated scenarios
- `safe_mode` for code scanning in automated pipelines

#### 3.7 Hooks / Guards
**Status: NOT FOUND**
- No hook or guard system
- `safe_mode` options (`off`, `ask`, `auto`) provide basic safety scanning
- `auto_run` controls whether code requires confirmation
- No pre/post-action triggers

#### 3.8 Project Activity
**Status: CONFIRMED — appears less actively maintained**
- Last significant commit activity has slowed compared to 2023-2024
- The `0.1` branch and newer architecture were explored but the project appears to have pivoted
- Poetry-based Python project structure

### Dead Ends
- MCP support: completely unverified despite web search claims
- Plugin system: does not exist
- Hook system: does not exist
- All three searches (GitHub code search for MCP, plugin, hook in OI repo) returned 0 results

---

## Comparison Matrix

### Extensibility Mechanism Comparison

| Mechanism | GitHub Copilot CLI | Claude Code | Aider | Open Interpreter |
|---|---|---|---|---|
| **Plugin System** | No (uses skills/agents) | ✅ CONFIRMED — full plugin architecture with marketplace | ❌ None | ❌ None |
| **Skills / Procedures** | ✅ `.github/skills/` SKILL.md | ✅ `.claude/skills/` SKILL.md (same open standard) | ❌ None (closest: CONVENTIONS.md) | ❌ None |
| **Custom Agents** | ✅ `.github/agents/` .agent.md | ✅ `.claude/agents/` .md files | ❌ None | ❌ None |
| **Custom Instructions** | ✅ `copilot-instructions.md` | ✅ `CLAUDE.md` (hierarchical, multi-scope) | ✅ `CONVENTIONS.md` (read-only context) | ✅ `custom_instructions` setting |
| **Hooks / Guards** | ✅ `hooks.json` | ✅ 25+ event types, 4 handler types | ❌ None (only lint/test auto-run) | ❌ None |
| **MCP Support** | ✅ `mcp-config.json` | ✅ First-class (stdio, SSE, HTTP, OAuth) | ❌ Not native (community wrappers only) | ❌ Not found |
| **Configuration Files** | N/A (uses instructions) | `.claude/settings.json`, `CLAUDE.md` | `.aider.conf.yml`, `.env`, `.aiderignore` | Python/YAML profiles |
| **Scripting API** | N/A | ✅ Agent SDK (Python/TS) | ✅ CLI `--message` + Python API (unsupported) | ✅ Python API (`interpreter.chat()`) |
| **Slash Commands** | N/A | ✅ User-definable via skills | Built-in only (~35 commands) | ❌ None |
| **Marketplace / Ecosystem** | N/A | ✅ Official + community marketplaces | ❌ None (community conventions repo) | ❌ None |
| **Auto Memory** | N/A | ✅ Auto memory across sessions | ❌ None | ❌ None |

### Can Users Build Execution/Automation Frameworks?

| Tool | Assessment |
|---|---|
| **GitHub Copilot CLI** | Yes — via skills (reusable procedures), agents (specialized personas), hooks (pre/post guards), and MCP servers |
| **Claude Code** | **Yes — most comprehensive** — plugins bundle skills+agents+hooks+MCP into distributable packages with marketplace support |
| **Aider** | **Limited** — headless `--message` mode + Python API enables scripting, but no formal framework. Convention files + `/load` provide basic workflow definition |
| **Open Interpreter** | **Limited** — Python API enables scripting, profiles enable configuration presets, but no plugin/hook/tool registration system |

### MCP Support Status

| Tool | MCP Status |
|---|---|
| **GitHub Copilot CLI** | ✅ CONFIRMED — native MCP client via `mcp-config.json` |
| **Claude Code** | ✅ CONFIRMED — full MCP client with 3 transports, OAuth, channels, plugin-bundled servers |
| **Aider** | ❌ NOT NATIVE — community wrappers exist (aider-mcp-server exposes Aider *as* an MCP server) |
| **Open Interpreter** | ❌ NOT FOUND — zero evidence in codebase or docs despite web search claims |

### Plugin Ecosystem Maturity

| Tool | Ecosystem |
|---|---|
| **GitHub Copilot CLI** | Skills/agents in `.github/` — project-scoped, no central marketplace |
| **Claude Code** | **Most mature** — official Anthropic marketplace, community marketplaces, 20+ official plugins across LSP/integrations/workflows/styles |
| **Aider** | **Minimal** — community conventions repo only (https://github.com/Aider-AI/conventions) |
| **Open Interpreter** | **None** — no ecosystem beyond Python profiles |

---

## Key Insights

### 1. Claude Code is the closest competitor to GitHub Copilot CLI's extensibility model
Both use markdown-based skills/agents with YAML frontmatter. Claude Code's skills follow the same [Agent Skills open standard](https://agentskills.io). Claude Code goes further with a full plugin packaging and marketplace system.

### 2. Claude Code's hook system far exceeds all competitors
25+ lifecycle events with 4 handler types (command, HTTP, prompt, agent) versus Copilot CLI's hooks.json and nothing from Aider or Open Interpreter.

### 3. Aider is configuration-rich but extensibility-poor
Excellent configuration (.aider.conf.yml with 100+ options) but no plugin API, no custom commands, no hooks, no MCP. Extensibility relies on external scripting.

### 4. Open Interpreter is the least extensible
Python profiles and a scripting API, but no formal plugin, hook, tool registration, or MCP system. Web search AI summaries claiming MCP support are **contradicted by code search evidence**.

### 5. MCP is a dividing line
Claude Code and Copilot CLI have native MCP support. Aider and Open Interpreter do not. This matters because MCP is becoming the standard for AI tool integration.

### 6. CLAUDE.md vs CONVENTIONS.md vs custom_instructions
All three competitors have some form of custom instructions, but only Claude Code matches Copilot CLI in sophistication (hierarchical, multi-scope, path-scoped rules, auto-discovery).

---

## Sources

### Claude Code
- https://docs.anthropic.com/en/docs/claude-code/overview
- https://docs.anthropic.com/en/docs/claude-code/plugins
- https://docs.anthropic.com/en/docs/claude-code/discover-plugins
- https://docs.anthropic.com/en/docs/claude-code/hooks
- https://docs.anthropic.com/en/docs/claude-code/mcp
- https://docs.anthropic.com/en/docs/claude-code/skills
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
- https://docs.anthropic.com/en/docs/claude-code/memory
- https://github.com/anthropics/claude-plugins-official

### Aider
- https://aider.chat/docs/config.html
- https://aider.chat/docs/config/aider_conf.html
- https://aider.chat/docs/usage/commands.html
- https://aider.chat/docs/usage/conventions.html
- https://aider.chat/docs/scripting.html
- https://github.com/Aider-AI/aider/blob/main/README.md
- https://github.com/Aider-AI/conventions
- https://github.com/disler/aider-mcp-server (community, not core)

### Open Interpreter
- https://docs.openinterpreter.com/guides/profiles
- https://docs.openinterpreter.com/settings/all-settings
- https://github.com/OpenInterpreter/open-interpreter (repo root, pyproject.toml)
- GitHub code search: 0 results for MCP, plugin, extension, hook in docs/
