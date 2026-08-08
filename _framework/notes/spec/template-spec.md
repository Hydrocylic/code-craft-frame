# 模板规范

> 区域: spec（规范区）
> 框架版本: v2.0

---

## 模板设计原则

1. **语言无关** — 代码块使用 `<language>` 占位符，命令使用 `<run-command>` 占位符
2. **自文档** — 每个模板用 HTML 注释标注模板路径和适用位置
3. **占位符清晰** — 使用 `<描述>` 格式的占位符，便于查找替换
4. **注释指引** — 关键部分附带注释说明填写方式

## 模板完整性

框架必须包含以下模板：

| # | 模板文件 | 适用位置 |
|---|---------|---------|
| 1 | `meta.yaml` | 任何项目根目录 |
| 2 | `project-readme.md` | projects/或products/下的 README.md |
| 3 | `round-notes.md` | curriculum/r<NN>-<title>/notes.md |
| 4 | `qa.md` | curriculum/r<NN>-<title>/qa.md |
| 5 | `code-refs.md` | curriculum/r<NN>-<title>/code-refs.md |
| 6 | `experiment-notes.md` | experiments/<exp-name>/notes.md |
| 7 | `concept-note.md` | notes/concepts/<name>.md |
| 8 | `daily-note.md` | notes/daily/YYYY-MM-DD.md |
| 9 | `resume-project.md` | resume/resume.md |
| 10 | `CLAUDE.md` | 仓库根目录 CLAUDE.md |

## 模板元要求

每个模板文件必须包含：

1. **标题** — `# <模板用途>`
2. **注释头** — HTML 注释标注模板路径和适用位置
3. **节结构** — 清晰的 Markdown 节
4. **内联注释** — `<!-- 填写说明 -->` 格式的指引

## 占位符约定

| 占位符 | 含义 |
|--------|------|
| `<project-name>` | 项目名称 |
| `<name>` | 通用名称 |
| `<title>` | 标题（kebab-case 用于目录名，自由文本用于标题） |
| `<concept-name>` | 概念名称 |
| `<exp-name>` | 实验名称 |
| `<language>` | 编程语言标识 |
| `<run-command>` | 运行命令 |

## 数学公式书写规范

笔记中所有数学讨论**必须使用 LaTeX 语法**，不使用纯文本或 ASCII 艺术拼接。

**格式要求**：

| 场景 | 语法 | 示例 |
|------|------|------|
| 行内公式 | `$...$` | `$f(n) = f(n-1) + f(n-2)$` |
| 独立公式 | `$$...$$` | `$$f(n) = \sum_{i=1}^{m} a_i f(n-i)$$` |
| 矩阵 | `\begin{pmatrix}...\end{pmatrix}` | `$$\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$$` |
| 多行对齐 | `\begin{aligned}...\end{aligned}` | 推导步骤使用 `&` 对齐 |
| 上下标 | `_{}` `^{}` | `$M^{\,n-1}$`, `$a_{m}$` |
| 省略号 | `\cdots` `\vdots` `\ddots` | 按方向选用 |
| 求和/求积 | `\sum` `\prod` | `$\sum_{i=1}^{n}$` |

**禁止事项**：

- ❌ 禁止用纯文本代码块写矩阵或公式（如 `[1 1] [f(n-1)]`）
- ❌ 禁止用 ASCII 艺术画矩阵框线（如 `┌ ┐ │ └ ┘`）
- ❌ 禁止用 `^` 代替上标、`_` 代替下标而不加 `$` 包裹
- 允许：代码块包裹算法伪代码或程序逻辑（非数学公式）

**适用范围**：所有项目类型（practice / reference / reconstruction / product）的笔记文件中均适用本规范。
