# MCPTT 配置续订换清单：CMS 何时在 NOTIFY 里给文档地址？

CMC 已使用 CMS 订阅代理，又要更改所订阅的配置清单。**看 CMS 实际收到的续订列表里的这条 `entry`：其 `uri` 是含配置管理文档应用 `auid` 的 XCAP URI，且该文档没有按 §6.3.13.3.2.3 建立的相关订阅。** 这里不要求把 XCAP 引用写成绝对 URI。条件都成立时，CMS 要在与初始 SUBSCRIBE 建立的订阅关联的 NOTIFY 中给出该文档的 XCAP URI。已有上述相关订阅时，不触发这里新增的返回地址要求。不能据此断言 CMS 不会发通知或不会在别处给地址。没看到相关订阅的记录，也不等于已经证实它不存在。

依据：3GPP TS 24.484 V20.1.0，Release 20，Stage 3，§6.3.13.2.2 的续订段与 §6.3.13.3.2.2 的 CMS 收包段。这里是终端配置管理客户端（CMC）改清单，不是业务服务器订阅业务配置。

## 哪个请求算改清单

- **终端发出。**CMC 发 SIP re-SUBSCRIBE。用代理订多项时，`application/resource-lists+xml` 正文里每项文档或元素各一条 `entry`，`uri` 按所引 RFC 5875 用文档相对路径引用。Contact 的 `g.3gpp.icsi-ref` 含 MCPTT ICSI `urn:urn-7:3gpp-service.ims.icsi.mcptt`。若走直接订阅，条文另写 Request-URI 是以终端配置的 `CMSXCAPRootURI` 为基地址、带对应 `auid` 的 SIP URI。代理续订项没有重述初订的代理 PSI 赋值；也没有在此规定删掉旧条目、改空清单或原样续期的处理。
- **CMS 收到。**CMS 的代理续订段要求这条 re-SUBSCRIBE 的 Event 为 `xcap-diff`，且带那类列表正文。CMS 按所引 RFC 5875 担任通知方。再分别核每个条目的 `auid` 和上述相关订阅条件。收到 NOTIFY 与收到文档正文是两件事；只看到新列表、SIP 响应或 URI，不能证明文档已经取回、新建了另一个订阅，或业务已经采用。初始代理订阅对应的地址规则没有写续订这项附加条件，不用初订规则推断换清单结果。

## 要隐藏身份时，两端查的条件不同

- CMC 在续订时需要隐藏身份，使用初始 SUBSCRIBE 中包含的 CSK，对 `application/vnd.3gpp.mcptt-info+xml` 与 `application/resource-lists+xml` 应用条文所引的保密和完整性保护。
- CMS 收到适用续订，列表中有 `EncryptedData`，且初订已在 `application/mikey` 正文中收到 CSK，须解密这个列表。两个条件要一起核；看到续订中出现加密列表，不能单独认定此条件已齐。
- 同节还有独立的发送条件：CMS 发送与初订建立的订阅关联的 NOTIFY，且初订已在 `application/mikey` 正文中收到 CSK，须对该 NOTIFY 应用所引的保密和完整性保护。不能用收到续订并解密列表，替代发送保护的证据。

这里未核 TS 24.379 的具体保护流程，也不推断重发 CSK、重发令牌或鉴权例外。

初次订阅和取文另查[首次 NOTIFY 与实际取文](cmc-subscription-notify-fetch.md)。若发起方是业务服务器，查[业务服务器订阅及续订鉴权](mcs-server-service-config.md)。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](cmc-subscription-refresh.json)
