# 在网临时广播组：谁能创建，谁能发送？

**获授权的用户须能创建临时广播组；业务须允许该组创建者在该组发送，不得允许其他用户发送。** 创建时要分清输入是一批组，还是一批用户。依据是 3GPP TS 22.280 V16.8.0（Release 16）在网 Stage 1 的 §6.6.3。[第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)；[§6.6.3，印刷页 35（PDF 第 36 页）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=36)。

| 要创建的临时广播组 | MCX 业务须提供的能力 |
| --- | --- |
| 临时组广播组（Group-Broadcast Group） | 须使获授权的 MCX 用户能够用该 MCX 业务内的多个 **MCX 业务组**创建。[R-6.6.3-001，印刷页 35](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=36)。 |
| 临时用户广播组（User-Broadcast Group） | 须使获授权的 MCX 用户能够用该 MCX 业务内的多个 **MCX 用户**创建。[R-6.6.3-001a，印刷页 35](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=36)。 |

两条都限定输入在该 MCX 业务内。仅知对象属于相同的业务类型，不足以认定它们在同一个 MCX 业务内。这里规定业务必须具备创建能力，不要求已经发生一次创建，也不证明某次请求已建组或已开播。

## 组创建者和某次呼叫的发起者不是一个判据

对这两类临时广播组，MCX 业务须允许**该组的创建者**在该组发送，不得允许其他用户发送。业务若连创建者也不允许发送，就没满足这项要求。假设甲创建了临时广播组 T，乙也有创建临时广播组的权限，甚至提交了 T 的一次广播发起请求。乙不是 T 的创建者，不能凭创建权限、在 T 的归属或发起请求取得在 T 发送的许可。甲作为创建者属于业务须允许在 T 发送的角色；这不保证某次呼叫获准建立、某次话权请求获准或甲已经发送媒体。[R-6.6.3-002，印刷页 35](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=36)。

**适用业务：** 表 A.1（MCPTT）、B.1（MCVideo）和 C.1（MCData）均在 §6.6.3 行列出这三项。[表 A.1，印刷页 66](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=67)；[表 B.1，印刷页 77](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=78)；[表 C.1，印刷页 88](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=89)。

[把广播组作为 Group Regroup 的输入](onnetwork-group-regroup-input-eligibility.md)、[发起广播时可否终止其他通信](onnetwork-broadcast-optional-termination.md)和[广播组的终端自动归属](onnetwork-affiliation-and-revocation.md)处理的是其他问题。若在查[MCPTT 预安排组上发起广播](../calls/onnetwork-prearranged-broadcast-origin.md)或[MCVideo 广播组呼](../mcvideo/onnetwork-broadcast-group-call.md)，按各自的 Stage 3、Stage 2 流程核对；**一次呼叫的发起角色不代替该临时组的创建者身份**。本节不规定这些流程怎样创建临时组、临时组存续时间、报文、实际发送或部署支持。
