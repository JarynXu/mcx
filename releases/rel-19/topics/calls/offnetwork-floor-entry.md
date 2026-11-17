# 离网话权入口：组呼参与者与临时仲裁者

## 适用范围

- 仅适用于 3GPP TS 24.380 V19.1.0 §7 的普通离网 MCPTT 组呼，不是在网 G/U 服务器模型。排除私呼、广播、system、紧急/迫近危险、dual floor、multi-talker 及 audio cut-in。
- 覆盖终接或后来加入者从 O: silence 发起请求、在 O: pending request 竞争后按 T201/C201 进入本地许可的有限路径，以及初始化和无排队本端释放边界；不是任意收包下的完整状态机。
- 离网呼叫已成功建立，且本条所需授权、载体与配置已满足。未核 ProSe、安全、SSRC 认证、完整报文编码或 TS 24.483 配置取得及缺失处理。
- 请求竞争中的优先级比较以已知有效比较值为输入；不覆盖完整离网优先级、抢占或排队算法。使用无排队释放分支时，必须另确认没有 queued request，不能从普通呼叫推导队列为空。
- 收到的事件按实际到达顺序处理。没有该状态专门过程的消息或媒体丢弃且状态不变，格式错误也忽略（§7.2.3.1，印刷页 132–133）。仅在逐条条件满足时采用下述动作。

## 谁承担离网话权仲裁

适用主体：单个MCPTT客户端/临时floor arbitrator。

当前状态：按本地O状态判断。

适用条件：
- 离网floor control session已开始。

当前发媒体的客户端临时承担仲裁；话权交给另一客户端后，新端开始发送媒体才成为新的仲裁者。控制消息面向全体参与者，不经另一个在网floor server；通常单仲裁者，但原文承认短时多个客户端可同时处于仲裁角色。

- 发送Floor Taken或本地has permission不能证明无线范围内唯一持有人、全员已收到或冲突已经完全收敛。

规范强度：架构/状态机描述。

依据：3GPP TS 24.380 V19.1.0 §7.1;7.2.3.1，印刷页 129、130、132、133。

## 终接或后来加入者进入静默状态

适用主体：终接/后来加入的floor participant。

当前状态：Start-stop。

适用条件：
- 尚无活动floor session；call control请求以terminating client启动普通组呼话权。

创建floor实体/基本状态机，启动T230并进入O: silence。此状态表示本端不知道任何仲裁者、尚未发请求且当前未接收 RTP 媒体；并不表示全组客观无人讲话。

计时与计数边界：T230运行；不是T201或呼叫控制TFG计时器。

- call control的S3、收到ANNOUNCEMENT或ACCEPT不能替代本地话权状态。

规范强度：SHALL；另列MAY及证据分析不新增协议义务。

依据：3GPP TS 24.380 V19.1.0 §7.2.1;7.2.3.2.3;7.2.3.3.1，印刷页 130、134、135、136。

## 发起入口的显式与隐式请求差异

适用主体：发起floor participant。

当前状态：Start-stop。

适用条件：
- 分别读取call control的originating启动请求及§7.2.3.2.2的带explicit floor request公告入口。

§7.2.1写originating启动后进入has permission并描述通常隐式持权；§7.2.3.2.2却限定建呼公告含explicit floor request，才列创建、向其他参与者发Granted（优先级及自身User ID）、保存自身SSRC和进入has permission。两段前提应分别保留，不把所有ANNOUNCEMENT补成含explicit request。

- TS 24.379 V19.4.0 的发起调用仅提供呼叫控制背景；该 explicit request 在 MONP 公告中的完整承载与映射未核。不得据此声称完整发起闭环或固定版本组合互通。

规范强度：SHALL；另列MAY及证据分析不新增协议义务。

依据：3GPP TS 24.380 V19.1.0 §7.2.1;7.2.3.2.2，印刷页 130、134。

## 原文差异

§7.2.1 versus 7.2.3.2.2（印刷页 130、134）：初始化总则通常隐式持权，细化入口却以公告含explicit floor request为前提；不自行合并成任意公告即持权。

## 证据边界

- 只覆盖列明事件，不是离网话权整体实现。未覆盖排队授予/T233、完整远端Granted/Deny、抢占、并呼合并或全部冲突收敛。
- TS24.483配置获取、完整报文安全/编码及与TS24.379 V19.4.0精确版本组合互操作未核。
- 无排队Release缺少显式stop RTP步骤、发起explicit/implicit文字差异均保留，不用常识补闭环。

## 按需继续

- 呼叫已成功建立，需判断已判非抢占请求的排队、用户接受与媒体移交事件，查[离网话权排队与移交：收到授予、用户接受和首包观察](offnetwork-floor-queue-and-handoff.md)。
- [离网请求竞争：重试、计数复位与本地取得话权](offnetwork-floor-request-contention.md)
- [呼叫控制：探测、加入与发起](offnetwork-group-probe-and-start.md)
- [呼叫控制：用户接受与公告](offnetwork-group-acceptance-and-announcement.md)

[3GPP TS 24.380 V19.1.0 / ETSI TS 124 380 V19.1.0（2026-01）](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅适用所列版本和条款。
