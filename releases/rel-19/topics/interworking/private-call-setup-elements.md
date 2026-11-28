# IWF 私呼建呼字段：被叫怎么寻址，应答说明什么？

**请求中的被叫 ID 和别名至少要带一个；两个都有时按被叫 ID 路由。** 应答里的请求结果、用户明确接受、话权参数可接受，是不同的事。

这里读 **TS 23.283 V19.5.0，Rel‑19 Stage 2**，只查 IWF↔MCPTT server 之间的 **IWF‑1 私呼建呼请求和应答**。两张表都列两个方向。主叫、被叫不随报文发送方向互换。表中 M 是必带，O 是可选，须连同表注读；查条文或已辨明的一条消息不必找齐全链。[§10.4.1.1，印刷页 89（PDF 第 90 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=90)。

## 请求：被叫身份和话权意图

| 要查什么 | IWF private call request（表 10.4.1.2-1） |
| --- | --- |
| **谁呼叫谁？** | 主叫 MCPTT ID **M**，主叫功能别名 **O**。被叫 MCPTT ID 和被叫功能别名各标 **O**，NOTE 1 要求这两项**至少带一个**，允许两个都带；两个都有时用被叫 ID 路由。主叫别名不能替被叫身份。仅别名路径怎么解析、核权，按相应建呼程序查；不因按 ID 路由就断言它不做别名校验。 |
| **是否用话权、是否同时申请？** | **Use floor control indication M** 写本通是否用话权控制；它必带不等于值一定为“用”。**Implicit floor request O** 写用户同时申请话权，NOTE 2 仅在发起客户端申请话权时允许携带。已知请求符合该表且该项出现，可知存在该申请；申请并不使该项变成必带。缺项不等于未申请，更不等于不用话权或被拒。 |
| **提了哪些媒体和加密条件？** | **SDP offer M** 是表所说的 MCPTT client 媒体参数。**Encryption mode M** 表明是否使用 E2EE；**Encryption Algorithm O** 填拟用算法，也能指示算法选择取自媒体流内信息。记录这些意图不等于算法已经协商好、媒体已加密或已建立。 |
| **还有哪些可选信息？** | **Requested commencement mode** 指拟用的开始模式，缺该项不能按此表补默认值。**Requested priority** 是请求的应用优先级，不是已经生效的优先级；**Location** 属主叫，不代表被叫位置或已获准转发。两个 true/false 项 **Transfer indicator** 和 **Forwarding indicator** 分别表示本请求是否由转接、前转产生。**Remotely initiated call request indicator** 表示因收到远程发起呼叫请求而产生，只能用于远程发起的呼叫；已知符合该表且确实带此项，可判断属于该场景，缺项不反推不是该类呼叫。 |

[§10.4.1.2、表 10.4.1.2-1 和 NOTE 1–3，印刷页 90（PDF 第 91 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=91)。

## 应答：结果、用户接受和参数可接受分别看

| 要查什么 | IWF private call response（表 10.4.1.3-1） |
| --- | --- |
| **哪方身份、哪次结果？** | 主叫 MCPTT ID **M**，被叫 MCPTT ID **O**；这张表没列功能别名，不套请求的身份二选至少一规则。**Result M** 是所应答私呼请求的成功或失败；**SDP answer M** 是选定的媒体参数。表没有把 SDP answer 的标记限定为成功时，也不能凭 SDP answer 说请求成功。 |
| **谁接受了什么？** | **Acceptance confirmation O** 表示用户是否明确接受，不能只看字段存在；它不替 Result。**Use floor control indication response O** 判断请求中“是否用话权控制”的指示是否可接受。**Implicit floor request response O** 判断请求中的隐式申请指示是否可接受。接受指示不等于该指示为 true，也不等于已取得话权或已发语音。 |
| **算法是否已经选定？** | **Encryption Algorithm(s) response O** 列一个或多个替代算法；读到列表不等于已选择或执行了其中某一项，也不据此证明 E2EE 生效。 |

两表的 **Additional application specific data O** 都在 LMR 系统使用该类数据时可以携带。GSM‑R 的 UUI 是例子，不是必带项、唯一格式或自动回显规则。应答有这个字段也不把它变成结束请求。[§10.4.1.3、表 10.4.1.3-1 和 NOTE，印刷页 91（PDF 第 92 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=92)。

例如，已辨明某应答是成功，并带可接受的隐式申请指示，但没有用户接受确认。可以说它**报告请求成功且认为该指示可接受**；不能补成用户明确接听、已授话权或已收到语音。只有要把消息关联到某次请求，才核同次呼叫和尝试、当事身份、接口两端与配对证据。向 IWF 或 server 发出不代表该端实收，更不证明另一个终端腿或媒体已通。实际采用[自动](private-automatic.md)或[手动](private-manual.md)流程，按该流程另查；[振铃与结束消息](private-call-ringing-and-end-elements.md)、[私呼加密](private-encryption.md)和[建呼后的话权](floor-control-owner.md)各有自己的判据。这里不定义 SIP／RTCP 编码、重试、默认值或策略。
