# 普通在网组呼：控制侧 U 已空闲，收到 Floor Release 后为什么还回 Idle？

在已建立的普通在网单话权 MCPTT 组呼中，控制服务器面向一名参与者的接口已处于 U: `not permitted and Floor Idle`。这个 U 实际收到本关联参与者的 Floor Release 后，**即使没有匹配的排队请求，也须向该参与者发 Floor Idle**。Release 是否要确认、队列是否命中、终端是否真的收到了 Idle，是三件事。

这里的 U 是控制侧逐参与者接口，不是终端的 U、非控制功能（NCF）的 P，也不是整场仲裁 G。以下只查普通组呼的这条媒体面程序，不套到广播、系统呼叫、紧急或迫近危险呼叫、临时组、环境监听、音频切入、双话权、多话者和 MBMS 程序。按本版 §8.2.7，普通在网 Floor Release 走单播，也可用于撤回排队请求，不要求发出者曾获准讲话。不能以终端、PF 或 NCF 已发出作为控制 U 实收的证据；这条程序不要求另证 G 处于 Floor Idle，也不以另有排队协商记录为入口。

## Release 的确认和发出的 Idle 各看自己的确认位

| 控制侧 U 实际观察到什么 | §6.3.5.3.7 要它怎样处理 |
| --- | --- |
| 来向 Floor Release 的 subtype 首位是 1 | 须发对此 Release 的 Floor Ack。程序字面是 `Message Type=4`（Floor Release）、`Source=2`（控制 MCPTT 功能）。队列没命中也须确认。 |
| 来向 Floor Release 的 subtype 首位是 0 | 不触发本条的 Floor Ack。该位不知道时，不能当成 0。 |
| 符合入口，不论来向 Release 是否要求确认或查找是否命中 | U 须为该关联参与者生成并发送 Floor Idle，消息序号加 1。U 可把这条 Idle 自己的 subtype 首位置 1 来请求另一笔确认；怎样处理收到或收不到该确认由实现决定。U 留在原态，不再执行入态步骤。 |

表 8.2.2.1-1 把两条消息分别写成 `x0100`（Release）和 `x0101`（Idle）。§8.2.3.14 的通用 Message Type 编码却要求包含**被确认报文**的 subtype 首位。它和程序字面的 `4` 有差异；不据此裁定实际线上值，也不把取证时看到的首位改成 0。确认 Release 的 ACK 不确认退队；以后若要核对 Idle 的应答，要对上实际被确认的 Idle 及该段收件，不能沿用这一笔 Release 的 ACK。

依据：[TS 24.380 V16.9.0 §6.3.5.3.1–.2，印刷页 75/PDF 76](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=76)；[§6.3.5.3.7 第 1–4 项，印刷页 76/PDF 77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=77)；[第 5–6 项，印刷页 77/PDF 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)；[表 8.2.2.1-1，印刷页 148/PDF 149](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=149)；[§8.2.3.14、表 8.2.3.14-1，印刷页 155/PDF 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=156)。

## 查队列用控制 U 实际收到的 Release

- **有 Track Info：** 用其中最上层（原文 topmost）的 Participant Reference 和这条 Release 的 SSRC 一起查。比如队列中有 `(P1, S)`，收到的是 `(P2, S)`，且该组合无记录，不能退回按 SSRC 删除 `(P1, S)`。
- **没有 Track Info：** 只用同一来向 Release 的 SSRC 查。抓包没截全，不等于字段确实不存在。两支都只有匹配才移除那一项，不清空队列；只有 Floor Ack 或 Floor Idle 的记录，不能证明实际命中或执行过删除。

Participant Reference 是本地接口能够识别的引用，不是 MCPTT User ID。§8.2.7 的通用 SSRC 文字写获准发送者，但 §6.3.5.3.7 明写使用收到的 Release 的 SSRC。本条不换用另一名当前讲话者的 SSRC，也不引入 §8.2.7 中仅用于离网的 User ID。

有 NCF 参与时，§8.2.7 的通用说明写 Release 包含 Track Info，§8.2.8 则明写 Idle 须带 Track Info。本条只写怎样用**收到的**字段查队列，不规定怎样把它复制到出向 Idle、怎样补值或据此确认下一跳收件。这里的 topmost 不改成另一条 NCF 下行程序所用的“最后一项”。只在终端腿见不到该字段，不证明控制 U 的来向也没有；NCF 被动队列的变化也不证明控制侧这次移出。

依据：[§6.3.5.3.7 第 3–4 项，印刷页 76/PDF 77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=77)；[第 5–6 项，印刷页 77/PDF 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)；[§8.2.3.13，印刷页 154–155/PDF 155–156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=156)；[§8.2.7–.8，印刷页 165–167/PDF 166–168](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=166)；[§6.5.4.3，印刷页 106/PDF 107](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=107)；[§6.5.4.8 第 1 项，印刷页 108–109/PDF 109–110](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=109)。

## 一条出向 Floor Idle 不能告诉你它从哪来

同一个已空闲的控制 U 还有另一条入口：**实际收到本场 G 发来的 Floor Idle**，才在 §6.3.5.3.10 向关联参与者转发。它可请求确认，仍保持原态；这条转发程序没有另列 §6.3.5.3.7 的生成、序号加 1 或按 Release 查队列的动作。只见 U 发出 Idle，无法区分这两条入口，更不能推定 G 的状态变化、T1/T4/T7 到期、全组通知、实际停转 RTP，或下一名已获准。

依据：[TS 24.380 V16.9.0 §6.3.5.3.10，印刷页 77/PDF 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)。

相邻分支：

- 若已确认是已建立的按需普通在网单话权组呼，U 和 G 都已 Idle，且控制侧 U 实收本关联参与者的非抢占、显式、非排队 Floor Request，查[空闲时的请求与条件授予](on-network-idle-floor-server.md)，不是本页的 Release。
- 若已确认是已建立的按需普通在网单话权组呼，而控制 U 当时其实处于 `not permitted and Floor Taken`，实收本关联参与者的 Release，且已协商排队、未在 `mc_priority` 中包含话权优先级，查 [Taken 下非持有者撤回](on-network-preemption-revoke.md)，不套本页的 Idle 应答。若是同系统、已建立的按需普通单话权组呼，原持有者显式请求获准、没有先发生抢占撤销或覆盖标记，且控制 U 仍为 `permitted` 并实收直接关联终端的主动放权，查[持有者放权](on-network-holder-release.md)。这条链上的 Release Ack 也不证明 G 已收或 RTP 已停。
- 查终端结果时，限已确认不涉及抢占的普通在网非广播单话权组呼，且这台终端**处于 pending Release 并实收同场 Floor Idle**，再读[终端话权状态](on-network-floor-client.md)：普通非广播分支须停 T100 并转为无许可；仅当收到的 Idle 要确认，才按终端程序字面回 `Message Type=5`、`Source=0`。只发出 Release 或收到迟到 Granted，都不能当作这个入口。
- 若要查下行到 NCF，先核对该场普通在网单话权组呼的 **NCF 服务器接口实际从 CF 收到 Floor Idle**，再按实收 Track Info 和相应 P 判断[非控制侧如何下发和确认 Idle](noncontrolling-floor-idle-delivery.md)。不是 NCF 的 P 实收 Release 就等于控制 U 实收，CF 的发送也不证明 NCF 或终端实收。
