# Cursor Rules — ProjectMemoryFramework Bridge

This file provides system-level guidance for Cursor when working in a project
that uses the Agent Business Memory Layer. Copy this file to your project root
as `.cursorrules` and fill in the placeholders.

Cursor reads `.cursorrules` automatically and injects its contents into the
system prompt for every AI interaction in the project.

---

## Framework Initialization Gate (MANDATORY)

Before reading or writing any `.agents/` memory documents, verify the framework
is initialized. All six conditions must be true:

1. `setup/project_profile.md` exists and contains no `{PLACEHOLDER}` values
2. `setup/search_scope.md` exists and contains no `{PLACEHOLDER}` values
3. `setup/scripting_patterns.md` exists **or** is explicitly marked `N/A`
4. `.agents/index.md` subsystem headings have been replaced (no `{Subsystem 1}` etc.)
5. `.agents/catalog.yaml` has a real `updated_at` date and a non-empty `areas` list
6. **The guidance layer is installed** — Git pre-commit hook must be in place

If any condition is unmet: complete `setup/checklist.md` Part 1 first.
Do not start the actual task until the gate passes.

## Read Order (MANDATORY)

Before starting any non-trivial task, read in this order:

1. `.agents/index.md` — find which modules and units are relevant
2. `.agents/modules/{relevant}.md` — system behavior, boundaries
3. `.agents/units/{relevant}.md` — entry points, risk points
4. `.agents/demands/{relevant}.md` — historical context (when needed)

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

## Automated Guarantees (Cursor Limitations)

Cursor does not support lifecycle hooks. The following are **not automated** and
require strict discipline:
- Catalog.yaml sync — you MUST manually add/update entries
- Memory status line — you MUST remember to include the final line
- Init Gate — you MUST self-check before reading `.agents/`

The Git pre-commit hook (`validate_agents_health.py`) will catch mechanical
errors (orphan docs, stale paths) at commit time, but cannot check turn-level
behavior.

## Project-Specific Context

- **Project name**: {PROJECT_NAME}
- **Primary focus areas**: {list 2-4 systems you work in most}
- **Scripting layer**: {Lua | Python | JS | none}
- **Key conventions**: {any project-specific coding patterns agents should know}
