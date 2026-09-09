# 会话实践规则 — 本地实例化

> 区域: 本地 explore（研讨区）
> 最后更新: 2026-08-31
> 来源: kotocord Phase 4（管线闭环验证）+ Phase 5（ASR 上下文偏置）会话实践沉淀

## 定位

AI 协作会话中反复出现的**工作方式约定**，经 kotocord 会话验证后沉淀于此。与 task-consolidation.md（任务收拢机制）互补：本文件记录**单次会话内**的工作规则，成熟后按 explore→spec 流程推上游。

## 规则条目

### 1. E0 资源预检（验证类任务动手前必做）

验证/联调类任务的第一步不是运行，而是 AI 以「**代码期望 vs 物理实际**」核对资源：读代码确认约定路径 → 查文件系统确认物理实际 → 错配即给修复命令（用户执行）。

**案例**: Phase 4 E0 发现模型在 `resources/res/` 而代码/脚本三方期望 `resources/model/`——gitignored 二进制不随代码约定迁移，错配潜伏两个多月（3 月放置 vs 8 月重构断档）。教训: **gitignored 资源与代码约定之间没有 git 保底，必须显式核对**。

### 2. 环境诊断三层

| 症状 | 判定 | 处置 |
|------|------|------|
| `0xc0000135`（含最小测试全挂） | DLL 缺失 | 先 `$env:PATH = "D:\Qt\...\bin;" + $env:PATH` |
| 终端中文乱码 | 编码不匹配（不影响功能） | 字节级判定（重定向文件）→ PS 5.1 用 `chcp 65001` + `[Console]::OutputEncoding`；VS Code 集成终端无效时换 VS 开发者控制台（cmd/conhost） |
| 外部服务连接失败 | 先看 OS 错误码 | `getaddrinfo failed` = DNS 解析失败（非 TLS/协议）；用 **sidecar 独立复现**绕过 app：先单独跑服务调用脚本，再隔离「系统解析 vs 进程解析」 |

### 3. 阶段性中止收束

任务中途叫停的收束四件套:

1. plan 状态 → 🔒 + 动态调整记录中止条目
2. log → 封存条目（**线头清单**: 未竟事项 + 去向——转交下个 agent / issues / 延后）
3. 知识 → knowledge-base QA 追加（当次会话的知识盲区）
4. 交接 → 双仓库 commit 文案 + 下个 agent 的冷启动入口说明

**案例**: Phase 5 中止——S2 实验问题较多，用户另启重构 agent；S2/S4/S5/品读全部线头化，含「main.cpp 引擎已切 whisper 未回切」这类**现场状态**也进线头。

### 4. 单测性设计（重型构造提取轻量小类）

构造函数需加载重型资源（如 466MB 模型）的类，其可测逻辑应**提取为独立小类**——否则单测进程要么加载模型、要么动私有成员。

**案例**: WhisperTranscriber 的 initial_prompt 窗口逻辑提取为 PromptContext（7 用例免模型单测）。计划草图中的私有方法在实施时改提取小类——**计划是设计意图，测试可达性是实施约束**。

### 5. 纠偏/阈值原则：欠纠优于误纠

模糊匹配类算法（编辑距离纠偏等）:

- 纠错失败用户可接受；**把正确内容改错是硬伤**
- ±窗口加结构约束（首字符对齐）防「前导删除」吞字
- 阈值宁紧勿松（2 字词 ≤1 距离；「删首字+插尾字」形态直接收紧掉）
- 回归用例锁行为（「精确词带上下文不被吞」）

### 6. 假设数据模式

用户暂无真实数据时，AI 先提供**假设数据**（标注「假设」）让流程跑通，用户后补真实数据。案例: 热词表 AI 假设 23 词，真实词表转交用户。

### 7. git 协作边界

AI 不执行 git 命令（写操作），可提供: commit 文案、诊断用只读命令。文案**不含 AI 协作者署名**（CLAUDE.md 规则）。中止/里程碑时主动提供双仓库 commit 文案供用户执行。

