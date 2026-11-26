# MCS 在网初始配置的 TLS 双向认证报 409：凭据漏配，还是两种都配了？

TS 24.484 V20.1.0，Release 20。这里核 MCS UE 初始配置文档中在网 `App-Server-Info` 的 TLS 隧道认证设置，不是核一次 TLS 握手。

**双向认证为 `true` 时，证书和预共享密钥两种凭据恰好要有一种。** 两种都没有或同时出现，配置管理服务器（CMS）都须返回 HTTP 409，带 XCAP `constraint-failure`。可用下面两条诊断区分；即使 HTTP 状态和 XCAP 错误元素都相同，也不能只凭它们判定是哪一条。（§7.2.2.6）

| 已确认的设置 | 这两条校验怎样处理 |
| --- | --- |
| 双向认证为 `true`，无 `x509`、无 `key` | HTTP 409 + `constraint-failure`。若含 `phrase`，宜填 `mutual authentication enabled without a X.509 certificate or pre-shared key`。 |
| 双向认证为 `true`，`x509` 与 `key` 都有 | 同为 HTTP 409 + `constraint-failure`。若含 `phrase`，宜填 `mutual authentication enabled with both a X.509 certificate and a pre-shared key`。 |
| 双向认证为 `true`，只有其中一种 | 不触发这两个组合错误。仍须符合 XML Schema 和其他校验；这不能证明配置获接受、凭据有效或实际握手成功。 |
| 已知开关为 `false` | 不满足这两条的 `true` 前提；不能推出其余校验会通过。若方法块存在却未给开关，须另看 Schema 所要求的布尔字段，不能当作 `false`。 |

这两条看元素有无，不检验证书或密钥是否有效。`phrase` 可省略。若还命中 KMS URI 不合语法等其他 409 条件，这两条不规定先报哪一个。

## 核原文时，分开规则和 XML 层级

- **结构与 Schema：** 在网 `App-Server-Info` 必须包含 `tls-tunnel-auth-method`。§7.2.2.1 项 3(g) 和 §7.2.2.3 的 `AuthMethodType` 把必需的布尔字段 `mutual-authentication`、可选 `x509`、可选 `key` 都放在 `tls-tunnel-auth-method` 之下。已确认整个方法块或布尔字段缺失，是结构问题，不等于布尔值明确为 `false`。这两条组合校验未为缺项另定 HTTP 状态。Schema 把两种凭据各自列为可选，不能仅看可选性就断言启用时可都省略或同时配置。
- **校验与语义的写法：** §7.2.2.6 两条校验写成 `mutual-authentication-element` 里的 `tls-tunnel-auth-method` 为 `true`；§7.2.2.7 项 4(g) 又写成 `tls-tunnel-auth-method` 包含 `mutual-authentication-element`。名称和包含方向不完全一致。这三处各按原文定位，不据此判定实际实现采用哪种 XML 层级，或把一种布尔拼法当线上唯一格式。
- **字段含义和引用：** §7.2.2.7 项 4(g) 说 `true` 表示 TLS 隧道使用双向认证；`x509` 载 X.509 证书，`key` 载预共享密钥。同段把开关引向 TS 24.483 §8.2.44B 的 `Mutual`，证书引向 §8.2.44C 的 `X509`，但把 `key` 引向 §8.2.44D 时原文也写 `X509`。这里只核引用，没有核目标正文或据此改字段名、密钥格式或实际认证行为。

另查：[共同初始配置模板与终端 XCAP 地址](initial-ue-config-xcap.md) · [默认用户档引用的独立 409 条件](default-profile-reference-xcap.md)

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip)
