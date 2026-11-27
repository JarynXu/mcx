# MCPTT 业务配置：私呼的静默时长、整通上限和单次发话时限

**静默看 `private-call/hang-time`，整通上限看该私呼话权类型对应的 `max-duration-…`，单次发话看 `transmit-time/time-limit`。**先确认读的是 MCPTT **业务配置文档**，再查在网或离网配置块。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.6/.7。这里的 `off-network` 是业务运行方式的配置块，不是[用外设下载离线配置](offline-ue-configuration.md)的过程。

| 要核的字段 | `on-network` 的 `private-call` | `off-network` 的 `private-call` |
| --- | --- | --- |
| `hang-time` | 同一私呼中连续两次发话之间的静默时长上限（§8.4.2.7 在网项 3、注 1）。 | 离网私呼的挂起计时值（离网项 3）。 |
| `max-duration-with-floor-control` | 在网带话权私呼的整通时长上限（在网项 4）。 | 离网带话权私呼的整通时长上限（离网项 4）。 |
| `max-duration-without-floor-control` | 在网无话权私呼的整通时长上限（在网项 5）。 | 不能把它当成离网可用参数。若该块含这个子项，§8.4.2.6 有忽略条款。 |

## 离网块出现无话权上限，为什么不算已配置？

两块的 Schema 都引用同一个 `private-callType`。这三个子项分别声明为 `xs:duration`、`minOccurs="0"`，没有 `default` 或 `fixed`。所以在共享类型里看得到字段，不等于它适用于两个分支，缺项也不能从这些声明读出一个值或回退规则。（§8.4.2.3）

§8.4.2.1 只在**在网**部分列无话权上限。§8.4.2.6 遇到离网 `private-call` 有这个子项时，原文写 `it shall be ignored`。**不能拿该项推离网无话权私呼已启用或上限生效。**这句没有另外明确要求删除整个 `private-call`、丢掉另外两个时长，或规定存储、整档验收和报错的先后。同一字段出现在正确的在网分支时，不触发这条离网例外。

## 静默预警与单次发话预警也不同

`transmit-time/time-limit` 和 `transmit-time/time-warning` 分别是该运行方式下组呼或私呼的**一次发话时限**，以及达到该时限前的警告时长。`hang-time-warning` 与 `private-call`、`transmit-time` 在同一个在网或离网配置块下，写的是达到 **Hang Time** 前的警告时长。（§8.4.2.3；§8.4.2.7 在网项 7–9、离网项 6–8）

当字段也出现在[在网 ad hoc 组呼](ad-hoc-broadcast-hang-time.md)时，先核完整路径。离网私呼的 `HangTime` 与 `MaxDuration` 分别指向 TS 24.483 §7.2.13、§7.2.12，这里不引入目标正文。配置字段不能代替[带话权私呼的业务要求](../calls/private-call-administration.md)、[在网单次发话到期和撤权](../calls/floor-permission-end-and-transmit-limit.md)或[离网静默后的呼叫终止](../calls/off-network-inactivity-call-termination.md)。这些字段不告诉你某次呼叫用了哪一份配置、何时启动计时或实际发了什么通知。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-private-call-service-timers.json)
