# MCData 也要求与 GSM-R 双向互通位置吗？

**是。** MCX 业务系统须让两侧的信息能够双向互通：一侧是 MCX 用户的定位信息，另一侧是为铁路移动通信系统 GSM-R 的移动台提供的位置信息。条文在 GSM-R 一侧引用 [9]、[10]，没有规定位置必须由移动台自己测得或上报。[§6.17.3.1，R-6.17.3.1-001，印刷页 49](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=50)

例如，只看到 GSM-R 一侧的信息出现在 MCX 客户端，能说明这一个方向有过结果，还不能说明 MCX 用户的定位信息也能向另一侧互通。条文要求双向能力，没有规定每份报告都要向两侧同时发送，也未指定 LMS、接口、坐标格式或周期。

这是 [3GPP TS 22.280 V16.8.0（Release 16，Stage 1）第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30) 的在网要求。[表 A.1（MCPTT），印刷页 69](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=70)、[表 B.1（MCVideo），印刷页 80](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=81)、[表 C.1（MCData），印刷页 91](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=92)均列出R-6.17.3.1-001。 MCData 的表 C.1 在 GSM-R 小节只列 **-001**，不能因位置条目适用就把同节的系统兼容性与功能别名条目一并套给 MCData。

若所问是在 MCX 系统内向谁提供位置、谁可启停报告，见[在网位置共享与报告控制](onnetwork-location-sharing-and-report-control.md)；它不是 GSM-R 两侧之间的取位或订阅规程。
