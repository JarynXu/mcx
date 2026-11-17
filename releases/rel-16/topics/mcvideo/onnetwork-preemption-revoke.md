# 普通在网组显式抢占：满容量撤销、等待与 End 证据

## 适用范围

- 固定 TS24.581 V16.9.0、Rel16 Stage 3；普通在网预安排组、非临时组。只解释已建立控制状态中的显式请求、撤销等待与实际 End 事件，不含广播、系统、紧急/危急升级、离网或完整初始化。
- 请求者 U、G 仲裁逻辑、旧发送者 U 以及客户端分别按各条实际状态和输入进入。满容量与 pre-emptive 只限定相应请求分支，不是后续 RTP、计时和结束事件的附加守卫；不要求撤销或交接已成功。
- 保护仍按角色和协商适用：控制功能在媒体保护已协商时透明转发加密 RTP；普通组控制消息保护已协商且 SPK/SPK-ID 已配置时，须依 §13.2、13.3.4 step2 使用派生材料。客户端对应组媒体保护以已协商且已取得 GMK/GMK-ID 为条件；单播控制保护以已协商且 CSK/CSK-ID 已送参与功能为条件，依 §13.3.3 step1 执行。这里不证明配置、密钥分发或跨功能安全路径已经完成。

共同依据：
- TS24.581 V16.9.0 §6.1;6.3.4.4.1;6.3.4.5.1;6.3.5.5.1;6.3.5.6.1; 13.2;13.3.3 step1;13.3.4 steps1–2 (protection dependency)；印刷页 33, 58, 62, 78, 80, 216, 218, 219, 222。

## 请求先经 U 的协商与策略条件，数字优先级不等于抢占许可

条件：请求者侧实际处于 U: not permitted and Transmit Taken，收到关联参与者的显式 Transmission Media Request；普通调用不带 Indicator 或 D/E 均为 0。按实际 queue/priority 协商、有效优先级和容量分别判分支，不预设可转交。

§6.3.5.4.4 首段以未协商 queue OR 未带 mc_priority 为条件：Cx 已满则发 Reject cause #1 并保持状态；未满调用 §6.3.4.4.7A。后段以已协商 queue OR 带 mc_priority（或两者）及本地策略为条件，按 §4.1.1.4 计算有效优先级：已协商且请求带优先级时取请求值与协商上限较低者；receive-only、缺请求字段或未协商时各用正文对应值。有效 receive-only 发 cause #5 并保持状态。按请求 SSRC 检查已有排队项；同有效优先级项在已协商 queue 时回 Queue Position Info，保持状态。实际转交抢占要求有效优先级为 pre-emptive、队列无其他 pre-emptive 请求且当前获准客户端非 pre-emptive，U 转交 G 并仍未获准。未协商 queue 且另一抢占请求已排队或当前获准者也为 pre-emptive 时，满容量拒绝 cause #1，未满调用非抢占 helper；不因请求声称高优先级直接发送媒体。

规范强度：上述条件动作与状态为 SHALL；拒绝说明文字及指定 Ack 请求位为 MAY；有效优先级的政策选择依 §4.1.1.4。

限制：
- 首段 no-queue OR no-priority 与后段 queue OR priority 在仅协商一项时重叠，原文没有在这里提供互斥调度；不能改成一套 if/else。receive-only 与同优先级排队项后的正文也未写统一 return，不补后续执行或停止算法。
- 有效优先级依本地策略、配置、协商及调用类型，不是数值高就可抢占。§14.3.3 对 recvonly 元素存在要求 answer 不含 mc_priority，非 recvonly 才取 offer、user-priority、num-levels-priority-hierarchy 最小值；本页不补配置获取或缺省 schema。
- 未协商 queue 的非抢占请求同样按容量拒绝或调用 §6.3.4.4.7A；已协商 queue 的非抢占满容量请求按同有效优先级之后插入/更新并回位置。本页不重建完整队列策略。§6.3.4.4.7A 的 one of 与列项末尾 and、条件 granted 保留，不把“未拒绝”改成必授予。

依据：
- TS24.581 V16.9.0 §4.1.1.4;6.3.2.2 priority/queue paragraphs; 6.3.5.4.4 (full actual caller);6.3.4.4.7A (alternative caller dependency); 14.2.2–3;14.3.1–3 (negotiation dependency); 9.2.3.2;9.2.3.11 (priority/normal-call comparison)；印刷页 21, 53, 60, 72, 73, 74, 75, 148, 151, 152, 224, 225。

## 满容量时撤销与置队首，不是立即给新请求发送许可

条件：G 实际处于 Transmit Taken，收到有效优先级为 pre-emptive 的显式请求。未满与满容量是替代分支；满容量还须满足正文关于已获准 transmission participants 非 pre-emptive 的条件及本地策略。

