# 向 LMS 查一次位置：201 之后，谁的位置到了请求端？

**201 确认的是查询资源，不是位置。** 请求端 LMC 向 LMS 发 `POST /lms-information/v1/requests`；LMS 在这笔事务返回 201，表示已为请求建资源。位置通过另一笔 HTTP POST 发回。例如，请求里有甲、乙，回调里只收到甲的位置：可以确认甲的这一项到了，不能据此断定乙拒绝分享，也不能认定甲的位置是刚测的。

这里读 **3GPP TS 24.283 V19.3.0，Release 19，Stage 3** 的一次性查询。查规范无需抓包；要判断某次通信，先分清三条路径：

| 哪一笔 | 发给谁 | 它能说明什么 |
| --- | --- | --- |
| 创建查询：`POST /requests` → 201 | 请求端 LMC → LMS | 此次匹配的 LMS 201 表示创建成功。`Location` 是新资源的 URI；应答体类型是 `ClientOriginatingLocationRequest`，没有在此返回查询到的位置。该资源表只列 POST，不能据此设计 GET 取结果。 |
| 返回位置：`LocationInfoNotify` POST | LMS → **请求端** LMC 留下的 `locationNotificationUri` | LMS 应发送一条或多条通知，每条可含一个或多个 MC UE。要说某位置已到请求端，看该 LMC 实收的匹配通知及其中的目标条目。 |
| 要目标上报：`LocationReportRequest` POST | LMS → **目标端**已注册的 LMC | 一次性查询显式要求刷新时才触发这里的步骤。请求上报、目标回报和请求端收到位置是不同的事。 |

[查询程序 §§6.3.2.2.1–.2，印刷页 24–26](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=25)；[资源与 201，§§7.2.3.1–7.2.3.2.3.1，页 62–63](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=63)。LMS 在步骤 5 发出创建应答，之后才检查组、目标和刷新。这个顺序不是两个端点实际收包时间的保证。LMS 已发 201 与请求端已收到 201 也要分开。

## 我问了哪些人，哪些位置可以给我？

请求携带适用的全部 Bearer 访问令牌、请求端 LMC 的实例 ID、接收结果的 URI，以及至少一类目标。LMS 从验证的令牌取得发起者的 MC service ID；客户端实例 ID、别名、回调地址和目标 ID 都不是这个凭证。任一令牌验证失败，LMS 回 401 并停止；通过令牌检查后，若三类目标数组实际全空，则回 403，Warning 为 `Invalid location request target client list`，也停止。未抓到完整数组、或数组有内容但目标后来被过滤，不是这条 403 条件。一次性查询没有把订阅创建的“混合身份头”拒绝条件照搬过来。

1. **直接点名**：取列出的 MC service ID。**按功能别名查询**：取实际激活该别名的用户 ID；仅配置过别名不够。
2. **按组查询**：先看发起者是否获准按该组查询：发起者配置规则匹配组 ID，`allow-request-location-of-groups=true`。不满足则忽略**这一个组**。对获准的 MCPTT、MCVideo 或 MCData 组，LMS 以服务于发起者的相应业务服务器角色订阅组动态数据，从收到的通知取当前已归属（affiliated）用户。静态成员名单和单独一笔 SIP SUBSCRIBE 都不是归属结果；忽略组也不会自动删掉被直接点名的同一人。
3. **看每个目标的两份许可**：发起者能不能查目标，和目标能不能向该发起者分享。正文允许按本地策略核查；按配置规则时，前者用发起者的规则匹配目标 ID，查 `allow-request-location-of-users=true`；后者用目标的规则匹配发起者 ID，查 `allow-to-share-location-information=true`。组许可不代替其中任一份。原步骤 9、11 的“忽略”分支只回指身份匹配项 i)，不能由它补出所有策略失败的处置或状态码。
4. 不属于当前 LMS 的目标，步骤 10 要求向拥有它的 LMS **另发请求**；怎样发现那个 URI 不在本规范范围。步骤 10 在两份许可核查步骤之间。不要把它读成同一 LMS 的不同实例之间用 307/308 重定向，也不要从另发请求推断对端已给结果。

[目标展开与权限，§6.3.2.2.2，页 25–26](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=26)；[安全与同 LMS 重定向，§§7.2.9–.10，页 72](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=73)。正文也列 MC service server、IWF 和另一 LMS 发起时用 `X-3GPP-Asserted-Identity` 携带其公共服务身份（PSI）。详列的接收和通知步骤写的是 LMC，A.3 的 `/requests` 声明 BearerAuth；§7.2.9 另要求确定认证身份，并给出获准 MC service server 的 PSI 清单。不能从这些条文补出网络发起者的完整授权和回程。

## 怎么看这一份结果？

`LocationNotification` 给出请求者的 `requestingMcServiceId`，可给出请求者已激活的别名。逐项看 `MCUserLocation` 的目标 `mcServiceIds` 和 `locationInfo`；设备标签 `mcServiceUELabel` 和目标已激活别名可选。同一用户有多台终端时，不把不明设备的一条位置算到每一台上。

收到这一笔通知，或有**该请求端 LMC 自己发出的匹配收件应答**，可认定该 LMC 收到这笔通知；判定哪一项到了，还需对应正文。只见 LMS 出站、代理回码、匹配的错误响应或另一实例收件不够。LMS 是否收到了应答、请求端应用是否采用或显示结果，是另外两件事；正文只说它可以使用。

