# MCPTT 用户配置档：私呼 KMS URI 与空值回退

查私呼 KMS URI，先确定是去话还是来话，再分名单共用和某个 MCPTT ID 的条目。只有确认**同方向名单级的 `uri-entry` 存在且为空**时，§8.3.2.7 才在这里写使用 MCS 初始配置档中的 KMS。个人项出现的条件是其 URI 与本方向名单中的 URI 不同；这不要求每个不同 URI 都必须写个人项。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.3.2.1/.3/.7；§8.3.2.6 仅核此用户档的通用 Schema 约束。本页说明配置里的联系地址，不判断本次私呼许可、实际连接或取钥匙结果。

## 去话不拿来话的名单

| 方向 | 按 §8.3.2.1 提纲定位 | 名单和个人分别指什么 |
| --- | --- | --- |
| 去话 | `Common/PrivateCall/PrivateCallList` | 名单级 URI 用来联系此名单 `PrivateCallURI` 所列 MCPTT ID 关联的 KMS；个人项只针对其中对应的目标 ID。TS 24.483 [4] §5.2.19B `PrivateCallKMSURI` 只作引用定位。 |
| 来话 | `OnNetwork/anyExt/IncomingPrivateCallList` | 名单级 URI 用来联系此名单 `PrivateCallURI` 所列 MCPTT ID 关联的 KMS；个人项只针对对应来话方 ID。TS 24.483 [4] §5.2.48Y5 `PrivateCallKMSURI` 只作引用定位。 |

名单级扩展属于名单，个人级扩展属于 `PrivateCallURI` 条目。不同方向的 ID、URI 和名单不互填；[任意私呼对端权限](mcptt-user-profile-private-call-any-peer.md)另查。

## 空值回退与个人项的出现条件

**名单级空值。** 去、来话各自的名单语义段都说：如果所指名单级的 `uri-entry` 为空，使用 MCS 初始配置档中的 KMS。回退不是在用户档写入默认 XML，也不是发送失败后重试的地址。缺节点、缺名单、片段没看到、仅见空白字符、URI 不合法或联系失败，不能当作已经证实这个元素为空。个人项的空值不继承这份回退。若未核初始档具体 KMS，不能补出地址。

**个人项。** 两方向分别写 `only present if`：关联 MCPTT ID 的 KMS URI 必须不同于**自己方向的名单级 `uri-entry`**，个人项才可出现。出现 ⇒ 不同；知道不同 ⇏ 必填。比较对象是原文指明的名单级 URI，不把它改成另一个方向的名单、初始档 KMS 或从配置推定的实际连接地址。如果名单级值缺失、为空或不清楚，本段没有另定比较方法、URI 相等算法或回退与比较的执行顺序。

## 提纲、Schema 和语义原写不拼成新路径

§8.3.2.1 两个 `PrivateCallURI` 描述都先说包含一个 `uri-entry`，紧接 `which contains:` 再列可放 KMS 的 `anyExt`。§8.3.2.3 的 `EntryType` 则把必需的 `uri-entry`（`xs:anyURI`）和可选的 `anyExt` 列为兄弟。名单和个人扩展中都可看到双层同名：全局 `PrivateCallKMSURI` 是 `PrivateCallKMSURIEntryType`，其内部的必需 `PrivateCallKMSURI` 是 `EntryType`；该内层有必需的 `uri-entry`。字段声明和局部形状不保证整档接受；本段不声明 URI 值节点可嵌一个元素，也不借初始档的 URI 校验给用户档另加 409。

§8.3.2.7 还保留三处不同的原写：

- 去话个人 `only present if` 的主语写 `Common/PrivateCallList/PrivateCallURI/anyExt/PrivateCallKMSURI`，漏掉 `PrivateCall`，且只写一个同名 KMS 层。该句的名单比较端和去话名单 URI 释义都保留 `Common/PrivateCall/PrivateCallList`，连到双层 KMS 的 `uri-entry`。
- 来话个人主语写 `OnNetwork/anyExt/IncomingPrivateCallList/PrivateCallURI/anyExt/PrivateCallKMSURI/PrivateCallKMSURI`，指同名内层。该句名单比较端的 `OnNetwork` 与 `IncomingPrivateCallList` 之间漏了外层 `anyExt`，名单内的 `anyExt` 还在。
- 来话名单 URI 释义同样漏掉 `OnNetwork` 后的外层 `anyExt`，并以双层 KMS 的**内层 `PrivateCallKMSURI`**作主语；其后另用 `uri-entry` 说空值回退。不能用提纲改写该句主语，也不能把几个原写当作可替换或已获准的 XML 路径。

[用户档的 XCAP 检查](mcptt-user-profile-xcap-validation.md)和[初始配置的 TLS 字段](initial-ue-tls-tunnel-validation.md)另有适用条件。[用户档私呼转接](mcptt-user-profile-private-call-transfer.md)、[用户档私呼转发](mcptt-user-profile-private-call-forwarding.md)与[带话权私呼的 Stage 1 条件](../calls/floor-controlled-private-call-basics.md)不决定这里的 KMS URI。本版的组 KMS 条目也不替换私呼规则。不从 URI 或回退推断 KMS 鉴权、加密流程、密钥交付或来话结果。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-user-profile-private-call-kms-uri.json)
