# ProjectMemoryFramework Installation Guide

A plugin-style business memory framework for agent-assisted Unreal Engine development.
Installs into any UE project without modifying or replacing existing files.

---

## What Gets Installed

Two items are added to your project root:

```
YourProject/
├── AGENTS.md          ← Framework hook (merged into or replacing your existing AGENTS.md)
└── .agents/           ← The entire framework lives here
```

---

## Installation

### Step 1 — Copy the Framework Directory

Copy the `.agents/` directory from this package into your project root:

```bash
cp -r ProjectMemoryFramework/.agents/ YourProject/.agents/
```

### Step 2 — Merge AGENTS.md

**If your project does NOT have an `AGENTS.md`:**

Copy `AGENTS.md` from this package to your project root:

```bash
cp ProjectMemoryFramework/AGENTS.md YourProject/AGENTS.md
```

Add any project-specific rules in the marked area at the top of the file, above the `---` separator.

**If your project already has an `AGENTS.md`:**

Append the framework section to your existing file. The framework section starts at the
`# Agent Business Memory Layer` heading (below the first `---` separator in `AGENTS.md`).

```bash
# Preview what will be appended:
grep -n "Agent Business Memory Layer" ProjectMemoryFramework/AGENTS.md

# Append to your existing AGENTS.md:
echo "" >> YourProject/AGENTS.md
sed -n '/^---$/,$ p' ProjectMemoryFramework/AGENTS.md | tail -n +2 >> YourProject/AGENTS.md
```

Your original content is completely preserved — the framework section is purely additive.

These commands are POSIX-style examples. On Windows, use equivalent PowerShell commands
or copy the section manually.

### Step 3 — Smart Setup (MANDATORY — run with your agent)

After copying, the setup templates still contain `{PLACEHOLDER}` values.
**The framework is not active until Smart Setup is complete.**

Tell your agent:

> "Please complete the framework initialization per `.agents/setup/checklist.md` Part 1.
> Run the Initialization Gate check at the end and confirm all six conditions pass."

The agent will:

1. **[Auto]** Read `.uproject` / `CMakeLists.txt` / existing `AGENTS.md` to infer project
   name, UE version, and VCS → write `setup/project_profile.md`

2. **[Auto]** Scan `Source/` and `Content/` to identify subsystem directories → write
   `setup/search_scope.md` with Tier 1/2 directory tables

3. **[Auto → Human Review Required]** Detect scripting files (`.lua` / `.py` / `.js`) and
   infer base class patterns, entry points, and data access patterns → write
   `setup/scripting_patterns.md`. Sections that need human review are marked `<!-- TODO: verify -->`.
   **Review and correct these sections before starting development work.**

4. **[Auto]** Replace placeholder subsystem headings in `index.md` with actual subsystem names
   inferred from the project structure

5. **[Auto]** Set real `updated_at` date and `areas` list in `catalog.yaml`

6. **[Auto]** Install the guidance layer — see Step 4 below.

After Smart Setup, run the **Initialization Gate** check (see `setup/checklist.md`).
The framework is not active until all six gate conditions pass.

### Step 4 — Install Guidance Layer (MANDATORY)

The framework's effectiveness depends on a **guidance layer** that injects context
at the moments agents are most likely to forget the protocol. This step is not optional.

Choose your primary agent platform:

**Kimi Code CLI:**

Run the installer from your project root:

```bash
# Windows (PowerShell)
.agents\hooks\install-hooks.ps1

# macOS / Linux
bash .agents/hooks/install-hooks.sh
```

This registers 6 **context-injection hooks** in `~/.kimi/config.toml`. These hooks
never block anything. They inject facts and rules into the agent's context:
- **Session start** — Project context + read-before-work reminder
- **User prompt** — Prompt text + "Is this a dev task?" guidance
- **PreToolUse (Read)** — Warning if reading `.agents/` before initialization
- **PostToolUse (Write/Replace)** — Reminder to evaluate memory impact
- **Turn end** — Prompt to include Memory status line
- **Context compacting** — Warning that memory docs may be evicted

