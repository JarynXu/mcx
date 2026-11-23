# 在网无话权控制私通信：谁能发起，通知和接收终端各看什么？

**请求已收到，不等于通信已建立。** 读 3GPP TS 22.280 V16.8.0（Release 16）的在网无话权控制私通信 Stage 1 要求时，分别看发起者的授权、接收用户指定的终端和通知表示的事实。以下四项都是业务须提供的机制，不是一次通信必须按顺序经历的四个步骤。[第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)；[§6.7.5，印刷页 39（PDF 第 40 页）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=40)；[§6.7.2-005，印刷页 38（PDF 第 39 页）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=39)。

| 要查什么 | 业务须提供什么 |
| --- | --- |
| 终端发起 | 业务须提供机制，让 MCX UE 向任一目标 MCX 用户发起无话权控制私通信，前提是**该 UE 的当前 MCX 用户已获准向该目标发起此类通信**。授权判断针对该终端的当前用户和本次目标，不是终端有一个身份就能联系所有人。本条没有把这一机制只写成手动开始。[R-6.7.5-001，印刷页 39](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=40)。 |
| 自动开始的发起 | 业务须提供机制，让 MCX 用户向任一目标 MCX 用户发起自动开始（Automatic Commencement）的无话权控制私通信，前提是**发起用户已获准向该目标发起此类自动开始通信**。一般联系权限或仅有手动开始权限不证明这项授权。发起者仍是 MCX 用户；名称并不规定业务应自行发起或被叫怎样接听。[R-6.7.5-002，印刷页 39](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=40)。 |
| 通知哪件事 | 业务须提供机制，使**发出请求的获授权 MCX 用户**获知**接收用户已收到该私通信请求**。这不是已接受、已应答、请求已显示、已建立通信或已收媒体的通知。[R-6.7.5-003，印刷页 39](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=40)。 |
| 接收用户用了多台终端 | 接收 MCX 用户已用多台 MCX UE 登录**该 MCX 业务**时，业务须提供机制，让无话权控制私通信可与**接收用户指定用于此类私通信的 MCX UE**建立。指定方是接收用户，不是发起用户。[R-6.7.2-005，印刷页 38](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=39)。 |

例如，乙已用终端 B1、B2 登录同一 MCX 业务，并指定 B2 用于无话权控制私通信。-005 要求能与 B2 建立这类通信，不凭指定动作推定已经建立，也不规定未指定时选哪台、是否并行递送或 B2 不可用时怎样处理。若甲随后被告知乙已收到请求，-003 的通知报告的是收到请求，不表示乙同意或有媒体往来。条文没有为未收到请求指定通知，也未规定具体信令、通知时点或时限。要查实时通信本身是否被接收或显示的通知，见[实时通信的接收或显示通知](../media/realtime-receipt-notification.md)，不要把它与收到通信请求混在一起。

**适用业务：** 表 A.1（MCPTT）、B.1（MCVideo）、C.1（MCData）均在相应要求行明确列出这四项。[表 A.1，印刷页 67](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=68)；[表 B.1，印刷页 78](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=79)；[表 C.1，印刷页 89](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=90)。

[发起权限及通信对象的管理员配置](onnetwork-no-floor-private-authorization.md)、[在网和参与能力的查询](onnetwork-private-status-query-visibility.md)、[多终端登录](../identity/multiple-device-login.md)回答的是不同问题。要读[MCPTT 无话权控制信令](private-no-floor-control-identification.md)、[普通 MCPTT 私呼的服务器准入](private-server-admission-routing.md)或[MCVideo 一对一视频拉取](../mcvideo/one-to-one-video-pull.md)，各按自己的 Stage 2 或 Stage 3 条件核对，不能用它们替代本页的业务能力要求。
