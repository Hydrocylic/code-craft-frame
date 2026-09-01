# git-practices — 仓库治理 git 实战实践（spec）

<!--
  位置: _framework/notes/spec/
  版本: 2026-08-26 创建（来源: renderer-lab 重组实战，已踩坑验证）
  状态: active
-->

以下实践来自 renderer-lab 单仓化改造的踩坑与验证（2026-08-25/26），适用于学习仓库的子模块治理与历史合并场景。

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
