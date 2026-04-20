# Agent Onboarding — Quick Start

This is your one-page guide to getting oriented in a project that uses the Agent Business
Memory Framework. Read this first if you are new to this project or this framework.

---

## Step 0 — Is the Framework Initialized?

Before reading any `.agents/` memory, check the Initialization Gate.
All six must be true:

1. `setup/project_profile.md` exists and has no `{PLACEHOLDER}` values
2. `setup/search_scope.md` exists and has no `{PLACEHOLDER}` values
3. `setup/scripting_patterns.md` exists or is explicitly marked `N/A`
4. `index.md` has no `{Subsystem N}` placeholder headings
5. `catalog.yaml` has a real date and a non-empty `areas` list
6. **The guidance layer is installed** (hooks for Kimi CLI, or bridge for other platforms)

**If any condition is unmet:** complete `setup/checklist.md` Part 1 before starting work.
Do not use `.agents/` memory until the gate passes.

---

## Step 1 — Understand the Project

Read in this order (5–10 minutes):

1. `AGENTS.md` (project root) — repository rules, conventions, search boundaries
2. `setup/project_profile.md` — project name, UE version, scripting language, developer role
3. `setup/search_scope.md` — Tier 1/2 directories, never-scan list
4. `.agents/index.md` — which subsystems and modules exist

---

## Step 2 — Before Any Non-Trivial Task

Read the relevant memory layer:

1. `.agents/index.md` → find relevant modules and units
2. `.agents/modules/{relevant}.md` → system behavior, debug entry points
3. `.agents/units/{relevant}.md` → risk points, entry point functions
4. `.agents/demands/{relevant}.md` → only if historical context or architecture decisions matter

Full rules: `rules/memory_governance.md` Pre-Task Protocol.

---

## Step 3 — After Every Task

MUST end your final response with exactly one of:

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

When you create, rename, or archive any formal doc:
- ~~Sync `catalog.yaml`~~ — **handled by the sync tool** (`python .agents/tools/sync-catalog.py`). On other platforms, sync manually.
- Sync `index.md` (if navigation changed) — **manual**, automation cannot reliably decide human-readable grouping

This list must stay aligned with `rules/memory_governance.md`.
Full rules: `rules/memory_governance.md` Post-Task Protocol.

---

## FAQ — Common Blockers

**Q: index.md and catalog.yaml have no entries yet. Is that expected?**
A: Yes. They start empty and accumulate as work progresses. If the framework was just
installed, complete `setup/checklist.md` Part 1 to confirm the gate passes.

**Q: search_scope.md has no content relevant to what I'm looking for.**
A: Either Tier 1/2 wasn't filled in correctly (complete Part 1 Step 2), or the area
genuinely isn't covered — use Tier 2 as a fallback and update search_scope.md if you
discover the correct location.

**Q: A document in .agents/ says X, but the code does Y. Which do I trust?**
A: The code always wins. Update the `.agents/` document to reflect what the code actually
does and mark what changed in the evolution log or module document.
