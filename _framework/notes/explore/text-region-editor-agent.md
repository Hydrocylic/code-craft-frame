# 局部区域文本修改 Agent 规划（text-region-editor）

> 区域: explore（探讨区）
> 框架版本: v2.0
> 创建: 2026-08-31
> 状态: ✅ 已确认（2026-08-31），待执行
> 来源: renderer-lab r04 qa.md Q10/Q11 文本整理实践

---

## 一、背景：一次局部修改的 token 账本

2026-08-31 整理 qa.md（260 行）中 Q10/Q11 两个 QA 条目（约占文件 25%）时，主会话的实际路径：

| 步骤 | 主会话消耗 |
|---|---|
| Read 全文定位区域 | 260 行全量入上下文 |
| 写一次性 Python 脚本 | ~150 行脚本 + 调试 |
| 二次 Read 核对拼接结果 | 85 行区域再入上下文 |
| Edit 修补脚本拼接的 2 处格式 bug | 2 次精确匹配往返 |

问题：**修改范围只占文件 1/4，上下文消耗却按整个文件计价**；脚本随用随弃，下次同样场景再写一遍。根因：

1. Edit 要求精确 old_string，而 Read 输出不显示尾随空格与行尾差异（CRLF/LF），逐字符抄写易失败 → 被迫转向脚本
2. 脚本没有沉淀位置，下一次从零开始
3. 主会话缺少"局部修改"纪律——先读全文找位置是默认动作

## 二、目标

一个专职"单文件局部区域文本更改"的 agent + 配套复用脚本：

1. 主会话 token 与文件大小**解耦**：只承载任务描述（路径 + 标记 + 新内容）与结果报告
2. 脚本资产沉淀复用，不再一次一写
3. 边界明确：区域级文本替换，不越界到结构调整（FRAMEWORK.md 决策 6 的四步流程不变）

## 三、现状审计

- 本仓库无 `.claude/agents/`，无任何自定义 agent
- `_framework/` 无 agents 概念；最相近组件是 `templates/CLAUDE.md`（"框架模板 → 仓库落位"的复制模式，FRAMEWORK.md §二）
- 上游 code-craft-frame 结构一致，同样无 agent 概念 → 本设计是框架的**新组件类型**，成熟后经 rule-sync 流程 2 回推

## 四、方案

### 4.1 Agent 包结构（canonical 在 _framework，激活副本在 .claude）

```
_framework/agents/                      # 新增：框架级 agent 组件区
├── README.md                           # agent 组件的安装/同步约定
└── text-region-editor/                 # 本 agent 包
    ├── agent.md                        # agent 定义（Claude Code frontmatter 格式）
    └── region-replace.py               # 复用脚本（与定义同版本管理）
```

激活方式：`agent.md` 复制到仓库 `.claude/agents/text-region-editor.md`（与 CLAUDE.md 模板 → 根目录同模式）；脚本不复制，agent 按相对路径调用 `_framework/agents/text-region-editor/region-replace.py`。框架拷贝到其他仓库时包整体跟随。

### 4.2 Agent 定义要点（text-region-editor）

- **职责**：单文件内的区域替换 / 插入 / 删除 / 格式改写。**内容由调用方（主会话）给定**，agent 是机械执行者——呼应"结构迁移 ≠ 内容填充"，agent 不做内容决策。
- **不做**：多文件移动/重命名/目录重组/批量新建（这些走结构调整四步流程）；不主动建议改什么内容。
- **工具**：Glob / Grep / Read / Edit / Bash（Bash 仅用于执行配套脚本；**不给 Write**——防止整文件重写绕开区域纪律）
- **模型**：不指定——继承环境配置的默认子 agent 模型；必要时主会话可 override
- **工作纪律**（token 控制核心，写入 agent 定义）：
  1. **定位用 Grep**（`-n` + head_limit），禁止整文件 Read 找位置
  2. **只读目标区域**：Read offset/limit 覆盖区域 ± 数行边界，不读区域外内容
  3. **改法二选一**：区域无尾随空格/行尾疑点 → Edit 精确替换；带空格/行尾/EOL 疑点 → 直接 region-replace.py，不再手工抄写
  4. **验证只回读改动区域**，不做全文件校验
  5. **报告固定格式**：文件、标记对、行数变化、改动摘要——不回传全文、不重复区域原文
