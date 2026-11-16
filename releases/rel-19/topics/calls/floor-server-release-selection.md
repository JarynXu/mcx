# 取消请求与释放现有话权：回到空闲和队首选择的原文边界

TS24.380 V19.1.0 的普通单话权在网组呼，不含广播/system/emergency/imminent-peril/ambient、临时组、抢占、dual floor、multi-talker 或 audio cut-in。

严格区分未获许可者取消排队与获许可者释放；状态属于服务器 G/U 实例，不把客户端 pending Release 直接当服务器状态。

本主题保留 §6.3.4.3.2 对队首选择的异常外层条件，不把它当所有已协商 queueing 情形的完整算法。

## 取消自己的排队请求

适用条件：U: not permitted and Floor Taken 收到该 participant 的 Floor Release；仅描述 §6.3.5.4.5 第二段已协商 queueing 的动作，不裁决与第一段的重叠。

若请求 Ack，回 Floor Ack(type=4,Source=2)，有 Track Info则回带。用 Track Info 最上层 Participant Reference+SSRC 或仅 SSRC 定位，若在 active queue中则移除。向该 participant 发送 Floor Taken，带当前获授者 Audio SSRC、递增的消息序号及请求 Track Info；无 privacy request 时带当前用户 ID，可带功能别名；普通非广播可带 Permission to Request=1，可要求 Ack。接口仍 not permitted and Floor Taken，当前发言者不因别人取消队列就释放。

依据：§6.3.5.4.5 second paragraph，印刷页 90。

边界：前一段条件是未协商queueing OR含mc_priority，因此可与本段同时成立；不宣称仅会发送一次 Taken，也不把该OR改成AND。原文没有要求本动作广播更新其余所有排队者位置。

## 已获许可者释放

适用条件：对应接口 U: permitted 收到当前获授 participant 的 Floor Release，且没有 overriding/overridden-without-revoke 指示。

请求 Ack 时先回 Ack(type=4,Source=2)，回带请求 Track Info；把 Release 交给 general 仲裁时将 Ack-required 位清0（若尚未清）。接口这一分支暂留 U: permitted，不能把回 Ack 就写成已转 no-permission。general G: Floor Taken 接到 Release 后停止转发该发送者的 RTP，停止其运行中的 T2/T20，普通非multi-talker进入 G: Floor Idle 的入口程序。

依据：§6.3.5.5.3 steps1,4;6.3.4.4.6 steps1–4，印刷页 94、65。

边界：T1/T2/T20 的其他开始、重发和到期动作由关联主题负责。这里没有将接口回Ack解释为全通话结束或下一位已获授。

## 有界空闲入口

适用条件：从非 Start-stop 进入 G: Floor Idle；没有任何客户端协商 queueing，且不存在 §6.3.6 dual-floor 状态机；active floor request queue 为空。

按 §6.3.4.3.2 第一段先清除关联 general 仲裁实例保存的 Track Info，然后向所有 floor participants 发 Floor Idle，消息序号加1，启动 T7并C7=1，启动 T4，设置 G: Floor Idle。只有在该段外层条件成立时，本条才给出完整动作；不能抹去“没有任何客户端协商queueing”条件。

依据：§6.3.4.3.2 first paragraph steps1–2，印刷页 60。

边界：§6.3.4.2.2 从 Start-stop 指向本入口，而本入口第一段排除 Start-stop，也是未补齐的初始化边界。T4/T7到期和固定计时值不在本条。

## 队首选择与衔接缺口

适用条件：同样从非 Start-stop 进入 G: Floor Idle；按原文没有任何客户端协商queueing，且无dual-floor状态机；但 active queue 非空。该组合仅作为条文陈述，不假设在普通协商排队流程中必可达。

第一段 step3 从 active queue 顶部选一项并将其移除；有 Track Info则保存并关联general实例，随后针对该 participant 进入 G: Floor Taken 的授予程序。外层却限定无人协商queueing，与本章通常在已协商queueing时入队的路径存在衔接缺口。本页保留队首选择文字，但不据其给出“任何释放都会立即授予已协商队列下一人”的结论。

依据：§6.3.4.3.2 first paragraph opening and step3;6.3.5.4.4 step8，印刷页 60、88、89。

边界：不反转 no；队首选择后授予/等待媒体依关联主题，客户端queued收到Granted仍需T132用户确认。

## 证据边界

- 仅按各页的状态与条件衔接；撤销发出不证明终端已停，排到队首不证明新 Granted，下一持有人首包成功也须独立观察。
- 队首出队的外层条件和多处OR重叠未被纠正，不能把本文称为完整无歧义仲裁实现。
- 本页不覆盖主动清空其他用户队列的权限、Revoke/T3、临时组和非控制角色切换；有限抢占撤销见关联主题，队列入口守卫及 T3 疑点仍不因此消失。
- 这里的floor释放不同于SIP通话释放，成员/归属/密钥也不会仅凭这些消息自动删除。

## 按需继续

- [优先请求与撤销的有限分支](floor-preemption-decision.md)
- [撤销传递、宽限与停止证据](floor-revoke-observation.md)
- [floor-server-queue-admission](floor-server-queue-admission.md)
- [floor-server-idle-request](floor-server-idle-request.md)
- [floor-participant-queue-release](floor-participant-queue-release.md)
- [floor-state-ownership](floor-state-ownership.md)

[ETSI 官方 TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)，印刷页60、65、88、89、90、94；仅本版本。


## 原文衔接问题

- §6.3.5.4.4：首拒绝条件为not queueing OR not mc_priority，后续处理入口却为queueing OR priority OR both，且允许未协商priority的default输入。保留重叠，不改AND。
- §6.3.5.4.4 steps4,8–9：已有同effective-priority请求step4回复后未写停止，后续step8允许更新已有请求位置且step9另有队满拒绝；本页不裁决并发/重复处理顺序。
- §6.3.5.4.5：第一段为未协商queueing OR含mc_priority，第二段为已协商queueing，两段可重叠；本页仅逐段报告，不补else-if或消除重复发送。
- §6.3.4.3.2：第一段外层写no MCPTT client negotiated queueing，并排除Start-stop，内却含active queue非空出队；本页不将该段扩大为普通已协商队列的完整释放选择。

[媒体静默与超时撤销](floor-server-media-timers.md)：仅按该页版本和适用条件衔接。
