# 普通预安排组呼：服务器显式传输请求、许可与结束职责

## 适用范围

- 固定 TS24.581 V16.9.0；普通在网、带传输控制的预安排组呼，非广播、系统、紧急、危急或临时组；不含 chat、私呼、离网、MBMS、远程推拉或抢占。显式请求不要求升级呼叫类型。
- 范围限 controlling MCVideo function 内的一般传输仲裁 G 与逐参与者基本接口 U；不展开 PF 跨节点转发及信令服务器建立算法。请求路径为未协商排队的普通参与者、非排队请求；所述整呼叫 Idle 重入动作另要求没有客户端协商排队。
- 初始化、请求、拒绝、授予、实际 RTP、End 与应用释放按各条角色/状态/事件分别适用。协商、业务授权和所需媒体/控制保护仍须满足各自义务，不把已授予、媒体到达或最终释放作为所有事件的共同前提。

## 职责与证据

### 受邀组成员的接口初始化，不等于获准发送

适用：初始化事件：预安排组呼的服务器收到终接 SIP 200；随后 SIP 会话已建立、属于普通组呼，且该客户端是受邀成员。请求事件另要求该成员接口处于 U: not permitted and Transmit Idle；不是把初始化和后续请求同时作为前提。

服务器为每个参与者建立独立的基本传输控制接口 U；预安排组主叫侧是在服务器发送 200 时创建，终接侧是在服务器收到 200 时创建。受邀客户端初始化时，若其他客户端已有发送许可，则进入 U: not permitted and Transmit Taken；若没有其他客户端获准，则 SHOULD 发送 Transmission Idle（消息序列号加 1），并 SHALL 进入 U: not permitted and Transmit Idle。处于后者状态的接口收到关联参与者的显式 Transmission Media Request 时，普通非广播分支将请求转交传输仲裁逻辑，仍留在 U: not permitted and Transmit Idle。

强度：实例创建、所述状态转换和请求转交为 SHALL；无人获准时向受邀客户端发送初始 Idle 为 SHOULD，不改成必发。

- G 是整个呼叫的传输仲裁状态，U 是每个参与者的接口状态，不等于两台物理服务器。G: Transmit Idle 表示当前无人获准；U 的请求转交本身不授予许可。
- G 初始化还受确认指示、基本实例就绪及 mc_granted/隐式请求分支控制。本页不从收到任意 200 推断 G 已 Idle。§6.3.4.2.2 在基本实例初始化后、非临时组、未协商 mc_granted 且不授予隐式请求的分支才明确进入 G: Transmit Idle。
- 已有人获准时的受邀 U: Transmit Taken 仅登记入口，本页不展开该状态的竞争、排队或抢占处理。私呼虽见于 §6.3.2.1 通用说明，§6.3.5.1 的具体创建列表和 .2.2 的 normal group 守卫不能直接当作私呼完整初始化。

依据：TS24.581 V16.9.0 §6.3.1–2.2, 6.3.4.2.2;6.3.4.3.1, 6.3.5.1–2.2 step4, 6.3.5.3.1–4, 14.3.4–5 (initialization boundary)，印刷页 52, 53, 56, 65, 66, 68, 69, 225。

### 仲裁授予、接口许可和真正收到 RTP 分别取证

适用：替代事件分别适用：G: Transmit Idle 收到一个获准提出请求的参与者的显式请求；仲裁作出拒绝或授予；U: not permitted and Transmit Idle 收到仲裁的 Grant/Reject；或随后 U: permitted/G: Transmit Taken 收到各自的实际 RTP 指示。拒绝事件不预置已经授予。

