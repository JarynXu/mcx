# 预配置用户重组：MCPTT 与 IWF 怎样取消？

取消请求指向**实际重组组 D** 的 MCPTT 组 ID，不是提供配置的来源组 P。按本次取消由谁发起来读步骤。两支都要求已有一个 MCPTT 客户端和至少一个本属 IWF 的用户被重组进同一个 D；用户本属、手头有 D 的配置或以前收到请求，都不能代替这个前提。[成形](preconfigured-user-regroup-formation.md)后的 NOTE 2 回指各自的显式取消流程。一次组呼结束不等于取消 D；回指也不授权另一侧代取消。

[§10.3.8.2.1/.2.2 NOTE 2，印刷页 87（PDF 第 88 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=88)；[§10.3.8.3.1/.2 前提与发起请求，印刷页 88–89（PDF 第 89–90 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=89)。

## MCPTT 系统发起取消

- **1–3：**获授权的 client 1 用户发起；client 1→MCPTT server 发取消请求并指定 D；server 检查 client 1 的取消权限。成形时的权限或发出本次请求，不等于这一笔验权通过。此分支明确要求已有 client 2 和至少一个本属 IWF 的用户重组进 D。
- **4–6：**server→client 2 发取消请求，由 client 2 通知其用户。client 2 **可以**回确认；步骤 4 实际用组播发送时，不回该请求的这条确认。图为简化只画一个接收客户端，不给终端数量上限或下发算法。
- **7/8：**server→IWF 发 IWF 取消请求；IWF→server 回 IWF 取消应答。**9** 是 server 退归属操作：正文列 MCPTT client 2 和 3，图框写 MCPTT clients **与 IWF**，图上仅画接收 client 2。保留两处写法，不能据图断 IWF 必退，也不能据正文未列断 IWF 不退；更不能从一条回包判某个用户已退。**10** 是 server→发起 client 1 的另一条应答，不是 8 转读成终端回包。

[§10.3.8.3.1、图 10.3.8.3.1-1、步骤 1–10，印刷页 88–89（PDF 第 89–90 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=89)。

## IWF 发起取消

**1** 由 IWF→server 发取消请求并指定 D。图标为 IWF 取消请求，正文省去消息名的 IWF 前缀，发送端仍然是 IWF。**2/3** 是 server→接收 client 发取消请求，再由该 client 通知其用户。**4** 是 client→server 可以回的确认；也不对组播发送的这条请求回确认。**5** 是 server→IWF 发 IWF 取消应答，方向与 MCPTT 发起的 8 相反。图也只画一个接收 client。

本支未写前支的验权步骤 3 或退归属步骤 9，不能照搬这两个步骤，也不能据此判免验权或不退归属。这里的 5 是应答，不是组成组重组取消的退归属 5、应答 6（[§10.3.7.3.2，印刷页 77–78（PDF 第 78–79 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=78)）。

[§10.3.8.3.2、图 10.3.8.3.2-1、步骤 1–5，印刷页 89（PDF 第 90 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=90)。

## IWF 请求和应答的表各管哪一条？

| 已识别的消息 | 用哪张表 | 这张表列什么 |
| --- | --- | --- |
| MCPTT 发起 7，server→IWF；IWF 发起 1，IWF→server | **10.3.2.16-1** | 请求者 MCPTT ID、实际重组组 D 的 MCPTT 组 ID，各 M。 |
| MCPTT 发起 8，IWF→server；IWF 发起 5，server→IWF | **10.3.2.17-1** | 请求取消者 MCPTT ID、实际重组组 D 的 MCPTT 组 ID、取消操作的 **Result**，各 M。 |

两张表都适用于 IWF-1 的两个方向，但按消息类型读自己的表。单查请求或应答各自的结构，不需要已看到另一条；认定它们对应才要核同一次取消。这些表不列形成时的来源组 ID 和名单，也不定义哪个实际用户退归属、结果码或可唯一配对同一事务的键。请求者 ID 不按发件网元或接收 client 的 ID 代填。不把 IWF 表套给原生 client 请求、可选确认或 MCPTT 发起的 Step 10。

[§10.3.2.1，印刷页 35（PDF 第 36 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=36)；[§10.3.2.16、表 10.3.2.16-1，印刷页 39–40（PDF 第 40–41 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=40)；[§10.3.2.17、表 10.3.2.17-1，印刷页 40（PDF 第 41 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=41)。

## 看见应答，哪些事还没证实？

MCPTT 发起的 6 或 IWF 发起的 4，是接收客户端的确认，不是 IWF 腿的 Result。没见确认，不能判没通知、取消失败或没有 IWF 应答；单播也不要求必回。客户端通知用户的动作与用户实际获知要分开。对一笔 IWF 8/5 或 server 回 client 1 的 10，也要区分**箭头起点送出**和**箭头终点实收**。报出的操作结果不证明全部终端已确认、已执行 Step 9 或特定 IWF 后方用户已退归属。示意箭头次序不是等待所有确认、超时或汇总算法。

这里只读 Stage 2 的 IWF 用户重组取消。原生 SIP MESSAGE、CF/T-PF 和 200 看[预配置重组移除](../groups/preconfigured-regroup-removal.md)；互通 ad hoc 呼叫释放看[临时组释放](adhoc-group-release.md)。都不替本笔的退归属、组是否仍有效、话权或实际媒体取证。

[两支取消步骤及图，印刷页 88–89（PDF 第 89–90 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=89)。
