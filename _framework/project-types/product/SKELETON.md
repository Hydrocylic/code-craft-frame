# 产出项目（产品项目）目录骨架

> 类型标识: `type: product`
> 框架版本: v2.0

---

## 定位

**产出完备的产品代码**，供开源、应用和展示。

- 结构设计反复重构调整以达到产品级质量
- 代码版本通过笔记系统保留（changelog + 架构文档）
- 展示整洁，面向最终用户和评审者
- 不需要 curriculum 轮次（那是学习过程的产物）

---

## 目录结构

```
products/<name>/
├── README.md                    # 项目介绍、快速开始、使用文档
├── LICENSE                      # 开源许可证
├── meta.yaml                    # type: product
├── CMakeLists.txt               # 构建入口

├── src/                         # ★ 产品源码
│   ├── include/                 #   公共头文件
│   └── *.cpp                    #   实现文件

├── shaders/                     # 着色器（图形学项目适用）
├── resources/                   # 资产（可提交或 gitignored，视大小而定）
├── samples/                     # 代码案例（可选，进 git；与条目/媒体同 slug 对齐，随离线打包交付）

├── docs/                        # ★ 任务笔记系统（日常主战场）
│   ├── README.md                #   文档系统自身的结构设计 + 使用规则（推荐）
│   ├── overview/                #   宏观架构（给外部人员介绍项目用）
│   │   ├── project-intro.md     #     项目定位、技术栈、功能边界
│   │   ├── milestones.md        #     里程碑 + 各阶段任务清单
│   │   └── structure-changes.md #     历次结构调整记录
│   ├── tasks/                   #   ★ 任务执行单元
│   │   ├── {name}-plan.md       #     任务计划（要做什么 + 设计调研）
│   │   ├── {name}-log.md        #     执行日志（实际做了什么 + Bug）
│   │   └── {name}-code-review.md #    代码品读（复盘质询，标注 T1–T7）
│   ├── issues.md                #   非主线问题追踪（IS-XXX 编号）
│   ├── knowledge-base.md        #   基础知识补全（推荐，QA 格式，单体不拆分）
│   └── decisions.md             #   技术选型记录（ADR 风格）

├── tests/                       # 测试（可选）

├── examples/                    # 使用示例（可选）

├── resume/                      # 简历描述
│   └── resume.md

└── notes/                       # 笔记系统（长期积累）
    ├── iterations/              #   重构迭代记录（保留历史代码版本）
    │   └── v<NN>-<title>.md     #   每次重构的原因、过程、结果
    └── concepts/                #   核心技术概念笔记
```

---

## 与 reconstruction 的关键差异

| 维度 | reconstruction | product |
|------|---------------|---------|
| 目标 | 理解结构 | 产出产品 |
| 工作单元 | curriculum/ 轮次驱动 | tasks/ 任务三元组驱动 (plan→log→code-review) |
| 代码组织 | 分散在 experiments/ | 统一在 src/ |
| 质量要求 | 跑通即可 | 产品级，含测试和文档 |
| 展示性 | 不对外的学习笔记 | 面向用户的清晰文档 |
| 笔记 | 课程轮次 notes + QA | 任务笔记 + issues + knowledge-base |
| 问题追踪 | 轮次内 qa.md 未解决问题 | issues.md（IS-XXX + 优先级） |

---

## 任务笔记系统

Product 项目的日常工作围绕 `docs/tasks/` 中的**任务三元组**展开：

```
tasks/{name}-plan.md          ← 任务计划（要做什么 + 设计调研）
tasks/{name}-log.md           ← 执行日志（实际做了什么 + Bug 踩坑）
tasks/{name}-code-review.md   ← 代码品读（复盘质询，标注 T1–T7 分类）
```

详细规范见 `_framework/notes/spec/task-note-system.md`，分类体系见 `_framework/notes/spec/code-review-classification.md`。

### 配套支撑文件

| 文件 | 用途 | 强制性 |
|------|------|--------|
| `docs/issues.md` | 非主线问题追踪（IS-XXX + 🔴🟡🟢 优先级） | ★ 标配 |
| `docs/knowledge-base.md` | 基础知识补全（QA 格式，单体不拆分） | 推荐 |
| `docs/decisions.md` | 技术选型记录（ADR 风格） | 推荐 |
| `docs/README.md` | 文档系统自身的结构设计 + 使用规则 | 推荐 |

### 工作流

