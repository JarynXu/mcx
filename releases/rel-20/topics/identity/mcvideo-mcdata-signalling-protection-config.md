# MCVideo 与 MCData 在网信令保护：客户端、服务器间与默认值

客户端与服务器之间，两项业务都把信令的保密性和完整性分开配置。服务器之间，MCVideo 另有传输控制信令保护开关；MCData 本版只定义通用的服务器间信令保护开关。这里查 TS 24.484 V20.1.0（Release 20，Stage 3）的在网业务配置，不用一个开关的值推另一个，也不由配置断言实际保护。

| 查哪一段 | 对应配置 | 原文 |
| --- | --- | --- |
| MCVideo 客户端与 MCVideo 服务器之间 | `on-network/signalling-protection` 的 `confidentiality-protection` 表示信令保密性是否启用；`integrity-protection` 表示信令完整性是否启用。 | §9.4.2.7 在网项 1/2。 |
| MCData 客户端与 MCData 服务器之间 | 本业务档同一路径、两个同名布尔项，看的是 MCData 信令。 | §10.4.2.7 在网项 7/8。 |
| MCVideo 服务器之间 | `on-network/protection-between-mcvideo-servers` 的 `allow-signalling-protection` 看 MCVideo 信令保护；`allow-transmission-control-protection` 单独看 MCVideo **传输控制信令**保护。 | §9.4.2.7 在网项 3/4。 |
| MCData 服务器之间 | `on-network/protection-between-mcdata-servers` 只声明一个具名布尔项 `allow-signalling-protection`，看 MCData 服务器间信令保护。 | §10.4.2.1 在网项 3、§10.4.2.3、§10.4.2.7 在网项 12。 |

### MCData 的注 1 多写了一个名字

§10.4.2.7 注 1 把 `allow-floor-control-protection` 与前三个字段一并列为默认 `true`。这个名字没有相应的 MCData 在网配置定义：§10.4.2.1 在网结构未列，§10.4.2.3 本业务 Schema 未声明，§10.4.2.6 未给它默认说明，§10.4.2.7 在网项也没有给它位置或业务语义。不能据注 1 加设这个开关。这里不把它改成 MCVideo 的传输控制开关；[MCPTT 的话权控制信令保护](mcptt-on-network-signalling-protection-config.md)有自己的字段定义，不能移用到 MCData。

MCData 的 `server-protectionType` 仍有可选 `anyExt` 和 `##other`／`lax` 通配。它们不是这个名字的本业务声明；也不能单凭注 1 判断某个扩展能否被接收，或 CMS 会如何处理实际文档。

### 默认值与字段是否出现分开查

§9.4.2.6 明列 MCVideo 上表四个字段的默认 `true` 和各自启用的保护，§10.4.2.6 明列 MCData 的三个。§9.4.2.7 注 1 点名的四个都有对应定义；§10.4.2.7 注 1 多出的名称不能算作第四个 Schema 默认项。

结构正文在 `on-network` 中列可选的两类父块和各自子项（§9.4.2.1 项 1/2、§10.4.2.1 项 2/3）。对应 XSD（两业务的 §.3）中，两类父块都是 `on-network` 的直接可选子元素，没有默认值。已声明的布尔子项各写 `minOccurs="0"`、`default="true"`，不是固定为 `true`。读到显式 `false` 就是对应配置为关闭，不用默认覆盖。布尔元素已出现、没有字符或子元素且符合声明时，XSD 校验可为它提供默认值；布尔元素缺失、包括父块整个省略时，不会靠 XSD 的子项默认补出元素。若手上只有片段，先确认能否判断缺项。这里不规定 CMS 回填、缺值时服务端应用何种策略，或某次信令是否用了保护。

[业务配置的 XML 校验](mcvideo-mcdata-service-config-validation.md)和[初始终端配置启用 TLS 隧道时的校验](initial-ue-tls-tunnel-validation.md)另查。本主题不选择加密、完整性或认证机制，不把信令保护开关当成媒体保护。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcvideo-mcdata-signalling-protection-config.json)
