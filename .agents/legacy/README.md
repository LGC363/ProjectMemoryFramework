# Legacy

This directory preserves historical notes after a documentation restructure or migration.

Files here are retained for context and traceability, but they are **not** the primary
discovery layer. Always prefer `modules/`, `units/`, and `demands/` first.

## When to Use Legacy

- Migrating from a previous documentation format (wiki dumps, ad-hoc markdown notes,
  old investigation reports) into the formal three-layer structure.
- Preserving raw analysis or investigation reports that have already been summarized into
  formal module/unit/demand documents, but where the source is worth keeping.
- Archiving notes from a previous project phase that no longer reflect current state.

## What Does NOT Belong Here

- **Active documentation**: if a note is still authoritative, it belongs in
  `modules/`, `units/`, or `demands/`.
- **Unstable drafts**: in-progress analysis that hasn't stabilized belongs in the
  conversation or a temporary demand with `status: planned`.

## Subdirectory Conventions

Organize by migration batch or source type if needed:

```
legacy/
├── demands/      Old demand or investigation reports
├── modules/      Old module wikis or architecture notes
└── {batch}/      Named migration batch if applicable
```
