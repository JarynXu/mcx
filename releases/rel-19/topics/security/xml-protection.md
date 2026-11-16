# SIP载荷的XML保护：保护范围和服务器可见性

TS33.180 V19.4.0 §9.3；公共安全使用场景的可选应用层机制。

## 服务方决定敏感内容是否需要应用层保护

适用条件：SIP-1/SIP-2传递身份、access token等敏感信息。

服务方可能要求在应用层保护这些信息，连SIP信令层也不能查看。XML机密性和完整性机制是可选机制，不能把本条改写成所有MC SIP消息都必须整包加密。

依据：§9.2.1.1；9.3.1。

## 整份加密仍保留消息类型

适用条件：启用XML机密性保护。

可保护整份XML，也可只保护用户/组标识、位置、告警、令牌、密钥材料或功能别名等字段。整份保护时EncryptedData仍须明确消息类型；服务器支持不能处理整份加密的旧客户端时，应仅保护单独标识和数值。

依据：§9.3.2。

## 完整性启用后覆盖全部XML MIME正文

适用条件：启用XML完整性保护。

SIP请求和响应内所有XML MIME bodies都须保护，每个受保护body对应签名并提供相应Content-ID。此范围是XML正文，不等于整个SIP头部和报文全部受此机制保护。

依据：§9.3.5。

## 持有保护密钥的MC端点可以解密

适用条件：客户端与MC域或MC服务器之间的XML保护。

客户端—MC域使用CSK作为XPK，MC服务器之间使用SPK。服务器提取CSK后可以解密相应用户信息，所以不能从XML加密推出MC服务器看不到内容。KMS—KM客户端有另外的TrK/InK配置条件，应按KMS下发主题判断，不能套用CSK关系。

依据：§9.3.3；9.2.1.3。

## 证据边界

- 不提供W3C XML安全实现、完整KDF或签名验证算法；不是实现符合性认证。
- 本页仅应用层范围，不撤销既有SIP/HTTP接口安全要求。KMS没有InK时的保护路径见KMS主题，不据§9.3.3孤立推出所有部署必须持有InK。

## 按需继续

- [signalling-key-update](signalling-key-update.md)
- [access-transport](access-transport.md)
- [kms-provisioning](kms-provisioning.md)
- [../identity/service-authorization](../identity/service-authorization.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页97、98、100、101、103、104；仅本版本。

## MCData具体XML程序

- [../mcdata/xml-protection-activation](../mcdata/xml-protection-activation.md)
- [../mcdata/xml-server-forwarding](../mcdata/xml-server-forwarding.md)

这些指定程序依据TS24.282 V19.7.0；不从其他安全架构页的可选机制表述推导MCData配置缺项即关闭。
