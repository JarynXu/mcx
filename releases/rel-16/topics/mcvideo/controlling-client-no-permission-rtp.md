# MCVideo 客户端无发送许可却上传 RTP：控制方何时发 #3，怎样收尾？

**先看这台客户端的 U 状态，不要只看原因 #3。** U 无发送许可且处于 Idle 时，处理带载荷 RTP 还要查上一许可态是否已收到结束请求。U 无发送许可且处于 Taken 时，这个入口没有同样的历史条件。收到结束请求后如何收尾，另看整通呼叫此时的 G 状态。

本文限于 3GPP TS 24.581 V16.9.0（Rel-16，Stage 3）的普通在网预安排组呼。传输控制已建立，**U** 是控制功能（CF）面向该直连 MCVideo 客户端的基本发送控制接口，**G** 是所属呼叫的发送仲裁。U 属于这一个参与端，G 属于整通呼叫。不把非控制功能（NCF）的接口当作 U，也不套到广播、紧急或离网流程。[§§6.3.1、6.3.2.2，印刷页 52](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=53)、[§6.3.5.1，印刷页 64–66](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=65)。

## 第一次拦在哪：U: Idle 和 U: Taken 的条件不同

**先分来源。** 在同一个 `U: not permitted and Transmit Taken`，这条路径上实际有来自本 CF 媒体分发器的 RTP 时，网络媒体接口按 §6.3.5.4.1 **向该关联端转发**。这是下行，不要求另证控制 U 自身接收 RTP 或收到一份事件指示；它不触发 §6.3.5.4.6 的上行 #3。规定转发不证明终端实收，也不授予发送或接收许可。只知道整通呼叫的 G，或只看到一份 Notify、一个 SSRC、NCF 的 P 无许可状态，都不足以套这条下行分支。[§6.3.5.4.1，印刷页 71](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=72)。

下面两条**上行**入口另要有网络媒体接口的指示：**实际收到本关联客户端发来的带载荷 RTP**。只看到 RTP 头、来源不明的包、分发器送来的下行包、别的终端的来包，或一条没有角色来源的 #3，都不满足这两条上行入口。

| 当时这个客户端的 U 状态 | 还须查什么 |
| --- | --- |
| `U: not permitted and Transmit Idle` | 同一个 U 在上一 `U: permitted` 状态中，已经实际收到 `Transmission End Request`。不能拿客户端曾发过请求、别的 U 的收件或一条 Ack 替代。 |
| `U: not permitted and Transmit Taken` | 该客户端仍无发送许可；这个状态用于另一客户端获准发送的场景。本入口未列 Idle 的前次 End Request 条件。 |

两条适用时都按这三步：U 要求网络媒体接口**不要把来包交给媒体分发器**，向关联参与端发 `Transmission Revoke`、原因 **#3**（无发送许可），再进入 `U: not permitted but sends media`。两个入口的注释都把 NCF 一侧的这类 RTP 交由 NCF 处理。[§6.3.5.3.8，印刷页 70–71](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=71)、[§6.3.5.4.1，印刷页 71](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=72)、[§6.3.5.4.6，印刷页 76–77](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=77)。

状态图给 Idle 画了来包自环和进入新状态的来包箭头，没有写下前次 End 收件条件。**缺前次收件记录，不能判 #3，也不能判放行。** 若已确认当前状态对这个实际事件没有适用处理，§6.3.5.1 的默认规则另要求 U 指示网络媒体接口丢弃来包，U 留在原状态；这不是前述发 #3 并入新状态的步骤。接口指令也不等于已验证网络媒体接口执行。[图 6.3.5.1-1，印刷页 65](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=66)、[§6.3.5.1 默认规则，印刷页 66](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=67)。

## T3 到期重发，不用等它到期才拦包

进入 `U: not permitted but sends media` 时，U 启动 T3。在这个状态，U 不请求网络媒体接口把该客户端的 RTP 转给分发器。T3 **实际到期**才向同一参与端再发原因 #3 的 Revoke，重启 T3，并留在此状态。重发几次、放弃时做什么由实现决定。注释建议放弃时断开这个客户端，没有要求释放整通呼叫。[§6.3.5.7.1–3，印刷页 82](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=83)。

