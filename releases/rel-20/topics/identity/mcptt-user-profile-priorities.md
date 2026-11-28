# MCPTT 用户配置档：组的呈现优先级与用户的呼叫优先级

在 MCPTT 用户配置档里，`RelativePresentationPriority` 属于某个模式下的组条目；`Priority` 属于该用户的共用呼叫配置。三个具体字段位置都要求整数 0 到 255（含两端）。先看路径和模式，不能用数字或相同的错误文字辨认字段。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.3.2.1/.3/.6/.7。下面的 TS 24.483 [4] 条号和字段名只作定位。

| 配置位置 | §8.3.2.7 的用意 | TS 24.483 [4] 指向 |
| --- | --- | --- |
| `OnNetwork/MCPTTGroupInfo/entry/anyExt/RelativePresentationPriority` | 这个在网组相对于其他**在网组和在网用户**的呈现优先级。 | §5.2.48B7 `RelativePresentationPriority` |
| `OffNetwork/MCPTTGroupInfo/entry/anyExt/RelativePresentationPriority` | 这个离网组相对于其他**离网组和离网用户**的呈现优先级。 | §5.2.53B `RelativePresentationPriority` |
| `Common/MCPTT-group-call/Priority` | 这个 MCPTT 用户用于**发起和接收 MCPTT 呼叫**的优先级。原句写 MCPTT calls，不能仅凭容器叫 `MCPTT-group-call` 把原句改成只写组呼，也不从该句推出私呼的使用过程。 | §5.2.44 `Priority` |

组条目比较同一模式下的组和用户，不跨在网、离网合排。§8.3.2.7 不定义数字方向、同值排序或比较算法，也没说用 `Common/Priority` 一类简写替代这三个路径。

## Schema 不用同一个类型

- **按组**：§8.3.2.1 的通用条目提纲允许 `entry/anyExt` 含 `RelativePresentationPriority`，它和 [GroupServerInfo](mcptt-user-profile-group-server-info.md) 同属该扩展的具名项目，不在服务器地址块里。§8.3.2.3 全局元素使用 `PriorityType`，以 `xs:nonNegativeInteger` 为基础，显式 `minInclusive=0`、`maxInclusive=255`。组条目的可选 `anyExt` 有自己的 `##any/lax` 声明，不据此补节点或判定整档通过。
- **按用户**：§8.3.2.1 项 8(e)(v) 在 `Common/MCPTT-group-call` 提纲里写零或一个 `Priority`。§8.3.2.3 在 `MCPTTGroupCallType` 的 `0..unbounded` choice 中把它列为具名直子项，类型为 `xs:unsignedShort`，无 default/fixed。§8.3.2.7 数据语义段写 `nonNegativeInteger`。两处各保留原写；不拿局部 choice 改写提纲次数，也不因类型能表示更大的数就扩大该字段允许值。

例如，整数 256 已超出组的 `PriorityType`；它可以由用户项的 `xs:unsignedShort` 表示，但仍违反用户项的 §8.3.2.6 取值要求。0 和 255 是数值界限，不是最高、最低或缺项默认值的说明。

## 哪个值超出范围？

§8.3.2.6 分别检查在网组条目、离网组条目、`MCPTT-group-call` 的用户 `Priority`。确认为上述某一路径的值超出 0 到 255 时，XDMS 须返回 HTTP `409 Conflict`，含 XCAP `constraint-failure`。若带 `phrase`，条文建议写 `Priority value out of range`，不要求每次都带。该节指向 RFC 4825 [14]；不借引用内容给这三个条件补处理顺序。

缺项、片段看不全、类型或格式有问题，不都等于已确认了一个越界整数。看到 409 或同一短语，也不能反推出是哪条路径、几个值出了问题或先处理哪项。[用户档的 XCAP 校验](mcptt-user-profile-xcap-validation.md)还列有其他 409 条件。

本页只查用户配置值。服务配置的 [Resource-Priority 组与报头](mcptt-on-network-resource-priority-config.md)、[抢占优先级层级](mcptt-override-priority-hierarchy-config.md)、[多发话者要求](../calls/group-multi-talker-control.md)各有自己的对象和条件。用户档的数字不证明填了哪个报头、谁拿到话权、谁被抢占或实际怎样呈现。另查[私呼 KMS 条目](mcptt-user-profile-private-call-kms-uri.md)时按其地址规则，不借本页的数字校验解释空值。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-user-profile-priorities.json)
