# MCVideo 私呼释放：客户端 BYE 与媒体停止、资源回收

TS24.281 V19.3.0，已经建立的普通在网、带 transmission control、单一直接 MCVideo ID 按需私呼。双方不使用预建立会话；不含功能别名、FTA、组呼、远程/ambient、无TC和离网。

本私呼不在紧急或迫近危险流程；没有未决的优先级升级/取消、紧急告警或其状态处置。本页不把取消尚未接受的 INVITE 与释放已建立会话混为一事。

每条规则独立继承本主题条件，再叠加自身 conditions；涉及24.581时仅指实际核读的V19.2.0，不声称与24.281 V19.3.0同版或完整互操作已验证。

## 客户端发BYE与两次媒体交互

适用条件：MCVideo用户要求释放该按需私呼，进入§10.2.4.1.1.1调用的§6.2.5.1；收到响应分支只指本BYE的200。

客户端先与媒体平面交互，再生成BYE；Request-URI使用要释放的MCVideo session identity，并向MCVideo server发送。收到该BYE的200后再次与媒体平面交互。会话标识不是重新指定被叫用户ID，也不把200(INVITE)替代此完成事件。

- 该段未给BYE失败、超时、重传或并发释放的完整算法，仍依赖TS24.229；不补固定Reason/Warning。
- 24.281两次媒体交互没有在本段逐字标成step1/step2；它们与24.581的两阶段接口分别列证，不凭编号猜映射。

依据：§10.2.4.1.1.1;6.2.5.1，印刷页 63、352。

## 收到BYE只确认对应事务

适用条件：客户端收到该私呼会话的SIP BYE；由§10.2.4.1.1.2或服务器发起释放的§10.2.5.2进入§6.2.6。

客户端与媒体平面交互，然后向MCVideo server发送BYE的200。此响应确认这一BYE事务，不能单独证明其他信令段的响应和资源回收也已完成。

- 本段只列一次交互及200发送；不额外插入应用层二次确认或为全部角色统一定义成功时刻。

依据：§10.2.4.1.1.2;10.2.5.2;6.2.6，印刷页 64、352、353。

## 第一阶段停止控制与RTP

适用条件：TS24.581 V19.2.0的participant正在释放本通话，进入call release step1；释放可由participant或transmission control server发起。

step1停止发送transmission control和reception control消息，客户端停止发送和接收RTP。用户平面可以发起step1；这一步本身不是所有状态机和资源已经销毁的证据。

- 这是整通话释放的两阶段规则，不重写单一Transmission End或Media Reception End处理；停止某个源不自动等于释放通话。

依据：§24.581 V19.2.0:6.2.2，印刷页 34。

## 第二阶段由信令触发回收

适用条件：TS24.581 V19.2.0中，应用/信令平面已经判定该MCVideo call释放。

step2终止本通话对应的basic transmission及basic reception状态机实例，并释放participant使用的资源。step2总由应用/信令平面发起，不能仅因本地不再发包就自行推断它已经发生。

- 原文此段列的是对应basic实例；general接收控制器的具体转移另见既有participant-reception-control，不把本句改成正文未列的实例清单。
- 24.281只写媒体交互，不在本段定义每种失败事务如何触发step2；本页不提供该缺口的实现算法。

依据：§24.581 V19.2.0:6.2.2，印刷页 34。

## 证据边界

- 仅所列已核入口；交叉引用疑义保留，不构成无歧义完整释放实现。

## 按需继续

- [private-call-client-signalling](private-call-client-signalling.md)
- [private-call-server-release](private-call-server-release.md)
- [participant-transmission-control](participant-transmission-control.md)
- [participant-reception-control](participant-reception-control.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

媒体释放另据 [TS24.581 V19.2.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf) 的上述具体条款；与信令标准分开追溯，不能据此宣称互通已验证。

取消紧急条件不等于 BYE 结束私呼，另见[私呼本人取消：通话、告警与用户状态分开处理](private-emergency-client-cancellation.md)。
