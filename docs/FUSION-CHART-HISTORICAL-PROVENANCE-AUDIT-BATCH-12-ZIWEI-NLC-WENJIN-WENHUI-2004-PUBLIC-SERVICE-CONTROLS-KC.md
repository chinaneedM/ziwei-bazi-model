# Fusion Chart Historical Provenance Audit R1 — Batch 12KC

## 国家图书馆文津 2004《文汇报》13-DVD 公开服务控件与登录边界

Status: **PUBLIC SERVICE CONTROLS OBSERVED / NLC01-002860236 OPAC CROSS-ANCHOR SOURCE-EMITTED / SSO WRAPPER NOT BYPASSED / ONLINE READING LOGIN-STATE DEPENDENT / DOCUMENT DELIVERY POST NOT SUBMITTED / NO PUBLIC DATE-PAGE OBJECT / ZERO PRODUCT IMPACT**

### 1. 目标

12KB 已把国家图书馆当前 item-level 对象闭合为 2004《文汇报》、1938–1999 图文数据光盘、ISBN 7-89999-583-3、13 DVD-ROM。12KC 只检查该详情页**自己公开发出的服务控件**，判断是否存在无需账号动作即可继续到 1951-08-18 日期/页级对象的路径。

### 2. 匿名详情页的服务面

当前匿名 GET 返回 HTTP 200 / 28,830 bytes / SHA-256 `8bd9bf6d8ec50ae70f0a19cd96a322de5558659e9cbd6ef16aba4e8414ffe1fb`。

页面直接显示：

- 在线阅读；
- 文献传递；
- 馆藏信息；
- 国家图书馆位置；
- 未登录情况下不能使用在线阅读的提示。

与 12KB 同一详情 URL 的响应仍为 28,830 bytes，但 digest 从 `a76daf5e…` 变成 `8bd9bf6…`。本批只把它记为动态应用响应漂移，不据此重开 12KB 已闭合的书目身份。

### 3. OPAC 交叉锚点

详情页直接 source-emit 一个 SSO 包装链接，内层参数明确包含：

```text
func=item-global
doc_library=NLC01
doc_number=002860236
```

这把 2004 光盘对象进一步绑定到 NLC OPAC catalog locator `NLC01 / 002860236`。

但该链接由页面**主动包在 SSO 登录路由里**。12KC 不绕过包装、不直接访问内层 OPAC URL，也不把 catalog number 当作 1951 原页。

### 4. 在线阅读合同

source-emitted `rdDetails.js`（SHA-256 `94a94b41d94e11b3f5d68ff23f5f62b6c46d9cefce87e5784e816fff0e04bbfe`）的 `initDocGetLink()` 明确引用：

`uri / isUserLogin / isInnerIP / isTsingHuaTongFang / directLink / isVpnLink / vpnUrlPrefix / isSamlLink`。

逻辑上：

- `uri` 为空时移除电子资源控件；
- 已登录时才根据内网、直连、VPN 等状态把 `readingurl` 绑定到 `directLink` 或 `uri`；
- 未登录时，点击在线阅读进入登录提示/SSO 流程。

KC 尚未读取这些变量在本条目上的具体匿名值，因此不会预判是否存在可公开观察但登录后才可使用的底层 URI。

### 5. 文献传递是外部动作边界

页面隐藏表单直接 source-emit：

```text
POST http://wxtgzx.nlc.cn:8111/gateway/UserRequestAdd.jsf
```

`fileTransfer()` 还会先记录 docDelivery 日志，再提交 `Form1`。本批没有 POST、没有提交文献传递、没有登录、没有注册、没有 VPN，也没有打开 SSO。

### 6. 控制证据

- workflow: `.github/workflows/probe-batch-12kc-nlc-wenjin-2004-wenhui-public-service-controls.yml`
- exact head: `87b3dd0d4d3fdb2b30425ae4ec1cda0a622f9e2a`
- run / job / artifact: `36854024255 / 110342117815 / 11157530228`
- artifact digest: `sha256:89d4b2f4dd009beada084715875d7f515198d17f8cd43d2858983e2e598c9961`

### 7. 项目影响与下一门

Matrix 继续保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / candidate collapse 均为 0。Transmission Graph 不新增边。

下一门 12KD 只解析匿名详情页已经发出的 `uri/directLink/VPN/login` 变量，不点击在线阅读、不跟随 SSO/VPN、不 POST 文献传递。如果没有具体匿名资源 URI，则该路线正式进入账号/服务授权门槛，并继续并行寻找上海《文汇报》1951-08-18 原页、《文物参考资料》1951年第9期 pp.221–233 与 2011《赵万里文集》第1卷 p.197。

Research record: `docs/research/ZIWEI-NLC-WENJIN-WENHUI-2004-PUBLIC-SERVICE-CONTROLS-R1.json`.
