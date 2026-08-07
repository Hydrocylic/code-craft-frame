# 框架使用手册

> 配套 `FRAMEWORK.md` — 先读方法论，再看本手册
> 版本: v2.0 | 创建: 2026-07-23 | 重构: 2026-08-07

---

## 快速开始

### 在新仓库使用本框架

```bash
# 1. 复制框架骨架
cp -r <source-repo>/_framework/ <new-repo>/_framework/

# 2. 创建必要目录
mkdir -p reference projects products notes/daily notes/concepts notes/resources envs

# 3. ★ 创建 CLAUDE.md（Agent 冷启动文件）
# 使用 _framework/templates/CLAUDE.md 模板，填入新仓库的具体内容
# 必须包含：仓库定位、核心规则、目录速查、创建约定、注意事项

# 4. 根据框架模板创建 .gitignore
# 参考 _framework/FRAMEWORK.md 中的 git 策略

# 5. 可选：用 submodule 引入参考项目
git submodule add <url> reference/<project-name>
```

### 在已有仓库采用本框架

> **重要：先审计，出报告，等确认，再动手。不要直接开始移动文件。**

**Phase 1: 审计（只读操作）**

```
├── 列出当前仓库中的所有文件和目录
├── 对照 FRAMEWORK.md §二 的目录结构，将现有内容分类：
│   ├── 哪些已经是参考项目的源码？      → reference/<name>/<source>/
│   ├── 哪些是学习过程中的笔记和实验？  → projects/<name>/curriculum/ 或 experiments/
│   ├── 哪些是独立的产品代码？          → products/<name>/src/
│   ├── 哪些是跨项目的通用笔记？        → notes/
│   ├── 哪些是环境配置文件？            → envs/
│   └── 哪些是不属于以上任何分类的？    → 需要讨论
└── 标记"不需要移动"的文件（如 README.md、.gitignore 等根目录文件）
```

**Phase 2: 提案（输出调整报告，不修改任何文件）**

调整报告应包含：
- **现状概览**: 当前文件数量和分布
- **调整方案**: before/after 目录结构对比
- **影响边界**: 明确哪些文件不动、哪些移动、移动后的路径
- **不归类的项目**: 列出来，等待用户决定
- **建议但不执行**: 如"这里建议创建 meta.yaml"（但不创建）

**Phase 3: 确认（等待用户审核）**

用户审核方案后：
- 可能同意全部方案
- 可能调整部分路径
- 可能否决某些变动
- 可能要求补充新内容

**Phase 4: 执行（按确认后的方案操作）**

分为两个子阶段：
- **4a. 结构调整**（批量操作，确认后可以执行）: 创建目录、移动文件、删除空目录
- **4b. 内容生成**（逐一操作，仅在用户明确要求时执行）: 创建 meta.yaml、填写 README 模板、撰写笔记 — 每一项都需独立确认

### Agent 行为约束

当使用 Agent（如 Claude Code）辅助结构调整时，Agent 应遵守：

1. **不主动批量生成文件** — 即使在 Phase 4，如果方案中包含"创建 5 个 meta.yaml"这样的批量操作，Agent 应逐一确认而非静默批量创建
2. **模板只复制、不填写** — 从 `templates/` 复制模板文件后，不自动填充内容（除非被明确要求）
3. **区分"结构迁移"和"内容生成"** — 移动文件是结构操作，可以批次处理；撰写笔记内容是生成操作，必须逐项确认
4. **默认只到 Phase 2** — Agent 收到"帮我按框架调整"这类指令时，默认只执行 Phase 1+2（审计+出报告），不自动进入执行

---

## 结构调整总则

本节适用于所有涉及**目录重组、文件迁移、项目类型转换**的场景。核心原则：

> **先给方案、等确认、再动手。不主动批量生成内容。**

### 四步流程

| 阶段 | 操作 | 是否修改文件 | 输出 |
|------|------|:-----------:|------|
| **Phase 1: 审计** | 扫描现状、归类内容 | ❌ 只读 | 现状清单 |
| **Phase 2: 提案** | 给出调整方案、影响范围 | ❌ 不修改（仅写提案笔记） | 调整报告（写入被分析工作区的 `.md` 笔记） |
| **Phase 3: 确认** | 用户审核方案 | ❌ 等待 | 确认/否决/修改 |
| **Phase 4: 执行** | 按确认后的方案操作 | ✅ | 4a.结构调整 + 4b.内容生成(按需) |

