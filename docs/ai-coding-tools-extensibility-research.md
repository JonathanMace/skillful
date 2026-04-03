# AI Coding Tools: Extensibility & Plugin Systems Research

**Date**: 2026-04-01
**Researcher**: Web Researcher (following `.github/agents/research-team/members/web-researcher.md` protocol)
**Scope**: Cursor, Windsurf/Codeium, Cline — extensibility mechanisms compared to GitHub Copilot CLI

---

## Table of Contents

1. [Cursor](#1-cursor)
2. [Windsurf / Codeium](#2-windsurf--codeium)
3. [Cline](#3-cline)
4. [Comparative Matrix](#4-comparative-matrix)
5. [Sources](#5-sources)

---

## 1. Cursor

### Source: cursor.com, cursor.com/docs, community resources
### Status: CONFIRMED (multiple official and community sources)

### 1.1 Custom Rules System

**Status: CONFIRMED — Mature, multi-layered**

Cursor has the most elaborate rules system of the three tools:

| Mechanism | Location | Format | Scope |
|-----------|----------|--------|-------|
| `.cursorrules` (legacy) | Project root | Markdown | Whole project, deprecated |
| `.cursor/rules/*.mdc` | Project directory | Markdown + YAML frontmatter | Fine-grained, glob-based |
| User Rules | Cursor Settings UI | UI/Settings | All projects for that user |
| Team Rules | Team Dashboard (web) | Managed via web | Organization-wide |
| `AGENTS.md` | Project root | Markdown | AI agent-specific instructions |

**Modern rules** (`.cursor/rules/*.mdc`) support YAML frontmatter with:
- `alwaysApply: true/false` — persistent or conditional
- `globs: ["src/components/**"]` — file-pattern matching
- `description:` — AI uses this to decide when to apply
- Manual triggering via `@rule-name` in chat

**Evidence**: https://design.dev/guides/cursor-rules/, https://www.agentrulegen.com/guides/how-to-set-up-cursor-rules, https://www.datacamp.com/tutorial/cursor-rules

**Community ecosystem**: Large. GitHub repo `PatrickJS/awesome-cursorrules` curates community rules. Sites like `cursorrules.org` and `cursor.directory` provide generators and directories. The `.cursorrules` format became a de facto standard that other tools (Windsurf, Cline) adopted equivalents for.

### 1.2 MCP (Model Context Protocol) Support

**Status: CONFIRMED — Full native support**

- Enabled via Settings → Features → MCP Integration
- Config file: `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global)
- Supports transports: `stdio`, `HTTP`, `SSE`
- Supports: Tools, Prompts, Resources, Roots, Elicitation, Apps
- OAuth and API key authentication supported
- Community directories: `mcpcursor.org`, `cursor.directory`

**Evidence**: https://cursor.com/docs/mcp (official docs, rate-limited at fetch time but confirmed via search results)

### 1.3 Hooks (Pre/Post Tool Guards)

**Status: CONFIRMED — Full lifecycle hooks system (v1.7+, Oct 2025)**

Config file: `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (global). Both scopes are merged.

**Hook events confirmed**:
- `sessionStart` / `sessionEnd`
- `preToolUse` / `postToolUse` / `postToolUseFailure`
- `beforeShellExecution` / `afterShellExecution`
- `beforeReadFile` / `afterFileEdit`
- `beforeMCPExecution` / `afterMCPExecution`
- `beforeSubmitPrompt`
- `stop`

Scripts communicate via JSON over stdin/stdout. Pre-hooks can block actions.

**Evidence**: https://cursor.com/docs/hooks (official), https://www.infoq.com/news/2025/10/cursor-hooks/, https://blog.gitbutler.com/cursor-hooks-deep-dive

### 1.4 Custom Agents & Personas

**Status: CONFIRMED — Multiple mechanisms**

- **`AGENTS.md`**: Open project-level format (also used by Codex, Claude Code). Provides machine-readable behavioral instructions.
- **`.cursor/modes.json`**: Explicit custom agent definitions with identity, model selection, behavioral controls, access control, and guardrails.
- **Background Agents**: Autonomous agents that run without the IDE open (cloud-powered, cron-like scheduling). Can handle documentation generation, backlog items, PR drafting.
- **Multi-Agent Collaboration**: Cursor 2.0 supports parallel agents delegating to subagents.
- **Personas**: Configurable agent personas for different programming styles or team cultures.

**Evidence**: https://cursor.com/help/ai-features/agent, https://deepwiki.com/bmadcode/cursor-custom-agents-rules-generator/3-custom-agents-system, https://aiidelist.com/blog/cursor-2025-deep-dive

### 1.5 Extension/Plugin Model

**Status: CONFIRMED — VS Code extension compatible + MCP-based**

Cursor is a fork of VS Code, so it inherits the VS Code extension marketplace. Beyond that:
- MCP servers act as the primary plugin mechanism for AI capabilities
- Cursor Marketplace for discovering MCP servers
- Community-built MCP servers via GitHub, `mcpcursor.org`
- No proprietary plugin SDK — extensibility is through rules, hooks, MCP, and VS Code extensions

### 1.6 Can Users Build Execution/Automation Frameworks?

**CONFIRMED: Yes.** Through:
1. Hooks (`hooks.json`) — lifecycle automation, guardrails, CI integration
2. MCP servers — custom tools, APIs, databases, workflows
3. Background agents — scheduled autonomous tasks
4. Custom agent definitions (`.cursor/modes.json`) — specialized agent behaviors
5. Rules (`.cursor/rules/`) — persistent behavioral guidance

### 1.7 Ecosystem Maturity

**HIGH**. Cursor has the largest mindshare among AI coding editors. The `.cursorrules` format became a community standard. Multiple community directories exist. MCP adoption is broad. Background agents and hooks are relatively new (2025) but well-documented.

---

## 2. Windsurf / Codeium

### Source: docs.windsurf.com, official blog, community resources
### Status: CONFIRMED (official docs fetched successfully)

### 2.1 Cascade — The Agent

**Status: CONFIRMED**

Cascade is Windsurf's core AI agent — a multimodal, context-aware system that can read, refactor, and execute code across entire projects. It operates in the IDE and terminal.

- **Cascade** is not a separate product — it's the name for Windsurf's agentic AI mode
- Supports autonomous multi-step workflows (create file → generate test → run test → fix errors)
- Maintains deep context awareness across code edits, commands, errors, linter output

### 2.2 CLI Tool

**Status: CONFIRMED — `wsc` (Windsurf CLI)**

- `wsc` is the official command-line tool for interacting with Cascade from any terminal
- Allows sending prompts to Cascade, switching models, managing workspaces
- Configurable auto-execution levels: Disabled / Allowlist / Auto / Turbo
- Team/admin controls for command restrictions
- Maintains conversation logs for reproducibility

**Evidence**: https://github.com/staronelabs/windsurf-cli, https://docs.windsurf.com/windsurf/terminal

### 2.3 Custom Rules System

**Status: CONFIRMED — Multi-layered rules (Wave 8+, May 2025)**

| Mechanism | Location | Scope |
|-----------|----------|-------|
| `.windsurfrules` | Project root | Legacy, whole project |
| `.windsurf/rules/*.md` | Project directory | Fine-grained workspace rules |
| `global_rules.md` | Windsurf Settings | All workspaces |
| Subdirectory rules | Nested directories | Monorepo subsections |

**Activation modes** for rules:
- **Always On** — rule always applies
- **Manual** — activated via @mention in Cascade
- **Glob** — applies to matched file patterns
- **Model Decision** — AI chooses when to apply based on description

Rules are Markdown format, support XML-like tag grouping, max ~12k characters per file.

**Evidence**: https://docs.windsurf.com/windsurf/cascade/memories (fetched), https://mer.vin/2025/12/windsurf-memory-rules-deep-dive/, https://www.claudemdeditor.com/windsurfrules-guide

### 2.4 Memories

**Status: CONFIRMED — Workspace-local automatic context**

- Cascade automatically generates "memories" — snippets of useful context from sessions
- Users can explicitly create memories ("create a memory of...")
- Workspace-local, not version-controlled, not shared across machines
- Supplementary to Rules (rules are the durable, shareable mechanism)

**Evidence**: https://docs.windsurf.com/windsurf/cascade/memories (official docs)

### 2.5 MCP Support

**Status: CONFIRMED — Full native support**

- Config file: `~/.codeium/windsurf/mcp_config.json`
- MCP Marketplace within Cascade panel for discovery/installation
- Supports transports: `stdio`, `Streamable HTTP`, `SSE`
- OAuth support for all transport types
- Supports: Tools, Resources, Prompts
- Limit of 100 concurrent MCP tools per workspace
- Admin whitelisting with regex pattern matching for enterprise
- Environment variable interpolation in config (`${env:VAR_NAME}`)

**Evidence**: https://docs.windsurf.com/windsurf/cascade/mcp (official docs, fetched in full)

### 2.6 Hooks (Pre/Post Tool Guards)

**Status: CONFIRMED — Full lifecycle hooks ("Cascade Hooks")**

Config file: `.windsurf/hooks.json` (workspace), user-level, or system-level. All scopes merged.

**12 hook events confirmed** (from official docs fetched):
- `pre_read_code` / `post_read_code`
- `pre_write_code` / `post_write_code`
- `pre_run_command` / `post_run_command`
- `pre_mcp_tool_use` / `post_mcp_tool_use`
- `pre_user_prompt` / `post_cascade_response`
- `post_cascade_response_with_transcript`
- `post_agent_stop`

Pre-hooks can **block actions** (exit code 2). Scripts receive context as JSON via stdin.

Three configuration levels:
- **System**: `/Library/Application Support/Windsurf/hooks.json` (Mac) / `C:\ProgramData\Windsurf\hooks.json` (Win)
- **User**: `~/.codeium/windsurf/hooks.json`
- **Workspace**: `.windsurf/hooks.json`

Cloud dashboard configuration also available for enterprise.

**Evidence**: https://docs.windsurf.com/windsurf/cascade/hooks (official docs, fetched in full)

### 2.7 Custom Agents & Personas

**Status: CONFIRMED — Via Personas (Soul Spec)**

- Personas can be assigned to Cascade using "Soul Spec" — a specification standard
- Created via ClawSouls CLI or manually
- Exported into `.windsurfrules` for per-project personas or applied globally
- Controls communication style, behavioral traits, workflow preferences

**No equivalent to Cursor's `.cursor/modes.json` for defining distinct named agents with separate tool access.** Windsurf has one agent (Cascade) that can be customized via rules and personas, but not multiple independent agent definitions.

**Evidence**: https://blog.clawsouls.ai/en/guides/windsurf-soul/

### 2.8 Can Users Build Execution/Automation Frameworks?

**CONFIRMED: Yes.** Through:
1. Cascade Hooks (`.windsurf/hooks.json`) — full lifecycle automation and guardrails
2. MCP servers — custom tools, external integrations
3. Rules (`.windsurf/rules/`) — behavioral guidance
4. CLI (`wsc`) — scriptable terminal automation with configurable auto-execution
5. Memories — ephemeral workspace context

### 2.9 Ecosystem Maturity

**MEDIUM-HIGH**. Windsurf is newer than Cursor as a standalone IDE (launched late 2024), but Codeium has a large user base. MCP support is well-documented. Hooks system is comprehensive (comparable to Cursor). Community directories exist (`windsurf.run/mcp`). Rules ecosystem is growing but smaller than Cursor's.

---

## 3. Cline

### Source: GitHub (cline/cline), docs.cline.bot, VS Code Marketplace
### Status: CONFIRMED (official docs fetched, multiple sources)

### 3.1 Overview

**Status: CONFIRMED — Open-source autonomous coding agent**

- VS Code extension (marketplace ID: `saoudrizwan.claude-dev`, formerly "Claude Dev")
- Also available as **Cline CLI 2.0** — standalone terminal tool (`npm install -g cline`)
- Open-source: https://github.com/cline/cline
- Supports multiple LLM providers: Anthropic, OpenAI, Google Gemini, AWS Bedrock, Ollama, LM Studio, DeepSeek, and more
- Human-in-the-loop by default (explicit approval for file/terminal changes)

### 3.2 CLI Tool

**Status: CONFIRMED — Cline CLI 2.0**

Full standalone terminal tool, independent of VS Code:
- `cline` — interactive mode
- `cline "prompt"` — direct task
- `cline -y "prompt"` — YOLO/auto-approve mode (CI/CD)
- `cline --json "prompt"` — structured output for scripting
- `cline -p "prompt"` — plan mode
- `cline auth` — authentication wizard
- `cline config` — interactive configuration with tabs for Settings, Rules, Workflows, Hooks, Skills

**Evidence**: https://docs.cline.bot/cline-cli/cli-reference (official docs, fetched in full)

### 3.3 Custom Rules / Instructions

**Status: CONFIRMED — `.clinerules` file/directory system**

| Mechanism | Location | Scope |
|-----------|----------|-------|
| `.clinerules` (file) | Project root | Whole project |
| `.clinerules/` (directory) | Project root | Modular, per-concern rules |
| Custom Instructions | Extension settings UI | Global (legacy, being replaced) |

`.clinerules` features:
- Markdown format, modular splitting (e.g., `.clinerules/01-coding.md`, `.clinerules/02-documentation.md`)
- Version-controlled, project-specific
- AI-editable — Cline can read and update rules interactively
- Team-shareable via repo
- Specialized MCP development mode when present in MCP working directory

**Evidence**: https://cline.ghost.io/clinerules-version-controlled-shareable-and-ai-editable-instructions/, https://docs.cline.bot/mcp/mcp-server-development-protocol (fetched in full)

### 3.4 MCP Support

**Status: CONFIRMED — Deep, first-class MCP integration**

- MCP is Cline's **primary extensibility mechanism** — MCP servers are the plugin system
- Built-in MCP Marketplace for discovery and one-click installation
- Configuration stored in `cline_mcp_settings.json`
- Auto-approve configuration per tool (`autoApprove: []` array in settings)
- No artificial limit on concurrent MCP servers/tools
- Cline can assist in building, scaffolding, and testing MCP servers via natural language
- `.clinerules` includes a structured MCP Server Development Protocol
- Supports TypeScript/JavaScript and Python MCP SDKs

**Evidence**: https://docs.cline.bot/mcp/mcp-server-development-protocol (fetched), https://mcpmarket.com/server/marketplace, https://github.com/cline/mcp-marketplace

### 3.5 Workflows

**Status: CONFIRMED — v3.16+ (2025)**

- Workflows are version-controlled `.md` files in `.clinerules/workflows/`
- Appear as slash commands (e.g., `/run-tests`, `/generate-doc`)
- Can chain Cline's internal tools and external programs (e.g., `gh` CLI)
- Enable "one-shot automation" — hands-off execution for trusted, repetitive tasks
- Visible in `cline config` → Workflows tab

**Evidence**: https://cline.ghost.io/cline-v3-16-one-shot-automation-with-workflows-plus-ui-stability-gains/

### 3.6 Hooks

**Status: CONFIRMED**

- Cline supports hooks for custom logic at defined workflow points
- Defined in `.clinerules` directory
- Visible in `cline config` → Hooks tab
- Can be toggled globally or locally

**Evidence**: https://docs.cline.bot/cline-cli/cli-reference (mentions Hooks tab in `cline config`), search results from docs.cline.bot

### 3.7 Custom Modes

**Status: CONFIRMED — Plan/Act dual mode**

- **Plan Mode**: Analyzes codebase, proposes strategy, asks clarifying questions
- **Act Mode**: Executes tasks, writes code, runs commands
- Toggle via keyboard shortcuts (VS Code) or `-p`/`-a` flags (CLI)
- Plan mode prevents premature execution; Act mode does the work

### 3.8 Skills

**Status: CONFIRMED**

- Visible in `cline config` → Skills tab
- Skills are enabled capabilities that extend Cline's functionality

**Evidence**: https://docs.cline.bot/cline-cli/cli-reference (mentions Skills tab in `cline config`)

### 3.9 Custom Agents / Personas

**Status: UNCERTAIN — No dedicated mechanism found**

- Cline does not appear to have a named custom agent/persona system equivalent to Cursor's `.cursor/modes.json`
- Behavioral customization is achieved through `.clinerules` and custom instructions
- The "Memory Bank" pattern (`projectBrief.md`, `systemPatterns.md`) provides deep context
- No evidence of distinct agent definitions or persona configurations

### 3.10 Can Users Build Execution/Automation Frameworks?

**CONFIRMED: Yes.** Through:
1. MCP servers — primary plugin/tool mechanism (no limits)
2. Workflows (`.clinerules/workflows/`) — slash-command automation
3. Hooks — lifecycle automation
4. `.clinerules` — behavioral guidance and MCP dev protocol
5. CLI YOLO mode — CI/CD automation (`cline -y`)
6. `CLINE_COMMAND_PERMISSIONS` env var — security guardrails for shell commands

### 3.11 Ecosystem Maturity

**HIGH for MCP, MEDIUM for other mechanisms**. Cline has deep MCP integration and an active MCP Marketplace. The `.clinerules` system is well-documented. Workflows and hooks are newer (2025). Being open-source drives rapid community contribution. CLI 2.0 is a significant expansion. However, rules/hooks/workflows are less mature than Cursor's equivalents.

---

## 4. Comparative Matrix

### 4.1 Feature-by-Feature Comparison

| Feature | GitHub Copilot CLI | Cursor | Windsurf | Cline |
|---------|-------------------|--------|----------|-------|
| **Custom Instructions** | `.github/copilot-instructions.md` | `.cursor/rules/*.mdc` + User/Team rules + `AGENTS.md` | `.windsurf/rules/*.md` + `global_rules.md` + `.windsurfrules` | `.clinerules` file/dir + legacy UI instructions |
| **Instruction Scoping** | Repo-level | Glob-based, always-apply, manual, AI-selected | Glob-based, always-on, manual, model-decision | Per-file in directory, project-level |
| **Custom Agents/Personas** | `.github/agents/*.agent.md` | `.cursor/modes.json` + `AGENTS.md` + Background Agents | Personas via Soul Spec (single agent) | None (behavioral via rules only) |
| **Skills (Reusable Procedures)** | `.github/skills/*/SKILL.md` | No direct equivalent (rules partially overlap) | No direct equivalent | Skills tab in CLI config (details sparse) |
| **Hooks (Pre/Post Guards)** | `hooks.json` | `.cursor/hooks.json` (12+ events) | `.windsurf/hooks.json` (12 events) | Hooks (in .clinerules/config) |
| **MCP Server Support** | `mcp-config.json` | `.cursor/mcp.json` | `~/.codeium/windsurf/mcp_config.json` | `cline_mcp_settings.json` |
| **MCP Marketplace** | No (manual config) | mcpcursor.org, cursor.directory | Built-in MCP Marketplace | Built-in MCP Marketplace |
| **CLI Tool** | `ghcs` (GitHub Copilot CLI) | Cursor IDE (VS Code fork) | `wsc` (Windsurf CLI) | `cline` CLI 2.0 |
| **Workflows/Automation** | Skills + Agents | Background Agents + Hooks | Cascade Hooks + CLI auto-exec | Workflows (slash commands) + YOLO mode |
| **VS Code Extension Compat** | N/A (standalone CLI) | Full (VS Code fork) | VS Code-like + JetBrains | VS Code extension |
| **Open Source** | No | No | No | **Yes** (MIT) |
| **Multi-LLM Support** | GitHub models only | Multiple (Claude, GPT, Gemini) | Multiple (Claude, GPT, etc.) | **Most flexible** (15+ providers incl. local) |

### 4.2 MCP Support Depth

| Aspect | Copilot CLI | Cursor | Windsurf | Cline |
|--------|------------|--------|----------|-------|
| MCP Config | ✅ `mcp-config.json` | ✅ `.cursor/mcp.json` | ✅ `mcp_config.json` | ✅ `cline_mcp_settings.json` |
| Tools | ✅ | ✅ | ✅ | ✅ |
| Resources | ✅ | ✅ | ✅ | ✅ |
| Prompts | ✅ | ✅ | ✅ | ✅ |
| stdio transport | ✅ | ✅ | ✅ | ✅ |
| HTTP/SSE transport | ✅ | ✅ | ✅ | UNCERTAIN |
| OAuth | ✅ | ✅ | ✅ | UNCERTAIN |
| Marketplace | ❌ | Community dirs | ✅ Built-in | ✅ Built-in |
| Tool limit | None stated | None stated | 100 per workspace | None stated |
| Admin whitelisting | N/A | Team rules | ✅ Regex patterns | N/A |
| MCP dev assistance | N/A | N/A | N/A | ✅ AI-assisted server building |

### 4.3 Hooks Comparison

| Aspect | Copilot CLI | Cursor | Windsurf | Cline |
|--------|------------|--------|----------|-------|
| Config format | `hooks.json` | `.cursor/hooks.json` | `.windsurf/hooks.json` | `.clinerules` + config |
| Pre-tool blocking | ✅ | ✅ | ✅ (exit code 2) | UNCERTAIN |
| File read/write hooks | UNCERTAIN | ✅ | ✅ | UNCERTAIN |
| Shell execution hooks | ✅ | ✅ | ✅ | Via `CLINE_COMMAND_PERMISSIONS` |
| MCP tool hooks | UNCERTAIN | ✅ | ✅ | UNCERTAIN |
| Prompt hooks | UNCERTAIN | ✅ | ✅ | UNCERTAIN |
| Multi-scope merge | UNCERTAIN | ✅ (project + user) | ✅ (system + user + workspace) | UNCERTAIN |
| Transcript logging | N/A | N/A | ✅ (JSONL transcript) | N/A |

### 4.4 Mapping to Copilot CLI Primitives

| Copilot CLI Concept | Cursor Equivalent | Windsurf Equivalent | Cline Equivalent |
|---------------------|-------------------|---------------------|------------------|
| **Skills** (`.github/skills/`) | No direct equivalent. Closest: rules with glob patterns + `AGENTS.md` build instructions | No direct equivalent. Closest: rules + workflows via MCP | **Skills** tab in config (sparse docs). Closest functional: Workflows + `.clinerules` |
| **Custom Agents** (`.github/agents/`) | `.cursor/modes.json` + Background Agents ✅ | Personas via Soul Spec (single agent, not multi-agent) ⚠️ | Not supported ❌ |
| **Custom Instructions** (`.github/copilot-instructions.md`) | `.cursor/rules/*.mdc` + Team/User rules ✅ | `.windsurf/rules/` + `global_rules.md` ✅ | `.clinerules` file/dir ✅ |
| **Hooks** (`hooks.json`) | `.cursor/hooks.json` ✅ (very similar) | `.windsurf/hooks.json` ✅ (very similar, more events) | Hooks ✅ (less documented) |
| **MCP** (`mcp-config.json`) | `.cursor/mcp.json` ✅ | `mcp_config.json` ✅ | `cline_mcp_settings.json` ✅ |

---

## 5. Sources

### Cursor
- **Official MCP docs**: https://cursor.com/docs/mcp
- **Official Hooks docs**: https://cursor.com/docs/hooks
- **Official Agent mode**: https://cursor.com/help/ai-features/agent
- **Rules guide**: https://design.dev/guides/cursor-rules/
- **Rules tutorial**: https://www.datacamp.com/tutorial/cursor-rules
- **Rules setup**: https://www.agentrulegen.com/guides/how-to-set-up-cursor-rules
- **Cursor 049 changelog**: https://cursorpractice.com/en/cursor-changelog/cursor-049-updates
- **Cursor 2.0 deep dive**: https://aiidelist.com/blog/cursor-2025-deep-dive
- **Background agents**: https://decoupledlogic.com/2025/05/29/background-agents-in-cursor-cloud-powered-coding-at-scale/
- **Hooks deep dive**: https://blog.gitbutler.com/cursor-hooks-deep-dive
- **Hooks InfoQ**: https://www.infoq.com/news/2025/10/cursor-hooks/
- **Custom agents system**: https://deepwiki.com/bmadcode/cursor-custom-agents-rules-generator/3-custom-agents-system
- **AGENTS.md standard**: https://agents.md/
- **awesome-cursorrules**: https://github.com/PatrickJS/awesome-cursorrules
- **MCP community**: https://mcpcursor.org/

### Windsurf / Codeium
- **Official MCP docs**: https://docs.windsurf.com/windsurf/cascade/mcp (fetched in full)
- **Official Hooks docs**: https://docs.windsurf.com/windsurf/cascade/hooks (fetched in full)
- **Official Memories docs**: https://docs.windsurf.com/windsurf/cascade/memories
- **Terminal docs**: https://docs.windsurf.com/windsurf/terminal
- **Wave 8 changelog**: https://alternativeto.net/news/2025/5/windsurf-editor-wave-8-adds-memories-for-cascade-rules-support-and-mcp-integration/
- **Rules guide**: https://www.claudemdeditor.com/windsurfrules-guide
- **Memory & Rules deep dive**: https://mer.vin/2025/12/windsurf-memory-rules-deep-dive/
- **Personas (Soul Spec)**: https://blog.clawsouls.ai/en/guides/windsurf-soul/
- **CLI (wsc)**: https://github.com/staronelabs/windsurf-cli
- **SWE-1.5 & Hooks guide**: https://www.digitalapplied.com/blog/windsurf-swe-1-5-cascade-hooks-november-2025
- **MCP servers directory**: https://windsurf.run/mcp

### Cline
- **GitHub repo**: https://github.com/cline/cline
- **Official docs**: https://docs.cline.bot/home
- **CLI reference**: https://docs.cline.bot/cline-cli/cli-reference (fetched in full)
- **CLI installation**: https://docs.cline.bot/cline-cli/installation
- **MCP development protocol**: https://docs.cline.bot/mcp/mcp-server-development-protocol (fetched in full)
- **.clinerules blog**: https://cline.ghost.io/clinerules-version-controlled-shareable-and-ai-editable-instructions/
- **Workflows v3.16**: https://cline.ghost.io/cline-v3-16-one-shot-automation-with-workflows-plus-ui-stability-gains/
- **CLI 2.0 announcement**: https://cline.bot/blog/introducing-cline-cli-2-0
- **VS Code Marketplace**: https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev
- **MCP Marketplace**: https://mcpmarket.com/server/marketplace
- **Cline MCP Marketplace repo**: https://github.com/cline/mcp-marketplace
- **MCP servers guide**: https://cline.ghost.io/supercharge-your-cline-workflow-7-essential-mcp-servers/

---

## Dead Ends

- `https://docs.cursor.com/context/rules` — returned HTTP 429 (rate limited)
- `https://docs.cursor.com/context/model-context-protocol` — returned HTTP 429 (rate limited)
- `https://docs.windsurf.com/windsurf/cascade/rules` — returned HTTP 404 (not found at this path; rules are documented under memories-and-rules)
- Cursor proprietary plugin SDK — does not exist; extensibility is through open standards (MCP, VS Code extensions, rules, hooks)
- Windsurf distinct multi-agent system — does not exist; single Cascade agent with persona customization
- Cline named custom agents/personas — no evidence found of a dedicated mechanism

---

## Key Takeaways

1. **All four tools now share a common extensibility vocabulary**: custom rules/instructions, MCP servers, and hooks. This convergence happened rapidly in 2024–2025.

2. **Cursor has the broadest extensibility**: rules + hooks + MCP + custom agents + background agents + `AGENTS.md`. Its rules ecosystem is the largest community-driven one.

3. **Windsurf has the most thoroughly documented hooks**: 12 events with official docs covering system/user/workspace scoping, transcript logging, and enterprise cloud dashboard configuration. Its MCP admin controls (regex whitelisting) are uniquely enterprise-focused.

4. **Cline is the most open and flexible**: open-source, 15+ LLM providers, no MCP tool limits, and the only tool with AI-assisted MCP server development built in. Its CLI 2.0 is the most feature-rich terminal agent with YOLO mode for CI/CD.

5. **GitHub Copilot CLI's unique differentiator remains Skills**: The `.github/skills/` concept — reusable, named, discoverable procedures with YAML frontmatter — has no direct equivalent in any competitor. Cursor rules partially overlap but lack the procedure/workflow framing. Cline's Workflows come closest but are less structured. This is the strongest competitive moat for the Copilot CLI extensibility model.

6. **GitHub Copilot CLI's Custom Agents** (`.github/agents/*.agent.md`) are more structured than any competitor's agent definition system. Cursor's `.cursor/modes.json` is the closest but lacks the markdown-based, repo-committed, team-shareable aspect with embedded subagent instructions.
