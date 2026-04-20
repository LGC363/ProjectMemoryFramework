# Setup Checklist

---

## Part 1 — Initial Setup (One-Time)

Complete these steps once when first installing the framework into a new project.
The goal is to make the framework immediately usable without leaving `{PLACEHOLDER}` values.

**Do not start any project work until the Initialization Gate at the end of Part 1 passes.**

### Step 1 — Fill Project Profile

Copy `setup/project_profile.template.md` → `setup/project_profile.md`, then fill in:
- Project name, UE version, version control system
- Primary scripting language (Lua / Python / JS / none)
- Developer role and current focus areas

### Step 1.5 — Identify Auto-Generated Directories

Open `rules/code_style_baseline.md` and fill in the `Auto-Generated Files` section:
- List every directory that is owned by an export tool, code generator, or build pipeline
- Specify the generating tool for each directory
- Until this is filled in, the "Never Modify Manually" rule is incomplete and may be violated

### Step 2 — Fill Search Scope

Copy `setup/search_scope.template.md` → `setup/search_scope.md`, then fill in:
- **Tier 1**: The directories where daily work happens (C++ headers, C++ implementation, scripts).
  These are searched first on every task.
- **Tier 2**: Supporting directories searched when Tier 1 is insufficient.
- **Never-scan**: Project-specific directories to exclude (in addition to the UE-general list in
  `rules/ue_repo_conventions.md`).

If running Smart Setup: scan `Source/` and `Content/` to infer Tier 1/2 directories from the
project's actual directory structure. Mark inferred entries with `<!-- Auto-inferred: verify -->`.

**Depends on Step 1** (project profile informs which subsystems exist).

### Step 3 — Fill Scripting Patterns

Copy `setup/scripting_patterns.template.md` → `setup/scripting_patterns.md`, then fill in
the scripting integration patterns for this project.

If running Smart Setup: scan script files to infer base class names, common import paths, and
data access patterns. Mark sections that need human review as `<!-- TODO: verify -->`.
**A human must review and correct all `<!-- TODO: verify -->` entries before relying on this file.**

If the project has no scripting layer: create `setup/scripting_patterns.md` with just:
```
# Scripting Integration Patterns
N/A — this project has no scripting bridge layer.
```

**Depends on Step 2** (search scope defines where to look for script files).

### Step 4 — Configure Claude Code (If Using Claude Code)

Copy `.claude/` from this package to your project root:

```bash
cp -r .claude YourProject/
```

This provides:
- `.claude/settings.json` — 6 native `prompt`-type hooks (project-level, commitable)
- `.claude/CLAUDE.md` — Per-session baseline rules

No per-machine setup required — team members opening this project in Claude Code
automatically get the guidance layer.

### Step 5 — Initialize Index and Catalog

- `index.md`: Replace the placeholder subsystem headings (`{Subsystem 1}` etc.) with your
  project's actual subsystem names. Leave module/unit entries empty — they accumulate as
  work progresses.
- `catalog.yaml`: Set `updated_at` to today's date. Fill in the `areas` list with the actual
  area codes for this project. Leave `documents` as an empty list.

**Depends on Steps 1 and 2** (subsystem names come from project profile and search scope).

### Step 6 — Install Guidance Layer (MANDATORY)

The guidance layer reminds agents of the protocol at the moments they are most
likely to forget. Skipping this step leaves the framework as vulnerable as any
purely convention-based system.

**For Kimi Code CLI:**
```bash
# Windows (PowerShell)
.agents\hooks\install-hooks.ps1

# macOS / Linux
bash .agents/hooks/install-hooks.sh
```

**For Claude Code:**
```bash
cp -r .claude YourProject/
```

Verify Kimi hooks with `/hooks` in a Kimi CLI shell.
Verify Claude hooks by checking that `.claude/settings.json` exists in your project root.

---

## Initialization Gate

**The framework is NOT active until all six conditions below are true.**
Run this check after completing Part 1. Do not proceed to project work until it passes.

| # | Condition | Check |
|---|---|---|
| 1 | `setup/project_profile.md` exists and contains no `{PLACEHOLDER}` | [ ] |
| 2 | `setup/search_scope.md` exists and contains no `{PLACEHOLDER}` | [ ] |
| 3 | `setup/scripting_patterns.md` exists **or** is explicitly marked `N/A` | [ ] |
| 4 | `.agents/index.md` has no `{Subsystem N}` placeholder headings | [ ] |
| 5 | `.agents/catalog.yaml` has a real date in `updated_at` and non-empty `areas` | [ ] |
| 6 | **Guidance layer is installed** — Kimi hooks / Claude `.claude/` / Cursor `.cursorrules` | [ ] |

If any condition is unmet, return to the corresponding step above and complete it.

---

## Part 2 — External Requirement Ingest Flow

Follow this flow whenever an external requirement arrives (TAPD ticket, design doc, PM request,
verbal requirement, Feishu/Confluence page).

### Step 1 — Read the Source

Read the full external document. Extract:
- What is the user-visible change or new capability?
- What systems or files are likely involved?
- Are there explicit constraints (deadlines, compatibility requirements, data limits)?

### Step 2 — Assess Complexity

| Complexity | Criteria | Action |
|---|---|---|
| **Simple** | Single-file change, no architectural decision, no cross-system impact | Work directly. Update `module` or `unit` doc when done if new knowledge was gained. |
| **Medium** | Multiple files, one subsystem, some design choice involved | Create a demand document. Work. Update docs when done. |
| **Large** | Multi-subsystem, architectural decision, long timeline, or high risk | Create a demand document with initial architecture section. Work in stages. Update docs at each stage. |

When in doubt, err toward creating a demand document. It costs little and provides lasting value.

### Step 3 — Create Demand Document (Medium/Large)

1. Copy `templates/demand.md` → `demands/{area}_{feature_name}.md`
2. Fill in: background, goals, out-of-scope items, requirement source (link to ticket/doc),
   affected modules
3. For large features: fill in the initial design architecture section
4. ~~Add an entry to `catalog.yaml`~~ — **handled by the sync tool** (`python .agents/tools/sync-catalog.py`)
5. Add a navigation entry to `index.md` under the relevant subsystem (REQUIRED — index.md
   navigation cannot be fully automated because it involves human-readable grouping decisions)

### Step 4 — Work

Execute the task. Follow the pre-task read protocol in `rules/memory_governance.md`.

### Step 5 — Update Memory

Follow the post-task protocol in `rules/memory_governance.md` to update module/unit/demand
documents based on what was learned and changed.

---

## Part 3 — Ongoing Workflow Reminders

- **Every task ends with a memory check.** See `rules/memory_governance.md`.
- **Code wins over docs.** If a document conflicts with the code, update the document.
- **Selective unit creation.** Do not create unit documents for every file — only for
  high-value entry points and high-risk implementations.
- **Demand documents are living records.** Append to the evolution log; do not rewrite history.
- **Catalog sync is tool-assisted.** Run `python .agents/tools/sync-catalog.py` after creating
  or modifying formal docs. You only need to sync `index.md` when navigation structure changes.