### Phase 4 的语义区分

这是最重要的区分：

| 操作类型 | 定义 | 执行方式 | 示例 |
|----------|------|---------|------|
| **结构调整 (4a)** | 移动文件、创建目录 | 确认后可以批量执行 | `mv old/file.md new/file.md` |
| **内容生成 (4b)** | 创建新文件并填充内容 | 每一项都需独立确认 | "创建 r01/notes.md 并填写学习目标" |

**结构调整**改变的是文件位置，不创造新内容。**内容生成**创造新的知识资产，必须由用户驱动。

### Agent 行为约束

当使用 Agent（如 Claude Code）辅助结构调整时：

1. **默认停止在 Phase 2** — 收到"帮我按框架调整目录"时，只做审计+出报告，不等确认不执行
2. **提案落盘** — Phase 2 的调整报告必须写成 `.md` 笔记文件写入被分析的工作区（如项目 `notes/` 或根目录 `notes/`），而非仅作为会话文本。提案笔记需包含 before/after 对比、影响范围、不归类项
3. **不批量创建内容文件** — 不应当在一次操作中创建 10 个 `notes.md` 并自动填充
4. **模板只复制不填写** — 可以提议"这里需要 meta.yaml"，但只在用户确认后才从模板复制，且不自动填写
5. **区分"移动"和"生成"** — 批量移动文件没问题，批量生成笔记内容不可以
6. **报告要可审核** — 调整报告必须包含 before/after 目录对比，使用户能逐项判断

---

## 创建参考项目（阅读）

参考项目用于只读分析。源码保持原样，笔记记录对代码的理解。

### 步骤

```bash
# 1. 创建项目目录
mkdir -p reference/<project-name>/notes

# 2. 放置或克隆参考源码到项目目录（手动操作）
#    - 下载的源码 → reference/<project-name>/<source>/
#    - git submodule → git submodule add <url> reference/<project-name>

# 3. 创建 meta.yaml
cp _framework/templates/meta.yaml reference/<project-name>/meta.yaml
#   编辑: type: reference, 填写 source 信息

# 4. 创建 README.md
#   记录来源、获取方式、内容概述

# 5. 创建首篇分析笔记
cp _framework/templates/concept-note.md reference/<project-name>/notes/overview.md
```

详细骨架见 `_framework/project-types/reference/SKELETON.md`。

---

## 创建复制项目（重构）

复制项目是本框架的核心学习载体。从参考项目中拆解代码，逐步重构。

### 前置条件

- 已有至少 1 个参考项目
- 对参考项目的知识体系有基本理解
- 准备好动手复现

### 步骤

```bash
# 1. 创建项目骨架
mkdir -p projects/<project-name>/{src/include,curriculum,experiments,resume,notes/concepts}

# 2. 创建 meta.yaml（type: reconstruction）
cp _framework/templates/meta.yaml projects/<project-name>/meta.yaml

# 3. 创建 README.md
cp _framework/templates/project-readme.md projects/<project-name>/README.md

# 4. 设计首轮课程
mkdir -p projects/<project-name>/curriculum/r01-<title>
# 创建 notes.md, qa.md, code-refs.md

# 5. 创建简历占位
cp _framework/templates/resume-project.md projects/<project-name>/resume/resume.md
```

### meta.yaml 示例

```yaml
project: <project-name>
type: reconstruction
status: planned           # planned → in-progress → completed → archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
description: >
  简要描述学习目标和范围。

refs:
  - reference/<ref-project>

rounds: []

resume: resume/resume.md
```

详细骨架见 `_framework/project-types/reconstruction/SKELETON.md`。

---

## 创建产出项目（产品）

产出项目面向展示和复用。产品代码统一在 `src/`，迭代记录在 `docs/` + `notes/`。

### 步骤

