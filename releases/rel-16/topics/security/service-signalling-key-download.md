# MCX 业务服务器下发信令密钥，收到哪个 200 才能开始用？

**服务器实际收到这台终端对本次密钥下载的成功应答后，才有这次流程给出的用钥依据。** 终端成功提取信令密钥后回 200；终端已发和业务服务器已收是两个观察点。这里的密钥是业务服务器下发的 CSK 或 MuSiK，用于保护信令。不是 KMS 供应的身份密钥材料，也不是 GMS 发的组主密钥（GMK）。[TS 33.180 V16.13.0，Release 16，§5.8.1，印 62](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=63)；[§5.8.2，图 5.8.2-1 及步骤 0–2，印 63](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=64)。

## 核对同一台终端的下载和应答

| 查到什么 | 能判断什么 |
| --- | --- |
| **准备：** KMS 已给终端配置该 MC 用户的身份材料；终端已在发起下载的 MCX 业务服务器注册。KMS 也给获准充当业务服务器的身份配置了材料。 | 图的步骤 0 写明，终端因此订阅该服务器的密钥下载通知。只见 IMS 注册或业务授权响应，不证明这笔下载已经发生。本节没有另规定具体订阅报文。 |
| **下载：** MCX 业务服务器给这台终端发带 MIKEY 载荷的 SIP NOTIFY 或 SIP MESSAGE。 | 本流程分发 MuSiK，或更新 CSK、MuSiK。载荷中的密钥针对接收的 MC 用户加密，用代表业务服务器的身份签名。发送不证明终端已成功提取。 |
| **成功应答：** 终端从本笔下载成功提取信令密钥并回 200；业务服务器实际收到匹配的 200。 | 服务器可以开始用**这笔下载的密钥**保护信令。不是立即必须换钥，也不证明某条出站消息已用新钥保护。 |

依据：[§5.8.1，印 62](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=63)；[§5.8.2，图 5.8.2-1 及步骤 0–2，印 63](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=64)。

例如，同一台终端先后收到两笔下载。服务器收到第一笔的 200，只能确认第一笔的成功应答，不能用它签认第二笔。别的终端的 200、REGISTER 或 PUBLISH 的 200 也不能替代。若只有终端发出第二笔应答的记录，服务器是否收到仍未证实。§5.8.2 没定义这时怎样重试、旧钥何时停用，或另一台终端何时用新钥。

## 看见 MIKEY，先分清是哪条路径

- **终端上送 CSK：** §5.4 的发送方是终端，接收方是 MCX 业务服务器。不是此处服务器发给终端的下载，不能套用上面的应答判据。§5.8.1 在这里说明分发 MuSiK 或更新 CSK/MuSiK，不判定其他程序能否由服务器初次下发 CSK。[§5.4，印 59](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=60)。
- **身份材料和组钥：** 若要确认 KMS 初始化或身份材料供应，查 [KMS 请求](kms-provisioning.md)；若要查新成员何时从 GMS 取得组记录和 GMK，或同一组的发送端选哪把已激活 GMK，查 [GMK 的成员和发送条件](../groups/gmk-member-add-and-send-selection.md)。它们的响应不能证明已完成上述下载。
- **MCPTT 专用 CSK：** 查参与功能（PF）是否另发 MESSAGE，要看它是否在授权用 REGISTER 或 PUBLISH 中实际收到 CSK，且已启用机密性保护。查终端核验和替换，看其实际收到的 SIP MESSAGE：`P-Asserted-Service` 含 MCPTT ICSI，正文有 `application/mikey`，其中 MIKEY 的 `CSB-ID` 内密钥标识是 CSK-ID。只在 `Accept-Contact` 看到 ICSI 不够，也不必先查出 PF 的更新原因。读 [MCPTT CSK 更新](../identity/shared-sip-registration.md)。
- **MCPTT MBMS MuSiK：** PF 打算用 MBMS 向这台终端发受机密性保护的话权信令时，要查 PF 是否收到这台终端对本笔下载的 200；确实没收到，才按专条对该终端和该钥针对的组改用单播话权。查终端时另看它实际收到的 SIP MESSAGE：`P-Asserted-Service` 含 MCPTT ICSI，`application/vnd.3gpp.mcptt-mbms-usage-info+xml` 含默认下载元素 `mbms-defaultMuSiK-download`（可含零个或多个组），或显式下载元素 `mbms-explicitMuSiK-download`（至少一个组）。只有 MIKEY 的 `CSB-ID` 内密钥标识是 MuSiK-ID，才查该 MIKEY 的 Status 分支；这不是判断默认/显式组范围或本笔是否有效的通用门槛。不必先查明 PF 的用钥意图。专用的 200 还可对应有效停用，并不证明已装入新钥。读 [MBMS MuSiK 下载](../media/mbms-musik-download.md)。
- **承载通告：** 若查的是 MCPTT 承载通告的 GPMS 安全材料，读 [MSCCK 的通告与接收](../bearers/mcptt-mbms-announcement-sdp.md)。§5.9 引用相同的安全分发程序，不等于把承载通告、MuSiK 下载和组媒体保护当成同一笔事务。[§5.9，印 63](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=64)。

[结构化条件与声明](service-signalling-key-download.json)。
