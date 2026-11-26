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

## 创建订阅：401、两种 403 和 201 各到哪一步？

这里看 LMC 向 LMS 发的 **`POST {apiRoot}/lms-information/v1/subscriptions`**，不是个别订阅 PUT、一次性 `/requests` 或收到位置时的回调。查标准无需抓包；判断实际拒绝，先对上这笔请求及 LMS 的应答。

| LMS 检查的条件 | 本次创建怎样处理 |
| --- | --- |
| 请求同时带 Bearer 方案及其访问令牌、又带 `x-3gpp-asserted-identity`；或任一访问令牌未通过校验 | 回 **401**，停止。不因其中一个令牌有效就忽略另一个，也不从 401 单独判断是两类凭据并存还是令牌验不过。 |
| 进入目标检查时，用户 ID、功能别名 ID、组 ID 三类目标数组全空 | 回 **403**，`Warning` 文本为 `Invalid subscription request target client list`，停止。只看到请求片段或某一类数组为空，不足以判三类全空。 |
| 通过入口目标检查后，MC 用户的配置文档找不到一条在 `<action>` 内将 `allow-subscription-on-location-information` 设为 `true` 的 `<rule>` | 回 **403**，`Warning` 文本为 `Unauthorized for location subscription`，停止。这里核的是创建订阅的许可，不是针对某个目标的分享许可。 |
| 前述检查通过，LMS 创建资源 | 生成独有的订阅标识，创建资源，回这笔 **201** 及 `Location`。不能拿已有订阅的更新结果、另一次查询或一次通知的状态码判本笔创建。 |

LMC 带全部适用于其有效 MC service ID 的 Bearer 访问令牌；LMS 从令牌派生发起者的业务身份。`mclocClientID` 只区分客户端实例，不是认证身份。原文还列出 MC 业务服务器、IWF 和另一 LMS 用断言头携带自身 PSI。接收步骤 3 写：**没有规定的 Bearer 头及令牌、但有该断言头时**，取其 URI 为发送者身份。同时，§7.2.9 要求按 TS 24.482 确定认证身份并用于授权；有头不等于授权通过。接收段按 LMC 描述，A.3 的 `/subscriptions` POST 声明 BearerAuth。不能据此为网络发起方补一个完整的创建、应答与回调流程，也不能规定缺两类凭据的固定返回码。[§§4.3、6.3.2.3.2、7.2.9，印刷页 12–13、27–28、72](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=28)；[A.3，印刷页 90](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=91)。

