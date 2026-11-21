# 普通私呼与首接应答：PCK 在哪份 SDP，验签失败为何是 488 或 BYE？

普通按需私呼的 PCK（保护本次私呼语音的密钥）由**主叫客户端**准备，密钥消息在初始 INVITE 的 SDP offer。首接应答呼叫的 PCK 则由**被叫客户端**准备，密钥消息在应答的 SDP answer。两者都以需要建立端到端安全为前提。抓包时先认呼叫类型和收到的那份 SDP，再判断哪个客户端要验证，不能把 SIP 主叫固定当成密钥消息的发起者。

范围：Release 16、Stage 3，TS 24.379 V16.14.0；普通在网按需 MCPTT 语音、带话权控制。不扩到预建立会话、紧急状态、密钥算法、信令 CSK 或 SPK 的更新。

## 按呼叫类型找密钥消息

| 场景 | 谁准备 PCK 和 PCK-ID | 查哪份 SDP |
| --- | --- | --- |
| `private`：普通私呼，需要建立端到端安全上下文 | 主叫客户端给受邀用户准备，用封装后的 PCK 和 PCK-ID 构成 MIKEY-SAKKE I_MESSAGE；消息发起者身份 IDRi 填主叫的 MCPTT ID。 | 初始 INVITE 的 **SDP offer**。在要求端到端安全的普通按需私呼中，查 `a=key-mgmt` 的 `mikey` 值，不是 SIP 头，也不是明文 PCK。[§11.1.1.2.1.1 第 11–12 项，印刷页 353–354](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=354)；[§6.2.1 第 4 项，页 57](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=58)。 |
| `first-to-answer`：首接应答，需要建立端到端安全上下文 | 收到邀请的**被叫客户端**给主叫准备，用自己的 MCPTT ID 填 I_MESSAGE 的 IDRi。它是密钥消息的发起者，却不是 SIP INVITE 的主叫。 | 在要求端到端安全的首接应答呼叫中，实际接受时查 200 的 **SDP answer** 里的 `a=key-mgmt`，同样是 `mikey` 值。准备密钥不等于已接受或已被选中。[§11.1.1.2.1.2 第 5 项及注 4，页 357](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=358)；[§6.2.2 第 5 项、§6.2.3.1.1 第 7–8 项、§6.2.3.2.1，页 58–59](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=59)。 |

两种准备都用密钥管理材料。规范让相应**客户端**生成这次的 PCK，不是让参与功能、控制功能或密钥管理服务器作为这次 I_MESSAGE 的发起者。排查时对准实际收到的 offer 或 answer，核对其中的消息发起者身份与该端验证结果，不用日志里的 SIP 主被叫角色替代 IDRi。

## 验证失败时，这边收到的是请求还是响应？

**被叫收到初始 INVITE，offer 带 MIKEY-SAKKE I_MESSAGE。** 被叫从消息取 MCPTT 身份，转为 UID 后校验签名。认证失败，须**对该 INVITE 回 488**，Warning 文本编号为 136。成功校验才继续解封并取得 PCK 和 PCK-ID，不等于用户已接听。136 是 Warning 文本中的业务编号，不是 SIP 状态，也不是 Warning 外层码。只见 488 不能认定验签失败：控制功能判定媒体不合要求也可出现 488。固定版该过程的 Warning 文字用 `MIKEY-SAKE`，Warning 文本表的 136 行用 `MIKEY-SAKKE`；排查时保留本次的方法、状态、编号和原始文字，不把拼写差异当成另一种认证机制。[§11.1.1.2.1.2 第 4 项，页 357](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=358)；[§4.4.1–2，页 33–34](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[表 4.4.2-2 第 136 项，页 37](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=38)；[§11.1.1.4.2 第 5 项，页 380](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=381)。

**主叫实际收到自己的首接应答 INVITE 的 200，answer 带 MIKEY-SAKKE I_MESSAGE。** 这次验证的是 answer 的消息，不是回查主叫发出的 offer。主叫取发应答端的 MCPTT ID，转 UID 后验签；验证成功才解封并取 PCK-ID。认证失败须**另发 BYE 释放会话**，并跳过本条余项，而不是向 200 再回一个 488。BYE 的 `application/vnd.3gpp.mcptt-info+xml` 正文，`release-reason` 按本版写为 `authentication of the MIKEY-SAKE I_MESSAGE failed`，不带 136。若控制功能实际收到带匹配原因的发起侧 BYE，再走指定的私呼释放程序。仅据 BYE 不能推定网络自动改选另一个被叫。[§11.1.1.2.1.1 收到 200 后第 2 项，页 355](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=356)；[§F.1.2 的枚举，页 546](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=547)；[§11.1.1.4.2 末段，页 383](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=384)；[§11.1.3.3.1，页 389](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=390)。

**只看到 200，还不知道密钥结果。** 首接应答的上述主叫验证分支以实收 answer 带指定 I_MESSAGE 为条件；没看到该消息，不可据此宣布验签成功，也不直接套用这个认证失败 BYE。普通 `private` 还有另一个分支：控制功能收到带 `P-Answer-State: Unconfirmed` 的 183，支持媒体缓冲且还未向发起侧发送最终响应时，需向发起侧发带 `Unconfirmed` 的 200。它不是首接应答选人，也不是被叫完成受话、验签或媒体保护的证据。即使两端成功共享 PCK，规范也只说明它们**能够**用 SRTP/SRTCP 建安全会话；实际媒体是否成功受保护并抵达，要另查同一场的媒体证据。[§11.1.1.4.2，页 381–382](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=382)；[§11.1.1.2.1.1 第 2 项及注 4，页 355](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=356)。

若要核对普通私呼是自动还是人工应答，见[被叫应答取证](private-client-answer-evidence.md)。若要判断首接应答候选如何被选中或被撤下，见[首接应答控制功能](first-to-answer-controlling.md)。若已有 BYE，要查哪一腿结束，见[普通按需私呼的释放信令](private-client-release.md)。

来源：[3GPP TS 24.379 V16.14.0 / ETSI TS 124 379 V16.14.0，Release 16](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf)。
