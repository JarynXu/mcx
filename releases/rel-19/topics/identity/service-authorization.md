# SIP 注册之后：服务范围、令牌校验与身份绑定

TS33.180 V19.4.0；区分SIP注册与MC用户服务授权。

## 初始 REGISTER 不等令牌

适用条件：初始SIP注册尚无access token。

不得仅因缺access token延迟REGISTER；先不携带令牌完成SIP注册，随后按服务授权流程发送令牌。不能据注册完成推定MC服务已全部授权。

依据：§5.1.3.2.1。

## 校验服务范围后才建立身份关联

适用条件：MCPTT、MCVideo或MCData用户服务授权。

客户端通过REGISTER（后续第三方注册）或PUBLISH送相应服务scope的access token。服务器校验成功后授权、确认，并建立维护IMPU与相应MC service ID关联；此关联仅应用层知晓。某一条REGISTER或PUBLISH是否携带令牌可选，不意味着服务授权免验证。

依据：§5.1.3.1、§5.1.3.2.2、§5.1.3.2.3。

## 位置消息另有逐条授权与异常策略

适用条件：UE支持MC位置服务；LMC向LMS发送位置消息。

每条位置消息携带location-management scope的access token；LMS验证成功才按流程处理。无法验证时可按本地策略处理，例如紧急情况下存储位置报告；这不是普遍免认证许可，也不自动授权向第三方披露。

依据：§5.1.3.1。

## 消费方各自验证

适用条件：使用取得的令牌。

客户端按OIDC规定验证ID token，资源服务器按RFC7519验证access token；HTTP bearer令牌放Authorization头。scope无效、过期或撤销时资源服务器应返回相应错误。SIP传递路径按§5.1.3，不能将HTTP头规则套到所有消息。

依据：§B.10、§B.11.1、§B.11.2。

## 证据边界

- OIDC/RFC7519完整验证规则未核；这里不提供JWT算法白名单、完整重放防护或Stage3 SIP编码。
- 位置异常处理为本地策略示例，不覆盖所有服务的失败策略。

## 按需继续

- [primary-registration](primary-registration.md)
- [native-authentication](native-authentication.md)
- [token-refresh](token-refresh.md)
- [on-demand-usage](../location/on-demand-usage.md)
- [kms-provisioning](../security/kms-provisioning.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，所列条款，印刷页 30、31、32、33、34、35、139；仅本版本，不声明与后续版本等同。

- [profile-selection](profile-selection.md)

配置数据另见：[获取](profile-acquisition.md)、[更新](profile-update.md)。
