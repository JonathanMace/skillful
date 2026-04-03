---
name: writing-plugins
description: >-
  Plugins package reusable agents, skills, hooks, and integrations into an
  installable Copilot CLI extension that can be shared across projects.  Use
  this skill to create a plugin, author `plugin.json`, lay out plugin
  components, test local install and update workflows, and prepare the plugin
  for distribution.
license: MIT
---

# Authoring Plugins for GitHub Copilot CLI

Plugins are the distribution mechanism for Copilot CLI customizations. They bundle one or more reusable components — such as skills, agents, hooks, MCP servers, and LSP servers — into a single installable package that users can add with `copilot plugin install`.

A well-authored plugin should be easy to inspect, easy to install, and easy to test locally while it is being developed.

## Procedure: Authoring a Plugin

1. **Inspect the current plugin state first** — read `plugin.json`, `README.md`, and any existing `skills/`, `agents/`, `hooks.json`, `.mcp.json`, `lsp.json`, or `.github/plugin/` files before changing anything. If the repository also has project-level customizations in `.github/`, decide which artifacts belong in the distributable plugin and which should remain repository-local.
2. **Decide whether a plugin is the right mechanism** — author a plugin when the capability should be reusable across repositories or shared with a team via `/plugin install`. For repo-specific guidance, prefer project-level files such as `.github/skills/`, `.github/agents/`, or `.github/copilot-instructions.md`. For the component itself, follow the owning skill: `writing-skills`, `writing-custom-agents`, or `writing-hooks`.
3. **Define the plugin boundary and install shape** — decide what the plugin will contain, whether the plugin root is the repository root or a subdirectory, and how users will install it (local path, `OWNER/REPO`, `OWNER/REPO:PATH`, Git URL, or marketplace entry). This scope drives the manifest, directory layout, and documentation.
4. **Author `plugin.json` at the plugin root** — every plugin requires a manifest named exactly `plugin.json`. Start with `name`, then add the metadata and component paths needed for the package you are building.
5. **Add the plugin components** — create only the directories and files the plugin actually needs. Use `skills/<name>/SKILL.md` for skills, `agents/<name>.agent.md` for custom agents, `hooks.json` for hooks, `.mcp.json` or `lsp.json` for integrations, and `commands/` only if you are intentionally packaging command directories and have checked the current CLI reference for their format. Keep each component self-contained and cross-reference the skill or doc that owns its deeper rules instead of duplicating them in the plugin skill.
6. **Document install and verification paths** — update `README.md` or equivalent docs so users can install the plugin, list it, and verify that its skills or agents loaded successfully. If the plugin lives in a subdirectory, document the `OWNER/REPO:PATH` install form explicitly.
7. **Test with a local install** — install the plugin from a local path, verify it appears in `copilot plugin list`, then confirm each packaged component is actually available (for example, `/skills list` for skills or `/agents list` for agents).
8. **Reinstall after every local change** — local plugin installs are cached. If you edit the plugin after installing it, run `copilot plugin install <path>` again so the CLI refreshes the cached copy before re-testing.
9. **Prepare distribution only after the local workflow works** — once the plugin behaves correctly from a local install, publish or reference it from a repository or marketplace as appropriate. If you plan to distribute through a marketplace, treat that as a separate follow-on artifact: read the marketplace docs first, then author `.github/plugin/marketplace.json` with the marketplace metadata and plugin entries it should expose.

## When to Author a Plugin (vs Other Customization)

- **Author a plugin** when the customizations should be installable across many repositories or shared as one package.
- **Author project-level skills, agents, hooks, or instructions** when the customization is specific to one repository and should live in `.github/`.
- **Author a single skill or agent first** when you are still shaping one component and do not yet need a distributable package. Package it as a plugin once the component becomes reusable.

Plugins are the right abstraction for distribution. The underlying authoring rules for each component still belong to the component itself.

## Plugin Structure

At minimum, a plugin directory needs a `plugin.json` file at its root. Everything else is optional.

```
my-plugin/
├── plugin.json
├── agents/
│   └── helper.agent.md
├── commands/
│   └── deploy/
├── skills/
│   └── deploy/
│       └── SKILL.md
├── hooks.json
├── .mcp.json
└── lsp.json
```

### Placement Guidance

| Situation | Recommended placement |
|-----------|------------------------|
| Repository is itself the plugin | Put `plugin.json` at the repo root and package `skills/`, `agents/`, and other plugin assets there |
| Plugin lives inside a larger repository | Put the plugin in a subdirectory with its own `plugin.json` and document installs as `OWNER/REPO:PATH/TO/PLUGIN` |
| Capability is repo-only and not meant for installation elsewhere | Keep it in `.github/` instead of packaging it as a plugin |

