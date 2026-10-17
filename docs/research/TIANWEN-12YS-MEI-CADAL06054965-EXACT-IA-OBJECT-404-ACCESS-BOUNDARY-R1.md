# 天问12YS｜梅文鼎《大統歷志》卷三至四：精确 IA 影像标识与实测 HTTP404 接入边界

## 文件级定位是突破，但不是完成原页核字

维基文库开放古籍索引 [清代 Internet Archive Scans](https://zh.wikisource.org/zh-hans/Wikisource:古籍資源/Internet_Archive_Scans/清) 明确列「（清）梅文鼎《大統歷志》」「浙江大学图书馆」及四个分册 `卷1~卷2 / 卷3~卷4 / 卷5~卷6 / 卷7~卷8`。本批在 [精确索引解析 Action](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39006970439) 从约164万字节的实际页面、12988条 HTML link 中找出**卷三至四唯一同列文件链接**：

`//archive.org/download/06054965.cn//06054965.cn.djvu`。

识别结果为 archive item `06054965.cn`。已解决12YO“仅知道CText分册”到“公开索引含精确文件ID”的定位缺口；但**没有梅氏古书页的原图字节**。

## 下载验证与访问边界

[原图采集 Action](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39007082727) 在不登陆、不猜测私有标识、不绕过访问限制的环境，分别直接访问：

- 双斜线源链接 `/download/06054965.cn//06054965.cn.djvu` → HTTP 404。
- 标准路径 `/download/06054965.cn/06054965.cn.djvu` → HTTP 404。

原始失败响应写入制品 `12090914681/access.json`，源文件大小及SHA、页数、图像位点均**尚不存在**。HTTP404只足以说明**当时这两条具体公开链接失败**，不是古籍不存在、同编号扫描丢失，或整个平台全面关闭的证明。

[CText相关影像著录](https://ctext.org/library.pl?if=gb&res=5775)、12YO 原 OCR 分册、Wikisource 数字收本均不提供当前已验证原图。另一公开下载目录 [集古作网四册PDF 17.38MB](https://www.jiguzuo.com/guji/17646034895005.html) 引向支付2元的入口；本批**未支付、未规避付费**，且不能据此确认 PDF 具体对应哪个历史实体副本。

## 史料地位及下一步

梅氏卷三和卷四原印数位尚未获得一张可复核原页，因此不将前轮 **0.0186 / 4.9386** 电子收本升格为原印。本批新增**文件级访问对象定位**，原印投票、物理副本版次、谱系关联均为零。CADAL06056955《明史》与国图1892本《明史》的两个数字印本对校仍有效，**不能替代梅氏原本**。TW-OPEN-0005 保持 OPEN；原表 G893 六控5/6、跨本0/6；历史审计222/222；排盘 R1 CLOSED。

下一步优先反查 IA 官方 Metadata / Wikimedia Commons 的公开馆目与同编号镜像，以及允许公开访问的文献影像提供者；取得书影 SHA、相应卷三卷四页、无 OCR 直接核字以后才讨论三差与 G893 原列对应。

详见 `docs/research/TIANWEN-12YS-MEI-CADAL06054965-EXACT-IA-OBJECT-404-ACCESS-BOUNDARY-R1.json`。
