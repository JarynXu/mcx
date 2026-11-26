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

## 这份报告是谁发的，是什么时候测的？

- **发送者和实例是两回事。** LMC 经 TLS 向 LMS 发上报，带适用于其有效 MC service ID 的全部 Bearer 访问令牌。LMS 按 §7.1.9 所引 TS 24.482 确定认证发送者，再按 TS 33.180 做业务授权。`mclocClientId` 是报告所属的 LMC 实例标识，不是令牌、经过认证的发送者身份或已授权的证据；也不用设备标签、别名或一个网络断言头代替 UE 的 Bearer 要求。[§6.2.2.8.2，印刷页 22–23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=23)；[§7.1.9，印刷页 60](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=61)。不在本文展开另一规范的完整身份链或网络实体权限。
- **测量时刻不是上传时刻。** 请求体是 `MCUELocation`。数据模型的 `locTimestamp` 是位置测量时间，不能拿 POST、201 或搜索结果的到达时间补它。`locationData` 不限于经纬度：正文要求按配置至少有一项适用位置数据，如服务小区；选择坐标时才有坐标项的相应条件。报告是否处于紧急状态、测量何时发生和设备实例要分别读。
- **先分触发，再读 ID。** 建立与 LMS 索要报告的关联时，若那笔实际收到的请求带 `requestId`，请求触发的报告应把它写入 `reportId`。请求表把 `requestId` 列为可选，不能在它未提供时编一个值；也不能因只有一个 `reportId` 就断言重传、去重、同一设备或查询者已经收到。按事件发布的报告不因此需要有一笔 LMS 请求。

[报告/请求数据类型 §§7.1.6.2.47、.49–.51，印刷页 55–57](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=56)；[A.2 模型，印刷页 85–87](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=86)。正文写 `reportID`、`requestID`、`locTimstamp`，表和 A.2 分别写 `reportId`、`requestId`、`locTimestamp`。正文列入上报触发 ID 数组，表 7.1.6.2.49-1 把 `triggerId` 标为可选；也不能因 A.2 未写 `required` 就把正文中的实例、测量时刻或至少一项位置内容都看成可以省略。保留这些写法的来源，不把拼法当别名。

## 读这一笔发布的 201 或 401

| 实际记录 | 能判断什么 |
| --- | --- |
| 只见 LMC 出站 POST，或代理、别笔请求报了 201 | 不是该 LMS 已接收或接受此报告的证据。 |
| LMS 对匹配发布 POST 应答 **201**，或 LMC 实收该应答 | 这是提交成功的协议结果。表与 A.2 的 201 正文类型都是 `MCUELocation`，表说明返回提交的位置数据；不是新采样、字节原样回显的保证，也不确认已通知另一端。LMS 已发与 LMC 实收分开。 |
| LMS 对这笔发布回 **401** | 该笔未按成功提交返回。若命中正文未获业务授权的分支，LMS 拒绝提交，不走获准分支的存储和使用步骤。只看该状态码不说明是哪份令牌、身份或授权条件没通过。 |

[§6.2.2.8.2，印刷页 23](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=24)；[§§7.1.1、7.1.3.5，印刷页 32、39–40](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=40)；[A.2 `submitLocationReport`，印刷页 76–77](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=77)。

**`Location` 也要按这笔应答看。** 报告资源的创建入口是 `{apiRoot}/lms-reporting/v1/locationreports`。表 7.1.3.5.3.1-5 将报告 201 的 `Location` 列为必带，所印新资源 URI 却用 `{apiRoot}/lms-location-report/<apiVersion>/locationreports/{locationreportId}`；A.2 这个 POST 的 201 定义带正文、未列该响应头。A.1 的优先范围是 API 信息元素和方法的编码，正文未写入 OpenAPI 的程序和条件仍适用。检查所收到的头，不自行拼接、改前缀、假定回退或据此 GET；A.2 未列不等于禁止发头，也不把印刷表要求抹掉。§7.1.10 的 307/308 中也有 Location，但指向同一 LMS 的另一服务实例，不是创建成功。[表，印刷页 40](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=41)；[A.1–A.2，印刷页 73、76–77](https://www.etsi.org/deliver/etsi_ts/124200_124299/124283/19.03.00_60/ts_124283v190300p.pdf#page=74)。

想查另一端拿到位置，看[一次性查询与通知](lms-one-time-location-request.md)或[位置订阅](lms-subscription-notification.md)。想查配置怎么到 LMC，看[注册与配置](lms-registration-configuration.md)。[单系统位置采集](report-acquisition.md)描述 Stage 2 业务触发，不替这个接口补计时器、鉴权、状态码、重放或历史保留规则。