G: Transmit Idle 的拒绝段列出仅一名客户端以及 on-network-recvonly 元素存在两项；拒绝时发送 Reject，分别使用 cause #3（Only one participant）或 #5（Receive only），可加原因文字，保持 G: Transmit Idle。原文连接词歧义见下述限制。若请求获准，则停止 T1、T2，保存获准参与者 SSRC，并进入 G: Transmit Taken：发送携获准优先级和参与者 SSRC 的 Grant，Cx 未达上限时加 1；向接收仲裁发送含发送者 SSRC、序列号加 1 的 Media Transmission Notify，未请求隐私时还带用户 ID，非广播时可带 Permission to Request=1，并启动一般接收控制实例。T4/C4 的启动只写给已排队请求，不移植到本页未排队分支。U 转发 Grant 后进入 U: permitted；转发 Reject 则仍为 U: not permitted and Transmit Idle。U: permitted 收到实际带载荷 RTP 指示时才要求网络媒体接口送到 media distributor；G 收到 distributor 关于获准客户端实际 RTP 的指示时，停止正在运行的 T4，并按本地策略和接收控制状态要求转发，仍为 G: Transmit Taken。

强度：上述条件动作及状态转换为 SHALL；Reject 原因文字、非广播 Permission to Request=1，以及接口为 Grant/Reject 请求 Ack 为 MAY。

- §6.3.4.3.3 先写 one of the following conditions，随后两项以 and 连接。本页保留该差异，不选择 OR/AND 实现，也不声称这是一份可直接执行的完整准入策略。recvonly 按元素存在，而非自行补 true 值守卫；配置 schema、缺省值及权限来源未展开。
- Grant/Reject 接口可以设置请求 Ack 的 subtype 首位；是否处理收到 Ack、未收到时如何处理是原文保留的实现选项。Ack 不是用户确认、媒体到达或接收呈现。
- Cx 的增减上下限条件来自程序正文；本页不赋予具体上下限值，也不把计数器表中的其他计数器值借给 Cx。请求优先级协商不等于完整竞争策略。
- Grant 消息中的获准参与者 SSRC 与消息头服务器 SSRC 不同。通知接收仲裁或要求转发不证明所有成员已收到或呈现视频；本页没有组接收客户端算法，也不以私呼接收页代替。
- §6.3.4.4.2 的通知要求消息序列号加 1，但 §9.2.13 的消息布局及字段说明未列 Message Sequence Number。本页记录内部程序义务，不据此补一份完整线上通知编码。

依据：TS24.581 V16.9.0 §6.3.4.3.3, 6.3.4.4.1–2;6.3.4.4.5, 6.3.5.3.5–6, 6.3.5.5.1–2;6.3.5.5.6, 9.2.2.1;9.2.5;9.2.6.2, 11.1.3 T4;11.2.3 (timer/counter boundary), 14.3.3 (priority dependency), 9.2.13 (notification layout comparison only)，印刷页 57, 58, 59, 69, 70, 78, 79, 145, 146, 157, 158, 159, 160, 161, 167, 168, 208, 212, 225。

### 未获准时的 End 与已获准后的 End 不能合并

适用：以下是替代入口：U: not permitted and Transmit Idle 收到关联参与者的 End Request；U: permitted 收到 End Request；G: Transmit Taken 收到 End Request；或 U: permitted 收到服务器 End Response。各动作只继承自己的状态和事件，不要求四者同时成立。

在 U: not permitted and Transmit Idle，收到 End Request 后按其 Ack 请求位决定是否发送控制 Ack，然后发送序列号加 1 的 Idle，按收到的 SSRC 检查排队请求并在存在时移除，仍留在该无许可状态。在 U: permitted，收到 End Request 后同样按请求位发送 Ack，再把 End Request 的 Ack 请求位置 0 转交一般传输仲裁，接口此时仍为 U: permitted。G: Transmit Taken 收到 End Request 时，Cx 未达下限则减 1，要求 distributor 停止转发该请求者的 RTP，停止正在运行的 T4，发送 End Response；仅 Cx 达到下限时进入 G: Transmit Idle。U 收到 End Response 后转发给参与者，才进入 U: not permitted and Transmit Idle。

强度：按各事件守卫的 Ack、转交、停止、响应和状态动作均为 SHALL；无许可分支发出的 Idle 可请求 Ack，相关 Ack 处理仍为实现选项。

