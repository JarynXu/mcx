# 原主叫收到转发MESSAGE后如何重新起呼

在网私呼转发 MESSAGE 到达原主叫后的会话路径选择、按需重呼、结果 MESSAGE 与映射授权衔接。预建立分支只覆盖明确已核的入口和转发专用字段，不宣称完整 REFER/SIP/媒体实现。

forwarded-calling-client是原主叫；forwarded-by-client是请求转发的原被叫；forwarded-to-client是新目标。

## 选择按需或预建立入口

适用条件：原主叫客户端收到 forwarding private call request 的 SIP MESSAGE。

SHOULD 告知用户收到转发请求；SHALL 从 mcpttinfo/mcptt-Params/anyExt/forwarding-target-id 取目标 MCPTT ID。本地策略采用 on-demand 时调用 11.1.1.2.1.1；本地策略采用 pre-established 且有可用预建立会话时调用 11.1.1.2.2.1。

依据：§11.1.9.2.2 steps 1–4。

## 按需路径生成新的initial INVITE

适用条件：客户端接受转发请求并沿 on-demand 路径重呼。

生成新的 initial INVITE，目标为收到的 forwarding-target-id。Priv-Answer-Mode 按原被转发呼叫的值带出；递增 forwarding-sequence-number；call-to-functional-alias-ind=false；session-type=private；anyExt 中 call-forwarding-ind=true，并携带 forwarding-immediate-list 与 forwarding-other-list。若收到 forwarding-target-is-functional-alias=true，则 called-functional-alias-URI 取收到的 forwarding-target-orig-id。

依据：§11.1.1.2.1.1 introductory paragraph, step 9 NOTE 2, step 14C。

## 保存与追加转发历史

适用条件：按需重呼转发请求。

reason=immediate 时向 immediate-list 追加；reason=no-answer 或 manual-input 时向 other-list 追加。entry 包含原文所称 forwarded MCPTT user 的 MCPTT ID；anyExt 含本次序号，并在收到时带入 forwarded-by-mcptt-id、forwarded-by-functional-alias、forwarding-target-orig-id、forwarding-target-is-functional-alias、forwarding-target-id。other-list 另带收到的 forwarding-reason。两份列表缓存到该 INVITE 的 final response 到达。

依据：§11.1.1.2.1.1 step 14C(b)–(e)。

## 预建立路径使用REFER

适用条件：本地策略采用预建立并有可用会话，且接受转发请求。

使用 dialog 外 SIP REFER，不是 initial INVITE；目标仍取 forwarding-target-id。转发分支递增序号、按 immediate/no-answer/manual-input 分流历史、置 call-forwarding-ind=true 与 call-to-functional-alias-ind=false；原目标是别名时保留 called-functional-alias-URI。两份列表缓存到 REFER 的 final response；Target-Dialog 指向预建立会话。

依据：§11.1.1.2.2.1 introductory paragraph and step 8c(ii)D1–G; step 12。

## 证据边界

- 原文未规定本地策略选择预建立但无可用会话时自动回退按需。
- SHOULD 告知不等于本段规定必须弹出用户确认或允许拒绝的完整 UI 流程。
- 普通呼叫由用户首次发起时 step 14B 将序号置 0；转发序号是同一呼叫 immediate 与 other 的总序号，首次转发为 1。
- 不推导缺少原 Priv-Answer-Mode 时的具体报文修复；按原文保留条件与字段。
- 不把解析后的目标 MCPTT ID 和原目标别名互换。
- 这些条件未包含 migrated，不把迁移转发自行归入 immediate 或 other。
- 原文 forwarded MCPTT user 的表述不替换成未经明确证明的其他角色。
- 原文 other 分支 forwarding-target- orig-id 含空格异常；不据此生成完整 XML。
- 缓存直到 final response 不扩展成缓存自动销毁或无限保留策略。
- 完整 Refer-To/hname 编码、应答及媒体绑定不在此主题复现。
- 按需 INVITE 和预建立 REFER 的 final response 不混为同一事务。

## 按需继续

- [forwarding-message-routing](forwarding-message-routing.md)
- [forwarding-client-results](forwarding-client-results.md)
- [originating-authorization](originating-authorization.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页415、418、419、428、430、431、432、507、508；仅本版本。
