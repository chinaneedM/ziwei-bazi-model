# Fusion Chart Historical Provenance Audit R1 — Batch 12LG

## 全国报刊索引：412 与同域公开活动页合同校准

Status: **ROOT 412 / SAME-DOMAIN ACTIVITY 200 / PATH-SCOPED ESA BROWSER PRECONDITION / SITE-WIDE INSTITUTIONAL-IP WALL NOT DEMONSTRATED / NO QUERY / NO LOGIN / ZERO PRODUCT IMPACT**

Batch 12LF 只证明匿名 GitHub runner 读取 `https://www.cnbksy.com/` 与 `/home` 时得到 HTTP 412，不能把 412 自动等同于机构 IP 授权墙。12LG 因而只比较同一域名下根页与一个可公开读取的第一方活动详情页，不提交任何赵万里 / 文汇报目标查询。

控制 run `36878743129` / job `110424801197` 在 exact head `648c6dfe004c36fae9fdcb79081bb36b076d0215` 上成功。根页返回 HTTP 412 / `text/html; charset=utf-8`，server header 为 `ESA`，设置 cookie，正文是带不透明脚本状态的 JavaScript 前置条件页面；扫描未见“登录”“授权”“验证码”“Access Denied”等明确授权语义。同域活动页 `/portal/pushManager/pushItem?id=322&isActivity=true&source=index` 返回 HTTP 200 / `text/html;charset=UTF-8`，同样观察到 `server: ESA`。

活动页直接 source-emits：

- `/home`
- `/signUp`
- `/login`
- `mailto:journal@libnet.sh.cn`
- 六个 script src（ESA 动态脚本、jQuery、Bootstrap、PDF.js 与 `/public/common/js/common.js?version=V20241206` 等）。

因此当前可裁决为：

```text
CNBKSY_ROOT_412 = CONFIRMED
SAME_DOMAIN_PUBLIC_ACTIVITY_200 = CONFIRMED
SITE_WIDE_INSTITUTIONAL_IP_AUTHORIZATION_WALL = NOT_DEMONSTRATED
CONTROLLING_ACCESS_CLASSIFICATION = PATH_SCOPED_ESA_BROWSER_PRECONDITION_BOUNDARY
SEARCH_CONTRACT = NOT_YET_CLOSED
```

“同一 ESA server header”只说明两个响应观察到同一 header 值，不证明更深层基础设施身份。12LG 也不推断活动页能绕过根页，不执行登录/注册，不跟随任何尚未闭合的检索路由。

下一门 12LH 只读取上述六个 source-emitted script URL，抽取检索相关函数名、路由字面量、navigation/AJAX builder；**发现路由也不执行**，且仍不提交赵万里 / 文汇报目标查询。

控制证据：workflow `.github/workflows/probe-batch-12lg-cnbksy-412-and-public-activity-contract.yml`; run/job/artifact `36878743129 / 110424801197 / 11168979871`; artifact digest `sha256:c3930c6b4c519202bfbe4e3b929cb953cde3051190366b0aa7af538f227eb596`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-412-AND-PUBLIC-ACTIVITY-CONTRACT-R1.json`.
