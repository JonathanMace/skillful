# GitHub Copilot SDK — Deep Technical Summary

> **Research date:** July 2026 | **Sources:** github/copilot-sdk repo, GitHub Blog, InfoQ, Microsoft Tech Community, MachineLearningMastery, DevLeader.ca, web search synthesis

---

## 1. What It Is

The **GitHub Copilot SDK** (`github/copilot-sdk`) is a multi-language SDK released **January 22, 2026** (technical preview) that wraps the same agentic runtime powering GitHub Copilot CLI and exposes it as a programmable library. It communicates with the Copilot CLI process via **JSON-RPC** over stdio, managing the CLI's process lifecycle automatically.

**Architecture:**
```
Your Application
       ↓
  SDK Client  (TypeScript / Python / Go / .NET / Java)
       ↓ JSON-RPC (stdio)
  Copilot CLI (server mode)
       ↓
  LLM APIs (GitHub-managed or BYOK)
```

The SDK is **not** a direct LLM API wrapper. It embeds Copilot CLI's full **agent loop**: planner → tool invocation → file edits → command execution → streaming response — so you don't build orchestration from scratch.

**Status:** Technical Preview (v0.2.0 as of March 2026). Not yet production-ready per GitHub's own FAQ. MIT licensed.

---

## 2. Repository Structure

```
github/copilot-sdk/
├── nodejs/          # @github/copilot-sdk (npm)
│   ├── src/
│   │   ├── client.ts          (69KB — CopilotClient)
│   │   ├── session.ts         (40KB — Session management)
│   │   ├── types.ts           (44KB — All TypeScript types)
│   │   ├── extension.ts       (VS Code extension support)
│   │   ├── telemetry.ts
│   │   └── generated/         (Auto-generated RPC types from schema)
│   ├── examples/
│   └── samples/
├── python/          # github-copilot-sdk (PyPI)
│   ├── copilot/
│   │   ├── client.py          (91KB — CopilotClient)
│   │   ├── session.py         (51KB — Session)
│   │   ├── tools.py           (8KB — @define_tool decorator)
│   │   ├── generated/         (Auto-generated types)
│   │   ├── _jsonrpc.py
│   │   └── _telemetry.py
│   └── samples/
├── go/              # github.com/github/copilot-sdk/go
│   ├── client.go              (51KB)
│   ├── session.go             (28KB)
│   ├── types.go               (41KB)
│   ├── definetool.go          (4KB)
│   ├── permissions.go
│   ├── telemetry.go
│   ├── generated_session_events.go  (74KB)
│   ├── rpc/
│   ├── embeddedcli/
│   └── samples/
├── dotnet/          # GitHub.Copilot.SDK (NuGet)
│   ├── src/
│   ├── samples/
│   └── test/
├── java/            # → github/copilot-sdk-java (separate repo)
├── docs/
│   ├── getting-started.md
│   ├── auth/        (GitHub OAuth, BYOK, env vars)
│   ├── features/    (hooks, custom agents, MCP, skills)
│   ├── setup/       (architecture, deployment, scaling)
│   ├── hooks/
│   ├── integrations/
│   ├── observability/
│   └── troubleshooting/
├── test/            # Cross-SDK integration tests
├── scripts/
└── sdk-protocol-version.json
```

**Package coordinates:**
| Language | Package | Install |
|----------|---------|---------|
| Node.js/TS | `@github/copilot-sdk` | `npm install @github/copilot-sdk` |
| Python | `github-copilot-sdk` | `pip install github-copilot-sdk` |
| Go | `github.com/github/copilot-sdk/go` | `go get github.com/github/copilot-sdk/go` |
| .NET | `GitHub.Copilot.SDK` | `dotnet add package GitHub.Copilot.SDK` |
| Java | `com.github:copilot-sdk-java` | Maven/Gradle (separate repo) |

**Community SDKs:** Rust, Clojure, C++ (unofficial, not supported by GitHub).

---

## 3. Core API Surface

### 3.1 CopilotClient

The central class. Manages the CLI subprocess lifecycle.

#### TypeScript
```typescript
import { CopilotClient } from "@github/copilot-sdk";

// Option A: Auto-launch CLI subprocess (default)
const client = new CopilotClient();
// or with options:
const client = new CopilotClient({
  cliPath: "/usr/bin/copilot",   // explicit CLI binary path
  logLevel: "debug",
  telemetry: {
    otlpEndpoint: "http://localhost:4318",
    sourceName: "my-app",
  },
});

// Option B: Connect to external CLI server
const client = new CopilotClient({ cliUrl: "localhost:3000" });

await client.start();
// ... use sessions ...
await client.stop();
```

