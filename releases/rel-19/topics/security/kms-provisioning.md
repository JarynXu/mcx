# KMS 角色与密钥获取：先区分直接连接和代理

TS33.180 V19.4.0；KM client 的用户密钥管理，不代表通话已被业务授权。

## 选择哪个KMS

用户恰有一个 Home KMS，可有多个 Migration KMS 和 External KMS。Home KMS提供本域密钥材料、迁移名单和外部证书；Migration KMS可为迁移域成员提供密钥。客户端不直接连接 External KMS，其证书由 Home KMS 提供。

依据：§5.3.1.1、§5.3.1.2、§5.3.1.3、§5.3.1.4。

## 经过HTTP代理

适用条件：通过 HTTP proxy 获取密钥；公共安全用途。

密钥内容须以 TrK 保护；请求包含 access token 和 TrK-ID，可含 InK-ID。若同一授权请求含 InK-ID，则用 InK 做完整性保护，否则用 TrK。TrK/InK及标识最初经带外分发；不能把经过TLS代理当作无需密钥内容保护。

依据：§5.3.2、§5.3.3。

## 直接连接KMS

适用条件：KMS 不使用 HTTP proxy。

KM client与KMS建立直接HTTPS连接，TrK/InK对内容的附加保护可选。请求类型仍与代理流程一致，不能因直连而取得对External KMS的直接访问权。

依据：§5.3.2、§5.3.3。

## 请求发给谁

适用条件：选择KMS请求及目的端。

KMSInit和KMSKeyProv可发给Home或Migration KMS；KMSCertCache请求与KRR上传只能发给Home KMS。初始化取得域参数，与取得特定身份/时间的密钥材料并非同一请求。

依据：§5.3.3。

## 证据边界

- 只核所列KMS角色、参考点和请求差异；Annex D XML、密钥轮换/撤销、TrK具体算法与完整KRR策略未核。
- 本主题不覆盖所有KMS请求，不能据此生成完整实现。

## 按需继续

- [access-transport](access-transport.md)
- [primary-registration](../identity/primary-registration.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，所列条款，印刷页 53、54、55、56、57；仅本版本，不声明与后续版本等同。
