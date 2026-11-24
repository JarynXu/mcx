# 哪些在网 MCX 业务必须支持合法监听？

在网 MCPTT、MCVideo 和 MCData 都必须支持合法监听（lawful interception）。[TS 22.280 V16.8.0 §6.13.5，R-6.13.5-001，印刷页 45](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=46) 要求的是业务具备这项能力，没有要求每次通信都被监听。本项没有授予任何人监听某次通信的权限，也没有规定授权条件、监听接口或操作程序。

这是 Release 16 的 Stage 1 要求。[第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)限定在网使用；规范性[表 A.1（MCPTT），印刷页 68](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=69)、[表 B.1（MCVideo），印刷页 79](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=80)和[表 C.1（MCData），印刷页 90](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=91)都列出了 R-6.13.5-001。

能力要求不能证明某次通信实际被监听。例如，一份 [MCVideo 服务器录像](../mcvideo/push-to-server-recording.md)可以是业务录制的结果；仅凭这份录像，不能认定发生了合法监听。
