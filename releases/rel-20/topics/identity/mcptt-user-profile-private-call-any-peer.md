# MCPTT 用户配置档：始发与终接的任意私呼对端

问「这个用户可以向谁发起 MCPTT 私呼」，查始发侧表 27。问「这个用户可以接收谁发来的私呼请求」，查终接侧实际表 48。两个字段各管自己的方向，分别有缺项 `false`。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.3.2.1/.3/.6/.7，表 8.3.2.7-27 和实际表 8.3.2.7-48。这里查 MCPTT 用户配置档，不用该档推断实际放行、送达或应答。

## 始发查目标，终接查来话方

| 原文与字段 | 哪个服务器功能读 | `true` | `false` 或确认该元素缺项 |
| --- | --- | --- | --- |
| 表 27：`allow-private-call-to-any-user` | 为该用户执行始发参与式 MCPTT 功能 | 用户可请求向任一 MCPTT 用户发起私呼，不受 `PrivateCall` 所述 `entry` 中列出的收件人限制。 | 指示服务器拒绝私呼请求。 |
| 实际表 48：`allow-to-receive-private-call-from-any-user` | 为该用户执行终接参与式 MCPTT 功能 | 用户获准接收私呼请求，不限于 `IncomingPrivateCallList` 所述 `entry` 中的发起方，可以来自任一 MCPTT 用户。 | 指示服务器拒绝私呼请求。 |

这两条 `false` 都没有「仅拒绝名单外」的条件。即使对端已列名，也不因此改变该表的拒绝说明。[私呼转接](mcptt-user-profile-private-call-transfer.md)表 51 的名单外条件只用于该项转接配置。不能用对端表、名单命中或一个 `true` 覆盖另一个字段，也不推两表怎样组合、谁先执行。配置片段看不到字段、字段存在但值异常、没有名单条目，都不等于确认这个元素缺失。

## 两个动作字段和两张名单是不同位置

§8.3.2.1 项 11(b)(xxvii)在 `ruleset/rule/actions` 直属列始发字段；11(b)(xxxviii)(K)在 `ruleset/rule/actions/anyExt` 列终接字段。§8.3.2.3 各有全局 `xs:boolean` 声明，没有 `default` 或 `fixed`。表 27、48 的缺项是各自的语义取值，不是 Schema 或服务器补写 XML。§8.3.2.6 的通用 Schema 要求仍适用；未给这两个字段或这两张名单专用 409。

| 目标方向 | 提纲位置 | §8.3.2.7 所述 `PrivateCallURI` |
| --- | --- | --- |
| 发给谁 | `Common/PrivateCall/PrivateCallList`，项 8(d)(i)写零个或多个所列子项。 | 可以向其发起私呼的 MCPTT 用户 ID；对应 TS 24.483 [4] §5.2.17 的 `MCPTTID`。 |
| 接收谁发来的 | `OnNetwork/anyExt/IncomingPrivateCallList`，项 10(g)(iii)写一个或多个所列子项。 | 可以接收其私呼的 MCPTT 用户 ID；对应 TS 24.483 [4] §5.2.48Y4 的 `MCPTTID`。 |

§8.3.2.3 分别为 `PrivateCallList` 和 `IncomingPrivateCallList` 使用 `PrivateCallListEntryType`，其局部 `xs:choice` 为 `0..unbounded`，列有 `PrivateCallURI`，其 `EntryType` 中必需的 `uri-entry` 为 `xs:anyURI`，`display-name` 可省。共享类型还列 `PrivateCallProSeUser`。入向提纲仍写一个或多个所列子项，不把这个共享类型子项或其他出向子项搬进入向提纲，也不从类型声明推来话许可。表 27/48 写 `entry`，提纲、Schema 和条目释义用 `PrivateCallURI`。不能据此把两个名字当 XML 别名、改写层级，或判空名单、缺名单、名单匹配与整档接受。

## 来话导语引表 28，实际标题是表 48

§8.3.2.7 对来话字段的导语确实印「表 8.3.2.7-28」。紧接的字段值表标题为「表 8.3.2.7-48」，而实际表 28 的标题写 `allow-regroup`。找来话 `true`、`false` 和缺项值看表 48，保留导语错号，不把重组规则带过来。私呼参与表 29 和未确认组呼邀请用户信息表 49 也不是这项许可。

TS 24.484 将出、入两个字段分别指向 TS 24.483 [4] §5.2.14 `AuthorisedAny`、§5.2.48X `AuthorisedIncomingAny`；TS 24.379 [9] 只作程序指向。两份引用不补协议、名单匹配算法或现场结论。若查[私呼管理中的目标范围](../calls/private-call-administration.md)、[终端真的应答没有](../calls/private-call-commencement-evidence.md)、[带话权私呼条件](../calls/floor-controlled-private-call-basics.md)或[来电怎样转发](../calls/incoming-private-call-forwarding.md)，读各自的 Stage 1；[用户档的私呼转发字段](mcptt-user-profile-private-call-forwarding.md)也保留独立入口。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-user-profile-private-call-any-peer.json)
