# 离网SDS：首次发送的目标与关联上下文

## 共同条件

- 固定 TS24.282 V19.7.0，Stage 3，§9.3 离网 standalone SDS 信令控制面；不套用在网 SIP/MSRP、MBMS/MBS、FD 或 SDS session 过程。
- 各结论仅在所列客户端角色与事件成立时使用；发送前授权、安全上下文、承载及地址配置应满足各自规范。本页不提供完整编码、安全或发现实现。
- 组发送请求在 AllowedSDS=false 时须拒绝并停止余下发送程序；其余初始发送参数和安全处理仍按§9.3.2.2，不以重试结论跳过。
- 本页仅普通离网初始消息生成，不展开增强状态、紧急或安全算法；初发的各项条件单独判断，不以重试或接收通知已发生为前提。

## 目标、会话与新消息分别标识

适用主体：发送MCData客户端。

适用条件：收到发送普通离网standalone SDS的指示，且未被适用的组AllowedSDS守卫停止；按是否one-to-one、是否已有conversation、是否回复或面向应用分别判断。

单用户发送保存目标用户ID，组发送保存目标组ID；消息Sender字段取自己的用户ID，Recipient或Group字段按相应分支取保存的目标。指明已有conversation时沿用其ID，否则生成UUID作为Conversation ID；本次新消息另生成UUID作为Message ID。保存当前UTC为传输时间，并将这些保存值写入对应IE。表15.1.7.1-1把目标用户和组字段列为O，不取消发送过程按分支设置目标字段的SHALL。

规范强度：保存目标、适用关联信息及指定字段动作SHALL；处置请求选择和可选IE保留MAY，不能把保存义务改为无条件携带义务。

- 不把业务用户/组ID当IP地址；传输规则沿用既有页，不新增发现、映射算法。
- UUID算法依赖RFC9562，本轮未核其细节；这是新消息生成，不为重试重新生成标识。

依据：[TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf) §9.3.2.2 steps2,4,5,10,11a–b,11d–f;15.1.7.1 Table15.1.7.1-1，印刷页261、262、356。

## 保存上下文不等于必须携带可选字段

适用主体：发送MCData客户端。

适用条件：收到发送普通离网standalone SDS的指示，且未被适用的组AllowedSDS守卫停止；按是否one-to-one、是否已有conversation、是否回复或面向应用分别判断。

客户端可按所需处置选择DELIVERY、READ或DELIVERY AND READ，并可把保存值写入处置请求IE。指明回复另一条SDS时须保存被回复消息ID，但InReplyTo的携带仍为可选；目标为应用时须保存Application ID或Extended application ID，对应IE携带仍为可选。表15.1.7.1-1同样将这些IE列为O。处置请求表达所请求的结果，不是接收者已送达、已读或应用已处理的证明。

规范强度：保存目标、适用关联信息及指定字段动作SHALL；处置请求选择和可选IE保留MAY，不能把保存义务改为无条件携带义务。

- 不自行规定可选IE省略时接收端如何恢复上下文，也不将两个应用ID改成必须同时出现。
- 本页不是完整线级消息模板。载荷和安全分支仍须按原文适用条件执行；未核安全规范，不以字段构造证明安全完成。

依据：[TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf) §9.3.2.2 steps3,6,7,11c,11g–h;15.1.7.1 Table15.1.7.1-1，印刷页261、262、356。

## 证据边界

仅初始业务上下文生成，不覆盖完整编码、密钥处理、承载发现或端到端结果。

## 按需继续

- [offnetwork-sds-retransmission](offnetwork-sds-retransmission.md)
- [offnetwork-sds-reception-and-read](offnetwork-sds-reception-and-read.md)
- [offnetwork-sds-notification-retry](offnetwork-sds-notification-retry.md)
