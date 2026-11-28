# MCPTT 用户配置档：私呼转发的许可、启用与目标

能不能请求转发，查 `allow-call-forwarding`；即时或未应答转发是否启用，查 `call-forwarding-on`。两项都面向为该用户执行终止参与式 MCPTT 功能的服务器，分别说明许可和启用状态。按用户手动输入请求转发，则查始发参与式功能使用的 `allow-call-forward-manual-input`。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.3.2.1/.3/.7，表 8.3.2.7-52 至 55。这里查 MCPTT 用户配置档；不同于[在网业务配置的即时转发次数上限](mcptt-on-network-service-authorization-forwarding-caps.md)。

## 先分规则动作和在网设置

§8.3.2.1 项 11(b)(xxxviii)(O/P)在 `ruleset/rule/actions/anyExt` 列请求许可 `allow-call-forwarding` 和手动输入许可 `allow-call-forward-manual-input`。在网设置则列在项 10(g) 的 `OnNetwork/anyExt`：`call-forwarding-on`、`forward-to-functional-alias`、`call-forwarding-condition`、`call-forwarding-no-answer-timeout`、`call-forwarding-target`。保留用户档的大小写；业务配置的 `on-network` 不替换它。

§8.3.2.3 对七个名字各给全局声明，未给 `default` 或 `fixed`：四个开关或许可是 `xs:boolean`；条件为 `xs:string`，时长为 `xs:duration`，目标为 `xs:anyURI`。这不等于给每个名称另定必填、次数或缺项回填。§8.3.2.6 的通用 Schema 要求仍适用；本节未为这七项另写专用 409。其他 [用户配置档的 XCAP 约束](mcptt-user-profile-xcap-validation.md)按各自条件查。

## 许可、启用、目标类型的三个 false

| 表与字段 | `true` | `false` | 确认该字段未出现 |
| --- | --- | --- | --- |
| 表 52：`allow-call-forwarding` | 为该用户执行**终止参与式 MCPTT 功能**的服务器，按配置认为该用户有权请求即时和未应答两类私呼转发。 | 指示该服务器拒绝这两类转发。 | 本字段取 `false`。 |
| 表 53：`call-forwarding-on` | 对同一类终止参与式功能，表示该用户的即时或未应答私呼转发启用。 | 表示即时或未应答私呼转发禁用。 | 本字段取 `false`。 |
| 表 54：`forward-to-functional-alias` | 转发目标类型为功能别名。 | 转发目标类型为 MCPTT ID。 | 本字段取 `false`，目标类型为 MCPTT ID。 |

这三个默认各归自己的字段。目标类型取 MCPTT ID 不表示已经填入目标、转发已开或请求已准。只查看到部分配置，不能把没看到当作已知缺项；字段出现却给了无效值也不是缺项。条款未规定这些字段互相覆盖的次序，不以许可或启用判断本次实际处理。

## 查条件、时长和目标时读不同字段

`call-forwarding-condition` 在 §8.3.2.7 分别写 `immediate`（即时）和 `no-answer`（未应答）。两种文字属于语义段，不是 XSD 枚举，也不能从 `xs:string` 推任何字符串都会被接受。`call-forwarding-no-answer-timeout` 是未应答计时的时长，不是即时转发次数，也不规定缺项值、实际起止、到期结果或多条件先后。配置条件不能替[私呼来电转发](../calls/incoming-private-call-forwarding.md)或[在网 ad hoc 组呼转发](../calls/ad-hoc-group-call-forwarding.md)各自的 Stage 1 触发条件。

`call-forwarding-target` 是目标值，写转发目标的 MCPTT ID 或功能别名；表 54 区分目标种类。两项不是正在进行的私呼转接所用的目标名单，也不说明[功能别名](mcptt-functional-alias-service-config.md)怎样解析、匹配到谁，或目标是否可达。

## 手动输入是另一项请求许可

表 55 的 `allow-call-forward-manual-input` 指向为该用户执行**始发参与式 MCPTT 功能**的服务器。`true` 表示该用户可请求按手动输入把私呼转发给任一 MCPTT 用户；`false` 则指示拒绝此类请求。**表 55 未给缺项默认**，不能从表 52～54 补 `false`，也不把手动输入理解为未应答、手动开始来电、拒接或已转发成功。

TS 24.484 在本段说明：除手动输入许可之外的六项不在它所指 TS 24.483 [4] 用户配置管理对象内；手动输入许可对应 §5.2.48T3 的 `AllowedCallForwardManualInput`。TS 24.379 [9] 是表中程序指向。两份引用保留为定位，不据此补协议、验证顺序或现场结果。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-user-profile-private-call-forwarding.json)
