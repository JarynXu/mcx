# 在网紧急告警：谁确认收警，业务须掌握谁的状态？

甲发了紧急告警，屏幕提示“业务已收到”。这条提示能说明 MCX 业务收到了甲的告警；它不是同组乙的回执。[R-6.8.8.4.1-002，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

**业务一定要让终端激活告警能力吗？** MCX 业务可以允许符合原文所列情形的 MCX UE 激活紧急告警能力。该版列举的是“unauthorized, not registered, or authenticated”（未获授权、未注册或已认证）。原文最后一项是肯定式，不能改读为“未认证”。本项不强制业务允许激活，也不能作为绕过认证或授权的依据。 [R-6.8.8.4.1-001，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

**业务收到告警，谁应获知？** MCX 用户须得到通知，获知 MCX 业务已收到紧急告警。收到告警的是业务，收到这项通知的是用户。仅凭业务收警不能认定对端或组员收到告警、用户已经阅读告警，或紧急通信已经建立。 [R-6.8.8.4.1-002，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。MCX 业务须支持配置通知用户的方式；视觉或声音提示是例子。本项没有指定必须使用哪种提示、是否同时使用两种，也没有指定由谁配置。 [R-6.8.8.4.1-003，印刷页 42](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=43)。

**业务还须记住什么？** MCX 业务须持续掌握该 MCX UE 的业务紧急状态，直到该状态被取消。这是 UE 的状态，不是组的状态或一条告警。条文没有规定状态从哪一刻开始、由谁取消，或取消采用什么程序。 [R-6.8.8.4.1-004，印刷页 43](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=44)。

**终端成功注册/认证后，会获知哪些告警？** 终端向 MCX 业务成功注册/认证后，MCX 业务须告知该终端当前仍有效的业务紧急告警。“注册/认证”保留原文的斜线，不据此判定两者必须都做或任选其一。本项没有指定 IMS 或 LMS 注册、协议消息、通知时限，也不证明组员已收到告警。 [R-6.8.8.4.1-005，印刷页 43](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=44)。这里的通知告诉终端“哪些告警还有效”；前面的收警通知告诉用户“业务收到了这条告警”。两者不能相互替代。

**能把告警发给附近的人吗？** MCX 业务须提供机制，使紧急告警能发往预配置的用户重组（User Regroup）操作所创建的临时 MCX 业务组。注中的例子是联系距用户当前位置一定半径内的特定其他用户。本项不要求按半径选人、设置地理围栏或由进出区域触发告警，也不保证每名组员收到。 [R-6.8.8.4.1-006，印刷页 43](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=44)及[该项后的注，印刷页 43](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=44)。若要查谁创建和修改临时组，见[在网用户重组](../groups/onnetwork-user-regroup-membership.md)；若要传送的是紧急组通信而不是告警，见[紧急组通信的临时组发送机制](onnetwork-emergency-group-communication.md)。

适用范围见 [TS 22.280 V16.8.0（Release 16，Stage 1）第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)。规范性表 [A.1（MCPTT），印刷页 68](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=69)、[B.1（MCVideo），印刷页 79](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=80)、[C.1（MCData），印刷页 90](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=91) 均在 §6.8.8.4.1 下列出六项要求；表中上一级标题 §6.8.8.4 的 NA 不是这六项的标记。

要判读具体过程，MCPTT 客户端的发警与反馈见 [Stage 3 独立组告警](standalone-group-alert-client.md)；MCVideo、MCData 的在网组员通知及所带位置见 [Stage 2 组告警](onnetwork-group-alert-location.md)，进出预设区域另见[区域触发程序](emergency-alert-area-entry-exit.md)。离网分别查 [MCVideo、MCData 的组告警](offnetwork-group-emergency-alert.md)或 [MCPTT 的组告警](offnetwork-mcptt-group-emergency-alert.md)。这些流程各有适用条件，不是上述六项要求的共同前提。
