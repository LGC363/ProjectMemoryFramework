#!/usr/bin/env python3
"""PreToolUse (ReadFile) — Lightweight Init Gate check.
Checks only project_profile.md (1 file) to avoid slowdown when batch-reading memory docs.
Event: PreToolUse  Matcher: ReadFile  Exit: 0 (always)"""

import json, os, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

path = data.get("tool_input", {}).get("path", "")
if ".agents/" not in path.replace("\\", "/"):
    sys.exit(0)

cwd = data.get("cwd", os.getcwd())
profile = os.path.join(cwd, ".agents", "setup", "project_profile.md")

try:
    gate_ok = os.path.exists(profile) and "{PLACEHOLDER}" not in open(profile, "r", encoding="utf-8").read()
except Exception:
    gate_ok = False

if gate_ok:
    print("【PMF】你正在读取业务记忆文档。若尚未读取 index.md → modules → units，建议先读取。")
else:
    print("【PMF】你正在读取 .agents/ 下的文件，但框架 Initialization Gate 似乎尚未完成。\n"
          "请确认 setup/project_profile.md 已填写且无占位符。若已确认通过，可忽略此提醒。")

sys.exit(0)
