# 在网单话权：显式抢占请求与撤销事件责任

## 适用范围

- 固定TS24.380 V16.9.0；已建立在网按需会话的单话权控制，以显式Floor Request及本地策略选择撤销为主。广播、ambient、system、临时组、audio-cut-in、dual和multi-talker不作为主流程；紧急/迫近危险指示仅按实际请求准入条件处理，implicit升级只作比较。
- 从已有G Taken、请求者U not permitted and Floor Taken及原持有者U permitted的相应事件开始；后续pending状态只适用于已进入该状态的角色。不提供初始化、完整授权政策、排队推进或完整通话释放算法。
- 各角色与消息/超时事件分别适用。请求失败、无queueing、尚未撤销及未收到Release均可落入对应条款，不以成功条件排除拒绝或超时。会话协商和适用媒体保护仍是独立依赖。

## 请求者 U 先处理准入与队列，优先级不是发送许可

条件：本次为已建立在网会话中的显式 Floor Request；关联请求者的服务器 U 处于 not permitted and Floor Taken。各拒绝、重复请求、转交和排队分支按自己的条件适用，不以已获准或已协商 queueing 作为共同前提。

非 multi-talker 时，若（请求无 Floor Indicator，或其中 D/E 均为0），并且（客户端未协商 queueing，或未在 mc_priority 中包含优先级），U 须发 cause1 Deny 并仍留 Taken。另一独立段在已协商 queueing 或包含 mc_priority 或两者均有、并按本地策略时，计算有效优先级：已协商且请求含值时取请求值与协商上限较小者；协商上限为 receive only 时采用 receive-only 优先级；已协商但非 receive-only 且请求缺值，或未协商优先级时，采用默认优先级。D=1 判 emergency，E=1 判 imminent peril；缺字段或两者均非1判 normal。有效优先级为 receive only 须发 cause5 Deny并保持 Taken。检查已有队列项时，有 Track Info 使用最上层 Participant Reference 加请求 SSRC，否则使用 SSRC。已有相同有效优先级的排队请求时，仅在已协商 queueing 时发送 Queue Position Info，并仍留 Taken。只有有效优先级是 pre-emptive、活动队列没有其他 pre-emptive 请求且当前持有者不是 pre-emptive 时，step5 才转交 G 并保持 Taken。未协商 queueing，且抢占请求遇其他抢占排队或抢占持有者时，step6 发 cause1 Deny；未协商 queueing且非抢占时，step7同样拒绝。已协商 queueing且非抢占时，step8 插入或更新到所有同有效优先级请求之后，发 Queue Position Info，仍留 Taken。Deny 的适用分支条件复制请求 Track Info，可附 Reject Phrase；Queue Info含位置与优先级。

强度：上述条件处理、转交、队列更新、发送和状态保持为 SHALL；Reject Phrase及相应分支请求ACK为 MAY。

- 原文的拒绝段使用“未协商 queueing OR 未含 mc_priority”，后续处理段使用“queueing OR mc_priority OR both”。例如只满足其中一种协商时，两段可能同时适用；本页不改成互斥 if/else，也不给重复输出定义先后或消歧政策。
- Floor Priority为0至255，缺字段默认0；是否抢占由有效优先级与本地策略决定，不等于数值高或紧急类型便必获准。§4.1.1.4还列用户优先级、层级数、参与者类型、当前持有者等输入，配置来源不是本页完整政策。
- §8.2.3.15 NOTE1称C/D/E仅informative、本Release未定义相应procedure；§6.3.5.4.4却实际使用D/E分类。保留两处差异，不用注抹掉正文或用正文改写注。Floor Indicator可同时置多位，组合及优先级由本地策略决定。
- Queue Info位置254表示未排队；255表示已排队但位置未知或策略不披露。Queue Position Info不是 Granted。Request和队列消息中的离网专用User ID、Queued User ID及queued SSRC不能直接套入在网。广播/ambient的cause5段，以及audio-cut-in、multi-talker入口仅作范围对照。

依据：3gpp-ts-24.380-v16.9.0 §4.1.1.4；§6.3.5.4.4 full (audio-cut-in/multi/broadcast/ambient comparison included)；§8.2.3.2;8.2.3.4–5;8.2.3.13;8.2.3.15；§8.2.4;8.2.12；§14.1–3，印刷页 21,78,79,80,81,149,150,151,154,155,156,161,162,172,173,237,238,239。

## 非持有者撤回排队：收到 Floor Ack 和 Floor Taken，能确认已移出队列吗？

