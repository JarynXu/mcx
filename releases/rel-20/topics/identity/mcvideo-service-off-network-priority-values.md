# MCVideo 离网私呼：ProSe 与 PQI 配置值

查离网私呼的优先级配置，先认父块，再区分普通或紧急、信令或媒体。ProSe 和 PQI 有四个同名字段，不是共用一份值。ProSe 的校验句写的是同一个值同时小于 1 **且**大于 8；PQI 的句子则把 `other than` 印了两遍。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.1/.3/.6/.7 和规范性附录 §C.4.2。这里的离网是业务配置的 `off-network`，不是说如何用外部设备离线配置终端。

### 同名字段要连父块读

§9.4.2.1 离网项 1 和 3 分别列 `default-prose-per-packet-priority`、`default-pqi`。两者是 `off-network` 下不同的直接子项。§9.4.2.3 把两个父块及各自的四个具名字段都声明为可选；这里的八个局部字段均为 `xs:unsignedShort`，未声明 `default` 或 `fixed`。字段名以 `default-` 开头，不表示缺块或缺字段时已有一个指定数值。

§9.4.2.7 离网项 1(a–d) 和 4(a–d) 分别给出两组字段的用途。同名字段的指向也相同，但要在实际父块下读值。下表中的“普通”只是与带 `emergency` 的字段名相对，不是现场判定应急状态的额外条件。

| 两个父块各自的字段 | 用途 | TS 24.483 [4] 对应元素和条款 |
| --- | --- | --- |
| `mcvideo-private-call-signalling` | 普通私呼信令 | `MCVideoPrivateCallSignalling`，§14.2.12 |
| `mcvideo-private-call-media` | 普通私呼媒体 | `MCVideoPrivateCallMedia`，§14.2.13 |
| `mcvideo-emergency-private-call-signalling` | 紧急私呼信令 | `MCVideoEmergencyPrivateCallSignalling`，§14.2.14 |
| `mcvideo-emergency-private-call-media` | 紧急私呼媒体 | `MCVideoEmergencyPrivateCallMedia`，§14.2.15 |

TS 24.483 在这里仅作指向，不据此判两个字段的实际值相同或能互作回退。私呼总时长、抢占层级和[在网 Resource-Priority](mcvideo-mcdata-resource-priority-config.md)是其他条目，不把那些字段的缺项规则带进来。

### 两条校验的触发条件不能互换

**ProSe。** §9.4.2.6 原句是 `less than 1 and greater than 8`，两边比较的是任一子字段中的同一个值。这个标量不能同时满足两边；即使一个字段是 0、另一个是 9，也没有一个值同时满足原句。不能擅换成 OR，也不能因此宣称 0 或 9 必被接受或没有别的校验。紧接的注 2 只谈 ProSe：数值越大，给信令或媒体的优先级越高。它不约束 PQI 的数值顺序，也不证明现场排序、调度或获准。

**PQI。** 同一节写的是 `other than other than`，随后列出 21–26、55–61、90–93 三段含端点的区间。可以查一个值是否在列举里：26 在，27 不在。重复的词后没有第二组值或另一条比较条件，不把它修成另一版规则，也不读成“在区间内反而错误”。数值在不在列举里，不等于已证明该次 CMS 接受或拒绝。

两条原句各写明：该条条件成立时，CMS 须返回 HTTP 409（Conflict），含 XCAP `constraint-failure`；如带 `phrase`，建议 `element value out of range`。这不是必带短语，也不能靠一个已见的 409 反推出触发原因。基础 XML 类型、各条所列条件和实际实现分开查。

### 5GS 对应关系不是数值换算

规范性附录 §C.4.2 在通用 MC Service over 5G ProSe 的语境下，把离网 `default-pqi` 的 PC5-5QI 写成 `default-prose-per-packet-priority` 的 5GS 对应项。它没给某个 ProSe 数值换算出哪个 PQI，也不判实际 MCVideo 呼叫用了哪个配置、先读哪块或缺项怎么回退。[MCPTT 的离网值](mcptt-service-off-network-priority-values.md)和[抢占层级配置](mcptt-override-priority-hierarchy-config.md)只作对照。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-service-off-network-priority-values.json)
