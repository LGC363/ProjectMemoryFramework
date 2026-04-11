# .agents — Project Business Memory Layer

This directory is the persistent business knowledge layer for agent-assisted development.
It accumulates knowledge about system behavior, implementation details, and feature history
so that agents can work with project context across sessions without rediscovering it
from scratch each time.

---

## Directory Structure

```
.agents/
├── index.md          Human-readable navigation — start here to find relevant docs
├── catalog.yaml      Machine-readable document index with IDs and cross-references
│
├── rules/            Governance rules. Most are ready-to-use; some contain required
│   └──               project-specific fill-in sections noted in setup/checklist.md
│   ├── ue_repo_conventions.md    UE scanning rules, file reading strategy
│   ├── memory_governance.md      Pre/post task protocols, update rules
│   └── code_style_baseline.md    Readability, encoding safety, no-modify rules
│
├── setup/            Project-specific configuration (fill in when installing)
│   ├── checklist.md              Setup steps + external requirement ingest flow
│   ├── project_profile.md        Project name, version, role, technology stack
│   ├── search_scope.md           Tier 1/2 directory search scope
│   ├── scripting_patterns.md     Scripting bridge integration patterns
│   └── CLAUDE.template.md        Bridge template for Claude Code
│
├── templates/        Document templates with inline examples
│   ├── module.md     Template for module behavior documents
│   ├── unit.md       Template for implementation unit documents
│   └── demand.md     Template for feature flow records
│
├── modules/          Current module behavior, debug entry points, boundaries
├── units/            Selected high-value implementation units
├── demands/          Feature flow records, requirement history, architecture decisions
│
├── exports/          Focused handoff packages for sharing subsets of knowledge
└── legacy/           Historical notes preserved after migration
```

---

## Reading Priority

If a document in `.agents/` conflicts with the actual code or runtime configuration:
**code and configuration win.** Update the document and mark it stale rather than trusting
the document over the code.

---

## Setup Note

Most files under `rules/` are reused as-is. However, when `setup/checklist.md`
explicitly tells you to fill in a project-specific section inside a rule file
(for example, auto-generated directories in `code_style_baseline.md`), that setup step
is mandatory and takes precedence over the default "ready-to-use" expectation.

---

## Governance Summary

See `rules/memory_governance.md` for the full protocol. Quick reference:

**Before each task**: Read `index.md` → relevant `modules/` → relevant `units/`

**After each task**: Evaluate whether any of the following changed:
- Module responsibilities, flows, or debug entry points → update `modules/`
- Key entry points, risk points, or bridge points → update `units/`
- Feature intent, architecture decisions, or history → update `demands/`
- Any formal doc created/deleted/renamed → sync `catalog.yaml`
- Any discoverability change → sync `index.md`

**Final response**: Always end with one of:
`Memory updated: module + unit` / `Memory updated: demand` / `No memory update needed`

---

## Document Creation Standards (Quick Reference)

| Document type | When to create |
|---|---|
| `modules/` | Non-obvious responsibility boundary, debug sequence worth preserving |
| `units/` | High-value entry point, high-risk area, repeatedly visited during debugging |
| `demands/` | Medium/large feature, architectural decision, systemic bug investigation |

**Do not create unit documents for every file.** Selectivity is the point.