**不能。** 甲有发媒体的许可，乙没有。乙发 Floor Release 撤回排队请求，不是在释放甲的话权。这里看的是**控制服务器面向乙的接口**，它在 `U: not permitted and Floor Taken` 状态收到关联参与者的 Release。例子只取已协商支持排队、未在 `mc_priority` 中包含话权优先级的普通单话权。无需先出现抢占、撤销，也不要求甲已经发出 RTP。[3GPP TS 24.380 V16.9.0，Release 16，Stage 3，§6.3.5.4.1，印刷页 77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)；[§8.2.7 开头，印刷页 165](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=166)。

1. **按条件回确认，再查队列。** Release 的 subtype 首位为 1 时，服务器须先发 Floor Ack，`Message Type=4`（Floor Release），`Source=2`（控制 MCPTT 功能）。查找用的是收到的 Release：有 `Track Info`，取最上层的 `Participant Reference` 和该消息的 `SSRC` 一起匹配；没有 `Track Info`，只用该消息的 `SSRC`。该关联客户端在活动话权请求队列中才移出。这是服务器程序的先后，不是网络送达顺序。[§6.3.5.4.5 已协商排队段，第 1–3 项，印刷页 82](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=83)。
2. **查到或没查到，都给乙这一侧发 Floor Taken。** `Granted Party’s Identity` 填获准者甲的 MCPTT ID，消息序号递增 1；Release 有 `Track Info` 时，Taken 须回带收到的字段。未请求隐私时可附甲的功能别名；普通非广播呼叫可附 `Permission to Request the Floor=1`。也可将 Taken 的 subtype 首位置 1 请求确认；是否处理确认、未收到确认时怎么做由实现决定。此接口仍留原状态。[§6.3.5.4.5 已协商排队段，第 4–6 项及注 2，印刷页 82–83](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=83)。

例如，控制服务器上已知乙的队列项使用 `(S, P)`，分别是来向消息的 SSRC 和最上层参与者引用。Release 查到 `(S, P)`，才按这一步移出。若收到的是 `(S, Q)`，且没有该组合对应的项，不能仅凭 SSRC 相同删掉 `(S, P)`。两种情况下都发 Taken；若来向 Release 要求确认，两种情况也都先发 Ack。Taken 回带的 `Track Info` 不是队列删除回执。要核对这次撤回是否移除该项，应看控制服务器此次查找是否命中、是否执行移出。[§6.3.5.4.5 已协商排队段，第 1–4 项，印刷页 82](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=83)。

端上看到 Ack，还要分清是哪一侧收到 Release。非控制 MCPTT 功能面向参与者的接口若在 `P: has no permission`，有的分支会就地回 Ack，有的才等控制服务器的 Ack。协议字段 `Source=2` 的含义，不能代替对实际观测链路的核对。不能从终端 Ack 倒推控制服务器一定收到 Release，更不能倒推已移出。[§6.5.5.3.10，第 1–3 项，印刷页 115–116](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=116)。

再看渠道本身。非控制侧的服务器接口收到待转发的 Release 后，发往控制功能的消息须按原来是否有 `Track Info`，追加参与者引用或补上 `Track Info`。若该参与者的 Floor Request 在本侧被动队列，它还须移出这一项。终端腿没有 `Track Info`，不代表控制服务器收到的也没有；本侧被动队列移出，也不能替控制侧活动队列作证。[§6.5.4.3，第 1、2 项，印刷页 106](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=107)。

上面的步骤只展开已协商排队的第二段。第一段另以“未协商排队，或在 `mc_priority` 中包含话权优先级”为入口；若同时协商排队并包含优先级，原文两段条件有交叠。本页不为交叠情形规定先选哪一段。[§6.3.5.4.5 两个入口段，印刷页 81–82](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=82)。

## 要查撤回后是否还在队列，看对应的队位答复

在相同的 U 状态，服务器收到关联参与者的 `Floor Queue Position Request`，须发 `Floor Queue Position Info`，在 `Queue Info` 中给出位置和话权优先级，仍留原状态。可以把答复的 subtype 首位置 1 请求确认。这是独立的查询程序；没要求先撤回。原文的 `Track Info` 条件写的是 **Info 消息**含该字段，没有在此规定查询带字段就一定回带。[§6.3.5.4.7，第 1、3 项及注，印刷页 83](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=84)。

先确认哪条答复对应控制侧同一通话、同一关联参与者的查询。只抓到终端腿的孤立消息，配不上这次控制侧查询，就不能判它报告了什么。按本页“请求者 U 先处理准入与队列”一节的编码，对得上的 **254** 报告当时未排队；**255** 不能记为退队。处理 Floor Request 时也可能另发 Info，仅因日志中它出现在 Release 之后，不能认定是这次查询的答复。即使取得匹配的 254，也只证明报告时未排队，不单独证明是哪一次撤回移除了请求。没有看到队位答复，或只有终端不再等待的记录，也不能判断服务器的队列结果。[§8.2.3.5，表 8.2.3.5-1 与位置值，印刷页 150–151](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=151)；[§6.3.5.4.4，第 8(b) 项，印刷页 81](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=82)；[§6.3.5.4.7，印刷页 83](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=84)。

