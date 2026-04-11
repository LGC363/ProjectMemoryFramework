# Memory Governance

Rules for reading and maintaining the `.agents/` business memory layer.
These rules apply to all agents working in any project that uses this framework.

---

## Core Principle

**Code and runtime configuration are the source of truth.**
`.agents/` documents are derived knowledge — they reflect understanding of the code, not the
reverse. When a document conflicts with the actual code, the code wins. Update the document
and mark it stale rather than trusting the document over the code.

---

## Pre-Task Protocol (MANDATORY)

**Before starting any non-trivial task, MUST follow these steps in order.**
Skipping any step is a protocol violation.

**Step 0 — Initialization Gate check:**
Verify that the framework Initialization Gate in `setup/checklist.md` has been passed.
All five conditions must be true before using `.agents/` as a context source.
If any condition is unmet, complete `setup/checklist.md` Part 1 first — do not proceed
with the task until the gate passes.

**Step 1:** MUST read `.agents/index.md` to identify which modules and units are relevant
to the task.

**Step 2:** MUST read the relevant `modules/` documents to understand current system behavior,
upstream/downstream relationships, and extension boundaries.

**Step 3:** MUST read the relevant `units/` documents for specific entry points, risk points,
and common modification patterns.

**Step 4:** If the task involves a feature with known history or architectural decisions,
MUST read the corresponding `demands/` document.

**Do not jump straight into the codebase without completing steps 1–3.** Doing so defeats
the purpose of maintaining the memory layer.

---

## Post-Task Protocol — Memory Maintenance (MANDATORY)

Memory evaluation is part of task completion. **Do not wait for the user to ask for an update.**

At the end of every completed task, MUST evaluate whether `.agents/` needs updating:

### Update Order

1. **`modules/`** — update if any of the following changed:
   - Module responsibilities, ownership boundaries, or scope
   - Upstream or downstream relationships
   - Main execution flow
   - Debug entry points (Function Anchors)
   - Extension boundaries or constraints

2. **`units/`** — update if any of the following changed:
   - A key entry point function was added, renamed, or removed
   - A new high-value risk point or pitfall was discovered
   - A bridge point between systems changed
   - Source file paths changed

3. **`demands/`** — update if any of the following changed:
   - Business intent, feature scope, or requirement source
   - Initial architecture decisions or their rationale
   - Task staging, milestones, or completion status
   - Long-term constraints or deferred items

### Catalog and Index Sync (MANDATORY)

After any create, delete, rename, or archive of a formal document, MUST sync:

**Sync `catalog.yaml` when:**
- [ ] A new `demand / module / unit` document is created
- [ ] A document is deleted or archived
- [ ] A document is renamed or moved
- [ ] A module's `related_units` or `related_demands` change
- [ ] A unit's `owner_module` changes

**Sync `index.md` when:**
- [ ] A new subsystem is introduced
- [ ] A new module is added that agents should be able to discover
- [ ] A module or demand is archived and the link should be removed
- [ ] The recommended reading path for any subsystem changes

Rule of thumb: **formal docs change → sync `catalog.yaml`; discoverability change → sync `index.md`**.
When in doubt, sync both.

### When NOT to Update

Do not update formal docs for:
- Pure mechanical edits with no new understanding gained
- Trivial bug fixes that don't reveal new knowledge about the system
- Changes that don't alter how an agent should approach this code in the future

---

## Document Creation Standards

### When to create a module document

Create a `modules/` document when a system area:
- Has a non-obvious responsibility boundary
- Has a specific debug entry sequence worth preserving
- Has extension constraints that are easy to violate
- Is frequently misunderstood or incorrectly modified

### When to create a unit document

Create a `units/` document only for **high-value** implementation points:
- Critical entry points or bridge points between systems
- High-risk areas that are often broken or misunderstood
- Places that are repeatedly visited during debugging
- Implementations with non-obvious timing or ordering constraints

Do not create unit documents for every file. Selectivity is the point.

### When to create a demand document

Create a `demands/` document for:
- Medium to large feature implementations
- Changes with significant architecture decisions
- Bug investigations that reveal systemic issues
- Any work where future agents will benefit from knowing "why this was done this way"

For simple, isolated changes: work directly, then update the relevant `module` or `unit`.

---

## Demand Document Principles

Demand documents are **feature flow records**, not just requirement summaries.

A demand document must retain, over its entire lifetime:
- The original requirement source and business context
- The initial design architecture (never delete this section once written)
- Key decisions made along the way and the reasoning behind them
- Evolution log with dated entries appended chronologically

The same document is updated over time. Do not create new demand documents for each
iteration — append to the evolution log instead.

---

## Final Response Convention (MANDATORY)

The final response of every task MUST include exactly one of the following lines:

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

---

## Optional Extension: log.md

For projects that need a chronological timeline of agent activity, a `log.md` file can be
maintained at `.agents/log.md`.

Format: `## [YYYY-MM-DD] {type} | {title}`

Type values: `task:completed` / `bug:fixed` / `demand:created` / `demand:updated` /
`module:updated` / `unit:updated`

This is **not required** by default. Enable it when the project benefits from time-ordered
traceability that goes beyond what demand evolution records provide.
