# 管理员能为哪些用户的组通信设置最长时长？

业务须让 MCX 业务管理员能为**其权限范围内的 MCX 用户**配置**组通信**的最长时长。条文的权限限定落在用户上。它没有授予管理员为权限外用户设置时限的权力，也不是让管理员为所有组统一设一个时限。见 3GPP TS 22.280 V16.8.0（Release 16，Stage 1） [R-5.1.6-001，印刷页 13](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=14)；网络模式见[第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)。

[表 A.1（MCPTT），印刷页 62](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=63)、[表 B.1（MCVideo），印刷页 73](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=74)、[表 C.1（MCData），印刷页 84](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=85) 的 §5.1.6 行分别是 -001、-001、NA。本项适用于 MCPTT、MCVideo。MCData 在这一行明确为 NA，不能单凭这条要求 MCData 提供同样的能力。

本项未给时长数值、计时起点或到时动作。若问在网时组通信允许**保持活动**多久，见[在网组通信终止条件、活动时长和人数](onnetwork-administrative-lifecycle.md)；若问离网到时是否提示或释放，见[离网组通信与私通信时限](../calls/offnetwork-communication-duration-limit.md)。管理员为其权限内用户配置**在网私通信**最长时长，另见[在网私通信终止与时限](../calls/onnetwork-private-termination-and-duration.md)。
