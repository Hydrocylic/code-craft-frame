# 学习框架方法论

> 版本: v2.0
> 创建: 2026-07-23
> 重构: 2026-08-07 — 三版本统一
> 来源: 融合 _framework1 (AI-LAB v1.0), _framework2 (cpp-lab v1.0), _framework3 (v1.1)
> 状态: active

---

## 一、设计哲学

### 核心信念

1. **代码是学习的第一载体** — 笔记围绕代码展开，而非代码围绕笔记
2. **参考不可变** — 优秀的参考项目保持原样，作为"标准答案"反复查阅
3. **项目是管理单元** — 每个项目自包含，三种类型各有独立骨架：参考（阅读）→ 复制（重构）→ 产出（产品）
4. **路径即配置** — 笔记中通过显式路径指令定位代码和环境，不依赖隐式全局状态
5. **框架边用边迭代** — 方法论在实践中打磨，规则从私有提升到共有
6. **结构调整克制先行** — 涉及目录重组、文件迁移、类型转换等结构化操作时，先给方案、等确认、再动手。不主动批量生成内容

### 适用范围

本框架面向**系统性的代码学习**：
- 阅读和理解优秀开源项目
- 从参考项目中提取知识并动手复现
- 记录学习过程（Q&A、代码映射、实验记录）
- 产出可用于简历的项目描述

**不适用的场景：**
- 最终面向大众的开源产品项目（那是另一种工程范式）
- 快速原型验证（本框架较重）

### 结构调整原则：先审计，再提案，确认后执行

任何涉及**目录重组、文件迁移、项目类型转换**的操作，无论是人工执行还是通过 agent 辅助，都遵循四步流程：

```
Phase 1: 审计（只读）         Phase 2: 提案（输出报告）
  扫描现状、归类内容        →   调整方案、影响范围、对比图
        ↓                           ↓
Phase 3: 确认（等待用户）    Phase 4: 执行（按需操作）
  用户审核方案，选择取舍    ←   结构迁移（移动文件），内容生成仅在被明确要求时进行
```

**核心约束**：
- **不主动批量生成** — 创建 `notes.md`、`qa.md`、`meta.yaml` 等是用户决策，不是 agent 的默认动作。Agent 可以提议"这里建议创建一个 meta.yaml"，但不应该在结构调整时自动成批生成
- **方案在动手之前** — 给出调整报告（before/after 目录对比、受影响文件清单），等待用户确认后再进行文件移动
- **结构迁移 ≠ 内容填充** — 移动文件到正确的位置是结构操作，可以批量执行；为每个轮次填充笔记内容不是结构操作，必须由用户逐一确认
- **提案落盘为笔记** — Phase 2 的调整方案应以 `.md` 笔记形式写入被分析的工作区中（如项目 `notes/` 或根目录 `notes/`），而非仅作为会话文本输出。这使提案成为仓库历史的一部分，可被后续查阅、审计和追溯

详细的 agent 协作指南见 `MANUAL.md` §"结构调整总则"。

---

## 二、目录结构规范

