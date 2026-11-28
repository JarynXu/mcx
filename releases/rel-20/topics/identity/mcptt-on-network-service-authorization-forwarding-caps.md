# MCPTT 在网业务配置：同时授权数与即时转发次数

一个 MCPTT 用户能同时拥有多少项业务授权，查 `max-simultaneous-authorizations`。允许多少次**即时呼叫转发**，查 `max-immediate-forwardings`。两项都在业务配置的在网块外层 `anyExt`，不是某条功能别名的设置。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.7；§8.3.2 的用户配置档仅用于区分同版的另一处字段。不移用离网或其他业务的规则。

## 放在业务配置的外层 anyExt

§8.4.2.1 在网项 13(b/c)把它们列在可选的 `on-network/anyExt` 内，与 `functional-alias-list` 并列。§8.4.2.3 在 `on-networkType` 中直接声明的可选项是 `anyExt`；它的 `anyExtType` 有 `##any`、`lax` 元素通配，与 `on-networkType` 自己序列的 `##other`、`lax` 通配不同。两个上限都声明为全局 `xs:positiveInteger` 元素，不是 `on-networkType` 或功能别名条目的具名直接子项。通配的次数不等于给两个名字各指定了必填或次数，也不证明 CMS 会接受某种放法或重复项。

两项均无 XSD `default` 或 `fixed`。显式 0 不符合这个正整数类型，也不是缺项或关闭开关。注 3 说的是项 44 的别名优先级；夹在两项之间的注 4 只给四个信令保护字段默认 `true`，没有给这两个计数补默认。§8.4.2.6 的通用 Schema 规则仍适用，本节未为这两个名字另列专用 409 条件或短语；见[整份 MCPTT 配置结构和重复项](mcptt-service-config-structure-and-extensions-validation.md)。

## 两项各数什么

| 业务配置字段 | §8.4.2.7 用途 | 别拿来数 |
| --- | --- | --- |
| `max-simultaneous-authorizations` | 项 45：一个 MCPTT 用户允许同时拥有的业务授权数上限 | 某一功能别名的并发激活、同时通话、终端注册或已授权的实况 |
| `max-immediate-forwardings` | 项 46：允许的即时呼叫转发次数上限 | 等待多久才转发、未应答触发、所有转发或已成功的次数 |

[逐别名的并发激活数](mcptt-functional-alias-service-config.md)是项 41 的 `max-simultaneous-activations`。[在网 ad hoc 多发话者配置](mcptt-on-network-adhoc-multi-talker-config.md)也是另一组字段。项 46 不说明按用户还是按呼叫等范围计数、时间窗口、何时重置或达到上限后的动作。查[私呼来电转发](../calls/incoming-private-call-forwarding.md)或[在网 ad hoc 组呼转发](../calls/ad-hoc-group-call-forwarding.md)的 Stage 1 条件与结果，不能用这个次数替代。

## 和用户配置档的相近字段分开

§8.3.2.7 另列用户配置档的 `OnNetwork/anyExt/user-max-simultaneous-authorizations`，也是该 MCPTT 用户允许同时拥有的业务授权数上限，类型为正整数。业务配置写 `on-network`，用户配置档写 `OnNetwork`。两个文件中的字段不能按同义词替换；只读这里的两条语义不能决定取较小值、谁覆盖谁、如何合并或缺一处时回退到另一处。

用户配置档中的 `call-forwarding-condition` 另用 `immediate`、`no-answer` 区分条件；`call-forwarding-no-answer-timeout` 给出未应答计时的时长。两者都不等于业务配置的即时转发**次数**，也不证明一次呼叫触发或实际转发。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-on-network-service-authorization-forwarding-caps.json)
