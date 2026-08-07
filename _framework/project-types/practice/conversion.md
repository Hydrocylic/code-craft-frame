# Practice 项目类型转换

> 类型: `practice`
> 本文件定义 practice 与框架其他三种项目类型之间的转换规则

---

## 转换总览

```
practice（轻量刷题）
    │
    ├── → reconstruction（重构学习）
    │    当某个题目涉及的知识点需要系统深入时，
    │    将该题目的核心算法/数据结构拆解为独立的 reconstruction 项目
    │
    └── → product（产出）
         当刷题过程中积累了可复用的工具集（如自定义数据结构库、
         算法模板库、测试框架），可抽象为 product 项目
```

Practice 是**单向输入型**——通常不从他类型转换到 practice（你不会把一本教科书的完整项目变成一道 LeetCode 题）。Practice 可以作为知识入口，触发更深度的学习项目。

## practice → reconstruction

### 触发条件

- 某道题涉及的知识体系需要系统学习（如"红黑树"不能靠一道题学完）
- 多道同类型题目需要统一整理（如"所有滑动窗口题"→ 拆解为一个 reconstruction 项目）
- 理解了算法但想从零实现一个完整版本

### 转换步骤

1. 建立 `projects/<name>/` 的完整骨架
2. 将原 practice 题目的代码放在 `experiments/<name>/src/` 作为参考起点
3. 设计 curriculum 轮次，从原理到实现逐步拆解
4. meta.yaml 中 `refs` 指向原始的 .cpp 文件路径

### 示例

```
LeetCodePractice/76.cpp  (滑动窗口 — 最小覆盖子串)
    ↓ 发现: 滑动窗口是一个需要系统学习的"模版类算法"
    ↓
projects/sliding-window/
├── src/          ← 从零实现通用滑动窗口框架
├── curriculum/
│   ├── r01-fixed-window/
│   ├── r02-variable-window/
│   └── r03-optimization/
└── experiments/
    └── lc76-reference/src/  ← 76.cpp 的原始代码放这里作为参考
```

## practice → product

### 触发条件

- 积累了可复用的工具代码（如 `leetcode-utils.hpp`：常用数据结构构造器、测试宏）
- 形成了可分享的算法模板库

### 转换步骤

1. 建立 `products/<name>/` 骨架
2. 将通用工具代码提取到 `src/`
3. 撰写 `docs/architecture.md` 说明设计
4. 在 tools 中保留对原始 practice 题目的引用

### 示例

```
LeetCodePractice/ (多道树相关题目中重复定义 TreeNode)
    ↓ 提取公共组件
products/leetcode-utils/
├── src/
│   ├── tree-utils.hpp    ← TreeNode 构造 + 打印
│   ├── list-utils.hpp    ← ListNode 构造 + 打印
│   └── test-macros.hpp   ← ASSERT_EQ 等测试宏
└── docs/
    └── architecture.md
```

## reference/reconstruction/product → practice

**不转换。** Practice 是单向的末端消费类型——你不会把一本教科书的系统学习项目降级为一道 LeetCode 题。

但可以从他类型中**提取**特定练习：
- 从 `reference/` 中读到的经典算法 → 在 practice 中写一道相关题验证理解
- 从 `reconstruction/` 中正在学的数据结构 → 在 practice 中找对应 LeetCode 题练手