```
<repo-root>/
│
├── CLAUDE.md                      # ★ Agent 冷启动文件（本框架必建组件）
│
├── _framework/                   # 元框架（可复制到其他学习仓库）
│   ├── FRAMEWORK.md              # 本文件 — 方法论
│   ├── MANUAL.md                 # 使用手册
│   ├── CHANGELOG.md              # 规则变更历史
│   ├── templates/                # 可复用模板
│   ├── project-types/            # 三种项目类型的骨架和转换规则
│   │   ├── README.md
│   │   ├── reference/
│   │   ├── reconstruction/
│   │   └── product/
│   ├── private/                  # 个人行为偏好 [gitignored]
│   └── notes/                    # 框架自身的规范与探讨
│       ├── spec/                 #   规范区 — 框架设计的规范化文档
│       └── explore/              #   探讨区 — 局限性、可调整内容、设计决策
│
├── reference/                    # 参考项目（阅读）[IMMUTABLE — 只读]
│   └── <name>/                   #   type: reference
│       ├── README.md
│       ├── meta.yaml
│       └── <source>/             #   参考源码（不动）
│
│   ★ 参考项目不含 notes/。分析笔记归属到 reconstruction 项目的 curriculum 中。
│
├── projects/                     # 复制项目（拆解重构）
│   └── <project-name>/           #   type: reconstruction
│       ├── README.md
│       ├── meta.yaml
│       ├── src/                  #   ★ 重构后的源码（项目核心产出）
│       ├── curriculum/           #   课程轮次
│       │   ├── README.md         #     轮次规划总览
│       │   └── r<NN>-<title>/
│       │       ├── notes.md
│       │       ├── qa.md
│       │       └── code-refs.md
│       ├── experiments/          #   动手实验
│       │   └── <exp-name>/
│       │       ├── src/          #     ★ 实验代码（必须保留）
│       │       ├── outputs/      #     运行产物 [gitignored]
│       │       └── notes.md
│       ├── resume/               #   简历描述（项目完成标志）
│       └── notes/                #   项目内跨轮次概念笔记
│
├── products/                     # 产出项目（产品）
│   └── <product-name>/           #   type: product
│       ├── README.md
│       ├── meta.yaml
│       ├── src/                  #   ★ 产品源码（统一结构）
│       ├── docs/                 #   架构文档 + 变更记录
│       │   ├── architecture.md
│       │   ├── changelog.md
│       │   └── design-decisions.md
│       ├── resume/
│       └── notes/                #   迭代记录 & 概念笔记
│
├── envs/                         # 环境配置（骨架，按需填充）
│   ├── README.md
│   ├── scripts/                  #   环境激活/检查脚本（可选）
│   ├── .env.template             #   环境变量模板（可选）
│   └── <build-templates>/        #   构建配置模板（CMakeLists.txt 等，可选）
│
├── notes/                        # 全局笔记（跨项目）
│   ├── daily/                    #   每日学习记录
│   ├── concepts/                 #   跨项目核心概念
│   └── resources/                #   外部资源索引
│
├── README.md
├── RESOURCES.md
└── .gitignore
```

### CLAUDE.md — Agent 冷启动文件

`CLAUDE.md` 是本框架的**必建组件**，放在仓库根目录。

**目的**：让 Claude Code（或其他 AI Agent）进入仓库时，无需阅读全部文档就能理解：

1. 这是什么仓库（学习型，不是生产项目）
2. 核心规则（参考不可改、项目自包含、路径即配置）
3. 目录速查（去哪里找什么）
4. 创建新内容的约定
5. 注意事项（git 策略、submodule、gitignore 规则）

**写法原则**：
- 浓缩，不复制 FRAMEWORK.md 的完整内容
- 用"规则 + 指针"的模式——每条规则一句话，详情指向具体文档
- 保持与 FRAMEWORK.md 和 MANUAL.md 的一致性
- 当框架规则变更时，同步更新 CLAUDE.md

**模板参考**：`_framework/templates/CLAUDE.md` 提供了可直接复制修改的范例。

---

## 三、项目类型体系

本框架定义四种项目类型，覆盖从轻量刷题到产品产出的完整学习链路：

```
practice（轻量刷题）──→ reconstruction（拆解重构）──→ product（产品产出）
    │                         │                          │
    ├── 单文件单题             ├── 课程轮次驱动           ├── 架构文档驱动
    ├── 代码+笔记双文件        ├── 代码保留在项目中       ├── 代码版本→笔记系统
    └── 扁平目录，题号命名     └── 实验共用构建环境       └── 展示整洁，面向用户

reference（只读分析）──→ reconstruction（拆解重构）──→ product（产品产出）
        │                        │                          │
        └── 笔记在项目内         ├── 课程轮次驱动           ├── 架构文档驱动
                                 ├── 代码保留在项目中       ├── 代码版本→笔记系统
                                 └── 实验共用构建环境       └── 展示整洁，面向用户
```

