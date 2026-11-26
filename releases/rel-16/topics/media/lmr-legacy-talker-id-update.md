# 旧式 LMR 互通组呼：为何先看到 IWF 的 ID，稍后才看到电台发话者？

旧式常规 FM 电台发起预安排互通组呼，开场时不知道电台发话者的 ID。例中的 IWF 在建呼请求中先用自身预配置的 MCPTT ID，MCPTT 终端收到的首轮 Floor Taken 也带这个 ID。媒体已开始传送，IWF 才在同一次发言中得知电台发话者的 ID。后续通知更新的是**当前话权上的发话者标识**。这次更新不要求放掉话权，也不是一次新的话权授予。[TS 23.283 V16.8.0，Rel-16 Stage 2，§10.13.3，印刷页 153（PDF 154）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=154)。

以下两例均以 MCPTT 服务器与 IWF 已从配置或建组获知互通组为前提。例中双方用户已归属该组，MCPTT 客户端已注册，其用户已认证并获准使用该服务，IWF 已配置两侧的组和用户身份映射。组定义在哪一侧，哪一侧控制这场呼叫和管理话权。首轮授予或占用通知见下表，只对应建呼请求带隐式话权请求且无人竞争的示例；不把无人竞争另立为后续 ID 更新的通用前置条件。[§10.13.3.1 前提和步骤 1（印刷页 153–154），步骤 6–7（印刷页 155）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=154)；[§10.13.3.2 前提和步骤 1、5（印刷页 155–156），步骤 6–7（印刷页 157）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=156)。

| 组定义侧 | 媒体建立后，首轮话权消息 | IWF 得知真实发话者后 |
| --- | --- | --- |
| **MCPTT** | MCPTT 服务器在步骤 7 向 IWF 发 IWF Floor Granted；同一步向 MCPTT 侧已归属用户发 Floor Taken，带预配置的 IWF MCPTT ID。步骤 8 有条件向 IWF 另发通知，条件见下。 | 步骤 9 学到 ID；步骤 10 由 IWF 向 MCPTT 服务器发 IWF Talker ID Update，告知正在使用话权的发话者而不释放话权。步骤 11 由服务器向已归属 MCPTT 用户发带新 ID 的 Floor Taken。步骤 12 是有条件、向 IWF 的另一支。见[图 10.13.3.1-1（印刷页 154，PDF 155）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=155)及[步骤 6–12（印刷页 155，PDF 156）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=156)。 |
| **LMR** | 在步骤 6，IWF 按已归属的 MCPTT 用户逐人向 MCPTT 服务器发 IWF Floor Taken。步骤 7 由服务器向目标用户发带预配置 IWF MCPTT ID 的 Floor Taken。 | 步骤 8 学到 ID；步骤 9 由 IWF 按已归属的 MCPTT 用户逐人向 MCPTT 服务器发 IWF Floor Taken，说明当前发话者、不释放话权。步骤 10 由服务器向目标 MCPTT 用户发带新 ID 的 Floor Taken。见[图 10.13.3.2-1（印刷页 156，PDF 157）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=157)及[步骤 6–10（印刷页 157，PDF 158）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=158)。 |

在 MCPTT 定义组例中，步骤 8 与 12 各有同一个条件：**组里还有主叫以外已归属的 LMR 用户，且 MCPTT 服务器已收到这些人的逐人归属**。满足条件时，条文写向 IWF 为每位已归属的 LMR 用户分别发 IWF Floor Taken。两次通知分别位于首轮话权和 ID 更新之后，不能合并；这条分支不替代向 MCPTT 用户的步骤 11。只有代表归属、缺逐人记录，或没有主叫以外的已归属 LMR 用户，都不能套用步骤 8、12 的逐人分发。条文的触发条件与计数措辞分开；不另推出必须给主叫补一份或混合归属的数量。[§10.13.3.1 步骤 7–8、11–12（印刷页 155，PDF 156）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=156)。

