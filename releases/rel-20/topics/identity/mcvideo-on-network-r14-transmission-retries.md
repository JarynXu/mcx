# MCVideo 在网 R14：Idle、Revoke 和 Granted 重发

T3 和 T4 重发的不是同一条消息，原文写的截止消息却相同：**收到 Transmission Release**。C4 管 Transmission Granted 的**发送次数**；T2 的重发间隔和 C2 的计数值虽都写 Idle，本段没有明说 C2 控制 T2。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.1/.3/.6/.7。这里只查在网 MCVideo 的 R14 块，不把它换成 [MCPTT 的话权重发](mcptt-on-network-floor-message-retries.md)。

| 字段 | §9.4.2.7 在网项 18 所述用途 |
| --- | --- |
| `T2-transmission-idle` | (g)：没有任何 MCVideo 客户端获准传输时，Transmission Idle 消息的重发间隔。 |
| `T3-transmission-revoke` | (h)：Transmission Revoke 的重发间隔，直到收到 Transmission Release。 |
| `T4-transmission-granted` | (i)：传输控制服务器重发 Transmission Granted 前应等待的时间，直到收到 Transmission Release。 |
| `C2-transmission-idle` | (m)：Transmission Idle 计数值，指向 TS 24.581 [29]。本项未说明它如何用于 T2。 |
| `C4-transmission-granted` | (n)：Transmission Granted 计数值，指向 TS 24.581 [29]；(i) 明说它控制 Transmission Granted 的发送次数。 |

T2 的条件是**未授予传输权**，不是已经授予但暂时没有 RTP 包。T3 和 T4 不拿发出 Release、收到其他消息或整通结束替代本处的收件条件。(i) 明写传输控制服务器；不把这个主语补入 (h)。C4 的原文是发送次数，不写“最多重发几次”，也没交代首发是否计入或是否要加一。单看配置不能判断某次消息已发送或收到。TS 24.581 在这里只作指向。

### 同一配置块里，时长和计数分开

§9.4.2.1 在网项 6(d) 在可选 `anyExt` 内列出 `tc-timers-counters-R14`。§9.4.2.3 的 R14 块另有全局元素声明，不是 `on-network` 的具名直接子项。对于已出现的 R14 块，T2、T3、T4 三项是必需的 `xs:duration`，C2、C4 两项是必需的 `xs:unsignedByte`，都没有声明 `default` 或 `fixed`。五项在同一序列中，中间还有其他成员。[同块的 T100 至 T104](mcvideo-on-network-r14-transmission-timers.md)是整数秒值，不和这里的三项时长混用。

### 响应码相同，触发条件不同

§9.4.2.6 后一份 `xs:duration` 清单点名 T2、T3、T4，要求按秒表示。表示式原写 `PT<h>H<m>M<n>S`（`<n>` 是有效秒值），格式校验句另写 `PT <n>S`。该段注 6 用 `PT0.3S` 举例表示 300 ms。保留两处原写和例子，不从中裁定空格、小时或分钟的实际解析方式，也不保证例值一定被 CMS 接受。

| 查到的条件 | CMS 必须返回 | 如果带 `phrase`，原文建议 |
| --- | --- | --- |
| T2、T3、T4 任一已提供的值不符合该段所写结构 | HTTP 409（Conflict），包含 XCAP `constraint-failure` | `invalid format for duration` |
| C2 或 C4 的值不符合 R14 清单 (f)/(g) 的整数 0 至 255（含两端） | HTTP 409（Conflict），包含 XCAP `constraint-failure` | `syntactically incorrect timer value`，还包含不合要求的标识。原文称计时器标识，举 T101 为例，不指定拼接方式。 |

后一份时长清单没有像[前面含 ad hoc 组呼时长的清单](ad-hoc-broadcast-hang-time.md)那样另写“收到无效 `<n>`”的响应。不能把前一段的数值诊断搬来，也不因此判无效值获准。缺必需标签不等于已提供的值不符合；只有 409 也不能判断是哪条或处理优先级。C2/C4 的 0 和 255 在范围内，不说明默认值、实际次数或整份配置会被接受。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-on-network-r14-transmission-retries.json)
