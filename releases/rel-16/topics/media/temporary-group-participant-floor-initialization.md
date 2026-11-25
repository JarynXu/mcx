# 临时组话权接口还在初始化：拒绝是否代表没入队？收到 Floor Release 怎么撤回？

拒绝不代表没入队。控制侧的逐参与者接口 U 如果已在初始化状态，并实收了这次 `Floor Request`，规范先要求计算有效优先级并入队，再按请求里带来的排队能力决定回复。**拒绝和入队是两件事。** 一条拒绝不证明服务器本次实际执行、跳过或撤销了入队。[TS 24.380 V16.9.0，Release 16，Stage 3，§6.3.5.10.5，印刷页 93](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=94)。

## 先对上哪一个 U 收到了什么

这里的 U 是临时组**控制侧话权服务器面向关联话权参与者的接口**。它不是终端的话权状态，不是非控制侧 P，也不是管整场的一般仲裁 G。按 §6.3.5.2.2 这个入态分支，临时组的 SIP 会话已建立，且关联话权参与者是一个组成 MCPTT 组或临时组会话的发起者。若尚未初始化一般状态机，接口须先初始化，再为这名关联方设置 `U: not permitted and initiating`。单独受邀的终端不因“在临时组里”就符合这一身份条件。[§6.3.5.2.2 的临时组段，印刷页 74](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=75)；[§6.3.5.10.1–.2，页 92](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=93)。

U 在此状态等待仲裁逻辑完成初始化，期间可以从非控制 MCPTT 功能实际收到 `Floor Request`。不要把发端记录、SIP 请求里的话权请求正文或一条最终 SIP 响应当成这个 U 已经实收。若只有信令面把组成组的请求正文交给一般仲裁 G，或要查 G 何时做首次选择，读[临时组的一般话权首次仲裁](temporary-group-floor-initial-arbitration.md)。这里不判断 G 的状态、初选结果、原组成组是否继续或整场呼叫是否建立完成。

## 入队的要求和出向回复分开看

符合上述状态及实收条件时，第 1–2 项要求 U 按 §4.1.1.4 确定本次请求的有效优先级，再按这个优先级把请求放入话权请求队列。**入队不以排队能力为 1 才执行。** §4.1.1.4 列出可用输入，允许按本地策略判断。不能用请求里的单个优先级值替代有效优先级，也不能自行补出同优先级的排序规则。[§4.1.1.4，页 21](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=22)；[§6.3.5.10.5 第 1–2 项，页 93](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=94)。

| 这次实收请求的 Track Info | 本条规定的回复 |
| --- | --- |
| `Queueing Capability=1` | 向提出请求的非控制 MCPTT 功能发 `Floor Queue Position Info`；`Queue Info` 中带队位和话权优先级。 |
| `Queueing Capability=0` | 发 `Floor Deny`，`Reject Cause=1`（Another MCPTT client has permission）。这份原因值不能单独证明 G 已经进入 Taken 或谁已获准。 |
| 没看到能力值、记录截断，或实收值是保留值 | 不能按 0 处理。缺字段和字段为 0 不同，本条没有为缺失或保留值规定默认回复。 |

前两种回复都须带**本次实收请求的 Track Info**；临时组会话须在 `Floor Indicator` 带相应指示。第 5 项仍令 U 留在 `U: not permitted and initiating`。第 4 项的注说：合并期间，若仍在进行会话的组成组话权空闲，有一名话权参与者请求话权，可以收到该组 MCPTT 客户端发来的 `Floor Request`，原文称「without the queueuing capability」。注没有给出实收字段的有无、数值或请求方是否支持排队的判据。[§6.3.5.10.5 第 3–5 项及注，页 93](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=94)；[§8.2.3.13 表 8.2.3.13-1，页 154](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=155)。

**排障时分开判三项。** 一条 `Floor Deny #1` 不能识别实际 U 状态和来向能力；缺能力的记录不能补成 0；没取得本次队列操作记录，不能认定已经入队，也不能认定从未入队或随后出队。队位应答也不是话权授予、队列持久性或语音到达的证据。若问题是[原组成组重递旧队列或拆分接回控制](merge-floor-queue.md)，查该组的角色切换，不复用本页 U 的入口。

## 收到 Floor Release：先查哪里，要不要回 Ack？

