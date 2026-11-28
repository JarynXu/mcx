# MCVideo 在网功能别名：条目、优先级与授权上限

要查别名能被同时激活几次，看**这个别名**的 `max-simultaneous-activations`。要查一个人能同时有几份业务授权，看 `max-simultaneous-authorizations`。两者数的对象不同。

依据是 3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§9.4.2.1/.3/.7 的在网 MCVideo 业务配置。字段说明的是配置含义，不是这次激活、接管或授权的结果。

### 两套文字都保留

| 要查什么 | 原文所写 |
| --- | --- |
| 列表的上层与条目数 | §9.4.2.1 在网项 6(a) 在可选的外层 `anyExt` 内列 `functional-alias-list`，说列表含一个或多个 `functional-alias-entry`。§9.4.2.3 则全局声明列表，该列表类型的条目是 `0..unbounded`。 |
| 一个已出现的条目 | §9.4.2.3 的序列声明四个必需的具名字段：`functional-alias`（`xs:anyURI`）、`max-simultaneous-activations`（`xs:positiveInteger`）、`allow-takeover`（`xs:boolean`）、`mcvideo-user-list`（`mcvideosc:ListEntryType`）。列表和条目各有自己的可选 `anyExt`。 |
| 别名优先级的位置 | §9.4.2.1 项 6(a)(i)(E) 和 §9.4.2.7 项 12 都将 `functional-alias-priority` 列在条目内。§9.4.2.3 不把它声明成条目的第五个具名字段，而是单独全局声明为 `xs:positiveInteger`。 |

`0..unbounded` 只说 Schema 里局部条目的基数，不能拿来覆盖结构文字的“一个或多个”或保证空列表被接受。全局声明、条目内的可选 `anyExt` 和 `##other` 通配项也不提供一个经证实的优先级落点。不要替两处原文选出新写法、判某个扩展合法，或因差异本身断定是未知元素、重复元素或会报 409。

### 字段的对象和动作分开看

| §9.4.2.7 在网项 | 配置描述 |
| --- | --- |
| 8 `functional-alias` | 功能别名自身的身份，类型是 URI。 |
| 9 `max-simultaneous-activations` | 这个别名允许的并发激活数量。 |
| 10 `allow-takeover` | 对**已激活**的这个别名，是否允许**另一位 MCVideo 用户**接管。 |
| 11 `mcvideo-user-list/entry` | 可激活这个别名的 MCVideo 用户的 MCVideo ID。 |
| 12 `functional-alias-priority` | 这个别名的相对优先级。该项注 2 把 MCVideo 服务器怎样使用该参数留给实现。 |
| 13 `max-simultaneous-authorizations` | 每位 MCVideo 用户可同时拥有的业务授权数量上限。项 6(b) 和本项把它写在外层 `anyExt`，与列表同级，不在别名条目内；Schema 有自己的全局 `xs:positiveInteger` 声明。 |

项 11 把用户项类型写作 `entryType`；Schema 中 `mcvideo-user-list` 用 `mcvideosc:ListEntryType`，它的 `entry` 用 `mcvideosc:EntryType`。列表类型的本地选择项是 `0..unbounded`，并不免除别名条目内具名用户列表。确有一个 `entry` 时，`uri-entry` 必需，`display-name` 可选。显示名不是 MCVideo ID；用户 ID 和别名 URI 也不是同一个标识。

在允许名单里、配置允许接管、别名已激活、已经成功接管是不同的证据。注 2 不规定排序方向、平局算法或自动接管。两项上限都是正整数，但不从类型推出实际计数、超额处理或专用 409。

[MCPTT 功能别名](mcptt-functional-alias-service-config.md) · [MCData 功能别名](mcdata-on-network-functional-alias-config.md) · [通用文档校验](mcvideo-mcdata-service-config-validation.md)

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-on-network-functional-alias-config.json)
