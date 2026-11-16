# MCVideo普通chat控制侧：资格、初建/已有分支与媒体许可

TS24.281 V19.3.0 普通在网、带transmission control、on-demand chat group(restricted)加入；普通GMS组，客户端→O-PF→CF。仅取不存在chat session identity的新会话，或已经ongoing的chat会话，不推导已分配但inactive遗留身份处理。排除预安排、broadcast、ad hoc、NCF/gateway、重组/预配置重组、功能别名、远程/ambient、预建立、离网及302重定向。

用户没有请求紧急/迫近危险/应用优先级，客户端emergency state未置位，也没有该组的in-progress emergency/imminent-peril或待确认优先状态；响应阶段不在紧急/迫近危险call-requested/call-granted状态。请求不含emergency-ind、imminentperil-ind、alert-ind及优先通信Resource-Priority；CF该组in-progress emergency与imminent-peril均为false。不能只由用户本次未点紧急按钮推定普通范围。

客户端主条本版step12实际写MIG2、MVIG3:confirm-pending，成功响应段写MEGC2而非MVEGC2；本页用语义排除全部这些优先状态，并保留原标签，不把预安排状态编号静默移植。

PF侧仅覆盖原已判affiliated的路径，或PF判未affiliated且served user/client记录存在、该client下没有目标group entry的新隐式affiliation路径；已有deaffiliating/deaffiliated且未过期等复杂记录组合不在本页闭合。

每条claim独立继承本主题common_conditions及自身conditions，不继承前条成功。先核每个角色实际入口，不把prearranged的join-handling/自动邀请/required或私呼Answer-Mode规则补进chat。

## CF入口检查

适用条件：CF收到chat group ID目标的INVITE，主叫取mcvideo-calling-user-id、组取mcvideo-request-uri。

CF可因资源不足/拥塞风险500并可带Retry-After；Accept-Contact缺MCVideo tag、缺相应ICSI tag、或Contact存在isfocus三项任一成立即403并停止。组文档preconfigured-group-use-only=true时403/167；随后按§6.3.5.2获取并初步处理组文档，只有该helper检查成功才继续。普通请求不含priority indication元素，故不进入相应验证支路。

- 原文preconfigured检查在step2A，获取组文档在step4；本页不重排步骤或推导此前缓存必如何取得。
- step3的MIME原文写application/vnd.3gpp.mcvideoinfo+xml（缺连字符），其余段为mcvideo-info+xml；保留差异，不以未读取schema强解。

依据：§9.2.2.4.1.1 steps1–4，印刷页 261、262。

## 组文档的chat类型条件

适用条件：CF进入§6.3.5.2对普通未重组组文档的初步处理，本请求session-type=chat。

未订阅时执行组文档xcap-diff订阅；订阅404对应404/113，其它4xx/5xx/6xx对应原最终响应加114并停止。收到文档或已有缓存后，on-network-disabled元素存在即403/115；名单无主叫entry即403/116；on-network-invite-members=true且本请求不是prearranged，因此404/117并停止。chat使用类型匹配检查，不是看到invite-members就自动邀请全组。

- disabled条件是present，不改成true。on-network-invite-members=false的helper分支只拒绝session-type不为chat者；不能照搬预安排页的404/118到此chat请求。
- 成员名单初检、PF本地chat授权和CF affiliation eligibility不是同一个条件。组文档订阅/缓存完整生命周期未展开。

依据：§6.3.5.2;9.2.2.4.1.1 step4，印刷页 135、136、137、262。

## 未归属用户的资格检查

适用条件：CF按§6.3.6判断主叫在该client未affiliated；本页普通非重组chat路径。

CF按§8.2.2.3.6调用.3.8检查implicit affiliation资格。group ID取mcvideo-request-uri、用户取calling-user-id；GMS中组不存在、用户不是成员、或CF没有匹配group ID的group information entry，任一成立就不eligible。eligible才可走后续隐式过程；not eligible时chat主条返回403/120并停止。这一版原文明确是not eligible，不反转为eligible失败。

- 本chat主条没有调用6.3.5.3的join-handling或6.3.5.4的allow-initiate-conference规则；本页不把预安排加入/发起权限字段擅自补为chat必查项，也不声称系统全局不存在其他授权。
- 原已affiliated者不因本步骤重复implicit eligibility；§6.3.6仍要求group/user/client记录和用户记录未到期，不能用名单成员资格替代。

依据：§9.2.2.4.1.1 step5;8.2.2.3.6;8.2.2.3.8;6.3.6，印刷页 139、140、200、201、262。

## 初建与已有会话容量

适用条件：CF通过此前服务、组文档及必要的隐式affiliation资格检查，进入媒体检查和会话状态分支；本页只取尚无chat session identity或确已ongoing的两种状态。

媒体检查不通过时488并停止。chat session identity不存在时，CF创建chat session并分配identity；主条写MAY按6.3.3.5处理TNG3。若chat已ongoing且on-network-max-participant-count已经reached，则除地方策略判请求用户更高优先级并实际采用MAY移除participant/跳过拒绝的支路外，返回486/122。不能把普通新建套成先向最多N人自动发邀请。

- 新建判据是identity不存在，不移植预安排“identity已分配且active”的定义，也不补已分配但inactive身份的处理。reached不改成exceeded。
- TNG3主条MAY与helper在maximum-duration存在时SHALL启动、缺失时SHALL不启动的措辞分别保留；chat该配置是optional，不自行裁决一般与专门条文优先级。
- 容量的更高相对用户优先级可来自地方策略，不等于一定发起紧急通信。其移除入口9.2.1.4.4.3错引6.3.3.1.5仍未修复，本页不研究替换实现。