**2026-09-08 补强（边界澄清）**: "写操作"包括但不限于 `commit / push / tag / add / mv / rm / reset / checkout / stash`——即**一切改动暂存区或仓库状态的命令**，文件整理类也不例外（`git mv` 也是 git 写）。AI 做文件移动/重命名时用普通文件操作（或给出 `git mv` 指令文本），暂存与提交一律交用户。AI 可用的只有只读命令: `status / log / diff / show / ls-files` 等。

**违规案例**: 2026-09-08 kotocord M0 归档整理，AI 直接执行了 `git mv`（两批共 14 个文件）——虽结果正确，但绕过了用户对暂存区的控制权；用户澄清后确认规则收紧为上述边界。

### 8. 第三方库集成 spike 先行

引入新第三方库（尤其无 release tag 的）**先 spike 后集成**，顺序:

1. 独立克隆上游，读四样东西: CMakeLists（target 名/选项/子项目行为）、LICENSE、依赖清单（如 Qt 模块——本机是否已装）、API 头文件
2. 无 release tag 则 pin commit（记入 log，版本迁移作为已知风险）
3. 在项目里做**最小编译验证**（FetchContent + 链接 + 一个空种子类 include 头文件编过）再动手写功能
4. spike 结论（版本/许可/依赖/坑）落 log，集成参数进 decisions

**案例**: QtNodes spike（2026-09-08）确认 pin `7bbcd3e`、BSD-3、需 Qt OpenGL（本机已装）——避免了集成中途发现缺模块的返工；同期发现"手动链 Qt6::OpenGL 报 LNK1104（目标未经本项目 find_package 声明），经库的 PUBLIC 传递链接即可"。

### 9. 路径敏感写后即验

文件写入/移动/重命名涉及**易错路径**（多级嵌套、相似目录名）时，操作后立即 `ls` 核对落点，不等到测试或运行时暴露。

**案例**: 2026-09-09 kotocord M4b，连续两个模板 JSON 写歪目录（`products/pipelines/`、`resources/pipelines/`，均非目标 `products/kotocord/resources/pipelines/`），Write 工具报成功无异常，最后靠"模板数 <4"的测试断言才发现并回溯定位。路径写对与否，工具反馈不可信，只有 ls 可信。

### 10. Qt/C++ 编译期陷阱速查（kotocord M4 会话实测）

| 症状 | 根因 | 处置 |
|---|---|---|
| `C2027/C2338 can't delete incomplete type` | 头文件里 unique_ptr 成员只有前置声明，隐式内联析构需要完整类型 | 析构声明进头文件、`= default` 定义进 cpp |
| 第三方头里 `std::numeric_limits<T>::max()` 编译炸（C2589） | `windows.h` 的 min/max 宏污染 | include windows.h 前定义 `NOMINMAX`（+ `WIN32_LEAN_AND_MEAN`） |
| `C3668 override did not override` | 虚函数签名按值 vs 按 const 引用不一致（基类 `PortIndex const`，派生写成 `const&`） | 逐字对齐基类签名 |
| `C2397 narrowing conversion` | 花括号初始化里 unsigned→int | 显式 `static_cast<int>` |
| QCOMPARE 断言解析错乱（C1075） | 宏参数内多行花括号初始化 | 先构造局部变量再传宏 |
| 运行时段错误（测试进程崩） | 注册表/工厂闭包持有临时对象的指针（目录对象按值传参后悬垂） | 元数据**按值拷贝进闭包**，生命周期与注册表一致 |

## 实践记录

- **2026-08-31** — kotocord Phase 4 + Phase 5 会话验证全部七条。首次应用: E0 预检（模型位置）、sidecar 复现（瞬时 DNS）、中止收束（Phase 5）、单测性设计（PromptContext）、纠偏原则（DomainDictionary 首轮缺陷修复）、假设词表、双仓库 commit 文案交接。
- **2026-09-08** — 规则 7 边界澄清: git 写操作全量交用户（含 `git mv`），起因见违规案例；同会话沉淀 git-branch-threads.md（分支线头规则）。
- **2026-09-09** — kotocord 节点编辑器重构全程（M0-M5）: 新增规则 8（QtNodes spike）、9（模板写歪目录）、10（六类编译/链接陷阱实测沉淀）；架构侧经验另立 graph-config-architecture.md。
