# MCData 在网通知服务器主机名：列表与原文命名

查 MCData 在网业务配置的通知服务器主机名，先从 `on-network/anyExt/notificationserver-hostname-list` 找 `ns-entry`。TS 24.484 V20.1.0（Release 20，Stage 3）§10.4.2.7 在网项 19 解释这个条目的含义时，父项字面写成了 `notificationservers`。核对 XML 结构时看 §10.4.2.1 和 §10.4.2.3，不把语义段的名字当成第二个已声明的 XML 路径。

### 正文说一条或多条，Schema 的次数下限是零

| 查哪一处 | 原文给出的信息 |
| --- | --- |
| §10.4.2.1 在网项 4(f) | 在可选 `anyExt` 内列 `notificationserver-hostname-list`，正文写列表包含一个或多个 `ns-entry`。 |
| §10.4.2.3 的在网类型和全局声明 | `on-networkType` 声明可选 `anyExt`；其类型有 `##any`、`lax` 的元素通配。列表另有全局元素声明，不是 `on-network` 的具名直接子项。 |
| §10.4.2.3 的列表类型 | `notificationserver-hostname-listType` 的 `xs:choice` 与其中 `ns-entry` 都从 0 到 `unbounded`；条目类型是 `xs:anyURI`。名单内另有 `anyExt` 和 `##other`、`lax` 通配，不要与外层 `anyExt` 混用。 |

只看这两处出现次数声明，零条不因次数被排除；这不消去正文的一个或多个，也不证明完整配置会被接受。外层 `anyExt` 可选，不等于它出现时正文所列的每项都明确可选。[同级 ad hoc 组数据块](mcdata-on-network-adhoc-group-data-config.md)的可选写法和缺项语义另查，不借给通知服务器列表。

### 条目语义是主机名，不是组织域

§10.4.2.7 在网项 19 的原写是 `notificationservers` 下的 `ns-entry` 包含通知服务器的主机名，对应 TS 24.483 [4] §11.2.16 中 `NotificationServer` **元素的叶节点**。这里仅保留指向。原文这两种父项拼法不能证明互为别名，也没有依据判定该怎样改名。Schema 的 `xs:anyURI` 是类型声明，不能拿任意 URI 替代条目的主机名语义，也不证明实际解析、选择、注册、连接或通知交付。

§10.4.2.6 要求业务配置文档符合 Schema，没有为这个列表或主机名另列一条专用 409。该节对组织 `domain` 值的语法和未知域检查针对的是业务配置参数块，不拿来检查通知服务器主机名。[未知或实收重复项](mcvideo-mcdata-service-config-validation.md)按其各自条件查。仅因语义段拼法不同，不能替服务端判一个具体元素是未知；多条都名为 `ns-entry` 也不能仅凭同名判成收到重复项。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcdata-on-network-notification-server-config.json)
