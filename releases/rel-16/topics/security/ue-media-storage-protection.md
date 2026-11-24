# 哪些在网业务必须保护终端上保存的媒体？

在网 MCVideo 和 MCData 必须为 MCX 终端（UE）上保存的媒体提供所有相关的安全保护。[TS 22.280 V16.8.0 §6.13.6，R-6.13.6-001，印刷页 45](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=46) 给了两类例子：视频和数据是可保存的媒体；数据加密、只允许获授权的 MCX 组成员访问，是保护措施。条文没有指定加密算法，也没有把这两项措施列成固定的实施清单。

这是 Release 16 的 Stage 1 要求。[第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)限定在网使用；规范性[表 B.1（MCVideo），印刷页 79](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=80)和[表 C.1（MCData），印刷页 90](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=91)都列出了 R-6.13.6-001。[表 A.1（MCPTT），印刷页 68](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=69)在 §6.13.6 一行标的是 **NA**：不能把这条要求直接套用到 MCPTT，也不能反推 MCPTT 的终端不需要任何存储保护。

本条管的是终端上已存媒体的保护，没有要求终端录下每次通信，也没有规定媒体保留多久。若视频录在服务器上，见 [MCVideo 服务器录制](../mcvideo/push-to-server-recording.md)；若文件传到内容服务器或通信历史存入用户账户，见 [MCData 文件与消息存储](../mcdata/message-store-vs-file-storage.md)。服务器保存成功不能证明终端上有副本，更不能证明终端副本受到了保护。