- 无许可分支仍有检查队列/存在才删除的程序义务；它不证明本页未协商排队的参与者实际有排队项，也不把取消解释为曾获准。
- §6.3.5.3.7 与 .5.3 要求 Ack 的 Message Type=4、Source=2；§9.2.2.1-3 的 End Request subtype 为 x0000，而 §9.2.3.10 又按被确认消息的 subtype（含 Ack 位）描述 Message Type。这里只保留程序数值与格式定义的接口差异，不构造统一编码修正规则。
- 进入 G: Transmit Idle 后的群发 Idle、T1/T2/C2 和 Cx=0 动作由 §6.3.4.3.2 的非 Start-stop 入口、无客户端协商排队及空队列等守卫约束，不是每次创建 G 实例都自动执行。本页不展开计时器到期策略、丢包恢复或未授权 RTP 撤销路径。
- End Response 和停止该发送者转发不等于 SIP 呼叫已释放、全部接收者已清理或完整会话资源已回收。
- §6.3.5.3.7 可为 Idle 请求 Ack，而表 9.2.2.1-2 将 Idle subtype 列为 01111、未以 x 标示可选 Ack 位；本页不替原文选择位编码。

依据：TS24.581 V16.9.0 §6.3.5.3.7, 6.3.5.5.3–3a, 6.3.4.4.6;6.3.4.3.2, 9.2.2.1 table9.2.2.1-3;9.2.3.10;9.2.3.12 (Ack comparison), 9.2.20–21;9.2.30–31，印刷页 56, 57, 59, 70, 78, 146, 151, 152, 172, 173, 174, 179, 180, 181。

### 应用释放是另外两个事件，不是 End 的同义步骤

适用：关联参与者的基本接口在非 Start-stop、非 Releasing 状态收到应用/信令面 call release step1；或该接口已在 Releasing 状态收到 step2。两事件分别适用，不要求 step1 时已完成 step2。

收到 step1 的基本接口停止向该参与者发送传输控制消息，要求停止向该客户端发送 RTP，并停止把该客户端来的 RTP 转交 distributor；忽略该参与者随后来的控制消息，通知一般仲裁该客户端已开始断开，然后进入 Releasing。收到 step2 时，要求释放该客户端在该呼叫的网络媒体资源，回到 Start-stop 并终止该参与者对应的基本传输控制实例。

强度：所述条件停止、忽略、通知、资源请求和状态动作均为 SHALL。

- 这里是基本接口对应用/信令面两个事件的职责，不是产生 SIP BYE、判断会话已释放或全体成员退出的完整算法。整体呼叫的一般实例及接收实例释放另有 §6.3.3 的范围，不由一个参与者 step2 推出全部终止。

依据：TS24.581 V16.9.0 §6.3.5.8.1–2;6.3.5.9.1–2, 6.3.3 (whole-call comparison)，印刷页 53, 54, 83, 84。

## 共同依赖与边界

- 这是按实际状态事件划分的服务器职责，不是从 SIP 建立直到全员媒体结束的完整实现。G 的初始化和授权策略、完整排队/竞争/抢占、撤销和异常 RTP、接收仲裁、客户端确认与呈现、传输可靠性和完整安全实现均未闭合。
- 只引用 TS24.581 本版实际接口，不用 Stage 2 功能职责或别的 Release 补程序。关联组建立页只提供其自身的信令事件边界；私呼传输/接收客户端页的共同条件不适用于本组呼。

共同依据：TS24.581 V16.9.0 §5.3;6.1, 6.3.1–3, 13.3.4 steps1–2 (protection dependency only), 14.2.2;14.3.1–2 (queue negotiation boundary)，印刷页 32, 33, 52, 53, 54, 222, 224, 225。

## 条件关联

- [预安排组呼客户端建立与应答](prearranged-group-client-establishment.md)：只在需要核对其初始信令事件时阅读；信令成功不替代本页媒体状态和许可条件。
