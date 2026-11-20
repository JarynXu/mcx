# MCPTT 位置配置、位置请求和报告：参与功能与终端各做什么？

在 3GPP TS 24.379 V16.14.0 的这条 Stage 3 流程中，参与 MCPTT 功能（PF）可以给终端下发规则，也可以单独要一份位置报告。**下发规则和索要报告都用 SIP MESSAGE，由消息体里的 `Configuration` 或 `Request` 区分；终端上报时发送的是带 `Report` 的 SIP 请求。** 这是 PF 与 MCPTT 终端间的信令，不是向 LMS 订阅另一个用户的位置。[§13.1–13.2.4，印刷页 460–461](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=461)；[§13.3.1，印刷页 462](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)。

## 什么时机下发配置？怎样认出是一份配置还是一次请求？

PF 需要终端位置时，§13.1 把配置放在**MCPTT 业务授权成功**之后。§13.2.2 允许 PF 发配置，并未规定每次 IMS REGISTER 成功都下发配置，也没规定授权成功后多少秒发出。若 PF 确实需要终端报告位置，§13.2.3 要求另按位置请求程序生成并发送 SIP MESSAGE。两种 MESSAGE 各自有以下内容：[§13.1、§13.2.2–3，印刷页 460–461](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=461)。

- Request-URI 是与 MCPTT 客户端身份对应的 URI。`Accept-Contact` 使用 `g.3gpp.icsi-ref`，值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`，带 `require` 和 `explicit`。同一个服务值也写入 `P-Asserted-Service`。
- `application/vnd.3gpp.mcptt-info+xml` 的 `<mcptt-request-uri>` 元素写目标用户的 MCPTT ID。另一个 MIME body 是 `application/vnd.3gpp.mcptt-location-info+xml`，在 `<location-info>` 根元素中分别放 `<Configuration>` 或 `<Request>`。
- **配置**在规定了 `TriggerId` 的触发条件子元素填写该属性，并把 PF 自己的公共服务标识（PSI）写进 `P-Asserted-Identity`（PAI）。位置请求条款没有列这项 PAI 要求，不能反过来解读为请求必须不带 PAI，也不从配置条款给它加上必带条件。

## 终端什么时候等 minimumReportInterval，什么时候直接走请求分支？

终端的两条接收程序先看**本机实际收到的 SIP MESSAGE**：`Accept-Contact` 是否含 MCPTT 的 `g.3gpp.icsi-ref` 值，`Content-Type` 是否为 `application/vnd.3gpp.mcptt-location-info+xml`，位置体的 `<location-info>` 内是否有对应元素。发端的字段要求不自动变成接收分支未列的检查项。[§13.3.2–3，印刷页 462–463](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)。

| 终端本机真正遇到的事件 | 终端动作 |
| --- | --- |
| 收到匹配的 `Configuration` | 保存配置、设置触发条件、启动 `minimumReportInterval`。附录列有可选的 `LocationConfigurationReceived` 触发条件；收到配置本身不表示每次立即上报。 |
| 已配置的事件触发，且 `minimumReportInterval` 正在运行 | 等计时器到期。到期时仍有报告触发条件为真，才按报告程序发送。不能把一度触发、到期时已不成立的条件当成到期时仍成立。 |
| 收到匹配的显式 `Request` | 按报告程序发送报告，并重置 `minimumReportInterval`。本分支未列“先等正在运行的计时器到期”，也未承诺端到端的秒数。 |

§13.3.4.1 没有另写事件触发但计时器未运行的处理，也未规定事件触发与显式请求同时到达时的先后。不要据此补定时器分支或调度策略。[§13.3.2–13.3.4.1，印刷页 462–463](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)；[附录 F.3.3，印刷页 566、568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=567)。

## Report 发到哪里？怎样证明它是对这次请求的报告？

若终端正因别的理由需要发一个 SIP 请求，就把含 `<Report>` 的位置 MIME body 加进该请求；MBMS 监听报告只是原文举例。若没有另一个要发的请求，终端构造独立 SIP MESSAGE：Request-URI 取自此前**收到的位置配置 MESSAGE** 中 PAI 的 SIP URI，不是取自这次位置请求；Content-Type 是上述位置 MIME，`Accept-Contact` 用不同的 `g.3gpp.mcptt` 特征标签，也带 `require` 和 `explicit`。独立 MESSAGE 的目的地规则需要这份配置里的 URI，条款没有为缺少该 URI 指定后备目的地。两种发送分支都把 `minimumReportInterval` 设为规定时长并启动，重置全部触发条件。在独立 MESSAGE 分支，正文把实际发送列在这些动作之后；不把这一步骤排序套到显式请求程序另列的重置动作上。[§13.3.3–13.3.4.2，印刷页 462–464](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=463)。

**只有由显式位置请求触发的报告才按该请求回填关联值。** 正文 §13.3.4.2 写 `RequestID` → `ReportID`；附录 F.3.2 的 XSD 把请求属性写作必需的 `RequestId`，把报告属性写作可选的 `ReportID`；F.3.3 的描述写 `RequestId` → `ReportId`。XSD 中的可选性并不抹掉显式请求分支的回填要求。对实际触发的事件，正文把来源属性写成 `Trigger-Id`，报告子元素写成 `TriggerId`；附录用 `TriggerId` 表述其关联属性。报告按已触发条件填对应内容，不以一个触发标识替代这次请求的回填值。这里保留定版中的拼写差异，不定义等价别名或可直接发送的 XML。[§13.3.4.2，印刷页 463–464](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=464)；[附录 F.3.2，印刷页 559](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=560)；[附录 F.3.3，印刷页 568](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=569)。

PF 实际收到 Content-Type 匹配、位置体的 `<location-info>` 内有 `<Report>` 的 SIP 请求，须按**收到的 MCPTT ID** 核准这份报告，用户获准才按需使用；区域进出另有流程，不在本主题展开。这里不指定 MCPTT ID 必在某一字段，也没有给出专用的 SIP 成功或拒绝码。终端发出报告、见到任意 SIP 2xx，或能用回填值配对，都不能单独证明 PF 已核准并使用位置。看到 `Report` 元素也不能直接断定含坐标。[§13.2.4，印刷页 461](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=462)。

若问的是 [LMS 如何在 Stage 2 配置事件上报](event-reporting-configuration.md)或[其他用户怎样订阅位置](user-subscription.md)，按 LMS 的角色读相应主题。若在排查 IMS 接入之后哪项 MC 业务获授权，见[共享 SIP 注册与业务授权](../identity/shared-sip-registration.md)。此处的 PSI 是位置配置 SIP MESSAGE 的 `P-Asserted-Identity` 所带的参与 MCPTT 功能标识，不是 LMS 有 SIP PSI 或 SIP SUBSCRIBE 的证据。
