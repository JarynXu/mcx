# 紧急和迫近危险组通信使用哪些业务应用，优先级由谁请求？

用户发起**紧急组通信**时，须使用一个 MCX 业务应用子集。用到的应用须同时满足两个条件：与发起用户相关，且已为目标 MCX 业务组配置。MCPTT、MCVideo 是应用例子；条文没有要求每次都用这两个应用，也没有指定要用多少个。[TS 22.280 V16.8.0 §5.6.2.1.2 R-5.6.2.1.2-001，印刷页 18](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=19)。

业务须让 **MCX 业务管理员**能配置两件事：

- 对**紧急组通信**，配置 MCX 用户处于业务紧急状态时进行这类通信所用的应用。[TS 22.280 V16.8.0 §5.6.2.1.2 R-5.6.2.1.2-004，印刷页 18](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=19)。
- 对**迫近危险组通信**，配置哪些应用可以用于这类通信。本项没有附加用户处于业务紧急状态的前提。[TS 22.280 V16.8.0 §5.6.2.1.2 R-5.6.2.1.2-005，印刷页 18](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=19)。

用户请求**迫近危险组通信**时，须由 **UE 内的 MCX 业务**为**当前活动的业务应用**请求迫近危险优先级。管理员配置某个应用可用，不表示它当前处于活动状态；终端发出优先级请求，也不表示已经获准或已抢占其他通信。[TS 22.280 V16.8.0 §5.6.2.1.2 R-5.6.2.1.2-003，印刷页 18](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=19)。

这是 Release 16 的 Stage 1 要求，出自[在网和离网共用的第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)。规范性[表 A.1（MCPTT），印刷页 63](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=64)、[表 B.1（MCVideo），印刷页 74](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=75)和[表 C.1（MCData），印刷页 85](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=86)在 §5.6.2.1.2 行都列出上述四项。正文列举的应用不是业务适用性清单。

若问在网业务能为哪些参与者请求提高优先级，分别查[在网紧急组通信](onnetwork-emergency-group-communication.md)和[在网迫近危险组通信](onnetwork-imminent-peril-group-communication.md)。若问离网时谁能设置迫近危险状态、要用哪个预配置组，查[离网迫近危险组通信](offnetwork-imminent-peril-group-communication.md)。若用户发起的是告警，查[紧急告警的用户状态和终端发送](common-user-initiated-emergency-alert.md)。
