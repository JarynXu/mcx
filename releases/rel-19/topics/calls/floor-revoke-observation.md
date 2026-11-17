# 撤销传递：服务端宽限、终端停止请求与交接证据

## 适用范围

- 限在网普通组呼叫：非广播、非ambient listening、非紧急/迫近危险、非system/temporary group；不含离网、dual floor、multi-talker或audio cut-in。
- 请求者同时协商queueing和mc_priority，最大许可不是receive only，显式Floor Request携带priority；有效优先级由服务端判定，不由数字大小自行推定。
- 仅追踪有效优先级为pre-emptive、当前持有人非pre-emptive、队列无其他pre-emptive请求，并由本地策略选择撤销旧持有人的分支。不把override without revoke混入本链。
- 规范状态机动作与实际终端/网络观察分开：发送通知、转发请求、排到队首均不证明终端已停止、已授予新持有人或首个媒体包已成功。

## 仲裁者与服务端接口各自计时

适用主体：仲裁者及旧持有人对应的服务端接口。

适用条件：仲裁者进入G: pending Floor Revoke；接口原在U: permitted。

仲裁者发Revoke并启动T3；接口转发Revoke，若含Track Info则保存，再进入自己的pending Floor Revoke并启动T8。两个计时器不属于同一状态机。

- 发送动作不是远端收到证据；不自行补普通呼叫必含Floor Indicator的义务。

依据：3GPP TS24.380 V19.1.0 §6.3.4.5.2;6.3.5.5.5;6.3.5.6.1;6.3.5.6.2，印刷页 71、95、97。

## T8重传与实现选择

适用主体：旧持有人对应的服务端接口 U: pending Floor Revoke。

适用条件：T8到期。

重传Revoke时保留前次Rejection Cause和Floor Indicator，重新启动T8并留在原状态。重传次数及放弃动作由实现选择；断开呼叫只是推荐。

- 不造固定次数、固定截止时间或必断开义务。

依据：3GPP TS24.380 V19.1.0 §6.3.5.6.3，印刷页 97、98。

## 宽限期间仍可能转发媒体

适用主体：接口 U: pending Floor Revoke 与仲裁者 G: pending Floor Revoke。

适用条件：接口收到关联参与者带payload的RTP；仲裁者收到来自permitted participant的RTP指示。

接口仍把RTP送到分发器；仲裁者重启T1并按本地策略要求转发。撤销已发出不等于服务器已停止接受或分发该媒体，更不能证明终端已停。

- 这不赋予已收到Revoke的终端继续发送的许可。T3上限小于T1时的注释不能泛化为所有配置T1均不超时。

依据：3GPP TS24.380 V19.1.0 §6.3.5.6.4;6.3.4.5.3，印刷页 71、98。

## 终端停止请求及G-bit条件

适用主体：旧持有人终端 U: has permission；对应服务端接口 U: pending Floor Revoke。

适用条件：终端实际收到Floor Revoke，且收到的Floor Indicator中G-bit=0；随后接口收到该终端含G-bit=0的Floor Release。

终端必须请求丢弃余下缓存、停止语音转发并通知用户；原因可提示。终端发G-bit=0的Release，可请求Ack，启动T100/C100=1并转pending Release。接口按Ack请求位回应后，把G-bit=0的Release交给仲裁者，仍留pending Floor Revoke。

- Ack为Message Type 4、Source 2，若Release含Track Info则回带。不能把Ack解释成下一位已获话权。
- 终端义务是向媒体组件提出停止/丢弃请求；仅靠服务器Revoke日志不能验收这些动作已完成。
- 此处与旧floor-participant-queue-release只作跨角色衔接，不另扩终端释放重试全流程。
- 收到的Floor Indicator存在且G-bit=0是本分支的额外前提；不能由普通组呼推定该字段存在，也不对缺字段补默认0。

依据：3GPP TS24.380 V19.1.0 §6.2.4.5.4;6.3.5.6.5，印刷页 45、98。

## 接口退出等待的证据

适用主体：旧持有人对应的服务端接口 U: pending Floor Revoke。

适用条件：从仲裁逻辑实际收到Floor Idle或Floor Taken。

接口转发对应消息，再进入not permitted and Floor Idle或not permitted and Floor Taken；请求Ack是may，Ack处理和缺Ack动作由实现选择。这是接口状态证据，不是终端停止或新持有人首包成功证据。

- 不自行补这两条未写出的stop T8动作。
- 不从两条NOTE推导T3/T1的唯一组合条件。T3到期的6.3.4.5.5在multi条件外列Release Multi Talker，且后续依赖当前talker列表；仍保留疑点，不据此构建已验证单话权超时交接闭环。

依据：3GPP TS24.380 V19.1.0 §6.3.5.6.6;6.3.5.6.7，印刷页 98、99。

## 原文差异与适用限制

§6.3.4.5.5，印刷页 72：multi条件与后续Release Multi Talker及列表动作未完全同层限定；不另造单话权超时流程。

## 证据边界

- 不声称复杂话权全部覆盖；dual floor、multi-talker、audio cut-in须另核。

## 按需继续

- [优先请求：何时触发撤销，为什么队首仍不等于获权](floor-preemption-decision.md)
- [服务器授予后的媒体计时：T20 重传、T1 静默与 T2 超时撤销](floor-server-media-timers.md)

[3GPP TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅所列版本和条款。

## 多talker独立范围

multi-talker的独立范围另见multi-talker-release-and-revoke；本页单话权优先撤销条件不直接迁移。新主题区分未满额允许名单转交与仲裁处理；不因此推定完整准入、队列后续授予或端到端媒体证据。

- [多talker逐人退出与满额撤销](multi-talker-release-and-revoke.md)
