# 命名约定

> 区域: spec（规范区）
> 框架版本: v2.0

---

## 目录命名

| 元素 | 约定 | 示例 |
|------|------|------|
| 项目名称 | kebab-case | `cpp-concurrency`, `diffusion-models` |
| 轮次目录 | `r<NN>-<kebab-title>` | `r01-memory-model`, `r03b-data-pipeline` |
| 实验目录 | kebab-case，动词-对象 | `conv2d-playground`, `lora-rank-sweep` |
| 概念笔记 | kebab-case | `virtual-dispatch.md`, `attention-mechanism.md` |
| 每日笔记 | `YYYY-MM-DD.md` | `2026-08-07.md` |
| 迭代记录 | `v<NN>-<kebab-title>.md` | `v01-refactor-build-system.md` |

## 字段命名（meta.yaml）

| 字段 | 类型 | 说明 |
|------|------|------|
| `project` | string | 项目短名，与目录名一致 |
| `type` | enum | `reference \| reconstruction \| product` |
| `status` | enum | `planned → in-progress → completed → archived` |
| `created` | date | 创建日期，ISO 格式 |
| `updated` | date | 最后更新日期 |
| `refs` | list | 参考项目路径列表 |
| `rounds` | list | 轮次目录名列表（reconstruction 专用） |
| `resume` | path | 简历文件相对路径 |

## 模板文件命名

- 模板文件名应**描述其内容**，而非描述其位置
- `round-notes.md` 而非 `curriculum-template.md`
- 模板内注释标注适用位置

## 框架文件命名

| 文件 | 职责 |
|------|------|
| `FRAMEWORK.md` | 方法论（what & why） |
| `MANUAL.md` | 使用手册（how） |
| `CHANGELOG.md` | 变更历史 |
| `SKELETON.md` | 目录骨架（每个项目类型） |
| `conversion.md` | 类型转换规则（每个项目类型） |
