# MCPTT 在网功能别名：身份、激活与接管配置

**一条配置看一个功能别名。**别名 URI 说明配置指向哪个别名；允许激活它的人用另一处 MCPTT ID 指定。以下是 TS 24.484 V20.1.0（Release 20，Stage 3）在网业务配置 §8.4.2.7 的项 40–44，不是某次请求的处理结果。

| 查什么 | 查这一项 |
| --- | --- |
| 是哪个别名？ | 项 40：`functional-alias` 用 `anyURI` 表示这一条的别名身份。 |
| 谁被列为可激活？ | 项 43：同一条的 `mcptt-user-list/entry` 表示允许激活该别名的用户 MCPTT ID。§8.4.2.7 将条目类型写成 `entryType`；§8.4.2.3 声明 `mcpttsc:EntryType`，其中 `uri-entry` 是必填的 `xs:anyURI`，可选的 `display-name` 不是 ID。 |
| 同时可以激活几次？ | 项 41：`max-simultaneous-activations` 是该别名允许的并发激活数，用正整数。项 45 的 `max-simultaneous-authorizations` 数一个用户可同时拥有的业务授权，项 46 的 `max-immediate-forwardings` 数允许的即时呼叫转发。两项都和别名列表并列，不是这个别名的上限。 |
| 已激活的别名可否让别人接管？ | 项 42：`allow-takeover` 是布尔值，表示另一个 MCPTT 用户是否可接管**当前已激活的这个别名**。它与允许谁激活、可同时激活几次是三个不同的问题。 |
| 别名之间有相对优先级吗？ | 项 44：可在**条目自己的** `anyExt` 中配置正整数 `functional-alias-priority`。它表示该别名的相对优先级；注 3 把 MCPTT 服务器怎样使用这个参数留给实现。这里没有规定数值比较方向或接管结果。 |

§8.3.2.7 表 8.3.2.7-46 另有用户配置字段 `allow-takeover-functional-alias-other-user`。它面向为该用户执行参与功能的 MCPTT 服务器，表示该用户是否获准接管别人先前激活的别名。它不是项 42 的逐别名开关。本页不从任一配置推算组合判定、缺项默认或实际激活、接管。

### 文档结构和 Schema 分开看

在网块的外层 `anyExt` 可省略；在其中设置 `functional-alias-list` 时，可以列多条 `functional-alias-entry`。§8.4.2.1 在网项 13(a) 写列表含 **一条或多条**；§8.4.2.3 的列表 Schema 对该元素写的是 **`minOccurs="0" maxOccurs="unbounded"`**。一个没有 `functional-alias-entry` 的列表满足 Schema 对这个子元素的次数声明，但不能据此说它符合 §8.4.2.1、会获 CMS 接收或能使用。两处文字均支持多个条目；[CMS 的重复项校验](mcptt-service-config-structure-and-extensions-validation.md)不能只拿节点同名来判断。

一条已出现的 `functional-alias-entry` 在 Schema 序列里要求别名 URI、并发激活上限、接管开关和用户列表容器。容器本身必填，不等于至少存在一个用户条目：`ListEntryType` 的选择组允许零次。没有列出的用户 ID，不能用空列表推成允许任意用户。别名优先级所在的可选 `anyExt` 在条目内，不是承载整个列表的在网外层。

别名的相对优先级也不等于用于[活动发话抢占的优先级层级](mcptt-override-priority-hierarchy-config.md)。两者配置对象不同。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-functional-alias-service-config.json)
