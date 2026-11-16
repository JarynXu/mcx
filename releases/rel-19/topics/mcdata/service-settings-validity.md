# MCData 设置刷新、退出与绑定有效期：哪些续期不能相互替代

TS 24.282 V19.7.0 第 7 章普通服务设置处理；区分 SIP 注册有效期、access token 有效期、身份绑定有效期和 service settings 到期。

设置更新与删除依赖相应 RFC 3903 处理；本文不推定未核 SIP 事务、ETag、缓存一致性或重试行为。

## 设置Expires的范围

适用条件：客户端调用 7.2.1A 填充授权/设置 PUBLISH，更新或刷新设置而非移除设置。

Request-URI 指向服务该用户的 PF 的 PSI，Event 为 poc-settings；非移除操作将 Expires 设为 4294967295。设置计时器只适用于匹配 Instance Identifier URN 的 client settings，更新它时服务器也更新 user service settings 的计时器。此值不是 access token 或身份绑定永久有效的证明。

- 本章没有据此规定绑定寿命等于该 Expires 或等于 token exp，也没有在此定义 token 刷新协议。
- 设置被移除时 Expires 改为 0，另见退出条目；自然到期不能直接套用显式 Expires=0 的全部清理动作。

依据：§7.2.1A steps1–4 and NOTE1–2;7.2.3 opening，印刷页 139、140、141。

## 失效绑定不能靠设置更新续回

适用条件：服务器进入 7.3.4：poc-settings Event、poc-settings body，以及含 mcdata-request-uri/client-id 的 mcdata-info body；不是含 token 的新服务授权入口。

服务器执行 7.3.1A，其中 request-uri/client-id 的成对机密性处理失败会触发调用者的 403/Warning140 并停止。还须验证现存 public user identity 与目标 MCData ID 的绑定；绑定不存在或已过期则 404 并停止。不能靠 settings-only 刷新请求重新建立已失效的授权绑定。

- 7.3.4 step1 从 P-Asserted-Identity 识别 IMS public user identity，step4 却写 Request-URI 中的该 identity，而客户端 7.2.1A 把 Request-URI 设成 PF PSI。保留此冲突，不提供替标准选择字段的算法。
- 两成对字段都加密时要求解密成功，只有一个加密也判保护不成功；没有加密的识别分支不等于放弃配置要求。
- 本入口没有把新的 access token 作为字段；不能把它等同于 token refresh grant。

依据：§7.2.3;7.3.1A request-uri/client-id block;7.3.4 opening and steps1–6，印刷页 141、144、145、147、148。

## 设置成功与后续profile处理

适用条件：授权 PUBLISH 已成功服务授权，或 settings-only PUBLISH 的绑定存在且未过期；相应前置安全/并发等适用门槛未阻断，并且 RFC 3903 PUBLISH 处理成功。

服务器缓存 service settings 至设置到期并发送 200；后续按 selected-user-profile-index 识别 active profile，必要时下载。缺 index 且有多个 profiles 时选含 Pre-selected-indication 的 profile，只有一个时默认它为预选项。profile 中有配置的 ImplicitAffiliations group entries 才调用 8.3.2.15，不是任意 200 都代表所有组已归属。

- 200 表示本设置通信的成功边界，profile 下载失败、预选标记缺失或冲突、隐式归属失败的完整处理不在本条补写。
- 8.3.2.15 的具体归属建立与结果本批未展开；不得把调用该过程写成归属已经成功。

依据：§7.3.3 steps7–12 and NOTE3–4;7.3.4 steps7–12 and NOTE1–2;7.2.3 final paragraph，印刷页 141、147、148。

## 显式退出的清理范围

适用条件：客户端移除 service settings 时发出 Expires=0 的 poc-settings PUBLISH；服务器收到此 Event 与 Expires 组合，按 RFC 3903 处理且成功。

这一路径使 MCData client 退出服务。服务器识别 P-Asserted-Identity 中的 IMS public user identity，成功处理后移除 service settings；原文 NOTE 说明包括移除所有 group affiliations；随后移除 MCData ID 与 public user identity 的绑定，并发送 200。

- 此处 all group affiliations 与多 client 并存、设置计时器按 Instance Identifier 限定之间，没有完整清理选择算法；不擅自扩大为用户所有设备的全部授权绑定都删除，也不删去原文 all。
- 这不是 SUBSCRIBE Expires=0 的只取当前状态语义，也不是 token 普通过期的自动删钥规则。
- 若其他 MC 服务仍注册，MCData 标签移除另按 7.1 重新注册，不让本退出步骤自动注销其他服务。

依据：§7.2.1A step4 and NOTE3;7.3.5，印刷页 139、140、148、149。

## 后续SDS仍检查当前绑定

适用条件：之后 O-PF 收到普通 standalone SDS 控制面 MESSAGE，资源/拥塞分支未终止处理，执行 9.2.2.3.1 的身份检查。

O-PF 从 P-Asserted-Identity 中的 public user identity 确定 MCData ID；该绑定来自服务授权，但到本次 SDS 时必须仍能找到且未过期，否则 404/Warning141 并停止。设置曾刷新、SIP 仍注册或客户端持有密钥，都不能替代这次绑定检查；有效绑定之后还另有本次通信授权。

- 本条仅作生命周期与既有 SDS 页的衔接，不重写 SDS 权限、大小和目标策略矩阵。
- 终接 PF 的独立条款没有复述相同过期/Warning141 条件，不将本发起侧规则当成所有入口的统一错误码。

依据：§9.2.2.3.1 steps1–3 and NOTE1,step6，印刷页 195、196。

## 证据边界

- 仅所列普通在网 MCData 分支；完整 SIP 事务、配置 schema、令牌及密码算法依赖按 claim 注明，不能从本页补全。

## 按需继续

- [../identity/token-refresh](../identity/token-refresh.md)
- [../identity/profile-selection](../identity/profile-selection.md)
- [../security/ue-key-lifecycle](../security/ue-key-lifecycle.md)
- [../security/signalling-key-update](../security/signalling-key-update.md)
- [sds-server-identities-and-private-admission](sds-server-identities-and-private-admission.md)
- [sds-notification-routing](sds-notification-routing.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文疑义

- §7.3.4 steps1,4 versus 7.2.1A step1：step1 从 PAI 取 IMS public user identity；step4 却指定 Request-URI 中的该 identity；客户端将 Request-URI 设为 PF 的 PSI。未裁决字段优先级或修正算法。
- §7.2.1A NOTE2;7.3.2 step4a;7.3.3 step5b;7.3.5 NOTE：client settings timer 有 Instance Identifier 范围，服务授权允许保留多 client 绑定；显式移除又称 all group affiliations，且绑定移除未细化 client 选择。保留原文，不推导跨全部设备或仅单设备的完整清理算法。
