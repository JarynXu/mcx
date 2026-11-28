# MCPTT 在网 Resource-Priority：配置范围与字段选择

**看要填哪类呼叫的 SIP `Resource-Priority` 字段，再查业务配置。**TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.7 在网项 35–37 分三种用途。

| 当时是哪一种 | 看哪个配置块 |
| --- | --- |
| MCPTT 紧急呼叫 | 项 35：`emergency-resource-priority`。 |
| MCPTT 紧迫险情呼叫（Imminent Peril） | 项 36：`imminent-peril-resource-priority`。 |
| 从上述任一类型降到普通优先级 | 项 37：`normal-resource-priority`。这句写的是降级，不凭“普通”二字套到从一开始就是普通优先级的呼叫。 |

这里说明按什么配置填头字段，不指明何时或由谁发起降级、用哪条 SIP 消息发送、怎样拼接字面值，也不保证头字段已发出、网络已采用或触发了抢占。

### 配置结构与等级限制分开查

- **结构：**§8.4.2.1 在网项 9–11 要求三类各有一份，都是 `on-network` 的直接子元素，不放到外层 `anyExt` 里代替；不随某次呼叫只留一类。§8.4.2.3 将三块声明为 `resource-priorityType`；每块按 Schema 序列依次含一个 `resource-priority-namespace` 和一个 `resource-priority-priority`，都是必填的 `xs:string` 子元素。其后仍可有 Schema 声明的扩展。XML 顺序看 Schema，不以结构说明的项目顺序代替。上层[范围组合检查](mcptt-service-config-structure-and-extensions-validation.md)也不能代替这一步。
- **等级：**§8.4.2.6 要求**每块**的命名空间为 RFC 8101 [20] 指定的 MCPTT 命名空间，等级在该 RFC 规定的范围内。等级关系是**紧急 ≥ 紧迫险情 ≥ 普通**，两处都允许相等；相等只满足排序，仍须单独查命名空间和等级是否合法。不能把 `xs:string` 当作任意字符串获准，也不能由类型推出字典序、纯数字比较或三个命名空间必须相同。
- **取值与报错：**§8.4.2.6 注 3 说明 MCPTT 运营方与网络运营方需要仔细商定这些值。这段约束未给这三类字段单独指定 HTTP 409 或 `phrase`。资料性表 A.2.3-12 在网配置响应示例对同一块的两个子项印作相同字符串；示例不是等级定义、默认值、必然通过 .6 或 SIP 头字段格式。RFC 8101 这里只作源文引用，不摘取具体值或拼接规则。

[抢占优先级层级](mcptt-override-priority-hierarchy-config.md)用的是另一组配置。SIP 资源优先级字段不表示参与者的抢占级别，也不能证明某次话权操作或资源分配。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-on-network-resource-priority-config.json)