详细骨架和转换规则见 `_framework/project-types/README.md`。

---

### 练习项目（Practice）— 轻量刷题

> 位置：`<practice-dir>/`（如 `LeetCodePractice/`） | type: `practice`

**定义**：面向高频、轻量的日常刷题场景。一个题目 = 一个代码文件 + 一个笔记文件。

**特征**：
- 单文件单题（`.cpp`），自包含：答案 + 多解法 + 测试用例三位一体
- 扁平目录结构，以题号命名
- 配套 `.md` 笔记，聚焦思路探讨而非完整记录
- 无轮次、无实验、无简历产出
- 可触发更深度的学习（practice → reconstruction）

**创建时机**：开始刷算法/面试题，需要系统记录而不是随手写完就丢。

**代码文件结构**：
```
<题号>.cpp
  ├── 问题描述（顶部注释块）
  ├── Solution / Solution2 / ... （多解法，标注思路+复杂度）
  └── main() （简单测试用例）
```

**笔记文件结构**：见 `_framework/templates/practice-note.md`。

**与 reconstruction 的关系**：当某道题涉及的知识点需要系统深入时，可将该题的核心算法拆解为独立的 reconstruction 项目（如多个滑动窗口题 → `projects/sliding-window/`）。

---

### 参考项目（Reference Project）— 阅读

> 位置：`reference/` | type: `reference`

**定义**：源码保持原样不动，只读参考。不包含分析笔记——笔记属于 reconstruction 项目的 curriculum。

**特征**：
- 源码不可修改（IMMUTABLE）
- 目录极简：仅源码 + README.md + meta.yaml + RESOURCES.md
- 分析笔记归属到 reconstruction 项目的 curriculum 中，通过 `code-refs.md` 映射到本目录
- 无 notes/、无 curriculum、无 experiments、无独立 src/

**创建时机**：获取了值得深入阅读的优秀源码，希望系统性分析其设计。

---

### 复制项目（Reconstruction Project）— 重构

> 位置：`projects/` | type: `reconstruction`

**定义**：从参考项目中拆解代码，逐步重构，理解结构。是学习的核心载体。

**特征**：
- 有独立的 `src/` 存放重构后的代码
- 课程轮次驱动（`curriculum/`）：每个 round 聚焦一个知识/实现模块
- 实验（`experiments/`）共用项目构建环境和头文件
- 阶段构建和运行测试
- 代码保留在项目中，支持复盘阅读
- 完成标志：`resume/resume.md`

**创建时机**：对参考项目的理解达到可以动手复现的程度。

---

### 产出项目（Product Project）— 产品

> 位置：`products/` | type: `product`

**定义**：产出完备的产品代码，供开源、应用和展示。

**特征**：
- 统一的产品 `src/`，非实验分散结构
- 架构文档驱动（`docs/architecture.md` + `docs/changelog.md`）
- 结构反复重构以达到产品级质量，迭代记录在 `notes/iterations/`
- 展示整洁：README、LICENSE、API 文档
- 无 curriculum 轮次（学习过程在 reconstruction 阶段已完成）
- 完成标志：`resume/resume.md`

**创建时机**：学习完成，准备整理产出；或直接以产品为目标从零构建。

---

### 三种类型对比

| 维度 | reference | reconstruction | product |
|------|-----------|---------------|---------|
| 主导力 | 源码驱动（只读） | 参考驱动（拆解） | 需求驱动（构建） |
| 代码 | 参考源码（不动） | src/ + experiments/ | 统一 src/ |
| 笔记系统 | 无（笔记在 reconstruction 中） | curriculum/（课程轮次） | docs/ + notes/iterations/ |
| 简历 | 可选（无独立 resume/） | 侧重"掌握了 X" | 侧重"从零构建了 Y" |
| 构建 | 参考项目的构建 | 项目级构建，实验共用 | 面向用户的构建 |
| 转换方向 | → reconstruction / product | → product | → reconstruction（自举） |

