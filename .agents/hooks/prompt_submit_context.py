#!/usr/bin/env python3
"""
UserPromptSubmit Hook — Context Injection
==========================================
When the user submits a prompt, injects a concise reminder to judge
whether this is a dev task that requires reading memory first.

This script does NOT echo the user's prompt (the agent already sees it).
It only injects the rules, letting the Agent make the judgment.

Event:  UserPromptSubmit
Exit:   0 (always)
"""

import json
import os
import sys


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    cwd = data.get("cwd", os.getcwd())

    if not os.path.exists(os.path.join(cwd, ".agents", "catalog.yaml")):
        sys.exit(0)

    context = (
        "【PMF】用户提交了新需求。请判断是否为开发/修改/实现/重构/添加/修复类任务。\n"
        "若是，请先读取 .agents/index.md 定位相关子系统，再读取 modules/ 和 units/ 文档。"
    )
    print(context)
    sys.exit(0)


if __name__ == "__main__":
    main()
