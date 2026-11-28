# MCVideo 与 MCData 在网 Resource-Priority：位置、等级与填头

**业务名决定先到哪里找。**TS 24.484 V20.1.0（Release 20，Stage 3）的在网业务档，MCVideo 和 MCData 都写紧急、紧迫险情、普通三个资源优先级块，但位置不同。

| 业务 | 三块在哪里 | 哪一条 |
| --- | --- | --- |
| MCVideo | 三个都是 `on-network` 的直接子元素，各必需一份；外层 `anyExt` 下的同名项不能代替。 | §9.4.2.1 在网项 3–5、§9.4.2.3。 |
| MCData | §10.4.2.1 在网项 4 的 `on-network/anyExt` 是可选块，正文在该块内列三类各一份。§10.4.2.3 把三个名称各自声明为全局元素，不是 `on-network` 的直接必需子元素。 | §10.4.2.1 在网项 4(a)–(c)、§10.4.2.3。 |

两业务的 `resource-priorityType` 都先有必填的 `resource-priority-namespace`，再有必填的 `resource-priority-priority`；两项都是 `xs:string`。其后可有声明的扩展。MCData 的外层 `anyExt` 在 Schema 中可省略；它用 `##any`、`lax` 通配，未逐名要求三项。与 `on-networkType` 直接序列里的 `##other` 不是同一处。不能用全局声明推成三块直接必填，也不能用外层通配证明空的扩展块或整档符合业务约束。

### 排序一样，原文的约束位置不全一样

- **MCVideo（§9.4.2.6）：**三块各用 RFC 8101 [20] 定义的 MCPTT 命名空间和规定的等级；紧急的等级高于或等于紧迫险情，后者高于或等于普通。
- **MCData（§10.4.2.6）：**比较的是两个字段值的“大于或等于”，对应同一组非严格顺序。该节对三块都写命名空间限制，对紧急和紧迫险情写 RFC 规定的等级。写完普通的命名空间后，没有再列普通等级一句；普通等级的 RFC 范围见 §10.4.2.1 在网项 4(c)(ii)，并不是可任填。

**相等只满足排序。**还要在各自业务的对应块核命名空间和等级。不能按 XML 字符串自行排字典序、补具体注册值或从这一段推专属 409。两节注 3 都说 RFC 8101 的 MCPTT 命名空间等级适用于所有 MC 业务，不要求各业务档同值。注 4 各要求本业务运营方与网络运营方仔细商定；MCData 在注 4 后重复这一点，不是再办一次批准。RFC 8101 在这里只作指向。

### 填 SIP `Resource-Priority` 时怎么选

| 场景 | 看哪个块 | MCVideo | MCData |
| --- | --- | --- | --- |
| 紧急呼叫／通信 | `emergency-resource-priority` | §9.4.2.7 在网项 5 | §10.4.2.7 在网项 9 |
| 紧迫险情（Imminent Peril）呼叫／通信 | `imminent-peril-resource-priority` | 项 6 | 项 10 |
| 从任一上述类别**降到普通优先级时** | `normal-resource-priority` | 项 7 | 项 11 |

从一开始就是普通，或只知当前普通，不能据这两项确定填头所用配置；也不等于其他条款禁止普通业务用头。这里不规定触发降级的程序、实际 SIP 消息或头的拼接格式。数值也不证明头已经发送或对端采用。

[MCPTT 的配置](mcptt-on-network-resource-priority-config.md)另查；不能只凭字段同名把两类档案的节点位置、选值或业务用途互换。若查 [MCVideo／MCData 参数块和文档校验](mcvideo-mcdata-service-config-validation.md)，另核该次操作和对应条件。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-mcdata-resource-priority-config.json)
