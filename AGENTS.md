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
All five conditions must be true:

1. `setup/project_profile.md` exists and contains no `{PLACEHOLDER}` values
2. `setup/search_scope.md` exists and contains no `{PLACEHOLDER}` values
3. `setup/scripting_patterns.md` exists **or** is explicitly marked `N/A` in its header
4. `.agents/index.md` subsystem headings have been replaced (no `{Subsystem 1}` etc.)
5. `.agents/catalog.yaml` has a real `updated_at` date and a non-empty `areas` list

**If any condition is unmet: complete `setup/checklist.md` Part 1 first.
Do not start the actual task until the gate passes.**

## Read Order

Before starting any non-trivial task, read in this order:

1. `.agents/index.md` — find which modules and units are relevant to the task
2. `.agents/modules/` — current system behavior, debug entry points, extension boundaries
3. `.agents/units/` — key implementation details, risk points, common modification patterns
4. `.agents/demands/` — feature history and architecture decisions (when historical context matters)

## Conventions and Governance

All agent behavior rules for this project live in `.agents/rules/`:

- `.agents/rules/ue_repo_conventions.md` — repository scanning rules, file reading strategy
- `.agents/rules/memory_governance.md` — pre/post task protocols, memory update rules
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

Omitting this line is a protocol violation.
