# MCVideo广播媒体角色：发起者发送、接收者Mode0与拒绝反向发送

TS24.281 V19.3.0 与媒体TS24.581 V19.2.0分别标版。普通在网、有transmission control、以broadcast发起的新组呼；普通GMS组，client–O-PF–CF–T-PF–client。不是chat、system、ad hoc、NCF/gateway、临时/预配置重组、功能别名、远程/ambient、预建立、重入、广播升级或离网。

请求broadcast-ind=true，但不含emergency-ind、imminentperil-ind、alert-ind、user-requested-priority或优先Resource-Priority；客户端既有emergency/group-priority/call-priority状态均未置位，CF组emergency和imminent-peril状态为false。广播不被当成紧急呼叫，亦不由本次未点紧急按钮推定全部既有状态为普通。

每条claim只继承本主题common_conditions及自身conditions，不继承前条成功。TS24.281 V19.3.0 §9.2.1.2.1.1 step3明确调用6.2.8.2，才构成这里使用prearranged signalling入口的依据；不因名字类似就继承既有普通非广播页面的全部结论。

该主题以各claim指明的24.581服务器/客户端状态及事件为准；SIP准入、安全和实际协商仍独立存在。只取初建广播的单源路径，不将重入、普通call升级广播、队列/抢占、多源和释放补成完整算法。

## 发起者与终接者初始许可

适用条件：实际读取24.581 V19.2.0：session已按broadcast建立，分别考察originating participant与terminating participant；不是rejoin或由普通call后升级为broadcast。

6.2.4.2.2 step5规定originating participant进入U: has permission to transmit；终接者6.2.4.2.3在发送SIP200建立call时仍进入U: has no permission to transmit。因而普通非广播页“必须等Granted才进入发送许可态”不能原封不动用于广播发起者。已在许可态时，收到用户编码视频或已有缓存才按6.2.4.5.2要求向服务器转发。

- 同一originating条step4对implicit请求要求T100/C100=1并进入pending，step5又对broadcast要求进入permission；本页分别保留条件及书写顺序，不静默删除一支或推导同时命中时的计时器清理。
- 客户端状态不是服务准入的替代，也不证明服务器各实例/所有接收者已ready。初始SSRC取得、完整广播授予接口及两规范版本组合未闭合，不能凭这条省略协商或安全。

依据：§6.2.4.2.2 steps1–5;6.2.4.2.3;6.2.4.5.1/.5.2，印刷页 36、39。

## 服务器拒绝接收者发送

适用条件：服务器关联某participant的basic transmission接口在U: not permitted and Transmit Idle或U: not permitted and Transmit Taken，收到其Transmission Media Request；session为broadcast。

Idle态只把广播发起者的请求转交仲裁，非发起者则SHALL回Transmission Reject cause5 Receive only，并留Idle。Taken态的broadcast专段直接规定回cause5并留Taken，没有重复Idle段的initiator例外。两段都可附解释/要求Ack，并带相应Transmission Indicator。被邀请者即使已经SIP接通或能接收媒体，也不能据此取得发送权。

- Taken同一条还有普通优先/排队处理段，本文不裁决其重叠分支优先级，也不将broadcast专段私自改写为“仅非发起者”。Idle中转交仲裁也不是已经grant。
- 这是server的per-participant接口，不是客户端6.2.4状态机。未展开广播升级、抢占、多源或队列算法。

依据：§6.3.5.3.4;6.3.5.4.4，印刷页 70、73、74。

## 通用接收控制选择Mode0

适用条件：服务器general reception处于Gr: Reception Idle，收到该已建立broadcast通话的Media Transmission Notification；相关basic接口已初始化。

服务器向其他participants发送通知，broadcast分支SHALL设置Reception Mode=0。按发送者关联的C11设为通话中接收客户端总数，保存参与者MCVideo IDs直到该媒体接收结束，C7按各流C11总和设置，并进入Gr: Reception Accepted。普通非broadcast/system/emergency/imminent-peril分支才设Mode1并从C11=0等待显式请求；不能把普通组Mode1限制套到broadcast。

- C11/C7是此general实例的计数，不是收到每人RTP或应用已显示视频的确认数量。这里的automatic reception也不是SIP Answer-Mode=Auto。
- 本页限首个源通知的Idle入口，不扩已有Accepted多流、privacy、C11计数变化或无人接收终止。

依据：§6.3.6.2.2;6.3.6.3.3，印刷页 87、88。

## 服务器按接收者安装源许可

适用条件：服务器某接收participant的basic reception接口处于U: not permitted to receive；收到需转给该participant的Media Transmission Notification且Reception Mode=0。随后若进入permitted态并处理RTP，另按该态事件。

接口发送含源User ID/SSRC的通知，可要求Ack；C9未达上限时加1，把获授发送源的音视频SSRC放入该接口Active SSRC List并进入U: permitted to receive。后续只有RTP SSRC在该列表内才按6.3.7.4.3转给媒体分发器，不在则丢弃。广播自动许可仍有接收方及源范围，不是所有未建会话终端都可收到任意流。

- 这是server按接收participant的basic实例及Active SSRC List，不是客户端按源新建basic的实例。实际下行、播放成功和错误恢复未由列表存在保证。
- 源码表述为转给media distributor；不擅自改成跨网络最后一跳传输已成功。

依据：§6.3.7.3.2/.3;6.3.7.4.3，印刷页 96、97、98、99。

## 客户端按源建立接收状态

适用条件：客户端general处于U: reception controller，收到server的Media Transmission Notification且Reception Mode=0。

客户端按Ack位需要时回Source=0/Message Type=6，向用户通知并保存发送者User ID和音视频SSRC；收到Functional Alias ID时也保存。它新建一个basic reception实例并映射这些源标识，进入U: has permission to receive；general仍留reception controller。该自动分支不要求先由用户再点一次Receive Media Request，但也不授予该客户端发送权。

- 客户端basic按源映射，与server per-participant basic不同。流接收许可不证明实际媒体已到达或解密播放成功。
- 广播的终止也有专属行为：basic terminated会通知general进入Call releasing（6.2.5.8.1），但本页未展开结束流程，不照搬普通非广播“只删源不动general”的结论。

依据：§6.2.5.3.2;6.2.5.8.1，印刷页 46、51、52。

## 证据边界

- 未核23.281业务语义或24.484全部广播专用配置，不从不存在的查找命中断言“没有其它授权”。
- 无required/TNG1未运行、自动接听、支持缓冲且未发final是本成功小链边界；手动、required聚合、无缓冲最终成功和全部失败/超时恢复未闭合。
- originating广播step5与同时implicit的step4均保留；初始媒体SSRC、服务器全部初态与客户端状态的端到端映射尚未闭合。
- 广播升级、恢复/晚入、停止广播及全组释放未展开；不能把普通非广播的permission/terminated结论直接类推。
- GKTP/MIKEY算法、安全验证、媒体端口/完整SDP、GMS配置schema、跨系统与跨版本互操作仍是外部依赖。

## 按需继续

- [broadcast-auto-setup-result](broadcast-auto-setup-result.md)
- [participant-transmission-control](participant-transmission-control.md)
- [participant-reception-control](participant-reception-control.md)
- [server-reception-permission](server-reception-permission.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；按条目单独标示媒体来源。

- [广播停止与会话释放的适用条件](broadcast-reception-ending.md)
