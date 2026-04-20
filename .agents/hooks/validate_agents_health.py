#!/usr/bin/env python3
"""
Agent Business Memory Health Validator
======================================
Run this as a Git pre-commit hook or on-demand to validate the integrity
of the `.agents/` business memory layer.

Usage:
    python3 .agents/hooks/validate_agents_health.py

Exit codes:
    0 — All checks passed
    1 — One or more checks failed (details printed to stderr)

Checks performed:
    1. No placeholder values in setup files
    2. All catalog.yaml paths point to existing files
    3. No orphan documents in modules/units/demands (files not in catalog)
    4. updated_at is not stale (> 30 days)
    5. index.md has no Subsystem placeholders
    6. No broken cross-references in catalog.yaml
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


def find_repo_root() -> Path:
    """Walk up until we find .agents/catalog.yaml or .git/."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".agents" / "catalog.yaml").exists():
            return parent
        if (parent / ".git").exists():
            return parent
    return cwd


def check_placeholders(agents_dir: Path) -> list[str]:
    """Check setup files for leftover placeholders."""
    errors: list[str] = []
    setup_dir = agents_dir / "setup"
    checks = [
        (setup_dir / "project_profile.md", r"\{PLACEHOLDER\}|\{PROJECT_NAME\}"),
        (setup_dir / "search_scope.md", r"\{PLACEHOLDER\}"),
        (setup_dir / "scripting_patterns.md", r"\{PLACEHOLDER\}"),
    ]
    for path, pattern in checks:
        if not path.exists():
            errors.append(f"MISSING: {path.relative_to(agents_dir.parent)}")
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(pattern, text):
            errors.append(f"PLACEHOLDER: {path.relative_to(agents_dir.parent)} contains unresolved placeholder")
    return errors


def parse_catalog_entries(catalog_path: Path) -> tuple[list[dict], list[str]]:
    """Parse catalog.yaml and return list of entries + parse errors."""
    errors: list[str] = []
    entries: list[dict] = []
    text = catalog_path.read_text(encoding="utf-8")

    # Find documents section
    docs_match = re.search(r"^documents:\s*$", text, re.MULTILINE)
    if not docs_match:
        errors.append("CATALOG: missing 'documents:' section")
        return entries, errors

    docs_text = text[docs_match.end():]
    # Split into individual entries
    entry_blocks = re.split(r"\n(?=  - id: )", docs_text.strip())
    for block in entry_blocks:
        if not block.strip():
            continue
        entry: dict[str, str | list] = {}
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("- id:"):
                entry["id"] = line.split(":", 1)[1].strip()
            elif line.startswith("title:"):
                entry["title"] = line.split(":", 1)[1].strip()
            elif line.startswith("type:"):
                entry["type"] = line.split(":", 1)[1].strip()
            elif line.startswith("area:"):
                entry["area"] = line.split(":", 1)[1].strip()
            elif line.startswith("status:"):
                entry["status"] = line.split(":", 1)[1].strip()
            elif line.startswith("path:"):
                entry["path"] = line.split(":", 1)[1].strip()
            elif line.startswith("related_units:"):
                entry["related_units"] = _parse_list(line)
            elif line.startswith("related_demands:"):
                entry["related_demands"] = _parse_list(line)
            elif line.startswith("owner_module:"):
                entry["owner_module"] = line.split(":", 1)[1].strip()
            elif line.startswith("source_paths:"):
                entry["source_paths"] = _parse_list(line)
            elif line.startswith("entrypoints:"):
                entry["entrypoints"] = _parse_list(line)
        if "id" in entry:
            entries.append(entry)

    return entries, errors


def _parse_list(line: str) -> list[str]:
    """Parse a YAML list like '["a", "b"]' or simple inline list."""
    val = line.split(":", 1)[1].strip()
    if val.startswith("[") and val.endswith("]"):
        return [v.strip().strip('"\'') for v in val[1:-1].split(",") if v.strip()]
    return [val] if val else []


def check_catalog_paths(repo_root: Path, entries: list[dict]) -> list[str]:
    """Verify every catalog path points to an existing file."""
    errors: list[str] = []
    for entry in entries:
        path_str = entry.get("path", "")
        if not path_str:
            errors.append(f"CATALOG: {entry['id']} missing path")
            continue
        full = repo_root / path_str
        if not full.exists():
            errors.append(f"BROKEN PATH: {entry['id']} → {path_str} (file not found)")
    return errors


