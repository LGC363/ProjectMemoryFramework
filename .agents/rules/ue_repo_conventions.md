# UE Repository Conventions

General rules for navigating and reading files in a large Unreal Engine repository.
These rules apply to all agents working in any UE project that uses this framework.

> **UE projects:** use this file as-is.
> **Non-UE projects:** review each section and adapt to your build system — the Never Scan list,
> binary file list, and C++ reading strategy may need to be replaced or removed entirely.
> Keep the Tiered Search strategy and Scripting Language strategy, as they apply universally.

---

## Large Repository Notice

This is a large repository. **Do NOT scan the entire repository.**
Always prefer targeted, scoped file searches over broad glob/grep across the whole project.

---

## Tiered Search Prerequisite

**Before using the Tier 1/2 search boundaries defined in `setup/search_scope.md`:**
verify that `setup/search_scope.md` exists as a filled file (not a template with `{PLACEHOLDER}`
values). If setup is incomplete, the Tier 1/2 boundaries are undefined.

If `setup/search_scope.md` is not yet filled:
- Do **not** treat the template placeholders as search boundaries.
- Perform minimal manual exploration limited to the most obvious directories.
- Complete `setup/checklist.md` Part 1 before starting the task.

---

## Directories — Never Scan

The following directories must never be searched or scanned unless the user explicitly requests it.
They contain engine internals, compiled output, or generated data that wastes tokens and provides
no useful business logic:

```
# UE engine internals
Engine/
Plugins/

# Build output
Binaries/
Intermediate/
DerivedDataCache/

# Runtime generated
Saved/
```

<!-- PROJECT: Add project-specific directories to never scan below this line.
Examples of common project-specific exclusions:
  Server/
  Content/Script/Datas/
  Content/Script/StoryCreator/
  Source/YourProject/Public/AI/
  Source/YourProject/Public/SDK/
-->

---

## Files — Never Read (Binary and Asset Files)

Reading these files wastes tokens and returns no useful text content:

```
# UE asset and map files
*.uasset  *.umap  *.ubulk  *.uptnl  *.uexp

# Pak and signature files
*.pak  *.sig

# Platform compiled output
*.exe  *.dll  *.lib  *.pdb  *.obj  *.o  *.a  *.so

# Image and texture files
*.png  *.jpg  *.jpeg  *.tga  *.bmp  *.dds  *.tiff  *.hdr  *.exr

# Audio files
*.wav  *.mp3  *.ogg  *.bank  *.fsb  *.wem

# 3D asset files
*.fbx  *.obj  *.mesh  *.anim  *.skeleton  *.morphtarget

# Font files
*.ttf  *.otf

# Archive files
*.zip  *.7z  *.rar  *.tar  *.gz
```

**Always safe to read:**

- `*.h` / `*.cpp` / `*.cs` — C++ source and build scripts under `Source/`
- `*.ini` — UE config files under `Config/`
- `*.json` — data and config JSON
- `*.xml` — markup config files
- `*.lua` / `*.py` / `*.js` / `*.ts` — scripting language files
- `*.proto` / `*.pb` — protocol definitions
- `*.md` / `*.txt` — documentation and notes
- `*.yaml` / `*.yml` — configuration files

---

## Search Strategy — Tiered Approach

When searching for code, follow this strict order:

1. Search **Tier 1 directories first** (defined in `setup/search_scope.md` for this project).
2. If not found, expand to **Tier 2**.
3. Never expand into the never-scan list above.

When the task involves a specific subsystem:
1. Identify the subsystem from `setup/search_scope.md`.
2. Search **only inside that subsystem's directories** first.
3. Do not cross into unrelated subsystems unless the search fails.

---

## C++ Reading Strategy

1. **Always read the header (`.h`) first** to understand the interface, exposed methods, and types.
2. Only read the `.cpp` implementation if the header is insufficient for the task.
3. Avoid reading both `.h` and `.cpp` unless the implementation detail is necessary.
4. For classes spread across multiple files, read the most specific subclass header first.

---

## Scripting Language Reading Strategy

For projects that use a scripting layer (Lua, Python, JS, etc.) bridged to C++:

1. Start from the **entry script for the relevant subsystem** (not from a global scan).
2. For global context, read the global bootstrap or data-access script first
   (check `setup/scripting_patterns.md` for project-specific entry points).
3. Follow the **call chain from the entry point** rather than reading all scripts.
4. Do not scan all script files under a directory — always navigate by call chain.
