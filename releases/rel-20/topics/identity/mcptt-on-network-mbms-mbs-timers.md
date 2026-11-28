# MCPTT 在网 MBMS 和 MBS：子信道释放与消息重发

**先查组会话用的是 MBMS 承载，还是 MBS 会话。**前者按承载查配置，后者按会话流查。静默计时决定何时要释放相应子信道；重发间隔与重发次数是另外的字段。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.6/.7。

| 查什么 | MBMS 承载 | MBS 会话 |
| --- | --- | --- |
| 组会话允许静默多久？ | `T15-conversation`：涉及 MBMS 承载的组会话在须释放 **MBMS 子信道**前，允许的最长静默（项 18）。 | `T25-mbs-conversation`：涉及 MBS 会话的组会话在须释放 **MBS 子信道**前，允许的最长静默（项 22）。 |
| 映射消息隔多久重发？ | `T16-map-group-to-bearer`：`Map Group To Bearer` 的重发间隔（项 19）。 | `T26-map-group-to-session-stream`：`Map Group To Session Stream` 的重发间隔（项 23）。 |
| 解映射消息隔多久重发，最多重发几次？ | `T17-unmap-group-to-bearer`：`Unmap Group To Bearer` 的重发间隔（项 20）。`C17-unmap-group-to-bearer` 是这条消息的最多重发次数（项 28）。 | `T27-unmap-group-from-session-stream`：`Unmap Group From Session Stream` 的重发间隔（项 24）。`C27-unmap-group-from-session-stream` 是这条消息的最多重发次数（项 30）。 |

### 不把子信道、组会话和消息算成一件事

T15/T25 只把静默界限连到各自**子信道**的释放。不能用这两项证明整通组呼结束、承载或 MBS 会话本身被释放，也不能把它们当成 [RTP 包间隔](mcptt-on-network-floor-rtp-timers.md) 或 [私呼的静默时长](mcptt-private-call-service-timers.md)。

这里把原名保留下来：MBMS 解映射仍写 `Unmap Group To Bearer`，MBS 解映射才写 `Unmap Group From Session Stream`。C17/C27 只管各自解映射的最多**重发**次数，不给映射消息补次数，也不规定初发如何算、等哪个确认、何时复位或是否成功。这些字段不同于 [Floor Idle、Floor Revoke 和 Floor Granted 的重发](mcptt-on-network-floor-message-retries.md)。

### 两个配置块

- **MBMS**：业务配置选了在网块时，基础 `<on-network>/<fc-timers-counters>` 是必需的。其中 T15、T16、T17 是必需的 `xs:duration`，C17 是必需的 `xs:unsignedShort`（§8.4.2.1 在网项 7 g/h/i/n、§8.4.2.3）。
- **MBS**：在网的 `<anyExt>` 可选，其中 `<R18-fc-timers-counters>` 也可选（§8.4.2.1 在网项 13 e）。若有这个 R18 块，其声明的四个子项都必需：T25、T26、T27 为 `xs:duration`，C27 为 `xs:unsignedShort`（§8.4.2.3 的单独全局元素及其类型）。它不是基础 `fc-timers-counters` 的必需子项，也不是在网类型直接声明的一个字段。没见 R18 块，不据此判断系统支持什么、选用了哪条路径或采用哪个默认值。

§8.4.2.6 的具名时长清单中，前一组 T 字段是项 16–18，后一组是项 20–22；C17/C27 不在清单内。要判格式问题和秒值问题，查[具名时长的两个校验分支](ad-hoc-broadcast-hang-time.md#缺项和校验怎么判)。这些字段的 Schema 声明未给默认值；附录 A 表 A.2.3-12 的数值是 HTTP 响应示例，不是缺项时自动采用的值。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-on-network-mbms-mbs-timers.json)
