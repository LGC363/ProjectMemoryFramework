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

## Guidance Layer

This framework does not use blocking enforcement. Instead, it employs a **guidance
layer** that reminds agents of the protocol at the moments they are most likely to
forget. The specific mechanisms depend on the agent platform:

### Kimi Code CLI

When the framework's hooks are installed (see `setup/checklist.md` Step 6), the
following context is injected automatically:

| Moment | Context Injected | Hook Event |
|---|---|---|
| New session starts | Project context + "Read memory before working" | `SessionStart` |
| User submits a prompt | Prompt text + "Is this a dev task?" guidance | `UserPromptSubmit` |
| Agent reads `.agents/` too early | Init Gate status + setup reminder | `PreToolUse` |
| Business code is modified | File path + "Evaluate memory impact" guidance | `PostToolUse` |
| Turn ends after code changes | Modified files list + Memory status line reminder | `Stop` |
| Context about to compact | "Memory docs may be evicted" warning | `PreCompact` |

These hooks **never block**. Python scripts print to stdout (exit 0) and Kimi adds
that text to the agent's reasoning context. The agent sees the context and can choose
to follow it or ignore it.

The hooks are **fail-open**: if a hook script crashes, the agent workflow is not blocked.

### Claude Code

Claude Code supports native `prompt`-type hooks via project-level `.claude/settings.json`.
No external scripts are needed — Claude evaluates the prompt instructions directly.

The same 6 events are covered, with the same philosophy: present facts and rules,
let the Agent judge:

| Moment | Context Injected | Hook Event |
|---|---|---|
| New session starts | Project context + read-before-work reminder | `SessionStart` |
| User submits a prompt | Prompt text + dev-task guidance | `UserPromptSubmit` |
| Agent reads `.agents/` | Init Gate check reminder | `PreToolUse` |
| Business code is modified | File path + memory impact evaluation | `PostToolUse` |
| Turn ends | Memory status line reminder | `Stop` |
| Context about to compact | Memory docs eviction warning | `PreCompact` |

Claude Code hooks are **project-level** (`.claude/settings.json` lives in the repo).
This means the guidance layer is automatically shared across all team members who
open this project in Claude Code — no per-machine setup required.

### Other Platforms (Cursor, etc.)

These platforms do not support lifecycle hooks. Guidance falls back to:

1. **System prompt injection** — via `.cursorrules`, the agent receives the
   full governance rules in every session context.

On these platforms, compliance relies entirely on agent discipline. The framework
still works, but the reminders are static (per-session) rather than dynamic (per-event).

---

## Pre-Task Protocol (MANDATORY)

**Before starting any non-trivial task, MUST follow these steps in order.**
Skipping any step is a protocol violation.

**Step 0 — Initialization Gate check:**
Verify that the framework Initialization Gate in `setup/checklist.md` has been passed.
All six conditions must be true before using `.agents/` as a context source.
If any condition is unmet, complete `setup/checklist.md` Part 1 first — do not proceed
with the task until the gate passes.

On **Kimi CLI** and **Claude Code**, Step 0 is also supported by the `PreToolUse` hook:
if you attempt to read `.agents/` before the gate passes, the hook injects a reminder
message explaining what still needs to be set up.

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

### Catalog and Index Sync

**`catalog.yaml` — TOOL-ASSISTED**

Run the sync tool after creating or modifying formal documents:

```bash
python .agents/tools/sync-catalog.py
```

This script scans all `.md` files under `modules/` / `units/` / `demands/`,
extracts their frontmatter, and regenerates `catalog.yaml` from scratch.
It is idempotent — safe to run any time.

You do **not** need to manually edit `catalog.yaml`.

**`index.md` — MANUAL**

`index.md` navigation must still be maintained by hand because it involves
human-readable grouping decisions that automation cannot reliably make.

Sync `index.md` when:
- A new subsystem is introduced
- A new module is added that agents should be able to discover
- A module or demand is archived and the link should be removed
- The recommended reading path for any subsystem changes

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

On **Kimi Code CLI**, the `Stop` hook injects a gentle reminder when business code
was modified during the turn: "Please include a Memory status line in your final
response." This is a reminder, not a block — the agent can still choose how to respond.

On other platforms, this remains a convention-based rule. Agent discipline is
the primary safeguard — there is no mechanical enforcement for turn-level behavior.

---

## Optional Extension: log.md

For projects that need a chronological timeline of agent activity, a `log.md` file can be
maintained at `.agents/log.md`.

Format: `## [YYYY-MM-DD] {type} | {title}`

Type values: `task:completed` / `bug:fixed` / `demand:created` / `demand:updated` /
`module:updated` / `unit:updated`

This is **not required** by default. Enable it when the project benefits from time-ordered
traceability that goes beyond what demand evolution records provide.
