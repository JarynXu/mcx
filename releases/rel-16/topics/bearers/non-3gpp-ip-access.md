# 在网 MCX 能从非 3GPP 网络接入吗？

可以。这里的“在网”说的是用户在使用 MCX 业务系统，不要求最后一段接入一定是 3GPP 网络。业务须提供机制，允许**基于 IP 的非 3GPP 接入**。这项能力受安全和运行约束，也受所用接入技术的限制。[§6.17.1，R-6.17.1-001，印刷页 48](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=49)

规范举的例子是调度员通过控制台连入系统。控制台只是例子，不是唯一允许的设备。反过来，控制台已有 IP 连通性，也不能证明该终端或业务请求已获准接入。这里仍有一个要访问的 MCX 系统，不是两台终端在没有该系统的情况下直接通信。[§6.17.1 注，印刷页 48](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=49)

这是 [3GPP TS 22.280 V16.8.0（Release 16，Stage 1）第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30) 的在网要求。[表 A.1（MCPTT），印刷页 69](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=70)、[表 B.1（MCVideo），印刷页 80](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=81)、[表 C.1（MCData），印刷页 91](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=92)均列出R-6.17.1-001。

要判断接入方究竟是调度终端还是外部应用，见[外部应用的认证与授权](../identity/external-application-access.md)；若问题是用户迁入伙伴系统时该接哪个移动网，见[伙伴迁移的网络接入](partner-migration-network-access.md)。
