# 产出项目类型转换规则

> 来源类型: product
> 框架版本: v2.0

---

> **克制原则**: 转换操作必须遵循框架的四步流程 — 审计→提案→确认→执行。
> 注意 product → reconstruction 是"自举"模式，产品代码充当参考角色，不应被修改。
> Agent 辅助时，默认只到 Phase 2。详见 `MANUAL.md` §结构调整总则。

---

## product → reconstruction

**触发条件**: 想深入理解产品中某部分实现的原理，退回学习模式进行系统性分析。

**转换步骤**（以下为 Phase 4 执行阶段的指引；Phase 1-2 的审计和方案必须先完成）：

1. **确定学习目标** — 想深入理解产品中的哪些模块/技术
2. **创建 reconstruction 骨架** — 在 `projects/<name>/` 创建目录
3. **设计轮次** — 将产品的 `docs/architecture.md` 按模块拆解为课程轮次
4. **填充 code-refs** — 指向产品自身 `src/` 中的关键实现（此时产品代码充当"参考"角色）
5. **建立实验** — 为关键模块创建隔离的实验环境，验证理解
6. **保留产品** — product 项目不删除，作为最终目标持续存在

**注意事项**:
- 这是一种"自举"模式：自己的产品代码作为自己的学习材料
- 在 reconstruction 的 `meta.yaml` 中 `refs` 指向原 product 项目
- 课程完成后可以反哺产品代码的质量提升

---

## product → product（版本迭代）

产品自身的版本迭代不需要类型转换。使用 `notes/iterations/v<NN>-*.md` 记录每次重大重构。

**Agent 辅助参数**: `--from products/<name> --to projects/<name>`

---

## product → reference

**触发条件**: 产品已成熟稳定，想将其作为"标准参考"供其他项目引用。罕见。

**转换步骤**:
1. 将产品代码以 submodule 或复制方式放入 `reference/`
2. 在 `notes/` 中撰写对该产品的分析解读
3. 原 product 继续维护，reference 中作为快照版本