- **失败语义**：标记不存在/不唯一、`--expect-lines` 行数不符 → 立即报错返回，不猜测、不扩大范围
- **范围指定格式**（调用方任务描述，写入 agent 定义）：

  ```
  文件: <path>
  范围: <start-marker> ~ <end-marker>    # 执行依据（Edit 模式为精确匹配的唯一字符串）
  定位线索: 约 L123–L145                  # 可选，仅辅助 Grep/Read 定位，不作为执行依据
  操作: 替换 / 插入 / 删除
  新内容: <...>
  ```

  行号不具约束力（文件被并行修改时会漂移）；范围约束由**机制**落实——Edit 只替换精确匹配段，脚本只重写标记之间，区域外字节原样不动。

### 4.3 复用脚本 region-replace.py

本次实践的定位-拼接逻辑泛化沉淀（Python 3 标准库，~150 行）：

| 模式 | 用法 | 说明 |
|---|---|---|
| 标记区域替换 | `--from-marker / --to-marker / --replace <file>` | 首选；含边界是否保留的选项 |
| 标记点插入 | `--insert-after / --insert-before <marker>` | 段落级增补 |
| 预览 | `--dry-run` | 只打印将要替换的区域，不落盘 |
| 防呆 | `--expect-lines N` | 替换区域行数与预期不符即 fail-fast 不改文件（防并发修改，2026-09-04 事故后增设） |

共性保证：EOL 自动检测保留（CRLF/LF）、UTF-8、fail-fast（标记缺失/不唯一/越界 → 非零退出且不改文件）、替换内容从 stdin 或文件读入（避免命令行转义问题）。**不做行号模式**（行号漂移不可控）；无唯一标记时 fail-fast 报错，由调用方提供更长的唯一标记，或改用 Edit 精确匹配。

### 4.4 框架集成步骤（确认后执行，不在本次范围）

1. 创建 `_framework/agents/` 包（README + agent.md + region-replace.py）
2. 观察期（已确认）：先只落 `_framework/agents/`，脚本 + 纪律在常规会话中试用几轮，**不激活**到 `.claude/agents/`
3. 观察通过后：复制激活 `.claude/agents/text-region-editor.md`；MANUAL.md 增补 "Agent 组件" 小节（定义格式、安装、同步约定）
4. `_framework/CHANGELOG.md` 落条目
5. 后续：renderer-lab 多轮验证 → code-craft-frame 回推（rule-sync 流程 2）

## 五、为什么是 agent 而不是别的东西

| 备选 | 评价 |
|---|---|
| 只沉淀脚本 | 最轻，但"不读全文、不改范围"的纪律无人执行，token 问题不解决 |
| Skill（指令包） | 指令加载进主会话，本身仍占用主上下文；agent 隔离上下文更彻底 |
| 专职 agent + 脚本 | 上下文隔离 + 资产复用 + 纪律可执行（工具收紧、失败语义）——本方案 |

预期对比：同类任务主会话从"600+ 行上下文（全文 + 脚本 + 核对）"降到"任务描述 + 报告约 20 行"。不引入新机制：Edit/Read/Grep 都是既有工具，agent 是纪律层，脚本是资产沉淀。

## 六、代价与局限

- 两处文件（`_framework/agents/` 与 `.claude/agents/`）需同步；约定"改 canonical → 重复制"，README 中写明
- 无唯一标记的区域需调用方提供更长标记（或改用 Edit）；标记失效时 agent 报错返回而非猜测
- 单次 agent 调用覆盖一个文件的一个区域；跨文件批量仍是结构调整流程
- agent 定义是 Claude Code 的机制（`.claude/agents/*.md`），其他 AI 工具不一定兼容——框架层留说明即可，不为此抽象

## 七、已确认决策（2026-08-31）

1. **名称**：`text-region-editor`
2. **模型**：不指定，继承环境配置的默认子 agent 模型
3. **脚本模式**：仅标记模式（区域替换/插入/dry-run），不做行号模式
4. **激活方式**：先只落 `_framework/agents/` 观察几轮，观察通过后再复制到 `.claude/agents/` 激活
5. **工具**：Glob / Grep / Read / Edit / Bash；不给 Write——写文件能力由 Edit（匹配即范围）与脚本（标记即范围）提供，范围由机制锁死，不靠约定
6. **并发防呆**（2026-09-04 事故后增设）：脚本 `--expect-lines N` 行数校验 + 纪律"改前必验"（落盘前 dry-run 核对区域行数/首尾行）——标记防"位置错"，行数校验防"内容变"
