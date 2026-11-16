# MCVideo预安排组呼：required、最低人数与Unconfirmed成功

TS24.281 V19.3.0 的普通在网、带 transmission control、按需预安排组呼初次建立；使用 GMS 维护的普通 MCVideo group ID，不是 TGI、重组、预配置重组、chat、广播、ad hoc、功能别名、远程/ambient 或离网。本页不处理已在进行的组呼加入/重入；CF 以 session identity 已分配且 session active 两项同时成立判断 ongoing。

请求不含 emergency-ind、imminentperil-ind、alert-ind 或优先级/功能别名扩展，发起客户端 emergency state 未置位，该组不处于 MVEG2、MVIG2/MVIG4，响应时不在 MVEGC2/3 或 MVIGC2/3；CF 组 in-progress emergency 和 imminent-peril 均为 false。没有待处理的优先级升级/取消。普通条件不能仅由用户这次未选择紧急推断。

各段均为按需会话，终接客户端没有可供本呼叫复用的空闲预建立会话。精确 helper 分流条件是：存在未绑定业务会话的预建立会话、video media-level sections 匹配、transmission-control media-level section 匹配三项同时满足才走预建立；本页选择没有此可复用组合的分支。

每条 claim 独立继承本主题 common_conditions，并叠加自身 conditions；不继承前一条 claim 的成功。这里核的是信令主干，不代表 IMS/RFC、媒体编码、密钥下发或全部异常已经实现。跨规范条文分别标明实际核读版本。

## 成员200计数及通知

适用条件：CF已发送本组呼的逐客户端INVITE，收到其响应。

收到183同时带Require:100rel和P-Answer-State:Unconfirmed时，CF发送PRACK。收到某邀请INVITE的200时，CF先与媒体平面交互，向已有conference订阅的participants发NOTIFY，再将邀请成员200计数加1。原文明确这些通知可早于给发起者的200，且不能证明组会话最终建立成功。

- 只为已订阅者通知，不是无条件广播给组名单；计数从§9.2.1.4.2 step8初始化0。本页不假定183能算作成员200或人类接受。

依据：§9.2.1.4.1.1 response paragraphs，印刷页 224。

## required确认与最低人数交集

适用条件：组文档中存在affiliated且on-network-required的成员，CF正在初次发起组会话。；成功分支只取两段都明确允许的交集：所有此类required邀请均收到200、当前响应MCVideo ID匹配对应INVITE、没有本页排除的NCF required等待，而且邀请成员200总计数≥on-network-minimum-number-to-start。

存在affiliated required成员时，CF在发邀请前SHALL启动TNG1。所有affiliated required的200收齐时停TNG1；在本claim明确的计数门槛满足后向发起者发200/SDP answer，媒体面处理须在发送前完成，再通知订阅者发起者已加入；因on-network-max-participant-count未能邀请全员时带Warning122。尚未回答的非required成员随后200视为加入ongoing会话，不是建立时必须等待全员。

- §6.3.3.3明确给出≥minimum，§9.2.1.4.2 required分支只引用停TNG1但未重复最低人数条件。本页不裁决两段在低于minimum时的差别，也不以主条省略为取消门槛。
- TNG1配置值依Annex B.2.1/配置规范，未核，不给固定时长。

依据：§6.3.3.3;9.2.1.4.2 required-200 branch，印刷页 125、232、233。

## TNG1到期策略

适用条件：TNG1已经到期；普通本地组建立，按§6.3.3.3处理。

若邀请成员200计数低于minimum，CF先等后续响应使计数达到相等，再继续expiry处理。计数≥minimum后，组文档on-network-action-upon-expiration-of-timeout-for-acknowledgement-of-required-members=proceed时发200/111和SDP answer，媒体处理先于200，并通知conference订阅者；=abandon时向发起者发480/112，已confirmed对话分别发BYE并交互媒体，未confirmed对话分别发CANCEL。

- 到期不等于立刻失败，也不是无条件继续。低于minimum等待和≥minimum处置是源文不同条件，不把前者改成定时器重启。
- proceed生成200引用6.3.3.2.2，但该条实际是缓存Contact feature tags；真正生成响应标题6.3.3.2.3.2，保留错引。未完成成员永不到达最低人数的最终收敛机制不由本段补足。
- 后续可选in-dialog MESSAGE、BYE以及一般组释放流程未展开；不把本页当完整超时恢复算法。

依据：§6.3.3.3，印刷页 125、126。

## required成员提前失败

适用条件：TNG1到期前收到affiliated且required成员的4xx/5xx/6xx最终响应。

若地方策略决定不在缺该成员时继续，CF停止TNG1并把该最终响应带Warning112送向发起者。若决定继续且200计数≥minimum，则在原文“if all other invited clients have not yet responded”条件下继续运行TNG1；若所有其他被邀请客户端均以200回答，则停TNG1、生成200/111与SDP answer，完成媒体处理后发给发起者。