### 项目类型转换

项目类型不是固定的。例如：复制项目在课程完成后可转为产出项目；产出项目中的模块想深入理解时可退回复制模式。

转换规则见 `_framework/project-types/<type>/conversion.md`。转换可由 agent 辅助执行，但必须遵循"先审计→出方案→等确认→再动手"的克制流程（详见 §一 结构调整原则和 MANUAL.md §结构调整总则）。

---

## 四、轮次机制（Round System）

### 概念

**轮次（Round）** 是课程的基本组织单元。每个轮次聚焦一个独立的知识点/实现模块。

### 轮次目录结构

```
curriculum/r<NN>-<kebab-title>/
├── notes.md        # 学习笔记
├── qa.md           # 问题与解答
└── code-refs.md    # 代码路径映射 → reference/
```

### 轮次设计原则

1. **独立可删** — 删除一个轮次不影响其他轮次
2. **可增补** — 随时可以插入新轮次（如 `r02b-visualization/`）
3. **命名稳定** — 轮次目录名用 kebab-case 描述主题，编号只表示推荐顺序
4. **收尾明确** — 每轮结束时在 `qa.md` 中记录"本轮未解决的问题"
5. **代码关联** — `code-refs.md` 中标注参考代码位置和本项目的对应实现

### 跨轮次 Q&A

在 `curriculum/` 下保留 `qa-cross.md`，记录跨轮次的综合问题和思考。不强制创建。

---

## 五、实验规范

### 实验的目的

实验不是"跑通代码"，而是：
- 验证对参考项目的理解是否正确
- 探索参数变化对结果的影响
- 记录意外发现和错误排查过程

### 实验目录结构

```
experiments/<experiment-name>/
├── src/             # ★ 实验代码（必须保留，不可删除）
├── outputs/         # 运行产物 [gitignored]
├── notes.md         # 实验记录 & 复盘
└── run.ps1 / run.sh # 可执行的运行指令脚本（可选）
```

### 实验命名

用简短 kebab-case 描述实验内容：`conv2d-playground`、`lora-rank-sweep`、`pooling-compare`。

### 实验记录模板要点

- 实验目的
- 运行指令（精确到路径）
- 预期结果
- 实际结果
- 差异分析
- 收获与启发
- 踩坑记录（错误信息 → 原因分析 → 解决方案）

---

## 六、环境管理

### 原则：代码与环境分离

- 代码属于仓库（`experiments/<exp>/src/`）
- 环境配置属于 `envs/`（骨架，按需填充）
- 运行产物属于各自的 `outputs/`（gitignored）

### 路径即配置

笔记中写显式路径，不依赖环境变量或隐式设置：

```markdown
## 运行方式

```bash
# 从仓库根目录执行
<run-command> projects/<name>/experiments/<exp>/src/<file>

# 输出见
# projects/<name>/experiments/<exp>/outputs/
```
```

### 环境适配

不同操作系统、工具链或技术栈可能需要调整配置：
- 编译型语言：构建配置（如 CMakeLists.txt）放在 `envs/<build-templates>/`
- 脚本型语言：依赖声明（如 requirements.txt）和激活脚本放在 `envs/scripts/`
- 环境变量：使用 `envs/.env.template` 模板
- 笔记中标注需要哪些外部依赖和硬件需求（GPU、大内存等）

### 远程运行支持

考虑到算力限制，代码可能在其他机器/服务器上执行：
- 环境配置文件放在 `envs/`
- 笔记中标注哪些实验需要特殊硬件（GPU / 大内存 / 特定 OS）
- 不强制 `venv/` 或 `build/` 在仓库内