def check_orphan_docs(repo_root: Path, entries: list[dict]) -> list[str]:
    """Find files in modules/units/demands not listed in catalog."""
    errors: list[str] = []
    cataloged_paths = {e.get("path", "") for e in entries}
    agents_dir = repo_root / ".agents"

    for subdir in ("modules", "units", "demands"):
        dir_path = agents_dir / subdir
        if not dir_path.exists():
            continue
        for f in dir_path.iterdir():
            if f.suffix != ".md":
                continue
            rel = str(f.relative_to(repo_root)).replace("\\", "/")
            if rel not in cataloged_paths:
                errors.append(f"ORPHAN: {rel} not listed in catalog.yaml")
    return errors


def check_stale_updated_at(catalog_path: Path) -> list[str]:
    """Check if updated_at is older than 30 days."""
    errors: list[str] = []
    text = catalog_path.read_text(encoding="utf-8")
    match = re.search(r"^updated_at:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    if not match:
        errors.append("CATALOG: updated_at missing or malformed")
        return errors

    try:
        updated = datetime.strptime(match.group(1), "%Y-%m-%d").date()
    except ValueError:
        errors.append("CATALOG: updated_at has invalid date format")
        return errors

    if updated == date(1, 1, 1) or match.group(1) == "YYYY-MM-DD":
        errors.append("CATALOG: updated_at is still a placeholder")
    elif (date.today() - updated) > timedelta(days=30):
        errors.append(f"CATALOG: updated_at is stale ({match.group(1)}, > 30 days)")
    return errors


def check_index_placeholders(agents_dir: Path) -> list[str]:
    """Check index.md for leftover subsystem placeholders."""
    errors: list[str] = []
    index = agents_dir / "index.md"
    if not index.exists():
        errors.append("MISSING: .agents/index.md")
        return errors
    text = index.read_text(encoding="utf-8")
    if "{Subsystem" in text:
        errors.append("INDEX: index.md still contains {Subsystem N} placeholders")
    return errors


def check_cross_references(entries: list[dict]) -> list[str]:
    """Check that cross-references between entries are valid."""
    errors: list[str] = []
    all_ids = {e["id"] for e in entries}

    for entry in entries:
        for field in ("related_units", "related_demands", "owner_module"):
            vals = entry.get(field, [])
            if isinstance(vals, str):
                vals = [vals]
            for ref in vals:
                if ref and ref not in all_ids:
                    errors.append(
                        f"BROKEN REF: {entry['id']} references missing {field} '{ref}'"
                    )
    return errors


def main() -> int:
    repo_root = find_repo_root()
    agents_dir = repo_root / ".agents"

    if not agents_dir.exists():
        print("No .agents/ directory found — nothing to validate.", file=sys.stderr)
        return 0

    all_errors: list[str] = []

    # 1. Placeholders
    all_errors.extend(check_placeholders(agents_dir))

    # 2-6. Catalog-based checks
    catalog_path = agents_dir / "catalog.yaml"
    if catalog_path.exists():
        entries, parse_errors = parse_catalog_entries(catalog_path)
        all_errors.extend(parse_errors)
        all_errors.extend(check_catalog_paths(repo_root, entries))
        all_errors.extend(check_orphan_docs(repo_root, entries))
        all_errors.extend(check_stale_updated_at(catalog_path))
        all_errors.extend(check_cross_references(entries))
    else:
        all_errors.append("MISSING: .agents/catalog.yaml")

    # 5. Index placeholders
    all_errors.extend(check_index_placeholders(agents_dir))

    if all_errors:
        print("【.agents/ Health Check FAILED】", file=sys.stderr)
        print("The following issues must be fixed before commit:\n", file=sys.stderr)
        for e in all_errors:
            print(f"  ✗ {e}", file=sys.stderr)
        print("\nRun `python3 .agents/hooks/validate_agents_health.py` for details.", file=sys.stderr)
        return 1

    print("【.agents/ Health Check PASSED】")
    return 0


if __name__ == "__main__":
    sys.exit(main())
