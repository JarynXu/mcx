# MCData 在网功能别名：谁可激活、并发数与接管

一条 `functional-alias-entry` 对应一个功能别名。别名 URI 标识这个别名，MCData ID 标识获准激活它的用户。并发激活数、已激活时可否由他人接管、别名相对优先级是三项配置，不能相互替代。

以下依据 TS 24.484 V20.1.0（Release 20，Stage 3）§10.4.2.1/.3、§10.4.2.7 在网项 14–18 和注 2。这里只查 MCData 业务配置。

| 要查什么 | 同一别名条目中的字段 | 语义 |
| --- | --- | --- |
| 哪个别名 | `functional-alias` | 项 14：功能别名的身份，`xs:anyURI`。 |
| 同时可激活几次 | `max-simultaneous-activations` | 项 15：对应别名允许的并发激活数，`xs:positiveInteger`。0 不满足该类型，不表示不限。这里数的不是现有激活数，也不是项 13 一个用户可同时拥有的业务授权数。 |
| 可由另一位 MCData 用户接管吗 | `allow-takeover` | 项 16：布尔项，指示是否允许另一位 MCData 用户接管这个**当前已激活**的别名。不是该用户的通用权限，也不证明本次已接管。 |
| 哪些用户被列为可激活 | `mcdata-user-list/entry` | 项 17：条目包含获准激活这个别名的用户的 **MCData ID**。不是别名本身或显示名。 |
| 这个别名的相对优先级 | `functional-alias-priority` | 项 18：`xs:positiveInteger`。注 2 只把 MCData 服务器怎样使用这个参数留给实现；不是整份别名配置都由实现定义，也不规定比较方向、平局或接管结果。 |

### 别名列表与条目内的用户列表，是两层次数

§10.4.2.1 在网项 4(e) 在可选 `anyExt` 里列 `functional-alias-list`，写它含一条或多条 `functional-alias-entry`。§10.4.2.3 另有列表的全局声明，`on-networkType` 声明的是可选 `anyExt`，不是具名直接的别名列表。Schema 把 `functional-alias-entry` 声明为 0 到 `unbounded`。零条不因这项 Schema 次数约束被排除；不能据此改掉正文的一条或多条或判 CMS 会接收整档。[通用重复项校验](mcvideo-mcdata-service-config-validation.md)仍需查实际条件，多个同名条目不等于收到重复项。

条目一旦存在，上表五个具名子项在 Schema 中按该顺序必需，包括 `mcdata-user-list` **容器**和与它并列的 `functional-alias-priority`。容器必需不等于名单必有一个用户：`mcdatasc:ListEntryType` 的 `xs:choice` 允许零次。仅凭这个结构不能断言空名单可激活，或把没列的用户判为获准或拒绝。[MCPTT 条目](mcptt-functional-alias-service-config.md)的优先级在条目自己的可选 `anyExt`，不要照搬到 MCData。

### 两处原文与 Schema 的写法分别保留

- **并发数的父项。**项 15 从子到父字面写 `max-simultaneous-activations → functional-alias-entry → functional-alias → functional-alias-list`。§10.4.2.1 4(e) 和 §10.4.2.3 则把并发数与别名 URI 列为同一 `functional-alias-entry` 的**并列字段**。并发数语义仍是对应别名允许的并发激活数；不据项 15 另立 XML 路径或猜标准勘误。项 13 的 `max-simultaneous-authorizations` 数一个 MCData 用户同时可有的业务授权，是外层 `anyExt` 下的同级配置，不在别名条目内。
- **用户条目的类型。**项 17 原写 `entryType`。Schema 将 `mcdata-user-list` 声明为 `mcdatasc:ListEntryType`，其中的 `entry` 才是 `mcdatasc:EntryType`，含必需的 `uri-entry`（`xs:anyURI`）和可选的 `display-name`。不把容器类型写成条目类型，也不把两种大小写当成可换用的 Schema 名称。

这些字段不规定用什么算法选人、容量满时怎么处理、多个用户争用时如何接管，或服务器实际用了哪一个优先级。注 2 不延伸到相邻的[通知服务器主机名](mcdata-on-network-notification-server-config.md)。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcdata-on-network-functional-alias-config.json)
