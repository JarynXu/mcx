# 离网时，发送本机位置和获取终端间的距离各有什么条件？

甲的 MCX 终端知道自己的位置时，必须能在隐私限制允许的范围内，把**本机的位置**发给其他 MCX 终端。这是对发送能力的要求，不是要求终端一知道位置就广播；位置未知时，这一条也没有要求先定位再发送。见 [TS 22.280 V16.8.0 §7.8，R-7.8-001，印刷页 55](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=56)。

如果要知道甲、乙相距多远，条件是**乙在甲的通信范围内**。甲的 MCX 终端必须能提供一种方式，获取本机与乙的距离。[R-7.8-002，印刷页 55](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=56) 没有把已知本机位置或先交换坐标列为前提，也没有指定测距方法或精度。知道两端相距一百米，单凭这个距离，不能确定任一端的经纬度。

这是 Release 16 的 Stage 1 离网要求，范围见[第 7 章标题，印刷页 50](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=51)。规范性[表 A.1（MCPTT），印刷页 70](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=71)、[表 B.1（MCVideo），印刷页 81](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=82)和[表 C.1（MCData），印刷页 92](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=93) 的 §7.8 行都列出 R-7.8-001 和 R-7.8-002。

这两项要求没有把向位置管理服务器（LMS）注册、订阅或上报列为步骤。在网时谁能[启停位置报告](onnetwork-location-sharing-and-report-control.md)，是另一个问题。离网终端之间传送位置与身份信息时，另见[保密与发送者认证](../security/offnetwork-location-and-identity-protection.md)。
