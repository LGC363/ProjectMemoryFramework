# Exports

Use this directory for focused handoff packages — a self-contained subset of `.agents/`
prepared for a specific sharing purpose: code review, agent handoff, onboarding a new
engineer to a subsystem, or archiving a completed feature's knowledge.

## Recommended Package Shape

```
exports/PKG-{Topic}-{YYYYMMDD}/
├── README.md          Summary and reading order for this package
├── modules/           Copied module documents
├── units/             Copied unit documents
└── demands/           Demand documents (only when history context matters)
```

## Sizing Guideline

Export the **minimum useful set**: typically one module plus 2-5 related units.
Add a demand document only when historical context — initial architecture, key decisions,
or ticket history — is essential for the recipient.

Do not export the entire `.agents/` tree. The value is in the focused selection.

## Package README Template

```markdown
# PKG-{Topic}-{YYYYMMDD}

## Purpose
{One sentence: what is this package for and who is it for?}

## Reading Order
1. `modules/` — start here for system behavior overview
2. `units/` — dive into specific entry points
3. `demands/` — historical context (if included)

## Scope
{What subsystems and features does this package cover?}
{What is explicitly NOT included?}
```
