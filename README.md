# code-craft-frame

跨工作区复用的通用协作框架（独立 Git，公开）。保存可迁移的规则、方法与模板；不保存产品、任务、个人或未公开内容。

## 使用方式

- 每个使用方在自己的工作区维护 `_framework/` 实例；本库是上游参考，不是 submodule。
- 按 commit 选择性采纳；不自动 pull、不自动合并、不覆盖实例已有规则。
- 实例的目录、角色词表、产品路径与命令权限属于实例策略，不因采纳本库文本而自动生效。
- **求同存异**：上游只收跨工作区成立的“最大公约数”；项目特色留在实例。不要求所有实例同版，不把单项目做法升级为默认。
- 采纳与提升的记录格式见 [`CHANGELOG.md`](_framework/CHANGELOG.md)；流程见 [`rule-sync-mechanism.md`](_framework/notes/spec/rule-sync-mechanism.md)。

## 入口

| 文件 | 职责 |
|---|---|
| [`AGENTS.md`](AGENTS.md) | agent 冷启动、阅读顺序与写入边界 |
| [`_framework/FRAMEWORK.md`](_framework/FRAMEWORK.md) | 总纲：边界与原则 |
| [`_framework/MANUAL.md`](_framework/MANUAL.md) | 操作手册 |
| [`_framework/notes/spec/`](_framework/notes/spec/) | 按需读取的现行规范 |
| [`_framework/templates/`](_framework/templates/) | 模板 |
| [`_framework/CHANGELOG.md`](_framework/CHANGELOG.md) | 变更账 |

## 当前内容

`_framework/` 当前是 v3.0 通用协作框架：总纲、手册、按需规范与模板。v2.0 学习框架的项目类型、agents 包、探讨区与旧模板已移入 [`archived/`](archived/README.md)，不再作为当前规则。

## 维护

作者副本维护；`commit` / `push` / tag 由仓库所有者执行。写入边界与目录职责见 [`AGENTS.md`](AGENTS.md)。提交或提升到上游前，按 [`sensitive-data-check.md`](_framework/notes/spec/sensitive-data-check.md) 做一次敏感信息自查。

## 许可证

MIT，见 [LICENSE](LICENSE)。贡献默认按同一许可证授权。
