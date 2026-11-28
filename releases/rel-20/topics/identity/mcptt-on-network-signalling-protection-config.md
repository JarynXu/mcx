# MCPTT 在网信令保护：两段链路的开关与默认值

**先分客户端到服务器、服务器到服务器，再看要保护的信令。**TS 24.484 V20.1.0（Release 20，Stage 3）在网业务配置 §8.4.2.7 分四项说明。字段表示配置上的启用或禁用；它不证明某条信令已经获得保护。

| 哪一段 | 配置块 | 看哪个字段 |
| --- | --- | --- |
| MCPTT 客户端与 MCPTT 服务器之间 | `signalling-protection` | 项 33 的 `confidentiality-protection` 看 MCPTT 信令的保密性；项 34 的 `integrity-protection` 看 MCPTT 信令的完整性。 |
| MCPTT 服务器之间 | `protection-between-mcptt-servers` | 项 38 的 `allow-signalling-protection` 看 MCPTT 信令保护；项 39 的 `allow-floor-control-protection` 专看 MCPTT 话权控制信令保护。 |

服务间两项分别核。项 38 没有定义它与项 39 的覆盖、优先或联动关系，不能拿一项的值替另一项。客户端一侧的保密性和完整性也不互相代替。

### 默认是字段的值，不是父块必须出现

- **四个字段的默认均为 `true`。**§8.4.2.7 注 4 点名这四项。§8.4.2.6 只另述客户端侧两项的默认 `true` 表示对应保护启用，不是在此为服务器之间两项另定默认或特定错误响应。表 A.2.3-12 的在网响应显式写出四个 `true`，没有展示缺项时默认怎样被采用。
- **Schema 分开写是否出现和值是什么。**§8.4.2.1 在网项 8、12 各列可选父块和对应子项；§8.4.2.3 的两个父块、四个布尔子项各有 `minOccurs="0"`。在这六个声明里，只有四个子项有 `default="true"`，不是 `fixed`，不把写明的 `false` 改成 `true`。
- **缺块、缺子项与子项本来就存在但没有内容，是三种不同输入。**XSD 校验可为有效出现但没有元素或字符内容的布尔子项提供默认值；元素不存在时不会因此新建。父块虽在却没给子项，也不会靠子项默认自动长出它。只看不完整片段不能确认缺失。这一层判断不说明 CMS 是否回填业务文档，或服务器怎样处理未提供字段的实际会话。[W3C XML Schema §3.3.5](https://www.w3.org/TR/2004/REC-xmlschema-1-20041028/#sic-eltDefault)仅解释这里的 XSD 元素默认语义。

这里不选择 TLS、CSK、加密或完整性机制，也不判它们是否已用于某条消息。若问初始配置启用 [TLS 隧道时的双向认证校验](initial-ue-tls-tunnel-validation.md)，或业务配置的[参数块与重复项校验](mcptt-service-config-structure-and-extensions-validation.md)，走各自入口。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-on-network-signalling-protection-config.json)
