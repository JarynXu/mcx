# 业务服务器从 CMS 取配置：SIP 订阅和 HTTP 取文分别核谁？

**SIP 初订要分清两个 PSI：Request-URI 指向 CMS，PAI 标识业务服务器。**HTTP 取文要另核这次 HTTP 请求的发送方与权限。初订命中服务器分支，不能证明 HTTP 取档已获准。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§§4.3.1、6.2.3、6.2.4.1、6.3.3.2.3、6.3.13.2.3、6.3.13.3.2.4。这里是业务服务器订阅**每个已配置且服务器支持的任务关键组织**的业务配置，不是[终端配置管理客户端（CMC）代用户订阅](cmc-subscription-notify-fetch.md)。标准不规定怎样给服务器配置组织标识。

## 初订：收件地址和订阅者身份是两处

- **业务服务器发出。**初始 SIP SUBSCRIBE 的 Request-URI 是 SIP URI：基址用服务器所配置的 **CMS PSI**，`auid` 标识要订阅的业务配置文档所属应用。公共业务标识（PSI）在这里标识一个 SIP 服务。服务器把**自身的 PSI**放在 `P-Asserted-Identity`（PAI）中。原文列出 `P-Asserted-Service` 的 ICSI `urn:urn-7:3gpp-service.ims.icsi.mcptt`，以及 `Contact` 的 `g.3gpp.icsi-ref` 同值。（§6.3.13.2.3）
- **CMS 收到。**`Event: xcap-diff`、Request-URI 的基址等于 CMS PSI、PAI 带有授权 MCS 服务器清单中的身份、`P-Asserted-Service` 带所列 ICSI。四项满足时，CMS 按 RFC 5875 扮演通知方。清单所列的是 CMS 所属业务提供方的 MCS 服务器 PSI，不是终端用户的 MCPTT ID。（§§6.2.4.1、6.3.13.3.2.4 初订段）

白名单不能单独决定分支。§6.3.13.3.2.3 的初始请求也检查白名单，但 Request-URI 基址条件写的是 CMS 的 **XCAP 根 URI**。CMC 代理初始请求则查代理 PSI、PAI 不含清单身份及规定正文，并从令牌取得 MCPTT ID（§6.3.13.3.2.2）。不要把终端的令牌当成业务服务器这条路径的通行证。初订缺其中一项时，这一条未给出固定的失败响应。

## 续订：只知初订通过，还不能解释这次 403

§6.3.13.2.3 的续订发送段列出 CMS PSI 和 `auid`，以及 `Contact` 的上述 ICSI 标签。§6.3.13.3.2.4 的接收段处理 `Event: xcap-diff` 且带 `application/resource-lists+xml` 正文的 re-SUBSCRIBE。CMS 用**这次入站 PAI 的 URI**作认证身份，查列表中文档或元素的变更订阅权限。

例如列表只有一份文档，而该身份没有它的订阅权限，CMS 必须回 SIP 403 并停止该流程。这里只据接收段查这次请求，不把发送段未列的 PAI 或资源列表解释成不应出现，也不推定其他条件下的响应。列表同时有获准项和未获准项时，本页不推定部分接受规则。

## 取文：用通知的 HTTPS URI，另看 HTTP 授权

§4.3.1 针对文档相对业务服务器所存版本已经更新的情况：服务器收到带该文档 HTTPS URI 的 SIP NOTIFY，并用通知里的 URI 取文。文档更新通知也可在业务运行期间到达。经 CSC-5 取文时，服务器按配置发 HTTP GET，请求 URI 指向目标 XML 并包含相应 AUID。这条取文规则并未把收到 NOTIFY 写成通用前提。（§6.3.3.2.3）

HTTP 发送端按 TS 24.482 附录 A 的网络实体客户端角色处理；CMS 按所引规则辨认这笔 HTTP 的发送方，用它作认证身份做授权（§§6.2.3、6.2.4.1）。SIP PAI 过清单、收到 NOTIFY、收到所请求文档正文，是三件事。查现场时，把业务服务器实际收到的 HTTP 响应对回同一文档的 GET；不要从 SIP 成功推出 HTTP 授权、拿到正文或业务已应用。这里不推导凭据格式和两种身份的映射。

**只以 MCPTT 为例：**业务配置文档是 `global` 树中的 `service-config.xml`，每个任务关键组织一份。§8.4.2.9 给出单组织根例 `mc-org-domain/mcorg12345/org.3gpp.mcptt.service-config/global/service-config.xml`，也给出共用根时的组织子目录例 `CMSXCAPROOTURI/org.3gpp.mcptt.service-config/global/mc-org-name/service-config.xml`。查的是组织的业务档，不是[某个 UE 的 `users` 目录](initial-ue-config-xcap.md)。原文明示用户访问只读，读写只给该组织系统管理员；`global` 本身不证明某次 HTTP 获准。不要把这两个 URI 示例当成部署唯一命名规则。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcs-server-service-config.json)
