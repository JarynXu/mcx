# 在网 MCVideo 客户端：请求传输、获准与结束

## 适用范围

- 固定 TS24.581 V16.9.0；信令入口只按 TS24.281 V16.12.0。范围为普通在网、带传输控制、按需一对一私呼的客户端 transmission participant；不含广播、组呼、系统/紧急/危急、ambient、远程推拉或离网。
- 媒体控制通道已按本次会话的 SDP 协商建立，适用的信令准入和媒体保护义务仍须执行；本页不以已获传输许可或已传送媒体作为共同前提。各条按客户端实际状态和事件分别适用，不要求这些事件全部发生。
- 覆盖终接初始化、显式请求、非排队响应、待请求收到排队信息后进入的队列分支及普通结束。各状态的条件只约束对应事件，排队后的获准须另满足用户确认才能开始发送媒体；不把此要求套给非排队获准。Transmission Revoked 的撤权或转队列入口、接收控制与服务端仲裁不在本页。

## 终接方发送 SIP 200 后仍处于无传输许可状态

条件：普通私呼终接客户端已按实际 Auto/Manual 入口处理邀请并发送 INVITE 的 SIP 200；本条不处理拒绝或尚未应答的邀请。

TS24.281 的自动私呼 helper 发送 200 后调用媒体面，手动 helper 在发送最终 200 时调用同一 helper。TS24.581 为此呼叫创建传输状态实例；终接方在呼叫建立时进入 U: has no permission to transmit，且其建立事件以应用与信令面发送 SIP 200 为准。收到用户请求发送媒体的指示后，在该无许可状态向传输控制服务器发送 Transmission Request，启动 T100、将 C100 置 1，进入 U: pending request to transmit。

强度：所述调用、状态、请求及计时动作是 SHALL；终接建立时点的解释来自 NOTE。

- Auto/Manual 的真实选择条件及安全检查仍由信令入口负责，不能把本页当成绕过准入的入口。
- 这里的 SIP 200 不带来终接方发送许可。主叫的 implicit request、早到消息缓存及 mc_granted SDP 分支不是本页的初始化算法；不从终接规则补普通主叫未协商 implicit 的初始状态。
- 按 §6.2.4.3.2，若要求不同于普通优先级，请求须携不高于协商上限的 Transmission Priority。本页只取普通优先级，不展开该协商算法。

依据：3gpp-ts-24.581-v16.9.0 §6.2.1；6.2.4.2.3；6.2.4.3.1–2，印刷页 33,36,37；3gpp-ts-24.281-v16.12.0 §10.2.2.2.2 steps7–8 (actual mode caller)；6.2.3.1.1 steps8–10；6.2.3.2.1 final-200 paragraph，印刷页 44,45,270,271。

## 待请求状态区分拒绝、重试和获准

条件：客户端处于 U: pending request to transmit，分别发生收到 Transmission Rejected、T100 到期或收到服务器 Transmission Granted；本条不取排队状态的 Granted 分支。

拒绝时按需发送 Transmission control Ack，通知用户请求被拒，可显示 Reject Cause 的原因，停止 T100 并回到无许可状态。T100 到期且未达 C100 上限时重发请求、重启 T100、C100 加 1 并留在待请求状态；达到上限则通知超时并回到无许可状态。收到 Granted 时按需 Ack，保存获准参与者的 SSRC 并在本次传输释放前用于 RTP，若尚未通知则通知用户获准，停止 T100，进入 U: has permission to transmit。在该获准状态，只有收到客户端关于用户编码视频到达或已有编码视频缓存的指示时，才请求客户端开始向服务器转发，并保持该状态。

强度：所述状态、计时、通知、SSRC 和转发请求为 SHALL；拒绝原因展示为 MAY。

- 按需 Ack 的守卫是收到消息的 subtype 首位为 1；过程写拒绝的 Message Type=1、Granted=0，Source=0。§9.2.3.10 又把 Message Type 定义为包含首位的五位 subtype 前补 000，和过程所列固定数值存在编码解释差异，本页不裁决或提供完整编码器。
- Granted 是许可，编码视频可用是另一个事件；两者均不证明其他用户已接收、呈现或获接收许可。
- T100 值取配置；§11.1.1 NOTE1 建议请求重传总时段小于 6 秒，并非 T100 固定为 6 秒。§11.2.1 列 C100 默认值 3；不从默认值擅定所有部署参数。排队信息及其后续确认不在本条。

