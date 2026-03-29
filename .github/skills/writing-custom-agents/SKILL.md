---
name: writing-custom-agents
description: >-
  Agent profiles let you define specialized Copilot personas with constrained
  tools, custom models, and focused prompts.  Use this skill to author a
  custom agent, create an agent profile, set up .github/agents, or configure
  specialized Copilot personas.
license: MIT
---

# Authoring Custom Agents for GitHub Copilot CLI

Custom agents are specialized Copilot personas with tailored expertise, tool access, and behavioral instructions. They are defined in `.agent.md` files and loaded as available agent profiles that Copilot can delegate work to via subagents.

## Procedure: Authoring a Custom Agent

1. **Decide whether a custom agent is the right mechanism** — for simple coding conventions, author custom instructions instead. For task-specific procedures without a persona, author a skill instead (see the `writing-skills` and `writing-custom-instructions` skills).
2. **Inspect existing agents** — check `.github/agents/` and `~/.copilot/agents/` for existing agents to avoid naming conflicts and match conventions.
3. **Define the agent's specialty** — articulate who this agent is, what it does, and what tasks should trigger delegation to it. This becomes the `description` field.
4. **Choose the tool set** — decide which tools the agent needs. Constrain tools to the minimum required for the agent's role.
5. **Author the `.agent.md` file** — write YAML frontmatter, then a Markdown prompt body defining the agent's behavior, responsibilities, and constraints.
6. **Review as if new to the repo** — re-read the agent profile from the perspective of someone unfamiliar with the project. The description should clearly convey when Copilot should delegate to this agent, and the prompt body should define clear boundaries.
7. **Test the agent** — invoke it with `/agent`, select it, and verify it behaves as expected. Confirm auto-delegation triggers correctly (or does not, if `disable-model-invocation: true`).

## When to Author a Custom Agent (vs Other Customization)

- **Author a custom agent** when you need a specialist persona, constrained tools, or automatic delegation for a domain.
- **Author custom instructions** for broad, always-on conventions that apply to every task.
- **Author a skill** for task-specific procedures that don't require a separate persona or tool constraints.

## File Format

Custom agents are Markdown files with YAML frontmatter, using the `.agent.md` extension.

**Filename:** `<agent-name>.agent.md`
- Allowed characters: `.`, `-`, `_`, `a-z`, `A-Z`, `0-9`
- The filename (minus `.agent.md`) is used as the default agent name if `name` is not set in frontmatter

## Placement

| Scope | Location |
|-------|----------|
| **Repository-level** | `.github/agents/` in the repo |
| **User-level** | `~/.copilot/agents/` |
| **Organization/Enterprise** | `/agents/` in the `.github-private` repo |

**Precedence on naming conflicts:** system-level > repository-level > organization-level.

## YAML Frontmatter Properties

```yaml
---
name: my-agent-name
description: What this agent does and its area of expertise
tools: ["read", "search", "edit"]
model: claude-sonnet-4.5
disable-model-invocation: false
user-invocable: true
---
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | No | Display name. Defaults to filename without extension. |
| `description` | string | **Yes** | Purpose and capabilities. Copilot uses this to decide when to auto-delegate. |
| `tools` | list/string | No | Tools the agent can use. Omit for all tools. `[]` for no tools. |
| `model` | string | No | AI model to use. Inherits default if unset. |
| `disable-model-invocation` | boolean | No | When `true`, agent must be manually selected — Copilot won't auto-delegate to it. Default: `false`. |
| `user-invocable` | boolean | No | When `false`, agent can only be invoked programmatically. Default: `true`. |
| `mcp-servers` | object | No | MCP servers available only to this agent. |
| `metadata` | object | No | Arbitrary key-value pairs for documentation/tracking. |
| `target` | string | No | Restrict to `vscode` or `github-copilot` environment. Omit for both. |

## Tool Configuration

### Enable All Tools (default)

```yaml
# Omit the tools property entirely, or:
tools: ["*"]
```

### Enable Specific Tools

```yaml
tools: ["read", "search", "edit", "execute"]
```

### Tool Aliases

| Alias | Covers | Purpose |
|-------|--------|---------|
| `execute` | `shell`, `Bash`, `powershell` | Run shell commands |
| `read` | `Read`, `NotebookRead` | Read file contents |
| `edit` | `Edit`, `MultiEdit`, `Write`, `NotebookEdit` | Modify files |
| `search` | `Grep`, `Glob` | Search files and content |
| `agent` | `custom-agent`, `Task` | Invoke other agents |
| `web` | `WebSearch`, `WebFetch` | Web search and fetch |

### MCP Server Tools

Reference tools from specific MCP servers using `server-name/tool-name`:

```yaml
tools: ["read", "search", "github/list_pull_requests", "custom-mcp/*"]
```

## Prompt Body

Below the frontmatter, write the agent's behavioral instructions in Markdown. This defines the agent's expertise, workflow, and constraints.

**Maximum length:** 30,000 characters.

### Structure

1. **Role statement** — who the agent is and what it specializes in
2. **Responsibilities** — specific tasks and behaviors
3. **Constraints** — what the agent should NOT do
4. **Workflow** — step-by-step approach for common tasks

### Example: Testing Specialist

```markdown
---
name: test-specialist
description: Focuses on test coverage, quality, and testing best practices without modifying production code
---

