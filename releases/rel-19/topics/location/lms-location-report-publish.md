# 向 LMS 上报位置：收到 201，能确认到哪一步？

**同一笔 `POST /lms-reporting/v1/locationreports` 的 LMS 201，确认位置报告已成功提交给 LMS。** 它不是注册成功，也不是查询者收到了位置。规范的获准分支要求 LMS 保存收到的位置、按需使用，再回 201。核实后端确实保存、转给某人或被应用使用，要分别看这些动作的证据。

这里读 **TS 24.283 V19.3.0，Release 19，Stage 3** 的 `LocationReportPublish`。LMC 是终端的位置管理客户端，LMS 是位置管理服务器。查规则不需要抓包；判一次实际上报，须区分 **发出报告、LMS 收到并鉴权、LMS 应答、LMC 收到应答**。匹配请求和应答时，先看发送方、目标资源和这笔事务，不能只认状态码。不要求同一份抓包也有注册的 201；这不表示未注册、过期或已注销就能通过发布鉴权。

## 何时发这一笔报告？

| 起因 | 在发布步骤前查什么 |
| --- | --- |
| 已配置的位置上报触发事件发生 | LMC 检查 `minimumReportInterval`。计时器正在运行则等到期；到期时**仍有任一上报触发条件为真**才按这条路径发送。不只看最初那个条件，也不把一次触发等同于已发送。本段未另写触发时计时器未运行的发送规则。 |
| LMC 实际收到 LMS 的 `LocationReportRequest` | 这是 LMS 发到目标端 LMC 注册时给的 `locationRequestUri` 的请求。收到才触发另发发布 POST；只见 LMS 发出不够。本段没有说这条路径也要等事件分支的计时器到期。 |

**计时从发报告算，不从收到 201 算。** LMC 发出 `LocationReportPublish` 时，按位置配置设定并启动最短上报间隔计时器。索要报告的独立回包，正文另有重置计时器；实际处理配置通知也有启动计时器的步骤。不能把这三处合成固定执行先后、优先级或重试规则。[§§6.2.2.7.2、6.2.2.8.1–.2，印刷页 21–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=22)。

**不要混应答。** 正文及 A.2 把目标 LMC 对 `LocationReportRequest` 的应答写为 200 + 报告，表 7.1.5.3.3.1-2 则写 204、无正文。无论看的是哪一处写法，那个响应属于 **LMS→LMC 的索要报告请求**，不等于 **LMC→LMS 的发布 POST** 已被接受。看到其中一路不证明另一笔也实际发生或承载同一位置样本。[表，印刷页 42](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=43)；[A.2，印刷页 74–75](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=75)。

### 配置了定期报告，就会按周期发位置吗？

**先认配置里的两个 `periodicReport`。** `TriggeringCriteria.periodicReport` 是可选的定期触发对象。实际查某次触发时，用同一 LMC 当时生效的配置：事件时终端紧急查 `emergencyTriggeringCriteria`，非紧急查 `triggeringCriteria`；不从后来报告的 `reportType` 倒推。例：非紧急的间隔放在 `triggeringCriteria.periodicReport.periodicReport`，单位是整数秒。同对象的 `triggerId` 是本项的唯一标识，不是周期。表 .23-1 把内层两项均列为 M、1，A.2 声明为整数和字符串标识，但对象未列 `required`，也未给该整数声明上下界或缺省值。0 不是这个字段定义的停报编码；未列限制也不等于服务必定接受 0、负数或缺项。收到 UPDATE 但没有这项，不能判原配置已被删除。[配置与触发表，印刷页 43–44（PDF 第 44–45 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=44)；[表 .23-1，印刷页 48（PDF 第 49 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=49)；[A.2 父对象，印刷页 78（PDF 第 79 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=79)、[周期对象，印刷页 82（PDF 第 83 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=83)、[标识，印刷页 85（PDF 第 86 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=86)；[A.1 编码界限，印刷页 73（PDF 第 74 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)。改配置另查[收件以及 FULL／UPDATE](lms-registration-configuration.md)（§6.2.2.5.2，印刷页 20）。

