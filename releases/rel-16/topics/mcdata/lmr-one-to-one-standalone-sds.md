# MCData 与 LMR 的一对一独立短数据：LMR 用户 ID 放哪边，处置通知关联哪一笔？

MCData 发给单个 LMR 用户时，**目标是分配给该 LMR 用户的 MCData ID**。反过来，IWF 代 LMR 用户发请求，**分配给该 LMR 用户的 MCData ID 是源地址**，不是把 IWF 自己当成发送用户。数据处置通知是另一条消息：用 `Disposition association` 找到它所报告的原事务。

这里是一名 MCData 用户与一名 LMR 用户经 IWF 交换一对一独立短数据（standalone SDS）。LMR 用户在 MCData 一侧用分配给他的 MCData ID 表示。 以下按 3GPP TS 23.283 V16.8.0（Release 16，Stage 2）判断；不把 IWF-2 的信息元素当作无线侧或 SIP 报文字段。

## 两个方向分别替换哪个客户端

| 发送方向 | IWF 后方的角色 | 传送面与依据 |
| --- | --- | --- |
| MCData 用户 → 单个 LMR 用户 | 接收客户端 2；LMR 用户的 MCData ID 是目的地址。 | 信令控制面回指 TS 23.282 §7.4.2.2，媒体面回指 §7.4.2.3。[§10.8.6.1 开始，印刷页 146](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=147)；[§10.8.6.1 续及 §10.8.6.2，印刷页 147](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=148)。 |
| LMR 用户 → 单个 MCData 用户 | 发起客户端 1；IWF 代发，LMR 用户的 MCData ID 是源地址。 | 信令控制面仍回指 TS 23.282 §7.4.2.2，媒体面仍回指 §7.4.2.3。[§§10.8.7.1–.2，印刷页 147](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=148)。 |

两向的 IWF 都以对等 MCData 服务器的角色工作。LMR 消息发往 MCData 时，IWF 把它转换为 SDS 发送请求；反向把请求转换为一个或多个 LMR 消息。两向的具体转换方法都不在该规范范围内。此处的字段表适用 IWF-2；其他参考点的 SDS 信息流查 TS 23.282 §7.4.2.1。[§10.8.1，印刷页 142](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=143)；[§10.8.2.1，印刷页 143](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=144)。

## 请求上的身份、事务和负载

[表 10.8.2.2-1，印刷页 143](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=144)用于 MCData 服务器到 IWF、IWF 到 MCData 服务器两个方向。两个必备的 `MCData ID` 各有角色：发送用户、目标用户。还须有 `Conversation Identifier`、`Transaction Identifier`、`Payload Destination Type` 和 `Payload`。注 1 要求为前两个标识各定义相应的预留值，表示发送方不支持该信息元素。表仍把字段列为必备，不支持不能理解成省略字段；这里没有给预留值的具体数值。

`Reply Identifier` 可选，指向本次事务回复的原事务。`Disposition Type` 可选，表示期望接收方报告送达、已读或两者，不是已取得的结果。`Payload Destination Type` 说明负载由应用还是 MCData 客户端消费。`Application identifier` 标记为可选；按注 2，只有面向应用消费才可带，不等于面向应用就必带。这张信息流表的引言同时回指控制面与媒体面的基础过程；表中列 `Payload` 不等于这里规定媒体面正文如何传送。

## 处置通知上的两项身份对应本条通知

[表 10.8.2.3-1，印刷页 143](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=144)用于 IWF 与 MCData 服务器之间的两向通知。五项均必备：通知接收用户、通知发送用户的 `MCData ID`，`Conversation Identifier`，`Disposition association`，以及 `Disposition`。会话标识有自己的不支持预留值。**识别原事务靠 `Disposition association`**，不能用会话号或请求里的 `Reply Identifier` 替代。

`Disposition` 可表示已送达、已读、送达且已读，或 `disposition prevented by system`（系统阻止处置）。最后一种不表示已送达、已读，也不能拿它断定正文被阻止。这里的枚举没有规定一对一场景中 IWF 何时可以或必须代表接收端回报。若问题是 [LMR 参与的组独立短数据如何代答](lmr-group-standalone-sds.md)，查组主题给出的适用条件。

若两端都在[同一 MCData 系统的一对一独立 SDS](one-to-one-standalone-sds.md)，可在该主题展开控制面与媒体面基础流程。查[普通一对一 SDS 的控制面服务器报文](sds-control-server.md)，另按该 Stage 3 主题的条件判断；它不定 IWF-2 的报文编码。
