# MCPTT 用户配置档：N2、N6、N7 分别数什么

在 MCPTT 用户配置档里，N2 数用户获准归属的组，N6 数用户同时接收的组呼，N7 数一次组呼中为抢占而同时接收的传输。三者都是配置上限。哪怕数值相同，计数对象也不同。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.3.2.1/.3/.6/.7。

| 本版配置路径 | §8.3.2.7 说明的上限 | §8.3.2.3 Schema 类型 |
| --- | --- | --- |
| `OnNetwork/MaxAffiliationsN2` | 告知 MCPTT 服务器：这个用户获准归属的 MCPTT 组数上限。语义段写 `nonNegativeInteger`。 | `xs:nonNegativeInteger` |
| `Common/MCPTT-group-call/MaxSimultaneousCallsN6` | 这个用户**同时接收的 MCPTT 组呼数**上限。语义段写 `positiveInteger`。 | `xs:positiveInteger` |
| `OnNetwork/MaxSimultaneousTransmissionsN7` | 告知 MCPTT 服务器：**一次** MCPTT 组呼中**同时接收的传输数**上限，原文限定 `for override`（用于抢占）。语义段写 `positiveInteger`。 | `xs:nonNegativeInteger` |

N2 不报告当前归属了几个组，也不证明某个新组获准归属。该句没规定应怎样合计显式和隐式归属；[按组查地址及组 ID](mcptt-user-profile-group-server-info.md)不提供这个计数。N6 不数用户发起的呼叫，也不等于功能别名的 `MaxSimultaneousEmergencyGroupCalls`。后者是每个指定别名的紧急组呼配置，与[别名服务配置的激活、接管和并发数](mcptt-functional-alias-service-config.md)也要分开。N6 的 XML 字段是 `MaxSimultaneousCallsN6`；§8.3.2.7 指向 TS 24.483 [4] §5.2.31 时印作 `MaxSimultaneouCallsN6`。保留两种原写，指向名不是第二个 XML 字段或接受规则。

N7 数同一次组呼内接收侧的传输，不数多通呼叫、发送人或获准发话的人数。配置值不证明谁被抢占、收到媒体或实际同时接收几路。[多发话者要求](../calls/group-multi-talker-control.md)、[ad hoc 多发话者配置](mcptt-on-network-adhoc-multi-talker-config.md)和[抢占优先级层级](mcptt-override-priority-hierarchy-config.md)按各自的对象读。

## 提纲、Schema 和 N7 的零值

§8.3.2.1 项 8(e)(i) 在必需的 `Common/MCPTT-group-call` 内列一个 N6；项 10(c/e) 先把 `OnNetwork` 写成零或一块，在该块出现时各列一个 N2 和 N7。§8.3.2.3 分别在 `MCPTTGroupCallType`、`OnNetworkType` 的 `0..unbounded` choice 中声明对应的具名直子项。三个局部声明都没有 default/fixed。局部 choice 不改写提纲，不等于整个用户档可任意缺项或接受重复值。

以 N7 的整数 0 为例：它符合 .3 声明的 `xs:nonNegativeInteger` 值域，不符合 .7 字面写的 `positiveInteger`。本版这两处不一致。它们都没解释 0 表示什么，也不能用其中一处断定系统接受或拒绝该文档。1 符合两处的数值类型，也不因此成为默认或证明整档通过。

§8.3.2.6 仍要求用户档符合 Schema，没有给 N2、N6、N7 各配专用的数值条件或 409。不能套[用户档优先级的 0 到 255 及 XDMS 诊断](mcptt-user-profile-priorities.md)、[其他用户档 XCAP 检查](mcptt-user-profile-xcap-validation.md)或[业务档的即时转发和授权计数](mcptt-on-network-service-authorization-forwarding-caps.md)。附录 A 的表 A.2.1-1、A.2.2-14 都明填 N2/N6/N7 为 3/3/1；两组相同的示例不是默认。缺项、空值、看不全与明填 0 分开，也不从一个上限补另一个。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-user-profile-count-limits.json)
