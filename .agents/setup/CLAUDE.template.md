# CLAUDE.md

<!-- Copy this file to the PROJECT ROOT as CLAUDE.md (not inside .agents/). -->
<!-- Fill in the paths and optional sections below. -->

This file provides Claude Code-specific guidance for this repository.

## Shared Project Rules

All repository-level rules, search policies, and memory governance are in `AGENTS.md`.

@AGENTS.md

---

## Claude-Only Additions

### Data Source Policy

- Treat `.agents/` as the repository-local business memory layer.
- Read order: `AGENTS.md` → `.agents/index.md` → `modules/` → `units/` → `demands/`
- Keep incomplete Claude-only analysis in Claude private memory, not in `.agents/`.
- When a note is intended to survive across sessions and be shared with other agents,
  write it in `.agents/` using the formal module/unit/demand structure.

### Local-First Boundaries

- `.agents/` is local-first project memory in the repository path.
- Claude private continuity, personal preferences, and session carry-over stay in
  Claude's own memory system, outside `.agents/`.

### Scripting IntelliSense (Optional — UnLua / Scripting Bridge)

<!-- Fill in if this project uses a scripting bridge that generates IntelliSense files. -->
<!-- Example for UnLua: -->
<!--
IntelliSense root: `{absolute path to IntelliSense directory}`

When reading or editing a script file, first locate and read the matching IntelliSense
file to confirm exposed widget/component fields before changing code.
-->

<!-- If this project does not use a scripting bridge with IntelliSense, delete this section. -->

### Claude Private Memory

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
