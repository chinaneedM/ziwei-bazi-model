# 天问 13LQ｜德国馆《明史》第二册 IIIF 清单及 20 张原馆预览真实获取

## 第一方来源实际采集

13LP 提交后在 [对应精确 HEAD Actions](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/41054248271) 成功执行 13LP 脚本、6项独立测试、遗漏台账父提交校验及项目连续性门禁。原馆 IIIF manifest 返回 `sc:Manifest`，1,762,391 字节，SHA256 `fb28be88c767636c6394926620c112e994f1b0b5d58cf896d4a5edc2919f047c`，含 **1880** 个 canvas。13LP 研究初始记录中的网页 **1886** 为另一个展示层数字，二者相差6；没有查明展示分组/索引口径，不能据此推断有6张古籍遗失。

严格按照 manifest 内 image service 采集20张 `/full/320,/0/default.jpg` 衍生预览，20/20返回成功、逐图 JPEG 与解码 RGB SHA 均记载在原始归档。画廊的首四张是封面或无正文页，之后抽样可目视确认古籍竖排文字；**未经高分辨率逐行核对**，不能认定此册包含《明史》卷三十五。预览为馆方 JPEG 衍生物，不是实物版木证据或完整原始扫描。

## 完整性与可复查性

GitHub Actions artifact `12975358673`（ZIP 280457 字节，SHA256 `c13af97a923dd36adbb2c242858bd50f32780cacc3982a301e3ba263148d949e`）已重新下载，与上传摘要独立复核一致，并**另行永久留存**资料库 `/命运/tianwen-13lp-bsb-mingshi1739-manifest-preview-evidence.zip`，Library ID `libfile_bd904974e1048191bcdc08a89e34db11`。其三份文件为 `manifest-probe.json`、`sampled-preview-index.json` 和 `preview-contact.jpg`；后者 1200×1300、287443 字节、SHA256 `5be41d5fb0cfdf0ab9f528e8672c647859d2349a5a61ab7b8f2c2d88f51d6810`。直接复核记录在配套 JSON。

## 判定与下一步

这次可以升级为 **馆方 manifest 与低清原馆衍生图实际获得**，不能升级为卷三十五原叶、238977.09/288977.09 新读数、1739 年实物印次、同版木或 G893 数值裁决。来源数量保持647+118=765，Matrix222/222，传承谱252节点/238边，11风险未结，排盘CLOSED、算法重开0。

先定位真实卷叶（允许转到该馆**已链接的**合适册次，不猜测对象ID），之后才能对目标原字执行馆方全分辨率采集和版本比对。
