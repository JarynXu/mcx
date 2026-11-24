# NCF 发出的 INVITE 183：PAI、Contact 和 Supported 写什么？

MCPTT 组的非控制功能（NCF）终接一笔 SIP INVITE，**在它实际发送 SIP 183（Session Progress）时**，须按 TS 24.229 生成应答。[TS 24.379 V16.14.0 §6.3.4.2.2.1，印刷页 129](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=130)对这份 183 的头字段有以下要求：

| 字段 | 要求 |
| --- | --- |
| `P-Asserted-Identity`（PAI） | 带发出这份 183 的 NCF 自己的公共业务标识（PSI）。 |
| `Contact` | 带 `g.3gpp.mcptt`，还要带值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt` 的 `g.3gpp.icsi-ref`。 |
| `Supported` | 按 RFC 4538 的规则加入 `tdialog`。 |

先把响应对回同一笔 INVITE，再确认 NCF 是这份 183 的发送方。NCF **收到**客户端响应是另一条程序，例如 [NCF 主动邀请晚入的客户端后收到 183](noncontrolling-prearranged-rejoin.md)。这里的 Contact 不套用控制功能（CF）另一腿的规则。本条没有规定在 Contact 填 MCPTT 会话标识或添加 `isfocus`，也没有禁止它们。

本条没有要求每个 INVITE 都回复 183，也不适用于其他 1xx。需查[组成聊天组终接 INVITE 的最终 200 和 SDP](trusted-regroup-refused-uri-list.md#chat-ncf-initial-invite)时，按那笔响应和它的触发条件判断。仅凭 183 状态码或 `tdialog`，不能断定需要 `100rel`、PRACK 或 SDP，也不能判定已获话权或 INVITE 已获最终接受。
