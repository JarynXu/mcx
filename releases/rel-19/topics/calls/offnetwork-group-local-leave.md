# 离网MCPTT组呼：本端退出、忽略窗口与最大时长

## 适用范围

- 仅TS24.379 V19.4.0 §10.2普通离网MCPTT组呼基本呼叫控制；排除广播、紧急/迫近危险变化、并发呼叫合并、私呼和在网SIP。每组ID独立状态机。
- 假定已具备该组的合法使用条件、可用承载、组播地址及所需配置；本主题不核ProSe发现/授权/安全，也不以GROUP CALL PROBE当作无线设备发现。
- 呼叫类型控制由原文明示的独立状态机承担；本范围限普通类型且不发生类型变更。媒体/离网话权仅核调用边界，不引入在网服务器仲裁，不宣称获准发声或端到端声音送达。

## 最大时长按已过时间扣减

适用主体：MCPTT client / UE。

适用条件：启用TFG6的建呼/加入路径；或S3；按入口计算TFG6；或TFG6到期

TFG6按从呼叫开始已过的时间扣减，而非每位后来加入者重新获得完整X。S3到期时释放媒体、调用24.380 §7.2.3.9.2停止话权、停运行的TFG2、启TFG5并进S6。

计时边界：TFG6=X−(Y−Z)秒；X为组OffNetwork/MaxDuration，Y为当前Unix UTC秒（不数闰秒），Z为触发计算公告的start time；没有此公告时用已存start time。

- 不编造MaxDuration默认；24.483准确配置表未核。
- 负剩余时长、时钟偏差和UTC回拨规则未在这些段落给出。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.1.2;10.2.2.4.5.9，印刷页 384、385、392、393。

## 本端退出不代表全组结束

适用主体：MCPTT client / UE。

适用条件：S3、S4或S5；用户要求release该组呼

释放已建立媒体（如有），调用24.380 §7.2.3.9.2停止话权，停相关计时并进入S6。条款是本端退出和忽略公告，不列向全组发结束消息，也不能用本端动作证明其他UE已退出。

计时边界：停运行的TFG4、TFG2、TFG6；启动TFG5。

- 不把此release改写为SIP BYE，也不把停止话权helper当已核全部离网话权状态转换。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.5.1，印刷页 390。

## 忽略窗口与清除状态

适用主体：MCPTT client / UE。

适用条件：S6；收到组ID匹配本状态机保存组ID的ANNOUNCEMENT；或TFG5到期

收到组ID匹配的公告时，更新保存的SDP、call identifier、originating user ID、refresh interval及Call start time，停止并重新启动TFG5，仍留S6。因此30秒不是自用户离开起绝对清理上限。TFG5到期释放保存的SDP、call identifier、originating user ID、refresh interval、group ID及Call start time，销毁call-type状态机并回S1；不以本端清理证明无线范围中该组呼结束。

计时边界：匹配公告停止并重新启动TFG5；到期清理。

- .5.2入口要求组ID匹配，未要求call identifier相同；不能复制周期公告的完整匹配表当作该段原文。
- S6主动重新加入的.5.3不在本主题展开。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.5.2/.4;B.3.1.1，印刷页 390、391、711。

## 探测期间取消

适用主体：MCPTT client / UE。

适用条件：S2之后的S7；S2用户release；之后S7收到匹配组公告或TFG1到期

S2尚在探测时用户退出只停重发、进S7，不走已有公告的S6释放分支。S7若收到匹配组公告，保存SDP、call ID、originator、refresh及start time，转S6；若TFG1先到期则释放组ID、销毁call-type状态机、回S1。

计时边界：S2取消停TFG3但未停TFG1；S7收到公告停TFG1启TFG5；TFG1到期回S1。

- 不把S7等待理解为仍在参与媒体；S7再次主动发起的.5.6未展开。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.5.5/.7/.8，印刷页 391、392。

## 证据边界

- 不是完整离网状态机、媒体发送成功或全员参与证明。

## 按需继续

- [离网MCPTT组呼：先探测，已有则加入、超时则发起](offnetwork-group-probe-and-start.md)
- [离网MCPTT组呼：用户接受、确认消息与周期公告](offnetwork-group-acceptance-and-announcement.md)
- [组呼参与者退出：BYE、REFER与全组释放判断](group-participant-leave.md)

[3GPP TS24.379 V19.4.0 / ETSI TS124379 V19.4.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)；仅所列版本和条款。