§6.3.4.4.7 未满时调用 Taken 入口。满容量的规定分支按本地策略选择一个无 pre-emptive 优先级的获准参与者撤销，停止正在运行的 T4，以 cause #4 构造 Revoke 并进入 G: pending Transmission Revoke。将新请求插入队首或把已有请求移至队首；仅 Queue Position Info 的发送另以已协商 queue 为守卫。G pending 入口发送带撤销原因的 Revoke 并设置状态，不在该分支直接发送新请求的 Grant。

规范强度：停止计时、原因构造、状态、队首操作及条件位置通知为 SHALL；被撤销者的选择按本地策略。

限制：
- U 转交条件写 current MCVideo client 单数，G 条件写已获准 transmission participants 复数。本页不把“找到一个非抢占者”改作整个集合守卫，也不代定多发送者量词。
- 置队首本身未带“已协商 queue”守卫；不能因为没有位置通知就删掉队首操作，也不能把位置通知当 Grant。Cx 的容量上限与有效优先级政策仍须外部配置，§11.2.3 表没有 Cx 行，不能借接收侧 C7/C9/C11 或 C4 的数值代替。
- 同一 pending 还可由 §6.3.4.4.13 的服务器 End Request/cause #8 进入；它与本页 cause #4 的显式抢占入口不同。§6.3.4.4.12 的紧急 implicit 仅作范围对照，不能反向用于补本页条件。

依据：
- TS24.581 V16.9.0 §6.3.4.4.7;6.3.4.5.1–2; 6.3.4.4.1–2 (Taken helper); 6.3.4.4.12–13 (entry comparison only); 9.2.10 (Revoke meaning/cause);9.2.3.5;9.2.12 (queue meaning comparison); 11.2.3 table11.2.3-1 (Cx absence/C4 versus reception counters comparison)；印刷页 58, 59, 60, 61, 62, 149, 164, 165, 166, 167, 212。

## 撤销等待仍可转发旧 RTP，cause #4 的客户端后续不能擅补

条件：旧发送者侧 U: permitted 实际收到 G 的 Revoke，或 U/G 已在各自 pending 状态收到旧 RTP/T3 到期；客户端则须实际处于 has permission to transmit 并收到 Revoked。各角色事件替代适用，不要求同时发生。

U 转发 Revoke 给关联参与者，进入 pending 并启动 T3。T3 到期重发保持相同原因和 Indicator 的 Revoke/End Request，重启 T3 并保持等待；重发次数及放弃动作是实现选项，注记建议放弃时断开客户端。U pending 仍把旧 RTP 转给 media distributor，G pending 仍按本地策略转发获准参与者的 RTP，发送 Revoke 因而不证明旧流已停止。客户端实际收到 Revoked 时须通知撤销、要求丢弃剩余缓存并停止编码视频转发，可说明原因；只有原因是 terminate RTP stream 时才明示进入 pending end、发 End Request 并启动 T101/C101=1，原因是 queue transmission 时才明示进入 queued、发 Queue Position Request 并启动 T102/C102=1。

规范强度：转发、重发、停止客户端向服务器转发编码视频与条件状态/计时为 SHALL；用户原因说明为 MAY；放弃重发后的断开是注记建议，不是固定次数后的无条件动作。

限制：
- §9.2.10.2 分别列 cause #4 Media Burst preempted、#5 Terminate RTP stream、#7 Queue transmission。§6.3.4.4.7 发 #4，而 §6.2.4.5.5 只为 terminate/queue 写后续状态；没有把 #4 映射为 #5 或 #7 的明确规则。可确认客户端停止向服务器转发编码视频的职责，但不能据 #4 推定其必发 End Request、进入 queued 或闭合抢占回程。
- T3 表默认 1 秒、可配置，normal stop 字面为 Reception of Transmission Release；正文 §6.3.5.6.8 则在收到客户端 End Response 时明确停止 T3。本页保留消息名差异，不用表替正文增加停止事件。U pending 与 not permitted but sends media 是不同状态，后者不转发 RTP 的规则不能提前套入等待期。
- 客户端 T101/T102 的实际发送、到期与响应有各自条件。计数表 C101/C102 默认上限 3，没有 increment 栏；递增应看状态正文。T101 本地到限转无许可不证明服务器收到 End；queued 收到位置通知仍不等获准。本文不把这些计时规则用于填 cause #4 的映射缺口。
- 图6.3.4.1-1 含 T20/T7 等标签，正文和本版计时表使用 T4/T2 等；图6.2.4.1-1 的 Revoked 箭头不能替代正文的原因守卫。本页按实际事件条款说明有限责任，不从图重建一套统一计时或补全状态算法。

