# 参考项目（阅读项目）目录骨架

> 类型标识: `type: reference`
> 框架版本: v2.0

---

## 定位

**只读分析**。参考源码保持原样不动，最多部署运行以验证理解。
笔记记录对代码的分析和解读，不涉及拆解实现。

---

## 目录结构

```
reference/<name>/
├── README.md                    # 项目来源、获取方式、内容概述
├── meta.yaml                    # type: reference
├── notes/                       # 分析笔记（项目内自包含）
│   ├── overview.md              #   整体架构分析：模块划分、数据流、关键设计
│   └── <topic>.md               #   按主题的源码分析（文件级、函数级）
└── <source>/                    # 参考源码 [IMMUTABLE — 绝不修改]
```

---

## 各文件说明

### README.md

- 项目来源（URL、作者、许可证）
- 获取方式（git clone / 下载 / 手动复制）
- 代码规模概览（文件数、行数、语言）
- 部署运行说明（如有）
- 分析笔记索引

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

notes:                         # 分析笔记索引
  - notes/overview.md
  - notes/<topic>.md
```

### notes/

分析笔记的核心约定：

1. **文件名**用 kebab-case 描述分析主题
2. **每条分析**标注对应的源码文件和行号
3. **引用格式**: `<relative-path-from-project-root>:L<line>`
4. **可以包含**: 架构图（Mermaid）、运行输出截图、关键断点调试记录
5. **不需要**: curriculum 式的轮次结构、QA 对话、实验记录

笔记模板见 `_framework/templates/concept-note.md`（可按需扩展）。

---

## 与其他项目类型的关系

- **→ reconstruction**: 分析足够深入后，可创建复制项目，在 `refs` 中引用本参考项目
- **→ product**: 理解透彻后，可从零构建产品级实现，本参考项目作为设计参考

转换规则见 `conversion.md`。