依据：§9.2.2.4.1.1 steps9–11;6.3.3.5.1，印刷页 128、262、263。

## CF提交归属记录

适用条件：CF在step5确定请求eligible for implicit affiliation，且本主条尚未调用§8.2.2.3.7；此前媒体/容量等检查未拒绝请求。

在step12 CF调用§8.2.2.3.7：定位已存在的组记录与主叫用户记录，不存在用户记录则新建；把从请求导出的client ID加入该用户client ID列表（若尚无），按地方策略设置用户记录expiration time，再调用该组affiliation状态通知helper§8.2.2.3.5。这个CF记录更新先于后面的200生成/发送，不等到PF向客户端转发成功后才开始。

- CF组→用户→client记录与PF用户→client→组候选列表不是同一存储视图。这里只确认调用和记录时点，不宣称各系统通知收齐或失败可原子回滚。
- 组记录缺失已在eligibility检查失败，此helper并非随意新建未知组。expiration是该用户记录的地方策略值，不补具体秒数；状态通知详细fanout未核。

依据：§9.2.2.4.1.1 step12;8.2.2.3.7，印刷页 200、201、263。

## 成功响应及有条件通知

适用条件：CF已通过普通chat服务/组文档、必要affiliation资格/提交、媒体及容量检查；没有priority UPDATE、告警或升级分支。

CF生成200和SDP answer，SHOULD带Session-Expires并监督SIP会话；refresher建议省略，若有为uac。Require带timer，Contact含MCVideo/ICSI、session identity和isfocus，Supported带tdialog。CF先与媒体平面交互再发送200。只有chat在该请求前已经ongoing且至少一名participant订阅conference时，step25才要求向已有订阅者发送NOTIFY；新建不直接套用这条条件通知。

- 此处没有预安排成功helper的Session-Expires SHALL，不升级本段SHOULD；普通范围排除SDP answer的priority UPDATE例外。
- 源文列先媒体交互再发送200，但没有预安排条款那句明确完成后才下一步的NOTE，不额外宣称全媒体处理已完成。
- 本条没有添加Warning123，也没有说所有成员均已加入；O-PF收到2xx后反而先向客户端发200再媒体交互，不能抹平角色顺序。

依据：§9.2.2.4.1.1 steps15–25，印刷页 264、265。

## 普通chat不自动邀请全组

适用条件：CF正在处理本页普通chat加入，用户请求及CF现有组状态均无emergency/imminent-peril；所有成功条件按本chat主条成立。

普通路径由组文档/affiliation/媒体/容量处理走向请求者的200，没有预安排式选取全部affiliated invitees、逐一邀请并等待required/minimum应答的步骤。该chat主条向已affiliated但尚未joined成员发INVITE的段落位于priority处理steps13/14，不能把它推广为所有普通chat加入都会触发。

- 这只是此普通chat入口的已核边界，不升级为“所有chat在任何流程绝不使用TNG1”。通用6.3.3.3的组建立措辞、外部required配置适用性未在本页裁决。
- 没有自动邀请不等于组无其他成员、成员无需授权或媒体可立即发送；这些分别由对应条件和TC控制决定。

依据：§9.2.2.4.1.1 steps10–25，印刷页 262、263、264、265。

## SIP成功与发送许可

适用条件：本普通有TC chat由客户端initial INVITE加入，并进入24.281成功媒体接口；对照实际核读24.581 V19.2.0。

24.281 §6.4将符合普通session发起且SDP transmission-control UDP流含mc_implicit_request fmtp的initial INVITE视为implicit transmit request，其他情况不作implicit请求。24.581中，已建立chat且INVITE不是implicit请求时进入U:has no permission to transmit；若为implicit请求则启动T100、C100=1并进入pending request，先前缓存的控制消息在该状态处理。两者都不能只因SIP200就声称已获发送许可。

- 这是chat普通发起/加入，不将预安排rejoin的禁止implicit规则搬过来。server §6.3.2.2同样保留chat initial INVITE/REFER除非explicitly stated才作implicit处理。
- 发送授予/排队/拒绝及按源接收流程见既有participant/server主题。本页明确24.28119.3与24.58119.2独立版本，不称同版互操作完成。

依据：§24.281 V19.3.0:6.4;9.2.2.2.1.1;24.581 V19.2.0:6.2.4.2.2;6.3.2.2，印刷页 140、141、249、36、52、53。

## 证据边界

- IMS/RFC完整事务/超时/错误恢复、CF PSI发现、302分支、跨系统与预建立扩展未闭合。
- 既有未过期deaffiliating/deaffiliated记录的重入implicit处理、候选expiry区间与N2地方缩减策略、affiliation通知fanout未展开。
- PF状态判定helper的9.2.2.2.2错引/入口名词、client MIG2/MVIG3/MEGC2标签、CF mcvideoinfo MIME拼写及PF响应step14错号均保留。
- TNG3 chat主条MAY与common helper条件SHALL不裁决优先；无自动邀请不推成全规范绝对无TNG1。
- GKTP内部处理、SDP完整编码、媒体安全和不同实际版本完整互操作未验证。

## 按需继续

- [chat-ondemand-entry](chat-ondemand-entry.md)
- [prearranged-call-admission](prearranged-call-admission.md)
- [prearranged-call-setup-result](prearranged-call-setup-result.md)
- [conference-state-notification](conference-state-notification.md)
- [participant-transmission-control](participant-transmission-control.md)
- [server-transmission-grant](server-transmission-grant.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；媒体层按此独立版本核对。

- [chat离开与存续的对应条件](chat-release-policy.md)
