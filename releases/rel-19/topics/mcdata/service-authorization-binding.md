# MCData 服务授权如何建立绑定：身份来源、并发上限和响应边界

TS 24.282 V19.7.0 普通 MCData server，分别进入 7.3.2 的第三方 REGISTER 或 7.3.3 的授权 PUBLISH 入口。

本页不列全部通用 SIP 分类条件；7.3.1 对 PUBLISH 识别还描述 SDS feature tag 及 require/explicit。完整分类和传输依赖 TS 24.229，不由 token 元素的单独存在决定。

## REGISTER与PUBLISH身份来源

适用条件：REGISTER 入口收到第三方 REGISTER，其中 message/sip body 包含客户端 REGISTER，内层 mcdata-info 含 token/client ID；或 PUBLISH 入口含 poc-settings Event、poc-settings body、含 token/client ID 的 mcdata-info body。

REGISTER 分支从第三方 REGISTER 识别 IMS public user identity，从内层客户端请求经 7.3.1A 识别 MCData 身份；PUBLISH 分支从 P-Asserted-Identity 识别 IMS public user identity，再执行 7.3.1A。PUBLISH 的 7.3.1A 处理不成功时，本调用条款明确发送 403/Warning140 并停止；不能把 XML 声明的 client ID 当成已经完成的 IMS 身份绑定。

- REGISTER 不得机械复制 PUBLISH 的 403/140 调用分支。
- 7.3.1A 内部还调用有自身验签失败响应的 6.5 程序；不据调用者的概括失败分支发明第二次响应或统一覆盖所有错误码。

依据：§7.3.2 opening and steps1–2;7.3.3 opening and steps1–3，印刷页 145、146。

## 并发上限的分支差异

适用条件：服务器已到达相应授权流程的并发数检查；身份提取及前置安全处理未阻断。

检查用户 profile 的 user-max-simultaneous-authorizations；该项不存在时，检查服务配置的 max-simultaneous-authorizations。达到适用上限后不能继续授权流程。REGISTER 条款在此只写停止；PUBLISH 明确发送 486/Warning228 并停止。不能给 REGISTER 擅自补上相同响应码。

- 未核 24.484 对两项缺失、取值范围及计数规则的完整定义，不能将缺配置推成无限制或自行定义重授权如何计数。
- PUBLISH step3A 未像 REGISTER step2A 一样重述 if present；本页保留 step3B 的明确缺项回退，不由措辞差异构造额外拒绝算法。

依据：§7.3.2 steps2A–2B;7.3.3 steps3A–3B，印刷页 145、146。

## 成功授权后的多客户端绑定

适用条件：已通过对应入口及并发检查，服务器按 33.180 执行服务授权且成功。

服务器绑定 MCData ID、MCData client ID 与 IMS public user identity。若同一用户此前已在另一 client 授权，以 client ID 与既有绑定比较确认后，应保留当前绑定并新增此 client 的绑定，而非踢掉旧 client。多于一个绑定时，相应 200 的 mcdata-info 含 multiple-devices-ind=true。

- 以上多客户端成功分支仍受并发上限约束。
- Resource-Share=supported 时还存在与 registration-token 所标 UE 身份的条件绑定，本文未把三元绑定当作全部数据库字段。
- PUBLISH 中建立绑定是 step5，先于 step7 的 RFC 3903 处理和 step9 的 200；本段没有明确后续处理失败时的回滚，不能改写成只有最终 200 后才建绑定。

依据：§7.3.2 steps3–4a,6;7.3.3 steps4–5b,9a，印刷页 145、146、147。

## 授权与设置处理的不同成功点

适用条件：服务器处理 7.3.3 授权 PUBLISH，安全和并发检查未终止，已执行服务授权。

服务授权失败时，403/Warning101 并停止。成功时还须处理 RFC 3903 PUBLISH；该处理不成功则不继续。处理成功后缓存收到的 service settings 到设置到期，并发 200。不能把 token 可读取、服务授权成功、PUBLISH 处理成功合成一个不可区分的事件。

- REGISTER 的 7.3.2 没有在相同位置给出 PUBLISH 这套显式授权失败响应；不移植。
- PUBLISH 200 后条款仍列 profile 选择及有条件的隐式归属步骤，因此该 200 不证明隐式归属已全部完成。
- token 验证及授权算法仍是 33.180 依赖，不把本条 403/101 当作全部 token 错误映射。

依据：§7.3.3 steps4–9，印刷页 146、147。

## 证据边界

- 仅所列普通在网 MCData 分支；完整 SIP 事务、配置 schema、令牌及密码算法依赖按 claim 注明，不能从本页补全。

## 按需继续

- [../identity/service-authorization](../identity/service-authorization.md)
- [../identity/token-refresh](../identity/token-refresh.md)
- [sds-server-identities-and-private-admission](sds-server-identities-and-private-admission.md)
- [sds-notification-routing](sds-notification-routing.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文疑义

- §7.3.3 step3;7.3.4 step3;7.3.1A：两个 PUBLISH 调用条款将 7.3.1A 不成功概括为 403/140；该 helper 又调用有各自错误处理的完整性/解密过程。不自行组合为重复 SIP 响应或覆盖全部失败码。
