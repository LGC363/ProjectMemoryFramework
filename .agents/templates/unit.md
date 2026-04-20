---
id: UNIT-{AREA}-{PascalCaseName}
type: unit
status: active
area: {AREA}
source_paths:
  # Actual source file paths this unit documents (relative from repo root)
  - {Path/To/SourceFile.ext}
owner_module: MOD-{AREA}-{OwnerModuleName}
related_demands: []
owners: []
tags: []
updated_at: YYYY-MM-DD
---

# UNIT-{AREA}-{PascalCaseName}

<!--
When to create a unit document:
  - This is a critical entry point or bridge point between systems
  - This area is often broken or misunderstood
  - This file is repeatedly visited during debugging
  - There are non-obvious timing, ordering, or state constraints here

Do NOT create unit documents for every file. Only create them where a note materially
reduces the chance of a mistake. Selectivity is the point.

source_paths: list the actual files this unit covers. One unit can cover 1-3 tightly
related files (e.g. a .h/.cpp pair, or a Lua file and its IntelliSense binding).
-->

## 1. 职责

<!--
One short paragraph. Describe what specific problem this implementation unit solves.
Be precise about its scope within the larger module.
-->

这个实现单元负责 {具体职责}，是 {owner module} 中的 {role，例如：状态机核心 / 入口桥接层 / 配置读取层}。

## 2. 主入口

<!--
List the key functions, lifecycle hooks, and their one-line purpose.
This is the "where to start reading" section.
-->

- **宿主 (Host)**: `{ClassName}` in `{path/to/file.ext}`
- **关键函数**:
  - `{FunctionName()}` — {one-line purpose}
  - `{FunctionName()}` — {one-line purpose}
- **生命周期入口**: `{InitFunction()}`, `{CleanupFunction()}`

## 3. 输入输出与依赖

- **输入 (Input)**: {What data, events, or calls come into this unit}
- **输出 (Output)**: {What this unit produces, emits, or hands off}
- **关键依赖 (Key dependencies)**: {Other units, modules, or global systems this unit relies on}

## 4. 常见修改点

<!--
List the places most frequently changed and what downstream effects those changes have.
Format: "修改 X → 影响 Y"
-->

- 修改 `{FunctionName()}` → 影响 {downstream behavior}
- 新增 {capability type} → 优先看 `{FunctionName()}` 是否已有扩展点
- 调整 {timing or state behavior} → 先确认 {invariant or constraint}

## 5. 风险点

<!--
Minimum 2 risk points. Each MUST:
  - Name a specific component, function, or state (not a vague category)
  - State a specific bad outcome if the risk is not respected (not a generic warning)

Bad example (too vague):  "Be careful with timing"
Good example:  "`InitWidget()` must be called before `SetData()` — calling out of order
               silently skips data binding with no error, causing blank UI on first open"
-->

- `{ComponentOrState}` 是 {actual role}，不是 {common misconception}；
  误改容易导致 {specific bad outcome}
- `{FunctionName()}` 依赖 {timing / order / external state}；
  改动时注意 {specific constraint}
- {Any invariant that must never be violated in this unit}

---
<!--
POST-CREATE: After saving this file as a formal unit document:
  1. ~~Add an entry to `.agents/catalog.yaml`~~ — handled by the sync tool (`python .agents/tools/sync-catalog.py`)
     (Kimi CLI hooks). On non-Kimi platforms, add the entry manually.
  2. If this unit is new to the index, add a navigation link in `.agents/index.md` (REQUIRED).
     This cannot be automated because it involves human-readable grouping decisions.
  Skipping step 2 leaves the index out of sync and breaks agent discovery.
-->
