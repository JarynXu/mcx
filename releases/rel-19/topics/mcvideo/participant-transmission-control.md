# 普通在网 MCVideo 发送：入会不等于可发送

TS24.581 V19.2.0，在网且使用 transmission control 的客户端 participant；普通非广播、非 system、非紧急/迫近危险业务。

仅跟踪一个发送者的视频及伴随音频源；不展开多流、抢占/override、远程发送、MBMS/MBS 或离网。

SIP 建立、身份准入、控制通道和所需安全处理已按各自规范满足；这里不把通话接通、组成员身份或媒体可达当作发送许可。

## 入会、隐式请求与重入

适用条件：初始化客户端的发送控制实例；分别判定终接、重入或发起分支。

终接端发送 SIP200 后进入无发送许可态；重入 ongoing call 也进入该态，而且 rejoin ongoing 组呼的 INVITE 不作隐式发送请求。非隐式请求的 chat 发起同样无许可。已协商隐式请求的普通发起则启动 T100、C100=1 并等待授予；早于 SIP200 收到的控制消息先存储，在进入等待态后处理。

依据：§6.2.1;6.2.4.2.2;6.2.4.2.3，印刷页 34、36。

边界：无隐式请求的普通非 chat 发起情形未由本条所列入口完整覆盖；不泛化为所有发起均走同一分支。

## 显式请求和超时

适用条件：发送态为 U: has no permission to transmit；用户要求发送。随后若处于 U: pending request to transmit，按本条重传分支。

向控制服务器发 Transmission Request，启动 T100、C100=1，进入等待态。T100 到期未达 C100 上限则重发、重启计时并加一；达上限则通知超时并回无许可态。请求本身与超时都不授予媒体权限。

依据：§6.2.4.3.2;6.2.4.4.1;6.2.4.4.3;6.2.4.4.4，印刷页 36、37、38。

边界：本主题仅 normal priority；非普通优先级请求必须带 Transmission Priority 且不得超过协商值，但优先级仲裁不在本页。

## 拒绝或排队不是授予

适用条件：U: pending request to transmit 收到 Transmission rejected 或 Queue Position Info。

拒绝时必须通知用户，可显示 Reject Cause，停止 T100 并回无许可态。排队时必须通知已排队，可显示位置/优先级，进入 U: queued transmission；表11.1.1-1 将收到 Queue Position Info 列为 T100 正常停止条件。两种消息若要求 Ack，均返回 Source=0，Message Type 分别为1、5。

依据：§6.2.4.4.2;6.2.4.4.5;11.1.1 Table11.1.1-1，印刷页 37、38、213。

边界：§6.2.4.4.5 步骤本身未列停止 T100，故明确区分表格补充证据；不把排队确认说成授予。

## 查询排队与最终超时

适用条件：U: queued transmission；客户端要求查询位置，或该查询已启动 T102。

查询发 Queue Position Request，启动 T102、C102=1。返回 Info 时按 Ack 位答复、停止运行中的 T102，仍排队；仅消息表示已排队或先前发过查询时，可显示位置/优先级。T102 未达上限则重查并加一；达上限则通知排队超时、发 Transmission End Request、启动 T101 且 C101 加一，进入等待结束态。

依据：§6.2.4.9.2;6.2.4.9.3;6.2.4.9.7;6.2.4.9.8，印刷页 42、43。

边界：上限分支原文为 increment C101，不替换成 initialize C101=1；其先前值在该段没有补充定义。

## 授予、源标识和真正发送

适用条件：等待请求或排队状态收到服务器 Transmission Granted；正常请求或排队两入口分别保留。

要求 Ack 时答 Source=0、Message Type=0；保存获授的 Audio/Video SSRC，直至释放均用于 RTP；未通知过则通知用户。停止入口对应的 T100 或 T102，进入 U: has permission to transmit。仅该状态收到已编码视频或已有缓存时才请求转发到服务器；曾排队者的 NOTE 还要求先取得用户确认，不确认则释放许可。

依据：§6.2.4.4.6;6.2.4.9.9;6.2.4.5.1;6.2.4.5.2，印刷页 38、39、43。

边界：不把缓存存在、客户端首选 SSRC 或 ACK 已发等同于对方已收到媒体。排队用户确认没有在此借用 MCPTT 的 T132。

## 主动结束与有限重传

适用条件：用户在等待授予、持有许可或排队时要求结束；随后处于 U: pending end of transmission。

发 Transmission end request，启动 T101、C101=1 并等待结束；从等待请求退出时另停止 T100。T101 未达上限则重发、重启并加一，达上限回无许可态。收到 End Response 时，要求 Ack 则答 Source=0、Message Type=1；可通知结束，停止 T101，普通非广播业务回无许可态。

依据：§6.2.4.4.7;6.2.4.5.3;6.2.4.9.4;6.2.4.6.2–6.2.4.6.4，印刷页 38、39、40、41、42、43。

边界：本地结束请求步骤没有在文字中逐项重复停止转发/清缓存，不能擅加为该段明示动作。结束发送不等于本普通通话已被 SIP 释放。

## 接收情况通知与服务器结束

适用条件：U: has permission to transmit；收到 Media reception notification 或服务器 Transmission End Request。

前者仅通知其他用户的接收情况，保留发送许可。后者须通知用户许可结束、丢弃剩余 RTP 缓存并停止向服务器转发，发送 End Response，普通非广播业务回无许可态。不能将接收情况通知本身当作停流或挂断命令。

依据：§6.2.4.5.6;6.2.4.5.7，印刷页 40。

边界：服务器何时发结束命令以及无人接收策略依赖 §6.3，本页不反推。Transmission Revoked 的终止/重新排队两分支另留。

## 证据边界

- 服务器仲裁准入、持续时间/容量策略、全部消息编码及 SDP 协商未闭合。
- 未实现状态机；未定义原文未规定的分支优先级或迟到消息策略。
- TS24.281信令建立、完整媒体安全及字段编码另有依赖，本页不证明跨版本完整互操作。
- §6.2.3（印刷页34）增加/删除媒体流对控制程序的影响仍为FFS；单源范围不填补该空白。

## 按需继续

- [transmission-admission](transmission-admission.md)
- [no-receivers](no-receivers.md)
- [participant-reception-control](participant-reception-control.md)

[ETSI 官方 TS24.581 V19.2.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；仅所列版本和条款。

## 服务器计时与结束证据

- [排队后授予：T4重发何时停止，达到上限是否撤权](server-queued-grant-retry.md)
- [某个源无人接收：T11到期、停止命令与T3确认](server-stream-idle-termination.md)

这些路径依据TS24.581 V19.2.0指定Stage3程序，不把业务要求、发出命令和完成停止视为同一事件。

- [先定位私呼会话与媒体协商边界](session-media-permission-boundary.md)

- [广播初建的角色许可规则](broadcast-media-roles.md)
