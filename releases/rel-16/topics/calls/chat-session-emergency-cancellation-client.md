# MCPTT 聊天组取消紧急状态：组状态和告警分别读哪项响应？

范围：TS 24.379 V16.14.0（Release 16，Stage 3）§10.1.2.2.1 的 MCPTT 客户端、限制型聊天组（chat group）。父标题写 On-demand chat group call，但这两个子条款都明确适用于按需和预建立会话。本页是发起操作的客户端，不是接收入向 re-INVITE 的对端客户端、控制功能或参与功能。

收到取消的 2xx，不等于个人告警一定已撤销。这里是限制型 MCPTT 聊天组中发出取消操作的客户端。虽然父标题写的是按需聊天组，这一条明确包含按需和预建立会话。用户请求取消该组的进行中紧急条件；不能用新建组呼的初始 INVITE 或其他节点收到的应答来判定本端结果。[印刷页 268](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=269)

## 请求发出前查什么？

1. 按 §6.2.8.1.7 判断该用户能否取消这个组的紧急状态。未获准时，客户端**宜告知用户无取消权限**，并**须跳过后续步骤**。
2. 取消组条件可以附带撤警。涉及本人发的告警时，MCPTT 信息正文按 §6.2.8.1.3；涉及另一用户发的告警时，按 §6.2.8.1.14。两条都是取消组紧急条件的正文分支，不能仅凭走了某个分支认定撤警成功。
   - 组状态取消获准不等于获准撤警。若还要取消同组另一位用户发起的告警，须另按 §6.2.8.1.6 获准。 在这个分支，客户端须在发出的 re-INVITE 的 `application/vnd.3gpp.mcptt-info+xml` 正文中放入 `alert-ind=false`，把 `originated-by` 设为**原告警发起者的 MCPTT ID**，不填取消请求者的 ID 或组 ID。同组可能有多人发过告警，这个元素标识要撤哪一条。仅取消组状态时，不能从这里要求两个告警字段。此处不规定缺少原发起者 ID 时的处理。[本条步骤 3，印刷页 268](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=269)、[所引 §6.2.8.1.14 步骤 3(a)–(b) 及注，印刷页 69](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=70)
3. 按需会话按 TS 24.229 和 §6.2.1 放入 SDP offer；预建立会话按已协商参数放入 offer。注 1 说预建立的语音和话权控制媒体段预期同原协商一致，不是整份 SDP 原样复用。按 §6.2.8.1.2 携带 Resource-Priority，再按 TS 24.229 发送这笔 re-INVITE。[印刷页 268](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=269)[印刷页 269](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=270)

## 匹配应答改变哪一个状态？

**2xx。** 本客户端把该组状态设为 `MEG 1: no-emergency`，把紧急组呼状态设为 `MEGC 1: emergency-gc-capable`。要把告警也设为 `MEA 1: no-alert`，还要同时满足：

- 本客户端当前告警为 `MEA 4: Emergency-alert-cancel-pending`。
- **本端发出的** MCPTT 信息正文没有 `originated-by`。
- **这笔匹配应答**没有 §4.4 所述 Warning，即文本含 `mcptt-warn-code=149` 的警告。

条件不齐，不能援引这一项认定告警已撤。149 是 Warning 文本中的 MCPTT 警告码，不是 SIP 响应状态码。[印刷页 269](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=270)

**4xx、5xx、6xx。** 这类匹配负响应使本地组状态设为 `MEG 2: in-progress`。注 3 说明取消被拒后，会话继续保持紧急组呼级优先级。对告警另查：

| 看什么 | 告警状态怎样处理 |
| --- | --- |
| 收到的 MCPTT 信息正文带 `alert-ind=true`，且**发出的请求**正文不带 `originated-by` | 设为 `MEA 3: emergency-alert-initiated`。 |
| **收到的负响应**没有带 `alert-ind` 的 MCPTT 信息正文，也没有 `originated-by` 元素 | 恢复进入这次取消过程前的 MEA 值。 |

后一行的两项缺失都以收到的负响应为对象，不是上一行的“已发请求无 `originated-by`”。明确的 `alert-ind=false` 既不是元素缺失，也不命中 `true` 分支；本节没有另外指定这种形态的 MEA 赋值。负响应也没有另写 MEGC 赋值。[印刷页 269](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=270)

**INFO 是另一个事件。** 这两个客户端子条款都规定：收到 SIP INFO，且 Request-URI 含标识进行中组会话的 MCPTT session ID，走 §6.2.8.1.13。不能把一条 re-INVITE 应答当成这条 INFO 已到。本页只登记这个入口，不展开辅助条款的动作。[印刷页 269](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=270)[印刷页 270](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=271)

相关问题：[聊天组升级紧急或迫近危险](chat-session-priority-upgrade-client.md)；[聊天组初始建立、加入与相邻状态处理](chat-establish-join.md)；[预安排组的客户端紧急操作](emergency-group-client.md)。
