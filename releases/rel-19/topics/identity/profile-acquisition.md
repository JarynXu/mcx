# 取得用户配置：主系统与迁移伙伴系统

TS23.280 V19.9.0 Stage2；本页讨论MC service user profile，不是组配置或密钥文档。

## 主系统按用户ID取得配置

适用条件：用户已在IdMS认证，UE能安全访问CMS。

配置管理客户端携带MC service ID请求CMS取得用户配置。需要下载时，响应包括与该ID关联的全部用户配置；不能把该过程限制为仅下载当前活动配置。

依据：§10.1.4.3.1。

## 伙伴系统获取需要迁移前提

适用条件：双方已配置迁移许可，用户已在伙伴系统认证并取得配置获取和服务授权请求所需凭据，UE已知伙伴CMS地址。

客户端向伙伴CMS请求迁移配置，伙伴CMS再向主系统CMS请求。主系统依据目标伙伴系统身份选择迁移配置；伙伴系统按本地配置信息修改并保存，不能假设直接复制主系统当前配置。

依据：§10.1.4.3.2 preconditions and steps 1–5。

## 验证是有条件的过程，失败则不下发

适用条件：伙伴系统处理迁移用户配置。

主系统可请求验证修改后的配置；若提出请求，原文仍使用may描述伙伴CMS回传修改后配置。发生验证且失败时，不执行向UE下发配置的步骤9。本条不把may改为强制，也不据此发明未回传时的超时、放行或拒绝规则。

依据：§10.1.4.3.2 steps 4–9。

## 证据边界

- 配置取得不等于已完成伙伴服务授权。
- 未核对Stage3编码、缓存校验、失败重试及具体服务配置字段。

## 按需继续

- [profile-selection](profile-selection.md)
- [service-authorization](service-authorization.md)
- [migration-authorization](migration-authorization.md)

[ETSI官方TS23.280 V19.9.0](https://www.etsi.org/deliver/etsi_ts/123200_123299/123280/19.09.00_60/ts_123280v190900p.pdf)，印刷页88、89、90、91、92；仅本版本。
