# 主系统 MCPTT 配置：初订怎么分流，首个 NOTIFY 给了什么？

**首个 NOTIFY 不等于取到正文。**TS 24.484 的示例中，第一次 SIP NOTIFY 给的是文档定位和 ETag。终端随后按文档发 HTTP GET，CMS 在对应的 HTTP 200 正文里返回配置。单看 SIP 200 或 ETag，不能确认终端已经收到、保存或采用某份配置。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）。用 §6.3.13.2.2、§6.3.13.3.2.2 判断终端的**多文档代理订阅**；直接订阅的初订入站另查 §6.3.13.3.2.3。用资料性附录 A.2.2 辨认此例的消息与现场证据。主系统的[初始配置、默认配置档和认证次序](primary-ue-online-configuration.md)另查。

## 先辨认这一条 CMS 代理订阅

- **终端发出。**配置管理客户端（CMC）把初始 SIP SUBSCRIBE 的 Request-URI 设为 CMS 订阅代理的公共业务标识（PSI）。`application/resource-lists+xml` 按所需文档或元素写相对引用；`application/vnd.3gpp.mcptt-info+xml` 的 `mcptt-access-token` 取自 TS 24.482 的认证过程。终端在 `P-Preferred-Service` 中使用 MCPTT 的 ICSI `urn:urn-7:3gpp-service.ims.icsi.mcptt`。（§6.3.13.2.2 初始请求）
- **CMS 收到。**代理分支核对 `Event: xcap-diff`、自己的代理 PSI、两类正文和 `P-Asserted-Service` 中的 MCPTT ICSI。该入站分支还要求有 `P-Asserted-Identity`、其中没有授权 MCS 服务器清单中的身份。CMS 从访问令牌取得发起方 MCPTT ID，用这个身份判断订阅权限；不是直接把入站的断言身份当成授权用户。例如认证身份对清单中的资源都无订阅许可时，CMS 回 SIP 403 并停止本分支。权限有允许也有拒绝时，不能据此断定处理结果。收包条件的 MIME 带 `mcptt-info`，取令牌的 c 项写为 `mcpttinfo`，不据这一处拼写另定线上 MIME。（§6.3.13.3.2.2）
- **通知对应哪次订阅。**在初始代理请求的资源条目 URI 带有标识配置文档应用的 `auid` 时，CMS 在该请求建立的订阅对应的 NOTIFY 中返回文档 XCAP URI。CMC 收到的是本订阅的 NOTIFY，才查这一条的处理。这里不展开身份隐藏下的保护流程，也不把业务服务器发起的订阅套进来。（§6.3.13.3.2.2 e 项；§6.3.13.2.2 的接收段）

## 初订用 XCAP 根：先查 CMC 直接订阅

**CMC 发出。**初始 SIP SUBSCRIBE 用直接订阅时，Request-URI 是 SIP URI，基址等于 CMC 配置的 CMSXCAPRootURI，auid 标识配置文档的应用用法（§6.3.13.2.2 a）。c、e、f 项还要求：按认证过程取得的 mcptt-access-token 放在 application/vnd.3gpp.mcptt-info+xml；P-Preferred-Service 的 ICSI 和 Contact 的 g.3gpp.icsi-ref 都用 urn:urn-7:3gpp-service.ims.icsi.mcptt。需要身份隐藏时另核 d 项。b 项的资源清单用在多文档代理程序；直订 a 项不列它，不能据此说直订禁止带清单。

**CMS 收到。**§6.3.13.3.2.3 的标题写 CMC 发起，初订入站条件却明确要求 P-Asserted-Identity（PAI）**含授权 MCS 服务器清单中的身份**。这不是把标题改成 MCS 服务器发起的理由。CMS 针对同一笔实收的初始 SIP SUBSCRIBE，还核 Event: xcap-diff、Request-URI **基址**等于自己的 XCAP 根，以及 P-Asserted-Service 中同一 MCPTT ICSI。四项符合时，CMS 按所引 RFC 5875 作通知方。§6.2.4.1 的清单由该 CMS 所属 MCS 提供方的 MCS 服务器 PSI 组成；不据这条推入站 PAI 是由终端怎样生成、如何把用户 ID 或令牌变成 PAI。

**别把近邻分支套进来。**上面的代理初订查自己的**代理 PSI**、PAI **存在但不含**清单身份及两种指定正文；缺 PAI 不满足这项。另见[业务服务器初订](mcs-server-service-config.md)：该入站条款也要 PAI 含清单身份，但 Request-URI 的基址是 **CMS PSI**，不把直订条件改成所有白名单来源都走同一分支。直订入站段没有单列 auid 或令牌正文条件；不能据此省略发端要求。只按初订段判断作通知方，不从它推出成功状态码、实际首个通知的正文、已取文或续订结果。

## 这几个 200 的对象不同

| 资料性附录 A.2.2 的步骤 | 现场消息能说明什么 |
| --- | --- |
| **4–5：SIP 200 对 SUBSCRIBE** | 例中 CMS 已完成这次订阅的授权，并经 SIP 核心返回确认。不是送达配置文档。 |
| **7–10：首个 SIP NOTIFY，随后 SIP 200 对 NOTIFY** | 实际收到的 NOTIFY 正文类型是 `application/xcap-diff+xml`。对每份文档，它给出 `sel`、`new-etag`、`previous-etag`，没有附上该份配置 XML。CMC 回复的 200 确认这条通知，不确认已取到配置。例中每份文档的新旧 ETag 相同，后面仍取文；只凭这两个值不知道终端当前本地版本。初始 SUBSCRIBE 的 `Accept` 中示例还写了 `message/external-body`，只说明支持内容间接引用。 |
| **11–16：另发 HTTP GET，各有 HTTP 200** | CMC 依据通知中每条文档的 `sel` 定位 XCAP URI，分别取 UE 配置、用户配置档和示例中的离网业务配置。CMS 对每次取文另核 HTTP `Authorization` 中的访问令牌；成功响应携相应 XML。示例的离网业务配置响应是 `common` 和 `off-network` 两部分，不能替代主系统正文对已启用业务的说明。 |

正文 §6.3.3.2.1–.2、§6.3.3.3 规定 CMC 通过识别目标文档的 HTTP GET 取文，使用配置的 XCAP 根与该应用的 `auid`。抓包时，确认是 **同一份文档**对应的 GET，且终端实际收到匹配的 HTTP 200 和配置正文。看到 CMS 发出响应、只见状态行、收到另一份档，都不足以证明这一份已到。正文 §4.2.2.1.1 讲的是有更新时 CMC 更新本地副本；它不是看到首个 NOTIFY 就能断定副本存在、已保存或业务已改用的依据。例中有 GET，不表示每次收到通知都必须重取，或有一套通用 ETag 比较规则。

找原文时注意两个例内标号：第 7 步引用表 A.2.2-7，紧随其后的表题印为 A.2.3-7；第 12 步标题的方向印成 CMC → CMS，段落、表题和图 A.2.2-1 都是 CMS → CMC 的 HTTP 响应。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](cmc-subscription-notify-fetch.json)
