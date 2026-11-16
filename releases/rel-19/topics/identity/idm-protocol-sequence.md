# IdM 的 HTTP 顺序：授权端点、令牌端点与服务客户端

仅 TS24.482 V19.0.0 §§4.1、5.3、6.2–6.3 的在网流程。认证成功不等于 MC 业务已获准；具体服务授权另行执行。

## 服务客户端触发，IdM 客户端访问授权端点

适用条件：MC service client 触发用户认证。

IdM client 通过 TLS 访问配置的授权端点，认证请求包含 client_id 及要求参数。正文展开 GET，也允许 OIDC 的 POST 替代。收到用于凭据表单的200后提示用户名/密码并POST；用户名/密码是必须支持的方法，不是唯一允许的方法。

依据：§5.3; 6.2.1; 6.3.1。

## 授权响应之后向另一个端点取令牌

适用条件：已收到 OIDC Authentication Response；完整流程还须执行适用的state等安全检查，见[native-authentication](native-authentication.md)。

IdM client 通过 TLS 连接配置的 token endpoint，通过表单编码POST发送 grant_type=authorization_code 与其余要求参数。服务器验证 Token Request，有效才生成成功 Token Response；不能把表单200或授权响应当作已取得业务 access token。

依据：§6.2.1; 6.3.1。

## 取得响应还需客户端处理和交付

适用条件：IdM client 收到 OIDC Token Response。

本版要求按 OIDC 验证响应中的 ID/access/refresh token，再将 ID/access token交给 MC service client，交付方法由实现决定。这里不把“验证”展开成客户端解码所有JWT；与安全规范的验证分工及字段可选性须分别核对。

依据：§6.2.1。

## 去伙伴域前先向 home 换 security token

适用条件：已取得 home access token，服务客户端请求用于伙伴身份认证的 security token。

通过 TLS 向 home token endpoint 发 token-exchange 表单POST。返回 access_token 字段承载的是 security token，IdM client 提取并暂存，供伙伴令牌请求使用；字段同名不代表可直接当作伙伴业务资源的 access token。暂存到到期或被替换的说明不等于规范定义了安全删除算法。

依据：§4.1; 6.2.2; 6.3.2。

## 证据边界

- OIDC、RFC6749/8693与配置文档完整原文未核，未提供全部错误、超时或重试策略。
- 本版要求客户端验证三类token；不能据此决定opaque access token的解析办法。
- 字段义务及文本疑义见 token-response-obligations；本页不统一跨规范措辞。

## 按需继续

- [native-authentication](native-authentication.md)
- [token-response-obligations](token-response-obligations.md)
- [partner-token-exchange](partner-token-exchange.md)
- [http-transport-endpoints](http-transport-endpoints.md)
- [service-authorization](service-authorization.md)

[ETSI 官方 TS24.482 V19.0.0](https://www.etsi.org/deliver/etsi_ts/124400_124499/124482/19.00.00_60/ts_124482v190000p.pdf)，印刷页7、8、9、10、12、13；仅本版本。

不得把客户端三token验证简化成只检查expires_in，也不得据此要求客户端解码全部token；外部OIDC依赖和两个规范的角色分工尚未完整消解。
