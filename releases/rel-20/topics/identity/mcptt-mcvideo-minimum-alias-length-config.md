# MCPTT 与 MCVideo：用户名称最小长度 N3

`common/min-length-alias` 给出管理员分配给本业务用户的字母数字名称的最小长度（N3）。MCPTT 查 MCPTT 业务配置，MCVideo 查 MCVideo 业务配置。字段可省略；显式填 0 和未写是两种证据，**未写不表示默认 0**。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.6/.7 与 §9.4.2.1/.3/.6/.7。下文的 `common` 数据供各自业务的在网、离网共用，不是跨业务共用一份配置，也不要求两种模式块同时出现。

## 先找对业务与字段

| 业务 | 声明与用途 | 管理对象指向 |
| --- | --- | --- |
| MCPTT | §8.4.2.1 的可选 `common` 项 1 与 §8.4.2.3 声明可选直接子项 `min-length-alias`。§8.4.2.7 的 `common` 项 1 指 MCPTT 管理员分配给 MCPTT 用户的字母数字名称。 | TS 24.483 [4] §7.2.9 `MinLengthAliasID` |
| MCVideo | §9.4.2.1 的可选 `common` 项 1 与 §9.4.2.3 声明可选直接子项 `min-length-alias`。§9.4.2.7 的 `common` 项 1 指 MCVideo 管理员分配给 MCVideo 用户的字母数字名称。 | TS 24.483 [4] §14.2.9 `MinLengthAliasID` |

两处 Schema 的此子项都直接声明 `xs:unsignedShort`、`minOccurs="0"`，未给 `default`、`fixed` 或这个子项专用的 255 上界 facet。查到局部可选，不表示整份配置可以只剩空块，也不能从片段中没看到断定实际缺项。[MCPTT 全文档结构](mcptt-service-config-structure-and-extensions-validation.md)和 [MCVideo 全文档结构](mcvideo-mcdata-service-config-validation.md)另查。

两节 §.6 均把 N3 指向 TS 22.179 [3] 附录 A；表中的 TS 24.483 也只作定位。这里不补命名算法、允许字符细则、长度计算单位或实际赋名结果。不把 N3 当作用户 ID 的长度、功能别名 URI 规则、激活名单、优先级或 MCData 规则。若问题是功能别名，按业务去 [MCPTT](mcptt-functional-alias-service-config.md)、[MCVideo](mcvideo-on-network-functional-alias-config.md)或 [MCData](mcdata-on-network-functional-alias-config.md)的在网配置。

## 409 要区分哪条条件

§8.4.2.6（MCPTT）与 §9.4.2.6（MCVideo）各自把 N3 的值写为 **0–255**。255 是 N3 配置值的上界，不是名称的最大长度。专用数值条件是已给的 `common/min-length-alias` 值 **大于 255**，不是“大于等于”。0、255 不触发这个条件，256 触发；这不判断词法、整个文档是否合法，或 CMS 实际会怎样处理。缺字段、负值和无法读出数值也不能直接用这条 `>255` 判错。

| 核实的条件 | 两处规定 CMS 必须返回 | 如带 `phrase`，建议用 |
| --- | --- | --- |
| 本业务 `common/min-length-alias` 的值大于 255 | HTTP 409（Conflict），含 XCAP `constraint-failure` | `element value out of range` |
| 本业务 `common/min-length-alias` 的值语义无效 | HTTP 409（Conflict），含 XCAP `constraint-failure` | `semantic error` |

数值在 0–255 内，不足以证明语义有效，更不能说 0 准许空名称。MCPTT 同句另列广播的 B1/B2 和 [在网话权队列 `depth`](mcptt-on-network-floor-queue-config.md)，MCVideo 同句另列 [广播的 Bc1/Bc2](mcvideo-service-priority-hierarchy-config.md)，未列 `depth`。这些字段不继承 N3 的数值边界。语义无效查对应业务和字段，不因共用 409 或短语就倒推具体问题，也不在两个谓词重叠时替原文规定先后。

## 附录的 5 与 12 不是默认值

本版资料性附录 A 的两份 **MCPTT** HTTP 响应示例都明确带了此字段：表 A.2.2-16 的值是 5，表 A.2.3-12 的值是 12。它们是写进示例的值，不是缺项的回退、在网和离网各自的规定值，也不是 MCVideo 的样例。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-mcvideo-minimum-alias-length-config.json)
