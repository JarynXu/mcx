# MCVideo 的广播层级数与离网抢占层级

广播组的两个层级数在 `common/broadcast-group`；离网传输的抢占层级在 `off-network`。只有在已确认的离网块内知道这个字段缺失，才按原文取最小值 **4**；不为广播的 Bc1 或 Bc2 补 4。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.1/.3/.6/.7。这里讨论 MCVideo 业务配置，不从配置证明终端或服务器某次授予结果。

### 广播组先分 Bc1、Bc2

`common` 是可选块，数据供在网、离网共用，不表示一份配置必须同时带两个模式块。§9.4.2.1 的 `common` 项 2 在可选 `broadcast-group` 内列出下表两个字段；§9.4.2.3 对父项和两个子项均声明 `minOccurs="0"`。两个子项均为 `xs:unsignedShort`，没有这里离网字段专用的 4–256 限制，也未声明 `default` 或 `fixed`。缺一个字段不等于填 0 或 4；不凭这组局部声明判断整份配置可接受。

| 字段 | §9.4.2.7 在 `common` 的用途 | 本版所列变量与引用 |
| --- | --- | --- |
| `num-levels-group-hierarchy` | 项 2：组广播组（group-broadcast groups）的组层级数 | Bc1，TS 22.280 [30] 附录 E；用途对应 TS 24.483 [4] §14.2.7 的 `NumLevelGroupHierarchy`。 |
| `num-levels-user-hierarchy` | 项 3：用户广播组（user-broadcast groups）的用户层级数 | Bc2，TS 22.280 [30] 附录 E；用途对应 TS 24.483 [4] §14.2.8 的 `NumLevelUserHierarchy`。 |

两项是层级数，不是组数、用户数或某人被赋的优先级。两个规范仅作指向；本页不据此填写 Bc1、Bc2 的取值表。

§9.4.2.6 写明：若这两个字段或 `min-length-alias` 中有语义无效的值，CMS 须返回 HTTP 409（Conflict），含 XCAP `constraint-failure`；如带 `phrase`，建议用 `semantic error`。邻段的 `min-length-alias > 255` 数值规则另有适用对象，不给 Bc1/Bc2 加一个 255 上限。字段未出现、类型合规、已知语义无效是不同问题。只看到 409 或短语不足以定位到本条件；[文档结构校验](mcvideo-mcdata-service-config-validation.md)另查。

### 离网抢占层级：4 的条件是已知字段缺失

§9.4.2.1 的 MCVideo 离网结构提纲未列 `num-levels-priority-hierarchy`。§9.4.2.3 却明确在 `off-network` 下声明这个可选的具名直接子项：`priorityhierarchyType` 以 `xs:unsignedShort` 为基础，限制为 **4 至 256（含两端）**，无 `default` 或 `fixed`。

确认相关 `off-network` 块存在，且能确认这个字段没有出现时，§9.4.2.7 离网项 3 明说用 Schema 所允许的最低值，即 4。不是因 XSD 自动补了一个标签。若整块不在、只看了片段、或者字段有值但不合类型或范围，都不能当作这种缺项；显式 4 则是已给配置，不是触发缺项取值的证据。§9.4.2.6 的通用 Schema 一致性仍适用，但本节没为该离网字段单列诊断；不移用广播层级数的 `semantic error`。

同一项说明该层级用于确定针对**正在进行的离网 MCVideo 传输**，哪些参与者、参与者类型和紧急传输类型的抢占请求应获准，并指向 TS 24.483 [4] §14.2.18 的 `NumLevelHierarchy`。不由层级数补具体排序、角色赋权、抢占算法或本次获准。也不把它换成[离网私呼的 ProSe/PQI 值](mcvideo-service-off-network-priority-values.md)、[在网 Resource-Priority](mcvideo-mcdata-resource-priority-config.md)或 [MCPTT 的独立抢占配置](mcptt-override-priority-hierarchy-config.md)。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-service-priority-hierarchy-config.json)
