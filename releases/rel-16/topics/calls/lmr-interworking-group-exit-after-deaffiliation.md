# 互通组呼还在进行，有人解除归属后，谁通知他退呼？

先看组定义在哪一侧。**组定义在 LMR 系统**时，互通功能（IWF）经 MCPTT 服务器向刚解除归属的 MCPTT 客户端发退呼请求。**组定义在 MCPTT 系统**时，MCPTT 服务器经 IWF 向刚解除归属的 LMR 用户发退呼请求。两条过程都适用于预安排组呼和聊天组呼，处理的是一名参与者退出，不是整场组呼释放。[3GPP TS 23.283 V16.8.0，Release 16，Stage 2，§10.3.6.1–.2，印刷页 68](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=69)；[§10.3.6.3，印刷页 69](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=70)。

两图的共同前提是：组已有归属的 MCPTT 用户，至少有一名 LMR 用户以 MCPTT ID 表示。本次进行中的通话至少有一名使用 MCPTT 客户端的用户和一名通过 IWF 参加的 LMR 用户。解除归属是图中的起点；图不办理解除归属本身。

## 组定义在 LMR：退出的是 MCPTT 用户

组已定义在 IWF。确认目标 MCPTT 客户端已解除归属后，**IWF → MCPTT 服务器**发 `IWF group call leave request`。服务器以 `group call leave request` 送给该客户端。该客户端上的用户得到退呼通知。

客户端向服务器回 `group call leave response` 并退出本场组呼。服务器再向 IWF 转回 `IWF group call leave response`。客户端回给服务器的是第一段响应，服务器转给 IWF 的是第二段；有第一段记录不能代替检查第二段。图最后记载被移出的是这名 MCPTT 用户的客户端。[§10.3.6.2 的前提，印刷页 68](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=69)；[图 10.3.6.2-1 和步骤 1–7，印刷页 69](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=70)。

## 组定义在 MCPTT：退出的是 LMR 用户

组已定义在组管理服务器（GMS）。已确认刚解除归属的是 IWF 代表的 LMR 用户时，**MCPTT 服务器 → IWF**发 `IWF group call leave request`，请这名 LMR 用户退出。图中没有再向旁边的 MCPTT 客户端发一条退呼请求。

IWF 向 MCPTT 服务器回 `IWF group call leave response` 并退出图示的组呼。结果落在目标用户：**这名由 IWF 代表的 LMR 用户**被移出正在进行的组呼。不能把 IWF 的这份响应当成其他 LMR 用户也退出、整场通话结束，或电台已收到某种无线侧消息的证据。[§10.3.6.3 的前提，印刷页 69](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=70)；[图 10.3.6.3-1 和步骤 1–4，印刷页 70](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=71)。

核对一次退呼时，把已解除归属的记录、针对该用户的退呼请求和两端实际收到的响应对上。单有退呼请求不证明对端已退出。这份 Stage 2 过程也不规定实际 SIP 报文、无线侧转发或媒体资源如何回收。要区分 MCPTT 定义组的代表归属和逐人归属，查[MCPTT 定义组的归属](../groups/mc-hosted-lmr-affiliation.md)。若已经归属成功，问题是怎样进入仍在进行的组呼，查[互通组呼的晚入](lmr-interworking-group-late-entry.md)。
