# Scripting Integration Patterns

<!--
SETUP: Copy this file to setup/scripting_patterns.md and fill in the patterns for this project.

During Smart Setup, the agent will scan script files to infer patterns and mark uncertain
sections with <!-- TODO: verify -->. A human MUST review and correct all TODO entries.

If this project has NO scripting bridge layer, create setup/scripting_patterns.md with:
  # Scripting Integration Patterns
  N/A — this project has no scripting bridge layer.
Do NOT leave this template file in place with {PLACEHOLDER} values — that fails the
Initialization Gate and blocks the framework from being used.
-->

This document records the scripting integration patterns for this project's script-to-C++ bridge.
It is the authoritative quick reference for how scripts are structured and how they interact with
the UE runtime. Agents should read this before writing or modifying any script file.

---

## Scripting Layer Overview

- **Scripting language**: {Lua | Python | JavaScript | other}
- **Bridge plugin**: {UnLua | sluaunreal | custom | other}
- **Script root directory**: {e.g. Content/Script/BluePrints/}
- **Global entry points**:
  - {GlobalBootstrap.lua / main.py / etc.} — {one-line role}
  - {DataAccess.lua / data_manager.py / etc.} — {one-line role, central data access}
  - {Constants.lua / const.py / etc.} — {one-line role, global constants}

---

## 1. Class / Module Definition Pattern

<!-- Describe how scripts define classes or modules in this project. -->
<!-- Example for a Lua/UnLua project: -->

```lua
-- Standard class definition
local M = Class({"ParentModule.SubPath.BaseClass_C"})

-- With multiple mixins
local M = Class({"ParentModule.SubPath.BaseClass_C", "SharedModule.MixinClass"})
```

<!-- Fill in the actual pattern for this project. -->

---

## 2. Component Composition Pattern

<!-- Describe how complex scripts split logic into components. -->
<!-- Example: -->

```lua
-- _components lists sub-modules whose methods are merged into M
M._components = {
    "Path.To.ComponentA",
    "Path.To.ComponentB",
}
-- Must be called at end of file to merge component methods
AssembleComponents(M)
```

<!-- Fill in the actual pattern, or remove this section if not applicable. -->

---

## 3. Event / Dispatcher Pattern

<!-- Describe how scripts subscribe to and dispatch events. -->
<!-- Example: -->

```lua
-- Subscribe to a global event
self:AddDispatcher("EventName", self, self.OnEventName)

-- Unsubscribe (typically in Destruct or Close)
self:RemoveDispatcher("EventName", self, self.OnEventName)
```

<!-- Fill in the actual pattern for this project. -->

---

## 4. Data Access Conventions

<!-- Describe how scripts access game data (config tables, player state, global constants). -->
<!-- Example: -->

| Access Target | Pattern |
|---|---|
| Global constants | `DataMgr.GlobalConstant["KeyName"].Value` |
| Config table row | `DataMgr.TableName[id]` |
| Player resource | `GWorld:GetAvatar():GetResourceNum(resourceId)` |
| Player progress | `Avatar.ProgressData[id]` |
| Localized text | `GText("UI_KeyName")` |
| Local cache | `Cache:Get("key")` / `Cache:Set("key", value)` |

<!-- Fill in the actual data access patterns for this project. -->

---

## 5. UI / Widget Lifecycle Pattern

<!-- Describe the standard widget lifecycle hooks. -->
<!-- Example: -->

```lua
function M:OnLoaded()   end  -- Called when widget is first created
function M:SwitchIn()   end  -- Called when widget becomes active (for sub-widgets)
function M:SwitchOut()  end  -- Called when widget is deactivated
function M:Destruct()   end  -- Called when widget is destroyed
```

<!-- Fill in the actual lifecycle hooks for this project. -->

---

## 6. Common Pitfalls and Gotchas

<!-- List the scripting-specific pitfalls that are most likely to cause bugs. -->
<!-- Example entries: -->

- **{PitfallName}**: {description of what goes wrong and how to avoid it}
- **{PitfallName}**: {description of what goes wrong and how to avoid it}

<!-- These should be filled in as they are discovered during development. -->

---

## 7. Debug Print Convention

<!-- Describe how debug prints are formatted in this project. -->
<!-- Example: -->

```lua
-- Debug prints use author prefix for easy filtering and cleanup
DebugPrint("{author_initials} {message}")
-- All such prints must be removed before shipping
```

<!-- Fill in the actual convention for this project. -->
