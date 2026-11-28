# MCPTT 用户配置档：私呼转接许可与目标名单

查能否请求私呼转接，用表 50 的 `allow-call-transfer`。查请求目标是否受名单限制，用表 51 的 `allow-call-transfer-to-any-user`。两表都写为该用户执行始发参与式 MCPTT 功能的服务器，但各管一件事。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.3.2.1/.3/.6/.7，表 8.3.2.7-50、51。本页查 MCPTT 用户配置档，不把[私呼来电转发或进行中转接的 Stage 1 条件](../calls/incoming-private-call-forwarding.md)加到这两个配置字段。

## 两种许可，各有一个缺项 false

| 表与字段 | `true` | `false` | 确认该元素未出现 |
| --- | --- | --- | --- |
| 表 50：`allow-call-transfer` | 表示该用户有权请求私呼转接。 | 指示服务器拒绝私呼转接请求。 | 本元素取 `false`。 |
| 表 51：`allow-call-transfer-to-any-user` | 表示该用户有权请求把私呼转接给任一 MCPTT 用户。目标为 MCPTT ID 或功能别名时，目标不受各自名单中 `entry` 的限制。 | 指示服务器拒绝向相应名单中没有条目的目标用户转接的请求。 | 本元素取 `false`，仍读本表的名单外拒绝。 |

表 51 的 `true` 不是表 50 已授权的证据。表 51 的 `false` 也不是全部拒绝；目标列在名单中不等于本次获准或转接成功。两表未写许可合并、先后、互相覆盖或回退规则。缺项指在对应配置中确认这个元素不存在，不是仅看片段没看到，也不是字段出现但值无效或名单没有条目。

## 两类名单的名称按出处保留

| 目标类型 | §8.3.2.1 项 10(g)(iv/v)、§8.3.2.3 和 §8.3.2.7 条目释义 | 表 51 原写的名单 |
| --- | --- | --- |
| MCPTT ID | `AllowedMCPTTIdsForCallTransfer` | `AllowedTargetMCPTTIDList` |
| 功能别名 | `AllowedFunctionalAliasesForCallTransfer` | `AllowedTargetFunctionalAliasIDList` |

§8.3.2.7 的条目释义把左列第一张名单的 `entry` 解释为可作私呼转接目标的 MCPTT ID，把第二张解释为可作目标的功能别名。表 51 则用右列两个名字说明名单限制。只按各处原写定位，不把两组名字改成拼写等价、两条已证实的 XML 路径或可互换元素。也不据此推断 [功能别名](mcptt-functional-alias-service-config.md) 怎么解析、ID 与别名如何比较，或某次实际查了哪张名单。

## 文档结构和条目次数分开查

§8.3.2.1 项 11(b)(xxxviii)(M/N)把两项许可列在 `ruleset/rule/actions/anyExt`；项 10(g)(iv/v)把左列的两张名单列在 `OnNetwork/anyExt`。提纲说后一处可含这些名单，每张已描述的名单含一个或多个 `entry`。用户档保留 `OnNetwork` 的大小写，不改成业务配置的 `on-network`。

§8.3.2.3 对两项许可各给一个全局 `xs:boolean` 声明，没有 `default` 或 `fixed`。两张名单各有全局 `ListEntryType` 声明；其 `xs:choice` 是 0 到不受限，可选择类型为 `EntryType` 的 `entry`。因此该局部 Schema 允许零个条目；若有 `entry`，其 `uri-entry` 必须给出，类型为 `xs:anyURI`，而 `display-name` 可省略。显示名不替代目标标识。这个局部声明不判定完整配置会接受空名单，不给省略名单后的权限，不表示 XML 会补写任何布尔值。§8.3.2.6 有通用 Schema 要求，无本页两许可或两名单的专用 409；其他[用户配置档的 XCAP 约束](mcptt-user-profile-xcap-validation.md)按各自条件查。

## 别把转接名单当成转发目标

[用户档私呼转发](mcptt-user-profile-private-call-forwarding.md)另查单独的目标值、目标种类、启用、条件和许可。[在网业务档的即时转发次数上限](mcptt-on-network-service-authorization-forwarding-caps.md)不是转接许可以及所列名单的大小。[在网 ad hoc 组呼转发](../calls/ad-hoc-group-call-forwarding.md)也有独立的 Stage 1 条件。

TS 24.484 将表 50、51 两字段分别对应到 TS 24.483 [4] §5.2.48T1 `AllowedCallTransfer`、§5.2.48T2 `AllowedCallTransferAny`。它同时说明前述两张名单的条目未出现在所指 MCPTT 用户配置管理对象中。TS 24.379 [9] 只作表 50、51 的程序指向；不以两份指向补消息流程、校验顺序或实际结果。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-user-profile-private-call-transfer.json)