#### Python (v0.2.0 API)
```python
from copilot import CopilotClient, SubprocessConfig, ExternalServerConfig

# Subprocess mode
client = CopilotClient(SubprocessConfig(
    cli_path="/usr/bin/copilot",
    log_level="debug",
    telemetry={"otlp_endpoint": "http://localhost:4318", "source_name": "my-app"}
))

# External server mode
client = CopilotClient(ExternalServerConfig(url="localhost:3000"))

await client.start()
# ... use sessions ...
await client.stop()
```

#### C# (.NET)
```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
// or with options:
await using var client = new CopilotClient(new CopilotClientOptions {
    Telemetry = new TelemetryConfig {
        OtlpEndpoint = "http://localhost:4318",
        SourceName = "my-app",
    },
});
await client.StartAsync();
```

#### Go
```go
import copilot "github.com/github/copilot-sdk/go"

client, err := copilot.NewClient(&copilot.ClientOptions{
    Telemetry: &copilot.TelemetryConfig{
        OTLPEndpoint: "http://localhost:4318",
        SourceName:   "my-app",
    },
})
err = client.Start(ctx)
defer client.Stop()
```

**Key client methods:**
- `start()` / `stop()` — Lifecycle management
- `createSession(config)` — Create new agentic session
- `resumeSession(id, config)` — Resume existing session
- `listModels()` — List available models (supports BYOK override via `onListModels`)
- `getLastSessionId()` — Retrieve last session ID (all SDKs)
- `on(event, handler)` — Register client-level event handlers

### 3.2 Session

A session is a stateful, multi-turn agentic conversation. It wraps the full Copilot agent loop.

#### Creating Sessions

```typescript
// TypeScript
const session = await client.createSession({
  model: "gpt-5",
  streaming: true,
  tools: [myCustomTool],
  onPermissionRequest: approveAll,      // REQUIRED — handles tool permission requests
  systemMessage: "You are a helpful assistant.",
  customAgents: [
    { name: "researcher", prompt: "You are a research assistant." },
    { name: "editor", prompt: "You are a code editor." },
  ],
  agent: "researcher",                  // Pre-select which agent is active
  onEvent: (event) => { /* ... */ },    // Catch-all event handler (registered before RPC)
});
```

```python
# Python (v0.2.0 keyword args)
session = await client.create_session(
    on_permission_request=PermissionHandler.approve_all,
    model="claude-sonnet-4.5",
    streaming=True,
    tools=[get_library_info],
    skill_directories=["./.copilot_skills/pr-analyzer/SKILL.md"],
    system_message="You are a helpful assistant.",
)
```

```csharp
// C#
await using var session = await client.CreateSessionAsync(new SessionConfig {
    Model = "gpt-5",
    OnPermissionRequest = PermissionHandler.ApproveAll,
    SystemMessage = "You are a helpful assistant.",
});
```

#### Sending Messages

```typescript
// TypeScript — fire-and-forget (streaming)
await session.send({ prompt: "Hello, world!" });

// TypeScript — wait for completion
await session.sendAndWait({ prompt: "What is 2+2?" });

// With attachments (blobs — images, binary data)
await session.send({
  prompt: "What's in this image?",
  attachments: [{ type: "blob", data: base64Str, mimeType: "image/png" }],
});
```

```python
# Python (v0.2.0 — positional prompt)
await session.send("Hello!")
await session.send_and_wait("What is 2+2?")
```

```csharp
// C#
await session.SendAsync(new MessageOptions { Prompt = "Hello, world!" });
```

#### Mid-Session Model Switching

```typescript
await session.setModel("gpt-4.1");
await session.setModel("claude-sonnet-4.5", { reasoningEffort: "high" });
```
```python
await session.set_model("gpt-4.1")
```
```csharp
await session.SetModelAsync("gpt-4.1");
```
```go
err := session.SetModel(ctx, "gpt-4.1")
```

#### Session Event Handling

Events are streamed in real-time. Key event types include:
- `assistant.message` / `assistant.message.delta` — Model output (streaming tokens)
- `tool.execution_start` / `tool.execution_complete` — Tool invocations
- `permission.request` / `permission.completed` — Permission prompts
- `session.idle` — Agent loop finished
- `session.start` — Session initialized
- `system.notification` — System-level notifications

