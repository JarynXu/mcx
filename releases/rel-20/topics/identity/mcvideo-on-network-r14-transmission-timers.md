# MCVideo 在网 R14：T100 至 T104 的字段与取值

T100 至 T104 是 MCVideo 在网业务配置中的五项整数秒值，放在 `on-network/anyExt/tc-timers-counters-R14`。读 T102 不要靠字段名猜计时用途；读 T103 则要分清结构正文和 Schema 的不同拼法。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.1/.3/.6/.7。这里的 R14 是配置块名。五项都指向 TS 24.581 [29]，本页只保留引用，不用被引规范的正文补运行细节。

| 字段（按 Schema） | §9.4.2.7 在网项 18(a)–(e) 所述用途，单位均为秒 |
| --- | --- |
| `T100-transmission-request` | 用于传输请求。 |
| `T101-transmission-end-request` | 用于传输结束请求。 |
| `T102-queue-position-request` | 原文说用于 RTP 媒体结束（`end of RTP media`），虽然字段名包含 `queue-position-request`。 |
| `T103-receive-media-request` | 等待接收媒体请求消息的响应，或等待用户取消该请求。 |
| `T104-receive-media-release` | 等待接收媒体释放消息的响应。 |

T100 和 T101 各说一种请求，不能互换，也不能据字段名推重发或请求已经发出。T102 保留名称和原文用途两处信息；不能只凭名称说它等待排队位置，也不据“RTP 媒体结束”补计时起点、停表或结束动作。T103 对应接收请求，还写了用户取消；T104 对应释放请求的响应，条文本项未写用户取消分支。不由此判设备如何处理取消、超时或是否真的释放媒体。

### 配置块与 T103 的两种写法

§9.4.2.1 在网项 6(d) 在可选 `anyExt` 里列出 `tc-timers-counters-R14`。§9.4.2.3 的 `on-networkType` 声明可选 `anyExt`；R14 块另有全局元素声明，不是 `on-network` 的具名直接子项。核对一个出现的 R14 块时，这五项按 T100 到 T104 的次序必需，各是 `xs:unsignedByte`，没有声明默认值或固定值。五项不是 R14 的全部成员，也不能从外层可选推出五项在块内可省略。

T103 在 §9.4.2.1 项 6(d)(iv) 原写 `T103-receive-media-requset`，而 §9.4.2.3 的声明、§9.4.2.6 的范围清单和 §9.4.2.7 的语义都写 `T103-receive-media-request`。按各自条文保留原写，不把不同拼法认成别名、第二个已声明字段或已核定的勘误。

### 取值不符时查整数范围，不查 PT 时长格式

§9.4.2.6 的 R14 范围清单 (a)–(e) 要求这五项为 0 至 255 的整数，含两端。任一具名值不符合所列范围，CMS 必须返回 HTTP 409（Conflict），含 XCAP `constraint-failure`。如果带 `phrase`，原文建议写 `syntactically incorrect timer value` **并包含不符合要求的计时器标识**，以 `T101-transmission-end-request` 为例；未指定拼接格式。只看到 409 不能反推是哪一项，也不能把缺必需子项当成已有值越界。

同一范围清单另有 R14 计数器 (f)–(j)，不是这里的秒值说明。另列的 `xs:duration` 字段使用另一段格式校验，不能把其 `PT` 表示法或诊断搬给 T100 至 T104。0 或 255 在范围内不等于默认、关闭、立即到期或整份文档被接受。本页不代替 [MCVideo 在网广播组呼时长](ad-hoc-broadcast-hang-time.md)、[MCPTT 话权消息重发](mcptt-on-network-floor-message-retries.md) 或 [MCPTT 在网 RTP 计时配置](mcptt-on-network-floor-rtp-timers.md)。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-on-network-r14-transmission-timers.json)
