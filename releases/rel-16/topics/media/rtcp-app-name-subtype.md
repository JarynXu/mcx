# RTCP APP 的 subtype 都是 10001：收到的是 Floor Granted 还是 Disconnect？

只看到 `PT=204`、`subtype=10001`，不能在这两条消息之间选择。**先读 RTCP APP 头里的四字节 ASCII Name，再按该 Name 对应的表查 subtype。** PT=204 只说明这是 APP 包。下面两种包都可以从服务端发给客户端，且 subtype 的首位都为 1，要求本消息族的确认；方向和首位都不能区分它们。〔TS 24.380 V16.9.0，Rel-16，Stage 3，§8.1.2，印刷页 145–146；表 8.2.2.1-1，页 148；表 8.3.2-1，页 175〕

| 实收包的 Name | 该表中 `10001` 的含义 | 要求哪种确认 |
| --- | --- | --- |
| `MCPT` | **Floor Granted**，授予话权 | 话权消息 **Floor Ack**；其 subtype 是 `01010`。 |
| `MCPC` | **Disconnect**，预建立会话的呼叫控制 | **Acknowledge**；其 subtype 是 `00010`。 |

日志没有 Name，就去查原始 RTCP APP 包或能分辨消息族的记录。日志漏记 Name 是观察证据不足，不等于终端收到未知消息、主动丢包，也不能看见通用的「Ack」就反过来猜消息族。〔§8.1.2 及两张消息表〕

## 同一初始状态，收到两种包，终端动作不同

假设一通普通在网私呼正在使用预建立会话，终端处于 `U: Pre-established session in use`，话权参与者处于 `U: pending Request`。下面是两种备选的实收有效报文，不是一前一后两个步骤。

- **实收 `MCPT/10001`：** 按 Floor Granted 处理。终端发送 Floor Ack，Message Type 为 **1**、Source 为 **0**。话权侧停止 T101，若可选的 T103 正在运行也停止，然后进入 `U: has permission`。预建立会话状态仍是 **in use**。这证明不了终端已经发过 RTP。〔§9.2.2.4.3，页 196；§6.2.4.4.2，页 39–40〕
- **实收 `MCPC/10001`：** 按 Disconnect 处理。终端发送原因 **Accepted** 的 Acknowledgement，并进入 `U: Pre-established session not in use`，随后依 §6.2.4 处理话权。这是本次呼叫不再使用该预建立会话，不是拆除预建立会话，也不证明服务端已经收到确认。〔§9.2.2.4.5，页 196〕

还要查[等待授予时的普通话权处理](on-network-floor-client.md)，或查[Disconnect 的发送端与收到确认后的状态](preestablished-release-outcome.md)，分别进入对应主题。

依据：[RTCP APP 头与 Name，印刷页 145–146](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=146)；[终端预建立会话在用状态，印刷页 196](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=197)。

已能认出消息族后，若实际接收记录提示 subtype 未知、字段未规定或可选字段语法错误，查[未知消息或字段的忽略范围](rtcp-app-unknown-control-fields.md)。日志少打一项，不等于接收端遇到未知项。
