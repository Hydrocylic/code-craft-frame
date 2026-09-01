# 本地-远程规则建立机制（rule-sync-mechanism）

<!--
  位置: _framework/notes/spec/
  版本: 2026-08-26 创建（由 renderer-lab 回推，泛化自其落地版本）
  状态: active
-->

## 目的

定义各学习仓库的本地 `_framework/` 与上游远程框架仓库 `code-craft-frame`（hub）之间的规则建立与同步流程，使"私有经验 → 共有规则 → 远程 hub → 其他工作区"全链路可追溯、可审阅。

## 角色与载体

| 角色 | 位置 | 说明 |
|---|---|---|
| 远程 hub | `<lab>/code-craft-frame/`（git submodule，pin 到 commit） | 所有学习仓库共用的框架规则库 |
| 本地工作副本 | `<lab>/_framework/` | 日常使用；本地规则先在这里迭代 |
| 同步账本 | `_framework/CHANGELOG.md` | 每条变更含日期/类型/来源/影响范围 |
| 个人私有 | `_framework/private/` | gitignored；规则的孵化池 |

## 三条同步流

### 1. 远端 → 本地（拉取）

触发：上游 hub 有新 commit。

```bash
git submodule status                    # code-craft-frame 前有 + 号 = pin 落后
git diff --no-index --stat _framework code-craft-frame/_framework   # 只读对比
```

流程：人类执行 `git submodule update --remote code-craft-frame` → 对比两份 CHANGELOG → 决定采纳哪些规则写入本地 `_framework/`（文件编辑由 Agent 完成）→ 本地 CHANGELOG 记一条 `sync-from-upstream`，标注上游 commit。

### 2. 本地 → 远端（提升）

触发：本地规则经多次验证成熟，且对多个学习仓库通用。

1. 经验先在 `_framework/private/` 记录，多次验证；
2. 提升到本地 `FRAMEWORK.md` / `MANUAL.md` / 模板 / spec；
3. 本地 `CHANGELOG.md` 落条目（类型 + `**来源**: <lab>/...` + 影响范围）；
4. 人类执行：在 code-craft-frame 子模块仓库内 `git add` / `git commit` / `git push`（上游 CHANGELOG 同步落条目）；
5. 人类执行：`git add code-craft-frame` 更新子模块 pin 并提交。

### 3. hub → 其他仓库（分发）

上游更新后，各学习仓库自行更新子模块 pin，不强制同步升级。hub 不代管任何仓库。

## 冲突处理

- 本地与上游同时改同一规则：以两份 CHANGELOG 的条目对比，逐条决定采纳；未提升的本地临时改动可被上游版本覆盖。
- 提升中的规则与上游新规则冲突：先合并上游最新版，再在上游仓库提交本地增量。
- 文件级冲突判断命令（只读）：

```bash
git diff --no-index _framework/FRAMEWORK.md code-craft-frame/_framework/FRAMEWORK.md
```

## 记录格式（CHANGELOG 条目）

```markdown
## YYYY-MM-DD — <type>: <标题>
**类型**: rule-add | rule-change | template-update | private-promote | structure | sync-from-upstream
**变更内容**: ...
**来源**: <lab>/<path> 实践反馈（本地 → 远端提升时必填）
**影响范围**: 现有仓库需同步？是/否；同步方式
```

## 与旧流程的关系

替代 v1.1 MANUAL.md 的"手动复制目录 + 对比 CHANGELOG"跨仓库同步方式：规则流通仍有手工环节（git 指令由人类执行），但方向、账本与冲突处理已规则化。
