# CLAUDE.md — Agent 冷启动文件

<!--
  模板: _framework/templates/CLAUDE.md
  适用: 仓库根目录 CLAUDE.md
  ★ 这是框架的必建组件。复制到新仓库根目录后按实际情况修改。
-->

## 仓库定位

这是一个**学习型仓库**，不是生产项目。目的是系统性学习 <领域/技术栈>。

核心规则:
- `reference/` 中的源码不可修改（只读参考）
- 笔记通过显式路径引用代码，不依赖隐式环境
- 项目自包含：课程 → 实验 → 简历，一条龙

## 目录速查

| 目录 | 用途 | 规则 |
|------|------|------|
| `_framework/` | 元框架（方法论 + 模板） | 可复制到其他仓库 |
| `reference/` | 参考项目 | **不可修改** |
| `projects/` | 复制项目（拆解重构） | 课程轮次驱动 |
| `products/` | 产出项目（产品） | 架构文档驱动 |
| `envs/` | 环境配置骨架 | 按需填充 |
| `notes/` | 全局笔记 | 跨项目概念、每日记录 |

## 创建新内容的约定

- **参考项目**: `reference/<name>/` + `meta.yaml` (type: reference) → 见 `_framework/MANUAL.md`
- **复制项目**: `projects/<name>/` + curriculum/ + experiments/ → 见 `_framework/MANUAL.md`
- **产出项目**: `products/<name>/` + docs/ + src/ → 见 `_framework/MANUAL.md`
- **新轮次**: 从 `_framework/templates/` 复制 `round-notes.md`、`qa.md`、`code-refs.md`
- **新实验**: 从 `_framework/templates/` 复制 `experiment-notes.md`

## Agent 行为约束（★ 重要）

本仓库遵循"结构调整克制先行"原则。作为 Agent：

1. **涉及目录重组、文件迁移、项目类型转换时，必须先出方案、等确认、再动手。**
   - 默认行为：审计现状 → 给出调整报告（before/after 对比）→ 停止，等待用户确认
   - 不要直接开始创建目录和移动文件

2. **区分"结构调整"和"内容生成"**:
   - 结构调整（移动文件、创建目录）→ 确认后可以批量执行
   - 内容生成（创建笔记文件并填充内容）→ 必须逐项等用户确认，不批量生产

3. **模板只复制不填写** — 用户要求创建某文件时，从模板复制骨架，不自动填充实质性内容

4. **不要主动批量创建** — 不要在一次操作中创建 10 个 notes.md 或批量生成 meta.yaml

5. **当不确定操作属于结构调整还是内容生成时，倾向于保守（视为内容生成，等确认）**

详见 `_framework/FRAMEWORK.md` §一"结构调整原则"和 `_framework/MANUAL.md` §"结构调整总则"。

## 其他注意事项

- **Git 策略**: `reference/` 的上游项目用 submodule；`_framework/private/`、`experiments/*/outputs/`、敏感 env 文件全部 gitignored
- **路径约定**: 所有笔记中的命令使用仓库根目录的相对路径
- **CLAUDE.md 同步**: 框架规则变更时，同步更新本文件

## 当前仓库的具体内容

<!-- 以下按实际情况填写 -->

### 参考项目

- `reference/<name>` — <简述>

### 进行中的项目

- `projects/<name>` (reconstruction) — <当前轮次>
- `products/<name>` (product) — <当前阶段>

### 环境

- <语言/工具链>
- <关键依赖>
- <运行平台>
