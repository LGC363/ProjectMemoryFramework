# ProjectMemoryFramework — Agent 业务记忆层

## 核心原则：Agent 自决

PMF 的 hooks 和文档**只注入上下文（事实 + 规则），从不代替你做决定**。
所有判断（是否读取记忆、是否更新文档、是否需要更多上下文）都由你（Agent）自行决定。

## 工作流

### 1. 任务开始时

如果用户提交的是**开发/修改/实现/重构/添加/修复**类任务：
1. 读取 `.agents/index.md` — 了解项目子系统划分
2. 读取 `modules/` 下相关模块 — 了解系统行为、边界、关键入口
3. 读取 `units/` 下相关单元 — 了解实现细节、风险点
4. 如果涉及历史决策，读取 `demands/` 下相关需求

如果用户提交的是**查询/解释/总结**类任务：可以直接回答，但如果涉及代码，仍建议先读 index.md。

### 2. 修改代码时

- 遵循 `.agents/rules/` 下的编码规范
- 如果修改了业务代码，评估是否产生了新知识：
  - 模块职责或边界是否变化？
  - 关键入口或风险点是否变化？
  - 业务意图或架构决策是否变化？
- 如果是，任务结束后更新对应 memory 文档

### 3. 任务结束时

如果修改了业务代码，在最终回复末尾追加一行且仅一行：

```
Memory updated: module
Memory updated: unit
Memory updated: demand
Memory updated: module + unit
Memory updated: module + demand
Memory updated: demand + module; index synced
Memory updated: catalog only
No memory update needed
```

## 关键文件速查

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | 项目级 Agent 规则（Initialization Gate、Read Order） |
| `.agents/index.md` | 子系统目录和关联映射 |
| `.agents/modules/*.md` | 模块级行为、边界、关键入口 |
| `.agents/units/*.md` | 实现细节、风险点、常见修改模式 |
| `.agents/demands/*.md` | 需求历史、架构决策 |
| `.agents/rules/` | 编码规范、扫描规则、治理规则 |
| `.agents/setup/` | 项目配置（搜索范围、脚本模式、项目画像） |
| `.agents/catalog.yaml` | 所有 memory 文档的索引 |

## 重要约定

- **Code wins over docs**：代码是真相来源，文档落后于代码时，更新文档
- **Initialization Gate**：`setup/checklist.md` Part 1 通过后才算框架就绪
- **Memory Update 是强约定，非机械强制**：由于 LLM 输出不稳定，我们不拦截输出，但你有义务在最终回复中报告 Memory 状态
- **只有 Git pre-commit hook 是机械强制**：`validate_agents_health.py` 会在提交前检查文档完整性
