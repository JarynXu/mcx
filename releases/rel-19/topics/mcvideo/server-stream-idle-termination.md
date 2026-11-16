# 某个源无人接收：T11到期、停止命令与T3确认

TS24.581 V19.2.0普通在网非广播/system/emergency/imminent-peril、非临时组；已存在一个获授发送源，排除抢占和多源仲裁扩展。

T11按发送者/源关联；G/Gr为通话仲裁，U为服务器面向此发送者的接口。

只在明确条件下跟踪本地策略选择Transmission End Request的分支；选择Transmission Revoke的替代链不在本页展开。

## 按源启动无人接收计时

适用条件：普通组Gr接收到Media Transmission Notification；或Gr: Reception accepted处理本源最后的接收End Request/End Response，使C11达到下限。

普通通知分支启动与发送者User ID关联的T11并令该源C11=0；已Accepted时通知新源也仍保留Accepted。接收结束使C11到下限时也启动T11；复用同一时钟还是新建由本地策略决定。T11默认10秒且可配置，来自T11-stream-reception-idle，不是固定十秒强制断整通话。

- 表的开始事件概述较宽，正文有普通manual通知及C11到下限条件；不能对每个接收结束消息无条件重启T11。
- C11是该源活跃接收数，C7是general接收计数；即使Gr仍Accepted，也可能有另一个具体源在等接收者。

依据：§6.3.6.3.3 step1b;6.3.6.4.10 step1b;6.3.6.4.4 steps3–4;6.3.6.4.5 steps3–4;11.1.3 Table11.1.3-1 T11 row，印刷页 88、90、91、92、220。

## 获授接收或源结束时停止T11

适用条件：Gr Idle或Accepted中，某接收请求获授本源；或者收到本源Transmission End Notify。

授予接收时停止运行中的本源T11并更新该源接收记录；源结束通知也停止其关联T11。仅收到接收请求、通知仍在路上或客户端SIP200，不能替代“请求获授”这一停止条件。

- Gr Idle授予段未在stop T11句重复User ID，紧随步骤定义该源计数与标识；本主题单源，不补多实例选取算法。

依据：§6.3.6.3.6 step2b–d;6.3.6.4.3 step2b–d;6.3.6.3.8;6.3.6.4.11，印刷页 88、89、90、92。

## T11到期只触发源终止处理

适用条件：与本源关联的T11到期，当前Gr为Reception Idle或Reception Accepted。

接收仲裁通知发送仲裁终止该源，自身保持原Gr状态。选择Revoke还是End Request由本地策略决定。它是启动终止处理的事件，不是当场证明媒体已停，也不是应用信令通话释放完成。

- 原文没有在此给出两仲裁模块间通知的全部编码；下一条仅在选择的End Request输入实际出现时成立。

依据：§6.3.6.3.9;6.3.6.4.12，印刷页 89、92。

## 结束命令进入宽限与重传

适用条件：本地策略选择End Request；G: Transmit Taken接到相应Transmission End Request，面向发送者的接口此前U: permitted。

general停止运行中的T4，将原因设为#8（无接收participant），可附说明，进入G: pending Transmission Revoke并发End Request。接口转发后进入U: pending Transmit Revoke并启动T3。该宽限期内接口仍把源RTP交媒体分发器，general按本地策略处理；不能说发出结束命令即丢弃一切媒体。T3到期重发同原因和Indicator的命令并重启，仍保持pending。

- 此事件标题Send但正文写Upon receiving，按实际输入条件陈述，不修正标题。
- T3默认1秒且可配置；重发次数及最终放弃动作是实现选项，断开客户端只是NOTE建议，不套用C4默认3。
- 无接收者时保留的转发动作不意味着真的有用户获准观看；接收策略与SSRC筛选仍独立适用。

依据：§6.3.4.4.13;6.3.4.5.2;6.3.4.5.3;6.3.5.5.10;6.3.5.6.1–6.3.5.6.4;11.1.3 Table11.1.3-1 T3 row，印刷页 62、63、81、82、219。

## 结束应答完成本条宽限路径

适用条件：服务器接口U: pending Transmit Revoke收到客户端Transmission End Response；general仍G: pending Transmission Revoke，且本源为唯一活跃发送者、没有排队请求。

接口按Ack位回Source=2、Message Type=1，停止运行中的T3，转交End Response并转无发送许可Idle。general要求停止该源RTP转发，Cx未到下限时减一；达到下限才转G: Transmit Idle。完成本源结束仍不等于整通话释放。

- 本条只覆盖End Response路径；对方反发End Request的替代终止路径没有在本稿补成同样停止T3。
- T3表normal stop写Transmission Release，程序此处明确End Response；保留命名差异，不自动改名。
- 转Idle后的T1/T2启动仍受其独立入态条件约束。

依据：§6.3.5.6.8;6.3.4.5.7;11.1.3 Table11.1.3-1 T3 row，印刷页 64、83、219。

## 证据边界

- 不改变前批“无人接收由本地策略丢弃/缓存”的结论，此处只补计时与停止确认关系。
- 客户端接收命令后的处理链接participant-transmission-control，不在本页重复状态机。

## 按需继续

- [server-reception-permission](server-reception-permission.md)
- [server-transmission-grant](server-transmission-grant.md)
- [no-receivers](no-receivers.md)
- [server-idle-timers](server-idle-timers.md)

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08), Release19](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；仅本版本。
