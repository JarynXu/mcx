# 在网广播 ad hoc 组呼：挂起时长用哪个配置字段？

**广播组呼有自己的配置字段 `broadcast-hang-time`。**在 MCPTT 和 MCVideo 的**业务配置文档**里，它与 `hang-time` 并列。只找到后者，不能据此判定广播值已配、等于普通值、或缺项时会沿用普通值。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）。只核两项业务的**在网** ad hoc 组呼配置，不能套到离网或 MCData。

## 先看业务文档，再区分两个字段

两种文档都在 `on-network → anyExt → adhoc-group-call` 下列出这两个字段，分别由各自业务的 Schema 定义。

| 业务 | `hang-time` | `broadcast-hang-time` |
| --- | --- | --- |
| **MCPTT** | 在网 ad hoc 组呼的挂起时长。§8.4.2.7 项 49 指向 TS 24.483 §7.2.32 的 `HangTime`。 | 在网**广播** ad hoc 组呼的挂起时长。§8.4.2.7 项 50 指向 TS 24.483 §7.2.36 的 `BroadcastHangTime`。 |
| **MCVideo** | 在网 ad hoc 呼叫的挂起时长。§9.4.2.7 项 16 指向 TS 24.483 §14.2.24 的 `HangTime`。 | 在网**广播** ad hoc 组呼的挂起时长。§9.4.2.7 项 16A 指向 TS 24.483 §14.2.26 的 `BroadcastHangTime`。 |

这里用“普通字段”指 `hang-time`，不是在替规范定义它与广播字段的运行优先顺序。邻项 `max-duration-of-call` 是呼叫允许的总时长，不是挂起时长。

## 缺项和校验怎么判

- **只缺广播字段。**两个字段的 XSD 声明都是 `xs:duration`、各自 `minOccurs="0"`，没有声明默认值。在完整的对应配置块中只有普通字段时，只能说广播字段未写。整块 `adhoc-group-call` 未出现则不同：两处校验条款均把整块缺失解释为该业务不支持 ad hoc 组呼；其中给出的默认 `true` 属于支持开关，不是任何时长的默认值。（§8.4.2.3/.6；§9.4.2.3/.6）
- **报格式问题。**§8.4.2.6 和 §9.4.2.6 的具名时长验证清单都列了 `hang-time`，没列 `broadcast-hang-time`。同为 `xs:duration` 不等于广播字段自动获得普通字段清单中的细化格式或 HTTP 409 规则。业务配置仍须符合各自的 Schema；不能据此宣称广播字段无需校验，或补写单位、取值范围及缺项回退。

只看**各清单已列的字段**，原文先描述 `PT<h>H<m>M<n>S`，检查格式的一句另写 `PT <n>S`。保留两种原文写法，不把它们改成一条验值规则。

- MCPTT 的 25 项清单与 MCVideo 的 3 项清单后，原文分别说明两种错误：格式不符或 `n` 值无效。两种都回 HTTP 409，含 `constraint-failure`。若带诊断 `phrase`，前者建议 `invalid format for duration`，后者建议 `invalid value for duration`。
- MCVideo 的另一份 13 项清单后，只明写格式不符的 HTTP 409 和上述格式诊断，没有另写无效 `n` 的响应。三份清单都没列广播字段，不能据此给它规定报错。

这几处条文区分的是配置字段，不给出计时器何时启动、重置、到期后释放呼叫或话权等运行规则。TS 24.483 的对应号只作原文索引，这里未核其正文。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](ad-hoc-broadcast-hang-time.json)
