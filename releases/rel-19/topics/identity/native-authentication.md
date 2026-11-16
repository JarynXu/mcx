# 原生客户端认证：注册、授权码与令牌分别做什么

TS33.180 V19.4.0；Annex B 本版详细定义的是 native MCX client。

## 先登记客户端

取令牌前客户端须向IdMS登记，原生客户端登记client_id与redirect URI；登记方法不由此profile规定。不能把这项登记和用户SIP注册混为一件事。

依据：§B.3、§B.4.1。

## 取得授权码，再交换令牌

适用条件：原生授权码流程。

认证请求使用response_type=code、已登记的client_id和redirect_uri、包含必选openid的scope、state、acr_values及PKCE的code_challenge/S256。响应state必须完全匹配；不匹配须忽略授权码，不交换令牌，也不返回错误。令牌请求使用grant_type=authorization_code并携带code_verifier，redirect_uri与认证请求一致；本条要求原生客户端认证（使用PKCE），若用client secret则按规定置于Authorization头。

依据：§B.4.2.2、§B.4.2.3、§B.4.2.4。

## 按消费方区分令牌

适用条件：令牌响应有效且获授权。

ID token由客户端消费，用于识别用户/MC service ID；access token交资源服务器用于服务访问。虽然流程概述描述三类令牌，B.4.2.5表明确把ID token与refresh token列为可选，不能据概述保证每次均有三个。

依据：§5.1.2.1、§5.1.2.3.1、§B.4.2.5。

## 证据边界

- 这里只给关键约束，不复制完整参数表或OIDC错误状态机。
- OIDC Core及RFC6749/7636等依赖原文未核，不能把本页当完整安全实现；PKCE与客户端认证的原文表述被保留，不擅自等同。

## 按需继续

- [service-authorization](service-authorization.md)
- [token-refresh](token-refresh.md)
- [access-transport](../security/access-transport.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，所列条款，印刷页 27、28、29、30、128、129、130、131、132；仅本版本，不声明与后续版本等同。

## 跨规范使用前

[令牌响应义务差异](token-response-obligations.md)列出 TS24.482 V19.0.0 与本页安全规范版本的不同措辞。不要把 ID/refresh 字段必选性静默统一。

按需续读：[协议步骤](idm-protocol-sequence.md)，注意页面所标规范版本及独立适用条件。
