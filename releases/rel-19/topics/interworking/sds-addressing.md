# 互通SDS：地址映射与代理回执

TS23.283 V19.5.0，Release19，Stage2。

## MC用户与单个LMR用户之间的SDS；使用信令控制面或媒体面

发往LMR用户时，目标是分配给该LMR用户的MCData ID；LMR用户发起时源地址使用其分配的MCData ID。IWF以对等MCData服务器角色参与，基础发送过程仍依赖TS23.282。 [§10.8.6–7](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## IWF-2 单人请求：地址、两种标识和负载怎样读？

**同一张表管两个方向。** 表 10.8.2.2‑1 适用于 MCData server→IWF 和 IWF→MCData server 的 standalone 请求。两个 MCData ID 都必选（M），一个是**发送数据的用户**，另一个是**目标用户**；不随网元发送方向互换。向单个 LMR 用户发，用分配给该 LMR 用户的 MCData ID 作目标；IWF 代表 LMR 用户发，用分配给该 LMR 用户的 ID 作源。可选的 Functional alias 属于发送数据用户，不是 IWF 节点 ID 或回执发出者。

| 另外查什么 | 表 10.8.2.2‑1 怎么写 |
| --- | --- |
| **Conversation Identifier 和 Transaction Identifier** | 两项各 M。NOTE 1 分别适用于两项：须定义保留值，表示发送者不支持该项。每个保留值都不是字段省略，也不是可用的会话或事务标识。一个字段用保留值，不表示另一个也不支持；未规定具体值或接收方如何处理。 |
| **Payload Destination Type 和 Payload** | 两项各 M。前者分应用消费和 MCData 客户端消费，后者是 SDS 内容；都不是目标用户 ID。 |
| **Application identifier** | 行标 O，标明预定消费负载的应用。文本、端口地址和 URI 是原文举例，不是清单。按 NOTE 2，符合本表的请求带此项，就只能是应用消费；应用消费仍可不带，客户端消费不能带。看实况就查同笔 Payload Destination Type，单看应用标识不能证实目的类型或合规。 |
| **Reply Identifier 和 Disposition Type** | 两项各 O。Reply Identifier 说明当前事务在答复哪个原事务，不替当前 Transaction Identifier。Disposition Type 请求送达、已读或两者，不是实际处置结果；Reply Identifier 不替处置通知关联的原事务。 |

例如，请求的当前事务是 T2，可选 Reply Identifier 指 T1。这不意味着 T1 是当前事务，也不能把对 T1 的一条处置通知当成对 T2 的报告。只见对 T2 请求送达或已读回执，不能说它已经送达或被读。日志摘录没显示某个 M 项，与已确认完整信息流缺项，是两种证据；本表不规定缺项时的线级响应。

[§10.8.2.1/.2、表 10.8.2.2‑1 及 NOTES 1–2，印刷页 147（PDF 第 148 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=148)。

**不要只凭两个用户 ID 猜是哪张表，也不要拿 Payload 或未列 SDP 断定传输面。** 本表的导语同时指向 TS 23.282 §7.4.2.2.2 与 §7.4.2.3.2；§10.8.6.1/.7.1 的单人信令控制面指 §7.4.2.2，§10.8.6.2/.7.2 的单人媒体面指 §7.4.2.3。先分本次确切流程，未核该外部正文，不从同名表补媒体步骤，不借组请求的 SDP offer、组 ID 或额外接收者字段。§2 [6] 未指定版本，按同一 Release 的该规范最新版本找。其他参考点不是这张 IWF-2 表的适用范围。

[§10.8.6/.7，印刷页 150–151（PDF 第 151–152 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=151)；[§2 [6]，印刷页 11（PDF 第 12 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=12)。

## MC用户向包含LMR用户的MCData组发送SDS；使用信令控制面或媒体面，跨侧客户端位于已归属该组的IWF后

消息寻址到MCData组ID。IWF可代表后方客户端回应disposition请求，给出精确值 disposition prevented by system；这种代理结果不是LMR终端已送达或已读的证明。 [§10.8.8](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## IWF 代 LMR 向 MCData 组发 SDS：找目标组，再找接收 IWF

**看原来谁发起和实际目标。** §10.8.9 是 IWF 代表 LMR 用户向 MCData 组发 standalone SDS；用 MCData group ID 寻址，client 1 位于 IWF 后。信令控制面 §10.8.9.1 指 TS 23.282 [6] §7.4.2.5，媒体面 §10.8.9.2 指 §7.4.2.6。IWF 对其他 MCData servers 作为对等服务器，不因此成了终端。这里核本版回指，不补 TS 23.282 的正文；§2 对未指定修订的 [6] 按同一 Release 的最新版找。[§10.8.9.1–.2，印刷页 151–152（PDF 第 152–153 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=152)；[§2 [6]，印刷页 11（PDF 第 12 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=12)。

**哪一侧查归属？** 两支都说接收 client 2…n 中一名或多名**可以**位于已归属目标组的 IWF 后。要判某位接收者是否落在这个情形，核其实际所在 IWF 对同一个组的归属；另一个组的归属、配置记录或发起 IWF 本身不能替代。没有 IWF 后方接收者也可以按原发起角色读 §10.8.9；本段不要求或免除发起 IWF 的归属，不规定两端是否使用同一实例。对照 §10.8.8：MCData 用户发组 SDS，信令控制面说跨侧接收者“在”IWF 后，媒体面说“可在”；那里的可选代理回执不直接套给 §10.8.9。§10.8.7 的单人源地址规则也不变成组地址规则。没有在本段列出，不等于其他适用条文禁止。[§10.8.7–.9，印刷页 151–152（PDF 第 152–153 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=152)；[归属回指 §10.1.2，印刷页 17（PDF 第 18 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=18)。

**看 IWF-2 这条腿的角色再读 ID。** IWF→MCData server 的组请求，信令控制面查表 10.8.2.4‑1，IWF 作发起客户端；媒体面查表 10.8.2.7‑1，IWF 代表客户端。两表必选发送数据用户的 MCData ID 与目标组 ID，未另列具体接收用户 ID。MCData server→处于客户端代理角色的 IWF，信令控制面查表 10.8.2.5‑1，媒体面查表 10.8.2.8‑1；除原发送者和组 ID，还必须有发给哪位用户的 MCData ID。这个接收用户 ID 不是 IWF 的 ID，也不是用单人 ID 替代组 ID。发生了哪条转发和谁实际收到，另核消息和接收端。[信令请求表，印刷页 148（PDF 第 149 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=149)；[媒体请求表，印刷页 149–150（PDF 第 150–151 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=150)。

**§10.8.5 按实际目的地址决定路由。** 如果 SDS 寻址到位于 IWF 后的 MCData ID 或 MCData group ID，MCData server 须路由到适当的 IWF；发起者在 IWF 后不是这个条件。§10.8.1 写 LMR 用户试图把 LMR 消息发给 MCData 服务时，IWF 把它转成 MCData SDS 请求；IWF 收到发送给某个 LMR 用户或一组 LMR 用户的 MCData SDS 请求时，转为一条或多条 LMR 消息。规范不规定转换方法，也不由数量推每人一份。server 发出、IWF 实收、转换、终端送达或已读，是分开的证据；不从路由能力或要求推出任何一项实际完成。[§10.8.1，印刷页 146（PDF 第 147 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=147)；[§10.8.2.1，印刷页 147（PDF 第 148 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=148)；[§10.8.5，印刷页 150（PDF 第 151 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=151)。

## 原有地址与代报流程的使用边界

仅解释跨侧地址及明确的代理回执例外，不覆盖TS23.282的SDS建立、传输、错误状态机和协议编码。

[scope](scope.md) · [affiliation-results](affiliation-results.md) · [delivery-evidence](../mcdata/delivery-evidence.md) · [结构化条件](sds-addressing.json)

## IWF-2：组媒体应答与处置通知

这两种信息流适用 TS 23.283 V19.5.0、Release 19、Stage 2。先确认实际事件在 IWF-2 上，再按信息流、方向和角色选表。同一方向也可能承载不同的信息流；其它参考点的原生 MCData SDS 不用这些表。[§10.8.1，印刷页 146](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=147)；[§10.8.2.1，印刷页 147](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=148)

**收到组媒体应答，知道选了哪些媒体参数。** §10.8.2.9 描述 IWF→MCData server，以及 MCData server→充当其他 MCData 客户端代理的 IWF。两种方向都按数据角色辨认用户，不按这条应答的发送方与接收方换位。表中五项都是必选：接收数据用户的 MCData ID、目标 MCData 组 ID、发送数据用户的 MCData ID、Conversation Identifier、SDP answer。表没有列独立的 Transaction Identifier、Disposition association、Disposition、结果或 SDS 负载。看到应答不能判已传送、终端已收到或已读，也不能判全组完成。[表 10.8.2.9‑1，印刷页 150](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=151)

**收到服务器发给代理 IWF 的处置通知，按原事务和本条通知的身份记录。** §10.8.2.6 的方向是 MCData server→充当 MCData 客户端代理的 IWF。表中五项都是必选：通知目标用户的 MCData ID、发出处置通知的用户的 MCData ID、Conversation Identifier、指向原 MCData 事务的 Disposition association，以及 Disposition。按通知实际报告的值记：delivered、read、delivered and read、disposition prevented by system。最后一个值表示系统阻止了处置回执，不能折算为终端送达/已读，也不等于终端没收到。此表没有把场景限成组 SDS；上面 §10.8.8 的归属和请求条件约束那条代理应答流程，不是读取本表的通用前提；也不能由本表断定所有单人流程都会发通知。[表 10.8.2.6‑1，印刷页 149；入口跨 148–149 页](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=150)

例如，同一会话 C 发了两条 SDS，原事务分别是 T1 和 T2。若符合 §10.8.2.6 的实际通知只关联 T1，就只能说相应通知身份对 T1 报告了该状态。对 T2、其他成员或独立的终端事件不作判断。日志摘录没显示关联是证据不足；完整信息流已确认少了关联是不满足表的必选项。不能拿 C、组 ID、时间顺序或请求里的可选 Reply Identifier 补齐；本表不规定缺字段时的协议响应。

**只看方向、请求或保留值，仍会选错。** IWF→MCData server 若是实际处置通知，查 §10.8.2.3 的双向通用通知表，不套 §10.8.2.6。服务器→IWF 若只能确认方向、还未确认 IWF 的代理角色与通知类型，也不能直接定为 §10.8.2.6。§10.8.2.3 和 §10.8.2.9 都保留了 Conversation Identifier 必选项，表注要求定义一个保留值，表示发送者不支持该项；保留值不等于省略，也不是一个可用的会话关联值。这两处没给具体数字；§10.8.2.6 没有这一表注，不替它写规则。组媒体请求 (§§10.8.2.7–8) 的 SDP offer 是提出参数、可选 Disposition Type 是请求哪种回执，均不等于实际处置报告。组信令控制面请求 (§§10.8.2.4–5) 的 SDS 负载也不是处置报告。[表 10.8.2.3‑1，印刷页 147](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=148)；[§§10.8.2.4–5，印刷页 148](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=149)；[§10.8.2.7，印刷页 149](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=150)；[§10.8.2.8，印刷页 150](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=151)

这些表不规定应答、媒体传送与处置通知之间的统一顺序，也不证明物理 LMR 端收到、显示或读取了内容。仍按原有主题查 [Stage 1 的送达和已读要求](../mcdata/delivery-evidence.md) 或 [普通在网 SDS 的 Stage 3 回执程序](../mcdata/sds-disposition-timing.md)；原生 SIP 200/202、原生消息 ID 或 LMR 侧编码不能用来补 IWF-2 的证据。
