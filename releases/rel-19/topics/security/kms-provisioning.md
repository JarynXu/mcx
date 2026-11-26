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

- 核所列 KMS 角色、参考点、请求差异和应答证据；Annex D 只核本页所列应答结构，未核完整 XML、密钥轮换/撤销过程、TrK 具体算法与完整 KRR 策略。
- 本主题不覆盖所有KMS请求，不能据此生成完整实现。

## 按需继续

- [access-transport](access-transport.md)
- [primary-registration](../identity/primary-registration.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，所列条款，印刷页 53、54、55、56、57；仅本版本，不声明与后续版本等同。

- [组密钥下发校验](group-key-distribution.md)

## 怎样判断这次 KMS 应答有没有给用户密钥

**先看这次实际回了什么。** 本节只讲 Release 19、TS 33.180 V19.4.0 的 KM client 向 Home 或 Migration KMS 取得身份密钥。查规范可以按题目给定的角色和请求读；判断某次下发，要核对实际应答与请求是否对应、正文能否核验，以及本例适用的保护条件。HTTP 成功只说明 HTTP 层成功。匹配的 `KmsKeyProv` 正文可以包含零个或多个 `KmsKeySet`。完整、可核验的正文中确实为零，只表示这次没有带用户密钥集；只有状态码、日志不全或正文尚不能核验时，密钥集数量未知。零套不等于规范指定了失败码、重试动作，或终端没有以前取得的密钥。[§5.3.4，印刷页 58](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=59)；[D.3.5.1，印刷页 157，`KmsKeyProvType`](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=158)。

**域证书和保护更新不是用户密钥。** 初始化应答提供本 KMS 的证书；证书缓存或单证书应答实际返回的证书属于域材料；所请求的单证书不可用时 Annex D 另列错误，KMS Lookup 提供 KMS 标识信息、不返回密钥材料。域证书里的公共参数不是用户的签名私钥或解密私钥。`KmsKeyProv` 可能带更新的 TrK；响应说明和 XML 扩展还允许独立的 InK 更新。即使收到这些候选更新，若没有实际 `KmsKeySet`，仍不能说得到了用户密钥，也不据此断定更新已经安装。直连、代理和跨域信任仍按各自条件判断。[§5.3.3，印刷页 57](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=58)；[§§5.3.4–5，印刷页 58](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=59)；[D.3.1，印刷页 148](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=149)；[D.3.5.1，印刷页 159，`KmsKeyProvTkIkType`](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=160)。

**有密钥集，再看它属于谁和哪个周期。** 用实际 `KmsKeySet` 的 `KmsUri`、`UserUri`/`UserID` 和 `KeyPeriodNo` 核对签发 KMS、用户 URI/UID 和所问周期。它提供 RSK（用户解密私钥）、SSK（用户签名私钥）和 PVT（公开验证令牌，不是私钥）。`CertUri`、`ValidFrom`、`ValidTo`、`Revoked` 都是可选字段；缺失不替代有效性或撤销检查，也不推定永久有效。外层 `KmsResponse` 的 `UserUri` 是应答对象，`KmsUri` 是应答发送者，`Time` 是应答发送时间，`ClientReqUrl` 标示请求的资源。不能拿这些外层字段替代密钥集的签发方、用户和周期。一份应答包含多套时，只把匹配的材料归给该身份和周期。[§5.3.6，印刷页 59](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=60)；[表 D.3.1‑1，印刷页 148](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=149)；[表 D.3.3.2‑1，印刷页 150](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=151)。

XML 另有 `KmsError` 表示错误。可核验的实际错误正文与 HTTP 状态分别记录；这里没有建立二者的固定映射，也不推定字段共现的含义、缺项时的错误或重试。[D.3.5.1：`KmsResponseType`，印刷页 156](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=157)及[印刷页 157](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf#page=158)。

取得材料与实际保存、启用或获准通信是不同证据。D.3.3.2 的注说明旧周期的材料有可能用于解密加密给该用户的旧消息，不能据这条注推定旧周期密钥可用于新消息，也不能据此要求永久保留。只问重启与换人时怎么保存，读 [UE 密钥生命周期](ue-key-lifecycle.md)；已进入在网私呼并要判断 PCK 生成、分发或后续信令，读 [私呼密钥分发](private-key-distribution.md)。KMS 的身份密钥集不是那次呼叫的 PCK，不能凭服务器回包或字段匹配就证明客户端已收到、验收、保存或启用密钥，也不证明业务授权、接听、媒体活动或端到端成功。