**索要历史时也可能看到同名对象。** A.2 的 `LocationRequest.requestLocationHistory.triggerCriteria.periodicReport` 属于历史报告条件，不是给终端启用当前定期触发的配置。历史对象自己的 `minimumIntervalLength` 也是请求参数，不是当前发布的计时器。[表 .47-1、.48-1，印刷页 55–56（PDF 第 56–57 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=56)；[A.2，印刷页 86（PDF 第 87 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)。

**报告周期不等于最短间隔。** 比如 `periodicReport.periodicReport=30` 表示定期触发的报告间隔为 30 秒，而 `RequestedLocationInfo.minimumIntervalLength=90` 表示位置报告之间最短 90 秒。两项配置不告诉你实际何时发：定期触发发生时，若 `minimumReportInterval` 正在运行，LMC 要等它到期；届时仍有**任一**上报触发条件为真才按这条路径发送，不必仍是原先的定期触发。实际收配置时启动、发发布 POST 时按配置设定并启动、正文的索要报告回包处理中的重置，都指最短间隔计时器，不能当作定期周期的起点或重置规则。本段没有规定周期起点、相位、错过周期的补发或合并，也没另写触发时计时器未运行如何发送。LMC 实收 `LocationReportRequest` 后的发布另看同节，不用等待周期来证明。[表 .33-1，印刷页 50（PDF 第 51 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=51)；[§6.2.2.5.2，印刷页 20（PDF 第 21 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=21)；[§6.2.2.7.2 和 §6.2.2.8.1–.2，印刷页 22–23（PDF 第 23–24 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)。

