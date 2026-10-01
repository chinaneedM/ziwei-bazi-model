# Fusion Chart Historical Provenance Audit R1 — Batch 12KD

## 国家图书馆文津 2004《文汇报》13-DVD 匿名阅读变量闭合

Status: **URI EMPTY / DIRECTLINK EMPTY / ANONYMOUS USER FALSE / VPN FLAG FALSE / GENERIC VPN PREFIX ONLY / NO READINGURL / LOGIN REQUIRED / ANONYMOUS CONTENT ROUTE CLOSED / ZERO PRODUCT IMPACT**

### 1. 目标

12KC 已证明 2004《文汇报》13-DVD 详情页存在在线阅读、文献传递和 SSO 包装控件，但尚未读取本条目在匿名状态下实际发出的 `uri/directLink/VPN/login` 值。12KD 只读取这些公开变量，不跟随任何资源地址。

### 2. 匿名变量

页面直接发出：

```text
uri = ''
directLink = ''
isUserLogin = false
isInnerIP = 'false'
isVpnLink = 'false'
isTsingHuaTongFang = 'false'
isSamlLink = 'false'
vpnUrlPrefix = 'https://vpn2.nlc.cn/prx/000/http/'
loginTip = '立即登录'
needlogin = '未登录情况下不能使用在线阅读功能，请您先登录!'
```

同时：

- `getEleAll` 只绑定 `javascript:void(0)`；
- `loginLink.hrefSrc` 为空；
- 页面没有发出 `readingurl` 属性；
- `otherLink` 初始隐藏。

### 3. 裁决

这里必须区分“内容 URI”与“通用 VPN 前缀”。

探针的通用字符串筛选会把 `vpnUrlPrefix` 算作一个非空 URI-like 值，但它只是 NLC 的通用 VPN 前缀，**不是本条目内容地址**。真正与本条目内容相关的两个变量：

```text
uri = ''
directLink = ''
```

均为空。

因此当前匿名层可正式裁决：

```text
ANONYMOUS_ITEM_CONTENT_URI = NOT_EMITTED
ANONYMOUS_DIRECTLINK = NOT_EMITTED
ANONYMOUS_READINGURL = NOT_EMITTED
ACCOUNT_OR_SSO_BOUNDARY = REACHED
```

这不代表馆内、登录后或文献传递一定无法取得内容；只表示匿名公开页没有发出可直接继续的内容 URL。

### 4. 动态响应漂移

同一详情 URL 三次响应：

- 12KB：28,830 bytes / `a76daf5e…`
- 12KC：28,830 bytes / `8bd9bf6…`
- 12KD：28,831 bytes / `97076907…`

这说明应用页存在动态包装漂移。由于 12KB 已独立记录 item-level 书目字段，且 KC/KD 的目的仅是服务控件和变量，本批不把 wrapper digest 变化升级成书目身份冲突。

### 5. 控制证据

- workflow: `.github/workflows/probe-batch-12kd-nlc-wenjin-2004-wenhui-reading-vars.yml`
- exact head: `c36cfc48e17c8b12c5260f7cd53a11da50924a2a`
- run / job / artifact: `36854903830 / 110344966161 / 11157936477`
- artifact digest: `sha256:7398e16bf987ff5a379f383e500c9460ad442dba43b7c78550db7b957ac6e2f0`

只执行匿名 GET；没有登录、SSO、VPN、POST、文献传递、账号注册或私有端点猜测。

### 6. 项目影响与下一门

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / candidate collapse 均为 0。Transmission Graph 不变。

NLC 2004 13-DVD 的**匿名在线阅读路线到此关闭**。下一步恢复最直接的文本目标：用已经在 12JX 校准的一方文津 GET 合同，直接检索赵万里《永乐大典展览的意义》及繁简/作者组合，争取取得 1951 文章或期刊 item-level 对象。若命中，再沿 source-emitted record/detail 控件继续；不再围绕空 `uri/directLink` 重试。

Research record: `docs/research/ZIWEI-NLC-WENJIN-WENHUI-2004-ANONYMOUS-READING-VARIABLES-R1.json`.