```typescript
session.on("assistant.message.delta", (event) => {
  process.stdout.write(event.data.deltaContent);
});
session.on("tool.execution_start", (event) => {
  console.log(`Tool called: ${event.data.toolName}`);
});
session.on("session.idle", () => {
  console.log("Agent finished.");
});
```

```python
from copilot.generated.session_events import SessionEventType

def handle_event(event):
    if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        sys.stdout.write(event.data.delta_content)
    elif event.type == SessionEventType.TOOL_EXECUTION_START:
        print(f"Tool: {event.data.tool_name}")

session.on(handle_event)
```

#### Resuming Sessions

```typescript
const session2 = await client.resumeSession(session1.id, {
  tools: [additionalTool],
  onPermissionRequest: approveAll,
});
```

#### Low-Level RPC Methods (v0.2.0)

Direct control over CLI subsystems:
```typescript
// Skills management
await session.rpc.skills.list();
await session.rpc.skills.enable("my-skill");
await session.rpc.skills.disable("my-skill");
await session.rpc.skills.reload();

// MCP server management
await session.rpc.mcp.list();
await session.rpc.mcp.enable("my-mcp-server");
await session.rpc.mcp.disable("my-mcp-server");
await session.rpc.mcp.reload();

// Extensions management
await session.rpc.extensions.list();
await session.rpc.extensions.enable("ext-name");

// Agent selection
await session.rpc.agent.select("researcher");

// UI / user input
await session.rpc.ui.elicitation({ ... });  // Structured user input

// Shell execution
await session.rpc.shell.exec("npm test");
await session.rpc.shell.kill(pid);

// Logging
await session.log("message", "info", /* ephemeral */ true);

// Plugins
await session.rpc.plugins.list();
```

### 3.3 Tool Registration

#### TypeScript — `defineTool()`
```typescript
import { defineTool } from "@github/copilot-sdk";

const searchTool = defineTool("search", {
  description: "Search the web",
  parameters: {
    type: "object",
    properties: { query: { type: "string" } },
    required: ["query"],
  },
  handler: async (params) => {
    return `Results for: ${params.query}`;
  },
  skipPermission: true,            // Skip confirmation for low-risk tools
  overridesBuiltInTool: false,     // Set true to override built-in tools
});

// Register in session
const session = await client.createSession({
  tools: [searchTool],
  onPermissionRequest: approveAll,
});
```

#### Python — `@define_tool` decorator with Pydantic
```python
from copilot.tools import define_tool
from pydantic import BaseModel, Field

class SearchParams(BaseModel):
    query: str = Field(description="Search query string")

@define_tool(description="Search the web for information")
async def search(params: SearchParams) -> dict:
    return {"results": f"Results for: {params.query}"}

# Register in session
session = await client.create_session(
    tools=[search],
    on_permission_request=PermissionHandler.approve_all,
)
```

#### Go — `DefineTool()`
```go
import copilot "github.com/github/copilot-sdk/go"

searchTool := copilot.DefineTool("search", copilot.ToolConfig{
    Description: "Search the web",
    Handler: func(params map[string]any) (string, error) {
        return fmt.Sprintf("Results for: %s", params["query"]), nil
    },
})
```

#### C# — `AIFunctionFactory` (Microsoft.Extensions.AI)
```csharp
using Microsoft.Extensions.AI;

var searchTool = AIFunctionFactory.Create(
    ([Description("Search query")] string query) => $"Results for: {query}",
    "search",
    "Search the web"
);
```

**Overriding built-in tools:**
```typescript
defineTool("grep", {
  overridesBuiltInTool: true,
  handler: async (params) => `CUSTOM_GREP: ${params.query}`,
});
```

### 3.4 System Prompt Customization (v0.2.0)

Fine-grained control over 10 prompt sections:
`identity`, `tone`, `tool_efficiency`, `environment_context`, `code_change_rules`, `guidelines`, `safety`, `tool_instructions`, `custom_instructions`, `last_instructions`

```typescript
const session = await client.createSession({
  onPermissionRequest: approveAll,
  systemMessage: {
    mode: "customize",
    sections: {
      identity: {
        action: (current) => current.replace("GitHub Copilot", "Acme Assistant"),
      },
      tone: { action: "replace", content: "Be concise and professional." },
      code_change_rules: { action: "remove" },
      guidelines: { action: "append", content: "\nAlways use TypeScript." },
    },
  },
});
```

Actions per section: `replace`, `remove`, `append`, `prepend`, or `transform` callback.

### 3.5 Multi-Client Architecture (Protocol v3)

