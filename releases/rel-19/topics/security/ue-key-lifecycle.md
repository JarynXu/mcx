# UE密钥生命周期：保存、换用户与失效清理

TS33.180 V19.4.0 §5.11；区分静态/半静态材料和业务动态密钥。

## 闲置材料也需要保护

适用条件：材料未在使用。

长期密钥与私有证书、CSK/GMK/MuSiK、基于身份的密钥材料及ID/access/refresh/security token必须受保护存储；本条不指定保护实现。

依据：§5.11.1。

## 重启保存与换用户隔离

适用条件：静态或半静态材料跨UE开关机、同一用户退出再登录。

CSK、GMK、TrK、InK、TLS/IPsec私有证书、KMS Key Set及ID/access/refresh/security token等静态或半静态材料必须安全保存，并跨这些转换维持。若随后登录的是另一用户，前用户材料必须安全删除或安全分区；保留材料仅允许其所属用户访问。不能将同一用户重启一概当成全部删钥。

依据：§5.11.2 paragraphs 1–2。

## 动态密钥有独立删除触发

适用条件：MKFC、MSCCK、PCK及其派生动态密钥。

应按业务需要安全存储（SHOULD）；不再需要时必须安全删除（SHALL）。UE关机、当前用户退出、关联access token因技术或认证原因到期，以及业务需要规定的时点，都触发相应动态密钥删除。

依据：§5.11.1；5.11.2 paragraph 3。

## 无法刷新引起的额外清理

适用条件：access token到期，且IdMS因技术或认证原因不能或不愿刷新。

UE必须安全删除CSK、GMK、MuSiK、MKFC、MSCCK、KFC、DPPK、PCK及access/refresh/security token。此明确清单不能推广成普通到期就删除一切，也不因未列TrK、InK、KMS Key Set、证书和ID token而推定它们可永久保留。

依据：§5.11.2 paragraph 4。

## 证据边界

- 不规定安全分区、密钥擦除实现或刷新失败重试阈值。
- 本页保留原文DPPK标识；不擅自替换为其他派生密钥缩写。成员变化的条件删除仍见独立主题。

## 按需继续

- [group-key-membership](group-key-membership.md)
- [kms-provisioning](kms-provisioning.md)
- [../identity/token-refresh](../identity/token-refresh.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页 64–65；仅本版本。

保存不等于仍可使用：§9.2.1.2把SIP会话拆除、用户退出等列为CSK停止使用条件。不能据存储保留继续使用旧CSK。参见[信令密钥更新](signalling-key-update.md)。
