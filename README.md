# ProjectMemoryFramework

`ProjectMemoryFramework` is a **reliable, repo-local business memory framework** for agent-assisted development in large Unreal Engine projects.

Unlike convention-only approaches that rely solely on agent discipline, this framework
combines **structured documentation** with **contextual guidance** and **automation tools**
to help agents follow the protocol without adding cognitive burden:

- accumulate project knowledge across sessions
- keep agent-readable memory close to the codebase
- standardize module / unit / demand documentation
- **contextually guide** agents to read-before-work and update-after-work
- **automate** mechanical tasks (catalog sync, health checks)

The framework is intentionally simple:

- `AGENTS.md` is the shared entry point
- `.agents/` is the local-first memory layer
- everything else is derived from those two

## What Problem It Solves

In long-lived UE projects, agents repeatedly lose time on the same problems:

- rediscovering subsystem boundaries
- re-tracing old debugging paths
- forgetting why a feature was designed a certain way
- drifting away from project coding and search conventions

`ProjectMemoryFramework` solves that by adding a small structure directly inside the repo:

- `modules/` for current system behavior
- `units/` for high-value implementation entry points
- `demands/` for feature flow history and architecture decisions
- `catalog.yaml` and `index.md` for discoverability

## Who It Is For

- Unreal Engine teams using AI agents for implementation, debugging, or maintenance
- projects that want repo-local shared memory instead of tool-private memory only
- teams that need a repeatable way to onboard new agents into an existing codebase

Although the defaults are UE-oriented, the structure is general enough to be adapted to other large repositories.

## Repository Layout

```text
ProjectMemoryFramework/
├── AGENTS.md
├── INSTALL.md
└── .agents/
    ├── README.md
    ├── index.md
    ├── catalog.yaml
    ├── rules/
    ├── setup/
    ├── templates/
    ├── hooks/              ← Guidance layer (core — not optional)
    ├── modules/
    ├── units/
    ├── demands/
    ├── exports/
    └── legacy/
```

## Core Ideas

### 1. Local-first memory

The memory layer lives inside the repository, not in a private external tool store.  
That makes it inspectable, portable, and shareable across agents.

### 2. Code wins over docs

Memory documents are derived knowledge.  
If `.agents/` conflicts with the actual code or runtime config, update the docs.

### 3. Read before work

Before a non-trivial task, the agent should read:

1. `AGENTS.md`
2. `.agents/index.md`
3. relevant `modules/`
4. relevant `units/`
5. relevant `demands/` when history matters

### 4. Update after work

Every completed task ends with a memory evaluation:

- did module behavior change?
- did a key implementation entry point change?
- did the feature history or architecture record change?
- does `index.md` need syncing? (`catalog.yaml` is synced via `python .agents/tools/sync-catalog.py`)

## Quick Start

If you want the fastest path from download to actual usage, follow these steps.

### Step 1. Download the package

Download the framework package:

1. Open the repository page
2. Click `Code`
3. Click `Download ZIP`
4. Extract the ZIP locally

After extraction, you should have:

```text
ProjectMemoryFramework/
├── AGENTS.md
├── INSTALL.md
└── .agents/
```

### Step 2. Copy the framework into your target project

Copy these two items into the root of your target project:

- `AGENTS.md`
- `.agents/`

Minimal install target:

```text
YourProject/
├── AGENTS.md
└── .agents/
```

If your project already has an `AGENTS.md`, merge the framework section instead of blindly overwriting it.  
See [INSTALL.md](./INSTALL.md) for the exact merge procedure.

### Step 3. Tell your agent to initialize the framework

After copying, the framework is still only a template. You must ask your agent to complete initialization before normal work starts.

Recommended prompt:

```text
Please initialize ProjectMemoryFramework for this repository.
Follow `.agents/setup/checklist.md` Part 1 exactly.
Fill all required setup files, replace placeholder values, install the guidance layer, and run the Initialization Gate check.
Do not start normal development work until all gate conditions pass.
```

Stricter prompt:

```text
Please set up the project memory framework in this repository.
Read `AGENTS.md`, then complete `.agents/setup/checklist.md` Part 1.
You must:
- create or fill `project_profile.md`
- create or fill `search_scope.md`
- create or fill `scripting_patterns.md` or mark it N/A
- replace placeholder subsystem headings in `index.md`
- initialize `catalog.yaml` with a real date and non-empty areas
- install the guidance layer (hooks for Kimi CLI, `.claude/` for Claude Code, `.cursorrules` for Cursor)
- confirm the Initialization Gate passes before doing any other task
```

### Step 4. Review the initialization result

Before letting the agent use the framework for real work, verify that these are complete in the target project:

- `.agents/setup/project_profile.md` (no placeholders)
- `.agents/setup/search_scope.md` (no placeholders)
- `.agents/setup/scripting_patterns.md` or an explicit `N/A` file
- `.agents/index.md` with real subsystem names
- `.agents/catalog.yaml` with a real `updated_at` value and non-empty `areas`
- **Guidance layer installed** (run install script for Kimi CLI; copy `.claude/` for Claude Code; copy `.cursorrules` for Cursor)

If any of these are incomplete, the framework is not active yet.

### Step 5. Start normal usage

Once initialization is complete, the agent should:

1. read `AGENTS.md`
2. read `.agents/index.md`
3. read relevant `modules/`, `units/`, and `demands/`
4. do the task
5. end with a memory update decision (you will be reminded on Kimi CLI)

## Installation

See [INSTALL.md](./INSTALL.md) for the full install and merge procedure.

## Typical Workflow

### Initial setup

1. Copy `AGENTS.md` and `.agents/` into your project
2. Fill `setup/project_profile.md`
3. Fill `setup/search_scope.md`
4. Fill `setup/scripting_patterns.md` or explicitly mark it `N/A`
5. Replace placeholder subsystem headings in `index.md`
6. Set real values in `catalog.yaml`

The setup is not complete until the Initialization Gate passes.

### Initialization Gate

The framework is only active when all of the following are true:

1. `setup/project_profile.md` exists and contains no placeholder values
2. `setup/search_scope.md` exists and contains no placeholder values
3. `setup/scripting_patterns.md` exists, or is explicitly marked `N/A`
4. `.agents/index.md` no longer contains placeholder subsystem headings
5. `.agents/catalog.yaml` has a real date and a non-empty `areas` list
6. **The guidance layer is installed** (Kimi CLI hooks via install script, Claude Code `.claude/` config, or Cursor `.cursorrules`)

If any of these fail, stop and finish setup before using the framework.

On **Kimi Code CLI** and **Claude Code**, the `PreToolUse` hook will remind you if you try to read `.agents/` before initialization is complete.

### During implementation

1. Read the relevant memory documents
2. Work in the codebase
3. Update `modules/`, `units/`, or `demands/` if new stable knowledge was created
4. Sync `index.md` when navigation structure changes (`catalog.yaml` is synced via `python .agents/tools/sync-catalog.py`)
5. End the final response with a memory status line (hooks will remind you on Kimi CLI and Claude Code)

## Document Types

### Module

Use a module document when a subsystem has:

- a non-obvious responsibility boundary
- a useful debug entry sequence
- extension constraints easy to violate

### Unit

Use a unit document only for high-value implementation points:

- key entry points
- bridge points between systems
- high-risk files or timing-sensitive logic

Do not create unit docs for every file.

### Demand

Use a demand document for medium/large features, important architecture decisions, or bug investigations with lasting value.

Demand docs are living records, not one-off task notes.

## Included Content

This package includes:

- UE repository reading/search conventions
- memory governance rules
- coding style baseline
- setup templates for project-specific initialization
- formal templates for module / unit / demand docs

It intentionally does not include:

- project-specific gameplay rules
- project-specific directory ownership
- project-specific generated-file paths
- private agent memory

Those belong to the target project after installation.

## Recommended Use

This framework works best when teams treat it as:

- a shared operational memory layer
- not a replacement for code review
- not a replacement for architecture docs
- not a dumping ground for every minor observation

Selectivity matters.  
The goal is not "document everything", but "preserve what future agents are likely to need".

## Recommended Prompts

These prompts work well in real projects.

### Initialize the framework

```text
Please initialize ProjectMemoryFramework for this repository.
Follow `.agents/setup/checklist.md` Part 1 exactly.
Do not begin normal project work until the Initialization Gate passes.
```

### Start a normal development task

```text
Before working, follow the read order in `AGENTS.md` and `.agents/rules/memory_governance.md`.
Use the existing memory layer first, then work in code.
At the end, explicitly tell me whether memory needed an update.
```

### Ingest a medium or large new requirement

```text
Treat this as a new requirement intake.
Use `.agents/setup/checklist.md` Part 2.
If the task is medium or large, create a demand document first, then continue.
```

## Guidance and Automation

The framework uses a **tiered strategy** to help agents remember the protocol:

| Platform | Mechanism | What it does |
|---|---|---|
| **Kimi Code CLI** | Native `command` hooks (6 events) | Injects context at session/task/code/turn/compact moments |
| **Claude Code** | Native `prompt` hooks (6 events) + `CLAUDE.md` | Injects context at same moments + per-session baseline rules |
| **Cursor** | `.cursorrules` system prompt | Injects static rules into every session |


See `.agents/hooks/README.md` for the full guidance architecture.

## Notes

- The setup and rules are written to be usable by multiple agents, not tied to a single tool
- Claude bridge generation is included as a standard setup step
- If you adapt this for non-UE repositories, review `.agents/rules/ue_repo_conventions.md` first

## License

Add a license file if you plan to distribute or reuse this publicly across projects.