```bash
# 1. 创建产品骨架
mkdir -p products/<product-name>/{src/include,docs,resume,notes/iterations,notes/concepts}

# 2. 创建 meta.yaml（type: product）
cp _framework/templates/meta.yaml products/<product-name>/meta.yaml

# 3. 创建架构文档
touch products/<product-name>/docs/architecture.md
touch products/<product-name>/docs/changelog.md
touch products/<product-name>/docs/design-decisions.md

# 4. 创建简历占位
cp _framework/templates/resume-project.md products/<product-name>/resume/resume.md
```

详细骨架见 `_framework/project-types/product/SKELETON.md`。

---

## 项目类型转换

项目类型可以转换（如 reconstruction → product）。**转换操作必须遵循"结构调整总则"**：先审计现有代码/笔记、出转换方案、等用户确认、再动手迁移。

转换规则和详细步骤见：
- `_framework/project-types/reference/conversion.md`
- `_framework/project-types/reconstruction/conversion.md`
- `_framework/project-types/product/conversion.md`

Agent 辅助转换时，默认只执行审计+提案（Phase 1+2），不自动执行结构调整。

---

## 添加新轮次

在一轮学习完成后，需要增加新一轮时：

```bash
# 创建新轮次目录
mkdir -p projects/<project-name>/curriculum/r0<N>-<title>

# 从模板创建笔记
cp _framework/templates/round-notes.md projects/<project-name>/curriculum/r0<N>-<title>/notes.md
cp _framework/templates/qa.md projects/<project-name>/curriculum/r0<N>-<title>/qa.md
cp _framework/templates/code-refs.md projects/<project-name>/curriculum/r0<N>-<title>/code-refs.md
```

更新 `meta.yaml` 的 `rounds` 列表和 `updated` 字段。

### 轮次编号约定

- 使用两位数编号：`r01`, `r02`, ..., `r10`, ...
- 编号只表示推荐顺序，不是强制的先后依赖
- 如果需要在两轮之间插入：`r02b-<title>`
- 如果有补充/拓展轮次：`r03-supplement-<title>`

---

## 创建实验

### 步骤

```bash
mkdir -p projects/<project-name>/experiments/<exp-name>/{src,outputs}

# 从模板创建
cp _framework/templates/experiment-notes.md projects/<project-name>/experiments/<exp-name>/notes.md
```

### 实验代码

将实验代码放在 `src/` 目录中。代码文件中使用注释标注：
- 关联的课程轮次
- 参考了哪些参考项目代码
- 关键参数说明

### 运行指令

在 `notes.md` 中写清楚运行指令（使用从仓库根目录的相对路径）：

```markdown
## 运行方式

```bash
# 编译型语言
<compiler> <flags> projects/<project>/experiments/<exp-name>/src/<file> -o outputs/<binary>
./outputs/<binary>

# 脚本型语言
<run-command> projects/<project>/experiments/<exp-name>/src/<file>

# 查看结果
ls projects/<project>/experiments/<exp-name>/outputs/
```
```

### 运行指令脚本（可选）

如果编译/运行命令较长，可以创建 `run.ps1` (Windows) 或 `run.sh` (Linux)：

```powershell
# run.ps1 — 示例
param(
    [string]$BuildType = "Release"
)
cmake -B build -DCMAKE_BUILD_TYPE=$BuildType && cmake --build build
```

---

## 撰写简历

项目完成（所有轮次结束）后，填写 `resume/resume.md`。

使用 `_framework/templates/resume-project.md` 模板。

简历撰写要点：
1. **不要复述过程** — 写成果，不写流水账
2. **技术栈要精确** — "PyTorch 2.0, ResNet18, LoRA (PEFT)" 或 "C++20, STL, CMake 3.28" 而非 "深度学习" 或 "C++"
3. **量化优于定性** — "ROUGE-L 从 0.07 提升到 0.22" 优于 "效果显著提升"
4. **写一个关键难点** — 面试官爱问"你遇到的最大挑战是什么"

---

## Git Submodule 管理

### 概述

框架推荐对**有上游**的参考项目使用 git submodule。但对于**已发布的稳定版本**（如从 GitHub Release 下载的源码包），使用普通目录即可。

### 添加参考项目为 submodule

```bash
# 添加 submodule
git submodule add <repository-url> reference/<project-name>

# 首次克隆后初始化
git submodule init
git submodule update

# 或者克隆时一步到位
git clone --recurse-submodules <repo-url>
```

