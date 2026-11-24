# 用户发起紧急告警时，谁进入紧急状态？终端须报告什么？

MCX 业务须支持用户发起**业务紧急告警**。用户发起后，进入业务紧急状态的是**这名 MCX 用户**；发送告警的是**这名用户所用的 MCX UE**。这是两个不同结果。用户已进入紧急状态，不表示某个组也进入紧急状态或紧急组通信已经建立。[TS 22.280 V16.8.0 §5.6.2.1.2 R-5.6.2.1.2-002，印刷页 18](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=19)。

终端发送的告警须包含：

- 位置。
- MCX 业务用户 ID。
- 该用户所属任务关键组织的名称。
- 通知 ID 列表，例如组或其他用户。
- 供紧急组通信使用的各应用业务的 MCX 业务组 ID 列表。所指的是用户选定的组或专用 MCX 业务紧急组。

最后两项用途不同。通知 ID 列表不能代替紧急组通信所用的组 ID，也不能证明这些对象已经收警。本条没有规定用户状态变化和 UE 发送的先后、位置的取得方式或告警的报文格式。

这是 Release 16 的 Stage 1 要求，出自[在网和离网共用的第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)。规范性[表 A.1（MCPTT），印刷页 63](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=64)、[表 B.1（MCVideo），印刷页 74](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=75)和[表 C.1（MCData），印刷页 85](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=86)在 §5.6.2.1.2 行都列出该项。

若问紧急组通信使用哪些应用，见[紧急与迫近危险组通信的应用](common-emergency-and-imminent-peril-group-applications.md)；若要判断在网是否收到或确认告警，见[在网收警与确认](onnetwork-emergency-alert.md)。离网时的组告警过程，分别查 [MCPTT](offnetwork-mcptt-group-emergency-alert.md)和 [MCVideo、MCData](offnetwork-group-emergency-alert.md)。若看的是终端进出预设区域的在网告警，而非用户主动发起，见[进区或离区的在网流程](emergency-alert-area-entry-exit.md)。
