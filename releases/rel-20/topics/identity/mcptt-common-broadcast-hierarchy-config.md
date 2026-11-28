# MCPTT 共用广播配置：组层级数 B1 与用户层级数 B2

MCPTT 组广播组有几层，查 **B1**；用户广播组有几层，查 **B2**。两个数都在业务配置的 `common/broadcast-group`。它们分别数各自的层级，不数广播组、用户或同时发话的人，也不是给某个组或用户分配的具体级别。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.6/.7。§8.4.2.7 把 `common` 定义为在网、离网共享的数据；不要求同时出现两种模式的配置块。

## 两个可选字段各数什么

| `common/broadcast-group` 的子项 | §8.4.2.7 用途 | 本版所列引用 |
| --- | --- | --- |
| `num-levels-group-hierarchy` | 项 2：组广播组（group-broadcast groups）的组层级数 | B1，TS 22.179 [3] 附录 A；TS 24.483 [4] §7.2.7 `NumLevelGroupHierarchy` |
| `num-levels-user-hierarchy` | 项 3：用户广播组（user-broadcast groups）的用户层级数 | B2，TS 22.179 [3] 附录 A；TS 24.483 [4] §7.2.8 `NumLevelUserHierarchy` |

§8.4.2.1 的 `common` 项 2 在可选的 `broadcast-group` 中列出这两个子项。§8.4.2.3 在 `commonType` 下直接声明可选的 `broadcast-group`；其序列直接声明两个分别可选的 `xs:unsignedShort` 子项。父项和两个子项各为 `minOccurs="0"`，不含 `default` 或 `fixed`。没写某项不等于写了 0、4 或 6，截取内容没看到也不证明缺项。局部可省略不替代[整份 MCPTT 业务配置文档的结构校验](mcptt-service-config-structure-and-extensions-validation.md)。

## 语义无效时 CMS 要返回什么

§8.4.2.6 指定：任一字段的值语义无效时，**配置管理服务器（CMS）须返回 HTTP 409（Conflict），含 XCAP `constraint-failure`**；如带 `phrase`，建议用 `semantic error`。本条不列出 B1 或 B2 的业务有效区间。类型符合不证明语义有效；缺项、值无法辨认、以及只看到 409 或短语，也不足以确定某个 B1 或 B2 的值语义无效。

同一句还列 [N3 `min-length-alias`](mcptt-mcvideo-minimum-alias-length-config.md) 和[在网话权队列 `depth`](mcptt-on-network-floor-queue-config.md)。N3 大于 255 的专用条件及 `element value out of range` 不适用于 B1/B2；不能用数值 256 单独判这两个字段有效或无效。[MCPTT 合用的抢占层级字段](mcptt-override-priority-hierarchy-config.md)是 `num-levels-priority-hierarchy`，它的 4–256 限制和缺项取 4 也不移到本页。同节的范围块组合也可能用 `semantic error`，不能由响应倒推错误字段或多项报错时的处理顺序。

[MCVideo 的 Bc1/Bc2](mcvideo-service-priority-hierarchy-config.md)使用同名 XML 字段，但要按 MCVideo 本节与对应变量查，不能拿它的指向替换 MCPTT 的 B1/B2。两项外部引用只供定位，不据此补取值、算法、排队或授权规则。

## 两张 HTTP 响应示例都填 6

资料性附录 A 的**表 A.2.2-16** 和**表 A.2.3-12** 各显式填 B1=6、B2=6。它们展示怎么表达两个字段，不是默认值、要求两数相同或任一模式的规定值，也不能证明某次部署的配置或 CMS 接受行为。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-common-broadcast-hierarchy-config.json)
