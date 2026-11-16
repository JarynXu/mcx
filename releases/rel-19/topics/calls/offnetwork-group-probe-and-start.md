# 离网MCPTT组呼：先探测，已有则加入、超时则发起

## 适用范围

- 仅TS24.379 V19.4.0 §10.2普通离网MCPTT组呼基本呼叫控制；排除广播、紧急/迫近危险变化、并发呼叫合并、私呼和在网SIP。每组ID独立状态机。
- 假定已具备该组的合法使用条件、可用承载、组播地址及所需配置；本主题不核ProSe发现/授权/安全，也不以GROUP CALL PROBE当作无线设备发现。
- 呼叫类型控制由原文明示的独立状态机承担；本范围限普通类型且不发生类型变更。媒体/离网话权仅核调用边界，不引入在网服务器仲裁，不宣称获准发声或端到端声音送达。

## 离网载体与基本边界

适用主体：MCPTT client / UE。

适用条件：离网组呼基本控制；参与已配置组的呼叫

MONP整个消息作为UDP payload，发到组播IP、UDP8809、TTL255；在该组播IP和端口接收的UDP作为MONP处理。本版只用speech，一个会话含一个media-floor control entity，整个呼叫SDP不变、媒体流不能修改；并发呼叫数受UE MaxCallN4限制。

计时边界：IP TTL=255不是计时器。

- 不提供ProSe发现、安全或完整SDP实现；TS24.483的相关配置字段和默认值未核。
- 不使用INVITE/200/BYE替代MONP。

依据：3GPP TS24.379 V19.4.0 §10.2.1.1.1/.2;10.2.2.1/.2，印刷页 381、382。

## 探测窗口与重发

适用主体：MCPTT client / UE。

适用条件：S1发起；或S2等待；用户发起指定组呼；或TFG3到期

S1保存组ID、创建call-type状态机并发送该组PROBE，进入S2。S2中TFG3到期重发保存组ID的PROBE、重启TFG3并留S2；不是每次重发重新开始整个TFG1等待，也没有本条重发次数上限。

计时边界：初发同时启动TFG3与TFG1；TFG3到期只重启TFG3。TFG1默认150ms，TFG3默认40ms，均可配置；TFG3依赖D2D特性。

- 默认值不是对所有UE固定值；配置缺失/坏值处理未核。
- 未收到回应不等于附近不存在另一呼叫。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.2.1/.2;B.3.1.1 Table B.3.1.1-1，印刷页 385、711。

## 等待到期后发起呼叫

适用主体：MCPTT client / UE。

适用条件：S2；TFG1到期，未转入已有公告接收路径

客户端创建并保存SDP、均匀随机0–65535的call identifier、refresh interval、自身originator ID和当前UTC call start time；公告使用保存的呼叫和call-type信息，Confirm mode IE为may。发送公告后建立媒体、以originating floor participant调用24.380 §7.2，启动计时并进入S3。注释将本版refresh interval固定为10秒。S3不是等齐所有组员确认之后才成立。

计时边界：停运行的TFG3；启动TFG6和TFG2。

- 随机标识不等于全网唯一保证；合并冲突另有过程未覆盖。
- 24.380调用不证明已核其内部发声许可。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.3.1，印刷页 386。

## 探测中收到已有呼叫

适用主体：MCPTT client / UE。

适用条件：S2；收到MCPTT group ID匹配保存组ID的ANNOUNCEMENT

保存收到的SDP、call identifier、originating user ID、refresh interval和Call start time；按该SDP建立媒体并以terminating floor participant调用24.380 §7.2，然后进入S3。这个S2入口没有S1入口的用户确认分支，也未要求发送GROUP CALL ACCEPT。

计时边界：停TFG3及TFG1；启动TFG6与TFG2。

- 未列ACCEPT不等于任意状态都不回应确认。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.3.2，印刷页 386、387。

## 证据边界

- 不是完整离网状态机、媒体发送成功或全员参与证明。

## 按需继续

- [离网MCPTT组呼：用户接受、确认消息与周期公告](offnetwork-group-acceptance-and-announcement.md)
- [离网MCPTT组呼：本端退出、忽略窗口与最大时长](offnetwork-group-local-leave.md)
- [组呼建立门槛：归属、required应答与最少人数](group-acknowledged-start.md)

[3GPP TS24.379 V19.4.0 / ETSI TS124379 V19.4.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)；仅所列版本和条款。
