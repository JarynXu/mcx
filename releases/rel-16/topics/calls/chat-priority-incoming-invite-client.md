# 已归属未入会：终端怎样处理聊天组的紧急或迫近危险 INVITE？

适用 TS 24.379 V16.14.0（Release 16，Stage 3）§10.1.2.2.1.6。这里是按需限制型聊天组中已归属但未入会的客户端，实际收到紧急或迫近危险组呼的**初始 SIP INVITE**。这不是用户回到覆盖后主动加入，不是已入会后的 re-INVITE，也不是参与功能转发邀请的程序。[§10.1.2.2.1.6 入口，印刷页 272](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=273)。

## 紧急邀请可以拒绝吗？

可以。客户端资源不足、该特定**主叫功能别名**的并发 MCPTT 紧急组呼已达上限，或有本规范范围外的其他原因时，客户端可以拒绝。上限取 TS 24.484 所述 MCPTT 用户档案中 `<FunctionalAliasList>` 下的 `<MaxSimultaneousEmergencyGroupCalls>`。这不是接收用户的全局并发额度。该节未给缺少别名或配置时的缺省值，也未写达到上限就必拒。注 1 说有紧急或迫近危险指示时，客户端仍可用本规范范围外的方式选择接受。

决定拒绝后，须向参与 MCPTT 功能答复并停止本节余下步骤。可以按 TS 24.229 返回适当拒绝码、带 §4.4.2 所述警告文本；用户获准隐藏失败原因时，才可选用不含警告文本的 SIP 480。[步骤 1–2 和注 1，印刷页 272](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=273)。

## 继续处理时，两个指示怎么选？

紧急和迫近危险指示是入向 `application/vnd.3gpp.mcptt-info+xml` 中 `<mcpttinfo>` / `<mcptt-Params>` 下的 `emergency-ind` 与 `imminentperil-ind`。

- `emergency-ind=true`：须设 `MEG 2: in-progress`、`MIG 1: no-imminent-peril` 和 `MIGC 1: imminent-peril-gc-capable`。宜显示紧急组呼邀请、`mcptt-calling-user-id` 指定的发起用户和 `mcptt-calling-group-id` 指定的组。还带 `alert-ind=true` 时，宜显示告警及相关信息。
- 未命中上一项且 `imminentperil-ind=true`：须设 `MIG 2: in-progress`。宜显示迫近危险组呼邀请，以及相同两个字段分别标识的发起用户和组。

步骤 3 末尾的 `otherwise` 限定步骤 4。缺字段不是 `false`；这两步也没有另设“收到 `false` 就清除”的分支。不能把组呼指示、个人告警显示和外部优先级头混成一个状态。[步骤 3–4，印刷页 272](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=273)、[印刷页 273](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=274)。

## 接受时，200 要带什么？

客户端**须检查**来向 INVITE 是否含 `Resource-Priority`，但发现后可采取的进一步动作不由本节定义。缺头不是这一步列出的拒绝条件。客户端须按 TS 24.229 接受并向 MCPTT 服务器发送 200 (OK)。应答含：

- `Contact` 中的 `g.3gpp.mcptt` 和 `g.3gpp.icsi-ref`，后者值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`。
- 对来向 SDP offer 的 answer，按 TS 24.229 和本规范 §6.2.2 构造。
- `Require` 中的 `timer`，以及 `Session-Expires`。客户端须按 RFC 4028 启动 SIP 会话计时器。来向 INVITE 未带 `refresher` 参数，响应填 `uas`；来向带了则沿用收到的值。

发送 200 后，客户端须按 TS 24.380 与媒体面交互。入向正文含 `functional-alias-URI` 时，可以显示邀请用户的功能别名。显示别名不是重写发起用户 MCPTT ID；应答和调用媒体面也不证明已经获话权或收发了 RTP。[步骤 5–14，印刷页 273](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=274)。

[进行中会话收到 re-INVITE](chat-session-incoming-reinvite-client.md)；[回到覆盖后由用户主动加入](chat-establish-join.md)；[预建立聊天组的 REFER 与参与功能职责](chat-preestablished-refer-outcome.md)。
