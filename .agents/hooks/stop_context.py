#!/usr/bin/env python3
"""
Stop Hook — Context Injection
==============================
At the end of each agent turn, injects a reminder to include a Memory
status line if business code was modified during the turn.

This hook does NOT track which files were modified (hook processes have
no shared state). It simply presents a reliable unconditional reminder.

Event:  Stop
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
        "【PMF】本轮即将结束。如果你修改了业务代码，请在最终回复末尾追加且仅追加一行 Memory status line。\n"
        "可选值：Memory updated: module / unit / demand / module + unit / module + demand / demand + module; index synced / catalog only / No memory update needed"
    )
    print(context)
    sys.exit(0)


if __name__ == "__main__":
    main()