**报告 ID 只能告诉你这份报告列了哪项。** 本次报告根层的 `MCUELocation.triggerId` 字符串数组与同一 LMC 当时生效的定期项 ID 对上，说明报告列了这项；不能据此确认定期触发的实际时刻、上报次数或它是唯一原因。正文将已经触发的 ID 列入数组；表 .49-1 把数组标为 O、1..N，不是每份报告都要带所有已配 ID。不能用 `reportId` 或测量时间 `locTimestamp` 补周期时钟。实际发送看这笔 LMC→LMS 的发布 POST，接受看匹配的 LMS 201。[§6.2.2.8.2，印刷页 22–23（PDF 第 23–24 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[表 .49-1，印刷页 56（PDF 第 57 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)；[A.2，印刷页 86（PDF 第 87 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)。

### 独立行进距离触发，和自适应触发有什么不同？

**先看是哪个配置项。** 按同一 LMC 的终端在事件发生时的状态，紧急查 `emergencyTriggeringCriteria`，非紧急查 `triggeringCriteria`。该分支下的 `travelledDistance` 是可选**对象**，不是直接填米数的位置。对象中的 `travelledDistance` 才是所需行进距离，单位米、整数；同层的 `triggerId` 是此项的触发标识。比如非紧急分支用 `triggeringCriteria.travelledDistance.travelledDistance` 填米数，用 `triggeringCriteria.travelledDistance.triggerId` 填标识。判断现网时查当时实际生效的配置，不拿后来报告的 `reportType` 倒推当时的状态。[表 7.1.6.2.3-1、.4-1，印刷页 43–44（PDF 第 44–45 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=44)；[表 7.1.6.2.32-1，印刷页 50（PDF 第 51 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=51)。

**能填什么，和接收方会做什么，是两件事。** 印刷表把对象内的距离和 `triggerId` 都标为 M、1，标识要唯一并回到位置报告。A.2 声明距离为 `integer`、标识为 `TriggerId`（字符串），对象未列 `required`，距离未列 `minimum`、`maximum`、`default` 或 `nullable`。不因未列约束就认定 0、负数、空值或缺项一定是有效配置，也不替接收方定报错方式。A.1 的优先限于 API 信息元素及方法的编码，未写入 schema 的程序条件仍适用。[A.2，印刷页 78（PDF 第 79 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=79)、[印刷页 84–85（PDF 第 85–86 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=85)；[A.1，印刷页 73（PDF 第 74 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)。

**不能借自适应规则计算这项距离。** 表 .32-1 和 A.2 没说明从哪一点算、取累计路程还是两点间距离、恰好等于门槛算不算、何时重新计算或清零。比如独立门槛为 100 米，终端往返走了 120 米并回到出发点，不能单凭这段标准判该项已触发或未触发。以“上次发报告的位置”为参照、先超过再复查至少达到门槛，是下面 `adaptiveTrigger` 的规则，不是独立项的算法。A.2 在 `TravelledDistance` 描述末尾孤立的 “shall be sent.” 也未给出何时发送的规则。[表 .32-1，印刷页 50（PDF 第 51 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=51)；[表 .34-1，印刷页 52–53（PDF 第 53–54 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=53)；[A.2，印刷页 84（PDF 第 85 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=85)。

**达到门槛也不是已经上报。** `RequestedLocationInfo.minimumIntervalLength` 是两次位置报告之间的最短间隔（整数秒），不是本项的米数，也不是 `periodicReport` 定期触发配置的报告周期。比如最短间隔写 60 秒，不要求每 60 秒发一份，也不证明计时器正在运行。走已配置的事件发布分支时，若 `minimumReportInterval` 正在运行，等到期、且届时仍有**任一**上报触发条件为真才按该路径发；不必是最初那项，不补距离条件怎样延续到期。实际发送看这笔 LMC→LMS 的 POST，接受看匹配的 LMS 201。报告根层的 `MCUELocation.triggerId` 数组若与当时生效的距离项 ID 对上，只说明报告列举了它；报告的 `MCUELocation` 和 `LocationInfo` 未定义专门回传这项米数的字段。ID 不能代替实测距离、证明这是唯一触发或证明 LMS 接受。LMC 实收 LMS 的索要报告请求另走发布分支，不由本项判断。[表 .33-1，印刷页 50（PDF 第 51 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=51)；[表 .23-1，印刷页 48（PDF 第 49 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=49)；[A.2 的定期触发与最短间隔，印刷页 82、85（PDF 第 83、86 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=83)；[§6.2.2.8.1–.2，印刷页 22–23（PDF 第 23–24 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[表 .49-1、.50-1，印刷页 56–57（PDF 第 57–58 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)；[A.2，印刷页 86–87（PDF 第 87–88 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)。

### 走过距离门槛，就会发位置报告吗？

**先越过门槛，再按配置复查。** 这里限 TS 24.283 V19.3.0 的 `adaptiveTrigger`。它是所在状态的 `TriggeringCriteria` 中可选的时间和距离组合触发；不是单独的 `travelledDistance`、定期报告，也不是 LMS 临时索要一份位置。比较距离时，参照的是**上次发位置报告时所在的位置**，不是请求到达时的位置或轨迹累计里程。[表 7.1.6.2.3-1、.4-1、.32-1、.34-1，印刷页 43–44、50–53](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=53)。

| 参数 | 本触发怎样使用 |
| --- | --- |
| `minPeriod` | 两次位置报告之间的最短等待，不因移动距离改变。整数秒，不小于 0；省略时为 0。 |
| `minDistance` | 正整数米。初次检测到离上次发报告的位置**超过**该距离，才进入下面的复查。省略时按无穷大处理，不是 0。 |
| `persistencePeriod` | 从初次检测到越过距离起，等这一段时间再检查届时的位置。整数秒，不小于 0；省略时为 0。复查仍相距**至少** `minDistance` 才走距离分支。首次恰好等于门槛，与越过后在复查时恰好等于门槛，结果不同。 |
| `additionalTime` | 正整数秒，省略时为 1。若没有按距离发报告，时间分支从**上一次报告**算 `minPeriod + persistencePeriod + additionalTime`，不是从检测越界或复查失败开始算。 |

例如，某 LMC 在第 0 秒发过报告，参数依次为 5 秒、50 米、3 秒、2 秒。第 6 秒测得距参照位置 55 米，第 9 秒复查只剩 45 米，不满足距离分支。这时从上一次报告算的时间界线是第 10 秒；不是从第 6 秒再等 10 秒。如果第 9 秒复查恰为 50 米，则满足**复查**的距离门槛。例子只核这项触发条件，不承诺会在某一秒实际发包。`minPeriod` 仍是等待下限；本段未给距上次报告不足该下限的复查、其他事件竞态或首次无参考报告时的完整调度算法。[表 7.1.6.2.34-1，印刷页 52–53](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=53)。

`rrcInactiveMinPeriod`、`rrcInactiveMinDistance`、`rrcInactivePersistencePeriod` 和 `rrcInactiveadditionalTime` 是四个可选的对应参数，用于 **UE 在 `RRC_INACTIVE` 中接收 MBS 流量**的场景。只有 RRC 状态、只知有 MBS，或只知某处会话是组播，都不足以套这些参数。本段不替部分配置规定与通用值怎样混用。印刷表将 `triggerId` 标为必需，并说它返回在位置报告中；A.2 的 `AdaptiveTrigger` 未列 `required`，上述数值限制和缺省值写在说明里。不要把可选参数的缺省值当成默认启用整个触发，也不用 schema 未声明某个限制推导接收方一定会接受。[表 7.1.6.2.34-1，印刷页 52–53；A.1–A.2，印刷页 73、78–79](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=79)。

**触发条件和实际发送另看。** §6.2.2.8.1 的事件发布分支还要查 `minimumReportInterval`：若它正在运行，等到期并确认届时仍有上报触发为真。`adaptiveTrigger` 的 `minPeriod` 不替代这条检查；本版未给两个时间规则的竞态或合并公式。距离不足也不证明定时分支、其他事件或 LMS 索要报告都不会产生报告。查规范不需要抓包；现场是否发布或 LMS 是否接受，分别看实际这笔 POST 和匹配应答，不从配置、测量或触发 ID 单推。[§6.2.2.8.1–.2，印刷页 22–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)。

## 这份报告是谁发的，是什么时候测的？

- **发送者和实例是两回事。** LMC 经 TLS 向 LMS 发上报，带适用于其有效 MC service ID 的全部 Bearer 访问令牌。LMS 按 §7.1.9 所引 TS 24.482 确定认证发送者，再按 TS 33.180 做业务授权。`mclocClientId` 是报告所属的 LMC 实例标识，不是令牌、经过认证的发送者身份或已授权的证据；也不用设备标签、别名或一个网络断言头代替 UE 的 Bearer 要求。[§6.2.2.8.2，印刷页 22–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[§7.1.9，印刷页 60](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=61)。不在本文展开另一规范的完整身份链或网络实体权限。
- **测量时刻不是上传时刻。** 请求体是 `MCUELocation`。数据模型的 `locTimestamp` 是位置测量时间，不能拿 POST、201 或搜索结果的到达时间补它。`locationData` 不限于经纬度：正文要求按配置至少有一项适用位置数据，如服务小区；选择坐标时才有坐标项的相应条件。报告是否处于紧急状态、测量何时发生和设备实例要分别读。
- **先分触发，再读 ID。** 建立与 LMS 索要报告的关联时，若那笔实际收到的请求带 `requestId`，请求触发的报告应把它写入 `reportId`。请求表把 `requestId` 列为可选，不能在它未提供时编一个值；也不能因只有一个 `reportId` 就断言重传、去重、同一设备或查询者已经收到。按事件发布的报告不因此需要有一笔 LMS 请求。

[报告/请求数据类型 §§7.1.6.2.47、.49–.51，印刷页 55–57](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=56)；[A.2 模型，印刷页 85–87](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=86)。正文写 `reportID`、`requestID`、`locTimstamp`，表和 A.2 分别写 `reportId`、`requestId`、`locTimestamp`。正文列入上报触发 ID 数组，表 7.1.6.2.49-1 把 `triggerId` 标为可选；也不能因 A.2 未写 `required` 就把正文中的实例、测量时刻或至少一项位置内容都看成可以省略。保留这些写法的来源，不把拼法当别名。

### 报告列了某个小区，能认定触发了进入或退出吗？

**不能只凭小区 ID。** 看同一 LMC 这笔发布的 `MCUELocation.locationData`：`ecgi`、`ncgi` 分别报告测量时的 E‑UTRAN、NR 服务小区；`neighbouringEcgi`、`neighbouringNcgi` 列出终端检测到的相应邻区。某 ID 只在邻区列表里，不能确认它当时是服务小区。即便报告把它列为服务小区，单次测量也没给出先前所在小区或进出方向。看报告的 `locTimestamp`，不拿 POST 到达时间、历史条目或同一用户另一台 LMC 的报告代替。[§6.2.2.8.2，印刷页 22–23；表 7.1.6.2.49-1、.50-1，页 56–57](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)。

**按变化当时的终端状态查规则。** 核对同一 LMC 当时生效的配置。小区发生变化时，对应的 MC UE（终端）处于紧急状态则查 `emergencyTriggeringCriteria`，非紧急则查 `triggeringCriteria`；`cellChange` 是可选项。之后报告的 `reportType` 描述发送报告时的状态，不能用它倒推变化时的终端状态。[§6.2.2.8.2 第 2 项，印刷页 22](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[表 7.1.6.2.49-1，页 56](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)。

| 适用配置 | 要核实的事件 |
| --- | --- |
| 有 `anyCellChange` 子项 | 实际小区发生变化即符合这项触发，不用命中指定小区名单。子项用对象表示，不是布尔开关。 |
| 有 `enterSpecificCell` | 终端实际**进入**该项列出的小区。 |
| 有 `exitSpecificCell` | 终端实际**退出**该项列出的小区。 |

只有进入 NR 小区 B 的规则时，假设同一 LMC 从 A 实际进入 B，符合该进入项；反向 B→A 不符合。邻区列表出现 B、或只有一笔 `ncgi=B` 的报告，都不足以确认这个变化。具体条目按 `eutranCells[].eutranCell`（ECGI）或 `nrCells[].nrCell`（NCGI）核对类型和 ID。不能用 NR ID 去命中 E‑UTRAN 列表，也不能把小区规则当成地理围栏或跨无线制式规则。[表 7.1.6.2.3-1 至 .9-1，印刷页 43–45；A.2，页 79–80](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=45)。

**用 `triggerId` 追溯报告列了哪一项。** 印刷表把 ID 放在 `anyCellChange` 对象里，或指定名单中各小区条目上；同一个小区的进入项和退出项要分别查。实际报告的 ID 与同一 LMC 当时有效的子项对上，可以辨认报告所列的触发；这个 ID 不能代替进出记录、计时器到期后的条件检查或同一 POST 的 LMS 应答。[§§6.2.2.5.2、6.2.2.8，印刷页 20、22–23；表 7.1.6.2.6-1、.8-1、.9-1、.49-1，页 44–45、56；A.2，页 79–80、86](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)。

**印刷表与 A.2 分开读。** 对进入或退出项，表 7.1.6.2.7-1 要求至少出现一个名单，并把列出的名单标为 `1..N`。A.2 的 `anyOf` 只查两键至少一键存在，不排斥同时存在，也没给名单 `minItems`。印刷表将小区项的 ID 和所指小区列为必须；A.2 在这些对象中未列 `required`。印刷表的 E‑UTRAN 名单和条目说明提到 NR；按其类型列，`eutranCells` 的每个 `EutranCell` 条目用 `Ecgi`，`NrCell` 条目用 `Ncgi`。A.2 也分别定义这两类条目。不要用空名单或省略 ID 当作有效触发，也不由 schema 单独推服务端一定接受、拒绝或怎样检测切换。邻区数组若给出，表 .50-1 也印为 `1..N`，A.2 未列 `minItems`；空数组不提供邻区数据。A.1 的优先限 API 信息元素和方法的编码，不取消未写入 schema 的程序条件。[印刷页 44–45、57；A.1–A.2，页 73、79–80、87](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=80)。

### PLMN 或跟踪区变化：先问进入还是退出

**进入看新去处，退出看实际离开的地方。** 查同一 LMC 的 MC UE 在变化**当时**所处状态及生效配置：紧急用 `emergencyTriggeringCriteria`，非紧急用 `triggeringCriteria`。报告后来标的 `reportType` 不倒推当时状态。[配置模型，印刷页 43–44（PDF 第 44–45 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=44)。

| 变化对象 | 任意变化 | 指定进入 | 指定退出 |
| --- | --- | --- | --- |
| `plmnChange` | 生效的 `anyPlmnChange` 对象对应任意实际 PLMN 变化 | `enterSpecificPlmnArea` 比对实际进入的 PLMN | `exitSpecificPlmnArea` 比对实际离开的 PLMN |
| `trackingAreaChange` | 生效的 `anyTrackingAreaChange` 对象对应任意实际跟踪区变化 | `enterSpecificTrackingArea` 比对实际进入的跟踪区 | `exitSpecificTrackingArea` 比对实际离开的跟踪区 |

例如，只配“进入 PLMN B”，A→B 命中，B→A 不命中；只配“退出 B”则相反。跟踪区也按各自方向判断。任意变化项用对象，不是布尔开关或当前位置值。只有当前 PLMN 或 TAC，或只见同一 UE 换了小区、RAT，不能补实际进出。PLMN 变化也不自动等于跟踪区变化；跨 PLMN 看到同一个 TAC 值，单凭它不能判跟踪区必同或必异。本段不定义比较算法或任何组合的优先级。[表 7.1.6.2.24–.31，印刷页 48–50（PDF 第 49–51 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=49)。

**配置层的条目不是报告字段。** 指定 PLMN 查 `plmnIds[].plmn`（`PlmnId`）；指定跟踪区查 `trackingAreas[].trackingArea`（`Tac`）。后者不是本地定义的 TAI（PLMN 和 TAC 的复合标识）对象，不补外部 TS 29.571 的格式。印刷表的指定列表为 M、`1..N`；每条的标识和 `triggerId` 各 M、1，任意变化对象自身的 `triggerId` 也 M、1。表和 A.2 的 ID 说明写唯一、返回在报告中。A.2 没给这些对象列 `required`，两个列表也没列 `minItems`。不因此把空名单、`null` 或缺 ID 当有效配置，不能猜接收方会怎样处理。A.1 的附录优先限 API 信息元素和方法的编码；没编码进去的程序条件仍适用。[复用类型及印刷表，印刷页 42、48–50（PDF 第 43、49–51 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=43)；[A.1，印刷页 73（PDF 第 74 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)；[A.2 PLMN 模型，印刷页 82–83（PDF 第 83–84 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=83)；[A.2 跟踪区及 ID，印刷页 84–85（PDF 第 85–86 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=85)。

**报告里的 `triggerId` 只能用于归因。** 看对应 LMC 当时生效的子对象或名单条目，能辨认该报告列出的规则，不能代替实际变化，也不证明唯一原因。生成报告正文列已触发的 ID，表 .49-1 将数组列为可选，A.2 未列 `required`。该版 `LocationInfo` 没单列 `plmn` 或 `trackingArea`；这不排除外部小区类型内部携带 PLMN，也不能由当前位置单样本重建进出。若事件发生时 `minimumReportInterval` 正在运行，要等到期且届时仍有任一上报触发为真；本段不补特定边界条件怎样持续、几项命中要发几份。实际上报看对应的 LMC 发布 POST，接受看匹配 LMS 201。[发布，印刷页 22–23（PDF 第 23–24 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[报告数据表，印刷页 56–57（PDF 第 57–58 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)；[A.2 发布报告，印刷页 86–87（PDF 第 87–88 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)。

### 4G、5G 切换时，什么会触发上报？报告能写哪个方向？

**配置管“要不要因切换而报”，报告管“这次切换是什么方向”。** 看同一 LMC 在变化发生时生效的配置：MC UE 紧急时查 `emergencyTriggeringCriteria`，非紧急时查 `triggeringCriteria`。其中 `ratTypeChange` 配有 `anyRatTypeChange`，任意实际跨无线接入技术（RAT）的变化都符合这项触发。只在 5G 内换小区，或只在 LTE 内从组播改成单播，不算跨 RAT。只见当前是 5G，或后来报告才标成紧急，也不足以判定这次变化。[状态和触发项，印刷页 43–44](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=44)；[表 7.1.6.2.37-1、.38-1，印刷页 53](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=54)。

报告里可选的 `MCUELocation.interRatType` 描述方向，不是配置开关。本版只为以下四种方向命名；先看从哪里来，再看去了哪里。

| 从 | 到 | `interRatType` |
| --- | --- | --- |
| 5G MBS | LTE MBMS | `5G_MBS_TO_LTE_MBMS` |
| 5G MBS | LTE 单播 | `5G_MBS_TO_LTE_UNICAST` |
| LTE MBMS | 5G MBS | `LTE_MBMS_TO_5G_MBS` |
| LTE MBMS | 5G 单播 | `LTE_MBMS_TO_5G_UNICAST` |

例如，从 **LTE 单播到 5G MBS** 确实跨了 RAT，命中已生效的上述触发，但本版没有对应的命名值。不能反用表中第二行，也不必为上报位置造一个方向值；`interRatType` 可以省略，不能代替报告里的 `locationData`。A.2 在这四值之外保留字符串分支，明说只用于未来扩展，不能把任意字符串解释成本版定义的方向。[报告正文 §6.2.2.8.2，印刷页 22–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=24)；[报告表 .49-1，印刷页 56](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)；[方向表 7.1.6.3.5-1，印刷页 59](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=60)；[A.2 枚举，印刷页 88](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=89)。

要问**报告把这次上报归给哪条规则**，看报告的 `triggerId` 与这台 LMC 当时的生效配置。方向值本身不证明是这条规则，更不证明只有这一个原因；要核实无线侧实际切换，另看同一终端切换前后。`AnyRatTypeChange` 的印刷表要求唯一 ID 并在报告中返回；A.2 声明这个属性但没列 `required`。发布正文按已触发的规则列 ID，报告表把 ID 数组标为可选。A.1 的附录优先限编码。命中触发时，若最短上报间隔计时器在运行，要等到期，而且届时至少一项上报触发仍为真才按这条路径发。要确认**已经发出**，看 LMC 的实际发布 POST；要确认 LMS 接受，再看匹配的 201。[事件与发布程序，印刷页 22–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[A.1，印刷页 73](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)；[A.2 触发对象，印刷页 78、83](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=84)及[报告对象，印刷页 86](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)。

### 报告里写了广播区域，能判定终端进了哪个区吗？

**单份报告只说明它报了哪个区。** 看同一 LMC 的这份 `MCUELocation`，时刻用 `locTimestamp`。这三种区域不是服务小区 `ecgi`／`ncgi`，也不是检测到的邻区。区域标识不证明终端进入或退出，更不证明它收到了该区的媒体。

| 位置报告的字段 | 读到什么 | 配置里查哪类变化 |
| --- | --- | --- |
| `locationData.mbmsSaiId` | MBMS 服务区。印刷表 .50-1 写 `string`；A.2 写整数，范围 0–65535。 | `mbmsSaChange` |
| `locationData.mbsfnArea` | MBSFN 区，A.2 引用 TS 29.571 的 `MbsfnArea`。不能拿配置条目里的整数 0–255 判断报告的 `MbsfnArea` 结构。 | `mbsfnAreaChange` |
| `locationData.nr5GMbsfsaArea` | 5G MBS 频率选择区，A.2 引用 TS 29.571 的 `MbsFsaId`。 | `nr5GMbsfsaAreaChange` |

例如，A.2 的报告 `mbmsSaiId: 42` 和 `mbmsSaiId: "42"` 不是同一种编码。保留表与附录的写法，不规定转换、兼收或错误码。A.1 的附录优先限 API 编码，没有抹掉正文里的程序条件。[生成报告，印刷页 22–23（PDF 第 23–24 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[复用类型，印刷页 42（PDF 第 43 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=43)；[报告数据表 .49-1、.50-1，印刷页 56–57（PDF 第 57–58 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=57)；[A.1 的编码优先，印刷页 73（PDF 第 74 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)；[A.2 的报告模型，印刷页 86–87（PDF 第 87–88 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=87)。

LMS 向目标索要报告时另有 `requestedLocationInfo`。其中 `mbmsSaiId`、`mbsfnArea`、`nr5GmbsfsaArea` 是 A.2 的可空布尔选择项，按键出现，不是区域值。注意请求第三个键是小写 `m`，报告的 `nr5GMbsfsaArea` 是大写 `M`。不能把请求值抄入报告；见[索要报告与回调](lms-location-report-request.md)。[选择项表 .33-1，印刷页 50（PDF 第 51 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=51)；[A.2 选择项，印刷页 85（PDF 第 86 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=86)。

**要判断哪条进出规则命中，看实际变化和变化时生效的配置。** 同一 LMC 对应的 MC UE 当时在紧急状态，查 `emergencyTriggeringCriteria`；非紧急则查 `triggeringCriteria`。三类变化各有任意、指定进入、指定退出：任意变化项是配置对象，不是请求里的布尔选择；启用时查本类是否实际变化。指定进入看新进哪一区，指定退出看从哪一区离开。比如只配「进入 MBMS 服务区 B」，A→B 命中，而 B→A 不命中该项。只见 B 的样本不知道先前在哪；稍后发报告时的 `reportType` 也不能倒推变化时处于哪种状态。[状态配置，印刷页 43–44（PDF 第 44–45 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=44)；[触发模型 .11–.22，印刷页 46–48（PDF 第 47–49 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=47)。

A.2 指定列表各自的标识为 `mbmsSaIdentities[].mbmsSaIdentity`、`mbsfnAreas[].mbsfnArea` 和 `nr5GMbsFsaIdentities[].mbsfnAreaIdentity`。最后一个在印刷表 .22-1 写 `mbsfsaAreaIdentity`，查的是 5G 的 `MbsFsaId`，不因 A.2 的拼法变成 MBSFN 区。任意 MBSFN 变化的属性写 `anyMbfsnAreaChange`，保留原字面。任意分支和指定列表条目的 `triggerId` 在印刷表里都是必带且唯一；列表也要求至少有一项。A.2 不为这些对象列 `required`，不为这些列表列 `minItems`。这不把空列表或缺 ID 当成满足程序条件。[A.2 触发模型，印刷页 78、80–82（PDF 第 79、81–83 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=81)。

报告的 `triggerId` 可以同生效规则对照，不能替代见到实际变化。若 `minimumReportInterval` 正在运行，等到期且仍有任一上报触发为真，才按事件分支发。是否已发看实际发布 POST；是否已交 LMS 看这一笔的匹配 201。报告到达不等于终端收到广播媒体。[事件与发布，印刷页 22–23（PDF 第 23–24 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)。

如果是在选 [自适应触发的 RRC_INACTIVE 变体](#走过距离门槛就会发位置报告吗)，同一 UE 必须同时处于 `RRC_INACTIVE` 并实际接收 MBS 流量。区域标识不能替代收流证据。两项都能证实，也只说明满足这里的状态和流量前件；还是要查适用的配置和门槛，不能说报告已发。[表 7.1.6.2.34-1，印刷页 52–53（PDF 第 53–54 页）](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=53)。

## 读这一笔发布的 201 或 401

| 实际记录 | 能判断什么 |
| --- | --- |
| 只见 LMC 出站 POST，或代理、别笔请求报了 201 | 不是该 LMS 已接收或接受此报告的证据。 |
| LMS 对匹配发布 POST 应答 **201**，或 LMC 实收该应答 | 这是提交成功的协议结果。表与 A.2 的 201 正文类型都是 `MCUELocation`，表说明返回提交的位置数据；不是新采样、字节原样回显的保证，也不确认已通知另一端。LMS 已发与 LMC 实收分开。 |
| LMS 对这笔发布回 **401** | 该笔未按成功提交返回。若命中正文未获业务授权的分支，LMS 拒绝提交，不走获准分支的存储和使用步骤。只看该状态码不说明是哪份令牌、身份或授权条件没通过。 |

[§6.2.2.8.2，印刷页 23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=24)；[§§7.1.1、7.1.3.5，印刷页 32、39–40](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=40)；[A.2 `submitLocationReport`，印刷页 76–77](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=77)。

**`Location` 也要按这笔应答看。** 报告资源的创建入口是 `{apiRoot}/lms-reporting/v1/locationreports`。表 7.1.3.5.3.1-5 将报告 201 的 `Location` 列为必带，所印新资源 URI 却用 `{apiRoot}/lms-location-report/<apiVersion>/locationreports/{locationreportId}`；A.2 这个 POST 的 201 定义带正文、未列该响应头。A.1 的优先范围是 API 信息元素和方法的编码，正文未写入 OpenAPI 的程序和条件仍适用。检查所收到的头，不自行拼接、改前缀、假定回退或据此 GET；A.2 未列不等于禁止发头，也不把印刷表要求抹掉。§7.1.10 的 307/308 中也有 Location，但指向同一 LMS 的另一服务实例，不是创建成功。[表，印刷页 40](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=41)；[A.1–A.2，印刷页 73、76–77](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)。

想查另一端拿到位置，看[一次性查询与通知](lms-one-time-location-request.md)或[位置订阅](lms-subscription-notification.md)。想查配置怎么到 LMC，看[注册与配置](lms-registration-configuration.md)。[单系统位置采集](report-acquisition.md)描述 Stage 2 业务触发，不替这个接口补计时器、鉴权、状态码、重放或历史保留规则。
