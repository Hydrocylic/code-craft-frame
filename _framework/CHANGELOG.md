# 框架变更日志

> 每条记录包含日期、类型、内容和影响范围
> 类型: rule-add | rule-change | template-add | template-update | private-promote | structure

---

## 2026-08-10 — v2.1: product 项目任务笔记系统 + 代码品读分类体系

**类型**: rule-add + template-add + spec-add + structure

**变更内容**:

**1. 新增 spec 规范文档（2 个）**:
- `notes/spec/task-note-system.md` — 任务三元组规范（plan→log→code-review），含追加式日志、Bug 内嵌时间线、issues 分流、knowledge-base 管理、定期整理工作流、格式约定、Agent 行为指引
- `notes/spec/code-review-classification.md` — T1–T7 分类路由表，含各类型详细说明、T1 迁移流程、核心原则

**2. 新增模板（2 个）**:
- `templates/task-plan.md` — 任务计划模板（目标/数据流/实现设计/附录）
- `templates/task-log.md` — 执行日志模板（时间戳条目/Bug 格式/产生文件表）

**3. 升级 product SKELETON**:
- `docs/` 从三文件（architecture/changelog/design-decisions）升级为任务笔记系统结构：
  - `docs/README.md`（推荐）— 文档系统自身说明
  - `docs/overview/` — project-intro, milestones, structure-changes
  - `docs/tasks/` — ★ 任务三元组（plan/log/code-review）
  - `docs/issues.md`（★ 标配）— IS-XXX + 🔴🟡🟢 优先级
  - `docs/knowledge-base.md`（推荐）— QA 格式，单体不拆分
  - `docs/decisions.md`（推荐）— ADR 风格
- 新增"任务笔记系统"节，描述工作流和配套文件
- 更新与 reconstruction 的对比表
- 迭代记录（`notes/iterations/`）保留，与 tasks/ 互补

**4. 更新 FRAMEWORK.md §二**:
- 同步 product 的 `docs/` 目录结构

**5. 更新 templates/CLAUDE.md**:
- 新增"项目特定规则"节（9 条）：代码保守/笔记丰富/规划先行/不主动指令/时间戳/日志追加/代码品读 T1–T7/知识粗糙积累/问题分流
- 保留"结构调整"子节（3 条）

**6. 更新 explore/ 探讨区**:
- `adjustable-items.md` 新增条目 10：knowledge-base.md 适用范围 — product 推荐使用，reconstruction 用轮次 QA

