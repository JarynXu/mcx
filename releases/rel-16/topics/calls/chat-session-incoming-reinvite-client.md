# MCPTT 聊天组收到 re-INVITE，什么时候清组状态或本地告警？

适用 TS 24.379 V16.14.0（Release 16，Stage 3）§10.1.2.2.1.2。这里是限制型聊天组中实际收到 SIP re-INVITE 的客户端。条款明确适用于按需和预建立会话。初始 INVITE、发起侧收到的应答、控制功能和参与功能的处理不在本节。

先看这笔入向请求的 `application/vnd.3gpp.mcptt-info+xml` 正文。以下指示取自 `<mcpttinfo>` 下的 `<mcptt-Params>`。缺字段不是明确的 `false`，不能用缺字段触发相应的清除分支。

| 入向指示 | 接收客户端的动作 |
| --- | --- |
| `emergency-ind=true` | 须设组紧急状态为 `MEG 2: in-progress`，将迫近危险组状态和组呼状态设为 `MIG 1: no-imminent-peril`、`MIGC 1: imminent-peril-gc-capable`。宜显示紧急组呼和发起者的 MCPTT ID；若还带 `alert-ind=true`，宜显示告警及相关信息。 |
| `imminentperil-ind=true` | 须设 `MIG 2: in-progress`。宜显示迫近危险组呼和发起者的 MCPTT ID。 |
| `imminentperil-ind=false` | 须设 `MIG 1: no-imminent-peril` 和 `MIGC 1: imminent-peril-gc-capable`。宜显示取消者的 MCPTT ID 和迫近危险组呼指示。 |

这是本节分别列出的条件。不能把初始邀请的 `otherwise` 分支搬进来，也不能把告警显示当作已修改本地告警状态。[§10.1.2.2.1.2 步骤 1、2，印刷页 267](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=268)；[步骤 4，印刷页 268](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=269)。

## 取消组紧急，不一定清本地告警

入向正文明确带 `emergency-ind=false`，客户端须设 `MEG 1: no-emergency`，宜显示取消紧急组呼的用户 MCPTT ID。该组的紧急组呼状态原为 `MEGC 3: emergency-call-granted` 时，才由这一步设为 `MEGC 1: emergency-gc-capable`。

同一取消分支内还明确带 `alert-ind=false` 时，客户端宜显示撤警和撤警者的 MCPTT ID；若正文还含 `originated-by`，宜显示它指向的告警发起者。**只有这个 MCPTT ID 与接收用户的 MCPTT ID 相同，才由此分支把本地告警设为 `MEA 1: no-alert`。** 两个 ID 的角色不同。撤警者是本次操作的人，`originated-by` 指原告警发起者。缺字段、字段指向别人，或只有组紧急取消，均不能从这一步推断本人告警已清。原文未给缺字段时的替代 ID。[§10.1.2.2.1.2 步骤 3，印刷页 267](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=268)。

## 如何回这笔 re-INVITE？

客户端可以查来向有无 `Resource-Priority`。发现该头后，按 TS 24.229 对它采取进一步动作也是可选的，本条不定义这些动作。可选的是优先级头的检查和后续动作，不是应答：客户端须按 TS 24.229 接受这笔 re-INVITE，向 MCPTT 服务器发送 SIP 200 (OK)。200 的 `Contact` 须含 `g.3gpp.mcptt` 和 `g.3gpp.icsi-ref`，后者值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`。

两种会话都在 200 中放入对来向 SDP offer 的 answer。按需会话按 TS 24.229 和本规范 §6.2.2；预建立会话按 TS 24.229 并以已协商参数为基础。注释只说语音和媒体话权控制两个媒体段预期同原协商一致，不要求整份 SDP 字节相同。本节没有另写初始邀请的 `Require: timer` 或 `Session-Expires` 处理；不能从这个 200 推断其他参与者的状态。[§10.1.2.2.1.2 步骤 5–11 与注释，印刷页 268](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=269)。

[已归属但未入会时的初始紧急或迫近危险邀请](chat-priority-incoming-invite-client.md)；[预安排组的客户端紧急操作](emergency-group-client.md)；[终接参与功能收到或转发 re-INVITE](chat-preestablished-refer-outcome.md)。
