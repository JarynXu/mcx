# MCData 离网一对一：ProSe 逐包优先级与 PQI

MCData 离网一对一的信令和媒体，在 ProSe 逐包优先级与 PQI 中各有字段。两块里的子项同名，**先查父块，再查信令或媒体**。ProSe 原句的两个比较用 AND 相连，PQI 则检查给定值是否在三段列举区间之外。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§10.4.2.1/.3/.6/.7。只查 MCData 离网业务配置的一对一字段，不套用 [MCVideo](mcvideo-service-off-network-priority-values.md) 或 [MCPTT](mcptt-service-off-network-priority-values.md) 的私呼四类字段，也不用于判断在网 `Resource-Priority`。

## 同名子项要连父块查

§10.4.2.1 离网项 1 和 2 分别列出可选的 `default-prose-per-packet-priority` 与 `default-pqi`，两块各列下表的两个子项。§10.4.2.3 把两块都声明为 `off-network` 的可选直接子项；每块各自的两个子项都是可选 `xs:unsignedShort`。共四个局部声明。父项和子项均无 `default` 或 `fixed`，字段名里的 `default` 不等于缺项时自动补值。局部可省略不证明整份文档通过校验，另查 [业务配置文档结构](mcvideo-mcdata-service-config-validation.md)。

| 两个父块均列的字段 | §10.4.2.7 用途 | TS 24.483 [4] 指向 |
| --- | --- | --- |
| `mcdata-one-to-one-call-signalling` | MCData 离网一对一信令的优先级值 | §11.2.11 `MCDataOneToOneSignalling` |
| `mcdata-one-to-one-call-media` | MCData 离网一对一媒体的优先级值 | §11.2.12 `MCDataOneToOneMedia` |

指向相同不等于两个父块的值相同、互相回退或已经生效。§10.4.2.6 的 PQI 条件和 .7 离网项 2 印作 `<default-pqi >`，尖括号内末尾有空格；.1 和 .3 的名称是 `default-pqi`。两处印写不构成第二个 Schema 字段，也不能据此判定实际 XML 接受或拒绝。

## 两条 409 条件要分开读

**ProSe。** §10.4.2.6 原句是 `less than 1 and greater than 8`，比较的是同一个子项的同一个数值。它不可能同时小于 1 且大于 8；信令填 0、媒体填 9 也不满足。不能改成 OR，也不能从原句反推 0 或 9 会被接受。紧邻的注 2 只说明 ProSe 数值越大，信令或媒体的相对优先级越高；不用于 PQI，也不证明实际发放、调度或接收。

**PQI。** §10.4.2.6 只有一个 `other than`。列出的区间是 **21–26、55–61、90–93**，都含端点。任一所列 PQI 子项的数值在这些区间之外，才满足这条专用条件。26 在列举内，27 不在。单看命中列举不能推出格式、语义或整份配置合规，也不使用 MCVideo 原文的重复写法。

两条各写明其条件成立时，**CMS 须返回 HTTP 409（Conflict），含 XCAP `constraint-failure`**；如带 `phrase`，建议 `element value out of range`。这不是短语必带，也不能从 409 倒推是哪条触发。缺项、语法问题、所给值不在列举内、某次有响应分别取证，不替条文补处理顺序。

§C.4.2 可用于对照：在 5GS 中，离网 `default-pqi` 的 PC5-5QI 是 ProSe 逐包优先级的对应项。它不提供逐值换算、优先选择或缺项回退。[在网 Resource-Priority 的字段与填头](mcvideo-mcdata-resource-priority-config.md)另查。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcdata-service-off-network-priority-values.json)