同一个 U 仍在 `U: not permitted and initiating`，且已收到**关联参与者**的 `Floor Release`，才读这一分支。§6.3.5.10.7 标题括号写的是 `S: Floor Release`，开头却明确写收到关联方的消息。不能凭对端的发送日志、先前的拒绝或缓存里有一份请求正文，认定 U 已经收到这次撤回。[§6.3.5.10.7，开头及第 1–4 项，印刷页 93–94](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=94)。

**撤哪一条？** 第 2 项要求用本次消息最上层的 `Participant Reference` 和原文所称的 SSRC 查这名参与者。先查活动话权请求队列；**查过且未命中**，才查缓存的 `application/vnd.3gpp.mcptt-floor-request+xml` 正文。队列命中就从队列移除该客户端的请求，不再走缓存分支；缓存命中也只移除该客户端的请求，不删整份正文。两处都没找到就没有本条要求移除的对象。各分支都保持 U 初始化。没看到队列日志，不等于已查且未命中。[第 2–4 项，页 94](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=95)。

**要不要回 Ack？** 看这次 `Floor Release` 的 subtype 首位，不看撤回有没有命中。首位为 1 须发 `Floor Ack`，即使两处都没找到；首位为 0 不触发本项的必发条件。没读到该位，不能按 0 处理。流程写 `Message Type=4`、`Source=2`（控制 MCPTT 功能）。一条 Ack 不证明对端收到回复、该客户端排过队或请求已经移除。[第 1 项，页 93–94](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=94)。

若要核对线上字节，同版原文有两处不能替它选边：

- 第 2 项把 SSRC 写作在 `Track Info` 内。[表 8.2.3.13-1，页 154–155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=155)列参与者引用，未单列 SSRC；[Floor Release 格式表 8.2.7-1，页 166](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=167)把报文 SSRC 与 Track Info 分列。不能据此断定必须取头部 SSRC 当查找键。
- 流程第 1(a) 项写 4。[表 8.2.2.1-1，页 148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=149)把 Floor Release 的 subtype 写成 `x0100`；[§8.2.3.14，页 155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=156)要求 Ack 的 Message Type 在前面补三个 0，保留原 subtype 的五位，含确认位。首位为 1 时照通用规则读为十进制 20。[§8.2.13 的 Message Type 说明，页 174](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=175)回指这条通用规则。两种文字读数不同，不能据本条宣布哪个线上取值唯一正确。

## 仲裁结果到达 U 后，转发给谁、进入什么状态？

这一步看的是**控制侧的同一个逐参与者接口 U**。U 还处于 `U: not permitted and initiating`，且已收到本场 MCPTT 话权仲裁逻辑交给它的结果。只有仲裁逻辑的发出记录、别的 U 的接收记录或最终 SIP 响应，不能证明这个 U 收到了结果。以下三条也未把该参与者先发过 Floor Request 写成前提。

三条都要求 U 把实收的消息转发给**这个 U 的关联话权参与者**。按实收结果分别进入下表状态：

| U 实收仲裁结果 | 进入的 U 状态 | 入态时的动作 |
| --- | --- | --- |
| Floor Taken | `U: not permitted and Floor Taken` | 移除已存的 Track Info（若有），设置该状态。[§6.3.5.10.3，印刷页 92](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=93)；[§6.3.5.4.2，页 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=79)。 |
| Floor Idle | `U: not permitted and Floor Idle` | 移除已存的 Track Info（若有），设置该状态。[§6.3.5.10.4，页 92–93](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=93)；[§6.3.5.3.2，页 75](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=76)。 |
| Floor Granted | `U: permitted` | 为关联方设置该状态。该入态条文没写移除 Track Info，也不能据它认定 Track Info 一定保留。[§6.3.5.10.6，页 93](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=94)；[§6.3.5.5.2，页 85](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=86)。 |

Taken 和 Idle 入态时清理的是已存的 Track Info。不能据此认定转发报文会删掉 Track Info，也不能认定请求队列或缓存请求正文已清理。

三条都允许 U 把出向消息的 subtype 首位设为 1 来请求 Floor Ack。收到 Ack 后怎样处理，没收到时做什么，由实现决定。**第 3 项要求进入对应状态，没有写成收到 Ack 才进入。** 首位为 1 只表示要求确认；发送记录或 Ack 不能充当现场 U 已入态、相关终端已收到通知、终端已改变状态或 RTP 已到达的证据。[表 8.2.2.1-1，页 148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=149)。

[结构化条件与声明](temporary-group-participant-floor-initialization.json)。
