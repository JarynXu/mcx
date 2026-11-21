# 非控制 MCPTT 功能收到 Floor Idle：谁回 ACK，怎样认出只发给一个人？

控制功能（CF）发来的 Floor Idle 要求确认，非控制功能（NCF）发给终端的那一侧却不再要求确认，而 CF 仍收到一条 Floor Ack。这并不矛盾。**先看 NCF 面向 CF 的服务器接口收到的 Floor Idle 有没有 Track Info，再核对两侧各自的消息和确认。** 以下限同一场普通在网 MCPTT 组呼的非双话权、非多话者分支。P 和被动队列按这一场的非控制侧查，不按服务器上的全部呼叫查。[§6.5.2.2，印 103–104](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=104)。

## 入向没有 Track Info：NCF 可以已经确认，终端却还没收到

服务器接口收到一条不带 Track Info 的 Floor Idle，且没有 Floor Indicator，或其中 G 位为 0，须向本 NCF 为这场组呼服务的所有话权参与者接口（P）发送 Floor Idle。**下行 subtype 的首位置 0，不要求终端确认**；出向序号按本地规则填。若 **CF 发来的原消息**首位是 1，NCF 还须向 CF 自己回 Floor Ack：`Source=3`（非控制功能），`Message Type=5`（Floor Idle）。不要用改过的下行首位替代原消息的首位。[TS 24.380 V16.9.0 §6.5.4.8 第 2 项，印 109](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=110)；[§8.2.2，印 147–148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=148)。

CF 收到这个 ACK，能确认的是 NCF 对这条控制消息的确认，不是本 NCF 下每个终端已收到 Floor Idle，更不是播放或媒体停止的凭据。第 3 项要求清空 **这场组呼在 NCF 侧的被动话权请求队列**，未把它写成只对不带 Track Info 的消息适用。这个动作也不等于 CF 的活动请求队列已空。[§6.5.4.8 第 2(c)、3 项，印 109](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=110)。

## 入向有 Track Info：只有一个引用时，出向会删掉整个字段

服务器接口用收到的 **最后一个 Participant Reference** 找到本地对应的 P，然后给这个 P 发 Floor Idle。这个引用指向本 NCF 的参与者接口，不是 MCPTT 用户 ID，也不是 RTP 的 SSRC。[§6.5.4.8 第 1 项，印 108–109](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=109)；[§8.2.3.13，印 154–155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=155)。

| NCF 从 CF 收到的引用 | 给所选 P 的出向 Floor Idle |
| --- | --- |
| 一个，例如 `[17]` | 用 17 找对应 P，删除整个 Track Info；单引用分支另列本地消息序号处理。 |
| 多个，例如 `[9, 17]` | 同样用 17 找 P，但只删最后一项，保留 `[9]`。不将单引用分支的序号动作套用到这里。 |

因此，**只看到 NCF 发给终端的那条消息没有 Track Info，无法判它是全体通知还是只发给这一人**。要区分，核对同一次事件的入向消息、末尾引用到本地 P 的对应关系，以及实际外发目标。第 1 项未用第 2 项的群发规则去改 subtype。对于单引用的计数与写入值，条文分别描述，不能据此补一个跨实现通用的序号算式。[§6.5.4.8 第 1–2 项，印 108–109](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=109)。

**终端回的 ACK 不是 NCF 在群发分支生成的 ACK。** 在无发送许可或有发送许可的 P 上，P 收到要下发的 Floor Idle 且 subtype 首位为 1，须记录期待此类确认。P 实际收到终端的 Floor Ack 时，要再看此时的状态。P 不在 Start-stop 或 Releasing，且有与该 ACK 的 Message Type 匹配的期待，才按本条把 ACK 上交服务器接口并清掉该期待；服务器接口实际收到上交的 ACK 后，按 §6.5.4.5 发往 CF 并处理 Track Info。若只见 ACK 出现在 CF 一侧，不能倒推为终端生成，更不能当作终端确认了另一次 Idle。已进入释放而不再适用该条时，不能凭之前记过期待就上交迟到 ACK。没收到期待的 ACK 怎样处置由实现决定。[§6.5.5.3.2，印 114](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=115)；[§6.5.5.4.5，印 117](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=118)；[§6.5.5.5.1–3，印 118](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=119)；[§6.5.4.5，印 107](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=108)。

- 如果回的是 [Floor Granted、Deny 或队位答复](on-network-noncontrolling-floor-grant.md)，看各自的引用和 ACK 规则，不照搬本页的 Idle 条款。
- 如果要问[CF 为什么进入空闲、活动队列怎么处理](on-network-idle-floor-server.md)，查控制方仲裁，不把 NCF 的被动缓存当成控制队列。
- 如果[抓包还没识别出消息类型](rtcp-app-name-subtype.md)，先检查 RTCP APP Name 和 subtype，再讨论 ACK 来自哪一段。
