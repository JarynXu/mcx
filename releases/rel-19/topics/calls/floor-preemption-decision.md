# 优先请求：何时触发撤销，为什么队首仍不等于获权

## 适用范围

- 限在网普通组呼叫：非广播、非ambient listening、非紧急/迫近危险、非system/temporary group；不含离网、dual floor、multi-talker或audio cut-in。
- 请求者同时协商queueing和mc_priority，最大许可不是receive only，显式Floor Request携带priority；有效优先级由服务端判定，不由数字大小自行推定。
- 仅追踪有效优先级为pre-emptive、当前持有人非pre-emptive、队列无其他pre-emptive请求，并由本地策略选择撤销旧持有人的分支。不把override without revoke混入本链。
- 规范状态机动作与实际终端/网络观察分开：发送通知、转发请求、排到队首均不证明终端已停止、已授予新持有人或首个媒体包已成功。

## 有效优先级与本地策略

适用主体：请求者的服务端接口 U: not permitted and Floor Taken。

适用条件：共同范围；收到显式请求。

协商的最大值与请求值取较低者参与有效优先级计算；本地策略可判定撤销或允许并发，故优先级较高不自动等于撤销。本文只选撤销。

- 不覆盖未协商priority、缺priority、receive-only或紧急位的替代分支。

依据：3GPP TS24.380 V19.1.0 §4.1.1.4;6.3.5.4.4 step 1，印刷页 22、86、87。

## 接口转发请求不是授予

适用主体：请求者的服务端接口 U: not permitted and Floor Taken。

适用条件：有效pre-emptive；没有其他pre-emptive排队；旧持有人非pre-emptive。

接口向仲裁者转发并标明抢占请求，仍留在原接口状态；这不是授予。

依据：3GPP TS24.380 V19.1.0 §6.3.5.4.4 step 5，印刷页 88。

## 撤销与移到队首

适用主体：仲裁者 G: Floor Taken。

适用条件：本地策略选择revoke，而非允许双发。

停止运行中的T1/T20，以cause 4进入撤销流程；请求者插入或移到队首，并向已协商queueing的请求者发送位置/优先级，携带请求中已有的Track Info。

- 队首不等于新Granted；不增加原文未列的T2停止动作。

依据：3GPP TS24.380 V19.1.0 §6.3.4.4.7;6.3.4.5.2，印刷页 65、66、71。

## 收到Taken仍保持请求等待

适用主体：请求者终端 U: pending Request。

适用条件：已发pre-emptive请求；随后收到因其他参与者取得话权而发来的Floor Taken。

保持pending Request，而非普通请求的退出分支。按消息Ack请求位回Ack；可提示Taken/呼叫类型；每位新talker的可选T103为should启动。本人不在Granted Users列表时原文要求停T100，不能改成T101。

- 非multi范围不展开I-bit通知；不把Taken当自己的Granted；该条仅适用于仍处于pending Request，不能覆盖已转queued者。

依据：3GPP TS24.380 V19.1.0 §6.2.4.4.11，印刷页 44。

## 释放后的队列交接边界

适用主体：仲裁者 G: pending Floor Revoke。

适用条件：收到先前被Revoke对象的Release，且活动队列非空。

要求媒体分发器停止转发，并停止运行中的T1，再停止T3，然后引用6.3.4.3.2进入G: Idle。不能据此宣称本范围下已完成下一位Granted。

- 6.3.4.3.2包含队首选择的首段外层却写没有客户端协商queueing；本页选择已协商queueing，不静默删外层条件来闭合交接。
- 保留G: Idle与目标条标题G: Floor Idle的原文名称差异。

依据：3GPP TS24.380 V19.1.0 §6.3.4.5.4;6.3.4.3.2，印刷页 60、71、72。

## 原文差异与适用限制

§6.3.5.4.4，印刷页 86：拒绝段not queueing OR not mc_priority与随后queueing OR priority处理段重叠；本文两项均协商，且普通呼叫，避开该重叠，不修原文。

§6.3.4.3.2，印刷页 60：队首选择段的外层no client negotiated queueing限制阻止本页范围宣称下一位授予已闭合。

§6.2.4.4.11，印刷页 44：未在Granted Users中的参与者停T100；原文不是T101。

## 证据边界

- 不声称复杂话权全部覆盖；dual floor、multi-talker、audio cut-in须另核。

## 按需继续

- [撤销传递：服务端宽限、终端停止请求与交接证据](floor-revoke-observation.md)
- [他人持有话权时：普通请求的拒绝、优先级输入与入队](floor-server-queue-admission.md)
- [入会与请求话权：SIP 成功、接收媒体和发送许可分别判断](floor-participant-entry-request.md)

[3GPP TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅所列版本和条款。

## 多talker独立范围

multi-talker的独立范围另见multi-talker-admission-and-media；本页单话权优先撤销条件不直接迁移。新主题区分未满额允许名单转交与仲裁处理；不因此推定完整准入、队列后续授予或端到端媒体证据。

- [多talker容量、授予列表与媒体分发](multi-talker-admission-and-media.md)

若本地策略选择不撤销原持有者，而允许两者同时发送，改读[双话权入口与媒体](dual-floor-entry-and-media.md)。该页有独立共同条件，不能沿用本页的撤销等待链。
