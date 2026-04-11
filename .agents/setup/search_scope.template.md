# Search Scope

<!-- Copy this file to setup/search_scope.md and fill in directory paths. -->
<!-- During Smart Setup, the agent will scan Source/ and Content/ to suggest values. -->
<!-- Review and correct after auto-fill. -->

---

## Tier 1 — Daily Work (Search Here First)

These directories contain the primary code for the systems this developer works on.
Always search Tier 1 before expanding to Tier 2.

| Subsystem | C++ Headers | C++ Implementation | Scripts / Other |
|---|---|---|---|
| **{Subsystem1}** | `Source/{Project}/Public/{Sub1}/` | `Source/{Project}/Private/{Sub1}/` | `{ScriptRoot}/{Sub1}/` |
| **{Subsystem2}** | `Source/{Project}/Public/{Sub2}/` | `Source/{Project}/Private/{Sub2}/` | `{ScriptRoot}/{Sub2}/` |
| **{Subsystem3}** | `Source/{Project}/Public/{Sub3}/` | `Source/{Project}/Private/{Sub3}/` | `{ScriptRoot}/{Sub3}/` |

<!-- Add rows for each primary subsystem. Remove rows that don't apply. -->

---

## Tier 2 — Supporting Code (Search When Tier 1 Is Insufficient)

These directories contain shared utilities, framework code, and cross-cutting concerns.

| Area | Path | Notes |
|---|---|---|
| Common / Shared C++ | `Source/{Project}/Public/Common/` | Shared types, macros, utilities |
| Shared Scripts | `{ScriptRoot}/Common/` | Shared scripting utilities, base classes |
| Game Framework | `Source/{Project}/Public/Game/` | GameMode, GameState, framework classes |
| Network / Protocol | `{NetworkPath}/` | Protocol definitions — read-only reference |
| {Other} | `{path}` | {description} |

---

## Subsystem Search Strategy

When the task involves a specific subsystem, search only that subsystem's directories first.
Do not cross subsystem boundaries until the targeted search fails.

Examples:
- Combat task → search only Combat directories in Tier 1
- UI task → search only UI directories in Tier 1
- Character task → search only Character directories in Tier 1

---

## Out of Scope — Never Search Unless Explicitly Requested

The following directories are excluded from all searches by default.
This list is in addition to the UE-general exclusions in `rules/ue_repo_conventions.md`.

```
# Project-specific out-of-scope directories
{OutOfScopeDir1}/
{OutOfScopeDir2}/
{OutOfScopeDir3}/
```

<!-- Common candidates for exclusion:
  Server/                           — server-side code not owned by this developer
  Content/Script/Datas/             — auto-generated data tables
  Content/Script/StoryCreator/      — story editor tooling
  Source/{Project}/Public/AI/       — AI systems not owned by this developer
  Source/{Project}/Public/SDK/      — third-party SDK wrappers
-->
