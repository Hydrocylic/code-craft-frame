# 设计决策记录

> 区域: explore（探讨区）
> 框架版本: v2.0
> 最后更新: 2026-08-07

---

## 决策 1: 采用三类型体系而非两类型

**日期**: 2026-07-28 (v1.1)，确认于 2026-08-07 (v2.0)

**背景**: _framework1 和 _framework2 使用 learning/practice 两类型。实践中 learning 和 practice 的边界经常模糊，FAQ 中出现"优先选 practice"的变通建议。

**决策**: 采用 reference/reconstruction/product 三类型

**理由**:
- 三类型形成了可操作的学习→输出链：阅读 → 拆解 → 产出
- 每种类型的目录结构、笔记方式、完成标志明确不同
- 类型转换规则使体系更灵活
- 去掉了 learning/practice 的语义模糊

**代价**: 比两类型复杂，新用户需要时间理解三种类型的差异

---

## 决策 2: 项目内笔记自包含

**日期**: 2026-08-07 (v2.0)

**背景**: _framework1 曾将实践项目的代码和笔记分置于 `practices/` 和 `notes/practices/`，_framework3 将笔记放回项目内。

**决策**: 所有笔记在项目内自包含

**理由**:
- 跨目录维护增加操作负担
- 项目自包含使迁移、归档更简单
- 三种类型的笔记形式自然不同，放在项目内更易理解

**折中**: product 类型如需代码仓库纯净，可将详细迭代笔记外置到全局 `notes/` 区

---

## 决策 3: 模板语言无关化

**日期**: 2026-07-25 (v1.0 cpp-lab)，确认于 2026-08-07 (v2.0)

**背景**: _framework1 的模板包含 Python/PyTorch 特化内容，迁移到 C++ 仓库时需要批量修改。

**决策**: 所有模板使用通用占位符（`<language>`, `<run-command>`），不出现特定语言/框架名称

**理由**:
- 框架已证明适用于 Python（AI/ML）和 C++ 两种场景
- 占位符方案清晰，不会误以为是"缺失"了具体名称

---

## 决策 4: envs/ 同时支持脚本型和编译型

**日期**: 2026-08-07 (v2.0)

**背景**: _framework1 的 envs/ 面向 Python（scripts/, .env.template, requirements-*.txt），_framework2/3 面向 C++（build-templates/）。统一框架需要兼顾。

**决策**: envs/ 同时包含 scripts/、.env.template、<build-templates>/ 的骨架

**理由**:
- 不同技术栈的需求不同，不能强制一种
- 提供骨架不增成本，但单方面简化会丢失信息
- 用户按需填充，不需要的目录可以留空

---

## 决策 5: 引入 spec/ 和 explore/ 双区

**日期**: 2026-08-07 (v2.0)

**背景**: 框架在前三个版本中没有自我记录机制。框架设计中的思考、取舍、局限性分散在 CHANGELOG、头脑中或丢失了。

**决策**: 在 `_framework/notes/` 下建立规范区（spec）和探讨区（explore）

**理由**:
- spec 区的写入是严肃的，需要同步更新 FRAMEWORK.md 和 CHANGELOG
- explore 区的写入是开放的，鼓励反思和记录，不强制同步
- 双区分离使框架既有稳定性又有反思空间

---

## 决策 6: 结构调整的克制原则

**日期**: 2026-08-07 (v2.0)

**背景**: 框架涉及大量结构性操作——目录重组、文件迁移、项目类型转换、模板复制。前三个版本中，这些操作的"自动化程度"没有明确边界：MANUAL.md 中写流程步骤、conversion.md 中写"可由 agent 辅助执行"，容易导致 agent 在一次对话中输出大量文件变更而不经用户审核。

**决策**: 将"结构调整克制先行"提升为框架核心信念（FRAMEWORK.md §一 第 6 条），并在所有相关文件中注入约束：

1. FRAMEWORK.md §一 — 新增"结构调整原则"小节，定义四步流程（审计→提案→确认→执行）
2. MANUAL.md — 新增"结构调整总则"节，区分"结构调整(4a)"和"内容生成(4b)"
3. 所有 conversion.md — 添加克制前言，声明 Agent 默认只到 Phase 2
4. templates/CLAUDE.md — 新增"Agent 行为约束"节，5 条具体规则

**理由**:
- 结构调整（移动文件）影响整个仓库的导航和引用关系，用户需要机会审核
- 内容生成（写笔记）创造知识资产，不应该由 agent 单方面决定
- "出方案—等确认—再动手"的流程在用户和 agent 之间建立了清晰的决策权边界
- 不这样做的话，agent 一次操作可能产生大量需要 undo 的变更

**影响**:
- agent 在面对结构调整指令时，默认行为从"执行"变为"出报告"
- 批量内容生成（如一次创建所有轮次的 notes.md）被明确禁止
- 用户始终保留对结构和内容两方面的最终决定权

---

## 决策 7: 参考项目不包含笔记

**日期**: 2026-08-08

**背景**: v2.0 的 reference SKELETON 包含 `notes/` 目录，用于存放对参考源码的分析笔记。在 ai-lab 工作区结构调整实践中发现：分析笔记天然服务于"拆解学习"这个动作，归属到 reconstruction 项目的 curriculum 中更自然。而在 reference 中维护 notes/ 导致同一份代码的笔记可能分散在 reference 和 projects 两处。

**决策**: reference 类型不再包含 `notes/` 目录。目录极简化为：源码 + README.md + meta.yaml + (可选) RESOURCES.md。

**理由**:
- 分析笔记服务于"拆解学习"，属于 reconstruction 项目，通过 `code-refs.md` 建立代码映射
- reference 保持源码级纯净，可被多个 reconstruction 项目复用，避免笔记冲突
- 减少跨目录维护负担

**影响**:
- reference SKELETON.md 重写，不再包含 notes/
- meta.yaml 的 `notes:` 字段对 reference 类型不再适用
- MANUAL.md 创建 reference 步骤简化
- 现有 reference 的 notes/ 可迁移到对应 reconstruction 项目的 curriculum 中
