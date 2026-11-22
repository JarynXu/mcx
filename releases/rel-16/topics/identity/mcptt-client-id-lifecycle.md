# MCPTT 客户端 ID：SIP 掉注册、重启和恢复出厂后，哪些状态能沿用？

**掉 SIP 注册、关机或电源重启，都不是重新分配 MCPTT 客户端 ID 的理由。** 固定 Rel-16 版本规定，MCPTT 客户端在第一次使用时自行分配客户端 ID；§4.10 列明，在已注册、未注册但终端仍开机、终端关闭和电源重启这几种状态下都保留它。恢复出厂设置是明示的例外：终端不保留这个 ID。这条不规定应用重装、清除应用数据或更换账号的行为，也不能单凭 ID 改变反推出一定恢复过出厂设置。[TS 24.379 V16.14.0，§4.10（含注），印 49](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=50)。

<a id="client-id-on-wire"></a>
## 两个客户端能共用用户的 SIP URI 当作 client ID 吗？

不能。用户可以在甲、乙两台终端登录同一个 MCPTT 账号，但 **MCPTT client ID 标识一个具体的客户端实例**。每个客户端首次使用时自行分配全局唯一的 **UUID URN**，生成方法指向 RFC 4122 §4.2。甲乙共用用户的 SIP URI 或手机号，既没有取得规定的标识形式，也没有区分两个实例。换成两端共用的一枚 UUID，也只解决了外形问题。不要在每次发 REGISTER 时重新生成；保留与恢复出厂的边界见上文。[TS 24.379 V16.14.0 §3.1，印 29](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=30)；[§4.10，印 49](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=50)。

**查办理 MCPTT 业务授权的 REGISTER，分两步验：先看有没有按程序带客户端 ID，再看它怎么装进 XML。** 这里的前提是用户认证成功、有可用访问令牌，而且客户端选用 REGISTER 办理授权。此时 `application/vnd.3gpp.mcptt-info+xml` 业务正文要带访问令牌和发起客户端的 ID；只做 SIP 注册的 §7.2.1AA 不是这个入口。附录 F.1.2 的通用结构把 `mcptt-client-id` 列为可选，F.1.3 第 17 项也只是列举可携带它的请求，不能拿来免除 §7.2.1 在本次请求中的要求。[§7.2.1，印 148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=149)、[受保护分支与 §7.2.1AA，印 149](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=150)；[附录 F.1.2，印 545](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=546)；[F.1.3 第 17 项，印 549](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=550)。

| 客户端的机密性配置 | 在 `mcptt-Params/mcptt-client-id` 中核对什么 |
| --- | --- |
| 未启用机密性，包括只启用完整性 | 属性 `type="Normal"`，子元素 **`mcpttString`** 中是发起实例的 UUID URN。虽然 URN 是一种 URI，客户端 ID 在这里不用 `mcpttURI`。启用完整性时另保护业务正文，不能把签名当作 ID 已加密。 |
| 已启用机密性 | 属性 `type="Encrypted"`，子元素是 XML Encryption 命名空间中的 `EncryptedData`，内有 `CipherData/CipherValue`。这次授权请求也要加密令牌。没有可读的 UUID 不说明缺 ID；要核对具体实例，须在相应保护处理成功后看解出的客户端 ID，不能拿密文与用户 SIP URI 比对。 |

[§7.2.1，印 148–149](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=150)；[§7.3.1A，接收端对令牌和客户端 ID 的处理，印 154](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=155)；[F.1.3 第 1–3 项，印 547](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=548)及[加密子元素，印 548](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=549)。表中 XML 路径相对业务正文的 `mcpttinfo` 根元素。业务元素属于 `urn:3gpp:ns:mcpttInfo:1.0`；`EncryptedData` 属于 `http://www.w3.org/2001/04/xmlenc#`，不靠前缀拼写识别。

**XML 校验通过不等于这个 ID 合规。** F.1.2 的共用类型同时容纳 `mcpttURI` 与 `mcpttString` 等子元素；后者的类型只是字符串。把电话号码填进 `mcpttString`，或把客户端的 UUID URN 填进 `mcpttURI`，不能仅凭 XSD 放行：前者用错了值，后者用错了明文子元素。服务设置表 7.4.1.2.2-3 在另一种正文的 `entity/@id` 里写了 `urn:uuuid:` 开头的示意值，它不是生成客户端 UUID URN 的测试样例。这些条款也没有给上述错误规定统一的 SIP 响应码，或规定客户端 ID 必须等于 SIP 的 `+sip.instance`。[F.1.2 共用类型，印 546](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=547)；[F.1.3 明文规则，印 547](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=548)；[设置示例，印 160](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=161)及[印 161](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=162)。

## 记录里有几个身份，用哪个来核对客户端是否变了？

查 MCPTT 协议所用的**客户端 ID**，不是用 SIP 注册结果猜。在 §7.3.2 的第三方 REGISTER 授权入口，服务端从外层请求识别 IMS 公共用户身份，授权用的客户端 ID 则在内嵌的客户端 REGISTER 的 `mcptt-info` 正文中。服务端比较授权来件中的客户端 ID 与现有绑定，用于识别同一个 MCPTT 用户是否已在另一客户端获准。两项身份可以同时出现在一笔事务里，不能用其中一个代填另一个。若内嵌 REGISTER 带 `Resource-Share: supported`，外层 `Contact` 的 `+g.3gpp.registration-token` 用来识别注册的 MCPTT UE，仍不是正文的客户端 ID。仅有公共用户身份、注册令牌或一次成功注册，不能确认此次请求写的是原客户端 ID。此处也不规定它与 SIP `+sip.instance` 之间的等值或转换规则。[§7.3.2（入参、步骤 1、4a、5），印 155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=156)；[§8.1A，印 161](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=162)。

## 恢复出厂后还是同一个用户，能用旧客户端的归属记录吗？

**不能只认用户名和组。** 例如，设备恢复出厂前的客户端 ID 为 A，现在的请求使用 B；组记录中这个用户只列 A，且用户条目尚未到期。若这次操作调用 §6.3.6 的归属检查，服务端依次按目标组、MCPTT 用户和**本次客户端 ID**找记录；找不到 B 就判本次客户端未归属该组。即使找到了 B，还要检查该用户条目是否到期。发起方的客户端 ID 可从这次客户端发出的 INVITE、REFER 或 MESSAGE 的 `mcptt-client-id` 找到；不要拿同一用户另一台设备的记录补本次客户端。[§6.3.6，印 135](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=136)及[印 136](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=137)。

反过来，普通重启后 ID 仍是 A，也不意味着原归属状态仍有效。**本机是否保留 ID、服务器是否把本次请求判为已归属、服务器是否删了 A 的旧记录**，是三个核对项。§4.10 的恢复出厂例外只说明本机不保留 ID；要结案说 A 的服务器记录已清理，须看服务器状态或清理记录，不能用本机重置或 B 的一次请求代替。[§4.10，印 49](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=50)；[§6.3.6，印 135–136](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=136)。

普通聊天组呼还有隐式归属条件，查[聊天组的加入准入](../calls/chat-establish-join.md)。如果工单是查[另一客户端的业务授权绑定](shared-sip-registration.md)或[用户多端归属上限 N2](../groups/implicit-affiliation-n2.md)，分别走其实际程序。要判断两项业务使用同一个 ID 值时各代表谁，查[跨业务用户身份映射](cross-service-user-mapping.md)。
