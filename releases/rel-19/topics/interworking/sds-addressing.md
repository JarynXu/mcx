# 互通SDS：地址映射与代理回执

TS23.283 V19.5.0，Release19，Stage2。

## MC用户与单个LMR用户之间的SDS；使用信令控制面或媒体面

发往LMR用户时，目标是分配给该LMR用户的MCData ID；LMR用户发起时源地址使用其分配的MCData ID。IWF以对等MCData服务器角色参与，基础发送过程仍依赖TS23.282。 [§10.8.6–7](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## MC用户向包含LMR用户的MCData组发送SDS；使用信令控制面或媒体面，跨侧客户端位于已归属该组的IWF后

消息寻址到MCData组ID。IWF可代表后方客户端回应disposition请求，给出精确值 disposition prevented by system；这种代理结果不是LMR终端已送达或已读的证明。 [§10.8.8](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

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
