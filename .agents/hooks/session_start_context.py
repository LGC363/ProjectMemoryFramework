#!/usr/bin/env python3
"""
SessionStart Hook — Context Injection
======================================
Injects project context at the beginning of every new/resumed Kimi CLI session.
This script does NOT make decisions. It only presents facts and asks the Agent
to evaluate them.

Event:  SessionStart
Exit:   0 (always — this hook never blocks)
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
    catalog = os.path.join(cwd, ".agents", "catalog.yaml")

    if not os.path.exists(catalog):
        sys.exit(0)

    context = (
        "【PMF 上下文补充 — SessionStart】\n"
        f"当前工作目录：{cwd}\n"
        "检测到 .agents/catalog.yaml 存在，说明本项目已启用 ProjectMemoryFramework 业务记忆层。\n\n"
        "请根据 PMF 规则自行判断：\n"
        "  - 如果这是一个新的工作任务，请在工作前读取 AGENTS.md → .agents/index.md → 相关 modules/ → 相关 units/\n"
        "  - 如果你已经读取过这些文档且上下文仍然有效，可以直接继续工作\n"
        "  - 任务结束后，请在最终回复末尾追加 Memory status line\n"
    )
    print(context)
    sys.exit(0)


if __name__ == "__main__":
    main()
