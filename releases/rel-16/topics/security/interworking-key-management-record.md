# 同一用户用两台互通终端，KMS 怎样选择 InterKMRec？

先用已通过验证的访问令牌中的 MC 业务 ID 找关联记录。同一个业务 ID 有多份记录时，再查请求终端是否已有与某份记录的 Secondary InterKMRec ID 的关联。若匹配不到，KMS 才按这条规则另选一份并建立关联。这里是 3GPP TS 33.180 V16.13.0（Release 16）[§11.2.3，印刷页 118–119](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=119) 的互通密钥管理，不是终端每次登录都要分一份新记录。

## InterSD 是消息，InterKMRec 是终端可用的初始参数

互通密钥归属非 3GPP 系统时，两侧借 InterSD 消息传送互通安全数据，IWF 或互通 MC 终端均可生成这类消息。InterSD 须能承载非 3GPP 安全数据，不依赖对端载荷格式或 IWF 之后的系统架构；本规范不定义载荷内容。InterSD 可以另受信令保护。为安全交换这类消息，互通 MC 终端**可能需要** InterKMRec，例如用其中的寻址或标识参数。[§11.2.2 及 §11.2.3 开头，印刷页 118](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=119)。

## 两级标识让 KMS 区分同一业务用户的不同客户端

| 图 11.2.3-1 的字段 | 出现及编码 | 用途 |
| --- | --- | --- |
| Primary InterKMRec ID | 必有，TLV，长度可变 | 与 MC 业务 ID 关联。 |
| Secondary InterKMRec ID | 必有，TLV，长度可变 | 区分同一业务 ID 使用的不同 MC 客户端。 |
| InterKMRec Payload | 必有，LV-E，长度可变 | 互通密钥管理参数；其内部格式与内容由非 3GPP 系统定义。 |

“必有”说的是**已经提供的一份记录**。不表示所有互通终端都需要记录，也不表示 Primary ID 必须等于 MCPTT ID，或 Secondary ID 的值就是客户端 ID。[图 11.2.3-1 及图后说明，印刷页 118](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=119)。

互通 MC 用户办理密钥管理授权时，KMS 在验证访问令牌后，检查令牌中的 MC 业务 ID 是否有关联记录。记录存在且与请求的 MC 业务 ID 关联时，KMS 须在此次密钥管理授权中向该互通 MC 终端提供记录。同一业务 ID 有多份时，KMS 先查客户端与 Secondary ID 的已有关联；匹配不到时，必须从这些记录中选一份，将请求端的客户端 ID 与其 Secondary ID 关联。只有一份时，不套用这里的多份匹配分支。没有关联记录时，所引条款未规定替代记录或错误码。记录怎样录入 KMS、如何实现关联，以及何时或怎样解除关联，也不在本节范围内。[§5.1.3.1 密钥管理授权段，印刷页 31](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=32)；[§11.2.3 图后范围、选取和交付段，印刷页 118–119](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=120)。

## 保护的是 KMS 交给终端的这份记录

MC 系统要求对这份记录加密时，KMS 须用互通 MC 终端的 TrK 保护传给该终端的 InterKMRec。签名是可选的；如果签名，有 InK 就须用 InK，没有 InK 才用 TrK。这个条件只说明怎样保护这份记录；不能凭记录已下发断定 InterSD 已发出、被非 3GPP 一侧接受，或已经安装互通密钥。[§11.2.3 末段，印刷页 119](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=120)。

若要查[通用 KMS 取密钥或证书的流程](kms-provisioning.md)，看请求与响应类型。若抓到的是[SIP 上的 MC 业务授权](../identity/mcx-sip-service-authorization.md)，不要据此认定 KMS 已发记录。若要查的是[IWF 与 GMS 交换组配置时的字段](../groups/iwf-group-configuration-message-fields.md)，按组配置流程核对，不把该流程的组级密钥材料当成发给某台终端的 InterKMRec。
