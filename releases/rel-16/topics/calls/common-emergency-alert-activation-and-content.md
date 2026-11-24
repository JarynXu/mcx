# 谁能激活业务紧急告警？告警内的业务组 ID 怎么确定？

**有权激活告警，不等于已经发出告警。** 业务须给获授权的用户提供激活业务紧急告警能力的途径。MCX 业务还须支持这项告警能力：一旦由 MCX 用户发起，进入业务紧急状态的是这名用户，发送告警的是这名用户所用的 MCX UE。条款没有指定谁授予激活权限，也没有规定状态变化和终端发送的先后。[R-5.6.2.4.1-001、R-5.6.2.4.1-002，印刷页 20](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=21)

**告警要带四项信息：** 位置、MCX 业务用户 ID、MCX 业务组 ID、该用户所属任务关键组织的名称。组 ID 按组配置确定，可以是用户所选组，也可以是专用 MCX 业务紧急组的 ID。例如，甲选了日常组 G，但配置为告警使用专用紧急组 E，则此处取 E 的 ID。条款不指定位置怎样取得或这些信息如何编码。[R-5.6.2.4.1-003，印刷页 20](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=21)

依据是 3GPP TS 22.280 V16.8.0（Release 16，Stage 1）[在网、离网共用的第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)。[表 A.1（MCPTT），印刷页 63](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=64)、[表 B.1（MCVideo），印刷页 74](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=75)、[表 C.1（MCData），印刷页 85](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=86) 的 §5.6.2.4.1 子行都列这三项。三表的 §5.6.2.4 父标题行虽写 NA，不能据此跳过子行。

UE 已发警和用户进入紧急状态，都不能证明组的状态改变或某场紧急通信已建立。收件对象分别按[组、紧急私通信和区域通知](common-emergency-alert-distribution.md)判断。如需判断[在网业务是否已收警](onnetwork-emergency-alert.md)，或查离网的具体程序，另读 [MCPTT](offnetwork-mcptt-group-emergency-alert.md)或 [MCVideo、MCData](offnetwork-group-emergency-alert.md)。
