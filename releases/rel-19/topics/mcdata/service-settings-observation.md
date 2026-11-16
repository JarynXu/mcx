# 观察 MCData 服务设置：同用户跨 client、订阅期限与通知归属

依据 TS 24.282 V19.7.0 的 7.2.4/7.3.6，发现同一 MCData 用户另一个 client 的设置，或核验当前 client 的设置，不将观察过程当作设置修改或服务授权。

客户端发送与服务器入口的 ICSI 字面存在未解差异，见下述 claim 及下方原文疑义；本页给可靠角色和状态边界，不提供已消解差异的互通报文模板。

## 区分服务器地址和用户目标

适用条件：客户端发起 7.2.4 的初始服务设置 SUBSCRIBE，以观察同一用户的本 client 或另一 client。

Request-URI 指向服务该用户的 originating PF 的 PSI；mcdata-info 中的 mcdata-request-uri 才是该 MCData 用户的 ID。客户端还设置 P-Preferred-Service 为 MCData ICSI、Event=poc-settings、Accept=application/poc-settings+xml。不能把目标 PF 地址当作被观察用户 ID，也不能借此查询任意其他用户。

- 此处客户端 ICSI 为 urn:urn-7:3gpp-service.ims.icsi.mcdata；与服务器入口的字面差异不在本文修正。
- TS 24.229、RFC 6665/4354/6050 及完整 XML 安全/事件包实现未在本批展开。

依据：§7.2.4 opening and initial SUBSCRIBE steps1–5，印刷页 141。

## Expires=0的两种订阅语境

适用条件：客户端已构造本服务设置观察请求，选择只取当前状态、继续观察或取消既有订阅。

初始 SUBSCRIBE 只取当前状态时 Expires=0；要当前状态及后续通知时设为 4294967295。重新订阅或取消订阅使用 in-dialog SUBSCRIBE，同样携带 poc-settings Event 和对应 Accept；继续观察设 4294967295，取消设 0。不能把这里的 SUBSCRIBE Expires=0 等同于 PUBLISH Expires=0 的 MCData 服务退出。

- 4294967295 是客户端请求值，不是已核服务器保证的永久订阅，也不延长 token 或服务授权绑定。
- 初始只取状态和 in-dialog 取消订阅虽然都用 0，语境不同；通知时序和完整订阅终止规则依赖 RFC 6665。

依据：§7.2.4 initial steps6–7 and in-dialog steps1–4;7.2.1A NOTE3，印刷页 140、141、142。

## 服务器仅允许同用户观察

适用条件：服务器收到符合 7.3.6.1 命名入口的 SUBSCRIBE：Request-URI 为服务 PF 的 PSI，mcdata-info 的 mcdata-request-uri 标识其所服务的 MCData ID，Event 为 poc-settings，P-Asserted-Service 含原文所列 ICSI。

服务器从 XML 取被观察的 served MCData ID，从 P-Asserted-Identity 的 public user identity 确定 originating MCData ID。两者不同即 403 并停止；未因此拒绝才生成 200，并在订阅持续期间按 7.3.6.2 通知设置变化。跨 client 不等于跨用户，订阅 200 也不是已经拿到每个 client 设置内容的证明。

- 服务器入口的原文 ICSI 是 urn:urn-7:3gpp-service.ims.icsi.mcdata,sds，包含逗号；不能静默改成 .sds 或客户端的无后缀 mcdata。
- 该分支没有为身份映射缺失/过期给出与 SDS 相同的 404/141 算法，也没有为这里的 403 指定 Warning；不移植其他流程。

依据：§7.3.6.1，印刷页 149。

## 按client识别并缓存通知

适用条件：服务器通知该订阅用户的设置变化，或客户端收到符合 7.2.4 所引 SIP/事件包规则且含 poc-settings body 的 NOTIFY。

服务器构造的 NOTIFY body 包含表示 active MCData user profile 的 selected-user-profile-index。接收客户端按 body 的 id 属性识别各 MCData client，分别缓存 am-settings 为该 client 的当前 Answer-mode，缓存 selected-user-profile-index 为该 client 的 active profile；不能把另一 client 的通知自动套为本机设置。

- 7.3.6.2 的服务器构造步骤只明确列 selected-user-profile-index，不能由客户端缓存 am-settings 的语句推导每次通知必含完整 Answer-mode 设置。
- id 属性的 schema/实例标识映射依赖 RFC 4354；缺字段、重复 id、缓存替换及接收失败的完整处理不在本段给出。
- 此处是观察和缓存，不是发送 PUBLISH 修改该 client 的配置，也不证明已下载整个 user profile 文档。

依据：§7.3.6.2;7.2.4 final NOTIFY processing，印刷页 142、149。

## 证据边界

- 限本页所列 MCData 协议分支；外部事件包、SIP 状态机及密码算法依赖不因接口引用而视为完整核验。

## 按需继续

- [service-settings-validity](service-settings-validity.md)
- [service-authorization-binding](service-authorization-binding.md)
- [../identity/profile-selection](../identity/profile-selection.md)
- [../identity/profile-acquisition](../identity/profile-acquisition.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文疑义

- §7.2.4 initial step3 versus 7.3.6.1 opening：客户端 P-Preferred-Service 使用 urn:urn-7:3gpp-service.ims.icsi.mcdata；服务器 P-Asserted-Service 入口写 urn:urn-7:3gpp-service.ims.icsi.mcdata,sds，含逗号，且入口编号重复 3。保留字面差异，不更正成点号后缀或自动统一。
- §7.2.4 final NOTIFY processing versus 7.3.6.2：客户端缓存 am-settings 和 selected-user-profile-index；服务器通知构造步骤只明确列 selected-user-profile-index。不能由接收缓存语句补成每个 NOTIFY 的完整必选字段模板。
