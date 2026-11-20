# 双栈 PDN 上，MCPTT 和 MCVideo 必须用同一种 IP 版本吗？

不用从共享的 APN 或 PDN 推定两项业务选同一种 IP 版本。已确认在网 PDN 连接到 §5.2.7.0 所列 APN 之一、连接类型为 **IPv4v6** 时，MC 业务客户端须按配置决定用 IPv4 还是 IPv6。**IPv4v6 描述连接类型，不是三项业务的选择结果。**〔TS 23.280 V16.7.0，Rel-16，Stage 2，§5.2.7.0 末段，印刷页 21〕

## 在网：分别查 MCPTT、MCData、MCVideo 的指示

初始 MC 业务终端配置表 A.6-1 分别列有在网 **MCPTT、MCData、MCVideo** 使用 IPv4 还是 IPv6 的指示。业务的 IP 版本指示不是该业务服务器的 URI，也不是 APN 值。比如同一终端共享一条 IPv4v6 PDN，已知 MCPTT 的指示是 IPv6，MCVideo 的指示是 IPv4：按这两项配置，预期分别用 IPv6 与 IPv4。不能将 MCPTT 的 IPv6 套给 MCVideo；若未查到 MCData 自己的指示，不能填成 IPv6 或 IPv4。〔表 A.6-1，印刷页 218〕

## 离网：查目标组，不沿用在网业务那一行

终端通过 ProSe 直接通信时，按该组适用的策略使用 IPv4 或 IPv6。表 A.4-3 为离网 MC 业务组单列 IP 版本指示；它与组播 IP 地址、二层组 ID 是不同的参数。红组的离网指示是 IPv4 时，即使该终端的在网 MCPTT 指示是 IPv6，也不能把这项在网配置套给红组。只掌握组播地址、二层组 ID 或在网业务配置时，仍应核对该组适用的离网配置。〔§8.1.3.2，印刷页 44；表 A.4-3，印刷页 217〕

这些规则用于判断**按配置应当用什么**。只知道 PDN 支持两种 IP、域名能解析成某个地址，或配置表已填值，都不能证明某次通信实际使用该 IP 版本；要核对那次通信的报文或端点记录。本段不规定配置缺失时的默认选择、IPv4/IPv6 回退次序或具体 DNS 行为。

查[APN 的用途与接入条件](attachment-apn-roles.md)或[离网组标识与 ProSe 地址](../groups/offnetwork-prose-addressing.md)，分别定位承载和组地址。依据：[3GPP TS 23.280 V16.7.0，Release 16，Stage 2（ETSI）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123280/16.07.00_60/ts_123280v160700p.pdf#page=22)。
