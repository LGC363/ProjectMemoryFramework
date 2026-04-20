---
id: MOD-{AREA}-{PascalCaseName}
type: module
status: active
area: {AREA}
entrypoints:
  # Key function anchors. Format: "FileName:FunctionName"
  - {SourceFile}:{KeyFunction}
related_units:
  - UNIT-{AREA}-{UnitName}
related_demands: []
owners: []
tags: []
updated_at: YYYY-MM-DD
---

# MOD-{AREA}-{PascalCaseName}

<!--
AREA codes: match the codes defined in catalog.yaml (e.g. CBT, UI, CHR, GAME, NET)
PascalCaseName: descriptive name for this module (e.g. PenalizeExecute, DungeonMatchUI)
-->

## Function Anchors

<!--
RECOMMENDED for any module with a multi-step execution flow or more than one entry point.
For a single-responsibility module with one obvious entry, you may DELETE this entire section.

Rule: if you keep this section, fill it with real anchors (minimum 3).
Do NOT leave the placeholder lines below in the final document — empty anchors are worse
than no anchors, because agents will treat them as information.

Function Anchors use a "symptom → debug entry" format, NOT a plain function list.
Each line answers: "When X goes wrong, start from here."

Format:
  - {symptom}: start from `{File}:{Function}()`, then `{File}:{Function}()`
  - {symptom}: check `{File}:{Function}()` and `{File}:{Function}()`

Real example (from a combat execute system):
  - monster does not enter Defeated state: start from `DeadLogic.cpp:EnterBePenalizedState()`,
    then `HitLogicComponent.lua:SetCharacterDefeatedTag()`
  - execute UI open but player press has no effect: trace `MonPenalizeComponent.lua:Penalize()`
    back to `AttackInputComponent.lua:UsePenalizeSkill()`
  - animation played but monster did not settle correctly: check
    `HitLogicComponent.lua:QuitDefeatedTag()` and `DefeatedRecoverToIdle()`

Remove this comment block when anchors are filled in, or delete the entire section if not needed.
-->

- {symptom 1}: start from `{File}:{Function}()`
- {symptom 2}: check `{File}:{Function}()` and `{File}:{Function}()`
- {symptom 3}: trace `{File}:{Function}()` to `{File}:{Function}()`

## 1. 模块职责

<!--
Describe what this module IS responsible for, and what it is NOT responsible for.
The "not responsible for" boundary is as important as the positive definition.
3-5 sentences.
-->

{Describe the module's core responsibility and explicit scope boundary.}

## 2. 上下游

- **上游 (Upstream)**: {What feeds data, events, or calls into this module}
- **下游 (Downstream)**: {What this module drives, outputs, or hands off to}

## 3. 主流程

<!--
Describe the main execution path as a numbered sequence.
Focus on "what happens in what order", not on code implementation details.
3-6 steps is ideal.
-->

1. {Entry point or trigger condition}
2. {Core processing step}
3. {Key decision point or state transition}
4. {Output, handoff, or completion}

## 4. 扩展边界

<!--
Answer two questions:
1. Where should new requirements for this module be attached?
2. Which modifications are most likely to cause unintended side effects?
-->

- 新需求应挂在 {correct layer or component} 中，不要直接修改 {fragile core component}
- 修改 {X} 容易影响 {Y}，注意 {specific constraint or invariant}
- {Any architectural rule that must be preserved when extending this module}

---
<!--
POST-CREATE: After saving this file as a formal module document:
  1. ~~Add an entry to `.agents/catalog.yaml`~~ — handled by the sync tool (`python .agents/tools/sync-catalog.py`)
     (Kimi CLI hooks). On non-Kimi platforms, add the entry manually.
  2. Add a navigation entry to `.agents/index.md` under the relevant subsystem (REQUIRED).
     This cannot be automated because it involves human-readable grouping decisions.
  Skipping step 2 leaves the index out of sync and breaks agent discovery.
-->
