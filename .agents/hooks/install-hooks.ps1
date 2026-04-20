# ProjectMemoryFramework — Kimi CLI Hook Installer (Windows)
# ============================================================
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
#   .agents\hooks\install-hooks.ps1

$ErrorActionPreference = "Stop"

# ------------------------------------------------------------------
# 1. Find Python
# ------------------------------------------------------------------
$PYTHON = $null
foreach ($cmd in @("python3", "python", "py")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $PYTHON = $cmd
        break
    }
}
if (-not $PYTHON) {
    Write-Host "[PMF] ERROR: No Python found. Please install Python 3." -ForegroundColor Red
    exit 1
}

# ------------------------------------------------------------------
# 2. Resolve absolute paths to hook scripts
# ------------------------------------------------------------------
$scriptDir  = $PSScriptRoot                    # e.g., C:\Project\.agents\hooks
$projectRoot = Split-Path $scriptDir -Parent   # e.g., C:\Project\.agents
$projectRoot = Split-Path $projectRoot -Parent # e.g., C:\Project

function AbsPath($name) {
    $p = Join-Path $scriptDir $name
    if (-not (Test-Path $p)) {
        Write-Host "[PMF] ERROR: Hook script not found: $p" -ForegroundColor Red
        exit 1
    }
    # Normalize to forward slashes for TOML compatibility
    return $p.Replace('\', '/')
}

$sessionStart   = AbsPath "session_start_context.py"
$promptSubmit   = AbsPath "prompt_submit_context.py"
$preToolUse     = AbsPath "pretooluse_context.py"
$postToolUse    = AbsPath "posttooluse_context.py"
$stopHook       = AbsPath "stop_context.py"
$preCompact     = AbsPath "precompact_context.py"

# ------------------------------------------------------------------
# 3. Build config block (with absolute paths)
# ------------------------------------------------------------------
$hookBlock = @"

# === ProjectMemoryFramework Context-Injection Hooks (auto-installed) ===
# These hooks inject context (facts + rules) into the agent's context.
# They NEVER block. Agent makes all judgments.
# Updated: $(Get-Date -Format "yyyy-MM-dd")

[[hooks]]
event = "SessionStart"
command = "$PYTHON \`"$sessionStart\`""
timeout = 5

[[hooks]]
event = "UserPromptSubmit"
command = "$PYTHON \`"$promptSubmit\`""
timeout = 5

[[hooks]]
event = "PreToolUse"
matcher = "ReadFile"
command = "$PYTHON \`"$preToolUse\`""
timeout = 5

[[hooks]]
event = "PostToolUse"
matcher = "WriteFile|StrReplaceFile"
command = "$PYTHON \`"$postToolUse\`""
timeout = 5

[[hooks]]
event = "Stop"
command = "$PYTHON \`"$stopHook\`""
timeout = 5

[[hooks]]
event = "PreCompact"
command = "$PYTHON \`"$preCompact\`""
timeout = 5
# === End PMF Hooks ===
"@

# ------------------------------------------------------------------
# 4. Write to ~/.kimi/config.toml (with update support)
# ------------------------------------------------------------------
$configDir  = Join-Path $env:USERPROFILE ".kimi"
$configFile = Join-Path $configDir "config.toml"

if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

if (Test-Path $configFile) {
    $content = Get-Content $configFile -Raw -Encoding UTF8
    # Remove any existing PMF block (match from ProjectMemoryFramework to End PMF Hooks)
    $content = [regex]::Replace($content, "(?s)\r?\n# === ProjectMemoryFramework.*?# === End PMF Hooks.*?\r?\n?", "")
    $content = $content.TrimEnd()
    Set-Content -Path $configFile -Value ($content + $hookBlock) -Encoding UTF8 -NoNewline
    # Ensure trailing newline
    Add-Content -Path $configFile -Value "" -Encoding UTF8
} else {
    Set-Content -Path $configFile -Value $hookBlock.Trim() -Encoding UTF8
}

# ------------------------------------------------------------------
# 5. Verify
# ------------------------------------------------------------------
$verify = Get-Content $configFile -Raw -Encoding UTF8
if ($verify -notmatch "session_start_context.py") {
    Write-Host "[PMF] ERROR: Verification failed — hooks not written correctly." -ForegroundColor Red
    exit 1
}

Write-Host "[PMF] Kimi CLI context-injection hooks installed to $configFile" -ForegroundColor Green
Write-Host "[PMF] Paths are ABSOLUTE - works from any working directory." -ForegroundColor Green
Write-Host "[PMF] These hooks inject FACTS and RULES. Agent makes all judgments." -ForegroundColor Cyan
Write-Host "[PMF] Restart Kimi CLI sessions for changes to take effect." -ForegroundColor Cyan
Write-Host "[PMF] For Claude Code, copy .claude/ to your project root (see INSTALL.md)." -ForegroundColor Cyan

exit 0
