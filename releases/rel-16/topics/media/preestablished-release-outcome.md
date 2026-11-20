# 预建立会话里的 Disconnect：结束一通私呼，怎么判断确认到了哪一端？

客户端两次回复 Accepted，不代表挂断了两通私呼。参与 MCPTT 功能（PF）收到本次 Disconnect 的确认，和等到重试上限，都会回到「预建立会话未在用」。要区分两种情况，必须查看 PF 侧实际收到的确认或定时器记录。这里谈的是普通在网私呼已经使用 PF 与该客户端之间的一条预建立会话，核对的是这条会话上的媒体面控制与本地状态。[TS 24.380 V16.9.0，Release 16，Stage 3，§9.1，印刷页 193](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=194)；[§9.3.2.1，印刷页 197](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=198)。

## 控制方释放本次私呼：谁发 Disconnect，谁回 Accepted？

PF 处于 `G: Pre-established session in use`，实际收到控制 MCPTT 功能（CF）的本次呼叫释放指示时，须停止仍在运行的 T55，向客户端发 MCPC Disconnect。**整个 MCPTT Session Identity 字段**沿用建立这通呼叫时发出的 Connect，既包括身份值，也包括 Session Type。PF **宜**把 subtype 的第一位设为 1（请求确认）；它须启动 T56，将 C56 初始化为 1，并转到 `G: Call releasing`。本条没有把启动 T56 限定为确认位已置 1。[§9.3.2.4.5，印刷页 200–201](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=201)；[§8.3.3.3，表 8.3.3.3-1，印刷页 176](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=177)。

看客户端实际收到 Disconnect 前，这条预建立会话是否在用：

| 客户端当时的状态 | 若收到的 Disconnect 请求确认 | 会话状态 |
| --- | --- | --- |
| 在用 | 回 MCPC Acknowledge，Reason Code 为 Accepted | 转到 `U: Pre-established session not in use`，并按 §6.2.4 处理。 |
| 已未在用 | 仍须回 MCPC Acknowledge，Reason Code 为 Accepted | 保持未在用。 |

subtype 首位为 0 时，上述两条不要求回确认；状态规则仍适用。于是，同一条会话由在用转为未在用后，实际又收到了要求确认的重发，客户端可以留下两次发送 Accepted 的记录。这不是第二次通话结束，也不证明两份确认中任何一份已抵达 PF。若还没确认两份消息属于同一通话，也不能仅按报文数量判重发。[§9.2.2.3.4，印刷页 195](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=196)；[§9.2.2.4.5，印刷页 196](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=197)。

Disconnect 表列的是 PF 的 SSRC 和 MCPTT Session Identity；Acknowledge 表列的是话权参与者的 SSRC 和 Reason Code，**没有** MCPTT Session Identity。核对这一对消息，要对照会话、方向、控制通道和实际收发时序，不能仅看 Accepted 就说它答的是 Disconnect 而非 Connect。这份确认是 MCPC 的 RTCP APP 报文，不是 SIP ACK 或话权 Floor Ack。[§8.3.2，表 8.3.2-1，印刷页 175](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=176)；[§§8.3.5–.6，表 8.3.5-1、8.3.6-1，印刷页 181–182](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=182)。

## PF 为什么回到「未在用」？看 T56 期间实际发生了什么

以下是 PF 已处于 `G: Call releasing` 时的三类事件，不是必须前后发生的三个步骤：

| PF 实际处理的事件 | 处理和结果 |
| --- | --- |
| 收到客户端本次 Disconnect 的 Acknowledge | 停止仍在运行的 T55，停止 T56；可以释放本次呼叫所用、但预建立会话不需要的媒体资源；转为 `G: Pre-established session not in use`。这条收件规则未另列 Reason Code 前提。 |
| T56 到期，未到 C56 上限 | 在本次呼叫的媒体面控制传输通道重发同一 Disconnect，启动 T56，C56 加 1，保持正在释放。 |
| T56 到期次数达到 C56 上限 | 不再重发 Disconnect；可以释放本次呼叫所用、但预建立会话不需要的媒体资源；转为 `G: Pre-established session not in use`。 |

达到上限并不补出一次确认收件。看到最终状态也分不出走的是哪一行；定案要核对 PF 收件、真实到期事件与本次计数。本版 T56、C56 可配，不能用默认时长乘计数猜一笔事务重发了几次。[§9.3.2.5.1–.4，印刷页 203](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=204)；[表 11.1.4-1，印刷页 221](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=222)；[表 11.2.4-1，印刷页 224](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=225)。

## 如果是客户端要求释放，释放的是通话还是整条会话？

- **只释放这通私呼，保留预建立会话。** 在用的 PF 实际收到客户端的这种指示后，向 CF 发呼叫释放指示，可释放本次通话所用而预建立会话不需要的资源，停 T55，转为未在用。此分支不列向客户端发 Disconnect、启动 T56 或等待媒体面确认。若客户端自己的这条会话仍在 `U: Pre-established session in use`，且实收其呼叫释放 REFER 的 2xx，就按客户端规则转为未在用并终止基本话权参与者状态机实例；这份 SIP 响应不是 PF 收到 MCPC Acknowledge。[§9.3.2.4.4，印刷页 200](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=201)；[§9.2.2.4.6，印刷页 196](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=197)。
- **客户端要求释放整条预建立会话。** 在用的 PF 实际收到客户端的预建立会话释放指示后，停止在客户端与 CF 之间传送 RTP 和话权控制消息，释放与这条预建立会话有关的媒体面资源和计时器，进入 `Start-stop`。这和「会话建着、当前没承接呼叫」是不同结果。[§9.3.2.4.6，印刷页 201](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=202)；[§9.3.2.3.1，印刷页 198](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=199)。

要确认上层信令所指的是业务还是预建立对话，查[普通私呼的释放信令](../calls/private-client-release.md)和[拆除在用预建立会话](../calls/preestablished-session-in-use-release.md)。要查建立阶段的 [Connect、Accepted 和 T55](preestablished-connect-outcome.md)，另看建立入口。这里不规定并发收件和到期的调度顺序，也不从一侧的确认推断对端已处理、双方媒体都停了或所有资源都已回收。

若尚不能确认线上的消息是 Disconnect，先查[RTCP APP 的 Name 和 subtype 怎样区分消息](rtcp-app-name-subtype.md)。
