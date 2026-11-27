# 预配置用户重组：MCPTT 与 IWF 怎样建组？

**先分两个组，再分谁发起。** TS 23.283 V19.5.0 §10.3.8 是把指定**用户**放进新的实际重组组，不是把几个组成组并在一起。来源组只提供配置，一组可给多个用户重组使用；实际重组的 MCPTT 组 ID 由获授权的发起用户或发起 IWF 在重组时给出。相关用户要提前取得配置。若按 NOTE 2 从其他已配置的 MCPTT 组取配置，要求该组已在所有相关 MCPTT 用户的 profile 里；若拟重组用户中有**本属 IWF**的，也要把同一来源组配在 IWF。用户本属哪个系统不是说已加入新组；组由谁托管，也不是 Step 9 实际执行的组归属。专用来源组有一个配置标记，这里只回指 TS 23.280，不补它的字段或编码。[§10.3.8.1，印刷页 84–85（PDF 第 85–86 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=85)；[§2 [5]，印刷页 11（PDF 第 12 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=12)。

## MCPTT 系统发起：实际重组组由 MCPTT server 托管

示例中 client 2、3 已注册 MCPTT 业务；它们与 IWF 都预先配好来源组并收到相关安全信息。client 1 已获授权并知道合适的来源组。Step 1 的获授权用户给出名单（示例为 client 2、3 对应用户和一个或多个 IWF 用户）、实际重组 ID 和来源组 ID。Step 2 是 client 1→server 的请求，本段明确它带用户名单；Step 3 server 还要检查发起权限。不把预先获授权、请求发出或 IWF 响应视作同一次验权已完成。[§10.3.8.2.1 前提与 Figure 10.3.8.2.1-1，印刷页 85–86（PDF 第 86–87 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=86)。

- **4a/4b**：server 分别向示例 client 2、3 发重组请求；各客户端通知自己的用户。正文第 5 步指回 4a/4b，图把客户端本地通知标为 **5a/5b**。**6a/6b** 是客户端可以回的确认，不针对组播发送的重组请求。通知动作、确认发出和 server 实际收到确认分别取证。
- **7/8**：server→IWF 发 IWF 请求，IWF→server 回 IWF 应答。这两条不是客户端的 6a/6b。**9** 的正文写 server 执行组归属（affiliate），把被重组的 MCPTT 客户端**和 IWF**归属进实际新组；图框只写 MCPTT 客户端。不把网关归属当成每个 IWF 用户已确认或已经入组。**10** 是 server 给发起 client 1 的另一条应答；送出、实收与前面的归属分别核。

[Figure 10.3.8.2.1-1 与步骤 4–10，印刷页 86（PDF 第 87 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=87)。

## IWF 发起：实际重组组由 IWF 托管

示例只画一个接收 client，不限实际只能有一个。client 已注册 MCPTT 业务，来源组在它和 IWF 上都已预配；本分支前提写明 **MCPTT client** 收到相关安全信息，不据此判 IWF 无需安全处理。**1** 是 IWF→server 的 IWF 请求，名单只列要重组且**本属 MCPTT 系统**的用户。它不是新组的全员名单，也不排除该组另有本属 IWF 的用户。**2** server→client 请求，**3** 由客户端通知其用户，**4** client→server 可以确认，也不是对组播请求回确认。**5** server→IWF：图简写“Preconfigured regroup response”，正文指的是 **IWF pre-configured regroup response**，不是客户端 4 的同一消息。本分支没有前一流程的 Step 3 验权或 Step 9 归属步骤的同样表述，不据此判免验权或不归属，也不补对称步骤。[§10.3.8.2.2 与 Figure 10.3.8.2.2-1，印刷页 87（PDF 第 88 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=88)。

## 两张 IWF 表只用在跨网关这几条消息

| 核对的消息 | 看哪张表 | 要区分的内容 |
| --- | --- | --- |
| MCPTT 发起 7：server→IWF；IWF 发起 1：IWF→server | **10.3.2.14-1** | 请求者 MCPTT ID、实际重组组 ID、来源组 ID 各 M。两个列表虽各标 O，注要求**有且只有一个**：本流程用用户 MCPTT ID list，不是组成组 MCPTT group ID list。 |
| MCPTT 发起 8：IWF→server；IWF 发起 5：server→IWF | **10.3.2.15-1** | 请求者 MCPTT ID、实际重组组 ID、Result 各 M。表没给逐用户状态、来源组、结果码或成员确认清单。 |

单查一条已识别方向和类型的消息就可读自己的表，不要求先有对向消息；说两条相配才核同一次重组。表不套原生客户端的请求、可选确认或给 MCPTT 发起者的 Step 10。只见 IWF 应答发出或对端实收，都不证明所有终端已经确认、谁已实际归属或通话已建立。图示 6/4 在 IWF 最终消息之前，不由此建立等待全员、超时或结果合并算法。[表 10.3.2.14-1、10.3.2.15-1，印刷页 39（PDF 第 40 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=40)；[两流程，印刷页 86–87（PDF 第 87–88 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=87)。

两流程都在后续组呼建立**之前**。其 NOTE 1 允许 MCPTT 客户端与本属 IWF 的用户同时参与多个用户与组重组；不要把[组成组重组](preconfigured-regroup.md)的冲突处理默套成用户只能参加一个。完成后 NOTE 2 说重组保持，直到各自的显式取消：MCPTT 发起回指 [§10.3.8.3.1](preconfigured-user-regroup-cancellation.md#mcptt-系统发起取消)，IWF 发起回指 [§10.3.8.3.2](preconfigured-user-regroup-cancellation.md#iwf-发起取消)。通话结束不当取消；这里不展开取消步骤、SIP、话权或实际媒体。[两流程及 NOTE 1/2，印刷页 85–87（PDF 第 86–88 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=86)。