**LMR 定义组例有一处用词差异。** 步骤 9 的正文与图中 9a/9b 都写 IWF Floor Taken；步骤 10 的正文却用 IWF Talker ID Update 指称新 ID 的来源。保留两处名称：本例说明 IWF 的逐人通知和服务器向目标用户转发新 ID，不据此判定两个名称是同一种线上报文，不添加一条独立的 Update，也不搬用 MCPTT 定义组例中服务器向 IWF 发的 Floor Granted。MCPTT 服务器向终端发通知，不改变 LMR 作为控制侧的职责。[§10.13.3.2 图 10.13.3.2-1 和步骤 5（印刷页 156，PDF 157）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=157)；[步骤 8–10（印刷页 157，PDF 158）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=158)。

## 通用信息流表与上述示例分开读

[表 10.5.2.17-1（印刷页 104，PDF 105）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=105)把 IWF Floor Talker ID Update 定义为可在 IWF 与 MCPTT 话权控制服务器之间双向传递的信息流，用来说明**当前已获话权的一方**的发话者 ID 变了。发话方 MCPTT ID 必带（M）。Source identifier 用来识别通信，例如复用中的媒体流；只有媒体复用时才可带，复用时仍标为可选（O）。两个 FM 组呼的更新从 IWF 发向 MCPTT 服务器；不能由表的双向定义给这两个例子加上反向更新。[表 10.5.2.10-1（印刷页 102，PDF 103）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=103)另列 IWF Floor Taken，表中有可选的确认请求字段。不能把这个字段抄到 Update 表，或凭步骤 9 的名称判定本次要求回执。

## 排查时看哪一段记录？

对照同一组、同一次媒体传送的记录：建呼和首轮通知中的 IWF 预配置 ID，随后 IWF **实际获知**的电台 ID，IWF 发给服务器的消息，再到服务器发给目标终端的 Floor Taken。开场看到 IWF ID 或收到语音，不说明 IWF 已知真实发话者。后段发出通知也不说明终端已收到、显示或播放；两例的注写本场其他话权参与者收到通知，以获知文中所谓新获话权者的身份。对应步骤没有再发授予；注也不能代替本次排查的实收证据。

标准未规定 IWF 如何取得电台 ID。两例的注还说，有的旧式系统在呼叫结束时才有 ID，这不是一条呼叫结束后补发更新的程序。§10.13.3 允许在本文其他已描述的 MCPTT 媒体传送中使用此机制，没有要求每场都更新，也未规定 SIP/RTCP 线上编码、媒体是否无断点或终端如何呈现。[§10.13.3（印刷页 153，PDF 154）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=154)；[§10.13.3.1 注 6、7（印刷页 155，PDF 156）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=156)；[§10.13.3.2 注 4、5（印刷页 157，PDF 158）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=158)。

若实际只查[预安排互通组呼的初始建呼](../calls/lmr-interworking-prearranged-group-setup.md)，按发起方和组定义侧看，不能从建呼确认推出稍后已学到 ID。若已有组呼、参与者已归属、话权起初空闲，有实际话权请求，查[最终仲裁与本地筛选](lmr-interworking-group-floor-arbitration.md)。若同一互通组呼仍在进行、MCPTT 服务器和 IWF 已知该组、IWF 已配置两侧组和用户映射，且参与侧实际成功归属同一组，再按组定义侧分。MCPTT 定义组的首位 LMR 用户可由 IWF 代表归属或逐人转达；同组后续 LMR 用户须由 IWF 实际逐人转达本人的归属，只在 LMR 本地归属或只由 IWF 代表归属不触发该后续跨 IWF 流程。LMR 定义组看新归属的 MCPTT 用户，首位和后续都适用，不套用 LMR 用户逐人转达的条件。符合对应条件，查[互通组迟入](../calls/lmr-interworking-group-late-entry.md)。若原参与者离开覆盖后回到仍在进行的 LMR 定义聊天组，查[回覆盖的媒体恢复](../calls/lmr-chat-return-to-coverage.md)。