依据：3gpp-ts-24.581-v16.9.0 §6.2.4.4.1–4；6.2.4.4.6；6.2.4.5.1–2；9.2.2.1；9.2.3.10；9.2.3.12；9.2.5 (message meaning/SSRC)；9.2.31；11.1.1 T100 and NOTE1；11.2.1 C100，印刷页 37,38,39,145,146,151,152,157,158,180,181,199,201,202,210,211。

## 用户结束请求不等于通话释放

条件：替代事件：待请求状态中的用户取消传输请求；已获许可状态中的用户结束发送许可；待结束状态中的 T101 到期或收到 Transmission End Response。

用户在待请求状态结束请求时发送 Transmission End Request，停止 T100，启动 T101、C101 置 1，进入 U: pending end of transmission；在已获许可状态结束许可时也发送 End Request、启动 T101、C101 置 1 并进入待结束状态。待结束时 T101 未达 C101 上限就重发 End Request、重启 T101、计数加 1 并保持状态；到上限则回到无许可状态。收到 End Response 时，若 subtype 首位为 1 则发送 Ack（过程列 Message Type=1、Source=0），可向用户通知结束，停止 T101；普通非广播会话回到无许可状态。

强度：所述发送、计时、Ack 和状态动作是 SHALL；结束通知为 MAY。

- 已获许可方即使尚未发送任何媒体，也可释放许可。§6.2.4.5.3 的用户结束步骤未另写立即丢弃缓存或停止 RTP，不能将下条服务器命令中的显式停止动作移入；也不能据此声称必须持续发送。
- 回到无许可状态不是 SIP 会话已释放，也不是服务器已处理成功的证明；尤其本地 T101 达上限不等于收到服务器确认。
- T101 值取配置；§11.1.1 NOTE2 建议结束请求重传总时段小于 6 秒，§11.2.1 列 C101 默认值 3。End Response 的 Ack 同样保留 Message Type 固定值与通用编码定义的差异。

依据：3gpp-ts-24.581-v16.9.0 §6.2.4.4.7；6.2.4.5.1；6.2.4.5.3；6.2.4.6.1–4；9.2.20–21 (message direction/format comparison)；9.2.3.10；9.2.31；11.1.1 T101 and NOTE2；11.2.1 C101，印刷页 38,39,40,41,151,172,173,174,180,181,199,201,202,210,211。

## 服务器停止命令与通话释放是不同事件

条件：替代事件：已获许可状态收到服务器 Transmission End Request；或适用状态收到应用与信令面的 call release step1；或 Call releasing 状态收到 step2。

在已获许可状态收到服务器 End Request，客户端通知用户许可正被撤销，可说明原因，要求丢弃剩余 RTP 缓存并停止向服务器转发编码视频，发送 End Response；普通非广播会话回到无许可状态。收到 call release step1 时则停止传输控制消息，要求停止发送 RTP，进入 Call releasing；等应用与信令面确认释放并发 step2，才释放全部资源（包括运行中的计时器）、回到 Start-stop 并终止当前状态实例。

强度：所述停止、响应、状态与清理是 SHALL；说明终止原因是 MAY。

- step1 的通用状态入口不包括 Start-stop 和 Call releasing；step2 不能提前用于单纯传输结束。用户面可发起释放第一步，但第二步始终由应用与信令面发起。
- 本页只登记媒体面两步释放界面，不证明 SIP BYE/CANCEL 全链完成；Transmission Revoked 的终止或排队原因分支不在本页。
- 对当前状态无具体处理程序的传输控制消息须丢弃并保持状态；格式错误消息也不改变状态。不能把任意到达的 Granted 或 End Response 当作跨状态通行证。

依据：3gpp-ts-24.581-v16.9.0 §6.2.4.5.7；6.2.2；6.2.4.7.1–2；6.2.4.8.1–2；6.2.4.1 unmatched/malformed message rule，印刷页 34,35,40,41,42。

