# LMS 向目标 LMC 要位置：这笔回调拿到了报告吗？

**先看方向和正文。** 在 TS 24.283 V19.3.0（Rel‑19 Stage 3）中，`LocationReportRequest` 是 **LMS → 已注册的目标 LMC** 的 HTTP POST。LMS 实收目标 LMC 对这笔 POST 的 **200 + 位置报告**，才能确认这一跳拿到了报告。印刷表的 **204** 只写请求收件，没有位置正文。两种写法不能当同一结果，也不是终端另发的上报 POST。

## LMS 发给哪个地址？

LMS **可以自行决定**向已注册的 LMC 要一份报告，先前不必有LMC 发起的查询，也不必等位置上报事件。目的地址是**目标 LMC 的适用注册中提供的 `locationRequestUri`**；用 POST，JSON 正文为 `LocationRequest`。API 的 A.2 将它列在注册 POST 的回调下，表达式读取注册请求正文的该字段，不是拼接 LMS 的 API 路径。不是配置回调地址 `locationConfigUri`，也不是查询方接收通知的 `locationNotificationUri` 或注册 201 的 `Location`。用户有多台 LMC 时，要对上这一次的实际 LMC 和注册；只知同一用户不代表每台设备都收到。

§6.2.2.7 没有另列本操作的能力握手或 GPS 可用先决条件；§7.1.8 也未定义该版 LMS_Reporting 的可协商特性（见[两接口的协商和错误规则](lms-registration-configuration.md#lms-特性协商与空错误表)）。这不等于目标必须能给出 GPS、所有所要字段或历史，也不从请求发出推送达。IMS 注册成功不能替代这里的 LMS 注册。查规范不必有抓包；现场先核目标的适用注册及回调事务，不要求同一段记录也含此前注册的 201。[§§4.1–4.2、6.2.2.2.2、6.2.2.7、7.1.8，印刷页 12、17–18、21–22、60](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=22)；[§7.1.5.3 与 A.2，印刷页 41–42、74–75](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=42)。

## 正文区分「要谁报」和「谁想知道」

| 字段 | 这笔请求的意思 |
| --- | --- |
| `requestedMcServiceId` | 必须给**要上报的用户**的 MC service ID。已激活的 `requestedFunctionalAliasId` 可附带，不替代这个 ID，也不代替注册回调地址。 |
| `requestingMcServiceId` | 若上游由 LMC 发起，正文要求填写**请求位置的用户**的 MC service ID；LMS 自行发起、此前没有 LMC 触发时不需要填。可附带请求者的已激活别名 `requestingFunctionalAliasId`。表和 A.2 把这两个 `requesting…` 字段的说明写成从其索取位置的用户；不要据此把请求者填成上报目标，也不把 LMC 条件扩成其他网络发起方的填法。 |
| `requestedLocationInfo`、历史请求、`requestId` | 可指明所需位置字段，也可索取历史明细或历史状态，或带本笔请求标识。历史明细可选数量、时间范围等；历史状态是摘要，不是历史报告本身。正文将两个历史请求写为 `requestedLocationHistory`、`requestedLocationStatus`，表/A.2 写 `requestLocationHistory`、`requestHistoryStatus`。不造兼容别名，也不从请求条件推已经给了历史。 |

表 7.1.6.2.47-1 的请求者字段是一般可选；A.2 的 `LocationRequest` 也没有必需字段清单，仍要保留上面的操作条件。若实际请求带 `requestId`，请求触发的 `MCUELocation` 用 `reportId` 回关联；正文报告条款写 `requestID`、`reportID`。未给 ID 不造值；有相同 ID 不能代替目标、实例与事务匹配，也不证明两笔报告是同一个样本。[§6.2.2.7.2、§6.2.2.8.2、表 7.1.6.2.47-1、.48-1、.49-1、.54-1 与 A.2，印刷页 21–22、55–56、58、85–88](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=56)。

## 哪个结果证明什么？

- **只见 LMS 发了 POST：**不能确认目标收到。看相应目标 LMC 的实际收件或它对这笔请求的真实应答；不要把代理返回、另一个 LMC 的应答或配置通知应答算进来。重定向或错误应答不是位置报告。
- **目标对该次 POST 回 200：**§6.2.2.7.2 要求应答带位置报告，A.2 的 200 正文为 `MCUELocation`。要确认 LMS 已拿到哪份报告，看 LMS 实收的匹配应答及可读正文。目标已发不是 LMS 已收；只知道状态码、抓包里没有正文，不能判断报告内容，也不能断言线上必定没有正文。完整应答确实没带报告，就不算这里定义的完整带报告响应。
- **目标对该次 POST 回 204：**表 7.1.5.3.3.1-2 写的是该请求的收件确认，`No Content`，不能提取位置报告。A.2 的这一回调列 200、未列该 204。A.1 的附录优先限 API 信息元素和方法的编码；没写进 OpenAPI 的程序和适用条件仍适用。保留差别，不规定两种码都要实现或接纳。表 6.2.2.1-1 的简介还误写目的为 LMS；方向按过程、回调 URI 表和 A.2 划分。

[§§6.2.2.7、7.1.5.3，印刷页 21–22、41–42](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[表 6.2.2.1-1、A.1 及 A.2，印刷页 17、73–75](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)。

**位置数据不必是经纬度。** 报告可以含适用的小区信息；`locTimestamp`（过程一处写 `locTimstamp`）标的是位置测量时刻，不能用 POST 或 200 的时间补它。和请求对上测量、目标及 LMC 后才能判断是不是刷新后的测量。报告里的 `mclocClientId` 是报告客户端实例，不是用户身份或认证凭据；表把它列为必需，A.2 的类型说明特别提到多 LMC 响应，这不证明只有一台时就可以省略。带报告应答不证明已经保存、转给查询方、显示或取回完整历史。[§6.2.2.8.2、表 7.1.6.2.49-1、.50-1、A.2，印刷页 22–23、56–57、86–88](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)。

**另发报告按另一笔事务看。** 回调过程列出发响应后重置 `minimumReportInterval`；查实际有没有重置要有 LMC 侧证据。§6.2.2.8.1 又要求目标实收请求后执行独立的[位置报告发布](lms-location-report-publish.md)，不套上报事件分支的等待条件。发布的 `POST /lms-reporting/v1/locationreports` 及对应 LMS 201、发布时设置并启动计时器，都不能由回调的 200 或 204 代替。本版没有给两笔网络操作合并、固定可见顺序或同样本的保证。问 **LMC → LMS** 的 `POST /requests` 怎样申请位置、要求刷新或收到结果，去看[一次性查询](lms-one-time-location-request.md)，那是另一项服务。[§§6.2.2.7.2、6.2.2.8，印刷页 22–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)。

## 收到历史状态，算拿到了历史位置吗？

**不算。** 对 LMS 向已注册目标 LMC 发的 `LocationReportRequest`，同一笔应答中的 `locationHistoryStatus` 是摘要，`locationHistoryData` 才承载历史条目。按 §6.2.2.7.2 与 A.2 判断实际拿到什么，要看 **LMS 实收这一笔匹配的 200 及 `MCUELocation` 正文**。印刷表中的 204 只确认请求收件，无报告正文。只查询规范不用先找抓包；现场只有状态码、缺正文或只见目标发出，不能确认 LMS 已取得历史条目。[§§6.2.2.7–.8，印刷页 21–23、表 7.1.5.3.3.1-2，页 42](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)。

| 看哪一块 | 怎样读 |
| --- | --- |
| **索要历史的请求** | 历史明细和历史状态是两个可分别请求的项；本版表与 A.2 分别写 `requestLocationHistory`、`requestHistoryStatus`。历史明细中的 `numberOfReports` 是请求的存储报告数量，`startTime` 指比此时**更新**的报告，`endTime` 指比此时**更早**的报告。两端都给时，恰等于任一端点的测量不满足相应条件。还可用 `triggerCriteria` 描述生成历史报告的条件，用 `minimumIntervalLength` 表明报告间的最短时间（A.2 写秒）。这些不是已取回数量、取样频率或 `minimumReportInterval` 计时器状态的证据。 |
| **`locationHistoryData` 明细** | 按每条 `LocationHistoryEvent` 的 `locationData` 和 `locTimestamp` 核实际历史位置及其测量时刻。不要拿顶层 `MCUELocation` 的时刻或收到 HTTP 应答的时间替代。一个条目也不证明整个区间已补齐。 |
| **`locationHistoryStatus` 摘要** | 表的 `storedReports` 是已存但未报告的数量，`startTime`、`endTime` 是最早、最新的已存报告时间。这两个时间不是请求的筛选界线。摘要也有触发标识字段。若只收到这份摘要，即使 `storedReports` 大于 0，也没有拿到相应位置明细；未抓到摘要不等于报告数为零。 |

例如，已核实本笔明细请求从 09:00 到 10:00。历史事件内的 `locTimestamp=09:00` 不满足这里的“更新于 09:00”，09:30 满足两个时间条件；10:00 不满足“早于 10:00”。09:30 在时间范围内，并不证明它符合其他筛选项或请求里的数量已补满。响应里的摘要即使列出 09:00 和 10:00，也不改变该请求的时间边界。[表 7.1.6.2.48-1、.52-1、.53-1 和 .54-1，印刷页 56–58](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)；[A.2 的 `RequestedLocationHistory`，页 86](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)。

**本版的历史明细结构有差异。** 表 7.1.6.2.52-1 列 `LocationHistoryData` 内的 `locationHistoryEvent` 数组，标记 M、`1..N`；A.2 将 `LocationHistoryData` 本身定义为 `LocationHistoryEvent` 数组，未列 `minItems`。事件的 `locationData` 在印刷表里类型是 `LocationInfo`，基数印为 `1..N`；A.2 引用单个 `LocationInfo` 对象。印刷摘要表的 `storedReports`、最早和最新时间标 M、`1`，`triggerId` 标 M、`0..N`；A.2 摘要模型未列 `required`。这些写法分别核对。A.1 的附录优先限 API 信息元素及方法的编码，不把两种外形定义为别名，也不以缺字段推零值、空表合规或报告不存在。[印刷页 57–58、73、87–88](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=88)。

收到明细只能确认这笔实际报告里有哪些条目。它不证明缓冲已清除、取到所有历史或有新的测量，也不证明独立发布 POST 或给上游查询 LMC 的位置通知已发、已收。没有完整事件正文，不能用摘要倒推经纬度或补造时间点。按 TS 23.280 V19.9.0 查[单系统历史补报与取消](history-recovery.md)时，另读 Stage 2，不为它补入这套 HTTP 报文规则。

## 索要坐标时，`coordinate: false` 是不要坐标吗？

**按本版不是。** 在 LMS 向已注册目标 LMC 索要报告的 `LocationRequest` 里，`requestedLocationInfo` 可省略。若带它，`coordinate` 这类选择字段按**键是否出现**表达要报告的项目。印刷表写 `Coordinate`；A.2 写 `coordinate`，类型为可空布尔，描述仍以出现为准。实际请求里带 `coordinate: false` 或 `coordinate: null`，不能用来表示不索要坐标。没带这个键，只说明该项没有通过这一个键提出，不等于禁止报告提供坐标，也不替任何位置传播许可作决定。`minimumIntervalLength` 是整数秒的间隔要求，不是这种出现即选的字段。[§6.2.2.7.2，印刷页 21](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=22)；[表 7.1.6.2.33-1、.47-1，页 50、55；A.2，页 85–86](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=51)。

| 实际看到什么 | 能确认什么 |
| --- | --- |
| LMS 实收同一目标 LMC 对这笔请求的匹配 200，报告含可读的 `locationData.currentCoordinate` 及地理坐标数据 | 可以确认这笔报告提供了坐标。看这份报告的 `locTimestamp` 判断测量时间，不拿 200 到达时刻当测量时间。还不能据此断定刚测、必为 GPS 或达到指定精度。 |
| 完整、匹配的报告正文只有 `ecgi`、`ncgi` 等小区信息，没有坐标 | 一般报告的位置数据不只一种；这份正文可以报告小区，但不能当作已经返回所请求的坐标。不从缺坐标推断未授权、GPS 关闭、取得失败或固定回退。历史条目里的坐标与该次报告的当前位置也要分开。 |
| 只见请求里有选择字段、目标端出站、孤立状态码或不完整的报告正文 | 不能确认 LMS 拿到坐标。按印刷表，204 只确认请求收件；即使实际收到 200 也要看这笔对应正文。未抓到坐标字段不等于线上漏发。 |

**一旦报告给出 `currentCoordinate`，就要再查其中的地理坐标数据。** §6.2.2.8.2 和表 7.1.6.2.51-1 写 `geographicalCoordinates`（复数），在该分支必带；A.2 的 `CurrentCoordinate` schema 写 `geographicalCoordinate`（单数），引用 TS 29.572 的坐标类型，未列 `required`。高度、水平和垂直精度、航向和速度都不因此必带。水平精度在正文与 A.2 写 `horizontalaccuracy`，印刷表写 `horizonalaccuracy`。A.1 的优先限信息元素和方法的编码。别把缺少 schema 关键字读成地理数据可以从本分支省掉，也不设字段别名、`null` 的缺省处理、经纬顺序、采集算法或兼容策略。本页不核 TS 29.572 的具体形状或精度要求。[§§6.2.2.7.2、6.2.2.8.2，印刷页 22–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[表 7.1.6.2.50-1、.51-1，页 57、A.1–A.2，页 73、87](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=58)。

查规范不用抓包。要判断某次通信，还要对上实际请求、响应方向和目标实例；另一笔发布 POST 的 201 或上游查询通知不能代替本次收到的报告。请求字段和报告类型都不说明谁获准索要或分享位置。

## 索要航向和速度后，到哪里确认拿到了？

**请求里的 `bearingAndSpeed` 是选择项，报告里的同名字段才装数据。** LMS 向已注册目标 LMC 发 `LocationReportRequest` 时，可在 `requestedLocationInfo` 里加这个键。表 7.1.6.2.33-1 按键的出现来指定报告所需内容；A.2 定义为可空布尔，说明仍以出现为准。因此 `false` 和 `null` 都没有省掉这个键，不能表示「不索要」。缺键只表示没有用它索要，不表示禁止报告提供。A.1 的优先规则限接口编码；这项语义不保证整笔请求被接纳或实际取得所要数据。[请求步骤，印刷页 21（PDF 第 22 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=22)；[选择项表，印刷页 50（PDF 第 51 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=51)；[A.1，印刷页 73（PDF 第 74 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)；[A.2 选择项，印刷页 84–85（PDF 第 85–86 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=85)。

| 要确认什么 | 看哪一份数据 |
| --- | --- |
| **这笔回调的报告有航向和速度吗？** | 先确认 LMS 实收同一目标 LMC 对该请求的匹配 **200 和可读的报告正文**。在 `locationData.currentCoordinate.bearingAndSpeed` 查实际值。它不是布尔量：表列为可选的速度与方位数据，A.2 引用 TS 29.572 的 `HorizontalWithVerticalVelocity`。若用了 `currentCoordinate`，只有运动资料不能代替其中必需的地理坐标数据。一般报告结构可选此项，不抹去请求按键选择的规则。 |
| **历史条目有，能算在这次的当前位置里吗？** | 不能。按 A.2，在 `locationHistoryData` 数组中找到那条历史事件，读**该条** `locationData.currentCoordinate.bearingAndSpeed` 和它自己的 `locTimestamp`。印刷表把事件数组列在 `locationHistoryEvent` 下。历史和顶层复用 `LocationInfo`，不共用时刻或字段值。顶层只有坐标时，历史有速度不等于顶层也有；顶层有值也不补给其他事件。只有历史摘要同样没有给出任何事件的实际数据。 |
| **查询端拿到了吗？** | 另查请求端 LMC 实收的匹配位置通知及目标条目。A.3 的 `mcUEResponseList` 中，目标条目的 `locationInfo` 也引用 `LocationInfo`；在该条的 `locationInfo.currentCoordinate.bearingAndSpeed` 核值。这个条目不带完整的 `MCUELocation`；模型没有报告顶层的 `locTimestamp` 或 `locationHistoryData`。要确认通知用的是哪次测量，还须独立关联，不能拿通知到达时刻当测量时刻。 |

一种常见误判：这笔回调报告的 `locTimestamp` 是 10:00，只有 09:30 的历史条目带运动值。读者可以认定**09:30 那条**报告了这项资料，不能把 09:30 的值当作 10:00 的，也不能认定 10:00 这次终端静止。若正文不完整，不能断定本次报告在线上缺这个字段。空值不是已取得运动数据；只有请求上的布尔量、印刷表无正文的 204 或另一笔发布的 201，也不证明本笔回调拿到了它。这里不推断少报的处理方式、所选字段是否适用于每条历史，也不补 TS 29.572 的单位、取值或内部编码，也不从类型名推定每个速度分量都必带。

[应答与普通报告 §§6.2.2.7.2、6.2.2.8.2，印刷页 22–23（PDF 第 23–24 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[204 响应表，印刷页 42（PDF 第 43 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=43)；[A.2 回调 200，印刷页 74–75（PDF 第 75–76 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=75)；[报告与历史表 .49-1 至 .54-1，印刷页 56–58（PDF 第 57–59 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)；[A.2 报告模型，印刷页 86–88（PDF 第 87–89 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)；[通知 A.3，印刷页 94–95（PDF 第 95–96 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=95)。[一次性查询](lms-one-time-location-request.md#怎么看这一份结果)另查通知和实际收件；不拿目标端的回调应答替代。
