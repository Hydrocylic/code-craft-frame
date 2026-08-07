# 项目类型体系

> 框架版本: v2.0

---

## 三种项目类型

| 类型 | 目录 | 一句话 | 核心动作 |
|------|------|--------|---------|
| **reference**（参考/阅读） | `reference/` | 只读分析，源码不动 | 阅读 → 分析 → 笔记 |
| **reconstruction**（复制/重构） | `projects/` | 拆解参考，逐步重构 | 轮次 → 实验 → 简历 |
| **product**（产出/产品） | `products/` | 产出完备产品代码 | 设计 → 迭代 → 展示 |

---

## 选择指南

```
要深入理解一个现有项目？
├── 只看不写 → reference
└── 动手复现 → reconstruction

要从零产出可展示的产品？
├── 基于学习成果 → reconstruction → product
└── 直接构建 → product

项目做到一半想改变方向？
└── 查看对应类型的 conversion.md
```

---

## 项目类型转换图

```
reference ──→ reconstruction ──→ product
    │               │                 │
    │               ↓                 │
    │           reference             │
    │         (罕见降级)              │
    │                                 │
    └─────────→ product ──────────────┘
              (直接构建)    (自举学习)──→ reconstruction
```

---

## 各类型的详细骨架

- [reference/SKELETON.md](reference/SKELETON.md)
- [reconstruction/SKELETON.md](reconstruction/SKELETON.md)
- [product/SKELETON.md](product/SKELETON.md)

## 转换规则

- [reference/conversion.md](reference/conversion.md)
- [reconstruction/conversion.md](reconstruction/conversion.md)
- [product/conversion.md](product/conversion.md)
