# git-practices — 仓库治理 git 实战实践（spec）

<!--
  位置: _framework/notes/spec/
  版本: v3.0（2026-10-19 由实例实践回推并去实例化）
  状态: active
  说明: 通用 git 实战；涉及具体检出名、分支名、路径的地方标为“可选实践”或占位符，实例可按自身布局替换。
-->

以下实践来自多个实例的单仓化改造、多 Agent 协作与命令交接踩坑验证，适用于子模块治理、历史合并，以及“Agent 写指令、人类执行”的交接场景。

<a id="commit-message"></a>

## 0. Commit message（唯一正本）

**起草消息也必须遵守本节**，不以是否执行 Git 为条件。旧任务单、旧模板及历史长消息不作为新提交的格式依据。

**共同约束**：英文祈使式，动词开头，一句话，最多 72 字符。

1. **默认只有一行，无正文**；该行 **≤72 个字符，空格与标点均计入**。不得用分号、破折号堆叠改动清单；超长就提炼主要变化，不截断单词或改用晦涩缩写凑数。
2. **不写内部轮次号、任务号、REQ 号、agent ID 或角色/库名前缀**（如 `r04 T7:`、`framework-261013:`、`notes:`）；不写测试数字、构建体积或 `Green:`。
3. 细节、原因、验证证据和交接事项放对应日志/交付件，不塞进消息。只有用户对本次提交明确要求时才附正文或采用其他格式；不能从旧例推定例外。
4. **交付前自检**：确认目标检出与实际改动，逐字计数，检查英文、动词开头、单行和禁写内容；给用户可直接复制的 message，不把字符计数或解释写进 message。默认只给消息，不给提交命令；Git 写权限仍按 §9。
5. **不追改旧历史**：旧长消息保留；修改规则不授权 amend、rebase、重写历史或强推。

合格示例（只是格式示例，不代表这些改动已完成）：

```text
Clarify commit message rules
Fix layer visibility after AI edits
```

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
git filter-repo --to-subdirectory-filter <target-prefix> --force

