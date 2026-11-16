# MCVideo注册与服务授权：令牌、保护检查和多客户端绑定

TS24.281 V19.3.0 第7章的普通在网 MCVideo 客户端与服务该用户的 PF/server；第10章仅作普通 on-demand、带 transmission control、直接单用户私呼的准入衔接。排除 partner migration、MCVideo gateway UE 接入、跨系统 gateway、别名/FTA、远程/ambient、优先通信及其例外。

每条 claim 只继承本主题 common_conditions 和自身 conditions。SIP 注册、用户认证、MCVideo 服务授权、CSK 可用、service settings 成功传达、某次呼叫获准及媒体发送/接收许可是不同结果。

外部 TS24.229、TS24.482、TS24.484、TS29.283、TS33.180 及 RFC/XML 算法只按明确调用定位依赖；不以别的服务、版本或既有高层概要补造本版报文、错误码、回滚和寿命。

## 共享注册与服务授权分开判断

适用条件：MCVideo client 执行 SIP 注册；共享注册部分另以同一 MC UE 同时运行其他 MC service client 为条件。

本版明确有无服务授权的 REGISTER 入口，二者都带 Contact 的 g.3gpp.mcvideo 与对应 MCVideo ICSI tag。服务授权可选 REGISTER 或服务设置 PUBLISH，选择依据实现及认证后 token 是否可用。若其他 MC 客户端同机运行，则组合为一个共享 REGISTER；其他服务已在运行时重新注册须保留其参数。即使 access token 相同，各服务仍有各自 MIME bodies；多个 Contact 还要求同 IP 和端口。因此 SIP 注册或能力标签本身不证明 MCVideo 已获服务授权。

- 不因本条列无授权 REGISTER 就把用户认证/令牌验证省略。“不得仅因缺 token 延迟 REGISTER”的直接证据在既有 TS33.180 V19.4.0 身份页，不冒充本条逐字要求。
- 支持 MCVideo service continuity 时，7.2.1AA 另调用 TS24.237 的 PS-to-PS IMS 注册；此依赖未展开，不声称普通注册覆盖连续性全流程。

依据：§7.1;7.2.1;7.2.1AA，印刷页 151、152、153。

## token、client ID 与保护开关

适用条件：客户端已成功完成用户认证、有可用 access token，并按实现选择 REGISTER 或授权加设置 PUBLISH；分别使用 §7.2.1 或 §7.2.2。

授权 XML 同时提供 mcvideo-access-token 和发起 mcvideo-client-id。任一机密性或完整性保护开启时，须加入 application/mikey，以 MIKEY-SAKKE I_MESSAGE 携带 CSK；仅完整性开启也不能省略此步骤。机密性开启则两字段都加密，关闭则均为明文；完整性开启则保护 mcvideo-info，PUBLISH 还保护 poc-settings。客户端保护配置中，confidentiality-protection 或 integrity-protection 各自缺失/true 表示相应保护开启，false 才关闭，不能套用“未配置即关闭”。

- 用户认证、token 格式/校验、CSK 产生与 MIKEY-SAKKE 密钥供应仍依赖 TS24.482/TS33.180；此 claim 不要求客户端任意解码 token，也不把 CSK 解封装成功当服务授权成功。
- gateway UE 条件被本页范围排除；该分支原文另要求 gw-mcvideo-usage=true，不能把本页摘要当作 gateway UE 完整模板。
- 完整 XML/MIME 编码与属性加密未在此实现；6.6.2.3.3 的算法文字自身含 AES-128-GCM algorithm HMAC，保留未核算法依赖，不按常识修写。

依据：§7.2.1;7.2.2;6.6.2.3.1;6.6.3.3.1;6.6.2.3.3，印刷页 143、144、148、152、153、154、155。

## 先核保护再读身份

适用条件：服务器进入 §7.3.1A：第三方 REGISTER 内含客户端 message/sip 请求，或授权 PUBLISH 含 mcvideo-info 的 token/client-id 与 poc-settings。

先判断并验证各 XML MIME body 的完整性，检查通过或原本未受完整性保护才继续判断机密性。token/client-id 都加密时，用收到 I_MESSAGE 的密钥信息解密，成功后才识别 MCVideo ID/client ID；只有一个加密即判机密性处理失败；均未加密时从明文字段识别。身份可读与服务授权通过不是同一步。授权 PUBLISH 调用者在 7.3.1A 不成功时明确回 403/Warning140 并停止；不能把此调用者规则复制成 REGISTER 的统一错误。

