# git-practices — 仓库治理 git 实战实践（spec）

<!--
  位置: _framework/notes/spec/
  版本: 2026-08-26 创建（来源: renderer-lab 重组实战，已踩坑验证）
  状态: active
-->

以下实践来自 renderer-lab 单仓化改造与多 Agent 协作的踩坑与验证（2026-08-25 ~ 09-16），
适用于学习仓库的子模块治理、历史合并，以及「Agent 写指令、人类执行」的命令交接场景。

## 1. 去子模块的正确顺序

**不要执行 `git submodule deinit`** —— 它会清空工作目录内容（已实际踩坑）。

```bash
# 先取回内容（远程尚在时）
git submodule update --init --depth 1 <path>
# 删除目录内 .git 指针文件与模块缓存（保留文件内容）
rm -f <path>/.git
rm -rf .git/modules/<path>
# 最后从索引移除 gitlink
git rm --cached --ignore-unmatch <path>
```

## 2. 子模块历史并入单仓（保留历史 + 过滤大文件）

用 `git filter-repo` 两段式重写后再合入：

```bash
# 第一段：从全历史滤除大文件（如纹理/资源）
git clone <remote-url> /tmp/import-<name>
cd /tmp/import-<name>
git filter-repo --invert-paths --path <大文件路径1> --path <大文件路径2> --force
# 第二段：把剩余文件挪到目标前缀下
git filter-repo --to-subdirectory-filter projects/<name> --force

# 主仓库侧：先提交 gitlink 移除，且把工作目录内容移开（避免 untracked 冲突）
git fetch /tmp/import-<name> HEAD:refs/heads/import-<name>
git merge --allow-unrelated-histories import-<name>
git branch -d import-<name>
```

要点：① 先提交 gitlink 移除再 merge（无关联历史的合并以空树为基，不会与 gitlink 冲突）；② merge 前把工作区同名未跟踪文件移开；③ 被滤除的大文件如需本地保留，从备份拷回并写入 .gitignore。

## 3. `git rm --cached` 与 `submodule update` 的顺序陷阱

先 `rm --cached` 后 `submodule update <path>` 会报 `pathspec did not match`（索引中 gitlink 已消失）。恢复：先 `git restore --staged <path>` 再 update；`rm --cached` 放到取回完成之后。

## 4. GitHub 账号改名后的旧 URL

GitHub 账号改名后，旧用户名 URL 会 301 重定向到新用户名，clone/fetch 仍可用——但旧用户名将来可能被他人注册，重定向会失效或指向错误。**文档与指令一律使用新用户名 URL**，不得依赖重定向。

## 5. Windows schannel TLS 瞬断处置顺序

报错特征：`schannel: failed to receive handshake` / `server closed abruptly` / `early EOF`。

按序尝试：① 重试同一条命令；② `git config --global http.sslBackend openssl`；③ 检查/取消代理（`git config --global --get http.proxy`，有值则 `--unset`）；④ 改用 SSH URL。

## 7. 命令交接纪律（Agent 把指令交给人类执行时的写法）

背景：同一套指令在 2026-09-16 连续踩两次坑——① 给的是 PowerShell `foreach`，用户在 **bash** 里跑，报
`syntax error near unexpected token '$b'`；② 单行 `foreach { A B }` 里两条命令**没写 `;`**，PowerShell 把
`git tag "slice/$b" $b git branch -d $b` 当成**一条** `git tag` 调用（`-d` 被解析成删除选项），连报 5 条
`tag '…' not found`。两次都不是 git 问题，是**交接写法问题**。

**写法纪律**：

1. **先声明 shell**：每段命令块标注 `PowerShell` / `Git Bash` / `cmd`，不指望读者自行切换。
2. **少语法、多重复**：能展开成显式多行就别用循环、管道、变量替换——一次跑通的成本低于多写十行。
3. **循环体里多条命令必须用 `;` 分隔**（或换行），否则会被拼成一条命令。
4. **先只读、后写入**，分两步给：第一步输出用于确认前提（如 `git branch -v`、`git ls-files --stage`），
   前提不成立就停。
5. **给出预期输出**：一句话说明"正常应该看到什么"，让用户能自行判断成败（如"首列应为 `160000`"）。
6. **破坏性动作给安全档位**：用 `-d` 而非 `-D`、`--cached` 而非直接删——让工具在前提不成立时**拒绝执行**。

## 8. `git checkout <ref> -- <path>` 的覆盖语义（取值合并前先看工作区）

合并时常用 `git checkout <ref> -- <path>` 把某路径整体换成目标 ref 的版本（跳过当前分支的改动）。
它的语义是「**用 `<ref>` 的版本覆盖索引与工作区**」——**该路径下的未提交改动会被静默丢弃**，
不警告、不 stash、不进 reflog。

2026-09-16 实测：`git checkout <主干> -- <目录>` 抹掉了当天写在该目录下三处文件的未提交内容
（后依会话留档重写恢复）。

**纪律**：

1. 执行前先 `git status --short`；**有未提交改动就先提交**（或先 `git stash`）。
2. 取值范围能缩就缩：能写具体文件就不写整个目录。
3. 已被抹掉时：先查 `git stash list` 与会话留档；`git fsck --lost-found` 只在极端情况下有用（dangling blob 不保证存在）。
