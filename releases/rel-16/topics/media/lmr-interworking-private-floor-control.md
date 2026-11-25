# MCPTT–LMR 私呼中打断发言：谁决定，谁转告？

先确认这通私呼由哪一侧控制话权。MCPTT 客户端收到服务器转来的拒绝，不表示服务器自己拒绝了请求。这里讨论一名 MCPTT 用户和一名陆地移动无线电（LMR）用户之间已建立、启用话权控制的私呼，两侧经互通功能（IWF）连接。依据为 3GPP TS 23.283 V16.8.0（Release 16，Stage 2）。

私呼中，由 IWF 或 MCPTT 服务器承担控制话权的角色，仲裁这两名用户的请求。未承担控制角色的一侧须把自己服务的参与者发出的**所有话权控制请求**转给控制方，不先筛选。控制角色可以按私呼的发起系统分配，也可以采用其他方式。[§10.5.3 的私呼段及注，印刷页 104](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=105)。

## LMR 控制：客户端放权后，打断 LMR 发言的请求在本例被拒

开场由 LMR 系统经 IWF 控制话权，MCPTT 客户端 1 持有话权。客户端 1 结束这一轮发言后向 MCPTT 服务器发 Floor Release，服务器通知 IWF。IWF 先向服务器报告话权空闲（Idle），后报告 LMR 用户取得话权（Taken）；服务器分别通知客户端 1。语音从 LMR 用户经 IWF 到客户端 1。图把 7a 标在 IWF 到服务器的箭头上，正文把 7a 放在 LMR 用户到 IWF 的描述中。判断图中可见的转发方向时，按箭头看 IWF → MCPTT 服务器 → 客户端 1，不把两处 7a 当成同一条腿的证据。Floor Release 结束本轮话权，不是私呼挂断。[§10.5.9 前提、图 10.5.9-1 和步骤 1，印刷页 111](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=112)；[步骤 2–7，印刷页 112](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=113)。

客户端 1 想打断正在发言的 LMR 用户时，向服务器发带适当优先级的 Floor Request，服务器转给 IWF。段首把这个例子的拒绝写为 IWF 拒绝；**步骤 11 把裁决和传递分开：LMR 系统拒绝，IWF 把拒绝通知 MCPTT 服务器。** 服务器再把 Floor Rejected 转告客户端 1。这个例子不能用来证明 IWF 在转交之前做了本地筛选，也不能断定某个优先级必被拒；步骤 11 后的注把拒绝理由留在本规范范围外。[§10.5.9 段首和图，印刷页 111](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=112)；[步骤 8–12 及注，印刷页 112](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=113)。

## MCPTT 控制：先给客户端发言，随后在本例允许 LMR 打断

开场话权空闲，由 MCPTT 服务器控制。客户端 1 请求话权后，服务器发 Floor Granted 给客户端 1（步骤 2），也发 IWF Floor Taken 给 IWF（步骤 3），告知 IWF 获权者是客户端 1。注 1 允许步骤 3 在步骤 2 之前或之后，两个通知都在例中。客户端 1 的语音由服务器转发给 IWF。[§10.5.10 前提、图 10.5.10-1，印刷页 112](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=113)；[步骤 1–4 及注 1，印刷页 113](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=114)。

客户端 1 正在发言时，LMR 用户请求打断，IWF 获知后向 MCPTT 服务器发具有足够优先级的 IWF Floor Request。例中服务器根据请求优先级和配置决定允许打断。服务器向原持有者发 Floor Revoked（步骤 8），也向 IWF 发 IWF Floor Granted，把话权授给 LMR 用户（步骤 9）。根据注 2，步骤 9 可以先于或晚于步骤 8，不能把其中任何一个动作当成可省，也不能补出先等撤权确认或原持有者另发 Floor Release 的条件。随后语音由 LMR 用户经 IWF 和服务器送往客户端 1。例中没有给出固定的抢占门槛。[图 10.5.10-1，印刷页 112](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=113)；[步骤 5–10 及注 2，印刷页 113](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=114)。

要查这通电话怎样建立，分别读[自动开始互通私呼](../calls/lmr-interworking-private-auto-setup.md)和[手动开始互通私呼](../calls/lmr-interworking-private-manual-setup.md)；要查结束整场通话和回执，读[互通私呼释放](../calls/lmr-interworking-private-release.md)。[互通组的话权仲裁](lmr-interworking-group-floor-arbitration.md)按组宿主和组侧筛选处理，不套到私呼。[加密互通组呼的转码](lmr-interworking-encrypted-group-transcoding.md)属于组呼媒体处理。这里的消息和语音方向不规定 SIP、RTCP 或 LMR 无线侧报文，也不证明实际终端收到了通知或语音。
