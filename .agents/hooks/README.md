# Guidance Layer

This directory contains the **guidance hooks** for the ProjectMemoryFramework.
Unlike traditional enforcement systems that block operations, these hooks
**inject context (facts + rules)** into the agent's context at key moments.
They present information and ask the agent to judge; they never interrupt the workflow.

> **Design philosophy:** Agents do not break rules on purpose — they forget.
> The solution is not punishment, but timely context injection at the moments when
> they are most likely to need it.
> 
> **Agent self-determination:** Hooks present facts and rules, but all judgments
> (read memory? update docs? ignore reminder?) are made by the Agent itself.

---

## How Guidance Hooks Work

Kimi Code CLI and Claude Code support lifecycle hooks that inject context
without blocking the workflow.

**Kimi Code CLI** (`command` type hooks):
- Scripts print to **stdout** (exit 0)
- Kimi automatically adds stdout content to the agent's context

**Claude Code** (`prompt` type hooks, project-level `.claude/settings.json`):
- Claude evaluates prompt instructions directly — no external scripts needed
- Supports template variables: `{{cwd}}`, `{{prompt}}`, `{{tool_input.path}}`, etc.
- Project-level config (`.claude/settings.json`) is commitable and shared across team members

Both platforms follow the same philosophy:
- The agent **sees** the context in its reasoning
- The agent **can choose** to follow it or ignore it
- The workflow is **never blocked**

---

## Hook Inventory

### Kimi Code CLI Scripts

| Script | Event | What it injects |
|---|---|---|
| `session_start_context.py` | `SessionStart` | Project context + "Read memory before working" |
| `prompt_submit_context.py` | `UserPromptSubmit` | "Is this a dev task?" guidance (does NOT echo the prompt) |
| `pretooluse_context.py` | `PreToolUse` (ReadFile) | Init Gate status + warning if reading `.agents/` too early |
| `posttooluse_context.py` | `PostToolUse` (Write/Replace) | File path + "Evaluate memory impact" guidance |
| `stop_context.py` | `Stop` | "Include Memory status line" reminder (unconditional) |
| `precompact_context.py` | `PreCompact` | "Memory docs may be evicted" warning |

### Claude Code Prompt Hooks (`.claude/settings.json`)

| Event | What it injects |
|---|---|
| `SessionStart` | Project context + read-before-work reminder |
| `UserPromptSubmit` | Prompt text + "Is this a dev task?" guidance |
| `PreToolUse` (ReadFile) | Init Gate check reminder |
| `PostToolUse` (Write/Replace) | File path + memory impact evaluation |
| `Stop` | Memory status line reminder |
| `PreCompact` | Memory docs eviction warning |

---

## Why This Approach?

### Problem with blocking hooks

Blocking hooks (`exit 2`) assume we can reliably detect every violation and that
the agent will correctly respond to the block. In practice:

- LLM output formats are unstable — precise string matching fails
- Agents use many paths to access files (`ReadFile`, `Shell`+`cat`, `Agent` subcalls)
- False positives frustrate users and train them to ignore the system
- Agents learn to bypass blocks instead of following the protocol

### Why context-injection works better

- **No false positives that block work** — worst case, the agent sees irrelevant context and ignores it
- **No format detection fragility** — we don't parse what the agent said, we just present facts and rules
- **Respects agent autonomy** — the agent makes the judgment call, but it makes it *informed*
- **Composable with other mechanisms** — context injection + `sync-catalog.py` tool + Git pre-commit = layered reliability
- **Works across platforms** — Kimi uses `command` scripts, Claude uses `prompt` hooks, same philosophy

---

## Platform Coverage

| Platform | Hook Type | Mechanism | Per-Event? | Team-Sharable? |
|---|---|---|---|---|
| **Kimi Code CLI** | `command` | Python scripts output to stdout | ✅ Yes | ❌ No (user-level `~/.kimi/config.toml`) |
| **Claude Code** | `prompt` | Claude evaluates prompt strings directly | ✅ Yes | ✅ Yes (project-level `.claude/settings.json`) |
| **Cursor** | N/A | `.cursorrules` static system prompt | ❌ No | ✅ Yes (project-level) |
| **Git (all)** | N/A | `validate_agents_health.py` pre-commit hook | N/A | ✅ Yes (project-level) |

### For Non-Hook Platforms (Cursor, etc.)

Use bridge files for static per-session guidance:
- **Cursor:** `.agents/setup/CURSOR.template.md` → project root `.cursorrules`

These bridge files inject static guidance text into the system prompt for every
session. They are less dynamic than hooks (no per-event reminders), but they
still ensure the agent knows the framework exists and what the rules are.

For all platforms, install the **Git pre-commit hook** as the mechanical bottom line:

```bash
cp .agents/hooks/validate_agents_health.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## Installation

```bash
# Windows (PowerShell)
.agents\hooks\install-hooks.ps1

# macOS / Linux
bash .agents/hooks/install-hooks.sh
```

Verify inside Kimi CLI:
```
/hooks
```

Expected output:
```
Configured Hooks:
  SessionStart:   1 hook(s)
  UserPromptSubmit: 1 hook(s)
  PreToolUse:     1 hook(s)
  PostToolUse:    1 hook(s)
  Stop:           1 hook(s)
  PreCompact:     1 hook(s)
```

---

## Design Principles

### Fail-Open

All hooks catch exceptions and exit `0`. A crashing hook must never harm the agent workflow.

### Zero External Dependencies

Standard library only. No `pip install` required.

### Absolute Paths

Install scripts write **absolute paths** to `~/.kimi/config.toml`. This ensures
hooks work correctly even when Kimi CLI is launched from a subdirectory.

> If you move the project to a different directory, re-run the install script
to update the paths in `config.toml`.

### Cross-Platform

Path separators are normalized. Installers provided for PowerShell and Bash.

---

## Hook JSON Schema

Kimi CLI `command` hooks receive a JSON payload via **stdin**. The exact fields
vary by event. There is **no `event` field** in the payload — the script infers
the event from which file is executing.

| Event | JSON fields | Example |
|---|---|---|
| `SessionStart` | `cwd` | `{"cwd": "/path/to/project"}` |
| `UserPromptSubmit` | `cwd`, `prompt` | `{"cwd": "...", "prompt": "fix the bug"}` |
| `PreToolUse` | `cwd`, `tool_input` | `{"cwd": "...", "tool_input": {"path": "file.cpp"}}` |
| `PostToolUse` | `cwd`, `tool_input` | `{"cwd": "...", "tool_input": {"file_path": "file.cpp"}}` |
| `Stop` | `cwd` | `{"cwd": "/path/to/project"}` |
| `PreCompact` | `cwd` | `{"cwd": "/path/to/project"}` |

**Important notes:**
- `PreToolUse` uses `tool_input.path` (the tool being invoked)
- `PostToolUse` uses `tool_input.file_path` (the file that was written)
- All scripts use `tool_input.get("file_path", tool_input.get("path", ""))` as a defensive fallback
- Scripts should always `try/except json.load(sys.stdin)` and `sys.exit(0)` on failure
