# 离网MCPTT组呼：用户接受、确认消息与周期公告

## 适用范围

- 仅TS24.379 V19.4.0 §10.2普通离网MCPTT组呼基本呼叫控制；排除广播、紧急/迫近危险变化、并发呼叫合并、私呼和在网SIP。每组ID独立状态机。
- 假定已具备该组的合法使用条件、可用承载、组播地址及所需配置；本主题不核ProSe发现/授权/安全，也不以GROUP CALL PROBE当作无线设备发现。
- 呼叫类型控制由原文明示的独立状态机承担；本范围限普通类型且不发生类型变更。媒体/离网话权仅核调用边界，不引入在网服务器仲裁，不宣称获准发声或端到端声音送达。

## 用户应答与Confirm mode分别判断

适用主体：MCPTT client / UE。

适用条件：S1；收到ANNOUNCEMENT，所含组ID不匹配其他呼叫控制状态机已保存的组ID

保存组ID及公告的SDP、呼叫ID、originator、refresh interval及Call start time，建立call-type状态机。UE配置要求用户应答时通知用户：公告有Confirm mode则进S5，否则S4。配置不要求应答时直接建立媒体、启动terminating floor participant；仅公告含Confirm mode时生成并发送ACCEPT，再启动计时进入S3。因此本地用户应答要求与对端Confirm mode是两个判断。

计时边界：需用户应答时启动TFG4；TFG4默认30秒，可配置，最大60秒。自动加入时启动TFG6、TFG2。

- 未核UE“需要应答”配置字段、缺省值及配置管理；不能假定缺字段自动接听。
- 本段没有把收到ANNOUNCEMENT本身等同于用户接受。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.3.3;B.3.1.1，印刷页 387、388、711。

## 本端接受与接受情况观察

适用主体：MCPTT client / UE。

适用条件：分别为S4/S5，或S3；用户接受；或S3收到组ID匹配的GROUP CALL ACCEPT

S4/S5用户接受均建立媒体、启动terminating floor participant、停等待计时并进入S3；S5还发ACCEPT，填写保存的call identifier、自己的Sending user ID、当前call type及组ID，S4路径不列该发送。S3收到组ID匹配的ACCEPT时可以提示用户接受情况，但仍留S3；不是服务器全员确认门槛，也不是媒体已经送达的证明。

计时边界：用户接受停TFG4、启TFG6和TFG2；接收ACCEPT段未列新计时动作。

- 接收ACCEPT这一条守卫只明列组ID匹配；不擅自增加call identifier匹配为原文要求。
- 不推导全部成员列表、去重或已读/已听保证。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.3.4/.5/.6，印刷页 388、389。

## 拒绝或未操作

适用主体：MCPTT client / UE。

适用条件：S4或S5；用户拒绝；或TFG4到期

用户拒绝和等待超时都转S6忽略公告；拒绝入口另明确停止TFG4。这两个基本控制过程没有发送SIP拒绝，也没有GROUP CALL REJECT发送步骤，不能据此生成在网拒绝码。

计时边界：拒绝时停TFG4；两种事件均启动TFG5（默认30秒，可配置）。

- 没有声称完整规范所有拒绝情形都无消息；结论只限这两个入口。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.3.7/.8;B.3.1.1，印刷页 389、711。

## 周期公告与探测响应抑制

适用主体：MCPTT client / UE。

适用条件：S3；TFG2到期；收到组ID匹配PROBE；或收到符合完整相等守卫的周期公告

TFG2到期发送保存呼叫信息的公告，probe response已置true时携Probe response IE，发送后清false、重启周期TFG2并保持S3。收到PROBE且该标志false时停TFG2并换短随机等待、标志置true；已true不再按此分支重置。收到公告只有组ID、start time、last type-change time、last changing user、call identifier、call type均等于保存值，且本地标志false或本地true并收到Probe response IE，才停/重启周期TFG2、必要时清标志并留S3。

计时边界：周期TFG2=refresh interval×(2/3+2X/3)，X均匀0至1。响应PROBE的TFG2=X/12秒。

- 发送周期公告step2引用10.2.2.1.1.1，实际载体标题在10.2.1.1.1；保留错引，不宣称引用已一致。
- 本组接收不满足全套相等条件不在此补行为；并呼合并另行处理。

依据：3GPP TS24.379 V19.4.0 §10.2.2.4.1.1.1/.2;10.2.2.4.2.3;10.2.2.4.4.1/.2，印刷页 384、385、389、390。

## 原文差异与未核边界

10.2.2.4.4.1 step2 p389–390：周期公告发送的运输交叉引用多一层.2。原文10.2.2.1.1.1与实际10.2.1.1.1并列，未静默修正。

10.2.2.4.2.3;4.4.1/.2：stored probe response初始化。本页未核出完整初始化契约；只在明确已知true/false条件下说明分支。

## 证据边界

- 不是完整离网状态机、媒体发送成功或全员参与证明。

## 按需继续

- [离网MCPTT组呼：先探测，已有则加入、超时则发起](offnetwork-group-probe-and-start.md)
- [离网MCPTT组呼：本端退出、忽略窗口与最大时长](offnetwork-group-local-leave.md)

[3GPP TS24.379 V19.4.0 / ETSI TS124379 V19.4.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)；仅所列版本和条款。

离网呼叫成功建立后，终接或后来加入者的话权初始化另见[离网话权入口](offnetwork-floor-entry.md)。呼叫应答不能替代本地话权状态；发起者的隐式与显式请求前提仍须分别判断。