Multiple clients can attach to the same session, each contributing different tools:
```typescript
const session1 = await client1.createSession({
  tools: [defineTool("search", { handler: doSearch })],
  onPermissionRequest: approveAll,
});
const session2 = await client2.resumeSession(session1.id, {
  tools: [defineTool("analyze", { handler: doAnalyze })],
  onPermissionRequest: approveAll,
});
// The agent can use tools from BOTH clients
```

### 3.6 Permission Handling

Required for all sessions. The handler receives tool execution requests and must approve/deny:

```typescript
// Auto-approve everything
import { PermissionHandler } from "@github/copilot-sdk";
const session = await client.createSession({
  onPermissionRequest: PermissionHandler.approveAll,
});

// Custom logic
const session = await client.createSession({
  onPermissionRequest: (request) => {
    if (request.toolName === "shell_exec") return { decision: "deny" };
    return { decision: "allow" };
  },
});
```

Permission outcomes: `approved`, `denied-interactively-by-user`, `denied-by-rules`, `denied-could-not-request-from-user`, `no-result` (new — for passive observers).

---

## 4. Authentication

Four methods supported:

| Method | How | BYOK? |
|--------|-----|-------|
| **GitHub signed-in user** | Stored OAuth from `copilot` CLI login | No |
| **OAuth GitHub App** | Pass user tokens from your OAuth app | No |
| **Environment variables** | `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN` | No |
| **BYOK (Bring Your Own Key)** | Your own OpenAI / Azure AI Foundry / Anthropic keys | Yes |

BYOK supports key-based auth only (no Entra ID / managed identities).

---

## 5. Billing