依据：
- TS24.581 V16.9.0 §6.3.5.5.5,10;6.3.5.6.1–4,8;6.3.4.5.1–3; 6.2.4.5.5;6.2.4.6.1–4;6.2.4.9.1–9 (conditional client dependency); 9.2.10.1–2 (cause mapping comparison); 11.1.3 table11.1.3-1 T3;11.1.1 table11.1.1-1 T101/T102;11.2.1 C101/C102; 6.3.5.7.1–3 (different-state comparison); 6.2.4.1 figure6.2.4.1-1;6.3.4.1 figure6.3.4.1-1;6.3.5.1 figure6.3.5.1-1 (diagram comparison only)；印刷页 35, 39, 40, 41, 42, 43, 55, 62, 63, 65, 79, 80, 81, 82, 164, 165, 200, 201, 207, 211。

## End 逐事件释放容量，取队首与后续媒体必须另取证

条件：G pending 实际收到 End Request 或 End Response；或旧发送者 U pending 收到客户端 End Request/Response、服务器 End Response/Idle/Notify。后续 Grant helper、请求者 U 或 queued 客户端只在实际相应调用/消息到达时适用，不以预期收到作前提。

G 收到 End Request 时停止该请求参与者的 RTP 转发，在 Cx 未到下限时减 1，并回 End Response；收到 End Response 时同样停对应流和有界减 Cx，但不另回一份响应。两条均在达到下限时调用 Idle；未到下限 AND 队列非空时才明确取出并移除队首、对该参与者进入 Taken。U 收到客户端 End Request 时按需 Ack、转 G 并仍 pending；收到服务器 End Response 则转发并进入 not permitted/Idle；收到客户端 End Response 则按需 Ack、停止正在运行的 T3、转 G 并进入 Idle。真正调用 Taken 入口才发送含获准优先级和 SSRC 的 Grant、按上限增 Cx，排队请求启动 T4/C4=1并通知接收仲裁。请求者 U 实际收到 Grant 才转发并进入 permitted；queued 客户端实际收到 Granted 才保存获准 SSRC、停 T102、进入有许可，且原先排队者发送媒体还须取得用户确认，编码媒体输入与实际 RTP 仍是另一事件。

规范强度：本条条件转发、计数、状态和 Grant 动作为 SHALL；指定 Ack 请求和接收 Notify 的 Permission-to-Request 为 MAY；排队者用户确认依客户端状态注记。

限制：
- 降到下限后引用的 §6.3.4.3.2 另有“从非 Start-stop 进入 AND 没有任何客户端协商 queue”的入口守卫：其空队列路径发 Idle、启动 T2/C2=1/T1、置 Cx=0；非空路径取队首进 Taken。不能抹掉守卫保证所有降到下限的抢占都自动授予队首。未到下限且空队列也不能补完整最终状态。
- U pending 收到 End Request、服务器 End Response 的条款未明示 stop T3，不能复制客户端 End Response 分支的 stop。实际 Idle 与 Notify 各有自己的转发/状态；§6.3.5.6.7 文字目标为 not permitted/Transmit Taken，却回指 §6.3.5.3.2 Idle，发送目的地也并列 participant 与 reception logic。本页不修号或补路由。
- T4 正文在排队请求时启动，表又写 queued 且 negotiated queue；表 normal stop 写 Sending RTP or losing permission，而 §6.3.4.4.5 是收到获准者 RTP 时 stop T4。T4 默认 1 秒、C4 默认上限 3，均可配置；到限正文保持 Taken、表停止 Grant 重发，不证明对端收到或媒体成功，也不补自动撤销。
- 接收侧通知、接收许可及显示有独立状态。本页不保证全组交付、重排公平性、完整队列/配置/安全算法或呼叫释放完成。SIP 200、请求入队、Revoke、End、Grant 和 RTP 不可合并为同一个成功证据。

依据：
- TS24.581 V16.9.0 §6.3.4.5.4,7;6.3.4.3.2 (full Idle caller guard); 6.3.5.6.5–8;6.3.5.3.2 (state-reference comparison); 6.3.4.4.2,5,9–10;6.3.5.4.9;6.3.5.5.1–2 (actual Grant path); 6.2.4.9.9;6.2.4.5.1–2 (queued user confirmation/media dependency); 11.1.3 table11.1.3-1 T4;11.2.3 table11.2.3-1 C4 (table/body comparison)；印刷页 39, 43, 56, 57, 58, 59, 61, 63, 68, 69, 77, 78, 80, 81, 82, 208, 212。

## 使用边界

- 本页只提供已建立 G/U 状态中的有限事件责任，不是端到端可执行的抢占闭环。原因映射、集合条件、原文回指和表/正文粒度差异均保留，不能用本页消除这些接口缺口。
- 普通非抢占服务器与接收服务器仅按各自状态/事件作关联阅读；私呼客户端、离网 single 或 MCPTT 算法不能替代这里的组调用条件。外部配置 schema、RFC 和密码规范不在本页完成核验。

## 条件化关联

- [普通组传输服务器](prearranged-group-transmission-server.md)：仅对其普通 Idle/非抢占事件，不作为本页满容量抢占的必经前置。
- [普通组接收服务器](prearranged-group-reception-server.md)：仅在实际接收侧输入和状态满足时使用，不以发送 Grant 保证接收或显示。