## 进入队列与查询位置不是获准发送

条件：替代事件：U: pending request to transmit 收到 Queue Position Info；或由该入口进入的 U: queued transmission 收到位置查询指示、Queue Position Info、未达 C102 上限的 T102 到期。各守卫只约束对应事件。

待请求收到 Queue Position Info 后，若 subtype 首位为1则发送 Ack（过程列 Message Type=5、Source=0），须通知用户请求已排队，可提供位置与优先级，并进入 U: queued transmission。队列中客户端指示查询时发送 Queue Position Request，启动 T102、C102 置1并保持排队。收到 Queue Position Info 时按同一守卫 Ack；若消息指明请求已排队，或此前发送过位置查询，则可向用户提供可用的位置与优先级；停止仍运行的 T102并保持排队。T102 到期且未达 C102 上限时重发位置请求、重启 T102、C102 加1并保持排队。

强度：消息、通知、计时器与状态动作按正文 SHALL；位置/优先级展示为 MAY。

- §11.1.1 的 T100 表将 Queue Position Info 接收列为正常停止事件；§6.2.4.4.5 的逐步程序没有重列停止 T100。本页同时保留两处表述，不据省略推定继续重传，也不拼接一套原文未给的调度算法。
- Queue Info 的位置值254表示未排队，255表示已排队但位置因服务器策略未给出或未知；收到这些值不等于 Granted。队列中 §6.2.4.9.2 仍规定保持排队，不自行增设254立即退出的动作。
- 在网 Queue Position Request/Info 仅用于单播承载；请求的 SSRC 是查询参与者，Info 的首部 SSRC 是服务器。消息图中 User ID、queued participant SSRC 和 Queued User ID 的相关字段仅用于离网，不能移植到本页。涉及 non-controlling function 才按定义带 Track Info；本页不实现完整路由和编码。
- T102 取服务配置，C102 默认上限为3，不把默认值当固定部署值。§9.2.11 的文字回指 Table8.2.11-1，但实际图表标号为9.2.11-1；保留该差异。Ack 的过程固定值与 §9.2.3.10 通用五位 subtype 编码定义差异仍不裁决。

依据：3gpp-ts-24.581-v16.9.0 §6.2.4.4.5；6.2.4.9.1–3；6.2.4.9.7；9.2.2.1；9.2.3.5；9.2.3.10；9.2.11–12；11.1.1 T100/T102；11.2.1 C102，印刷页 38,42,43,145,146,149,151,165,166,167,201,211。

## 排队后的 Granted 先改变许可状态，发媒体还需确认

条件：由待请求的 Queue Position Info 入口进入 U: queued transmission 后，收到服务器 Transmission Granted；以及其后在获准状态的用户确认和编码视频可用事件，不要求获准前已有媒体。

收到 Granted 时，若 subtype 首位为1则发送 Ack（过程列 Message Type=0、Source=0），保存获准参与者 SSRC 并在本次传输释放前用于 RTP；若尚未通知则通知用户获准，停止 T102，进入 U: has permission to transmit。§6.2.4.5.1 NOTE 要求曾排队的参与者在开始发送媒体前请求用户确认：确认才开始发送，否则释放发送许可。编码视频到达或已有缓存仍是 §6.2.4.5.2 请求客户端转发视频的另一个事件；Granted 本身不能证明已有可转发媒体或其他用户已收到。

强度：Granted 的 Ack、保存、通知、计时与状态为 SHALL；发送前用户确认来自 §6.2.4.5.1 NOTE，媒体可用事件下的转发请求为 SHALL。

- 原文先进入 has permission，再约束开始发送前的用户确认；没有给出本页可据以实现的确认计时器或独立确认状态，不套用 MCPTT 的 T132。未确认时释放许可的 NOTE 不在此被扩写为未给出的自动消息/超时算法。
- 非排队获准的条件仍按前述独立小节，不把排队确认设成全部 Granted 的共同门槛。用户确认、发送许可、编码视频可用、对端接收/呈现分别是不同证据。

