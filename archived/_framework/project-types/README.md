# 项目类型体系

> 框架版本: v2.0

---

## 四种项目类型

| 类型 | 目录 | 一句话 | 核心动作 |
|------|------|--------|---------|
| **practice**（练习/刷题） | `<practice-dir>/` | 高频轻量，单文件单题 | 刷题 → 笔记 → 积累 |
| **reference**（参考/阅读） | `reference/` | 只读参考，源码不动（不含笔记） | 阅读 → 分析（笔记在 reconstruction 中） |
| **reconstruction**（复制/重构） | `projects/` | 拆解参考，逐步重构 | 轮次 → 实验 → 简历 |
| **product**（产出/产品） | `products/` | 产出完备产品代码 | 设计 → 迭代 → 展示 |

---

## 选择指南

```
要刷算法/面试题？
└── practice（单文件，每题独立）

要深入理解一个现有项目？
├── 只看不写 → reference
└── 动手复现 → reconstruction

要从零产出可展示的产品？
├── 基于学习成果 → reconstruction → product
└── 直接构建 → product

刷题过程中发现需要系统学习的知识点？
└── practice → reconstruction（见 conversion.md）

项目做到一半想改变方向？
└── 查看对应类型的 conversion.md
```

---

## 项目类型转换图

```
practice ──→ reconstruction ──→ product
   │              │                 │
   │              ↓                 │
   │          reference             │
   │        (罕见降级)              │
   │                                │
   └────────→ product ──────────────┘
            (工具提取)    (自举学习)──→ reconstruction

reference ──→ reconstruction ──→ product
    │               │                 │
    │               ↓                 │
    │           reference             │
    │         (罕见降级)              │
    │                                 │
    └─────────→ product ──────────────┘
```

---

## 各类型的详细骨架

- [practice/SKELETON.md](practice/SKELETON.md) — 轻量刷题模式
- [reference/SKELETON.md](reference/SKELETON.md)
- [reconstruction/SKELETON.md](reconstruction/SKELETON.md)
- [product/SKELETON.md](product/SKELETON.md)

## 转换规则

- [practice/conversion.md](practice/conversion.md)
- [reference/conversion.md](reference/conversion.md)
- [reconstruction/conversion.md](reconstruction/conversion.md)
- [product/conversion.md](product/conversion.md)