```
接到任务 → tasks/{name}-plan.md
执行中   → tasks/{name}-log.md（每次对话追加）
产出代码 → tasks/{name}-code-review.md（T1–T7 分类）
定期整理 → T1→knowledge-base / T3,T5,T6→issues / 决策→decisions
```

---

## 重构迭代记录规范

`notes/iterations/v<NN>-<title>.md` 记录每次重大重构（与 tasks/ 互补——tasks/ 记录日常，iterations/ 记录阶段性架构变更）：

```markdown
# v01 — <重构标题>

**日期**: YYYY-MM-DD
**触发原因**: <!-- 为什么这次重构？ -->

## 变更内容

- 旧: <之前的做法>
- 新: <之后的做法>
- 原因: <为什么改>

## 影响范围

- 修改的文件: ...
- 破坏性变更: 是/否

## 复盘

- 做得好的: ...
- 可以改进的: ...
```

---

## 代码整洁 vs 笔记丰富

产出项目面向展示，源代码区（`src/`）保持整洁；详细的迭代思考和任务记录在 `docs/` 和 `notes/`。

如果你希望代码仓库完全纯净（例如作为独立开源项目发布），可将 `docs/tasks/` 和 `notes/` 中的详细记录外置到全局 `notes/products/<name>/`，使产品目录仅保留代码和核心文档。

---

## Submodule 变体: 代码与笔记跨仓库分离

当产品以 **git submodule** 形式挂载在元仓库 `products/<name>/` 时，submodule 仓库保持纯代码，产品文档与笔记在元仓库 `notes/<name>/` 下按 product 骨架镜像管理：

```
<meta-repo>/
├── products/<name>/            ← git submodule — 纯代码（README/LICENSE/src/tests）
└── notes/<name>/               ← 元仓库内 — 笔记与私有文档
    ├── README.md               ←   笔记索引
    ├── docs/
    │   ├── overview/           ←   宏观参考（构建配置、项目概述、构建速查）
    │   ├── tasks/              ←   任务三元组（plan─log─code-review）
    │   ├── roadmap.md          ←   特性路线图（优先级分批次）
    │   ├── issues.md           ←   非主线问题追踪（IS-XXX + 🔴🟡🟢）
    │   ├── knowledge-base.md   ←   基础知识补全（QA 格式，推荐）
    │   └── decisions.md        ←   技术选型记录
    ├── notes/
    │   └── questions.md        ←   开放讨论（尚未决策的架构问题）
    └── resume/                 ←   简历条目、面试 Q&A
```

### 与标准骨架的映射

| 标准 product 骨架 | submodule 变体 |
|-------------------|----------------|
| `products/<name>/docs/` | `notes/<name>/docs/`（元仓库） |
| `products/<name>/notes/` | `notes/<name>/notes/`（元仓库） |
| `products/<name>/resume/` | `notes/<name>/resume/`（元仓库） |

### 笔记目录语义

| 目录 | 内容性质 | 维护方式 |
|------|----------|----------|
| `docs/overview/` | 长期参考文档 | 随项目演进持续更新 |
| `docs/tasks/` | 已完成任务的记录 | 归档后只读，plan-log 配对 |
| `docs/roadmap.md` | 特性规划 | 完成一项划一项 |
| `docs/issues.md` | 待解决问题的追踪 | 发现→诊断→修复→关闭 |
| `docs/decisions.md` | 已落地的技术决策 | 决策时追加 |
| `docs/knowledge-base.md` | 零散知识条目 | QA 格式粗糙积累 |
| `notes/questions.md` | 开放讨论，未决策 | 决策落地后提炼到 decisions.md |
| `resume/` | 对外展示材料 | 项目完成后填充 |

### 要点

- submodule 仓库保持纯代码 + 面向使用者的核心文档（README、LICENSE）；私有内容（设计讨论、简历、面试准备）只在元仓库
- 机器相关的构建配置（如 `CMakeUserPresets.json`）放 submodule 内但 gitignored，避免硬编码路径进入版本库
- 第三方二进制资源（预编译 DLL、模型文件）体积大不进 git：用 gitignore 排除 + 打包/拆解脚本管理迁移（详见 `notes/explore/` 资源工具链讨论）
- 代码案例（如 `samples/<slug>/`）是文本资产，进 git 随仓库公开：与条目/媒体同 slug 对齐，由打包脚本携带交付；大工程排除生成物只留源码（来源: portfolio-site 决策 D7，2026-08-20）

---

## 与其他项目类型的关系

- **reconstruction → product**: 课程完成，整理为产品
- **product → reconstruction**: 想深入理解某部分，退回学习模式

转换规则见 `conversion.md`。
