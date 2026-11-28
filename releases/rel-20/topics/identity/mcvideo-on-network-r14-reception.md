# MCVideo 在网 R14：接收等待和接收者计数

先看计时针对什么。参与者已请求接收媒体，`reception-hang-time` 给的是服务器释放私呼前的等待；接收空闲时，T11 给的是终止媒体流前的等待。T6 配的是另一件事：重发 **Transmission Grant** 前的等待。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.1/.3/.6/.7。只查在网 MCVideo 业务配置，不从字段推断这次实际收发、计时起止或释放结果。

| 字段 | §9.4.2.7 在网项 18 所述用途 |
| --- | --- |
| `reception-hang-time` | (j) 参与者已请求接收媒体时，传输控制服务器释放该私呼前应等待的时长。 |
| `T6-reception-granted` | (k) 未收到 RTP 包 **或** 参与者失去发送许可时，传输控制服务器重发 Transmission Grant 前应等待的时长。原文没要求两个条件同时成立。 |
| `T11-stream-reception-idle` | (l) 接收空闲时，传输控制服务器终止该媒体流前应等待的时长。 |
| `C6-reception-granted`、`C7-reception-accepted` | (o)/(p) 分别是接收授予、接收接受的计数值，均指向 TS 24.581 [29]。 |
| `C11-media-receivers` | (q) 是媒体接收者数量计数器的最大值，同样指向 [29]；不是这次的实际接收人数。 |

`reception-hang-time` 不是项 18(f) 的 `private-call-hang-timer`，也不是 [T103 等接收请求的响应](mcvideo-on-network-r14-transmission-timers.md)。请求接收不等于已经收到媒体；接收空闲也不等于整通私呼结束。(k) 原印 **Transmission Grant**，不要因字段含 `reception` 改写成 Reception Grant，也不要套用 [T4 的 Transmission Granted](mcvideo-on-network-r14-transmission-retries.md) 和收到 Transmission Release 才截止的条件。没有抓到 RTP 不是服务器未收到 RTP 的充分证据；未见授权也不等于曾授予的许可已丢失。

(o) 没有明说 C6 控制 T6，不能从名字或 T4/C4 的明写关系补配，更不能从 C6/C7 判最多重发几次、是否计首发。C11 的值不是整网或某个组的用户上限，也不规定怎样清点、拒绝或处理超额。TS 24.581 在这里只作指向。

### C7 要看正在读哪一处

§9.4.2.1 在网项 6(d) 在可选 `anyExt` 内列出 `tc-timers-counters-R14`。§9.4.2.3 把 R14 写成独立全局元素，不是 `on-network` 的具名直接子项。R14 块若存在，表中前三个是必需的 `xs:duration`，后三个是必需的 `xs:unsignedByte`，均无 `default` 或 `fixed`；这不是块中的全部成员。

C7 在 §9.4.2.3 Schema 元素声明原写 **`C7-reception-accpeted`**，在 §9.4.2.1 结构清单、§9.4.2.6 (i) 范围校验和 §9.4.2.7 18(p) 用途里原写 **`C7-reception-accepted`**。两种字面各归原处，不能认作可互换标签、勘误或 CMS 会接受哪一种的结论。

### 同是 409，先核不合的是格式还是数值

| 查到的条件 | CMS 必须返回 | 如果带 `phrase`，原文建议 |
| --- | --- | --- |
| `reception-hang-time`、T6、T11 中任一值不符合 §9.4.2.6 后一份时长清单的格式 | HTTP 409（Conflict），含 XCAP `constraint-failure` | `invalid format for duration` |
| C6、C7 或 C11 的值不符合 §9.4.2.6 (h)–(j) 的 0 至 255 整数范围（含两端）；(i) 原拼写为 `accepted` | HTTP 409（Conflict），含 XCAP `constraint-failure` | `syntactically incorrect timer value`，且包含不合要求的标识；原文举 T101 为例，不规定拼接。 |

后一份时长清单的第 5–7 项要求按秒表示。表示式写 `PT<h>H<m>M<n>S`，其中 `<n>` 是有效秒值；格式校验句另写 `PT <n>S`。注 6 以 `PT0.3S` 表示 300 ms，不能用例子判 CMS 实际接受、空格或 H/M 怎么解析。该段没另写收到无效 `<n>` 的诊断，不从前一份时长清单移用，也不意味着无效值获准。缺必需标签不是已给出的坏值；同码不能反推出触发条件或处理先后。未知和重复另查 [MCVideo/MCData 通用文档校验](mcvideo-mcdata-service-config-validation.md)，不靠 C7 拼写差异直接分类。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-on-network-r14-reception.json)
