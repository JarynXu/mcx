# MCData 注册与服务授权入口：REGISTER、PUBLISH 和受保护的身份字段

TS 24.282 V19.7.0 普通 MCData 客户端的第 7 章流程，不把其他版本的 Stage 2 顺序或通用安全要求当成本页报文规则。

仅列关键入口和保护分支，不替代 TS 24.229、TS 24.482、TS 33.180 及 MIME/schema 的完整实现。

## 能力标签不证明授权

适用条件：客户端执行 7.2.1AA 的不携带服务授权流程的 SIP 注册，或判断注册中的服务能力标签代表什么。

本版明确有无服务授权的 REGISTER 流程，仍携带 MCData ICSI，并按所支持的 SDS/FD/IPCONN 携带相应服务能力标签。标签声明支持能力，不是服务授权成功的证据。7.1 另允许以 REGISTER 或服务设置 PUBLISH 进行授权，选择取决于实现及用户认证后 access token 的可用性。

- 初始 REGISTER 不应因缺 token 延迟的明确要求沿既有 TS 33.180 V19.4.0 身份页引用，不冒充 24.282 本条的原文句子。
- 本条不把注册成功推导成允许发起 SDS。

依据：§7.1 first paragraph;7.2.1AA，印刷页 137、139。

## 多服务共享SIP注册

适用条件：MCData 与其他 MC service client 在同一 MC UE 同时运行，或 MCData 退出而其他 MC 服务仍需保持注册。

这些客户端共享 SIP 注册，注册参数组合为单个 REGISTER；其他服务已运行时，MCData 注册采用包含其他服务参数的重新注册。MCData 退出而其他服务保留时，重新注册去掉 MCData 对应标签，但保留其他服务参数。相同 access token 可用于多个服务的授权，也仍需各服务自己的 MIME bodies。

- 多个 Contact 的允许条件还要求相同 IP 地址和端口；不从共享注册推导共享所有业务授权。
- 本条不等于删除整个 UE 的 SIP 注册或清除其他 MC 服务。

依据：§7.1 second–fourth paragraphs，印刷页 137。

## 授权请求的身份与保护

适用条件：客户端已成功完成 24.482 所述用户认证，有可用 access token，并由实现选择 REGISTER 或 PUBLISH 执行 MCData 服务授权。

请求中的 mcdata-info 提供 access token 和发起 MCData client ID。任一 XML 机密性或完整性保护开启时，加入以 MIKEY-SAKKE I_MESSAGE 携带 CSK 的 application/mikey body；仅开启完整性也不能省掉这一条件步骤。机密性开启时 token 与 client ID 都加密，关闭时两者为明文；完整性开启时保护相应 XML bodies，PUBLISH 还保护 poc-settings body 并提交所选 user-profile-index。

- 使用 MCData gateway UE 时另须 gw-mcdata-usage=true；本文不是省略该条件的完整模板。
- PUBLISH 还调用 7.2.1A 设置目标 PF 的 PSI、poc-settings 事件及 Expires。
- REGISTER 完整性调用文号写成 6.6.3.3.3，见原文疑义；不据此自造算法。
- 用户认证及 token 格式/验证在本页未重新核，不能要求客户端自行解码所有 access token。

依据：§7.2.1;7.2.2，印刷页 138、139、140。

## 服务器先验证再识别

适用条件：服务器对含 access token 与 client ID 的授权 REGISTER 内层请求或授权 PUBLISH 执行 7.3.1A；PUBLISH 同时含 poc-settings body。

服务器先识别并验证所施加的 XML 完整性，再处理机密性。token 与 client ID 都受保护时，使用所收 MIKEY-SAKKE I_MESSAGE 的密钥信息解密，成功才从明文识别 MCData ID/client ID；仅其中一个受保护也被判为机密性处理不成功；两者都未加密则从相应明文元素识别。识别身份不等于随后服务授权已通过。

- 无保护的识别分支不是普遍允许绕过保护配置，仍须结合第 7 章调用及 6.5 依赖。
- 对 settings-only PUBLISH，成对字段改为 mcdata-request-uri/client-id，见“MCData 设置刷新、退出与绑定有效期”。
- MIKEY-SAKKE 本身的认证、解封装及 token 中 MCData ID 的获取算法依赖其他规范，未在本页完整核验。

依据：§7.3.1A integrity block and access-token/client-id block，印刷页 143、144。

## 证据边界

- 仅所列普通在网 MCData 分支；完整 SIP 事务、配置 schema、令牌及密码算法依赖按 claim 注明，不能从本页补全。

## 按需继续

- [../identity/primary-registration](../identity/primary-registration.md)
- [../identity/service-authorization](../identity/service-authorization.md)
- [../identity/native-authentication](../identity/native-authentication.md)
- [../identity/idm-protocol-sequence](../identity/idm-protocol-sequence.md)
- [xml-protection-activation](xml-protection-activation.md)
- [xml-inbound-validation](xml-inbound-validation.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文疑义

- §7.2.1 final integrity-protection step：REGISTER 完整性调用写 6.6.3.3.3；已核 XML 完整性 procedure 在 6.5.3.3.3。本页标记不一致，不静默改号。
- §7.3.3 step3;7.3.4 step3;7.3.1A：两个 PUBLISH 调用条款将 7.3.1A 不成功概括为 403/140；该 helper 又调用有各自错误处理的完整性/解密过程。不自行组合为重复 SIP 响应或覆盖全部失败码。

- [MCData设置刷新、退出与绑定有效期](service-settings-validity.md)
