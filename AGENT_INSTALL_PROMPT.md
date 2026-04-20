# ProjectMemoryFramework — Agent Self-Installation Prompt

Copy and paste the following prompt into any agent (Kimi Code CLI, Claude Code, Cursor, etc.) to install PMF into the current project.

---

## Prompt

```text
请为当前项目安装并初始化 ProjectMemoryFramework（PMF）业务记忆框架。

你的工作：
1. 扫描项目结构，理解项目类型和技术栈
2. 将 PMF 框架文件复制/合并到当前项目
3. 完成 Smart Setup（自动推断项目信息 + 填充模板）
4. 根据你所在的 Agent 平台安装 Guidance Layer
5. 运行 Initialization Gate 验证
6. 运行 Initialization Gate 验证并逐项确认

在 Gate 完全通过之前，不要开始任何项目业务工作。

---

### Step 0 — 复制框架文件

将 PMF 包中的以下内容复制到当前项目根目录：
- `.agents/` 目录（完整复制，保留所有子目录）
- `AGENTS.md`：
  - 如果当前项目已有 `AGENTS.md`，将 PMF 的 `AGENTS.md` 中 `# Agent Business Memory Layer` 以下的内容追加到现有文件末尾
  - 如果当前项目没有 `AGENTS.md`，直接复制 PMF 的 `AGENTS.md`

复制后的项目根目录应包含：
```
YourProject/
├── AGENTS.md
└── .agents/
    ├── index.md
    ├── catalog.yaml
    ├── rules/
    ├── setup/
    ├── templates/
    ├── hooks/
    ├── modules/
    ├── units/
    └── demands/
```

---

### Step 1 — Smart Setup（自动推断）

读取 `.agents/setup/checklist.md` Part 1，按顺序完成以下步骤。
每个 setup 文件应从项目实际结构中推断信息，不要留空或保留占位符。

**Step 1.1 — project_profile.md**
- 读取项目根目录下的 `.uproject` / `.sln` / `package.json` / `Cargo.toml` / `pom.xml` / `CMakeLists.txt` 等文件
- 推断：项目名称、引擎/框架版本、版本控制系统、主要编程语言
- 写入 `.agents/setup/project_profile.md`（基于 `setup/project_profile.template.md`）
- **标准**：文件中不能包含 `{PLACEHOLDER}` 或 `{PROJECT_NAME}`

**Step 1.2 — code_style_baseline.md 的 Auto-Generated Files**
- 扫描项目，列出所有由代码生成工具/构建管线拥有的目录
- 常见例子：`Intermediate/`、`DerivedDataCache/`、`Binaries/`、`node_modules/`、`target/`、`.vs/`、`.idea/`
- 填入 `.agents/rules/code_style_baseline.md` 的 "Auto-Generated Files" 章节
- **标准**：每个目录都要标明生成工具名称

**Step 1.3 — search_scope.md**
- 扫描项目目录结构（重点是 `Source/`、`src/`、`Content/`、`assets/`、`Scripts/` 等）
- **Tier 1**：日常工作的目录（核心源码、主要脚本）
- **Tier 2**：辅助目录（第三方库、配置、测试）
- **Never-scan**：不需要搜索的目录（构建输出、缓存、版本控制元数据）
- 写入 `.agents/setup/search_scope.md`（基于 `setup/search_scope.template.md`）
- 如果某项是推断的，标记 `<!-- Auto-inferred: verify -->`
- **标准**：文件中不能包含 `{PLACEHOLDER}`

**Step 1.4 — scripting_patterns.md**
- 如果项目使用脚本层（Lua / Python / JS / C# / 其他）：
  - 扫描脚本文件，推断基类名、常见导入路径、数据访问模式
  - 写入 `.agents/setup/scripting_patterns.md`
  - 不确定的项标记 `<!-- TODO: verify -->`
- 如果项目**没有**脚本层：
  - 创建 `.agents/setup/scripting_patterns.md`，内容仅为：
    ```
    # Scripting Integration Patterns
    N/A — this project has no scripting bridge layer.
    ```
