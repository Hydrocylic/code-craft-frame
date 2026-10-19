# 复制项目类型转换规则

> 来源类型: reconstruction
> 框架版本: v2.0

---

> **克制原则**: 转换操作必须遵循框架的四步流程 — 审计→提案→确认→执行。
> 尤其 reconstruction → product 这种大规模转换，审计阶段（代码审计、笔记审计、依赖梳理）是所有后续步骤的前提。
> Agent 辅助时，默认只到 Phase 2。详见 `MANUAL.md` §结构调整总则。

---

## reconstruction → product

**触发条件**: 课程轮次基本完成，对领域知识有了系统性掌握，希望整理出可用于展示和复用的产品级代码。

**转换步骤**（以下为 Phase 4 执行阶段的指引；Phase 1-2 的审计和方案必须先完成）：

1. **审计现有代码**
   - 遍历 `src/` 和 `experiments/*/src/`，列出所有代码文件
   - 识别核心代码 vs 实验探索代码 vs 废弃代码
   - 标记依赖关系

2. **规划产品 src/**
   - 将分散在各实验中的核心实现收敛到统一的 `src/` 结构
   - 清理实验特有的临时代码、调试代码
   - 确定公共 API 和模块边界

3. **转换笔记**
   - 从 `curriculum/r<NN>-*/notes.md` 中提取关键技术决策 → `docs/design-decisions.md`
   - 从 `curriculum/r<NN>-*/qa.md` 中提取常见问题 → 补充到 README FAQ
   - 从 `notes/concepts/` 中提取核心概念 → `docs/architecture.md`

4. **简化构建**
   - 移除以实验为粒度的构建目标
   - 统一为面向最终用户的构建入口
   - 添加安装规则（如有）

5. **撰写文档**
   - README.md: 快速开始 + 功能列表 + 依赖说明
   - docs/architecture.md: 架构设计
   - docs/changelog.md: 从 curriculum rounds 中提取版本演进

6. **创建 resume**
   - 从 reconstruction resume 升级为 product resume
   - 侧重"从零构建了什么"而非"学习了什么"

7. **归档原始结构**（可选）
   - 将原 reconstruction 目录整体归档或标记 `status: archived`
   - 在 product 的 `meta.yaml` 中标注 `derived_from: projects/<name>`

**Agent 辅助参数**: `--from projects/<name> --to products/<name>`

---

## reconstruction → reconstruction（拆分/合并）

**触发条件**: 一个 reconstruction 项目的范围过大或过小，需要重新划分。

**拆分**:
1. 确定拆分边界（按 curriculum round 或 experiments）
2. 为每个子项目创建独立骨架
3. 共享的 `src/` 库代码提取到公共位置
4. 更新 `refs` 和交叉引用

**合并**:
1. 确定合并后的统一项目名
2. 合并 `curriculum/` 轮次，去重
3. 合并 `experiments/`，保持原有目录名
4. 统一 `meta.yaml` 的 `refs` 列表

---

## reconstruction → reference（降级）

**触发条件**: 发现某个主题更适合阅读分析而非动手重构。罕见但可能。

**转换步骤**:
1. 将重构过程中积累的分析笔记保留在 reconstruction 项目的 curriculum/ 中（不迁移到 reference）
2. 保留有价值的实验代码作为参考补充说明
3. `src/` 中的重构代码可保留作为"理解验证"的产物