T3 表的默认值为 **1 秒，可配置**。表的启动栏写向已有许可的参与端发 Revoke，正常停止栏写收到 `Transmission Release`；这里的专门程序却在无许可状态入态时启动 T3。下面 §6.3.5.7.4 对收到 `Transmission End Request` 未另列停止 T3。不要把两条消息混用；等待撤销的 U 实收 End Response 时停 T3，也是另一条。这里不由正文没列该动作就断定离态后计时器继续或已停。[表 11.1.3-1 T3 行，印刷页 207](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=208)、[§6.3.5.7.4，印刷页 82–83](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=83)、[§6.3.5.6.8，印刷页 81–82](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=82)。

## 真收到 End Request 后，先看 Ack 位，再按 G 收尾

此处仍是**该端的** `U: not permitted but sends media`，且 U 实际收到关联端的 `Transmission End Request`。Subtype 首位为 1 时，U 须发传输控制 Ack，步骤 1 写 `Message Type=4`、`Source=2`；位为 0 时，这一步不要求发 Ack。Ack 位不决定以下走哪一支。这是媒体控制 Ack，不是 SIP ACK，也不是 `Transmission End Response`。步骤里的 Message Type 数值与消息表列出的请求 subtype `x0000`、以及字段定义按含首位的 subtype 编码，不能当作已经一致的线上编码。[§6.3.5.7.4 步骤 1，印刷页 82–83](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=83)、[表 9.2.2.1-3，印刷页 146](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=147)、[§9.2.3.10，印刷页 151](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=152)。

| 当时这通呼叫的 G | U 要做什么 |
| --- | --- |
| `G: Transmit Idle` | 发 `Transmission Idle`，消息序列号加 1；转到 `U: not permitted and Transmit Idle`。本分支没另列 End Response。 |
| `G: Transmit Taken` | 向**接收控制仲裁**发 `Media Transmission Notify`。未请求隐私时在 Granted Party's Identity 字段带**获准者**的 MCVideo ID，不把结束请求人的 ID 当成获准者。普通非广播可带 `Permission to Request the transmission=1`，也可单独请求这份通知的 Ack；如何处理该 Ack 或未收到由实现决定。U 转到 `U: not permitted and Transmit Taken`，并启动面向该参与端的基本接收控制实例。 |

**进来的 U 状态不替代此刻的 G 状态。** 两个出口都仍无发送许可。给接收仲裁发通知、保留请求发送的可能、启动接收实例，都不等于给该端授权发送或接收，也不是终端收到通知、收到 RTP 或显示画面的证据。图中两个 End Request 出口没有标明 G 条件，分路按正文步骤 2–3；没有这两个 G 状态的证据时，不补猜出口。[§6.3.5.7.4 步骤 2–3，印刷页 83](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=84)。

## 两条容易混在一起的记录

- **NCF 的 P 也能发 #3。** 在网组同一会话、P 无发送许可，且实收网络媒体接口报告是关联端来的 RTP 时，P 发本地 #3，仍在无许可态，并记录期待 `Transmission Release`。其来包分支未列对这批包的转发或丢弃指令。不要从同一个原因值推断来源、此前有过许可，或此时在等 CF 的 End Request。[§6.5.5.3.9，印刷页 113](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=114)、[§9.2.10.1–2，印刷页 164–165](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=165)。
- **CF 的 U 仍在等撤销时，须继续转发收到的关联端 RTP。** 对仍处于 `U: permitted` 的关联端，接口收到带载荷来包指示便要求网络媒体接口把 RTP 转给分发器；处于 `U: pending Transmit Revoke` 时，收到该端带载荷 RTP 则仍向分发器转发，保持等待。只看到 Revoke 发送或 T3 正在跑，不足以判已进入无许可仍发送态。[§6.3.5.5.6，印刷页 79](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=80)、[§6.3.5.6.2–4，印刷页 80](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/16.09.00_60/ts_124581v160900p.pdf#page=81)。

若查**普通未排队的发送许可处理、已有许可 U 的实际入包或普通 End**，看[服务器的普通发送控制](prearranged-group-transmission-server.md)。若实际在查**普通预安排组的显式抢占、满容量撤销或已观察到的旧发送端 U pending 阶段**，看[抢占等待与 End](onnetwork-preemption-revoke.md)。若已定位到**在网组的 NCF P**，要查同一关联端的来包指示或实际收到的 Release，看[非控制侧的 RTP、#3 与 Release](noncontrolling-participant-rtp-release.md)。若追的是**普通预安排组的接收仲裁或逐流许可**，按实际申请、授予及 SSRC 在[服务器的接收控制](prearranged-group-reception-server.md)取证，不把这份 Notify 当成接收授予。
