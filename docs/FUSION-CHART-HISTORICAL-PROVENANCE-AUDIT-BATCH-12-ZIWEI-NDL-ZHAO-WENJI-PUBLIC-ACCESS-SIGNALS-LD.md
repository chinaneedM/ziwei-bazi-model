# Fusion Chart Historical Provenance Audit R1 — Batch 12LD

## NDL《趙萬里文集》第1卷：公开访问信号盘点

Status: **EXACT NDL OBJECT CLOSED / PUBLIC RECORD HTTP200 / NO DIGITAL-COLLECTION TOKEN / NO INTERNET-PUBLIC TOKEN / NO REMOTE-COPY TOKEN / GENERIC SITE HELP LINKS ONLY / NO LINK FOLLOW / NO COPY REQUEST / ZERO PRODUCT IMPACT**

12HG 已关闭 2011《趙萬里文集》第1卷的精确 NDL 实物对象：

```text
call number = UM11-C247
NDLBibID    = 023434359
ISBN        = 9787501346653
target      = p.197
```

12LD 匿名读取其 NDL Search 公共记录。对象身份再次直接出现，但页面源码中以下 item-access 关键词均为 0：

```text
国立国会図書館デジタルコレクション = 0
インターネット公開                 = 0
図書館・個人送信                   = 0
遠隔複写                           = 0
複写                               = 0
オンライン                         = 0
```

抓到的“网上阅读 / 获取复制件 / 图书馆阅读”链接属于站点全局帮助/页脚，不是该书专属数字对象；另有 CiNii 馆藏查询链接。12LD 不跟随任何链接，不登录，也不提交复制申请。

因此目前只能说：

```text
EXACT PHYSICAL HOLDING = CLOSED
ITEM-SPECIFIC PUBLIC DIGITAL ACCESS = NOT DEMONSTRATED
DIRECT P197 TEXT = NOT REVIEWED
```

控制证据：workflow `.github/workflows/probe-batch-12ld-ndl-zhao-wenji-public-access-signals.yml`; exact head `22bf28e727d2348d22f3b8b91716eff13c90f06e`; run/job/artifact `36876093767 / 110415795113 / 11168722610`; artifact digest `sha256:fdf365761480b87bd7fbec2e8200ab7d8f5c1de70d275fda1b2b1b8717e8cc85`。

下一门 12LE：把主内容与全局页脚隔离，只检查 item-level action/availability block 和 server-rendered embedded record data；如果仍无数字对象信号，就把 NDL p.197 收口为 physical-holding-only，并转向其他公开 primary-text 路线。

Matrix 继续 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

Research record: `docs/research/ZIWEI-NDL-ZHAO-WENJI-PUBLIC-ACCESS-SIGNALS-R1.json`.
