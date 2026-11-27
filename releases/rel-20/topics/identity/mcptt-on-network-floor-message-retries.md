# MCPTT 在网：话权空闲、撤回和授予消息的重发

**先看重发的是哪条消息。**MCPTT 在网业务配置中，T7 管 `Floor Idle`，T8 管 `Floor Revoke`，T20 管 `Floor Granted`。等到的消息和次数怎么写，要按各自的配置项查。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.6/.7。

| 要查什么 | §8.4.2.7 在网项怎么写 |
| --- | --- |
| 话权空闲时，`Floor Idle` 隔多久重发？ | `T7-floor-idle` 是话权空闲时的重发间隔。项 14 说 `C7-floor-idle` 控制最多重发多少次；项 27 说 C7 是最多发送多少次。 |
| 重发 `Floor Revoke` 要等到哪条消息？ | `T8-floor-revoke` 是重发间隔，直到收到 `Floor Release`（项 15）。不是等新的 `Floor Request`，也不是撤权后 RTP 媒体还能转发多久。 |
| 话权控制服务器何时重发 `Floor Granted`？ | `T20-floor-granted` 是每次重发前的等待时间，直到收到 `Floor Request`。项 21 说 `C20-floor-granted` 控制发送次数；项 29 说 C20 是最多重发多少次。 |

### 次数和停止条件分开核

原文在 C7 和 C20 的两对描述里分别用了「发送」和「重发」。读到一个配置数，不要擅自加减一次、断定初发是否计入，或把零写成现场从不发消息。这些项也没有给默认次数。T8 这条没有列出计数项，不据此推定永远重发，或断言其他规范没有限制。

T8 提到收到 `Floor Release`，T20 提到收到 `Floor Request`。只知道对端发出了相应消息，不能确认本端已经收到。此处不规定如何把日志里不相关的报文和这次重发配对，也不把收到 `Floor Release` 当成整通呼叫结束。若在查撤销 **RTP 发送许可后**服务器还能转发多久，走 [T3 的 RTP 计时](mcptt-on-network-floor-rtp-timers.md)，不要用 T8 替代。

### 字段声明和时长校验

这五项都在业务配置已选的 `<on-network>/<fc-timers-counters>` 内，§8.4.2.1 在网项 7 和 §8.4.2.3 声明为必需，无声明默认值。T7、T8、T20 是 `xs:duration`，C7、C20 是 `xs:unsignedShort`；不把这套必需项移到只有离网块的配置。

§8.4.2.6 具名时长清单的项 12、13、19 分别是 T7、T8、T20，不是两个计数器。需要判格式或秒值错误时，查[具名时长的两个校验分支](ad-hoc-broadcast-hang-time.md#缺项和校验怎么判)。字段声明和含义不能证明某次发送、接收、启动或重置了计时器。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-on-network-floor-message-retries.json)