### 固定版本

添加 submodule 后，建议固定到特定 commit 或 tag（而非追踪分支），确保参考代码的不可变性：

```bash
cd reference/<project-name>
git checkout <tag-or-commit>
cd ../..
git add reference/<project-name>
git commit -m "fix: pin reference/<project-name> to <tag>"
```

### 更新参考项目

当上游发布新版本，需要更新参考时：

```bash
# 进入 submodule 目录
cd reference/<project-name>

# 拉取最新
git fetch origin

# 切换到新版本
git checkout <new-tag-or-commit>

# 回到仓库根目录，提交更新
cd ../..
git add reference/<project-name>
git commit -m "ref: update reference/<project-name> to <new-version>"
```

### 移除 submodule

```bash
# 1. 从 .gitmodules 中移除
git submodule deinit -f reference/<project-name>

# 2. 删除目录
rm -rf reference/<project-name>

# 3. 从 git 中移除
git rm -f reference/<project-name>

# 4. 清理 .git/modules/ 中的残留
rm -rf .git/modules/reference/<project-name>
```

### 注意事项

- Submodule 更新后，必须在父仓库中 commit 这次引用变更——否则其他克隆者看到的仍是旧版本
- Submodule 的 `.git` 是指向父仓库 `.git/modules/` 的指针，复制目录时需要注意
- 如果参考项目需要搜索/跳转代码，普通目录的体验比 submodule 好——按需选择
- **慎用 `--recursive`** — 参考项目内部可能有自己的嵌套子模块（测试框架、第三方依赖等）。`git submodule update --init --recursive` 会把参考项目的构建依赖也一并拉取。对于只读参考场景，用 `git submodule update --init` 即可，无需递归

---

## 将此仓库作为字库（submodule）纳入其他项目

### 场景

本仓库的核心资产是 `_framework/` 目录。其他学习仓库可以：
1. **复制方式**: `cp -r learn-frame/_framework/ <other-repo>/_framework/`（最简单，但失去与母库的更新关联）
2. **字库方式**: 将 learn-frame 作为 submodule 引入，然后从其 `_framework/` 中引用模板和规则

### 字库（submodule）方式

```bash
# 在目标学习仓库中
cd <target-repo>

# 1. 添加本库为 submodule（放在隐藏/元目录中）
git submodule add <learn-frame-url> .meta/framework-source

# 2. 在 CLAUDE.md 中指向字库中的框架
# CLAUDE.md:
# 框架来源: .meta/framework-source/_framework/
# 模板路径: .meta/framework-source/_framework/templates/

# 3. 创建新项目时从字库复制模板
cp .meta/framework-source/_framework/templates/meta.yaml projects/<name>/meta.yaml
cp .meta/framework-source/_framework/templates/CLAUDE.md ./CLAUDE.md
```

### 更新字库中的框架

```bash
# 当母库中的 _framework/ 有更新时
cd <target-repo>/.meta/framework-source
git fetch origin
git checkout origin/master  # 或特定的 tag/commit
cd ../..
git add .meta/framework-source
git commit -m "meta: update framework-source to <version>"
```

### 字库 vs 复制的选择

| 维度 | 复制 _framework/ | submodule 字库 |
|------|-----------------|---------------|
| 简单度 | ✅ 一步完成 | 需要理解 submodule |
| 独立性 | ✅ 完全独立，可自行修改 | 修改需在母库中进行 |
| 同步更新 | ❌ 手动对比 CHANGELOG | ✅ `git fetch` + checkout |
| 适合场景 | 想摆脱母库，独立演化 | 想持续获取框架更新 |
| 版本追踪 | 自己维护 | 通过 submodule commit 追踪 |

**建议**: 
- 刚起步的学习仓库 → 复制方式，简单直接
- 多个学习仓库需要同步框架更新 → 字库方式
- 对框架有了自己的修改 → 复制方式（分叉演化）

### 框架更新检查

无论使用哪种方式，定期检查 `CHANGELOG.md` 的变更：

```bash
# 查看当前框架版本
head -5 _framework/FRAMEWORK.md | grep "版本"

# 对比字库中是否有新变更
git diff --submodule .meta/framework-source
```