## `plugin.json` Essentials

The manifest can be minimal, but it should be explicit enough that a future maintainer can understand what the plugin ships.

```json
{
  "name": "my-dev-tools",
  "description": "Reusable Copilot CLI helpers for frontend teams",
  "version": "1.0.0",
  "author": {
    "name": "Jane Doe"
  },
  "repository": "https://github.com/example/my-dev-tools",
  "license": "MIT",
  "skills": "skills/",
  "agents": "agents/",
  "hooks": "hooks.json",
  "mcpServers": ".mcp.json"
}
```

### Core manifest fields

| Field | Required | Notes |
|-------|----------|-------|
| `name` | **Yes** | Kebab-case plugin name, max 64 chars |
| `description` | No | Brief summary of what the plugin adds |
| `version` | No | Semantic version such as `1.0.0` |
| `author` | No | `name` is required inside the object if `author` is present |
| `license` | No | SPDX-style identifier such as `MIT` |
| `repository` / `homepage` | No | Useful for published plugins |
| `skills`, `agents` | No | Path or array of paths; CLI defaults to conventional locations if omitted |
| `commands` | No | Path or array of paths to command directories; only include it when the plugin intentionally packages commands, and confirm the directory format in the current CLI reference |
| `hooks`, `mcpServers`, `lspServers` | No | Path to config file or inline object |

Prefer explicit component-path fields when the layout is not obvious, when the plugin has more than one directory of a given type, or when future maintainers may otherwise assume the wrong default.

## Install and Testing Workflow

Use the actual CLI workflow while authoring:

```sh
copilot plugin install ./my-plugin
copilot plugin list
```

Then verify the packaged components:

```text
/skills list
/agents list
```

Useful install forms:

| Install source | Example |
|----------------|---------|
| Local directory | `copilot plugin install ./my-plugin` |
| Repository root | `copilot plugin install OWNER/REPO` |
| Repository subdirectory | `copilot plugin install OWNER/REPO:plugins/my-plugin` |
| Git URL | `copilot plugin install https://github.com/o/r.git` |

If you change a locally installed plugin, reinstall it before testing again:

```sh
copilot plugin install ./my-plugin
```

To remove the local install after testing:

```sh
copilot plugin uninstall my-dev-tools
```

Use the plugin `name` from `plugin.json` when uninstalling or updating — not the directory path.

### Marketplace packaging

Marketplace configuration is separate from the plugin itself. If you are curating a marketplace rather than only publishing a single plugin, author `.github/plugin/marketplace.json` and include the marketplace `name`, `owner`, and the `plugins` entries it exposes. Treat this as an advanced distribution step after the plugin already works from direct installs.

## Packaging Constraints and Precedence

- Skills and agents from plugins use **first-found-wins** precedence. A project-level or personal skill with the same name will shadow the plugin copy instead of being overridden by it.
- Choose distinctive skill and agent names so plugin components do not silently lose to existing project-level configurations.
- Hooks, MCP servers, and LSP servers have different loading rules; read the official CLI reference before assuming a plugin can override an existing configuration.
- Keep plugin documentation honest about what is packaged. Do not claim the plugin ships skills, agents, or integrations that are not present in the manifest and directory tree.

## Cross-References

- Use `writing-skills` to author any `skills/<name>/SKILL.md` content the plugin packages.
- Use `writing-custom-agents` to author any `agents/*.agent.md` profiles.
- Use `writing-hooks` to author `hooks.json`.
- Use `bootstrap-skillful` when you are first preparing a repository to host Copilot CLI infrastructure before packaging it as a plugin.
- For full field definitions and install syntax, consult the official Copilot CLI plugin documentation rather than copying large reference tables into the plugin itself.

## Done Criteria

- Plugin root contains a valid `plugin.json`
- Manifest `name` is kebab-case and matches the intended install/uninstall name
- Component directories and files exist exactly where the manifest says they do
- README or equivalent docs explain how to install, list, and verify the plugin
- Local install flow is documented and tested, including reinstalling after local edits
- Each packaged skill, agent, hook, or integration follows the rules of its own authoring mechanism
- The plugin boundary is clear: repo-only customizations remain in `.github/`, distributable ones live in the plugin

## Best Practices for Authoring Plugins

1. **Keep the manifest explicit** — even when the CLI has defaults, explicit component paths reduce ambiguity for future maintainers.
2. **Choose distinctive component names** — plugin skills and agents can be shadowed by project-level or personal ones with the same name.
3. **Test the install lifecycle, not just the files** — verify install, list, use, update, and uninstall behavior with the actual CLI commands.
4. **Keep docs aligned with what ships** — README examples, manifest paths, and on-disk directories should describe the same packaged surface.
