# 用户 Data 的保护与认证：服务器转发不替代客户端验证

TS 24.282 V19.7.0 的普通在网 one-to-one 或组通信，处理信令面承载的 MCData Data 消息；与 Data signalling 和 XML 分开。

本主题只核 6.6 的职责、前提及证据边界，不展开保护协商、密钥分发、TLV 位编码、KDF 或签名算法。

## 保护与端到端签名认证分别判断

适用条件：判断一条 MCData Data 消息是否一定同时具有加密和发起者端到端认证。

6.6.3.1 允许 Data 消息加密并完整性保护，也分别描述整条消息加密和仅 Payload IEs 加密。未保护的 Data 与已保护的 Data 都可以另做端到端认证。因此不能只看 protected 就断言已验证发起者签名，也不能从签名存在断言整个消息已加密。

- 具体采取哪种保护取决于相应协商和调用流程；不由概述断言每份 Data 都已加密或签名。
- 本条未验证 TS 33.180 的具体包格式及位 7/8 编码，不输出实现位图。

依据：§6.6.3.1;6.6.1，印刷页 132、133。

## 客户端按协商保护用户数据

适用条件：客户端发送 MCData Data 消息，或接收 protected MCData Data 消息，按协商的保护方法执行 6.6.3.2。

发送方按协商方法使用对应 DPPK/DPPK-ID 保护 Data：one-to-one 使用 PCK/PCK-ID，组通信使用 GMK/GMK-ID。接收 protected Data 的客户端按协商方法及对应 DPPK/DPPK-ID 解密并认证该保护消息；不能改用服务器逐段信令密钥作为用户 Data 的通用密钥。

- 此处保留 protected 消息 decrypt and authenticate 的原文职责；它不替代下一条针对 signed Data 的签名验证。
- 6.6.2 另引用派生 DPCK 的过程；本页不把角色层 DPPK 描述变成直接将其输入任意密码算法的实现配方。

依据：§6.6.3.2 first and third paragraphs;6.6.1;6.6.2，印刷页 132、133。

## 签名验证依赖发起者身份与KPAK

适用条件：客户端为 MCData Data 生成 authentication signature，或客户端收到 signed MCData Data 消息。

生成签名时使用 KMS 配置的密钥材料。收到 signed Data 的客户端必须使用收到的签名、发起 MCData 客户端身份及 KMS 配置的 KPAK 验证签名。这是明确的客户端职责，不因 PF/CF 转发、共享保护密钥可用或 XML 验签通过而省略。

- 本段未给出发起者身份如何取得/绑定、验签与解密的完整先后、失败后 SIP 响应码或重试策略；不凭 XML 6.5 的 139/140 补全。
- SSK/PVT/KPAK 的配置和认证算法沿用外部依赖，具体内容见关联的密钥知识。

依据：§6.6.3.2 second and fourth paragraphs;6.6.1，印刷页 132、133。

## 服务器转发不替代客户端安全职责

适用条件：PF 或 CF 收到 protected MCData Data 消息，分别执行 6.6.3.3 或 6.6.3.4 的首段，而不是 Data signalling 分支。

PF 和 CF 均应将该 protected Data 转给下一实体，不为它增加安全框架相关动作。该职责与对 Data signalling 的解密及按出口配置重新保护不同，不能要求服务器先解密用户 Data 才能转发，也不能把服务器转发当成已完成客户端签名验证。

- 范围仅是对 protected Data 的安全框架动作，不取消其他条款的身份绑定、业务准入、路由或回执处理。
- 本条未说明所有未保护或仅 signed Data 的完整服务器处理，也不意味着整个 SIP 消息逐字透明或服务器对元数据一无所知。
- 转发本身不是用户已收到、显示或应用处理完成的证明。

依据：§6.6.3.3 first paragraph;6.6.3.4 first paragraph，印刷页 133、134。

## 证据边界

- 仅核本版本指定在网信令面职责，不覆盖完整保护协商、密钥准备及失败恢复；不能将XML错误码或配置缺项默认外推到本页。

## 按需继续

- [security-layers](security-layers.md)
- [xml-inbound-validation](xml-inbound-validation.md)
- [sds-disposition-timing](sds-disposition-timing.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
