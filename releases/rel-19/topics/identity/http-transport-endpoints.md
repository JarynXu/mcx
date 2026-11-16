# HTTP 代理与 IdM 直连的 TLS 端点

仅 TS24.482 V19.0.0 Annex A；本页解释连接端点，不替代 TLS 密码套件或证书配置规范。

## 普通资源连接代理，IdM 流程直连

适用条件：UE 建立 HTTP 所用连接。

通常按配置连接 home HTTP proxy 的 FQDN/port；用于 §6.2、§6.3 的 IdM 客户端到服务器流程时改为连接 IdM server。在使用证书认证、收到服务器证书时：连接终止于代理则核对代理 FQDN，而非资源 URL；连接终止于 IdM 则核对所连接 IdM 服务器的 URL 身份。不能要求 PSK 分支凭空具有服务器证书。

依据：§A.2.1.2。

## 传输保护与协议语义同时保留

适用条件：UE HTTP 客户端。

所有 HTTP 消息经 TLS。认证方式按配置选择代理证书单向认证、证书双向认证或预共享密钥双向认证，并使用对应凭据。按所用 HTTP/1.1 或 HTTP/2 保持语义；位置管理客户端另外要求支持 HTTP/2。

依据：§A.2.1.1; A.2.1.2。

## 证据边界

- 本页没有校验 RFC2818、HTTP 各 RFC 和 TS33.180 的所有算法细节。
- TLS 可止于代理；不能由此声称资源服务器与 UE 之间天然端到端加密。
- V19.0.0 与后续版本未比较。

## 按需继续

- [http-sender-identity](http-sender-identity.md)
- [native-authentication](native-authentication.md)
- [../security/access-transport](../security/access-transport.md)

[ETSI 官方 TS24.482 V19.0.0](https://www.etsi.org/deliver/etsi_ts/124400_124499/124482/19.00.00_60/ts_124482v190000p.pdf)，印刷页14、15；仅本版本。
