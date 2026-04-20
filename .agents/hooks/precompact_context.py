#!/usr/bin/env python3
"""
PreCompact Hook — Context Injection
====================================
When Kimi CLI is about to compact the session context, this script
injects a reminder that previously-read memory documents may be evicted.

The Agent decides whether to re-read critical documents.

Event:  PreCompact
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
        "【PMF 上下文补充 — PreCompact】\n"
        "会话上下文即将被压缩，之前读取的 .agents/ 文档可能从上下文中丢失。\n\n"
        "请根据当前工作需求自行判断：\n"
        "  - 如果接下来的工作仍需要参考已读取的 memory 文档，请在压缩完成后重新读取\n"
        "  - 读取顺序：.agents/index.md → modules/ → units/ → demands/\n"
        "  - 如果当前任务已接近尾声且不再需要这些文档，可以忽略此提醒\n"
    )
    print(context)
    sys.exit(0)


if __name__ == "__main__":
    main()
