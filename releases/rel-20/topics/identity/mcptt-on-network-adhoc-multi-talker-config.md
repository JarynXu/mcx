# MCPTT 在网 ad hoc 组呼：多发话者开关与人数

在网 MCPTT ad hoc 组呼能否使用多发话者，查 `adhoc-multi-talker-control`。允许多发话时能有多少发话者，查 `adhoc-multi-talker-max-talkers`。人数缺项的 **1** 是后者的语义默认，不会打开多发话者支持，也不是实际发话人数。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.7。在网 ad hoc 业务配置以外的行为不由这两个字段判断。

## 两层扩展和两个字段

§8.4.2.1 在网项 13(d)(vi/vii)把两个字段都列在 `on-network/anyExt/adhoc-group-call/anyExt` 的**内层** `anyExt`。在网的外层 `anyExt` 以及其中的 `adhoc-group-call` 在提纲里各是可选。§8.4.2.3 的 `on-networkType` 和 `adhoc-group-callType` 各自声明可选的 `anyExt`；两者使用 `anyExtType` 的 `##any`、`lax` 元素通配。这与两个父类型序列中各自的 `##other`、`lax` 通配不同。

| 字段 | §8.4.2.3 全局声明 | §8.4.2.7 用途和 TS 24.483 [4] 指向 |
| --- | --- | --- |
| `adhoc-multi-talker-control` | `xs:boolean` | 项 52：在网 ad hoc 多发话者支持启用或禁用；§7.2.34 `AllowAdhocMultiTalker` |
| `adhoc-multi-talker-max-talkers` | `xs:positiveInteger` | 项 53：允许多发话者时的允许发话者数量；§7.2.35 `MaxNoTalkers` |

两个全局声明均无 `default` 或 `fixed`，也都不是 `adhoc-group-callType` 序列里具名的直接子项。通配不规定这两个名字各要出现多少次，也不证明某个写法会被接受。项 52 明写内层 `anyExt`；项 53 的字面父链直接写 `adhoc-group-call`，**未列内层 `anyExt`**。这是语义段的印写与结构提纲的差别，不据此另立直挂路径、别名或 CMS 处理规则。

## 缺人数时的 1 不给开关取值

项 53 先定义允许多发话者时的人数，然后写**人数元素不存在时取 1**。查这个条文不需要实时开关或呼叫记录。判断某份配置是否缺人数，看相关完整配置；片段里未见、人数字段显式写 0 或写入无效值都不等于缺项。1 不来自 XSD，也不表示存档时要补写，更不能推断控制元素缺项取 `true` 或 `false`，或有人已经获准发话。项 52 所说的启用、禁用是配置含义，不单凭它判断本次实收音频或授予话权。

## 一般 ad hoc 支持和参与者人数另查

- `allow-adhoc-group-call-support` 是**一般在网 ad hoc 组呼支持**。§8.4.2.6 写它的语义默认 `true`，并把**整个** `adhoc-group-call` 块不在解释为系统不支持 ad hoc 组呼。不能用人数缺项的 1 补一整个支持块。§8.4.2.3 在已出现的 `adhoc-group-callType` 中把该支持字段和 `max-no-participants` 声明为必需的直接子项；语义默认不替代这项 Schema 声明。一般支持、挂起时长及其校验见[在网广播 ad hoc 组呼](ad-hoc-broadcast-hang-time.md)。
- `max-no-participants` 是项 48 的允许**参与者**人数；项 53 数允许的**发话者**。两项同为正整数类型，不等于两数相同，也不能从这两项推出数值关系、实际入会或抢占结果。

§8.4.2.6 的通用 Schema 一致性仍适用，但未为这两个多发话字段单列 409 条件或短语。查[缺项、组合和收到重复项](mcptt-service-config-structure-and-extensions-validation.md)要看各自条件。两项 TS 24.483 引用只供定位。已配置的[在网多发话者组的抢占、发话申请结果和降上限](../calls/group-multi-talker-control.md)是另一层；[ad hoc 组呼转发](../calls/ad-hoc-group-call-forwarding.md)和 [MCData 组数据](mcdata-on-network-adhoc-group-data-config.md)也各有适用范围。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-on-network-adhoc-multi-talker-config.json)
