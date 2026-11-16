# 刷新 access token：不能借刷新扩大授权

TS33.180 V19.4.0 Annex B.5 的授权码客户端刷新路径；客户端已取得可用refresh token。

## 先检查 grant 类型

B.5.1将refresh token限定为authorization-code grant客户端，不发给implicit grant客户端；此处只描述该刷新路径，不将该句提升为所有伙伴交换的绝对限制。刷新可减少access token过期后的重新登录，并不保证永远免登录。

依据：§B.5.1。

## 刷新请求仍有范围和认证条件

适用条件：向IdMS token endpoint刷新。

grant_type为refresh_token，请求scope只能等于或小于原授权请求范围。如果IdMS发放过client credentials，客户端须用登记时建立的凭据向token endpoint认证。

依据：§B.5.2。

## 新 refresh token 并非必返

适用条件：刷新响应。

响应提供access token，可另发refresh token；不能假设每次刷新均轮换refresh token。

依据：§B.5.3。

## 证据边界

- 这里只核grant、scope与响应的基本边界；未覆盖完整撤销、轮换存储、失败恢复或账户失效处理。

B.7.4–B.7.5的伙伴jwt-bearer交换另列可选refresh token，与B.5.1概括存在范围张力；不可据本页否定伙伴响应字段。

## 按需继续

- [native-authentication](native-authentication.md)
- [service-authorization](service-authorization.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，所列条款，印刷页 132、133、134；仅本版本，不声明与后续版本等同。

- [伙伴域令牌交换](partner-token-exchange.md)

- [UE密钥保存与清理](../security/ue-key-lifecycle.md)
