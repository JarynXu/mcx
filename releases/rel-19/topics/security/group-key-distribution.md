# 组密钥下发：收到GMK之前要验证什么

TS33.180 V19.4.0 §5.7；GMS和各客户端已按§5.3配置身份密钥。

## 下发材料

适用条件：GMS向组用户下发GMK。

GMK按用户身份封装并由GMS签名；采用端点多样性。组配置通知带GMK、GUK-ID及GMK-ID相关材料，关联参数由GMK加密。

依据：§5.7.1；5.7.2。

## 接收校验

适用条件：客户端接收下发通知。

验证签名，提取GMK、GUK-ID、GMK-ID并检查GMK-ID不与已有项重复；解密组标识、激活时间和文本；根据用户配置中的Group ID确认GMS URI对应关系。任何检查失败均返回错误，成功才保存密钥和参数并响应。

依据：§5.7.2 step 2。

## KMS不匹配

适用条件：接收方不接受所用KMS。

可通过KMS Redirect Response要求重试；这不保证重试成功，也不能绕过签名和组配置校验。

依据：§5.7.2 steps 1a–2。

## 安全网关边界

适用条件：组有成员由Security Gateway代表。

GMS需标示GMK与Security Gateway共享；接收该标志的发起客户端应警告用户，不能宣称媒体只对终端可见。

依据：§5.7.1；5.7.2。

## 证据边界

- 不提供完整MIKEY编码、错误码映射或KRR算法。§5.7.1引用E.3存在与GMK格式E.2的交叉引用差异，不据此生成报文。
- 取得GMK不能证明归属、入呼或话权已经获准。

## 按需继续

- [kms-provisioning](kms-provisioning.md)
- [group-key-membership](group-key-membership.md)
- [private-key-distribution](private-key-distribution.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页 60–62；仅本版本。

- [组媒体与控制保护](group-media-control.md)

- [kms-redirection](kms-redirection.md)
