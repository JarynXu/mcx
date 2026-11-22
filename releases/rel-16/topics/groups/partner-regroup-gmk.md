# 跨域临时重组：谁生成 GMK，伙伴 GMS 怎样发给自己的成员？

把主侧的 A 组和伙伴侧的 B 组编成一个跨域 MCPTT 临时组 T 时，**主组管理服务器（主 GMS）为 T 新建 GMK 和 GMK-ID。伙伴 GMS 取得同一对 GMK 和 GMK-ID，再为本侧已归属用户重新封装**，不是另造一把 T 的组密钥，也不是把发给自己的加密载荷原样转给终端。这是 3GPP TS 33.180 V16.13.0 的 Rel-16 安全流程。开始前，MC 终端、主 GMS 和伙伴 GMS 都已按 §5.3 由 KMS 提供所需资料。[§7.3.3.3 引言、图 7.3.3.3-1、前提及步骤 6，印刷页 79（PDF 第 80 页）](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=80)；[步骤 11，印刷页 80](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=81)。

## 主 GMS 给伙伴，和两侧各自给成员，是三段分发

| 发给谁 | 谁加密、用谁的身份签名 |
| --- | --- |
| **主 GMS → 伙伴 GMS** | 主 GMS 在重组通知中加入 Group Key Transport 载荷，把伙伴 GMS 当作组内接收者。用伙伴 GMS 的身份加密新 GMK，使用主 GMS 自己的身份签名。主 GMS 从伙伴 GMS 的 URI 生成 User Salt，再用该 Salt 派生这一份的 GUK-ID。[步骤 7–8，印刷页 79](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=80)。 |
| **伙伴 GMS → 本域已归属用户** | 伙伴 GMS 从通知取出 T 的 GMK 和 GMK-ID。它按本域每名已归属用户的身份对这把 GMK 重新加密，为每位用户生成新的 GUK-ID，以伙伴 GMS 自己的身份签名。换的是给各收件人的封装和 GUK-ID，不是 T 的组密钥。[步骤 11，印刷页 80（PDF 第 81 页）](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=81)。 |
| **主 GMS → 本域已归属用户** | 主 GMS 另通知本域已归属用户。它在 Group Key Transport 载荷中放入 GMK 和 GUK-ID，用该 MC 用户的身份加密 GMK，以主 GMS 自己的身份签名。不需要绕经伙伴 GMS。[步骤 14，印刷页 80](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=81)。 |

看记录时，先分清比较的是 **T 的 GMK-ID** 还是 **某份封装的 GUK-ID**。主、伙伴 GMS 与成员间的 GUK-ID 不要求相同，也不能把两个 GUK-ID 不同当成伙伴换了组密钥。两侧用户分发是各自的路径，本节未用一侧的终端安装结果作为另一侧发送的前提。

## 选的 KMS 不获接受，需要重来吗？

主 GMS 发给伙伴 GMS 的重组通知中，MIKEY 消息里的发起方 KMS（`IDRkmsi`）或接收方 KMS（`IDRkmsr`）不获接受时，**可能**有 KMS Redirect Response 返回主 GMS，提供 KMS 信息。收到该响应的主 GMS **可以**重新尝试前面的过程。这里既未规定每次都返回，也未要求收到后必须重试；不规定如何选替代 KMS 或重试几次。[§7.3.3.3 注 1，印刷页 80](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=81)。通用 KRR 规则见[推荐 KMS 不获接受时怎样读 KRR](../identity/kms-redirect-response.md)。

## 伙伴由 MC 安全网关代表，要向谁说明？

若有伙伴 GMS 由 MC Security Gateway 代表，该伙伴 GMS 的 KMS 证书属性 `IsSecurityGateway` 为 `true`。原文将这种代表情形与完整的端到端安全区分开。在这种情况下，**主 GMS 须向所有组用户及本次重组的所有伙伴 GMS 标明 GMK 与安全网关共享**。设置 GMK 密钥参数的 `Status` 字段中的 `Security Gateway` 位，就是这一告知。仅知 GMK 经加密和签名分发，不能断言任一跨域临时组一定具备完整的端到端安全。该位也不是收到、解密或安装 GMK 的回执。[§7.3.3.3 末段，印刷页 80](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=81)。

组建通知和成员回执的业务字段见[跨系统临时重组](partner-system-regroup.md)。两份规范的步骤号各读各的，不能从 Stage 2 回执认定终端已解密、安装密钥或开始用它保护媒体。已从组里移出的成员如何处置本地 GMK，另见[成员移出后的 GMK 处理](removed-member-gmk.md)。
