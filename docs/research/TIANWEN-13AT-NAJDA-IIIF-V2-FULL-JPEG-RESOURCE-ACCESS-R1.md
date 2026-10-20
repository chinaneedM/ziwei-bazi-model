# 天问13AT｜日本国立公文书馆《高麗史》第52物理册 IIIF 资源实证

13AS Actions [运行](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39375082543) 实际取得馆方 [IIIF Manifest](https://www.digital.archives.go.jp/api/iiif/4898854/manifest.json)，HTTP200，29791字节，SHA256 `a7ef9f1d7953eca9c44168dee0f482f2a408ca1a18a093410b0b5c1da221f7d2`，IIIF Presentation2，32个 Canvas，题名「高麗史５２」、请求号 `282-0006-0052`。清单每个画布包含真正可调用的 `images[0].resource["@id"]`，源给出 `/api/content/item/.../full/max/0/native.jpg` 形式的全尺寸图像URL。

上一版直接GET源浏览器JS内 `/content/...jp2`，3项HTTP400；这是服务资源标识不等于直接图像的访问格式问题，不是缺页证明。现以清单**原样输出**的URL作为下载目标，3页封顶、每页12MB、保存原字节/哈希/魔数，不合成或枚举ID。返回的JPEG是从JP2生成的图像表示，不能自动称为JP2底层源文件。

目前仍不知第52册是否含正文卷五十二，也尚未亲读日16太阳表。零算法重开，来源754，11条遗漏全部保留开放。