## G 选择撤销后把请求放到队首，不等于立即授权

条件：G 已在 Floor Taken；收到有效优先级为抢占的显式请求，当前持有者有效优先级非抢占；非multi-talker、非audio-cut-in。这里仅展开本地策略选择 revoke 的后续，未选择撤销不继承这些动作。

§6.3.4.4.7先按本地策略在撤销当前说话者与允许两者媒体之间选择。选择撤销时，G须停正在运行的T1/T20，指定 Floor Revoke cause4 Media Burst pre-empted，进入 pending Floor Revoke，并将请求者插入或更新至所有排队请求之前；仅在请求者已协商 queueing 时，向其发 Queue Position Info，含位置、优先级并条件复制请求中的Track Info。进入pending的helper须向原持有者发Revoke、启动该参与者T3并设置G pending状态；特殊呼叫类型按该helper条件携Floor Indicator。Revoke的SSRC是服务器SSRC，cause4不附额外原因信息。

强度：选择撤销之后的停止、cause4、状态、队首更新和条件通知为 SHALL；策略本身保留原文给定选择，不写成强制选撤销。

- 原入口还列“or if audio cut-in”，另一策略选项调用dual流程。这里只取非audio-cut-in的单话权撤销分支，不将原文OR改为全局AND，不展开dual/multi-talker算法。
- 显式请求的队首插入没有以协商queueing为前提，Queue Position Info发送才有该前提；两者不能合并。此时没有给新请求者发送Granted的动作。
- implicit仅供比较：§6.3.5.4.8要求已有会话升级emergency且信令告知后续offer含mc_implicit_request；§14.5只规定normal→emergency的该后续语义。§6.3.4.4.12则写emergency或imminent升级，并在先称Queue Position Info后称Queue Position Request。本页保留调用和消息名差异，不据呼叫紧急状态补一个隐式媒体许可链。

依据：3gpp-ts-24.380-v16.9.0 §6.3.4.4.7;6.3.4.4.7a (multi comparison)；§6.3.4.5.1–2；§8.2.10.1–2；§6.3.5.4.8;6.3.4.4.12;14.5 (implicit comparison)，印刷页 61,62,64,65,83,169,170,171,240。

## 持有者 U 的撤销重传与客户端停止是不同事件

条件：以下为替代事件：原持有者服务器U在permitted收到G的Revoke；该U在pending收到RTP或T8到期；原持有者客户端在has permission收到Revoke。客户端响应Release的G=0字段守卫仅限相应发送动作，不要求服务器事件已等到客户端响应。

U收到G的Revoke须转交，若含Track Info则保存，进入pending并启动T8。pending收到关联参与者含payload的RTP仍须转发给media distributor并保持pending。T8到期须重发Revoke，使用与上次相同的Rejection Cause和Floor Indicator，重启T8并仍留pending。客户端has permission收到Revoke须通知用户许可正在撤销，可解释原因，并要求media mixer丢弃剩余缓冲RTP、停止向服务器转发编码语音。收到的Floor Indicator G=0时须发含G=0的Release，可请求ACK；客户端随后启动T100、C100置1并进入pending Release。

强度：U转交、保存、T8重传/状态和客户端清缓存、停止转发、条件Release、T100/C100为 SHALL；向用户解释原因和Release请求ACK为 MAY。放弃重传时断开客户端是NOTE中的建议，非强制。

- 服务器T8重传次数和放弃后的动作是实现选项；表11.1.3给T8默认1秒、可配置，正常停止为T3到期或收到被撤销者Release。C7/C20表不提供T8次数上限，不能把C100当服务器T8计数器。
- Floor Indicator缺失不能自动当G=0。Revoke生成helper只对所列特殊呼叫要求携该字段；客户端和服务器Release分派却明确检查G位，本页不补普通消息的默认位或完整构造闭合。
- 客户端pending Release中的晚到Granted按条件ACK后仍留pending；T100上限转has no permission，Idle/Taken/RTP各有自己的后续入口。它们不证明新请求者获准；完整普通客户端重传责任见已有在网话权客户端主题。

依据：3gpp-ts-24.380-v16.9.0 §6.3.5.5.5;6.3.5.6.1–4；§6.2.4.5.4;6.2.4.6.1–8；§6.3.4.5.2 (Floor Indicator construction boundary)；§8.2.2;8.2.3.15;8.2.7；§11.1.1 T100;11.2.1 C100;11.1.3 T8;11.2.3 (counter comparison)，印刷页 43,45,46,47,65,86,87,88,148,155,156,165,166,213,219,223,224。

## G 按 RTP、匹配 Release 或计时器到期分别收尾

