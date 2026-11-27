# MCPTT 业务配置的 XML 校验：缺参数块、组合不符，还是重复项？

**先看完整 MCPTT 业务配置是否有参数块，再数三类业务范围。**根元素是 `<service-configuration-info>`；根的直接子元素 `<service-configuration-params>` 里才查 `<common>`、`<on-network>` 和 `<off-network>`。如果只拿到 XCAP 节点片段或客户端记录，不要把没看到的内容当成整档缺项。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.6，Schema 与分支子项见 §8.4.2.3/.1。

| 查到的问题 | §8.4.2.6 建议的 `phrase`（若带此属性） |
| --- | --- |
| 根下没有 `<service-configuration-params>` | `mandatory element is missing` |
| 有参数块，但三类范围元素一个都没有 | `mandatory element is missing` |
| 三类范围元素的组合不在下列七种里 | `semantic error` |

每条都规定配置管理服务器（CMS）返回 **HTTP 409（Conflict）**，包含 XCAP 错误元素 `<constraint-failure>`。`phrase` 可不带。空参数块也不在七种组合内；原文没说此时哪项先判或必选哪个短语。

## 七种组合只管范围元素的数量

三类范围可以单独放一种（3 种）、任意两种各放一个（3 种），或三种各放一个（1 种）。`on-network` 与 `off-network` 各一个时，不必另加 `common`；只放一个 `off-network` 也符合这个组合判据。同类范围元素出现两个就不符合七种组合。

§8.4.2.3 的 XML Schema 把根下参数块声明为 `minOccurs="0"`，把三类范围元素声明为 `minOccurs="0" maxOccurs="unbounded"`，并列在 `xs:sequence` 中。§8.4.2.6 另要求文档符合该 Schema，也要求通过自己的缺项和组合校验。不能拿 Schema 的数量声明豁免这两种校验，也不能用组合列表推定元素可任意排序。

**选中了在网分支，还要核在网分支里面。**例如，只有一个在网块符合七种组合的计数，但在网块仍须包含 `<fc-timers-counters>` 和三种 `<emergency-resource-priority>`、`<imminent-peril-resource-priority>`、`<normal-resource-priority>` 资源优先级（§8.4.2.1 在网项 7、9–11，§8.4.2.3 `on-networkType`）。缺这四项要查分支本身，不能直接套上表专指参数块和范围的两个缺项分支。只选离网块时也不继承这四项。在网块和离网块的 `<private-call>` 都可选；见[私呼的时长字段](mcptt-private-call-service-timers.md)，不能把没有私呼块当成缺了一个范围元素，或判定私呼不受支持。

## 未知项与 CMS 收到的重复项分开判

- **未知元素或属性：**原文写业务配置服务器（service configuration server）忽略它。忽略不是删除或写回，也不表示完整文档通过 Schema，或者请求已获准。
- **CMS 收到重复元素或属性：**配置管理服务器（configuration management server）须返回 HTTP 409（Conflict）并含 XCAP `<constraint-failure>`；若带 `phrase`，建议 `duplicate attribute or element received`。只看客户端内容不足以确认 CMS 收到。同名也不足以判重复，例如 §8.4.2.3 允许功能别名列表含多个 `<functional-alias-entry>`。条文没有规定判重方法或处理顺序。

§8.4.2.6 注 1 的字面是 `<mcptt-info>` 下的 `##any` 元素粒子。§8.4.2.3 的根类型和参数类型分别声明 `##other` 元素通配及 `##any` 属性通配，均为 `lax`。按各处的原文读，不把注 1 当成 Schema 根的声明，也不从命名空间或通配写法直接判某项“未知”。以上两个服务器名称按条文区分职责，不据此判定有几个部署实例。

收到 409 而未能定位正文时，另查 [MCPTT 请求标识和组织域](mcptt-service-target-domain-validation.md)或[离网私呼的优先级数值](mcptt-service-off-network-priority-values.md)。[MCVideo、MCData](mcvideo-mcdata-service-config-validation.md)要看各自的 §9.4.2.6、§10.4.2.6；七种范围组合相同，不因此搬用另一业务的分支字段，例如 MCData 的文件可用时间要求。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-service-config-structure-and-extensions-validation.json)
