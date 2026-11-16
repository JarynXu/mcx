# Bearer 失败不能一律归成403

RFC6750 原始2012-10版本的选定资源请求规则。MCX 的特定入口拒绝仍见 http-sender-identity，不用通用示例覆盖其明确分支。

## 按失败原因区分响应

适用条件：资源请求失败且按 RFC6750处理。

请求畸形或重复传token为 invalid_request，SHOULD 400；过期、撤销等无效token为 invalid_token，SHOULD 401，客户端 MAY 取得新token重试；权限不足为 insufficient_scope，SHOULD 403，可返回所需scope。SHOULD不是无条件必然返回该码。

依据：§3.1。

## 一次请求只能采用一种token传递方式

适用条件：客户端发送 bearer 资源请求。

不得同时用多种方式携带token；Authorization头是推荐方式且资源服务器必须支持。无认证信息时须提供 Bearer WWW-Authenticate；服务器 SHOULD NOT 附带错误码或其他错误信息。MCX UE已有Bearer时须用头的更具体规则另见身份页。

依据：§2; 2.1; 3; 3.1。

## TLS止于代理后仍需保护token

适用条件：TLS在真正提供资源的后端之前终止。

前端到后端仍须采取足够措施保密token，加密token只是可能方法之一。本节不规定token编码或完整验证算法，也不是当前TLS版本选择指南。

依据：§5.2。

## 证据边界

- 只核所列RFC规则；不实现完整OAuth/JWT/OIDC验证。
- TS24.482 V19.0.0 无token且无断言头明确403，不能被RFC的通用401示例替换。
- 取得新token与重试为MAY，不能当作自动无限重试许可。

## 按需继续

- [http-sender-identity](http-sender-identity.md)
- [http-transport-endpoints](http-transport-endpoints.md)
- [token-refresh](token-refresh.md)

[RFC6750 官方原文](https://www.rfc-editor.org/rfc/rfc6750.html)，§2、2.1、3.1、5.2；2012-10。

这些错误用于 Bearer 受保护资源请求，不是 IdM token endpoint 的错误表。
