# MCPTT 离网私呼配置：PQI 和 ProSe 逐包优先级怎么校验？

**先查外层字段，再判数字。**MCPTT 业务配置的 `<off-network>` 下有两类可选配置：`<default-pqi>` 和 `<default-prose-per-packet-priority>`。两类都有同名的私呼信令和媒体字段，适用的数值校验却不同。这里的离网是业务配置分支，不是终端用外设做[离线配置](offline-ue-configuration.md)。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.6/.7。

| 外层字段 | §8.4.2.6 的判据 |
| --- | --- |
| `<default-pqi>` | 任一子元素的值不在 **21–26、55–61、90–93** 三个含端点区间中的任何一个，配置管理服务器（CMS）须返回 **HTTP 409（Conflict）**，含 XCAP 错误元素 `<constraint-failure>`。响应若带 `phrase`，建议用 `element value out of range`。 |
| `<default-prose-per-packet-priority>` | 原文条件是同一子元素的值“小于 1 **且**大于 8”（`less than 1 and greater than 8`）。原句为该条件规定同样的 409 和错误元素；若带 `phrase`，建议用同一短语。一个数不能同时满足两个比较，不能把原文改成“小于 1 **或**大于 8”。 |

例如，PQI 填 **27** 命中该项；填 **26** 只说明不命中这项 409，不代表其余检查都通过。ProSe 逐包优先级填 **0** 或 **9**，或两项分别填这两个值，都不能凭所引文字断言该项 409。也不能反过来断言 CMS 一定接受这些值。具体请求的校验结果不在这两句里。

## 两类配置的同名子元素

`mcptt-private-call-signalling`、`mcptt-private-call-media`、`mcptt-emergency-private-call-signalling`、`mcptt-emergency-private-call-media` 分别对应普通私呼和紧急私呼的信令和媒体（§8.4.2.7 离网项 9、11）。§8.4.2.3 在两类父块里都把这四个具名子元素各自声明为可选的 `xs:unsignedShort`，未为这些声明指定缺项默认值。**基本类型不是数值校验。**例如，PQI 的 27 可以表示成该类型的值，仍不在上表的区间里。同名不能推出两块应填相同数值。

§8.4.2.3 的 Schema 摘录把 PQI 父项写成 `name="default-pqi "`，引号内多一个末尾空格。§8.4.2.1/.6/.7 的元素名不带这个空格。两处按原文定位，不把空格解释成另一个报文元素，也不据此判断某个校验器会接受哪种 Schema 摘录。

§8.4.2.6 注 2 只说明 ProSe 逐包优先级的值越大，给予信令或媒体的优先级越高。附录 C §C.4.2 将 `<default-pqi>`（PC5-5QI）列为 5GS 下离网逐包优先级配置的对应项。这是两类配置的用途关系，没有给出逐值替换表。不要把注 2 的数值排序套给 PQI，也不要把两项写成[离网话权抢占的优先级](../calls/off-network-floor-override.md)。

若 409 指向的是 [MCPTT 业务配置的 AUID 或组织域名](mcptt-service-target-domain-validation.md)，另查同节的 URI 或正文属性条件。两路共用 HTTP 409，不表示诊断原因相同。§8.4.2.7 指向 TS 24.483 §7.2.22–.25；这里未核对被引条款的内容或实际信令和媒体的处理。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-service-off-network-priority-values.json)
