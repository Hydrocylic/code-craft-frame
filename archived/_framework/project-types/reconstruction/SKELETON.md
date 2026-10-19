# 复制项目（重构项目）目录骨架

> 类型标识: `type: reconstruction`
> 框架版本: v2.0

---

## 定位

从参考项目中**拆解代码，逐步重构，理解结构**。

- 代码保留在项目中，共用运行环境和头文件
- 阶段构建和运行测试
- 课程轮次驱动：每个 round 聚焦一个知识/实现模块
- 实验是对轮次知识的验证和拓展

---

## 目录结构

```
projects/<name>/
├── README.md                    # 项目概述 & 参考项目指向
├── meta.yaml                    # type: reconstruction
├── CMakeLists.txt               # 项目级构建（可选，有编译需求时必建）
├── vcpkg.json / conanfile.txt   # 包管理清单（按需）

├── src/                         # ★ 重构后的源码（项目核心）
│   ├── include/                 #   头文件
│   └── *.cpp                    #   实现文件

├── shaders/                     # 着色器（图形学项目适用）
├── resources/                   # 重型资产框架
│   ├── README.md                #   资产来源 & 获取说明
│   └── .gitkeep                 #   资产文件 gitignored

├── cmake/                       # CMake 辅助模块

├── curriculum/                  # ★ 学习轮次
│   ├── README.md                #   轮次规划总览 & 依赖关系
│   └── r<NN>-<kebab-title>/
│       ├── notes.md             #   学习笔记（对参考项目的阅读分析）
│       ├── qa.md                #   问题与解答
│       └── code-refs.md         #   代码路径映射 → reference/

├── experiments/                 # ★ 动手实验
│   └── <exp-name>/
│       ├── src/                 #   实验代码（必须保留）
│       ├── outputs/             #   运行产物 [gitignored]
│       ├── notes.md             #   实验记录 & 复盘
│       └── run.ps1 / run.sh     #   运行指令脚本

├── resume/                      # 简历描述（项目完成标志）
│   └── resume.md

└── notes/                       # 项目内跨轮次笔记
    └── concepts/                #   跨轮次核心概念笔记
```

---

## 轮次设计原则

1. **独立可删** — 删除一个轮次不影响其他轮次
2. **可增补** — 随时可以插入新轮次（如 `r02b-<title>`）
3. **命名稳定** — 目录名用 kebab-case 描述主题，编号只表示推荐顺序
4. **收尾明确** — 每轮结束时在 `qa.md` 中记录"本轮未解决的问题"
5. **代码关联** — `code-refs.md` 中标注参考代码位置和本项目的对应实现

---

## 实验与轮次的关系

```
curriculum/r03-model-loading/     ← 理论学习
        ↓
experiments/model-loading-test/   ← 验证理解
        ↓
curriculum/r04-lighting/          ← 下一轮
```

- 一个轮次可以有 0-N 个实验
- 实验代码保留在 `experiments/<exp>/src/`，**不删除**
- 实验结果和复盘记录在 `notes.md` 中

---

## 构建约定

- 根构建文件定义项目级构建目标和公共依赖
- 每个实验可独立编译（通过子目录或独立构建文件）
- `src/` 中的库代码被所有实验共享
- `resources/` 中的重型资产 gitignored，通过脚本或手动获取

---

## 与其他项目类型的关系

- **reference → reconstruction**: 分析完成，开始重构
- **reconstruction → product**: 学习目标达成，整理为产品级代码

转换规则见 `conversion.md`。