Same billing model as Copilot CLI: each prompt counts toward your **premium request quota**. Copilot has a free tier with limited usage. See [GitHub Copilot pricing](https://github.com/features/copilot#pricing).

---

## 6. Default Tool Capabilities

By default, the SDK operates in `--allow-all` mode, enabling all first-party CLI tools:
- **File system:** read, write, edit, create, delete files
- **Git operations:** status, diff, commit, branch, etc.
- **Shell execution:** run arbitrary commands
- **Web requests:** fetch URLs
- **Grep/glob:** code search
- **Code intelligence:** language-aware operations

All of these can be customized (enabled/disabled per session).

---

## 7. Observability & Telemetry

**OpenTelemetry support** across all SDKs (v0.2.0):
- OTLP exporter configuration
- W3C trace context propagation on session.create, session.resume, session.send
- Tool execution linked to originating trace
- Source name customization

```typescript
const client = new CopilotClient({
  telemetry: {
    otlpEndpoint: "http://localhost:4318",
    sourceName: "my-app",
  },
});
```

---

## 8. Real-World Case Study: agent-framework-update-everyday

[kinfey/agent-framework-update-everyday](https://github.com/kinfey/agent-framework-update-everyday) — automated daily blog generator using the SDK.

**Architecture:**
1. GitHub Actions cron (Mon–Fri UTC 00:00)
2. Installs Copilot CLI + Python SDK
3. Runs `pr_trigger_v2.py` with `COPILOT_GITHUB_TOKEN`
4. Uses custom Copilot Skill (`.copilot_skills/pr-analyzer/SKILL.md`) for PR analysis
5. Generates structured blog posts to `blog/` directory
6. Auto-commits and pushes

**Key patterns:**
- Model selection: Claude Sonnet for execution, GPT-5 for exploration
- Skill-based prompting for domain focus
- Streaming mode for real-time output
- CI/CD integration with retry strategies and rate limit handling

---

## 9. What You Can Build

Demonstrated use cases from GitHub engineers and community:
- **YouTube chapter generators** — analyze video transcripts, produce chapters
- **Custom GUIs for agents** — wrap SDK in Electron/web UIs
- **Speech-to-command workflows** — voice → agent → desktop automation
- **AI games** — competitive AI players
- **Content summarizers** — analyze repos/PRs/docs and produce summaries
- **Automated code reviewers** — PR annotation bots
- **ASP.NET Core AI assistant APIs** — expose Copilot as an HTTP endpoint with SSE streaming
- **Interactive coding agents** — REPL-style file read/modify/test loops
- **Data pipeline automation** — clean, transform, analyze datasets autonomously
- **CI/CD automation agents** — triage issues, generate changelogs, cross-repo checks
- **Enterprise internal agents** — domain-specific tools with BYOK

---

## 10. Limitations & Constraints

### Hard Limitations
- **Requires Copilot CLI installed separately** — SDK is a thin RPC wrapper, not standalone
- **Technical Preview** — breaking changes expected (Python API already overhauled in v0.2.0)
- **CLI process dependency** — each client spawns or connects to a CLI process; not serverless
- **No Entra ID / managed identity for BYOK** — key-based auth only
- **Billing tied to premium requests** — each prompt costs against your Copilot quota
- **Not production-ready** per GitHub's own FAQ

### Practical Constraints
- **Latency** — JSON-RPC over stdio to a subprocess adds overhead vs. direct API calls
- **State is CLI-bound** — session state lives in the CLI process; if it crashes, state is lost
- **Model availability** — constrained to models available via Copilot CLI (though BYOK expands this)
- **Platform dependency** — need Node.js installed for CLI regardless of which SDK language you use
- **`autoRestart` removed** — was never fully implemented; no built-in crash recovery
- **Rate limits** — standard GitHub API rate limits apply
- **Concurrency** — multi-client sessions possible (v3 protocol) but still experimental

### API Churn
The Python SDK had a major breaking change in v0.2.0 (TypedDict → keyword args). Go changed context semantics for `Client.Start()`. Expect more changes before GA.

---

## 11. Version History (Key Milestones)

| Version | Date | Highlights |
|---------|------|-----------|
| v0.1.30 | 2026-03-03 | Override built-in tools, `setModel()` convenience method |
| v0.1.31 | 2026-03-07 | Multi-client tool/permission broadcasts (protocol v3) |
| v0.1.32 | 2026-03-07 | Backward compat with v2 CLI servers |
| **v0.2.0** | **2026-03-20** | Fine-grained system prompt customization, OpenTelemetry, blob attachments, agent pre-selection, `skipPermission`, Python API overhaul, new RPC methods |

---

## 12. Comparison with Other Frameworks

| Feature | Copilot SDK | Semantic Kernel | LangChain | OpenAI Agents SDK |
|---------|------------|-----------------|-----------|-------------------|
| **Runtime** | Copilot CLI (battle-tested) | Custom orchestration | Custom orchestration | OpenAI API direct |
| **Built-in tools** | Full FS/Git/Shell/Web | Plugin-based | Tool ecosystem | Code interpreter, web |
| **Model support** | All Copilot models + BYOK | Azure OpenAI focused | Broad | OpenAI only |
| **Session management** | Built-in (multi-turn, persistent memory) | Manual | Manual | Threads API |
| **MCP support** | Native | Community plugins | Community | No |
| **Languages** | TS, Python, Go, .NET, Java | C#, Python, Java | Python, JS | Python |
| **Auth** | GitHub OAuth + BYOK | Azure AD | N/A | API keys |
| **Unique strength** | Production agent loop, no orchestration needed | Enterprise Azure integration | Ecosystem breadth | Simplicity |
| **Unique weakness** | CLI subprocess dependency | Azure lock-in perception | Complexity | OpenAI-only |

---

## 13. Sources

1. **github/copilot-sdk** repository — README, CHANGELOG, source code structure
   https://github.com/github/copilot-sdk
2. **GitHub Blog** — "Build an agent into any app with the GitHub Copilot SDK" (Jan 22, 2026)
   https://github.blog/news-insights/company-news/build-an-agent-into-any-app-with-the-github-copilot-sdk/
3. **InfoQ** — "GitHub Copilot SDK" (Feb 2026)
   https://www.infoq.com/news/2026/02/github-copilot-sdk/
4. **Microsoft Tech Community** — "Building Agents with GitHub Copilot SDK: A Practical Guide"
   https://techcommunity.microsoft.com/blog/azuredevcommunityblog/building-agents-with-github-copilot-sdk-a-practical-guide-to-automated-tech-upda/4488948
5. **MachineLearningMastery** — "Agentify Your App with GitHub Copilot's Agentic Coding SDK"
   https://machinelearningmastery.com/agentify-your-app-with-github-copilots-agentic-coding-sdk/
6. **DevLeader.ca** — GitHub Copilot SDK for .NET series
   https://www.devleader.ca/2026/02/26/github-copilot-sdk-for-net-complete-developer-guide
7. **kinfey/agent-framework-update-everyday** — Real-world SDK integration
   https://github.com/kinfey/agent-framework-update-everyday
8. **Microsoft DevBlogs (Semantic Kernel)** — Copilot SDK + Agent Framework integration
   https://devblogs.microsoft.com/semantic-kernel/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/
