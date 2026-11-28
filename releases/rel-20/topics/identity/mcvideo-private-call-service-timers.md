# MCVideo 私呼：离网整通上限与在网 R14 挂起计时

查 MCVideo 私呼的时长，先分模式。**离网** `mcvideo-max-duration` 是整通私呼允许的最长时长。**在网** R14 `private-call-hang-timer` 是私呼的挂起计时值。两项都声明为 `xs:duration`，但不共用全部校验条件。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.1/.3/.6/.7。本页只查 MCVideo 业务配置。

## 配置位置、拼写与用途

| 问什么 | 在业务配置里查哪里 | 用途 |
| --- | --- | --- |
| 离网私呼最长多久 | `off-network/private-call/mcvideo-max-duration`。§9.4.2.1 离网项 2(a) 列出这条路径；§9.4.2.3 把 `private-call` 和其内的时长字段各自声明为可选。字段无 `default` 或 `fixed`。 | §9.4.2.7 离网项 2(a)：离网私呼允许的最长时长。只指向 TS 24.483 [4] §14.2.17；这里不补目标元素名、时长默认值或到期后动作。 |
| 在网私呼的挂起计时值 | §9.4.2.1 在网项 6(d)(vi) 在可选 `anyExt` 的 R14 块里原写 `private-call-hang-time`。§9.4.2.3 将 `tc-timers-counters-R14` 声明为全局元素，块内的必需子项原写 `private-call-hang-timer`，无 `default` 或 `fixed`。§9.4.2.6 和 .7 也用后者。 | §9.4.2.7 在网项 18(f)：在网 MCVideo 私呼的挂起计时值。未规定本计时器何时启动、重置或到期后怎么处理，也未指向 TS 24.581。 |

两种挂起字段写法分别保留。不能从拼写差异判定 CMS 接受哪一种、两者可作别名，或产生另一条支持的路径。R14 是 `on-network/anyExt` 所列的块，不是 `on-network` 的具名直接子项；块内必需不等于整份配置必带 R14。离网项或字段可选，也不表示缺项就不限时、补零或沿用在网值。现有材料只有片段时，不能确认值已配或确知缺项。

若要查“参与者已请求接收媒体，传输控制服务器释放私呼前等多久”，读 [R14 接收等待](mcvideo-on-network-r14-reception.md)的 18(j) `reception-hang-time`，不把这个条件移给 18(f)。[在网 ad hoc 组呼](ad-hoc-broadcast-hang-time.md)注 3 所述同通连续发送之间的静默也不替代私呼用途。只看到配置值，不能判断某次计时、释放或终止是否发生。

## 收到 409 时查哪份清单

两份清单都要求时长按秒表示。正面表示句写 `PT<h>H<m>M<n>S`，其中 `<n>` 是有效秒值；格式校验句另写 `PT <n>S`。注 5 和注 6 都举 `PT0.3S` 表示 300 ms 的例子。例子不裁定 CMS 实际接受的小数、空格或 H/M 写法，也不给出诊断顺序。

| §9.4.2.6 的具名字段 | 触发条件 | CMS 必须返回 | 如带 `phrase`，建议用 |
| --- | --- | --- | --- |
| 前一份时长清单第 1 项：离网 `mcvideo-max-duration` | 已给的时长值不符合该清单的格式 | HTTP 409（Conflict），含 XCAP `constraint-failure` | `invalid format for duration` |
| 同一前段 | 收到无效的 `<n>` 值 | HTTP 409（Conflict），含 XCAP `constraint-failure` | `invalid value for duration` |
| 后一份时长清单第 1 项：在网 R14 `private-call-hang-timer` | 已给的时长值不符合该清单的格式 | HTTP 409（Conflict），含 XCAP `constraint-failure` | `invalid format for duration` |

后一份清单后单列的时长 409 只写格式不符。这里仍要求有效秒值并遵循通用 Schema，不能据此断定无效值会被接受或不受校验。R14 有自己的一份[整数定时字段清单](mcvideo-on-network-r14-transmission-timers.md)，其 0–255 规则不套到本页的 `xs:duration`。前段另有在网 ad hoc 的 `hang-time`、`max-duration-of-call`，不是只查离网的清单。后段另列 13 项。只有缺标签、只有 409 或只有一个诊断短语，都不能证明发生了这里的坏值条件。

另查 [R15/R18 的组会话与映射计时](mcvideo-on-network-r15-r18-mbms-timers.md)、[MCPTT 私呼配置](mcptt-private-call-service-timers.md)或 [MCVideo 离网抢占层级](mcvideo-service-priority-hierarchy-config.md)。后者的缺字段取最低层级不用于私呼时长。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-private-call-service-timers.json)
