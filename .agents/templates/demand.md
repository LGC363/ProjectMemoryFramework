---
id: DEM-{AREA}-{PascalCaseFeature}-{NNN}
type: demand
status: planned
area: {AREA}
related_modules: []
owners: []
tags: []
updated_at: YYYY-MM-DD
---

# DEM-{AREA}-{PascalCaseFeature}-{NNN}

<!--
Status values: planned | in_progress | active | archived

NNN: sequential number within the same area+feature (001, 002, ...).
Use a new NNN only for a completely separate feature, not for a revision of the same feature.

A demand document is a FEATURE FLOW RECORD, not just a requirement summary.
It should retain enough context that any agent reading it alone can recover:
  - Why the feature was built and what business problem it solves
  - What the original architecture looked like
  - Key decisions made along the way and why
  - Where it currently stands and where it connects to module/unit docs

The same document is updated over time. Do not create new demand docs for each iteration —
append to the evolution log instead.
-->

## 1. 背景

<!--
Why does this demand exist? What business problem or user-visible issue triggered it?
Include any system history that explains why this approach was chosen over alternatives.
-->

{描述业务背景和触发原因}

## 2. 目标

**目标 (In Scope):**
- {Goal 1}
- {Goal 2}

**明确不覆盖 (Out of Scope):**
- {Item explicitly excluded from this demand}

## 3. 需求来源

- **Ticket**: {TAPD / Jira / Linear — ID and link}
- **Design doc**: {Feishu / Confluence / Notion link}
- **Other references**: {PRD, verbal requirement date, etc.}

## 4. 初始设计架构

<!--
RECOMMENDED for medium/large features — can be omitted for simple changes.

If included: record the ORIGINAL design at the time this demand was created.
NEVER rewrite or delete this section once it has been written — not even when the
implementation deviates significantly. Later deviations and corrections belong in
Section 7 (演进记录). The value of this section is preserving the original reasoning.

Describe:
  - High-level architecture as initially proposed
  - Key modules / components involved
  - Data flow or state transitions at a conceptual level
  - Significant trade-offs made in the initial design
-->

**初始架构 (Initial Architecture as of {YYYY-MM-DD}):**

{描述初始设计方案}

**初始关键决策 (Initial Key Decisions):**
- {Decision and the reason for it}
- {Decision and the reason for it}

## 5. 影响模块

<!--
List the formal module IDs involved. Must match entries in catalog.yaml.
-->

- `MOD-{AREA}-{ModuleName}`

## 6. 风险与遗留项

**风险 (Risks):**
- {Risk 1}

**遗留项 (Deferred Items):**
- {Item intentionally deferred to a later stage}

## 7. 演进记录

<!--
Append dated entries here as the demand evolves. Do NOT delete earlier entries.
This is the living history of the feature from planning to landing.

Format:
### YYYY-MM-DD — {Stage or milestone name}
- {What changed, was decided, or was discovered}
- {Any deviation from Section 4 initial architecture, and why}
- {New modules or units created as a result}
- Post-landing: links to module/unit docs that now own this feature
-->

### {YYYY-MM-DD} — 初始创建 (Initial Creation)

- {Initial state of the demand}
- {Early constraints or context worth preserving}

---
<!--
POST-CREATE: After saving this file as a formal demand document:
  1. ~~Add an entry to `.agents/catalog.yaml`~~ — handled by the sync tool (`python .agents/tools/sync-catalog.py`)
     (Kimi CLI hooks). On non-Kimi platforms, add the entry manually.
  2. Add a navigation entry to `.agents/index.md` under Formal Demands (REQUIRED).
     This cannot be automated because it involves human-readable grouping decisions.
  Skipping step 2 leaves the index out of sync and breaks agent discovery.
-->
