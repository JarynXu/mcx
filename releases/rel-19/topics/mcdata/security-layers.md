# MCData保护层次：DPPK不是一种新密钥

TS33.180 V19.4.0 §8；区分MCData信令参数、Data signalling payload和真正的用户Data payload。

## 先确认保护的内容和链路

适用条件：选择MCData Payload Protection Key（DPPK）。

DPPK是既有密钥在MCData保护中的用途名称，不是一把新类型的通用密钥。在网客户端—服务器单播信令用CSK，组播下行信令用MuSiK，服务器间信令用SPK；不能因此推导用户数据也用服务器信令密钥。

依据：§8.1；8.2。

## 端到端用户数据按私有或组通信选钥

适用条件：对SDS/FD用户数据启用端到端保护。

两客户端通信使用PCK，组通信使用GMS下发的GMK；HTTP文件也可在上传前受到端到端保护。§8.3/8.4明确服务方要求时应实施payload保护，不能只靠概述中的保护描述断言每份MCData都已加密。组流程另有用户归属该组的前提。

依据：§8.2；8.3；8.4。

## SDS和FD可以复用同一对端PCK

适用条件：源和目的之间已经建立PCK。

同一源和目的的后续SDS/FD交换可以继续使用该PCK，并在每个SDS消息中提供PCK-ID。此处是允许复用，不是跨任意对端共享，也不覆盖失效或撤销后的无限复用。

依据：§8.3。

## 加密完整性与发起者认证分开判断

适用条件：处理protected或authenticated payload。

protected payload需收发方共享DPPK及标识，经KDF生成DPCK后进行加密和完整性保护；authenticated payload另需KMS配置的SSK、PVT和KPAK。规范区分仅protected、仅authenticated及两者同时的payload，不能把持有共享密钥等同于完成发起者认证。

依据：§8.5.1；8.5.2；8.5.3。

## 端到端保护不隐藏全部元数据

适用条件：MCData protected payload，包括端到端保护的数据。

Date and Time明文保留，使服务器能排序并判断是否过期；Payload ID和序号支持跨多条SIP消息拆分。HTTP文件的保护描述随FD信令传递，受保护二进制文件本身经HTTP上传。因此端到端保护不意味着服务器对消息一无所知。

依据：§8.5.4.1 notes 1–3。

## 证据边界

- TS24.282消息格式、TS23.282完整归属/会话流程、KDF及密码算法实现未核；不输出报文实现配方。
- 离网信令使用PCK/GMK另有路径，本页不把在网CSK/MuSiK/SPK规则套用离网；完整密钥失效清理见UE生命周期主题。

## 按需继续

- [delivery-evidence](delivery-evidence.md)
- [conversation](conversation.md)
- [../security/group-key-distribution](../security/group-key-distribution.md)
- [../security/ue-key-lifecycle](../security/ue-key-lifecycle.md)
- [../security/signalling-key-update](../security/signalling-key-update.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页89、90、91、92、93；仅本版本。

原文边界：§8.5.2.1对SPK/MuSiK及标识的列举次序不一致，不可机械套用respectively生成错误映射。
