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
