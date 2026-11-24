# 双话权：覆盖话权持有者退场，服务器停哪路语音？

乙在双话权下持有覆盖话权。该呼叫的双话权仲裁 D 处于 `D: Floor Taken`。控制侧话权服务器从面向乙的**话权控制接口**实际收到乙已开始断开本次 MCPTT 呼叫的指示时，D 须处理乙的覆盖媒体并结束双话权实例。本条不以乙发来的 `Floor Release` 为前提；也没把某一条 SIP BYE 或其应答规定为这份内部指示。[TS 24.380 V16.9.0 §6.3.6.3.8，印刷页 100](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=101)

1. **停乙这路。** D 请求 MCPTT 服务器的媒体分发器停止向其他 MCPTT 客户端分发来自乙的 RTP。D 提出停转请求，不能凭这项记录确认分发器已执行。
2. **发 `Floor Idle`。** 发送对象是本场呼叫中的非控制 MCPTT 功能（NCF），以及接收乙这路 RTP、且由控制 MCPTT 功能（CF）控制的话权参与者。后者不要求只听乙。消息的 `Floor Indicator` 中 G 位设为 1（Dual Floor），消息序列号加 1。广播组呼、系统呼叫、紧急呼叫、迫近危险呼叫或临时组会话，还要在 `Floor Indicator` 中带上相应指示。
3. **结束 D。** 释放为双话权操作预留的媒体面资源，包括 D 实例和该状态机关联的运行中计时器。D 进入 `Start-stop`。这里的 G 位是消息字段，不是一般话权仲裁 G 的状态。

这条程序没有要求停止一般话权的 RTP，也没有规定 G 要切到哪个状态。不能从 D 退出或发出这份 Idle 判定整组空闲、整场呼叫已释放、NCF 已转发或终端已收到。若实际消息已到终端，还要按[终端收件前的许可和覆盖标记](on-network-dual-floor-client-idle.md)另判。

若退场的是[普通单话权的持有者](on-network-holder-departure.md)，查一般仲裁和逐参与者接口。若覆盖者没退场，只发 `Floor Release`，或 D 实收 `Terminate`，查[双话权交接和释放的不同入口](on-network-dual-floor-handover.md)。计时器到期则按[双话权 T11/T12 的分支](on-network-dual-floor-timeouts.md)核对。
