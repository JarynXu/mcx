# 离网组呼：探测、创建与加入判据

## 适用范围

- 固定 3GPP TS 24.281 V19.3.0（ETSI TS 124 281 V19.3.0，Release 19），Stage 3。
- 既定普通MCVideo组的离网基本组呼，组ID、组播地址和传输配置已具备；非紧急、非迫近危险、非广播、非临时重组、非网关；不将预安排的业务对象等同在网session-type=prearranged。
- emergency state=false，用户未请求紧急或迫近危险，所收公告类型为BASIC GROUP CALL；分别按本地状态、事件和各条条件应用。无竞争呼叫合并、类型升级或迁移。
- 主动端探测加入和终接无需用户确认分支；授权配置、ProSe承载、SDP细节及安全依赖不完整。TS24.581媒体调用仅保留原文接口，不能以S3证明媒体许可、首帧或全组一致状态。
- S1是不在呼叫中；S2等待探测公告；S3参与进行中呼叫；S6在拒绝/离开后不呈现来话公告；S7是已发探测但未收发公告时取消后的等待。T0等待建立，T2为进行中的普通类型。S与T属于不同状态机。

## 组地址与呼叫状态不沿用私呼

适用条件：主体为MCVideo 客户端，本地基本呼叫控制；适用状态为按 MCVideo group ID 维护基本控制实例。 参与所选离网组呼。

MONP 载体是完整 UDP 负载，发往组 multicast IP 的 8809 端口，TTL=255；同组地址及端口收到的 UDP 按载体处理。会话含一个媒体传输控制实体；本版同一呼叫期间媒体流不能修改，SDP 保持不变。同时呼叫数受 MaxCallNc4 约束。

- 不能从在网 SIP 的 PF/CF 或离网私呼 P 状态推导组 S 状态。组地址配置、载体完整编码及超限处置不在本主题闭合。

规范强度：所述过程动作 SHALL；另外标明 NOTE、MAY 与解释边界。

依据：3GPP TS 24.281 V19.3.0 §9.3.1.1.1–2；§9.3.2.1–3，印刷页 294、295、296。

## 发起先探测，超时才自行公告

适用条件：主体为MCVideo 客户端，本地基本呼叫控制；适用状态为S1→S2；S2 重传。 用户要求向既定组发起普通呼叫。

存组 ID、创建 call type control、发送含组 ID 的 PROBE，启动 TFG3 和 TFG1 后进入 S2。TFG3 到期重发 PROBE 并重启 TFG3，仍为 S2。普通类型要求 emergency state=false 且用户未请求紧急或迫近危险；类型控制设置 BASIC GROUP CALL、相应 ProSe 优先级、当前变更时间及本用户 ID，留 T0。

- 类型控制与基本控制是关联的不同状态机；不补事件调度顺序。探测没有收到响应不证明组内无人。

规范强度：所述过程动作 SHALL；另外标明 NOTE、MAY 与解释边界。

依据：3GPP TS 24.281 V19.3.0 §9.3.2.4.2.1–2；§9.3.3.4.2，印刷页 297、298、308、309。

## 等待结束后创建本地呼叫

适用条件：主体为MCVideo 客户端；基本呼叫控制及关联类型控制，分别按各自状态与事件；适用状态为S2，TFG1 到期。 所选普通类型成立。

先停运行中的 TFG3，生成并存 SDP；在 0 到 65535 之间按均匀分布随机生成 call ID，选择 refresh interval，存自己的发起用户 ID 及 UTC 起始时间。公告携这些值、组 ID、当前类型、最后类型变更时间和用户，Confirm indication 可选。发送公告后建立 SDP 媒体，以 originating transmission participant 调用 TS24.581 clause a.b，启动 TFG6、TFG2 后进 S3。NOTE 固定本版 refresh interval 为10秒。 对应类型控制 T0 在因 TFG1 到期发送公告且 stored current call type=BASIC GROUP CALL 时，按 §9.3.3.4.6 进入 T2。

- 媒体 clause a.b 是原文字面占位引用，未修补。TFG2=refresh*(2/3+2X/3)，X均匀0到1；不是固定每10秒发公告。TFG6=配置MaxDuration−(当前UTC秒−call start time)，不猜负值处置或配置默认。
- 基本控制与类型控制各有触发条件；本条没有定义两个状态机之间的完整调度顺序。