---

## 维护 _framework/

### 添加新模板

1. 在 `_framework/templates/` 中创建模板文件
2. 在 `CHANGELOG.md` 中记录：`template-add: <name> — 用途`

### 修改现有规则

1. 在 `FRAMEWORK.md` 或 `MANUAL.md` 中更新
2. 在 `CHANGELOG.md` 中记录变更内容 + 影响范围
3. 检查各项目 `meta.yaml` 的 `updated` 字段，判断哪些需要同步

### 提升私有规则

```markdown
## YYYY-MM-DD — private-promote: <规则名>

**来源**: private/ 中的 <文件名>

**提升至**: FRAMEWORK.md §<章节号>

**规则内容**: <简述>

**影响范围**: 新项目自动适用；现有项目可选升级
```

### 定期检查清单

- [ ] `private/` 中是否有经多次验证可提升的规则？
- [ ] 模板是否仍然实用？（跑一个学习项目感受一下）
- [ ] `CHANGELOG.md` 是否最新？
- [ ] 参考项目的路径（submodule URL）是否仍然有效？
- [ ] `notes/explore/` 中是否有应纳入规范的改进建议？

---

## 跨仓库同步

### 框架复制

当在新仓库使用本框架时：

1. 复制 `_framework/` 目录（不含 `private/`）
2. 将 `_framework/private/` 中的通用内容提升到 `FRAMEWORK.md`
3. 在新仓库创建自己的 `private/learner-profile.md`

### 框架更新回传

当在一个仓库中的框架迭代产生了有价值的更新：

1. 记录在 `CHANGELOG.md`
2. 手动同步到其他使用本框架的仓库的 `_framework/`
3. 对比各仓库 `CHANGELOG.md` 确认版本一致性

---

## 常见问题

### Q: 三种项目类型的界限模糊了怎么办？

**A:** 
- 不确定是"分析"还是"重构" → 先建 reference 项目，分析透彻后再转为 reconstruction
- 不确定是"学习"还是"产出" → 先建 reconstruction 项目，学习完成后再转为 product
- 不确定是"产品"还是"参考" → 先建 product 项目，需要深入理解其中模块时局部退为 reconstruction（自举模式）

### Q: 一个复制项目能参考多个参考项目吗？

**A:** 可以。在 `meta.yaml` 的 `refs` 中列出所有参考项目。但通常有 1 个"主要参考"，避免注意力分散。

### Q: 笔记写到一半发现轮次划分不合理怎么重构？

**A:** 轮次独立设计就是为了这个场景。直接创建新轮次，把旧轮次的内容迁移过去，然后删除旧轮次目录。不影响其他轮次。

### Q: experiments/outputs/ 被 gitignored 了，想保留某个关键结果怎么办？

**A:** 把关键结果（如 loss curve 图、metrics 表格、关键输出截图）贴到 `notes.md` 中。原始日志和模型权重放在 `outputs/` 中 gitignored。

### Q: 环境配置应该在项目内还是 envs/ 中？

**A:** 
- 项目特有的依赖 → 项目 README.md 中说明
- 可复用的环境脚本和模板 → `envs/`
- 跨项目共享的依赖声明 → `envs/requirements-*.txt` 或 `envs/<build-templates>/`
- 原则：能复用则放 `envs/`，仅本项目使用则放项目内

### Q: 远程运行时如何组织代码和配置？

**A:**
1. 环境配置（requirements.txt、环境变量模板）放在 `envs/`
2. 笔记中标注硬件需求（GPU / 内存 / OS）
3. 在实验的 `notes.md` 中写清楚远程运行的步骤
4. 运行产物可以留在远程机器，关键结果贴回笔记中

### Q: 框架的 CLAUDE.md 模板和本仓库的实际 CLAUDE.md 是什么关系？

**A:**
- `_framework/templates/CLAUDE.md` 是**模板**——给新仓库复制后填写
- 本仓库根目录的 `CLAUDE.md` 是**实例**——本仓库实际使用的冷启动文件
- 新仓库应该：复制模板到根目录 → 填写仓库的具体内容 → 随仓库演进持续维护