**7. 更新 spec/ 规范区**:
- `template-spec.md` 模板完整性表新增 task-plan.md (#11) 和 task-log.md (#12)

**设计原则**:
- product 项目：任务笔记系统偏强制性（标配 issues.md、强制 tasks/ 三元组、推荐 knowledge-base.md）
- reconstruction 项目：推荐采用，不强制替代现有 curriculum 体系
- reference / practice 项目：不适用

**来源**: virtual-human (products/virtual-human) 项目实践反馈至上游框架

**影响范围**:
- 新 product 项目直接使用新的 docs/ 结构
- 现有 product 项目的 `docs/architecture.md`、`docs/changelog.md`、`docs/design-decisions.md` 可重新分布到新结构中（architecture→overview/project-intro, changelog→overview/milestones, design-decisions→decisions.md）
- reconstruction 项目可选升级，无强制迁移要求
- CLAUDE.md 实例（使用本模板的仓库）建议同步更新"项目特定规则"节

---

## 2026-08-07 — v2.0: 三版本统一

**类型**: structure + rule-change

**变更内容**:
- 融合 _framework1 (AI-LAB v1.0)、_framework2 (cpp-lab v1.0)、_framework3 (v1.1) 的设计
- 保留三类型体系 (reference / reconstruction / product) — 来自 _framework3 v1.1
- 保留语言无关模板 — 来自 _framework2/3
- 环境管理支持编译型和脚本型两种技术栈 — 融合 _framework1 + _framework2/3
- 恢复远程运行支持指导 — 来自 _framework1
- 新增 §十一 "框架自身的规范与探讨" — 新增 spec/explore 双区
- 新增 `_framework/notes/` 目录（规范区 + 探讨区）
- FRAMEWORK.md 从 10 节扩展为 11 节
- MANUAL.md 更新为三类型系统，新增 FAQ 条目（环境配置、远程运行）

**影响范围**:
- 现有使用旧版 _framework/ 的仓库可按需升级
- 升级时需检查: meta.yaml 的 type 字段、目录结构、项目类型的调整
- _framework1/2/3 保留作为历史参考，不再更新

**来源**:
- 分析笔记见仓库根目录 `notes/analysis/`

---

## 2026-07-28 — v1.1: 项目类型体系重构

**类型**: rule-change + template-update

**变更内容**:
- 将原有两类型体系（learning / practice）重构为三类型体系（reference / reconstruction / product）
- 新增 `_framework/project-types/` 目录，包含三种类型的 SKELETON.md 和 conversion.md
- FRAMEWORK.md §二 目录结构中 `practices/` 替换为 `products/`，`projects/` 定位为 reconstruction
- FRAMEWORK.md §三 完全重写，描述三种类型及其对比
- MANUAL.md 更新项目创建步骤，新增"项目类型转换"节
- 更新 `templates/meta.yaml` — type 字段改为 `reference | reconstruction | product`

**影响范围**:
- 现有 `projects/` 下的项目如原 type 为 `learning`，需更新为 `reconstruction`
- 现有 `practices/` 目录如存在，需迁移到 `products/` 或 `projects/`（按实际定位）
- 新项目直接使用新类型标识

---

## 2026-07-25 — cpp-lab 仓库初始化

**类型**: structure

**变更内容**:
- 从 AI/ML 学习仓库迁移框架至 C++ 学习仓库
- 建立完整的目录结构：`reference/`、`projects/`、`notes/`、`envs/`
- 创建 .gitignore、README.md、envs/ 环境配置骨架

**影响范围**:
- 框架的跨语言适用性得到验证

---

## 2026-07-25 — 模板语言无关化

**类型**: template-update

**变更内容**:
- 移除所有模板中 Python/PyTorch/AI-ML 特化内容
- 代码块 `python` → `<language>` 占位符
- 运行命令 `python ...` → `<run-command>` 占位符
- 参数示例 → 通用占位符
- FRAMEWORK.md 和 MANUAL.md 中移除 AI/ML 术语、GPU/CUDA 引用、pip/conda/venv 引用

**影响范围**:
- `_framework/` 现在可跨语言复制使用

---

## 2026-07-26 — 实践项目代码与笔记分离

**类型**: rule-change | structure

**变更内容**:
- 实践项目的课程笔记 (`curriculum/`) 和简历 (`resume/`) 从 `practices/<name>/` 移至 `notes/practices/<name>/`
- `practices/<name>/` 现在仅保留代码相关内容
- 此变更后被 v1.1 的三类型体系替代

**影响范围**:
- 仅影响 v1.0 中使用 practices/ 的仓库

---

## 2026-07-23 — 初始框架建立

**类型**: structure

**变更内容**:
- 建立 `_framework/` 元框架目录
- 编写 `FRAMEWORK.md`（方法论）和 `MANUAL.md`（使用手册）
- 创建 8 个模板文件
- 定义目录结构规范、项目类型、轮次机制、实验规范、简历规范
- 定义共有/私有规则区分及提升机制
- 定义时间戳和版本管理规范

**影响范围**:
- 第一个学习仓库建立

---

## 2026-08-07 — rule-add: 提案落盘原则 + 慎用 --recursive

**类型**: rule-add

**变更内容**:
- FRAMEWORK.md §一 核心约束新增：**提案落盘为笔记** — Phase 2 调整方案以 `.md` 笔记写入被分析的工作区
- MANUAL.md §结构调整总则：Phase 2 输出描述更新；Agent 行为约束新增第 2 条"提案落盘"（5 条 → 6 条）
- MANUAL.md §Git Submodule 管理注意事项新增：**慎用 `--recursive`** — 参考项目的嵌套子模块不应被递归拉取

**来源**: cpp-lab 实例化 v2.0 过程中发现并验证，回馈至上游框架

**影响范围**:
- Agent 在结构调整时，Phase 2 的输出从"会话文本"变为"工作区中的 `.md` 笔记文件"
- 提案笔记成为仓库历史的一部分，可被 git 追踪、后续查阅和审计
- 子模块操作指南更安全，避免递归拉取无关依赖

---

---

## 2026-08-08 — rule-change: 参考项目不再包含 notes/ 目录

**类型**: rule-change + structure

**变更内容**:
- reference 类型项目移除 `notes/` 目录。分析笔记归属到 reconstruction 项目的 curriculum 中，通过 `code-refs.md` 建立映射
- FRAMEWORK.md §二 目录结构中 reference 移除 notes/
- FRAMEWORK.md §三 reference 特征描述更新：从"笔记在项目内"改为"不含 notes/"
- FRAMEWORK.md §三 类型对比表更新：reference 笔记系统为"无"
- reference SKELETON.md 完全重写 — 移除 notes/，新增"如何使用参考项目"指引
- reference conversion.md 更新 — 移除所有"从 notes/ 迁移"相关描述
- MANUAL.md 创建参考项目步骤更新 — 不创建 notes/，不复制 concept-note.md
- 新增 RESOURCES.md 作为 reference 的可选组件，记录外部资源获取方式

**影响范围**:
- 现有 reference/ 项目如有 notes/：建议将笔记内容迁移到对应的 reconstruction 项目 curriculum 中，或提升为跨项目概念笔记放入 notes/concepts/
- 新 reference 项目直接使用新骨架
- meta.yaml 的 `notes:` 字段对 reference 类型不再适用

**来源**: ai-lab 工作区结构调整反馈

---

## 模板文件

<!-- 后续变更在此行之上添加 -->

---

## 2026-08-08 — rule-add: 数学公式必须使用 LaTeX 语法

**类型**: rule-add + spec-update

**变更内容**:
- 新增 `_framework/notes/spec/template-spec.md` §数学公式书写规范
- 所有笔记中的数学讨论必须使用 `$...$`（行内）和 `$$...$$`（独立公式）
- 矩阵、求和、多行推导等数学结构使用标准 LaTeX 环境（`pmatrix`, `aligned` 等）
- 禁止 ASCII 艺术拼接矩阵、禁止纯文本代码块写数学公式
- 适用范围：所有项目类型（practice / reference / reconstruction / product）

**来源**: cpp-lab LeetCodePractice/70.md 的数学内容整理实践

**影响范围**:
- 新笔记直接适用 LaTeX 规范
- 已有笔记中的 ASCII 数学图示可逐步迁移为 LaTeX

---

## 2026-08-07 — rule-add: 新增 practice 项目类型（轻量刷题模式）

**类型**: rule-add + template-add + structure

**变更内容**:
- 新增第四种项目类型 **practice**（练习/刷题），面向高频轻量的单文件日常刷题场景
- 新增 `project-types/practice/SKELETON.md` — 描述单文件 + 单笔记的轻量模式
- 新增 `project-types/practice/conversion.md` — practice → reconstruction/product 转换规则
- 新增 `templates/practice-note.md` — 刷题讨论笔记模板
- 更新 `project-types/README.md` — 四种类型体系
- Practice 特征：一题双文件（`.cpp` 三位一体 + `.md` 思路探讨），扁平目录，题号命名

**来源**: cpp-lab LeetCodePractice 轻量化设计实践，回馈至上游框架

**影响范围**:
- 新练习目录可直接采用 practice 骨架规范
- 现有扁平 `.cpp` 练习目录可按 conversion.md 逐步迁移
- 框架项目类型从三种扩展为四种