规范强度：所述过程动作 SHALL；另外标明 NOTE、MAY 与解释边界。

依据：3GPP TS 24.281 V19.3.0 §9.3.2.4.3.1；§9.3.2.4.1.1.1；§9.3.2.4.1.2；§9.3.1.1.2；§9.3.3.4.6，印刷页 294、295、297、298、299、311。

## 探测端收到同组公告便进入所列加入程序

适用条件：主体为MCVideo 客户端；基本呼叫控制及关联类型控制，分别按各自状态与事件；适用状态为S2→S3。 ANNOUNCEMENT 的组 ID 匹配已存组 ID；本主题仅普通类型。

停 TFG3、TFG1，存公告 SDP、call ID、发起用户 ID、refresh interval、start time；据 SDP 建立媒体，以 terminating transmission participant 调用 TS24.581 clause a.b，再启 TFG6、TFG2 并进 S3。类型控制 T0 在收到 BASIC 类型且自身已为 BASIC 时复制类型变更时间和用户并进 T2。

- 基本控制入口只列组 ID 匹配，不擅自加入 call ID 相同或 Probe response IE 必须存在的门槛。不能把 S1 的用户确认分支移来；S3 不是实际发流/接收许可。

规范强度：所述过程动作 SHALL；另外标明 NOTE、MAY 与解释边界。

依据：3GPP TS 24.281 V19.3.0 §9.3.2.4.3.2；§9.3.3.4.3，印刷页 299、309、310。

## 未探测接收端有自己的加入条件

适用条件：主体为MCVideo 客户端；基本呼叫控制及关联类型控制，分别按各自状态与事件；适用状态为S1→S3，选择无需用户确认分支。 公告组 ID 不匹配其他状态机已存的组 ID；终接 UE 配置为无需用户 acknowledgement；普通组类型。

存 SDP、call ID、发起用户 ID、refresh interval、组 ID、start time，并创建类型控制。建立媒体并调用 terminating transmission participant 的 TS24.581 clause a.b。仅公告含 Confirm indication 时发送 ACCEPT，含 call ID、本用户 ID、当前类型和组 ID；随后启 TFG6、TFG2，进 S3。 关联类型控制在 T0 收到无需用户确认的空闲接收公告时，先复制最后类型变更时间与用户；公告类型为 BASIC GROUP CALL 时，设置 current type 与离网基本组呼 ProSe 优先级并进入 T2。

- 类型控制 §9.3.3.4.5 与基本控制 §9.3.2.4.3.3 各自规定动作，未在此给出跨状态机的完整调度顺序。

规范强度：所述过程动作 SHALL；另外标明 NOTE、MAY 与解释边界。

依据：3GPP TS 24.281 V19.3.0 §9.3.2.4.3.3；§9.3.3.4.5，印刷页 299、300、310、311。

## 条款边界

§9.3.2.4.3.1–3;9.3.3.4.5–6：基本控制和类型控制分别规定动作；媒体引用仍为TS24.581 clause a.b。

## 未覆盖的行为

- 不覆盖人工确认S4/S5的接受拒绝、重入、并发呼叫合并、紧急/迫近危险或广播。
- TS24.581媒体接口保留clause a.b占位引用；不闭合媒体许可、首帧、缓存清空或跨规范互通。
- MaxCallNc4、MaxDuration和ProSe优先级的配置来源与默认值不在这里展开；不提供负时长算法。
- 跨基本控制与类型控制的调度顺序未规定于所列步骤，不补调度实现。

## 按需继续

- 已参与普通BASIC组呼并收到同组另一BASIC呼叫公告，需要判断有限合并分支，查[离网普通组呼合并：选择另一通话与本地切换](offnetwork-group-merge.md)。
- 普通终接配置要求用户应答，应改读S4/S5条件路径，查[离网组呼来话：等待用户、接受与拒绝后的状态](offnetwork-group-user-confirmation.md)。
- [离网组呼：公告回应与本地离开](offnetwork-group-announcement-and-leave.md)

[3GPP TS 24.281 V19.3.0，ETSI 官方发布版](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅适用于所列版本和条款。
