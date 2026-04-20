# CLAUDE.md

<!-- Copy this file to the PROJECT ROOT as CLAUDE.md (not inside .agents/). -->
<!-- Fill in the paths and optional sections below. -->

This file provides Claude Code-specific guidance for this repository.

## Shared Project Rules

All repository-level rules, search policies, and memory governance are in `AGENTS.md`.

@AGENTS.md

---

## Framework Initialization Gate (MANDATORY)

Before reading or writing any `.agents/` memory documents, verify the framework
is initialized. All six conditions must be true:

1. `setup/project_profile.md` exists and has no `{PLACEHOLDER}` values
2. `setup/search_scope.md` exists and has no `{PLACEHOLDER}` values
3. `setup/scripting_patterns.md` exists or is explicitly marked `N/A`
4. `index.md` has no `{Subsystem N}` placeholder headings
5. `catalog.yaml` has a real date and a non-empty `areas` list
6. **The guidance layer is installed** — Git pre-commit hook must be in place

If any condition is unmet: complete `setup/checklist.md` Part 1 before starting work.
Do not use `.agents/` memory until the gate passes.

## Read Order (MANDATORY)

Before starting any non-trivial task, read in this order:

1. `AGENTS.md` (project root) — repository rules, conventions, search boundaries
2. `.agents/index.md` — find which modules and units are relevant
3. `.agents/modules/{relevant}.md` — system behavior, debug entry points
4. `.agents/units/{relevant}.md` — risk points, entry point functions
5. `.agents/demands/{relevant}.md` — historical context (when needed)

## Memory Update Requirement (MANDATORY)

Every completed task MUST end with exactly one of:

- `Memory updated: module`
- `Memory updated: unit`
- `Memory updated: demand`
- `Memory updated: module + unit`
- `Memory updated: module + demand`
- `Memory updated: demand + module; index synced`
- `Memory updated: catalog only`
- `No memory update needed`

## Automated Guarantees (Claude Limitations)

Claude Code does not support lifecycle hooks. The following are **not automated** and
require strict discipline:
- Catalog.yaml sync — you MUST manually add/update entries when creating formal docs
- Memory status line — you MUST remember to include the final line
- Init Gate — you MUST self-check before reading `.agents/`

The Git pre-commit hook (`validate_agents_health.py`) will catch mechanical
errors (orphan docs, stale paths) at commit time, but cannot check turn-level
behavior.

## Data Source Policy

- Treat `.agents/` as the repository-local business memory layer.
- Keep incomplete Claude-only analysis in Claude private memory, not in `.agents/`.
- When a note is intended to survive across sessions and be shared with other agents,
  write it in `.agents/` using the formal module/unit/demand structure.

## Local-First Boundaries

- `.agents/` is local-first project memory in the repository path.
- Claude private continuity, personal preferences, and session carry-over stay in
  Claude's own memory system, outside `.agents/`.

## Scripting IntelliSense (Optional — UnLua / Scripting Bridge)

<!-- Fill in if this project uses a scripting bridge that generates IntelliSense files. -->
<!-- Example for UnLua: -->
<!--
IntelliSense root: `{absolute path to IntelliSense directory}`

When reading or editing a script file, first locate and read the matching IntelliSense
file to confirm exposed widget/component fields before changing code.
-->

<!-- If this project does not use a scripting bridge with IntelliSense, delete this section. -->

## Claude Private Memory

<!-- Fill in the path to Claude's cross-session memory for this project. -->
<!-- This path is machine-specific and should not be committed to version control. -->
<!--
Claude Code cross-session memory for this project:
`{C:\Users\YourName\.claude\projects\ProjectName\memory\}`

Use it only for:
- User preferences and working style
- Session continuity notes
- Temporary reminders not meant for other agents

Do not store module, demand, or unit knowledge there — it belongs in `.agents/`.
-->
