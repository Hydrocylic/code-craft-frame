# 无头复现工具链（渲染疑难 bug 的 JS 侧诊断方法论）

<!--
  来源: webgl-path-tracer r09 BUG-003（起源）→ r15 BUG-006（成熟化）→ r16 BUG-012（扩 GPU 级真机复现）
  状态: spec-add（2026-09-06 提升为共有规则；多次验证）；spec-update 2026-09-09 增补 GPU 级章节
  适用: GPU/渲染类疑难 bug——画面异常（全黑/花屏/错误渲染）与 GPU 崩溃类（TDR/context loss）的排查顺序
-->

## 核心原则

**GPU 侧黑屏/错渲染时，先用 Node 无头复现把 JS 侧数据链路证到"无可怀疑"，再碰 GPU 侧。** 顺序反了会浪费大量轮次——GPU 侧无法单步调试，JS 侧全可单步。

## 三步递进

### 第一步：数据来源诊断（原始资产解析）

- glTF/模型文件直解析（不经过加载器）：解 JSON + bin 的 accessor，算 AABB、查 NaN、查节点变换（glTF 根节点常有 scale！）
- 回答：模型在哪、多大、坐标是否有限、变换是否需要应用

### 第二步：加载器/物化链路复现（真实代码 + DOM 桩）

让**真实加载器代码**在 Node 里跑通，关键桩：

```js
globalThis.self = globalThis;                 // GLTFLoader 引用 self.URL
globalThis.ProgressEvent = class { constructor(t, i) { this.type = t; Object.assign(this, i); } };
globalThis.Image = class { set src(v) { this._src = v; this.width = 64; this.height = 64; queueMicrotask(() => this.onload?.()); } get src() { return this._src; } };
globalThis.document = { createElement: () => ({ getContext: () => ({ drawImage() {}, getImageData() { return { data: new Uint8ClampedArray(4096).fill(128) }; } }) }) };
// file:// fetch 桩（three 的 FileLoader 传 Request 对象；Windows 盘符处理）
const origFetch = globalThis.fetch.bind(globalThis);
globalThis.fetch = async (input, init) => {
  const urlStr = input instanceof Request ? input.url : String(input);
  const u = new URL(urlStr, 'file:///');
  if (u.protocol === 'file:') return new Response(fs.readFileSync(u.pathname.replace(/^\/([A-Za-z]:)/, '$1')));
  return origFetch(input, init);
};
```

- 物化核心函数拆成 `extract*(gltf)` 导出（load 外壳 + 物化核心分离）——诊断脚本只测核心
- 回答：真实物化输出是否正确（数量/AABB/NaN/albedo）

### 第三步：打包数据遍历模拟（GPU 拿到什么就测什么）

- 构建函数导出（`buildBVH` 之类）；`buildBVHTextures(...).texture.image.data` 就是**上传给 GPU 的精确 Float32Array**
- 用打包数组 + texelFetch 同款索引数学（`index % w` / `index / w`）做 shader 同款遍历模拟
- 回答：GPU 收到的数据逐字节正确、遍历在 JS 侧能命中——**如果三步全过还黑屏，嫌疑收敛到 GPU 侧：上传/驱动/着色器/管线**（此时做二分实验与 GPU 读回探针）

### 附：场景遮挡问题 → 可见性扫描

- 地面网格点向候选光源方向发 shadow ray，用字符图（O=见天/X=被挡）画出开口/遮挡区域——把"面光该放哪"变成二维可视化问题

## Debug 检查点提交

黑屏级疑难 bug 攻坚前，先把当前状态 commit 为 WIP 检查点（含诊断脚本）：
- 攻坚失败可随时回退；诊断脚本随 commit 保留，换对话/换 agent 时是现成资产
- 提交信息风格：`R<NN> WIP: <已确认的修复>; <未解症状> (debug checkpoint)`

## 与 r09 版本的关系

r09 记录了初版（_check-bvh.mjs 一次性脚本）；r15 成熟化：DOM 桩体系、file:// fetch 桩、打包数据模拟、天空扫描、checkpoint 提交——本 spec 是合并版。

---

## GPU 级疑难：TDR / context loss 的真机复现（r16 BUG-012 增补）

**适用前置**：JS 侧三步全绿（数据链路无可怀疑）、症状是 context lost / 驱动重置 / 帧率随机崩塌类——无头复现（SwiftShader）测不到驱动行为，必须**真机 + 真实 GPU**。

### 金标准：操作系统事件日志，不信页面事件

- Windows：事件查看器 System 日志 **Id=4101**（"显示驱动程序 nvlddmkm 已停止响应并已恢复"）——`powershell Get-WinEvent -FilterHashtable @{LogName='System'; Id=4101}` 只读查询，与实验时间窗对照即实锤
- 页面 `webglcontextlost` **只作参考**：TDR 后 webview/iframe 场景可能收不到事件或恢复较快；"没收到 lost"≠"没发生 TDR"

### 真机复现的仪器化（Agent 控制浏览器标签页时）

1. **帧推进监测**：轮询暴露的帧计数 uniform（如 `__pt.uniforms.uFrame.value`），每 5-10s 采样——区分"健康满帧率 / 逐渐变慢 / 冻结 / 重载（计数归零）"
2. **rAF 心跳**：注入独立 rAF 计数器记录 >300ms 间隙——**无间隙 + 帧计数冻结 = JS 不阻塞、GPU 队列饱和**（单帧 GPU 时间爆炸）；有间隙 = 页面隐藏/JS 阻塞
3. **contextlost 钩子 + 页面装载标记**（`window.__mark = Date.now()`）——标记消失 = 整页重载（钩子被洗掉，勿误判为"未发生"）

### 三条实测教训（污染源）

- **实验期间禁止改源文件**：dev server HMR 全页重载会重置帧计数、洗掉注入钩子，实验作废——先改完再开跑
- **多标签页互扰**：只留一个受测标签页，其余关闭（后台标签 rAF 冻结会制造假象）
- **TDR 与"平均负载"无关**：看门狗看的是**单次 GPU 指令耗时**——持续降载（降分辨率/锁帧/分块）只能推迟发病，随机巨帧（实测 66ms→2.3s）才是根因载体；帧计数从健康帧率瞬间冻结 = 巨帧特征

### 排除法武器：URL 参数单项回退开关

诊断期在代码里预留 `?flag=` 开关（如 `?tex=0` 关贴图采样、`?noatlas=1` 跳过图集上传、`?tris=N` 截断几何），真机 A/B 各跑一轮 + 事件日志对照——每轮排除一个变量，比猜测驱动行为可靠得多。开关保留在代码里作为复发时的二分工具。

### r16 BUG-012 的排除记录（方法应用示例）

复现 5 次真实 nvlddmkm TDR 后排除：贴图采样（门控后仍丢）、图集（noatlas 仍丢）、三角形数（截断 5 万反而更早丢）、显存/温度（全程正常）——嫌疑收敛到驱动层/遍历路径，详见项目 r16-sponza/sponza-log.md 第六轮。
