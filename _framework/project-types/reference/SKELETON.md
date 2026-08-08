# 参考项目（阅读项目）目录骨架

> 类型标识: `type: reference`
> 框架版本: v2.0
> 最后更新: 2026-08-08 — 移除 notes/，分析笔记归属 reconstruction 项目

---

## 定位

**只读参考**。参考源码保持原样不动，最多部署运行以验证理解。

参考项目本身**不包含分析笔记**。对参考代码的分析和解读归属到重建项目（`projects/`）的 curriculum 中，通过 `code-refs.md` 建立映射。这样设计的原因是：
- 分析笔记服务于"拆解学习"动作，天然属于 reconstruction 项目
- 避免同一份参考代码的分析散落在多处
- reference/ 保持源码级纯净，便于跨项目复用

---

## 目录结构

```
reference/<name>/
├── README.md                    # 项目来源、获取方式、内容概述
├── meta.yaml                    # type: reference
├── RESOURCES.md                 # 归档资源说明（数据集、权重等，如有）
└── <source>/                    # 参考源码 [IMMUTABLE — 绝不修改]
```

**不含**:
- `notes/` — 分析笔记在 `projects/<name>/curriculum/` 的 `code-refs.md` 中建立映射
- `curriculum/` — reference 不涉及课程轮次
- `experiments/` — reference 不涉及实验
- `resume/` — reference 不独立产出简历

---

## 各文件说明

### README.md

- 项目来源（URL、作者、许可证）
- 获取方式（git clone / 下载 / 手动复制）
- 代码规模概览（文件数、行数、语言）
- 部署运行说明（如有）

### meta.yaml

```yaml
project: <name>
type: reference
status: active                  # active | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
description: >
  项目来源和内容概述。

source:
  url: <原始URL或"manual">      # 获取来源
  license: <许可证>
  language: <编程语言>
  lines: <大约行数>

# 可选字段:
# tags: [<domain-1>, <domain-2>]
```

### RESOURCES.md（可选）

记录参考代码依赖的外部资源（数据集、预训练权重等），包括：
- 资源内容说明
- 获取方式（URL、网盘等）
- 解压后的目录结构要求

---

## 如何使用参考项目

1. **阅读阶段**: 直接阅读源码，理解架构和关键实现
2. **分析阶段**: 在 `projects/<name>/curriculum/r<NN>-<title>/code-refs.md` 中建立代码路径映射
3. **实验阶段**: 在 reconstruction 项目的 `experiments/` 中基于理解进行复现和验证

引用格式：
```markdown
# reference/<name>/<file>:L<start>-L<end>
```

---

## 与其他项目类型的关系

- **→ reconstruction**: 创建重建项目，通过 `code-refs.md` 建立映射；在 curriculum 中逐轮分析
- **→ product**: 理解透彻后，从零构建产品级实现

转换规则见 `conversion.md`。
