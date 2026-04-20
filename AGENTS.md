# AGENTS.md

<!--
INSTALLATION NOTE:
  - New project (no existing AGENTS.md): copy this file to your project root as AGENTS.md.
    Add any project-specific rules in the section above the separator below.
  - Existing AGENTS.md: append everything from the "Agent Business Memory Layer" section
    downward (below the first "---") to the end of your existing AGENTS.md.
    Your original content is completely preserved.
  After copying, run Smart Setup per INSTALL.md before starting any work.
-->

<!-- ============================================================ -->
<!-- ADD PROJECT-SPECIFIC RULES ABOVE THIS LINE                   -->
<!-- The framework hook begins below. Do not modify it.           -->
<!-- ============================================================ -->

---

# Agent Business Memory Layer

This project uses a structured business memory layer for persistent agent knowledge accumulation.

**REQUIRED before any non-trivial task:** read the memory layer in the order defined below.
Skipping this step defeats the purpose of maintaining the layer and is not permitted.

## Framework Initialization Gate

Before reading or writing any `.agents/` memory, verify the framework is initialized.
All six conditions must be true:

1. `setup/project_profile.md` exists and contains no `{PLACEHOLDER}` values
2. `setup/search_scope.md` exists and contains no `{PLACEHOLDER}` values
3. `setup/scripting_patterns.md` exists **or** is explicitly marked `N/A` in its header
4. `.agents/index.md` subsystem headings have been replaced (no `{Subsystem 1}` etc.)
5. `.agents/catalog.yaml` has a real `updated_at` date and a non-empty `areas` list
6. **The guidance layer is active** — see `rules/memory_governance.md` § Guidance Layer

**If any condition is unmet: complete `setup/checklist.md` Part 1 first.
Do not start the actual task until the gate passes.**

## Read Order

Before starting any non-trivial task, read in this order:

1. `.agents/index.md` — find which modules and units are relevant to the task
2. `.agents/modules/` — current system behavior, debug entry points, extension boundaries
3. `.agents/units/` — key implementation details, risk points, common modification patterns
4. `.agents/demands/` — feature history and architecture decisions (when historical context matters)

## Guidance and Automation

The framework uses a **layered strategy** to help agents remember the protocol:

1. **Guidance Hooks** (Kimi CLI) — inject reminder text into context at key moments:
   - Session start: "Read memory before working"
   - Dev task detected: "Find relevant modules first"
   - Code changed: "Consider updating memory docs"
   - Turn ending: "Include Memory status line"
   - Context compacting: "Memory may be evicted, re-read if needed"

2. **Automation Tools** — agents explicitly call these to reduce mechanical burden:
   - `python .agents/tools/sync-catalog.py` — regenerates `catalog.yaml` from all doc frontmatters
   - `python .agents/hooks/validate_agents_health.py` — checks for stale docs / broken refs

3. **Git Pre-Commit Hook** — the mechanical bottom line for all platforms:
   - Rejects commits with orphan documents, placeholder leaks, or stale paths

These mechanisms **guide** and **assist**; they do not override the agent's judgment.
The agent still decides what knowledge is worth preserving.

## Conventions and Governance

All agent behavior rules for this project live in `.agents/rules/`:

- `.agents/rules/ue_repo_conventions.md` — repository scanning rules, file reading strategy
- `.agents/rules/memory_governance.md` — pre/post task protocols, update rules, guidance details
- `.agents/rules/code_style_baseline.md` — engineering standards and coding guidelines

## Project Configuration

Project-specific configuration (search scope, scripting patterns, project profile) lives in
`.agents/setup/`. Read these files to understand the project structure before working.

## Memory Update Requirement

Every completed task MUST end with a memory evaluation. See `rules/memory_governance.md`
for the full protocol. The final response MUST include exactly one of:

```
Memory updated: module
Memory updated: unit
Memory updated: demand
Memory updated: module + unit
Memory updated: module + demand
Memory updated: demand + module; index synced
Memory updated: catalog only
No memory update needed
```

Omitting this line is a protocol violation. The guidance layer will remind you
if it appears to be missing, but the final judgment is yours.