You are a testing specialist focused on improving code quality through comprehensive testing. Your responsibilities:

- Analyze existing tests and identify coverage gaps
- Write unit tests, integration tests, and end-to-end tests following best practices
- Review test quality and suggest improvements for maintainability
- Ensure tests are isolated, deterministic, and well-documented
- Focus only on test files and avoid modifying production code unless specifically requested

Always include clear test descriptions and use appropriate testing patterns for the language and framework.
```

### Example: Implementation Planner (Constrained Tools)

```markdown
---
name: implementation-planner
description: Creates detailed implementation plans and technical specifications in markdown format
tools: ["read", "search", "edit"]
---

You are a technical planning specialist. Your responsibilities:

- Analyze requirements and break them into actionable tasks
- Create detailed technical specifications and architecture docs
- Generate implementation plans with clear steps and dependencies
- Document API designs, data models, and system interactions

Focus on creating thorough documentation rather than implementing code.
Always structure plans with clear headings, task breakdowns, and acceptance criteria.
```

### Example: Agent with MCP Server

```markdown
---
name: db-assistant
description: Helps with database queries, schema design, and data management
tools: ["read", "search", "edit", "execute", "db-mcp/query", "db-mcp/schema"]
mcp-servers:
  db-mcp:
    type: local
    command: db-mcp-server
    args: ["--connection-string", "$DB_CONNECTION"]
    tools: ["*"]
    env:
      DB_CONNECTION: ${{ secrets.DB_CONNECTION_STRING }}
---

You are a database specialist. Help with query writing, schema design,
and data management tasks.
```

## How Custom Agents Are Invoked (Context for Authors)

Understanding how agents are invoked helps you author better descriptions and tool constraints.

### Select Interactively

```
/agent
```

Then use arrow keys to select from the list.

### Reference in a Prompt

```
Use the test-specialist agent to review test coverage for the auth module.
```

Copilot infers the correct agent from the prompt.

### Command-Line Argument

```bash
copilot --agent=test-specialist --prompt "Review test coverage"
```

### Automatic Delegation

When `disable-model-invocation` is `false` (the default), Copilot may automatically delegate tasks to the agent when the task matches the agent's `description`. This is why the description field is critical — it controls when auto-delegation triggers.

## Best Practices for Authoring Agents

1. **Author a clear description** — this is how Copilot decides when to delegate. Include the domain and trigger keywords.
2. **Constrain tools appropriately** — a read-only auditing agent should not have `edit` or `execute` tools.
3. **Define clear boundaries** — state what the agent should and should NOT do.
4. **Keep the prompt focused** — a 30,000 character limit is generous, but concise instructions outperform verbose ones.
5. **Use `disable-model-invocation: true`** for agents that should only be invoked explicitly (e.g., destructive operations).
6. **Test the agent** — invoke it with `/agent` and verify it behaves as expected before sharing.
7. **Version with your code** — agent profiles in `.github/agents/` are version-controlled and can be branched.
