# 位置订阅的 201，和位置通知的收件应答有什么区别？

**创建订阅与收到通知是两笔事务。** 这里限 Rel-19 **TS 24.283 V19.3.0 Stage 3** 的 `LMS_Information`，讨论位置管理客户端（LMC）向位置管理服务器（LMS）订阅他人位置。查条款不用先有抓包；判断某次交付才需要下面的证据。

| 查哪一笔 | 怎样确认 |
| --- | --- |
| LMC 创建订阅 | LMC 向 LMS 发 `POST {apiRoot}/lms-information/v1/subscriptions`。LMS 成功创建订阅后，回这笔请求的 `201 Created`，`Location` 给出新订阅资源的 URI。它不是通知回调地址，也不能证明以后这项订阅仍在生效。 |
| LMS 发出位置通知 | LMS 向请求订阅的 LMC 另发 `LocationInfoNotify` HTTP POST，正文是 `LocationNotification`。按正文和 API 表，目标取订阅请求给的 `locationNotificationUri`；规范性附录在这处另有不一致，见下文。 |
| LMC 收到这份通知 | 查目标 LMC 实收这份通知的证据，或该 LMC 对同一回调的实际匹配收件应答。仅有 LMS 出站记录、孤立状态码，或只知中间节点转出响应，都不能确认目标 LMC 实收。匹配的错误响应不是收件确认。缺收件记录也不等于送达失败。 |

[创建步骤 §6.3.2.3.2，印刷页 27–28](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=28)；[资源与响应 §7.2.3.3，印刷页 63–64](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=64)；[通知程序与回调表 §6.3.2.4.2、§7.2.5.2，印刷页 28、69](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=70)。

**同一用户或同一回调地址不能替代订阅标识。** 表 7.2.6.2.4-1 把 `subscriptionID` 一般标为可选，表注明确：**因订阅而发送通知时必带**。把这个 ID 与实际订阅和目标 LMC 对上。已有独立证据对上这次通知，就不要求同一份记录也有历史创建的 201。一次性位置请求也用位置通知程序，不能仅凭地址或状态码认定它来自订阅。只看到正文片段、没找到 ID，既不能判定实际通知缺字段，也不能据此判成一次性请求。[表 7.2.6.2.4-1 及表注，印刷页 71](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=72)。

### 同一版标准有两处不一致

| 核对项 | 原文分别怎么写 |
| --- | --- |
| 目标 LMC 对通知的应答 | §6.3.2.4.2 第 1 项写 **201**；§7.2.5.2.3.1 的响应表与 Annex A.3 的订阅回调写 **204**。对照 OpenAPI 响应定义看到的是 204。接收方对通知回的 201 即使实际抓到，也不属于 LMS 创建订阅的那笔 201。 |
| 回调地址从哪里取 | 流程和回调表用订阅请求的 `locationNotificationUri`，A.3 的请求 schema 也将它列为必需。A.3 的 `subscriptionNotification` 却引用 `subscriptionResponseUri`，同一个请求 schema 没定义这个字段。|

[A.1 的附录优先规则，印刷页 73](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)只管 API 信息元素和方法的编码，业务程序仍要读正文；[A.3 的订阅回调，印刷页 91](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=92)与[请求 schema，印刷页 94](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=95)须分别核对。不要把两个字段认作别名，也不从原文不一致推出实现必须同时接受 201 和 204。确认目标 LMC 的应答属于本笔通知，是对**实际收件证据**的判断，与接口编码是否合规是两件事；收件不证明应用已显示或使用位置，也不证明取得了新坐标。若要确认 LMS 收到 LMC 的应答，另查 LMS 实收。

若问题是动态组目标、通知或取消的业务流程，另查 **TS 23.280 V19.9.0 Stage 2** 的[位置订阅](subscription-lifecycle.md)。LMS 为取得组归属而做的 SIP 订阅不是这笔 HTTP 位置订阅。若问题是 LMC 登记或 `locationConfigUri` 的配置回调，另查 [LMS_Reporting 注册与配置](lms-registration-configuration.md)。位置通知既不是配置下发，也不是被查询终端向 LMS 上报位置。
