# 伙伴域令牌：换取对象、受众与迁移授权

TS33.180 V19.4.0；主系统用户已获得服务授权。

涉及同一MC系统内伙伴域的组时，主域服务授权已完成且用户配置指明该伙伴域组成员关系；迁移另走相应分支。不把普通服务器间互通等同于此客户端流程。

## 前提

适用条件：客户端需要伙伴域授权。

客户端先在伙伴IdMS注册；伙伴IdMS通过带外配置取得主IdMS签名证书。UE直接通过HTTPS访问伙伴IdMS。

依据：§5.1.4.2；B.6。

## 交换对象

适用条件：面向一个指定伙伴IdMS。

主域access token作为subject_token送主IdMS，取得面向伙伴的security token（响应字段仍名为access_token）。客户端将该security token作为assertion，以JWT bearer grant送伙伴IdMS，伙伴IdMS验证security token后签发伙伴access token；这些对象不能与ID token互换。

依据：§B.7.2–B.7.5。

## 每个伙伴分别指定受众

适用条件：请求伙伴域security token。

resource指定伙伴token endpoint；security token的aud包含客户端client_id及与resource相同的目标IdMS。每个伙伴分别换取security token并重复交换，不将一个伙伴令牌当成所有伙伴通行证。

依据：§B.7.2；B.8表B.8-1；B.7.1；5.1.4.2。

## 令牌之后仍有授权

适用条件：取得伙伴access token后。

同系统伙伴域按§5.1.3继续服务授权；迁移场景先完成§5.1.5迁移授权，再执行正常服务授权。图5.1.5-2的初始请求提供伙伴access token并校验；其后步骤3–11不再要求或提供该令牌。

依据：§5.1.4.2；5.1.5。

## 证据边界

- 仅所列MC profile；未提供RFC/OIDC完整校验、aud序列化或通用OAuth实现。
- B.7.4示例2的scope使用逗号，与正文空格分隔规则不一致；按正文识别规则，不复制示例为实现。B.5.1与B.7.5刷新边界见令牌刷新主题。

## 按需继续

- [native-authentication](native-authentication.md)
- [service-authorization](service-authorization.md)
- [token-refresh](token-refresh.md)
- [migration-authorization](migration-authorization.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页 35–38、134–139；仅本版本。

## 跨规范使用前

[令牌响应义务差异](token-response-obligations.md)列出 TS24.482 V19.0.0 与本页安全规范版本的不同措辞。不要把 ID/refresh 字段必选性静默统一。