条件：G处于pending Floor Revoke。下述RTP、收到已被发Revoke参与者的Release、该参与者T3到期、该参与者T1到期是替代入口；不能把Release到达当超时分支的前提。

pending收到原permitted参与者RTP的指示时，G须重启T1，按本地策略要求media distributor继续转发并保持pending。收到对应Revoke的Release时，G须要求停止转发、停运行中的T1并停T3；活动队列非空则调用Idle；队列空且当前获准列表空也调用Idle；队列空但列表非空则调用Taken。T3到期时，G须先告知客户端接口general state现在是Floor Idle，再按相同的队列/列表条件调用Idle或Taken。被撤销者T1到期时须停T3，只有floor now empty才调用Idle；不能将它改成任何T1到期都进入Idle。

强度：上述按实际事件的转发、停止、通知及条件状态动作为 SHALL。

- T3默认3秒且可配置；audio-cut-in为0不适用于本页。计时表T3的Cause of start仅列T2到期，实际pending helper另明确启动T3，不能用表格删除抢占入口。T3表的到期描述为不再允许RTP且floor idle，而正文仍按队列/列表分支处理。
- §6.3.4.5.5 step2仅在支持multi时移除列表项，step3发送Release Multi Talker却未带multi守卫；本页保留这个字面动作差异，不给step3擅加条件，也不因此宣称普通单话权完整实现已闭合。相较之下，匹配Release和被撤销者T1到期中的相应multi动作有条件。
- §6.3.4.5.6另有“其他参与者T1到期”段，不能移用来替代被撤销者分支。表11.1.3 NOTE3仍使用MBCP Media Burst Release字样及最后RTP序号条件，本页不补该序号编码算法。

依据：3gpp-ts-24.380-v16.9.0 §6.3.4.5.1–6 full；§11.1.3 T1/T3 and NOTE3; T20 comparison，印刷页 64,65,66,67,218,219,220。

## Release 与 Idle/Taken 返回只结束相应局部责任

条件：原持有者服务器U在pending Floor Revoke。来自关联参与者的Release、来自G的Idle、来自G的Taken是替代事件；Release中G=0仅约束向G转交分支，不是Idle/Taken接收前提。

U收到Release时，若subtype要求ACK，须回Floor Ack，Message Type=4、Source=2。收到Release的Floor Indicator G=0时须转交G且仍留pending。后来收到G的Idle须转给参与者并进入not permitted and Floor Idle；收到Taken须转给参与者并按正文进入not permitted and Floor Taken。这两种下发可请求ACK；是否处理ACK及收不到后如何处理是实现选项。

强度：条件ACK、Release转交、Idle/Taken下发和正文状态为 SHALL；下发请求ACK为 MAY。

- §6.3.5.6.7称进入not permitted and Floor Taken却回指§6.3.5.3.2（Idle helper）；保留状态名与回指差异，不静默修成另一个编号。
- 进入Idle后的§6.3.4.3.2第一段要求非Start-stop、没有客户端协商queueing、且dual状态机不存在，却在内部列出空队列和非空队列处理。不能据撤销返回Idle，跨过no queueing守卫证明协商排队后的自动选队首和Granted。
- 发送Revoke、收到Release、返回Idle/Taken、队首位置都不是新请求者已获发送许可的证据。本页也不保证全部RTP已送达或已被播放，不把紧急呼叫状态当媒体许可。

依据：3gpp-ts-24.380-v16.9.0 §6.3.5.6.5–7；§6.3.5.3.2 (cited helper comparison)；§6.3.4.3.2 (queue advancement boundary)；§8.2.2;8.2.5 opening (permission evidence);8.2.13，印刷页 56,75,88,89,148,162,173,174。

## 共同依赖与边界

- U是逐参与者接口，G是逐通话仲裁；内部实体说明不指定实现架构。协商、SSRC/Track Info身份关联和配置输入应实际成立，不能从SIP成功反推话权状态。
- §13.2/13.3.2–4按协商及已提供CSK或已配置SPK要求相应控制消息保护；受保护RTP在PF/CF透明转发。本页只保留这些接口条件，不实现外部RFC3711、TS33.180、密钥分配或配置管理。

依据：3gpp-ts-24.380-v16.9.0 §4.2.1 (entity prose only)；§14.1–5；§13.2;13.3.2–4 (on-network control protection interface)，印刷页 25,229,230,231,232,233,235,236,237,238,239,240。

## 相关主题

- [普通在网话权客户端](on-network-floor-client.md)：普通客户端请求、授权和释放事件。
- [Idle服务器条件授予](on-network-idle-floor-server.md)：仅已有Idle上的非排队请求，不补本页排队推进。

若组实际配置了 audio cut-in，查[低或同优先级请求怎样替换当前发言人](on-network-audio-cut-in.md)，不要套本页按有效抢占优先级的入口。