# 主仓库侧：先提交 gitlink 移除，且把工作目录内容移开（避免 untracked 冲突）
git fetch /tmp/import-<name> HEAD:refs/heads/import-<name>
git merge --allow-unrelated-histories import-<name>
git branch -d import-<name>
```

要点：① 先提交 gitlink 移除再 merge（无关联历史的合并以空树为基，不会与 gitlink 冲突）；② merge 前把工作区同名未跟踪文件移开；③ 被滤除的大文件如需本地保留，从备份拷回并写入 `.gitignore`。

## 3. `git rm --cached` 与 `submodule update` 的顺序陷阱

先 `rm --cached` 后 `submodule update <path>` 会报 `pathspec did not match`（索引中 gitlink 已消失）。恢复：先 `git restore --staged <path>` 再 update；`rm --cached` 放到取回完成之后。

## 4. GitHub 账号改名后的旧 URL

GitHub 账号改名后，旧用户名 URL 会 301 重定向到新用户名，clone/fetch 仍可用——但旧用户名将来可能被他人注册，重定向会失效或指向错误。**文档与指令一律使用新用户名 URL**，不得依赖重定向。

## 5. Windows schannel TLS 瞬断处置顺序

报错特征：`schannel: failed to receive handshake` / `server closed abruptly` / `early EOF`。

按序尝试：① 重试同一条命令；② `git config --global http.sslBackend openssl`；③ 检查/取消代理（`git config --global --get http.proxy`，有值则 `--unset`）；④ 改用 SSH URL。

## 6. 子模块登记的正确顺序与「嵌套仓库 gitlink」陷阱

**先有远端提交，再登记子模块。** 对一个刚建好的空仓库执行 `git submodule add` 会失败（远端没有可指向的提交）。

**错误顺序**：

```text
git clone <url> <path>              # 先把仓库克隆到最终路径
（往里面放内容、提交、push）
git add -A                           # ← 灾难点：此时目标路径已是「嵌套仓库」
git submodule add <url> <path>
# → fatal: '<path>' already exists in the index
```

原理：索引里一旦存在该路径的条目，`git submodule add` 的前置检查就会拒绝——它会写 `.gitmodules`、但**不会**帮你把索引条目换成 gitlink。而 `git add -A` 遇到嵌套仓库时记的不是文件，而是一个 **gitlink**（mode `160000`，只存一个提交号）。此时即便把目录 `rm -rf` 删掉，**索引条目依然在**（工作区删除 ≠ 索引删除），下一次 `submodule add` 仍然报同一个错。

**正确顺序**：

```bash
# 1) 在仓库外的暂存位置（或临时 clone）准备内容并 push 首个提交
# 2) 回到主仓登记子模块——git 会自己 clone 到目标路径
git submodule add <url> <path>
git add .gitmodules <path>
git commit -m "<message>"
```

**已经踩了怎么办（修复）**：索引里已是 gitlink、`.gitmodules` 也已有条目时，**就地补完**比推倒重来简单：

```bash
git submodule update --init <path>     # 按索引里的提交号把工作区克隆回来
git add .gitmodules <path>
git commit -m "<message>"
```

若必须重来，要先清索引与 `.gitmodules` 两处：

```bash
git rm --cached <path>                                   # 清索引条目（不碰工作区）
git config -f .gitmodules --remove-section submodule.<path>   # 清 .gitmodules 条目
git add .gitmodules && git commit -m "Drop half-registered submodule"
git submodule add <url> <path>
```

**排查命令（只读）**：`git ls-files --stage -- <path>` —— 输出首列 `160000` 即 gitlink，末列路径即索引中的真实路径（不要靠 `ls` 判断，索引与工作区是两回事）。

## 7. 命令交接纪律（Agent 把指令交给人类执行时的写法）

背景：同一套指令连续踩两次坑——① 给的是 PowerShell `foreach`，用户在 **bash** 里跑，报 `syntax error near unexpected token`；② 单行 `foreach { A B }` 里两条命令**没写 `;`**，PowerShell 把两条命令拼成一条。两次都不是 git 问题，是**交接写法问题**。

**写法纪律**：

1. **先声明 shell**：每段命令块标注 `PowerShell` / `Git Bash` / `cmd`，不指望读者自行切换。
2. **少语法、多重复**：能展开成显式多行就别用循环、管道、变量替换——一次跑通的成本低于多写十行。
3. **循环体里多条命令必须用 `;` 分隔**（或换行），否则会被拼成一条命令。
4. **先只读、后写入**，分两步给：第一步输出用于确认前提（如 `git branch -v`、`git ls-files --stage`），前提不成立就停。
5. **给出预期输出**：一句话说明“正常应该看到什么”，让用户能自行判断成败（如“首列应为 `160000`”）。
6. **破坏性动作给安全档位**：用 `-d` 而非 `-D`、`--cached` 而非直接删——让工具在前提不成立时**拒绝执行**。
7. **实际交接的命令块不要留尖括号占位符**：在 bash 里 `<` 是输入重定向，粘贴后不会报错，而是把后面的内容吃掉、终端停在续行等输入，看起来像“卡住”。给字面量（把真实 hash 直接写出来），或写成 `这里替换成第一步输出的 hash`（不带尖括号）。命令块必须标注实际要用的 shell。

## 8. `git checkout <ref> -- <path>` 的覆盖语义（取值合并前先看工作区）

合并切片时常用 `git checkout <main> -- <path>` 把某路径整体换成主干版本（跳过分支的改动）。它的语义是“**用 `<ref>` 的版本覆盖索引与工作区**”——**该路径下的未提交改动会被静默丢弃**，不警告、不 stash、不进 reflog。

**纪律**：

1. 执行前先 `git status --short`；**有未提交改动就先提交**（或先 `git stash`）。
2. 取值范围能缩就缩：`-- <dir>` 覆盖整个目录，能写具体文件就不写目录。
3. 已被抹掉时：先查 `git stash list` 与会话留档；`git fsck --lost-found` 只在极端情况下有用（dangling blob 不保证存在）。

## 9. Agent 的 git 边界（谁执行、谁能读）

**写操作一律由人类执行**——`add` / `commit` / `push` / `tag` / `merge` / `reset` / `checkout` / `stash` / `mv` / `rm` … 都在内。Agent 的职责是把指令写成文档或消息交给人类，并给出**预期输出**（写法与档位见 §7）。**默认不代执行**；用户明确授权具体 Git 写动作时，按任务契约写入后执行。不得从“优化框架”推定获准提交、重写历史或推送；任务结束授权即失效。

**只读查询 Agent 可直接执行**。范围：`status` / `log` / `diff` / `show` / `ls-files` / `submodule status` / `branch -v` / `tag -l` / `worktree list` / `rev-parse` 这类**不改变仓库状态**的查询。理由：这些查询是决策输入；只读命令没有副作用；“手滑”风险只存在于写操作。

**判据一句话**：**能改仓库状态的一律交出去；只读的可以自己跑。** 拿不准时按“交出去”处理——表面像读取、实则覆盖工作区的命令是典型反例（`git checkout <ref> -- <path>`，见 §8）。

**仍推荐的文件系统只读手段**（与 git 只读并行，不冲突）：目录遍历、逐行文件对比、读 `.git` 指针文件——不依赖 git 可执行文件与工作区状态；差异比较方法见 `rule-sync-mechanism.md`。

另见：本地临时装置与 `_local/` 的归属，见总纲 §二与手册“并行与接手”。

## 10. 相关：跨平台操作坑

Windows 目录联接的删除、子模块 detached HEAD 的“推不上去”、静态托管子路径的 404、沙箱用户与目录属主不一致等，各有“症状 → 判法 → 正解”，见 [`platform-pitfalls.md`](platform-pitfalls.md)。

## 11. 分支与 worktree（可选实践）

以下是常见默认口径，不是所有实例的硬规则；实例可按自己的分支模型调整，并在 `UPSTREAM.md` 记录偏离。

- **默认不建分支**：能在既有工作线（现有 worktree / 现有分支）上继续，就不额外开分支；是否开由用户定。
- **“一轮一分支”不是默认规则**：分支 / worktree + `--squash` 是当时的选择；临时 worktree 用完即删的用法不变，但开不开由用户定。
- **零碎修理**用 `--fixup`；确需冻结起点做 A/B 时才考虑独立 worktree。

## 12. 验证证据必须由**要提交的那棵树**取证

**现行落点**：新提交按 §0 不写 `Green:` 或测试数字；证据记入日志/交付件。本节历史教训保留，取证纪律不变。

**纪律**：

1. **谁记录验证结论，谁对证据负责**：声明通过之前，应由获授权的执行者在**待提交的那棵树 / 那个路径上**运行适用门禁；日志中注明命令、结果与取证版本。已有证据须明确对应的 commit/树，不把历史结果当作当前验证。
2. **取证不到就标未验证**：不把未经取证的结论写成通过；起草消息不自动授权运行测试或构建。
3. **半成品不要混入另一批的提交**：停线 / 中断时把未完成改动**挪开或明确标注**，别让它随下一批“顺手提交”。
4. **发现历史里已有错写的 Green**：按“历史不改”保留原 message，在任务 log / 执行日志里记一条勘正。

## 13. 主干 / 开发分支的命名、合并与历史重写

> 本节是通用纪律；具体分支名、worktree 路径由实例决定。给出的 `main` / `dev` 只是常见示例（可选实践）。

### 13.1 命名与含义

| 名 | 含义 |
|---|---|
| `main`（或 `master`） | **主干**；只放已收编的提交 |
| `dev`（或实例自定） | **开发分支**；AI / agent 的写通常在这条 |

**纪律**：AI / agent 只在开发检出里写；主干检出留给合并 / 构建 / 发布。查法（只读）：`git worktree list`（首列路径、二列 HEAD、三列分支）。

**远程分支**：默认只推主干；`dev` 是否推送由实例决定。发布 = `dev` → 快进 `main` → push `main`。规则要写明“哪些分支上远程”，避免 agent 用常见 GitHub flow 补空。

**repo 级操作落点**：remote / push / fetch / tag 这类**仓库级操作对主 worktree 做**；linked worktree 只做分支内容开发。判据：`.git` 是目录的是主 worktree，是文件的是 linked worktree。

### 13.2 合并策略

- **默认 `--ff-only`**：开发线每轮一条内聚提交 ⇒ 快进即可，主干历史干净。
- **出现大量 WIP 时才 `--squash`**：把一条开发线压成一条主干提交。
- **`worktree` 的价值不是“压缩提交”**——是**不切分支就能并行两条线**。想压缩合并信息是合并策略的事，与要不要 worktree 无关。

### 13.3 历史重写的安全顺序（`filter-branch` / `filter-repo` 类）

**顺序不能颠倒**——多个 worktree 共用一份 `.git` 时，并行的检出会在重写后错位：

1. **先备份**：给要改的分支留一个备份引用（`git branch backup/<name>` 或记下原 hash）。
2. **只重写主干**：在主干检出上重写 `main`（**不要**同时改开发检出的工作区）。
3. **另一档跟进**：到另一个 worktree 里用 `reset --hard <新 main>` 或（要保内容时）`merge`，把它的分支接到重写后的历史上。
4. **核一遍**：`git worktree list` + 两边 `git log --oneline -3` + `git status --short`（工作区应干净）。

**优先确定性 plumbing**：重写类风险操作优先用 `commit-tree <已知树>` 这类确定性 plumbing 生成提交，**不用会动工作树的 porcelain**。每步**先只读核对**（树顶层 / 文件数 / `git status`）再进下一步。

**工具限制不许反过来改目录设计**：当规则 / 工具要求“多一个目录、多一次复制”时，先找替代工具或替代做法。

### 13.4 历史重写的**对齐判据**：看 HEAD + 提交消息，**不要看 tree**

**教训**：用 `git rev-parse a^{tree}` 与 `b^{tree}` 比“两条线是否对齐”——**只改提交消息**的重写**不会让 tree 哈希变**（两边的 tree 本来就相同）⇒ 该判据**假阳性**。

**正确判据**：**`HEAD` 哈希 + 提交消息**（`git log --oneline -1 <branch>` 逐条比对），必要时加 `git rev-parse <branch>`。**tree 哈希只在“改了内容”时才是判据**——用它判“消息改没改”永远相等。

### 13.5 Windows 下 `git worktree move` 的占用排查与兜底

**症状**：`git worktree move` 报 `Permission denied`——目录 / 文件被**终端、编辑器、`node` 进程**占着。

**三段式**（人工单照此写）：

1. **占用排查**：列 `node` 等进程；把当前终端 `Set-Location` 到别处（别停在待移动目录里）。
2. **兜底**：`Rename-Item` 直接改名 + `git worktree repair`。
3. **放弃路径**：**写明“这步不做也能往下走”**（改目录名只是美化，不影响任何引用）。
