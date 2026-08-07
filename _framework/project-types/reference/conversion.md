# 参考项目类型转换规则

> 来源类型: reference
> 框架版本: v2.0

---

> **克制原则**: 转换操作必须遵循框架的四步流程 — 审计→提案→确认→执行。
> Phase 1-2（审计+出方案）是免费操作；Phase 4（结构调整+内容生成）必须等用户确认后才执行。
> Agent 辅助时，默认只到 Phase 2。详见 `MANUAL.md` §结构调整总则。

---

## reference → reconstruction

**触发条件**: 对参考项目的代码结构和核心机制有了足够理解，决定动手复现。

**转换步骤**（以下为 Phase 4 执行阶段的指引；Phase 1-2 的审计和方案必须先完成）：

1. **确认知识边界** — 从 `notes/` 中梳理已分析的知识点，确定课程轮次规划
2. **创建项目骨架** — 在 `projects/<name>/` 按 reconstruction SKELETON 创建目录
3. **填充 refs** — 在 `meta.yaml` 的 `refs` 中指向原参考项目
4. **设计首轮** — 从分析笔记中选择最有代表性的入口点，创建 `r01-<title>/`
5. **编写 code-refs** — 将 notes 中的代码引用映射为 `code-refs.md` 格式
6. **保留原参考** — reference 项目不删除，作为"标准答案"继续引用

**注意事项**:
- 不复制参考代码到 reconstruction 的 src/ — 自己写
- 原参考项目的 notes/ 可以继续更新（新发现），但主体笔记转移到 reconstruction 的 curriculum/
- Agent 辅助时：提供 `--from reference/<name> --to projects/<name>` 参数

---

## reference → product

**触发条件**: 理解透彻，决定从零构建产品级实现。

**转换步骤**:

1. **确认设计目标** — 产品的核心功能和目标用户
2. **创建产品骨架** — 在 `products/<name>/` 按 product SKELETON 创建目录
3. **撰写架构文档** — 基于对参考项目的理解，设计自己的架构
4. **标注参考来源** — 在 `docs/design-decisions.md` 中记录哪些设计参考了原项目
5. **保留原参考** — 不删除，作为后续迭代的参考

**注意事项**:
- Product 从零写代码，不复制参考代码（除非许可证允许且标注来源）
- 在 resume 中可以提及"研究了 X 项目后从零实现"
