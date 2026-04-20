#!/usr/bin/env python3
"""
PostToolUse Hook — Context Injection
=====================================
When the agent modifies a file, this script injects the file path and
asks the Agent to evaluate whether the change created new knowledge
worth recording.

This script does NOT classify the file. It only presents the path.

Event:   PostToolUse
Matcher: WriteFile | StrReplaceFile
Exit:    0 (always)
"""

import json
import os
import sys


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", tool_input.get("path", ""))
    cwd = data.get("cwd", os.getcwd())

    norm = file_path.replace("\\", "/")

    if ".agents/" in norm:
        sys.exit(0)

    if not os.path.exists(os.path.join(cwd, ".agents", "catalog.yaml")):
        sys.exit(0)

    context = (
        "【PMF 上下文补充 — PostToolUse】\n"
        f"你刚刚修改了文件：{file_path}\n\n"
        "请根据 PMF 规则自行判断：\n"
        "  1. 这是否是一个业务源代码文件（非 .agents/ 下的文档）？\n"
        "  2. 本次修改是否产生了值得记录的新知识？例如：\n"
        "     - 模块职责或边界是否变化？\n"
        "     - 关键入口或风险点是否变化？\n"
        "     - 业务意图或架构决策是否变化？\n"
        "  3. 如果是，请在完成任务后更新 modules/ / units/ / demands/ 文档，\n"
        "     并运行 python .agents/tools/sync-catalog.py\n"
        "  4. 如果没有任何新知识产生，请在最终回复中写：No memory update needed\n"
    )
    print(context)
    sys.exit(0)


if __name__ == "__main__":
    main()
