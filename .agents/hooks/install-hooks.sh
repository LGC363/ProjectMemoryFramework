#!/usr/bin/env bash
# ProjectMemoryFramework — Kimi CLI Hook Installer (macOS / Linux)
# ================================================================
# Registers PMF context-injection hooks in ~/.kimi/config.toml.
# Uses ABSOLUTE paths so hooks work regardless of where Kimi CLI
# is launched from.
#
# Supports UPDATE mode: if an old PMF block exists, it is replaced
# rather than duplicated.
#
# These hooks inject *context* (facts + rules). They NEVER block.
# Agent makes all judgments.
#
# For Claude Code, hooks are project-level (.claude/settings.json).
# See INSTALL.md for Claude setup instructions.
#
# Usage:
#   bash .agents/hooks/install-hooks.sh

set -euo pipefail

# ------------------------------------------------------------------
# 1. Find Python
# ------------------------------------------------------------------
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" >/dev/null 2>&1; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[PMF] ERROR: No Python found. Please install Python 3."
    exit 1
fi

# ------------------------------------------------------------------
# 2. Resolve absolute paths to hook scripts
# ------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

abs_path() {
    local p="${SCRIPT_DIR}/$1"
    if [ ! -f "$p" ]; then
        echo "[PMF] ERROR: Hook script not found: $p"
        exit 1
    fi
    echo "$p"
}

SESSION_START=$(abs_path "session_start_context.py")
PROMPT_SUBMIT=$(abs_path "prompt_submit_context.py")
PRE_TOOL_USE=$(abs_path "pretooluse_context.py")
POST_TOOL_USE=$(abs_path "posttooluse_context.py")
STOP_HOOK=$(abs_path "stop_context.py")
PRE_COMPACT=$(abs_path "precompact_context.py")

TODAY=$(date +%Y-%m-%d)

# ------------------------------------------------------------------
# 3. Build config block (with absolute paths)
# ------------------------------------------------------------------
# Use printf to avoid quoting issues with single quotes inside single quotes
HOOK_BLOCK=$(cat <<EOF

# === ProjectMemoryFramework Context-Injection Hooks (auto-installed) ===
# These hooks inject context (facts + rules) into the agent context.
# They NEVER block. Agent makes all judgments.
# Updated: ${TODAY}

[[hooks]]
event = "SessionStart"
command = "${PYTHON} ${SESSION_START}"
timeout = 5

[[hooks]]
event = "UserPromptSubmit"
command = "${PYTHON} ${PROMPT_SUBMIT}"
timeout = 5

[[hooks]]
event = "PreToolUse"
matcher = "ReadFile"
command = "${PYTHON} ${PRE_TOOL_USE}"
timeout = 5

[[hooks]]
event = "PostToolUse"
matcher = "WriteFile|StrReplaceFile"
command = "${PYTHON} ${POST_TOOL_USE}"
timeout = 5

[[hooks]]
event = "Stop"
command = "${PYTHON} ${STOP_HOOK}"
timeout = 5

[[hooks]]
event = "PreCompact"
command = "${PYTHON} ${PRE_COMPACT}"
timeout = 5
# === End PMF Hooks ===
EOF
)

# ------------------------------------------------------------------
# 4. Write to ~/.kimi/config.toml (with update support)
# ------------------------------------------------------------------
CONFIG_DIR="${HOME}/.kimi"
CONFIG_FILE="${CONFIG_DIR}/config.toml"

mkdir -p "${CONFIG_DIR}"

if [ -f "${CONFIG_FILE}" ]; then
    # Remove any existing PMF block, then append new one
    awk '
        /# === ProjectMemoryFramework.*Hooks/ {skip=1; next}
        /# === End PMF Hooks/ {skip=0; next}
        !skip {print}
    ' "${CONFIG_FILE}" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "${CONFIG_FILE}"
    echo "${HOOK_BLOCK}" >> "${CONFIG_FILE}"
else
    echo "${HOOK_BLOCK}" > "${CONFIG_FILE}"
fi

# ------------------------------------------------------------------
# 5. Verify
# ------------------------------------------------------------------
if ! grep -q "session_start_context.py" "${CONFIG_FILE}"; then
    echo "[PMF] ERROR: Verification failed — hooks not written correctly."
    exit 1
fi

echo "[PMF] Kimi CLI context-injection hooks installed to ${CONFIG_FILE}"
echo "[PMF] Paths are ABSOLUTE — works from any working directory."
echo "[PMF] These hooks inject FACTS and RULES. Agent makes all judgments."
echo "[PMF] Restart Kimi CLI sessions for changes to take effect."
echo "[PMF] For Claude Code, copy .claude/ to your project root (see INSTALL.md)."