Verify with `/hooks` inside a Kimi CLI shell. You should see 6 configured hooks.

**Claude Code:**

Copy `.claude/` to your project root:

```bash
cp -r ProjectMemoryFramework/.claude YourProject/
```

This provides:
- **`.claude/settings.json`** — 6 native `prompt`-type hooks that mirror the Kimi
  hook events. Claude evaluates these prompts directly (no external scripts).
  Supports template variables: `{{cwd}}`, `{{prompt}}`, `{{tool_input.file_path}}`, etc.
- **`.claude/CLAUDE.md`** — Per-session baseline rules. Claude reads this at session
  start and uses it as grounding throughout the conversation.

> Claude Code hooks are project-level and commitable. Every team member opening this
> project in Claude Code automatically gets the guidance layer — no per-machine setup required.

### Step 5 — Generate Bridge File for Other Platforms (Optional)

**Cursor:**
Copy `setup/CURSOR.template.md` to the project root as `.cursorrules` and fill it in.

This injects static rules into Cursor's system prompt, providing the best available
guidance when native lifecycle hooks are not supported.

### Step 6 — Clean Up

Delete the `ProjectMemoryFramework/` installation package from your project root.
It is a temporary installer, not part of the project.

```bash
rm -rf ProjectMemoryFramework/
```

---

## After Installation

```
YourProject/
├── AGENTS.md             Project rules + framework hook
├── .agents/              Framework — all business memory lives here
│   ├── rules/            UE conventions, governance, coding baseline
│   ├── setup/            Project-specific configuration (auto-filled)
│   ├── templates/        Document templates for module/unit/demand
│   ├── hooks/            Guidance scripts (auto-installed in Step 4)
│   ├── modules/          System behavior docs — accumulates with work
│   ├── units/            Implementation unit docs — accumulates with work
│   ├── demands/          Feature flow records — accumulates with work
│   ├── exports/          Focused handoff packages
│   └── legacy/           Historical notes after migration
├── Source/               Your existing code
└── Content/              Your existing content
```

---

## Cross-Platform Guidance

The framework uses a **tiered guidance strategy** to maximize coverage across platforms:

| Platform | Guidance Mechanism | Coverage |
|---|---|---|
| **Kimi Code CLI** | Native `command` hooks (6 events) | Context injection at session/task/code/turn/compact moments |
| **Claude Code** | Native `prompt` hooks (6 events) + `CLAUDE.md` | Context injection at same moments + per-session baseline rules |
| **Cursor** | `.cursorrules` system prompt | Static rules per session |

> **Philosophy**: All hooks are *context-injection only* — they present facts and rules,
> but the Agent makes all judgments. There is no mechanical blocking.

## Updating the Framework

To update to a newer version:

1. Download the new package.
2. Compare `rules/` files — merge any new rules into your existing `rules/` files.
3. Check `templates/` for updated templates — optionally update your copies.
4. Compare `hooks/` — install updated hook scripts and re-run the hook installer.
5. Do **not** overwrite `setup/`, `modules/`, `units/`, or `demands/` — these contain
   your project's accumulated knowledge.

---

## Removing the Framework

1. Delete `.agents/` from your project root.
2. Remove the appended framework section from `AGENTS.md` (from `# Agent Business Memory Layer`
   to end of file, or from the `---` separator that precedes it).
3. Remove `CLAUDE.md` / `.cursorrules` if generated by the framework.
4. Remove PMF hooks from `~/.kimi/config.toml` (delete the block between
   `# === ProjectMemoryFramework Hooks` and `# === End PMF Hooks`).
5. Remove `.claude/` from your project root (if using Claude Code).

---

## Optional Enhancements

**log.md** — Append-only activity log for time-ordered traceability.
Format: `## [YYYY-MM-DD] type | title`
Create `.agents/log.md` and note it in `rules/memory_governance.md`.
