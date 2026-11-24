# KMS 用户密钥换周期：同一个 MC 业务 ID 怎样对上 UID 和密钥集？

MC 业务 ID 可以不变。用于 MIKEY-SAKKE 的 UID 要按业务 ID、KMS 和密钥周期计算，不能把上个周期的 UID 当成本周期的结果。检查 `KmsKeySet` 时，先分清 `UserUri`、`UserID` 和 `KeyPeriodNo`。它们分别标出用户的 URI、这个密钥集对应的 UID 和周期号。以下依据 3GPP TS 33.180 V16.13.0（Release 16）[§5.3.5 末段，印刷页 58](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=59)和[附录 D.3.3.2 表 D.3.3.2-1，印刷页 148](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=149)。

## 用哪张证书、哪个时间算周期？

取需要计算 UID 的用户所对应的 KMS 证书。附录 D 将 UID 格式字段列作 `UserIDFormat`，其值须为 `2`，表示按 F.2.1 生成；附录 D.3.5.1 的 XML 元素写作 `UserIdFormat`。这两处写法指向同一个格式值，不是两个字段。[表 D.3.2.2-1 与 D.3.2.3，印刷页 147–148](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=148)；[D.3.5.1 的证书 schema，印刷页 155–156](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=156)。

证书中的 `UserKeyPeriod` 是周期长度（秒，记为 `P3`），`UserKeyOffset` 是第一周期起点相对 1900 年 1 月 1 日 00:00 的偏移（秒，记为 `P4`）。`P4` 必须小于 `P3`。用同一起点计秒的 NTP 时间 `TIME`，周期号 `P5` 可按 `floor((TIME - P4) / P3)` 计算。到了 `P4 + n × P3` 就进入第 `n` 个周期，不按自然月划界。F.2.1.1 的注 2、注 3 说明，在 MIKEY 中通常用载荷内的 NTP 时间；区分加密所用的收方标识和签名所用的发方标识。[F.2.1.1、注 2–3，印刷页 171–172](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=172)。

计算 UID 时，F.2.1.1 的输入顺序是 `FC || P0 || L0 || … || P5 || L5`，每项参数后跟自身的字节长度。`FC` 为 `0x00`，`P0` 为固定字符串 `MIKEY-SAKKE-UID`，其余参数依次是业务用户标识、KMS 标识、周期长度、偏移和周期号。条款回指 TS 33.220 §B.2 的输入编码，不调用该节的 KDF；这里计算 SHA-256，使用完整 256 位结果并做 Base64 编码。`UserKeyPeriod`、`UserKeyOffset`、`KeyPeriodNo` 在 XML schema 里是整数项；XML 的数字文本不能直接当作散列输入。F.2.1.2 例中的秒数和整数字节长度只用于核对该例，不是部署默认值。[F.2.1.1、注 1，印刷页 171–172](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=172)；[F.2.1.2 的示例编码，印刷页 172–173](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=173)；[D.3.5.1 的两个 schema，印刷页 155–156](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=156)。

## 收到密钥集后，哪些字段要对上？

`KmsUri` 标出签发这份 `KmsKeySet` 的 KMS，`UserUri` 标出用户的 URI，`UserID` 是这份密钥集对应的 Base64 UID，`KeyPeriodNo` 是密钥的周期号。核对是否为本次所需的密钥集时，不能只比 `UserUri`。解密用 `UserDecryptKey`（SAKKE RSK）；签名用 `UserSigningKeySSK`（ECCSI 私钥），`UserPubTokenPVT` 是 ECCSI 的公开验证令牌。含有这些字段不证明客户端已安装密钥或能完成通信。[§5.3.6，印刷页 59](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=60)；[D.3.3.1 与表 D.3.3.2-1，印刷页 148](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=149)。

`CertUri`、`Issuer`、`ValidFrom`、`ValidTo` 和 `Revoked` 在证书与密钥集各自的表和 schema 中都是可选项。证书的 `CertUri` 标记证书本身；密钥集的 `CertUri` 指向可用于验证该集的证书。哪一份对象带了有效期或撤销信息，就按那一份对象理解。字段没出现，不能补出有效期或据此认定未撤销；`KeyPeriodNo` 也不能代替证书或密钥集的有效期。[表 D.3.2.2-1，印刷页 147](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=148)；[表 D.3.3.2-1，印刷页 148](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=149)；[D.3.5.1，印刷页 155–156](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=156)。

周期结束后，D.3.3.2 的注说旧密钥**可能**在定义的使用周期之外仍有效，以便解密以前发给该用户的消息。这不是继续用旧密钥签名的授权，也不规定必须保留旧密钥多久。它没有给出字段缺失时的接收决策、撤销处理或取新材料的周期。[D.3.3.2 表后注，印刷页 148](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=149)。

要查[怎样请求材料、响应可返回几份密钥集](kms-provisioning.md)，读供应流程。若问题是[归属、迁移和外部 KMS 的职责](kms-domain-roles.md)、[更新的是 KMS 根证书](kms-root-certificate.md)或[重启、退出等事件后的材料保留和删除](../identity/ue-key-persistence.md)，分别按对应规则判断。
