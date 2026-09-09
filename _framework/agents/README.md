# Agent 组件区（_framework/agents）

> 框架版本: v2.0
> 创建: 2026-08-31
> 状态: 首个组件 text-region-editor 观察期（未激活）

## 定位

框架级的 **Claude Code 自定义 agent 定义 + 配套资产**。区别于 `templates/`（模板）与 `project-types/`（骨架）：本目录存放可直接复制的 agent 包——每个包一个目录，包含 agent 定义与它专属的脚本/数据。

规划与决策记录见 `_framework/notes/explore/text-region-editor-agent.md`。

## 目录约定

```
_framework/agents/
├── README.md                       # 本文件
└── <agent-name>/                   # 一个 agent 一个包
    ├── agent.md                    # agent 定义（frontmatter: name/description/tools）
    └── <配套脚本或数据>             # 随包版本管理，不单独复制
```

## 安装 / 激活

1. 把 `<agent-name>/agent.md` 复制到目标仓库的 `.claude/agents/<agent-name>.md`
2. 配套脚本**不复制**：agent 在仓库根目录运行，按相对路径调用 `_framework/agents/<agent-name>/<script>`
3. 框架整体拷贝到其他仓库时，本目录随 `_framework/` 整体迁移，路径引用自动成立

## 同步约定

- canonical 在 `_framework/agents/`；`.claude/agents/` 中的是激活副本
- 修改流程：改 canonical → 重新复制激活副本（两处不同步编辑）
- 观察期内的 agent **不激活**：只在常规会话中以"纪律 + 脚本"方式试用，观察通过后再复制激活

## 当前组件

| 组件 | 状态 | 说明 |
|---|---|---|
| text-region-editor | 观察期（未激活） | 单文件局部区域文本替换/插入；配套 region-replace.py（标记模式） |
