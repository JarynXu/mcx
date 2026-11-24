# MCPTT 聊天组怎样升级紧急或迫近危险？什么时候才补位置？

范围：TS 24.379 V16.14.0（Release 16，Stage 3）§10.1.2.2.1 的 MCPTT 客户端、限制型聊天组（chat group）。父标题写 On-demand chat group call，但这两个子条款都明确适用于按需和预建立会话。本页是发起操作的客户端，不是接收入向 re-INVITE 的对端客户端、控制功能或参与功能。

聊天组会话已经存在。用户是要将它升级到紧急，还是迫近危险？这里是发出升级请求的客户端，按需和预建立会话都适用。客户端按 §6.2.8.1.8 查所请求类型的授权；没获准时，宜提示该类型无授权，并须跳过其余步骤。[印刷页 269](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=270)[印刷页 270](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=271)

| 用户请求 | application/vnd.3gpp.mcptt-info+xml 正文 | 本分支的 Resource-Priority 回指 |
| --- | --- | --- |
| 紧急 | §6.2.8.1.1 | 步骤 3(b)：§6.2.8.1.2 |
| 迫近危险 | §6.2.8.1.9 | 步骤 4(b)：§6.2.8.1.12 |

共同步骤 8 仍写携带 Resource-Priority 并按 §6.2.8.1.2 处理。两处回指须保留，不能因此断言迫近危险时要发两份同名头，或自己选一个步骤覆盖另一个。按需会话的 SDP offer 按 TS 24.229 和 §6.2.1，预建立会话依据已有协商参数；注释对语音和话权控制媒体段写的是预期与原协商一致。客户端按 TS 24.229 发送 re-INVITE。[印刷页 270](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=271)

## 隐式话权请求要不要补位置？

需要隐式话权请求时，须按 §6.4 指示。只有以下三点都成立，这个升级步骤才要求补加位置正文：

1. 本次需要隐式话权请求。
2. 由**主叫 MCPTT 用户的 MCPTT ID** 标识的用户档案里，`ruleset` 的 `allow-location-info-when-talking` 为 `true`。
3. 这笔 re-INVITE 尚未包含位置。

此时加入 `application/vnd.3gpp.mcptt-location-info+xml` 正文，根 `<location-info>` 中包含 `<Report>`。已有位置时，不能从这一步推出须再加一份，或须删除本来已有的位置。这是升级步骤的附加条件，不是所有 re-INVITE 的通用规则；请求话权也不等于获授话权。[印刷页 270](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=271)

## 应答要匹配本次升级

- **匹配 2xx：** 客户端须按 TS 24.380 与用户面交互，并执行 §6.2.8.1.4 的优先呼叫成功处理。
- **匹配 4xx、5xx 或 6xx：** 客户端须执行 §6.2.8.1.5 的优先呼叫失败处理。

本节没有把辅助处理改写成“收到 2xx 就能确定最终状态”。不要把取消紧急状态时的 MEG、MEGC 或 MEA 赋值套进升级，也不能用其他节点看到的响应推定本端已完成。带进行中组会话 ID 的 SIP INFO 另走共同的 §6.2.8.1.13 入口，见取消页的说明。[印刷页 270](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=271)

相关问题：[聊天组取消紧急与两个子条款的 INFO 入口](chat-session-emergency-cancellation-client.md)；[聊天组初始建立、加入和相邻迫近危险取消](chat-establish-join.md)；[预安排组的发起端动作](emergency-group-client.md)；[隐式话权 SDP 的答复如何判读](../media/implicit-floor-sdp-ssrc.md)。
