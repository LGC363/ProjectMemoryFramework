# ProjectMemoryFramework

`ProjectMemoryFramework` is a lightweight, repo-local business memory framework for agent-assisted development.

It gives Unreal Engine projects a consistent way to:

- accumulate project knowledge across sessions
- keep agent-readable memory close to the codebase
- standardize module / unit / demand documentation
- enforce a predictable read-before-work and update-after-work protocol

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
- do `catalog.yaml` and `index.md` need syncing?

## Installation

See [INSTALL.md](./INSTALL.md).

Minimal install target inside your project:

```text
YourProject/
├── AGENTS.md
└── .agents/
```

After copying, you must complete:

- `.agents/setup/checklist.md` Part 1
- the Initialization Gate check

Until that gate passes, the framework is not considered active.

## Typical Workflow

### Initial setup

1. Copy `AGENTS.md` and `.agents/` into your project
2. Fill `setup/project_profile.md`
3. Fill `setup/search_scope.md`
4. Fill `setup/scripting_patterns.md` or explicitly mark it `N/A`
5. Replace placeholder subsystem headings in `index.md`
6. Set real values in `catalog.yaml`

### During implementation

1. Read the relevant memory documents
2. Work in the codebase
3. Update `modules/`, `units/`, or `demands/` if new stable knowledge was created
4. Sync `catalog.yaml` and `index.md` when formal docs change
5. End the final response with a memory status line

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
The goal is not “document everything”, but “preserve what future agents are likely to need”.

## Notes

- The setup and rules are written to be usable by multiple agents, not tied to a single tool
- Claude bridge generation is included as an optional setup step
- If you adapt this for non-UE repositories, review `.agents/rules/ue_repo_conventions.md` first

## License

Add a license file if you plan to distribute or reuse this publicly across projects.