依据：3gpp-ts-24.581-v16.9.0 §6.2.4.9.9；6.2.4.5.1 NOTE;6.2.4.5.2–3；9.2.5；9.2.3.10;9.2.3.12，印刷页 39,43,151,152,157,158。

## 主动撤回、服务器取消和查询超时分别处理

条件：由待请求的 Queue Position Info 入口进入 U: queued transmission 后，分别发生客户端取消队列请求、收到 Transmission Cancel Request Notify，或 T102 达 C102 上限到期；不将三事件合取。

客户端取消队列请求时发送 Transmission End Request，启动 T101、C101 初始化为1，进入 U: pending end of transmission。服务器 Cancel Request Notify 到达时，若 subtype 首位为1则 Ack（过程列 Message Type=10、Source=0），直接进入 U: has no permission to transmit。T102 达 C102 上限到期时，§6.2.4.9.8 正文要求通知客户端排队超时，发送 End Request，启动 T101、将 C101 增加1，并进入 pending end of transmission；此处不是把 C101 初始化为1。待结束状态的响应和 T101 处理仍按本页对应状态小节，不代表 SIP 通话已释放。

强度：取消与通知处理的相应动作是 SHALL；§6.2.4.9.8 的发送步骤为原文操作指令，其他计时/状态步骤为 SHALL。

- Figure6.2.4.1-1（p35）把 queued 的 Timer T102 exp. N times 箭头画到 has no permission；§6.2.4.9.8（p43）正文却经 End Request/T101 到 pending end。图与正文的目的状态差异保留，不合成或裁决为实现算法。
- 主动取消的 C101 初始化为1与查询到限的 C101 增加1是不同原文操作；§11.2.1 表给出默认上限及达到上限后的停止重传行为，没有 increment 栏，不能从表格编造另一增值事件或消除正文差别。
- §6.2.4.9.4/.6 没有重列停止 T102；T102 表明确列 Queue Position Info 及因 Granted 离开队列的正常停止。本页不为其他退出补通用停止算法。Cancel Request Notify 的直接无许可不需先等 End Response，也不证明全会话释放。

依据：3gpp-ts-24.581-v16.9.0 §6.2.4.9.4;6.2.4.9.6;6.2.4.9.8；6.2.4.1 Figure6.2.4.1-1 (comparison)；6.2.4.6.1–4 (pending-end interface)；9.2.19–21；9.2.3.10；11.1.1 T101/T102；11.2.1 C101/C102，印刷页 35,40,41,42,43,151,172,173,174,201,211。

## 边界与关联

- 本页说明客户端有限传输控制责任，未展开服务端准入/仲裁、队列调度/抢占、接收控制、MBMS、完整报文编解码、媒体呈现或端到端交付。
- §4.3 的控制通道是 UDP/IP 上的 RTCP APP，经 SDP offer/answer 协商；该节将具体编码回指 clause8，而实际消息章节是 clause9。本页保留回指，不自行修订。
- 适用的 §6.1/§13 媒体保护仍须执行；普通私呼 PCK 媒体保护与 CSK 控制消息保护有不同条件，不能由传输许可替代。TS33.180、TS24.484 配置、RFC 和完整密钥/编码实现未在本页验证。
- §14.3.4 允许在满足条件时通过带 mc_granted 的 SIP200 指示 implicit 请求获准；因此不能泛称所有 SIP200 都与许可无关。本页不覆盖这个 SDP 授权分支，也不以普通无该证据的 200 当授权。

补充依据：3gpp-ts-24.581-v16.9.0 §4.3.1–3；5.2.1；6.1；6.2.4.2.2 (originating comparison only)；13.3.3 item3 (private security dependency)；14.3.4–5 (implicit grant comparison only)，印刷页 30,31,33,36,220,225；3gpp-ts-24.281-v16.12.0 §6.4 (implicit request comparison only)；6.2.2 step5 (control SDP dependency)，印刷页 44,107。

若需先判断普通按需私呼的客户端应答入口，且符合其条件，参阅[客户端请求与应答证据](private-client-answer-evidence.md)。该关联不保证邀请获准、媒体控制通道已协商或用户已获发送许可。