- 继续运行TNG1的条件保留原文，不裁决“全都未答”或“尚未全答”的量词范围。后续成功条款覆盖所有其他被邀请客户端均以200回答的情形，不把这个充分条件提升为排他必要条件；存在其他非2xx、部分响应等组合不补算法。
- 继续分支生成200同样指向6.3.3.2.2，保留错引。策略“预计对应proceed/abandon”的NOTE不是把地方策略替换为硬性等式。

依据：§6.3.3.3 early failure paragraphs，印刷页 126、127。

## 缓冲支持下Unconfirmed成功

适用条件：CF收到已发送邀请的183，明确带P-Answer-State=Unconfirmed；TNG1未运行；CF支持media buffering；尚未向邀请者发送最终响应。

这四项同时满足时，CF生成200/SDP answer并带P-Answer-State=Unconfirmed；组成员数大于on-network-max-participant-count时带Warning122。CF先完成媒体平面处理，再向发起者发送200，随后通知已订阅conference的客户端发起者加入。这个200允许在被邀请用户最终确认前出现，不代表所有用户已接听。

- 本分支未规定先达到minimum；不能把另一个200计数分支的门槛塞入，也不能删除buffering前提使其适用于任何服务器。无buffering分支本页不补造。

依据：§9.2.1.4.2 183-Unconfirmed response branch，印刷页 232。

## 缓冲支持下最低计数分支

适用条件：CF收到某邀请INVITE的200；TNG1未运行；本地邀请成员200计数恰好等于on-network-minimum-number-to-start；CF支持media buffering；尚未向发起者发最终响应。

在这五项同时满足并按地方策略的分支，CF生成200和SDP answer，完成媒体处理后发给发起者，并通知conference订阅者其已加入。若因组成员数超过max-participant-count而没有邀请全员，带Warning122。成功条件不是任意一个成员200，也不是计数≥minimum的泛化。

- 此处使用max-participant-count，而其他容量/Warning122段使用on-network-max-participant-count；不静默统一字段。生成200错引6.3.3.2.2，保留。
- 本页未展开本主条后续无TNG1的4xx/5xx/6xx与补邀组合，也不凭本条宣称缺buffering时永远不能建呼。

依据：§9.2.1.4.2 minimum-count response branch，印刷页 233、234。

## 发起PF转带结果的顺序

适用条件：O-PF收到其向CF发出的本组呼INVITE的2xx，或收到4xx/5xx/6xx。

2xx分支先在含MKFC-GKTPs时执行§6.3.2.3.2，生成客户端侧200/SDP answer，转带实际收到的Warning，PAI为PF PSI，并纳入映射自下行Contact所给session identity的MCVideo session identity；之后先向客户端发送200，再与媒体平面交互，再启动SIP session timer。4xx/5xx/6xx则生成相应响应、转带收到的Warning并送客户端。客户端收到INVITE的2xx后与24.581用户平面交互。

- O-PF先发200再媒体交互与CF先完成媒体处理再发200不同，不统一成一个全链时刻。原文入口写2xx但内部数次写收到200，保留而不扩大其它2xx细节。
- 普通链没有执行priority专用implicit affiliation，因此不把该主条成功完成/失败撤回implicit affiliation的条件步骤说成每次组呼都执行；session identity放置字段本段未再明确，不自行补Contact位置。

依据：§9.2.1.3.1.1 response paragraphs;9.2.1.2.1.1 response paragraphs，印刷页 210、219。

## 信令成功不等于媒体许可

适用条件：本普通有TC组呼已经进入相应24.281成功/媒体交互接口；以下24.581规则只依据实际核读的V19.2.0，分别满足本句角色条件。

24.581中，终接participant在信令发送INVITE的200后创建basic transmission实例并进入U:has no permission to transmit。发起者若INVITE含隐式Transmission request，则进入pending request、启动T100并把C100设1；此前缓存的控制消息在进入该状态后处理，不是仅凭SIP200自动授予。双方在各自发送/收到200的建立点创建每call的general reception controller；basic reception实例按每次receive media request建立，因此会话200也不能代替针对某源的接收许可。

- 24.281 V19.3.0与24.581 V19.2.0独立标版，不声称同版互操作验证。普通预安排且无implicit request时的发起状态不从chat专用条款推导。
- 媒体授权/拒绝/排队及普通组服务器Mode1详见既有participant/server主题；接收Mode0的客户端条件规则并不授予普通组服务器任选Mode0的权利。

依据：§24.281:9.2.1.2.1.1;6.2.3.1.2;6.4;24.581 V19.2.0:6.2.4.2.2/.2.3;6.2.5.1;6.2.5.2.2/.2.3，印刷页 62、140、141、210、36、45、46。

## 证据边界

- 限普通初建和所列成功分支；原文错引与门槛差异未裁决，不代替完整组呼实现。

## 按需继续

- [prearranged-call-admission](prearranged-call-admission.md)
- [prearranged-call-terminating](prearranged-call-terminating.md)
- [participant-transmission-control](participant-transmission-control.md)
- [participant-reception-control](participant-reception-control.md)
- [server-reception-permission](server-reception-permission.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

媒体状态机另据 [TS24.581 V19.2.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf) §6.2.4.2.2–.2.3、6.2.5.1、6.2.5.2.2–.2.3，印刷页36、45–46；与信令来源分别追溯。
