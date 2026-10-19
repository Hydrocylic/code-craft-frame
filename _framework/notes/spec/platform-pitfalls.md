# platform-pitfalls — 跨平台操作坑（spec）

<!--
  区域: spec（规范区）
  创建: 2026-09-22（来源: 多次实测翻车；均非项目逻辑问题但都白烧时间）
  状态: active（每条都有实测）
  关联: git-practices.md、test-preflight.md、任务工作流的人工步骤收尾
  写法: 每条三段——**症状**（你看到什么）→ **判法**（怎么一眼确认是这条）→ **正解**（怎么做）
-->

## 1. Windows 目录联接（junction）：**不要用 `Remove-Item -Recurse` 删**

**症状**：删一个“链接目录”时，目标里的文件**一起被删掉了**。

**判法**：`Get-Item <路径> | Select-Object LinkType, Target`——`LinkType = Junction` 即联接；或看目录图标（带箭头的小方块）。**取消链接与删除内容在文件系统里长得很像**。

**正解**：删链接用 **`cmd /c rmdir <路径>`**（只断链，不动目标）；`Remove-Item -Recurse` 会**穿透**链接把目标内容一并删掉（实测：差点删掉主仓数十个重资产文件）。

**建链接**（装配 worktree 时共享大资产）：`New-Item -ItemType Junction -Path <新路径> -Target <主仓路径>`。

## 2. git 子模块常在 detached HEAD：普通 `git push` 会“无事可做”

**症状**：在子模块里提交了，`git push` 却提示“Everything up-to-date”或“no upstream”；提交只躺在本地。

**判法**：`git -C <子模块路径> status` 首行显示 `HEAD detached at <sha>` 或 `HEAD detached from …`；`git -C <子模块路径> log --oneline origin/<分支>..HEAD` 列出“推不上去”的提交。

**正解**：显式推 HEAD 到目标分支——`git push origin HEAD:master`（或 `main`）；想留在分支上就先 `git switch -c <tmp-branch>` 再推、再回主仓更新 pin。

## 3. GitHub Pages 项目站在子路径：绝对路径一律 404

**症状**：本地 `npm run dev` 正常，发布到 `https://<user>.github.io/<repo>/` 后**资源全 404**。

**判法**：`Ctrl+U` 看首页源码——引用写成 `/assets/…`、`/textures/…`、`/src/main.js`（**以 `/` 开头**）就是绝对路径 ⇒ 在子路径下必然 404；写成 `./assets/…` 才对。

**正解**：① 构建产物用**相对路径**（Vite 的 `base: './'`）；② 发布源显式指向 `gh-pages` 分支——**发布设置里分支下拉“只有 master”是正常的**，把分支推上去后它才会出现；③ 发布后**必须**做一次“人工收尾判据”（打开首页看引用前缀），把它写进人工任务单。

## 4. 沙箱用户 ≠ 目录属主 ⇒ git 全是 `dubious ownership`（**连只读查询也会失败**）

**症状**：`git status` / `git log` 一律报 `detected dubious ownership in repository at '<path>'`，并给出“add an exception”提示——**只读查询也过不去**，而本框架口径是“**git 只读查询 Agent 可自行执行**”。

**成因**：沙箱进程的用户与工作区目录属主不是同一个。

**解法**：**逐条命令带参数**（不改全局配置）——`git -c safe.directory='*' -C <repo> <cmd>`（或 `<具体路径>`）。用户侧若想永久免除：`git config --global --add safe.directory <repo>`（由用户执行）。

## 5. `git submodule` 子命令只在 Git Bash 里能跑

**症状**：PowerShell 里跑 `git submodule status|update|add` 报 `.: git-sh-setup: file not found`（或 `basename` / `sed` 找不到）。

**成因**：mingw 的 `git-submodule` 是 shell 脚本，依赖 Git Bash 提供的工具链。

**解法**：子模块类命令**在 Git Bash 执行**（或由用户执行）；本框架口径 = **git 写指令一律由用户执行**，只有只读查询可由 Agent 跑（走第 4 条的 `-c safe.directory`）。
