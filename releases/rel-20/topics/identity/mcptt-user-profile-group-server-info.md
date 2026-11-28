# MCPTT 用户配置档：按组查 GMS、IDMS 与 KMS 地址

先用 `MCPTTGroupInfo/entry/uri-entry` 定位哪一个组，再到同一条目的 `anyExt/GroupServerInfo` 查服务器联系地址。外层 `uri-entry` 标识组，不是给 GMS、IDMS 或 KMS 的地址。在网、离网都有对应三段；两种模式不能互填。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.3.2.1/.3/.7。这里查 MCPTT 用户配置档，不从条目有值推实际入组、地址已选中或服务器已响应。

## 同一组要查哪一个端点？

下表均指 `OnNetwork` 或 `OffNetwork` 内同组 `MCPTTGroupInfo/entry/anyExt/GroupServerInfo` 下的字段。表中的 TS 24.483 [4] 条号和名称只作引用定位。

| 字段 | 在网原文 | 离网原文 |
| --- | --- | --- |
| `GMS-Serv-Id` | 联系此组的组管理服务器。§5.2.48B8 `GMSServID`。 | 联系此组的组管理服务器。§5.2.53C `GMSServID`。 |
| `IDMS-token-endpoint` | 联系此组的身份管理服务器**令牌端点**。§5.2.48B9 `IDMSTokenEndPoint`。 | 原文只说联系此组的**身份管理服务器**，尽管字段名与指向名仍带 token。保留 §5.2.53D8A9 `IDMSTokenEndPoint` 的原写。 |
| `GroupKMSURI` | 联系此组的密钥管理服务器。§5.2.48B10 `GroupKMSURI`。 | 联系此组的密钥管理服务器。§5.2.53E `GroupKMSURI`。 |

离网描述没有明写 token endpoint，不等于另定协议或排除令牌端点。两个模式的同名字段也不保证填同一个地址。组的 KMS 配置与[私呼名单或个人的 KMS URI](mcptt-user-profile-private-call-kms-uri.md)分开。

## 查空值前，先确认原文说的是哪个字段

- **GMS**：在网、离网两句话都只说明组管理服务器联系 URI，没有为此处 GMS 明写空值时用初始配置。不借初始档的 `gms`，也不据此断言规范其他处或运行中不存在任何回退。
- **IDMS**：在网、离网各自写，若原文所说的 entry 为空，使用 MCS 初始配置档中的 `idms-auth-endpoint` **和** `idms-token-endpoint`。不能只取其中一个，或把二者当作组档中的两个同名字段。
- **KMS**：在网、离网各自写，若原文所说的 entry 为空，使用 MCS 初始配置档中的 `kms`。不要借两项 IDMS 值或私呼个人项的比较规则。

这四处各写 `If the entry element is empty`。该条件句没有指定完整路径。不把 **entry** 改成组标识 `uri-entry`、某个端点的 `uri-entry` 或确指某一层的 `<entry>`，也不从[私呼](mcptt-user-profile-private-call-kms-uri.md)明确写 `uri-entry` 为空的句子反推。节点不见、片段空白、地址无效或联系失败，不证明这里所说的 entry 为空。回退到初始配置档的字段名不等于已知道具体地址、已经认证、发了令牌请求或领到密钥。

## 提纲和 Schema 的条目次数分开查

§8.3.2.1 分别写可有零或一个 `OffNetwork`（项 9）和 `OnNetwork`（项 10）。在相应模式块内，提纲各写一个 `MCPTTGroupInfo`；离网含一个或多个 `entry`，在网含零个或多个。§8.3.2.3 在两种模式各自的 `0..unbounded` choice 中列 `MCPTTGroupInfo`，其类型为 `ListEntryType`；**名单内部**另有独立的 `0..unbounded` choice。不以其中一个层级替另一个，不从局部次数判整个配置是否可用或允许空名单。通用条目提纲另写 `index` 必需；共用 `IndexType` 的 Schema 声明为 `xs:token`，未写 `use="required"`。两种表面保留，不互相改写。

通用条目提纲的 `anyExt` 可含 `GroupServerInfo`。Schema 把这个扩展全局声明为 `GroupServerInfoType`；它不是每条都要有，也不是 `EntryType` 的具名直子项。已出现且采用这个类型的元素，局部 `xs:sequence` 顺序为必需的 `GMS-Serv-Id`、`IDMS-token-endpoint`、`GroupKMSURI`。各自为 `EntryType`，各有必需的 `uri-entry`（`xs:anyURI`）。外层条目可选 `anyExt` 的 `##any/lax`，与类型内另有的可选扩展及 `##other/lax` 不是同一处声明。它们不把字段存在、字符串有效性或整份文档接受性合在一起。

§8.3.2.6 仍有通用 Schema 要求，没有以上字段的具名 409。[用户档 XCAP 检查](mcptt-user-profile-xcap-validation.md)和[初始档 TLS 检查](initial-ue-tls-tunnel-validation.md)各读其条件，不借初始档 URI 检查给组档新增诊断。[私呼对端](mcptt-user-profile-private-call-any-peer.md)、[用户档私呼转发](mcptt-user-profile-private-call-forwarding.md)、[用户档私呼转接](mcptt-user-profile-private-call-transfer.md)也不是这个按组地址的用途。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-user-profile-group-server-info.json)
