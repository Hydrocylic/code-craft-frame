# 产出项目（产品项目）目录骨架

> 类型标识: `type: product`
> 框架版本: v2.0

---

## 定位

**产出完备的产品代码**，供开源、应用和展示。

- 结构设计反复重构调整以达到产品级质量
- 代码版本通过笔记系统保留（changelog + 架构文档）
- 展示整洁，面向最终用户和评审者
- 不需要 curriculum 轮次（那是学习过程的产物）

---

## 目录结构

```
products/<name>/
├── README.md                    # 项目介绍、快速开始、使用文档
├── LICENSE                      # 开源许可证
├── meta.yaml                    # type: product
├── CMakeLists.txt               # 构建入口

├── src/                         # ★ 产品源码
│   ├── include/                 #   公共头文件
│   └── *.cpp                    #   实现文件

├── shaders/                     # 着色器（图形学项目适用）
├── resources/                   # 资产（可提交或 gitignored，视大小而定）

├── docs/                        # ★ 架构文档 + 重构记录
│   ├── architecture.md          #   整体架构设计
│   ├── changelog.md             #   轻量级变更日志（版本迭代记录）
│   └── design-decisions.md      #   关键设计决策 & 权衡

├── tests/                       # 测试（可选）

├── examples/                    # 使用示例（可选）

├── resume/                      # 简历描述
│   └── resume.md

└── notes/                       # 笔记系统
    ├── iterations/              #   重构迭代记录（保留历史代码版本）
    │   └── v<NN>-<title>.md     #   每次重构的原因、过程、结果
    └── concepts/                #   核心技术概念笔记
```

---

## 与 reconstruction 的关键差异

| 维度 | reconstruction | product |
|------|---------------|---------|
| 目标 | 理解结构 | 产出产品 |
| 轮次 | curriculum/ 驱动 | docs/changelog.md 驱动 |
| 代码组织 | 分散在 experiments/ | 统一在 src/ |
| 质量要求 | 跑通即可 | 产品级，含测试和文档 |
| 展示性 | 不对外的学习笔记 | 面向用户的清晰文档 |
| 笔记 | 课程轮次 notes + QA | 迭代记录 + 架构文档 |

---

## 重构迭代记录规范

`notes/iterations/v<NN>-<title>.md` 记录每次重大重构：

```markdown
# v01 — <重构标题>

**日期**: YYYY-MM-DD
**触发原因**: <!-- 为什么这次重构？ -->

## 变更内容

- 旧: <之前的做法>
- 新: <之后的做法>
- 原因: <为什么改>

## 影响范围

- 修改的文件: ...
- 破坏性变更: 是/否

## 复盘

- 做得好的: ...
- 可以改进的: ...
```

---

## 代码整洁 vs 笔记丰富

产出项目面向展示，源代码区（`src/`、`docs/`）保持整洁；详细的迭代思考记录在 `notes/`。

如果你希望代码仓库完全纯净（例如作为独立开源项目发布），可将 `notes/` 中的迭代记录外置到全局 `notes/products/<name>/`，使产品目录仅保留代码和核心文档。

---

## 与其他项目类型的关系

- **reconstruction → product**: 课程完成，整理为产品
- **product → reconstruction**: 想深入理解某部分，退回学习模式

转换规则见 `conversion.md`。