---

## 七、简历描述

### 定位

每个项目完成后，撰写简历项目描述。这是**项目完成的收尾标志**。

- **参考项目**: 无独立 resume/，关键收获汇入对应的 reconstruction 项目简历
- **复制项目**: `projects/<name>/resume/resume.md`
- **产出项目**: `products/<name>/resume/resume.md`

### 模板要点

- 项目概述（1-2 句）
- 技术栈（精确到版本号）
- 个人贡献/学习内容
- 量化成果（如有）
- 关键难点与解决

---

## 八、私有规则与共有规则

### 区分

| | 共有 | 私有 |
|------|------|------|
| 位置 | `_framework/FRAMEWORK.md` | `_framework/private/` |
| 内容 | 方法论、规范、模板 | 个人学习风格、常见错误 |
| 共享 | ✅ 可跨仓库复制 | ❌ gitignored |
| 变更 | 需记录 CHANGELOG | 自由修改 |

### 提升机制

当一个私有规则经过多次验证被认为足够通用时：
1. 将其从 `private/` 提升到 `FRAMEWORK.md` 或 `MANUAL.md`
2. 在 `CHANGELOG.md` 中记录时间戳和变更内容
3. 标注来源：从哪个私有经验提升

---

## 九、版本与时间戳

### CHANGELOG 规范

`_framework/CHANGELOG.md` 记录每次框架变更：

```markdown
## YYYY-MM-DD — 变更标题

**类型**: rule-add | rule-change | template-update | private-promote | structure

**变更内容**:
- ...

**影响范围**:
- 现有项目需同步？是/否
- 同步方式: ...
```

### 项目级时间戳

每个项目的 `meta.yaml` 中记录：
- `created` — 创建日期
- `updated` — 最后更新时间
- 每个 round 的完成日期

### 同步检查

当 `_framework/` 发生变更时，通过对比 `CHANGELOG.md` 的时间戳与各项目 `meta.yaml` 的 `updated` 字段，判断哪些项目需要同步更新。

---

## 十、Git 策略

- **reference/** — 参考源码放普通目录（手动下载），有上游的放 git submodule。不可修改
- **_framework/private/** — gitignored
- **experiments/**/outputs/** — gitignored
- **envs/ 中的敏感文件** — gitignored
- 提交由开发者手动完成，框架不强制 commit 策略

---

## 十一、框架自身的规范与探讨

框架不是一成不变的。`_framework/notes/` 记录框架设计中的思考：

### 规范区（spec/）

框架设计的规范化文档。记录"应该怎么做"——设计意图、命名约定、模板规范。规范区的变更是严肃的，需要同步更新 FRAMEWORK.md 和 CHANGELOG。

### 探讨区（explore/）

框架的局限性和可调整内容。记录"为什么这样设计""有哪些已知局限""什么场景下可能需要调整"。探讨区的内容是开放的、反思性的，不强制同步到其他文档。

详见 `_framework/notes/README.md`。

---

## 附录：框架迭代生命周期

```
  ┌──────────┐
  │ 实践中发现问题 │
  └──────┬──────┘
         ↓
  ┌──────────┐
  │ 私有规则记录  │ ← private/learner-profile.md
  └──────┬──────┘
         ↓
  ┌──────────┐
  │ 多次验证有效 │
  └──────┬──────┘
         ↓
  ┌──────────┐
  │ 提升为共有规则│ ← FRAMEWORK.md + CHANGELOG.md
  └──────┬──────┘
         ↓
  ┌──────────┐
  │ 同步现有项目 │ ← 检查 meta.yaml updated 字段
  └──────┬──────┘
         ↓
  ┌──────────┐
  │ 反哺新一轮实践│
  └──────┬──────┘
         ↓
  ┌──────────┐
  │ 反思与探讨  │ ← notes/explore/ 记录局限和改进方向
  └──────────┘
```