**201 先于逐目标判断。** 这是 LMS 的处理顺序，不是请求端的收包时序。创建后按一次性查询 §6.3.2.2.2 的步骤 6–11 决定订阅实际涵盖谁：组查询许可与当前动态归属、已激活别名或直接点名的展开、发起者对该目标的查询许可、目标对该发起者的分享许可。创建订阅的许可不能替代后两份判断。哪些规则可按本地策略核查、以及外属目标的另一次 LMS 请求，见[一次性查询的目标判断](lms-one-time-location-request.md#我问了哪些人哪些位置可以给我)。订阅以归属或已激活别名展开目标时，目标可能随订阅期间的实际状态变化。只复用步骤 6–11，不把一次性查询步骤 12 的强制刷新带入订阅；订阅段另写 LMS 可能需要更新所订阅 LMC 的上报配置。非空目标后来被筛除，不是入口全空的 403；201 或没见某人的位置，均不能说明该用户拒绝分享、终端离线或未来没有通知。现场要确认哪一项实际到了，仍核本订阅的匹配通知及正文。[§6.3.2.3.2 末段及 §6.3.2.2.2 步骤 6–11，印刷页 25–28](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=29)。

A.3 的 `LocationSubscriptionRequest` 必带 `expTime`、`mclocClientID` 和 `locationNotificationUri`。`anyOf` 检查三类目标字段至少一个存在，未设数组最小长度；表 7.2.6.2.5-1 将可选数组的条目数列为 `1..N`。通过这一项 schema 检查不等于目标非空或获准创建。正文写 `mclocClientId`，表和 A.3 写 `mclocClientID`；不设字段别名。A.1 的附录优先只限 API 信息元素和方法的编码，未表达的程序条件仍适用。[印刷页 71、73、94](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=95)。

## 同一订阅已创建：更新、取消和到期

本节仍限 **TS 24.283 V19.3.0 Stage 3 的 LMS_Information**。查规则不必先有抓包。要判断某一次结果，先对上那一个订阅资源、LMC、LMS 及实际请求和应答。同一显示名、同一通知地址或孤立状态码不能代替关联。

### 更新用完整 PUT，不是只改 expTime

LMC 向 LMS 的**个别订阅资源**发 `PUT`，用完整 `LocationSubscriptionRequest` 替换原资源的全部属性。请求带客户端实例 ID、通知地址 `locationNotificationUri`、至少一类目标清单（用户业务 ID、已激活功能别名或组 ID），以及到期日期时间 `expTime`。流程写 `mclocClientId`，表和 A.3 请求 schema 写 `mclocClientID`。只发 `expTime` 不是这条完整替换，也不能据此认为旧字段已保留或新期限已经生效。[§6.3.2.5.2，印刷页 29–30](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=30)；[表 7.2.6.2.5-1，印刷页 71](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=72)；[A.3 请求 schema，印刷页 94](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=95)。

- **更新成功：**LMS 替换完整资源后回这笔 `PUT` 的 `204`，流程和响应表都这样写。A.3 的 `UpdateLocationSub` 另列带 `LocationSubscriptionRequest` 正文的 `200`，并列无正文的 `204`。别把 A.3 的 200 填回流程，也不要求实现接受两种写法。只见 LMS 发出成功应答不能确认 LMC 实收；这也不是 GET 读回，不证明更新后任何一份通知已发、已到或被应用使用。[§6.3.2.5.2 第 7–8 项，印刷页 30](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=31)；[表 7.2.3.4.3.1-3，印刷页 66](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=67)；[A.3 PUT，印刷页 91–92](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=92)。
- **更新受拒：**流程第 4 项列出两类造成 `401` 的凭据校验情形：实际同时带规定的令牌和网络身份头，或任一令牌未通过校验。目标清单全空与没有获准订阅的配置规则都可导致 `403`，但 Warning 文本和判定条件不同；这些分支都停止处理本次更新。只见 401 或 403 不能反推是哪一条。[§6.3.2.5.2 第 4–6 项，印刷页 29–30](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=31)。

### 取消用 DELETE，同一 204 也可能是别的应答

LMC 向 LMS 的**同一个别订阅资源**发 `DELETE`。收到请求后，LMS 先核实该 LMC 的身份和删除权限。获准后，找不到按订阅 ID 标识的资源则回 `404`；找到就删除这项订阅及其资源，回 `204`。正文没有为未获准分支指定一个固定状态码。要把实际 404 归到「获准但找不到」，须另证该条件；孤立 404 不能说明权限、是否曾存在或是否已过期。匹配的删除 204 是该资源的成功结果，不是存储清理或其他订阅已结束的证据。只见发出 DELETE 不能确认 LMS 已收到。也不能拿 PUT 或 LocationInfoNotify 的 204 确认这次删除。[§6.3.2.6.2，印刷页 30–31](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=31)；[表 7.2.3.4.3.2-3，印刷页 67](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=68)。

### 到期约束发送，不把迟到当成取消失败

创建和更新的末段都规定：LMS 反复发这项订阅的通知，直到按**生效的 `expTime` 到期**，或收到退订消息。仅在未确认结果的更新请求里见到新期限，不能按新值判断。收到退订和获准删除仍分别查；条文没有给被拒绝或并发退订补出调度顺序。到期或删除成功后 LMC 才见通知，不等于 LMS 在界线之后才发。这里没规定在途通知如何排空，也没规定到期时必须删存储或停掉该终端的上报、注册和其他订阅。[§§6.3.2.3.2、6.3.2.5.2 的末段，印刷页 28、30](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=29)；[§6.3.2.6.2，印刷页 30–31](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=31)。

### 这版的路径和 DELETE 正文不要靠猜

- §7.2.3.4.2 印 `{apiRoot}/lms-information/<apiVersion>/subscription/{subscriptionID}`；资源总表和 A.3 写复数 `/subscriptions/{subscriptionId}`，A.3 基址为 `{apiRoot}/lms-information/v1`。创建的流程和 A.3 使用 `Location`，而印刷页 64 的表 7.2.3.3.3.1-5 写 `Locationn`，例子还用 `lms-location-information`。认实际资源要查这一订阅的返回地址或独立关联证据。别重拼 URI、把拼写视为别名或猜哪种回退可用。更新第 7 项的印刷回指 §7.2.3.3.3 指向集合 POST 小节，不把本次个别资源 PUT 改成重建订阅。[印刷页 28、30、62、64–65](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=65)；[A.3，印刷页 89–92](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=90)。
- DELETE 的请求体表 7.2.3.4.3.2-2 把类型写成 `n/a`，又标 `M 1`；同页还有 POST 和 200 的表标签，成功响应行则写 204。A.3 的 DELETE 未声明 `requestBody`。A.1 对附录的优先规则限 API 信息元素和方法的编码；这里不补空 JSON、必填更新体或兼容约定。[印刷页 67、73、92](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=68)。

TS 23.280 V19.9.0 的组目标与取消业务流程、LMS_Reporting 的 LMC 登记续期分别读上文入口，不借它们解释这一项订阅的资源结果。
