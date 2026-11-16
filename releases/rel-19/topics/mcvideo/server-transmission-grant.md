# 服务器发送授权：空闲请求、源标识与接收控制衔接

TS24.581 V19.2.0，controlling MCVideo function，在网普通组呼，非广播/system/emergency/imminent-peril/临时组；不请求 privacy。

从已初始化的发送仲裁 G: Transmit Idle 与请求方接口 U: not permitted and Transmit Idle 开始；本次是允许提出请求的 participant 的显式、非抢占请求。

仅一个本次发送源，初始 Cx=0 且上限允许至少1；本次请求未排队，不展开多流并发、跨系统非控制功能、MBMS/MBS及完整初始SIP/SDP程序。

## 通话仲裁与用户接口各自拥有状态

适用条件：识别本通话的 general 发送仲裁及请求方的 basic 发送接口；收到其 Transmission Media Request。

发送 general 每通话一个；basic 发送接口每个 participant 一个。普通非广播接口转交请求给仲裁，转交后仍无许可。只有收到仲裁的 Grant 才转送并进入服务器 U: permitted；Reject 转送后仍无许可。两种答复可请求 Ack，Ack收到或丢失的后续处理是实现选项，不是此处许可状态转换的强制等待条件。

- U: permitted 是服务器针对该participant的记录，不证明客户端已收取Grant或已开始发送。

依据：§6.3.2.2;6.3.4.1;6.3.5.1;6.3.5.3.4–6.3.5.3.6，印刷页 52、55、66、67、70、71。

## 空闲时的拒绝条件与源标识分配

适用条件：G: Transmit Idle 收到允许提出请求 participant 的 Transmission request。

以下任一项目满足即拒绝：通话只有一个客户端（cause#3），或对应entry存在 on-network-recvonly（cause#5）；拒绝后保持Idle，可附解释。授予分支停止T1(Inactivity)/T2(Transmit Idle)，保存发送者User ID，并分配和保存全局唯一Audio SSRC及Video SSRC直至该传输释放，再进入Taken程序。

- 开头为任一所列条件，a项末尾却有and，按原文保留此文字异常；不能反推必须两项同时成立。
- on-network-recvonly条件是元素存在，不擅改为布尔值true；两个拒绝项目同时满足的cause优先级未规定。

依据：§6.3.4.3.3，印刷页 57。

## 发送授予与接收通知分开处理

适用条件：仲裁进入 G: Transmit Taken，本次请求按common_conditions未排队。

向发送方发Granted，带获授优先级及已存音视频SSRC；Cx未达上限时加一。另把Media Transmission Notification交接收仲裁，带发送者标识、音视频SSRC、递增序号；请求曾带Functional Alias ID时也带上。普通非广播可带Permission to Request the Transmission=1。接收general由此启动；这不是对其他用户逐个授予接收。

- T4/C4只在本次请求曾排队时启动，本链不把它设为所有Grant共有的确认计时器。
- 发送者User ID的强制包含限于未请求privacy，本主题已明确该前提。Permission字段只允许请求，不等于发送许可。

依据：§6.3.4.4.2，印刷页 59。

## 获授上行仍受接收侧筛选

适用条件：请求方服务器接口已U: permitted，收到该participant带payload的RTP；仲裁G: Transmit Taken收到获授客户端媒体到达指示。

发送接口要求网络媒体接口把该RTP交媒体分发器；general仲裁停止运行中的T4，并要求分发器按本地策略及接收控制状态分发。发送许可不是向所有在会者无条件广播，仍须接收侧按用户和源筛选。

- 这里只核授权到分发的控制条件，不实现编解码、媒体混合或网络传输。

依据：§6.3.5.5.6;6.3.4.4.5;6.3.7.1，印刷页 80、59、95。

## 普通发送结束的处理顺序

适用条件：已获授发送者的接口U: permitted收到Transmission End Request；随后general G: Transmit Taken处理该请求。

接口按请求Ack位回Ack（Source=2、原文Message Type=4），内部转交时清Ack位且暂留permitted。general按下限减Cx、要求停止该participant的RTP转发、停运行中的T4并回End Response；Cx到下限才转Idle。接口转送End Response后转无许可Idle。普通停流不是整通话释放。

- Ack Message Type=4是本程序原文，与此前§9.2.2.1表的End Request subtype值不一致；此处不生成修正编码。
- Idle入态§6.3.4.3.2的队列外层条件另有异常，本批仅闭合到状态转换，不声称已完整验证队列续传。

依据：§6.3.5.5.3;6.3.4.4.6;6.3.5.5.3a，印刷页 79、80、59、60。

## 无人接收不等于通话失败

适用条件：接收general为Gr: Reception Idle，收到本获授发送者的RTP；或本源关联T11到期。

没有接收者时，RTP按本地策略丢弃或缓存，Gr保持Idle。T11到期则通知发送仲裁终止其关联的源，Gr仍Idle；用Revoke还是End Request由本地策略选择。不能把发送者有许可、收到RTP或T11到期，分别等同于已有人观看或SIP通话已释放。

- T11值及Revoke/End Request后的完整宽限重传链未在本批展开；结束命令发出不等于已完成停流。

依据：§6.3.6.3.7;6.3.6.3.9，印刷页 89。

## 证据边界

- 不覆盖最初呼叫准入、隐式请求、排队/抢占或忙时并发授权。
- 服务器重入unless显式请求与客户端不得隐式的措辞张力在此保留，不据此构造重入授权。

## 按需继续

- [participant-transmission-control](participant-transmission-control.md)
- [server-reception-permission](server-reception-permission.md)
- [no-receivers](no-receivers.md)

[ETSI TS 124 581 V19.2.0 / 3GPP TS24.581 V19.2.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；仅本版本。

## 服务器计时与结束证据

- [服务器空闲计时：通知重发不等于释放通话](server-idle-timers.md)
- [排队后授予：T4重发何时停止，达到上限是否撤权](server-queued-grant-retry.md)
- [某个源无人接收：T11到期、停止命令与T3确认](server-stream-idle-termination.md)

这些路径依据TS24.581 V19.2.0指定Stage3程序，不把业务要求、发出命令和完成停止视为同一事件。