一次性查询与订阅共用通知操作。A.3 的这两个一次性请求/通知模型没有一次性查询 ID；若两笔查询用了同一地址、同一用户，要靠能区分这笔请求的上下文关联。同一次查询可有多条通知。缺少 `subscriptionID` 并不能指定归属。判断某次通知由订阅触发，要看通知实际携带的 `subscriptionID` 是否与同一个别订阅、应收的请求端 LMC 对应。收到多次、ID 未知或错配都不足以认定是订阅。只查标准里的订阅规则不要求有这些抓包记录。

至少一类目标数组提交时非空，后续却没有任何目标通过筛选，这与入口三类数组实际全空不同，不能套步骤 4 的请求级 403。这里的条款没有说明全被筛除时是否发送空结果 POST、逐目标拒绝或最后一条通知，也未给等待期限。通知不列逐目标拒绝原因，也未给最后一条标记或完整性清单。没看到乙不等于乙离线、拒绝、查无位置、整次查询已完成或最终不会有另一条通知。

[通知程序 §6.3.2.4.2，页 28](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=29)；[通知表与数据类型 §§7.2.5–7.2.6，页 69–71](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=70)；[A.3 的结果类型，页 94–95](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=95)。

## 怎样判断位置是否新测？

步骤 12 要求 `refresh` **存在且为 true**，LMS 才因这一条件向相应目标 LMC 要报告。地址来自目标端注册时提交的上报请求回调，不是请求端的 `locationNotificationUri`。`false`、`null` 或未传不满足这一步，也不能反推目标没有因其他事件更新。即使是 true，仍要看目标实际给了哪次测量：将目标、设备、报告与本次结果关联，核完整报告的 `locTimestamp`（测量时刻）或可独立验证的测量证据。请求时间和回调到达时间都不是测量时间；通知条目只嵌套 `LocationInfo`，不是整个 `MCUELocation`。位置也不必是经纬度。可选的历史范围或状态请求不是已经取回完整历史的证明。

**若另外核实目标回报**：§6.2.2.7.2 和 A.2 的目标 LMC 对 `LocationReportRequest` 答 200 + 位置报告（`MCUELocation`）；表 7.1.5.3.3.1-2 则写 204、无正文。§6.2.2.8.1 另写目标收到请求时发布位置报告（独立 POST）；不能把发布、前述应答和请求端通知算成同一笔，也不能据此认定两处都实际传了同一测量。上报路径可出现的请求/报告 ID 不等于一次性查询共享的端到端 ID。[§§6.2.2.7–.8，页 21–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=22)；[表，页 42](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=43)；[测量时刻，页 56–57](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)；[A.2 回调，页 74–75](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=75)、[报告模型，页 86–87](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)。

## 对照抓包与本版 API 时

- **返回位置的收件码**：§6.3.2.4.2 写请求端 LMC 回 201，表 7.2.5.2.3.1-2 和 A.3 一次性查询回调写 204、无正文。它们都不是创建查询的那个 201。A.3 的 `locationRequestResponse` 取 `locationNotificationUri`；写成 `subscriptionResponseUri` 的是另一项**订阅**回调。一次性 204 描述误称 Configuration，但请求体引用 `LocationNotification`。不推定双码兼容或地址回退。
- **字段写法**：正文写 `mclocClientId`、`mcServiceIDs`、`requestedLocationHistory`、`requestedLocationStatus`、`mcUserResponseList`；表和 A.3 相应写 `mclocClientID`、`mcServiceIds`、`requestLocationHistory`、`requestHistoryStatus`、`mcUEResponseList`。表 7.2.6.2.2-1 行内 `functionalAliasIds`，表下注却写 `functionalAliasIDs`。不据此把不同拼法声明为可互换。表和程序写的必需正文、条目及目标不能用 A.3 未列 `required` 或 `minItems` 推翻；A.3 请求的 `anyOf` 检查至少一类字段存在，不检查数组非空。A.3 把 `refresh` 定义为可空布尔，其描述按字段存在表述；步骤 12 还要求值为 true。
- **印刷引用**：步骤 9/11 分别回指 6/7，实际合并三路目标 ID 的是步骤 8；步骤 12 也写“步骤 8 的 LMC”，而 8 列的是 service IDs。页 63 的 201 响应行和 A.3 要求返回 `Location`，同页单列的 201 头表却写 n/a。§7.2.2.1 指 A.4，但 §6.1 表 6.1-2 列 A.3，本版实际定义也在 A.3；其 externalDocs 写 V19.1.0，不改变本页固定原件 V19.3.0。
- [A.1，页 73](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)的优先范围是 API 信息元素和方法的编码，未在 OpenAPI 表达的程序和适用条件仍有效。核实现分别看 [A.3 创建与回调，页 89–91](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=90)和 [A.3 字段，页 93–95](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=94)。

要问订阅创建、更新、取消或由订阅触发的通知，读[位置订阅](lms-subscription-notification.md)；要问注册与配置，读[LMS_Reporting](lms-registration-configuration.md)。[单系统按需位置](on-demand-usage.md)和[IWF 跨系统位置查询](../interworking/location-query.md)是不同的 Stage 2 信息流；[MCData 本地直接 ID 查询](../mcdata/local-location-request.md)是另一套 Stage 3 业务程序。