- 完整性 helper 的 reference/signature 验证失败自身明确 403/Warning139；缺 Signature 必需子元素且不能由其他方式获知时则失败退出。保留 helper 与调用者各自条件，不发明第二次响应或声称所有失败统一140。
- 无加密/签名的识别分支不豁免发送侧配置；不据其存在允许丢弃已要求的保护。
- 7.3.1 对 PUBLISH 识别还写 g.3gpp.mcvideo tag 及 require/explicit；本页不把 token 元素单独存在当作完整 SIP 分类条件。

依据：§7.3.1;7.3.1A;7.3.3 steps1–3;6.6.3.4.2;6.6.2.4.2，印刷页 145、149、157、158、160。

## 并发授权上限与方法差异

适用条件：服务器已进入第三方 REGISTER 的 §7.3.2 或授权 PUBLISH 的 §7.3.3，并完成该方法在上限检查之前的身份/保护步骤。

先查 user profile 的 OnNetwork/anyExt/user-max-simultaneous-authorizations；该项存在时检查是否达到上限，缺失才查 service configuration 的 OnNetwork/anyExt/max-simultaneous-authorizations。达到适用上限均停止后续步骤，但 REGISTER 条款只明写停止；PUBLISH 明确回 486/Warning166 后停止。这里的166是 MCVideo 本版响应，不能移植 MCData 的228。

- 未核 TS24.484 对两项都缺失、计数口径、重复授权和取值范围的完整定义，不把缺配置理解为无限制，也不补 REGISTER 的相同响应码。
- 这是最大同时服务授权数，不是呼叫数 N6、媒体并发源数、组成员数或一个用户的静态 client 列表。

依据：§7.3.2 steps2a–2b;7.3.3 steps3a–3b，印刷页 159、160、161。

## 多 client 身份绑定

适用条件：REGISTER 或授权 PUBLISH 已按 TS33.180 对识别出的 MCVideo ID 授权成功，且该方法此前检查未停止；多客户端部分另要求同一用户已在另一 MCVideo client 授权。

服务器将 MCVideo ID、MCVideo client ID 绑定到 IMS public user identity。REGISTER 的 IMS identity 来自第三方 REGISTER；PUBLISH 来自 P-Asserted-Identity。另一 client 已授权时保留原绑定并建立新绑定；PUBLISH 明确通过 received client ID 与既有绑定比较判断这一情形。若同一 MCVideo ID 存在多个绑定，相应 200 的 mcvideo-info 带 multiple-devices-ind=true，而非自动踢掉旧 client。

- 三元绑定不是全部状态：Resource-Share=supported 时原文另有与 registration-token 所标 MCVideo UE 的绑定；external database 还存 server identifier。未重做这些接口，不把本摘要当数据库schema。
- 多设备成功仍受并发授权上限限制。REGISTER 的该成功段没有复制 PUBLISH 明确的 403/101 失败步骤，不统一方法的失败码。
- PUBLISH step5 建立绑定先于 step7 RFC处理及 step9 的200；不能改成“只有最终200之后才建绑定”，也不能补规范未给的后续失败回滚。

依据：§7.3.2 steps1–6;7.3.3 steps1,4–5,9;6.8，印刷页 150、159、160、161。

## 授权成功与设置发布结果

适用条件：服务器收到 Event=poc-settings、application/poc-settings+xml，以及含 token/client-id 的 mcvideo-info 的授权 PUBLISH；先前身份、保护、上限检查已通过。

服务授权失败则 403/Warning101 并停止。授权成功、建立绑定之后，仍须按 RFC3903 处理 PUBLISH；处理失败就不继续。处理成功才缓存 settings 至设置计时器到期，并发送200。Answer-Mode、multiplex 支持、active profile 和条件隐式 affiliation 的处理仍排在该200之后，不能把200当作所有 profile/归属工作或下一次呼叫均已完成。

- 第7章未给所有 RFC3903 错误或 client 重试算法，不能自行补 ETag、缓存一致性、回滚和绑定到期时刻。
- 隐式 affiliation 是条件调用，不是调用即成功；partner migration 的 step14 已排除。

依据：§7.3.3 steps4–13，印刷页 161、162。

## 证据边界

- 普通本系统路径。外部认证、配置schema完整性、MIKEY算法、partner migration、gateway UE、全SIP事务和当前call强制结束未闭合；settings订阅仅有界观察链。

## 按需继续

- [../identity/service-authorization](../identity/service-authorization.md)
- [service-settings-validity](service-settings-validity.md)
- [csk-key-update](csk-key-update.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

服务授权之后，另行判断发送紧急告警的用户与组权限，见[紧急告警 MESSAGE：权限、组内通知与接收确认](emergency-alert-message.md)。