- **标准**：存在且有内容，或明确标记 N/A

**Step 1.5 — index.md**
- 从项目目录结构推断主要子系统名称
- 替换 `.agents/index.md` 中的 `{Subsystem 1}`、`{Subsystem 2}` 等占位符
- module/unit 条目留空（随工作进展积累）
- **标准**：文件中不能包含 `{Subsystem` 字符串

**Step 1.6 — catalog.yaml**
- 将 `updated_at` 设置为今天的日期（格式 `YYYY-MM-DD`）
- 将 `areas` 列表填入实际子系统代码（从 index.md 的子系统名缩写而来）
- `documents` 保持为空列表
- **标准**：日期不是占位符，`areas` 非空

---

### Step 2 — 安装 Guidance Layer（平台分支）

根据你当前运行的 Agent 平台，执行对应的安装步骤：

**如果你运行在 Kimi Code CLI：**
```bash
# Windows (PowerShell)
.agents\hooks\install-hooks.ps1

# macOS / Linux
bash .agents/hooks/install-hooks.sh
```
安装完成后，运行 `/hooks` 命令确认 6 个 hooks 已配置。

**如果你运行在 Claude Code：**
确认 `.claude/` 目录已存在于项目根目录（应在 Step 0 中已复制）。
检查 `.claude/settings.json` 和 `.claude/CLAUDE.md` 存在即可。
无需额外安装 — Claude Code 会自动读取项目级的 `.claude/settings.json`。

**如果你运行在 Cursor 或其他不支持 lifecycle hooks 的平台：**
- 复制 `.agents/setup/CURSOR.template.md` → 项目根目录 `.cursorrules`
- 填入项目特定的 IntelliSense 根路径等信息

---

### Step 3 — Initialization Gate 验证

框架**只有在以下 6 个条件全部满足时才算真正激活**。
请逐项检查，在最终回复中以表格形式报告结果。

| # | 条件 | 你的检查结果 |
|---|---|---|
| 1 | `.agents/setup/project_profile.md` 存在且无 `{PLACEHOLDER}` | 通过 / 未通过 |
| 2 | `.agents/setup/search_scope.md` 存在且无 `{PLACEHOLDER}` | 通过 / 未通过 |
| 3 | `.agents/setup/scripting_patterns.md` 存在或明确标记 N/A | 通过 / 未通过 |
| 4 | `.agents/index.md` 无 `{Subsystem N}` 占位符 | 通过 / 未通过 |
| 5 | `.agents/catalog.yaml` 有真实 `updated_at` 日期且 `areas` 非空 | 通过 / 未通过 |
| 6 | Guidance Layer 已安装（Kimi hooks / Claude config / Cursor rules）| 通过 / 未通过 |

**如果任何一项未通过，列出具体原因和修复步骤。不要开始项目业务工作。**

---

### 完成报告格式

请在最终回复中使用以下格式：

```
## PMF 安装报告

### 项目概况
- 项目类型：xxx
- 引擎/框架：xxx
- 主要语言：xxx
- 子系统数量：x

### Initialization Gate
| # | 条件 | 状态 |
|---|---|---|
| ... | ... | 通过 / 未通过 |

### 平台配置
- Agent 平台：Kimi CLI / Claude Code / Cursor / 其他
- Guidance Layer：已安装 / 未安装

### 说明
[如果有未通过的项，写在这里；如果全部通过，写 "Gate 已通过，框架已激活，可以开始工作。"]
```
```

---

## Notes for Human Users

- **One-shot usage**: Copy the prompt block above and paste it into your agent.
- **Before pasting**: Ensure the PMF package (`.agents/` + `AGENTS.md`) is already copied into the target project.
- **After installation**: Review the agent's Gate report. If any condition is unmet, ask the agent to fix it before proceeding.
- **Multi-platform teams**: Kimi CLI hooks are per-user (`~/.kimi/config.toml`); Claude Code config is project-level (`.claude/settings.json`, commitable). Both can coexist in the same repo.
