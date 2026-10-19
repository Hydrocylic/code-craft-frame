# AGENTS — code-craft-frame

本库是通用框架上游，不是项目工作区。写入只限可跨工作区复用的规则、方法与模板。

## 开工

1. 本文件 → [`_framework/FRAMEWORK.md`](_framework/FRAMEWORK.md)（总纲）→ [`_framework/MANUAL.md`](_framework/MANUAL.md)（操作）。
2. 改规则前读 [`rule-sync-mechanism.md`](_framework/notes/spec/rule-sync-mechanism.md) 与 [`CHANGELOG.md`](_framework/CHANGELOG.md)。
3. 同一路径有并行写者时，先确认旧线已停；登记不是锁。

## 边界

- 只写通用内容；产品路径、任务编号、个人数据与未公开材料留在实例。单项目特色留实例，不升级为默认（求同存异）。
- 提交或提升到上游前，按 [`sensitive-data-check.md`](_framework/notes/spec/sensitive-data-check.md) 做一次敏感信息自查；扫描通过不等于没有泄露。
- 不自动同步、不覆盖实例规则；跨库写入需实例方用户授权。
- Git 写操作（commit / push / tag）由仓库所有者执行；只有当次任务明确授权时才例外。
- 结构调整先审计、出方案、等确认；不批量生成内容。
- 证据对应实际版本：区分已读、已运行、采信记录与未验证。

## 目录

| 路径 | 职责 |
|---|---|
| `_framework/FRAMEWORK.md` | 总纲：设计原则与边界 |
| `_framework/MANUAL.md` | 操作层：按任务阅读 |
| `_framework/notes/spec/` | 现行规范 |
| `_framework/scripts/` | 检查脚本（敏感信息扫描等） |
| `_framework/templates/` | 模板 |
| `_framework/private/` | 个人私有池；不写入通用内容 |
| `_framework/CHANGELOG.md` | 变更账 |
| `archived/` | 退役材料；不作为当前规则或授权依据 |
