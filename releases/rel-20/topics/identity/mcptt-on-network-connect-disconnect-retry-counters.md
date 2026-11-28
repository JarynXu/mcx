# MCPTT 在网 Connect / Disconnect：重发间隔与两组计数说明

**重发间隔有明确字段；次数不能只凭本版这四项定用哪个计数器。**计时器段交叉引用了两个计数器，计数器各自的说明却按消息同名对应。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.6/.7。下表项号均为 §8.4.2.7 在网项。

| 消息 | 重发间隔 | 计时器段说哪个计数器控制重发次数 | 计数器自身哪一段定义这条消息的最多重发次数 |
| --- | --- | --- | --- |
| `Connect` | `T55-connect`，项 25 | `C56-disconnect`，项 25 | `C55-connect`，项 31 |
| `Disconnect` | `T56-disconnect`，项 26 | `C55-connect`，项 26 | `C56-disconnect`，项 32 |

项 25/26 说「控制重发次数」，项 31/32 说「最多重发次数」。两组原文的指向不同，本页不选一组覆盖另一组，也不把它们合成两个计数器共同控制一条消息。这里核的是配置与消息名称，不是整通呼叫接通或拆除、SIP/TCP 的连接、初发如何计或实际重发结果。

### 字段、类型和示例各自能说明什么

业务配置选了在网块时，四项在必需的 `<on-network>/<fc-timers-counters>` 中，§8.4.2.1 在网项 7 k/l/p/q 与 §8.4.2.3 都列出。T55、T56 是必需的 `xs:duration`，C55、C56 是必需的 `xs:unsignedShort`；这些声明没有默认值。§8.4.2.6 具名时长项 23、24 是 T55、T56，不是 C55/C56。格式和秒值要分开查[具名时长的两个校验分支](ad-hoc-broadcast-hang-time.md#缺项和校验怎么判)。

附录 A 表 A.2.3-12 是 HTTP 响应示例：T55/T56 都是 `PT2S`，C55/C56 都是 `3`。这组相同值区分不了两种计数指向，也不是缺项默认值。XML 中的字段类型、字段名或示例值，都不能补出该版在上述两组文字间未定的归属。

[在网话权消息重发](mcptt-on-network-floor-message-retries.md)与 [MBMS/MBS 映射消息重发](mcptt-on-network-mbms-mbs-timers.md)各按自己的字段核，不借那些计数器解释这两条消息。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-on-network-connect-disconnect-retry-counters.json)
