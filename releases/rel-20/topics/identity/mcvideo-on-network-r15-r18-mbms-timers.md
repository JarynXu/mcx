# MCVideo 在网 R15/R18：子信道静默与映射重发

T300 和 T310 提供子信道释放前的静默上限；另四个字段提供具名消息的重发间隔。虽然 T310 与 session stream 的映射字段同在 R18 块，T310 的原文仍写 **MBMS bearer** 和 **MBMS subchannel**。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.1/.3/.6/.7。R15、R18 是本版在网 MCVideo 配置扩展块的名称，不是拿两个不同 Release 的规范相拼。

| 配置块 | 字段 | §9.4.2.7 在网项 19/20 所述用途 |
| --- | --- | --- |
| R15 | `T300-transmission` | 19(a)：涉及 MBMS bearer 的组会话中，必须释放 MBMS subchannel 前的最长允许静默。 |
| R15 | `T301-map-group-to-bearer` | 19(b)：Map Group To Bearer 的重发间隔。 |
| R15 | `T303-unmap-group-to-bearer` | 19(c)：Unmap Group To Bearer 的重发间隔。 |
| R18 | `T310-transmission` | 20(a)：同样原写涉及 MBMS bearer 的组会话及必须释放 MBMS subchannel 前的最长允许静默。 |
| R18 | `T311-map-group-to-session-stream` | 20(b)：Map Group to session stream 的重发间隔。 |
| R18 | `T312-unmap-group-from-session-stream` | 20(c)：Unmap Group from session stream 的重发间隔。 |

两条静默定义的对象相同，不代表两个字段的配置值相同，也不能把 T310 的 MBMS 改成 MBS。释放的是子信道，不是整个组会话；不能换成 [ad hoc 组呼中两次发话之间的静默](ad-hoc-broadcast-hang-time.md)或 [R14 的接收流空闲](mcvideo-on-network-r14-reception.md)。

映射和解除映射各有自己的消息。R15 解除映射的消息也写 **To Bearer**，R18 才写 **from session stream**。这些项没有规定首发、确认、重发次数或计时起止。不从 [MCPTT 的 MBMS/MBS 计时与计数](mcptt-on-network-mbms-mbs-timers.md)搬入 C17/C27，配置值也不能证明这次已经重发、释放或收到确认。

### 每个块各查自己的三个必需时长

§9.4.2.1 在网项 6(e)/(f) 把两块列在可选的外层 `anyExt` 内。§9.4.2.3 中 `tc-timers-counters-R15` 和 `tc-timers-counters-R18` 各是独立的全局元素，不是 `on-network` 的具名直接子项。对应块出现时，各自的三个具名时长须按序列存在，类型都是 `xs:duration`，未声明 `default` 或 `fixed`。每块另有可选的内层 `anyExt`，和本类型的 `##other` 元素通配项。外层可选不代表块内时长可省；两组六个时长也不是要求两块必须一起出现或某份配置必被接受。

### 六个时长都查后一份格式清单

§9.4.2.6 后一份 `xs:duration` 清单的第 8–13 项点名这六个字段，要求按秒表示。表示式原写 `PT<h>H<m>M<n>S`，其中 `<n>` 是有效秒值；格式校验句另写 `PT <n>S`。注 6 以 `PT0.3S` 举例表示 300 ms，不据此认定具体 CMS 的空格、小时、分钟或小数解析结论。

给出的值不合该段结构时，CMS 须返回 HTTP 409（Conflict），含 XCAP `constraint-failure`；如带 `phrase`，建议 `invalid format for duration`。缺必需标签不是已给值的格式问题。这里不移用前一份时长清单另列的无效 `<n>` 诊断，也不套 R14 的 0 至 255 整数范围诊断；同一个 409 不能识别现场违反了哪一条。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-on-network-r15-r18-mbms-timers.json)
