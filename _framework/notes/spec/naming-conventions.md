# 命名约定

> 区域: spec（规范区）
> 框架版本: v3.0

---

## 目录命名

| 元素 | 约定 | 示例 |
|------|------|------|
| 项目 / 服务对象 | kebab-case | `cpp-concurrency`, `editor-core` |
| 轮次目录（如实例使用轮次） | `r<NN>-<kebab-title>` | `r01-memory-model`, `r03b-data-pipeline` |
| 实验目录 | kebab-case，动词-对象 | `conv2d-playground`, `lora-rank-sweep` |
| 概念笔记 | kebab-case，随项目走、**平铺**（按需建，不强制 `concepts/` 子目录） | `virtual-dispatch.md`, `attention-mechanism.md` |
| 迭代记录 | `v<NN>-<kebab-title>.md` | `v01-refactor-build-system.md` |

### 当前任务文件

任务按 `<task-dir>/` 组织，目录用 kebab-case。优先用 `plan.md`、`design.md`、`survey.md` 等用途短名；多个同类文件并列才加主题或日期。文件按需要创建，不强制 plan/log/notes/qa 成套存在。

运行交接放动态解析的 `<workspace-root>/_local/<ID>/`（工作区起点/容器根）；正式任务与交接分开。未定提案进入 `proposals/`，旧过程材料进入 `archived/`，不重建旧派工或全局日志区。

## 字段命名（meta.yaml）

| 字段 | 类型 | 说明 |
|------|------|------|
| `project` | string | 项目 / 服务对象短名，与目录名一致 |
| `type` | enum | 由实例定义（如 `product` / `reference` / `reconstruction`）；不要求所有实例同一枚举 |
| `status` | enum | 建议封闭枚举：`planned → in-progress → paused → completed → archived`；实例可改枚举措辞，但不要新增同义词 |
| `created` | date | 创建日期，ISO 格式 |
| `updated` | date | 最后更新日期 |
| `refs` | list | 参考项目路径列表 |
| `rounds` | list | 轮次目录名列表（仅使用轮次的实例） |
| `code_repo` | path | **代码仓**路径（不是“开发检出”）。若仓有多个 worktree，写仓的任一检出，并在同一行注释里写明开发检出。 |
| `resume` | path | 简历文件相对路径（仅需要该主题的实例） |

> **`status` 的用词收敛**：中断 / 延后 / 封存 / 暂停一律用 `paused`；要区分“什么时候能重启”就写进该行**注释**，**不要造新状态值**。判据：状态是**机器可读的封闭枚举**，重启条件是**人读的注释**——两者不要混。

## 模板文件命名

- 模板文件名应**描述其内容**，而非描述其位置：`round-notes.md` 而非 `notes-template.md`。
- 模板内注释标注适用位置。

## 路径写法（引用其它文件时）

1. **默认写仓根相对完整路径**：`_framework/notes/spec/git-practices.md`。
2. **唯一允许省略 `_framework/` 前缀的场合**：文件自身就在 `_framework/**` 内（上下文已是框架根）。
3. **`_framework/**` 之外一律不简写**——笔记、轮次文档、交接件里出现 `notes/spec/…` 视为待修。
4. **历史记录不改**：带日期的日志条目（执行日志、轮次 log）按“历史保留”口径原样留着。
5. **断链的处理范围**：**只有规则文件与产物代码里的引用算缺陷**——规则文件 = `_framework/**`、根 `AGENTS.md` / `README.md`、各区 `README.md`、当前任务契约与必要导航；产物代码 = 实例的源码与随码文档。其余（轮次笔记、归档件、历史日志）的死链允许丢弃，不为它们开修缮线。
6. **活引用 vs 历史记述**：**删 / 迁文件时只改活引用**；历史记述里的旧路径不修、不补指针。需要找回被删内容时用 `git log --diff-filter=D -- <path>`——历史的真源是 git + 带日期的记述，不是文件系统上的残留。

**引用方向：持久内容不指任务**：实例的规范/读物/长期材料不写任务目录（`<task-dir>/`）路径；任务可引用持久内容。向上引用会随任务归档断开，是**耦合缺陷**——修法是就地自述或把知识提升进持久区，不是改指向归档任务。

## 框架文件命名

| 文件 | 职责 |
|------|------|
| `FRAMEWORK.md` | 总纲（what & why） |
| `MANUAL.md` | 使用手册（how） |
| `CHANGELOG.md` | 变更历史 |
| `notes/spec/*.md` | 按需读取的现行规范 |
| `templates/*.md` | 结构模板（不是必建文件清单） |
