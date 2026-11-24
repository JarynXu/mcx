# 本地发起的在网环境监听：被听用户和远端听方谁能结束？

**发起人也是被听的一方。** 业务须允许获授权的 MCX 用户通过自己当前使用的 MCX UE 发起环境监听，由另一名获授权的 MCX 用户接收。接收方可以是调度员，不限于调度员。“本地”指从被听方发起，不是离网通信。[R-6.15.2.2.3-001，印刷页 46](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=47)

本地触发后，业务须允许以下两方结束监听：

- 被听的 MCX 用户本人。
- 在这次通信中担任听方的远端 MCX 业务管理员和/或获授权用户。

远端管理员的职务不能代替“曾是本场听方”这个条件。条文说这两方**可以**结束，没有写成只有远端一方可以。[R-6.15.2.2.3-002，印刷页 46](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=47) 远端发起时另有“仅远端获授权用户可结束”的规定，见[远端发起的环境监听](onnetwork-remotely-initiated-ambient-listening.md)。

这些是[TS 22.280 V16.8.0（Release 16，Stage 1）第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)的在网要求。规范性表 [A.1（MCPTT），印刷页 69](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=70)、[B.1（MCVideo），印刷页 80](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=81)、[C.1（MCData），印刷页 91](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=92) 在 §6.15.2.2.3 下均列出这两项。对被听终端的[发送和提示要求](onnetwork-ambient-listening.md)不随发起方向改变。若需判断某次已建立的在网按需 MCPTT 呼叫是否已经释放，看 [MCPTT 释放证据](ambient-call-release-evidence.md)；有权结束，不等于已执行结束。
