# MCVideo普通chat入口：客户端寻址、PF准入与隐式归属结果

TS24.281 V19.3.0 普通在网、带transmission control、on-demand chat group(restricted)加入；普通GMS组，客户端→O-PF→CF。仅取不存在chat session identity的新会话，或已经ongoing的chat会话，不推导已分配但inactive遗留身份处理。排除预安排、broadcast、ad hoc、NCF/gateway、重组/预配置重组、功能别名、远程/ambient、预建立、离网及302重定向。

用户没有请求紧急/迫近危险/应用优先级，客户端emergency state未置位，也没有该组的in-progress emergency/imminent-peril或待确认优先状态；响应阶段不在紧急/迫近危险call-requested/call-granted状态。请求不含emergency-ind、imminentperil-ind、alert-ind及优先通信Resource-Priority；CF该组in-progress emergency与imminent-peril均为false。不能只由用户本次未点紧急按钮推定普通范围。

客户端主条本版step12实际写MIG2、MVIG3:confirm-pending，成功响应段写MEGC2而非MVEGC2；本页用语义排除全部这些优先状态，并保留原标签，不把预安排状态编号静默移植。

PF侧仅覆盖原已判affiliated的路径，或PF判未affiliated且served user/client记录存在、该client下没有目标group entry的新隐式affiliation路径；已有deaffiliating/deaffiliated且未过期等复杂记录组合不在本页闭合。

每条claim独立继承本主题common_conditions及自身conditions，不继承前条成功。先核每个角色实际入口，不把prearranged的join-handling/自动邀请/required或私呼Answer-Mode规则补进chat。

## 客户端初始请求

适用条件：用户以识别chat组的MCVideo group ID要求建立/加入本组会话；生成客户端初始请求。

若list-service/preconfigured-group-use-only存在且true，客户端SHOULD告知不能呼叫并SHALL跳过余下步骤。否则生成initial INVITE，Request-URI为serving PF PSI；mcvideo-info中session-type=chat、mcvideo-request-uri=组ID、mcvideo-client-id=客户端ID。携带MCVideo/ICSI Contact、相应带require/explicit的Accept-Contact、MCVideo P-Preferred-Service及§6.2.1 SDP offer；主叫用户ID由O-PF加入。需要implicit transmission request时按§6.4指示，不是每次chat加入都隐式请求发送。

- 该入口对新建/加入使用initial INVITE；不能用预安排session-identity rejoin模板替代，也不要求先向所有成员发邀请。
- Supported timer和Session-Expires在客户端此请求是SHOULD，refresher建议省略，若有为uac；完整RFC/SDP字段不在本claim展开。

依据：§9.2.2.2.1.1;6.4，印刷页 248、249、140、141。

## PF身份与媒体准入

适用条件：O-PF收到目标为chat组、session-type=chat的INVITE。

O-PF可因资源不足/拥塞风险拒绝500并可带Retry-After；否则按PAI的public user identity确定并授权主叫MCVideo ID。地方策略禁止chat组呼时403/Warning108；媒体参数不接受或未提供MCVideo codecs时488；MaxSimultaneousCallsN6已exceeded时486/103。不能把预安排的403/109换到chat。

- N6原文exceeded与Warning的reached不同，不改成≥。service authorization建立绑定另依赖§7.3，本页不补私呼绑定过期404/141。
- 此处是O-PF地方策略，不等于CF组文档、成员或affiliation检查已通过。

依据：§9.2.2.3.1.1 steps1–5，印刷页 256、257。

## 普通chat的隐式归属

适用条件：O-PF依§8.2.2.2.11判断该用户在该客户端未affiliated；本页只取served user/client记录存在且目标group entry缺失的新隐式路径。

普通chat也SHALL调用§8.2.2.2.12，不需要priority call前提。helper以请求client ID、group ID和PAI绑定用户识别记录，在候选列表加入目标组entry，置affiliating并设候选到期时间。N2计数按该用户各客户端中未过期且affiliating/affiliated的不同group ID合并计算，不是只数当前客户端；超过N2时按服务商策略减少候选组。helper中，若目标组因N2仍无法加入，就丢弃候选列表并跳过其余步骤；否则以候选列表替换served client的组列表。返回主条后，只有此次隐式affiliation确因N2不成功的分支返回486/102并停止。

- 不是“已有N2所以任何新请求必拒绝”：helper有候选列表按策略缩减。策略选择、candidate expiration interval来源和值未核，不作具体配置建议。
- PF状态判定§8.2.2.2.11将affiliating和affiliated都判为affiliated；本页不以CF的记录/expiry算法替换它。该helper step1还引用9.2.2.2.2并在找user记录后写group entry，保留错引/名词异常，不重建完整状态机。
- 本页不覆盖已有未过期deaffiliating/deaffiliated记录如何重设；也不把临时候选affiliating当作CF已接受。

依据：§9.2.2.3.1.1 steps6–7;8.2.2.2.11;8.2.2.2.12，印刷页 191、192、193、257。

## 按组寻址CF

适用条件：O-PF已通过本chat入口检查及必要的新隐式affiliation候选处理；没有302重定向、别名或跨系统扩展。

O-PF按组ID确定CF PSI，生成INVITE并把Request-URI设为该CF PSI；在mcvideo-info加入主叫mcvideo-calling-user-id，按收到的客户端offer生成SDP offer，再转发。CF PSI发现方法在规范范围外。这里没有预安排条款显式“不复制Answer-Mode/Priv-Answer-Mode”的chat步骤，不能因看起来相似就加入。

- 本claim只列普通主干；若请求含location MIME仍需按step13有条件复制，若含Resource-Priority则step14转带并留CF验证。普通范围排除该优先头，不靠丢弃请求字段修复异常。
- 响应段称above INVITE in step14，但实际step14为Resource-Priority，转发是step15；保留错号。302重定向的6.3.2.1.10未在本页展开。

依据：§9.2.2.3.1.1 steps8–15，印刷页 257、258。

## 成功提交与失败撤销

适用条件：O-PF收到其向CF发出的chat INVITE的2xx或4xx/5xx/6xx；若提及隐式affiliation完成/取消，则本请求确已调用§8.2.2.2.12。

2xx时先在含MKFC-GKTPs的条件下调用§6.3.2.3.2，再生成客户端200/SDP answer，转带收到的Warning、PAI设PF PSI；若曾调用implicit helper，先执行§8.2.2.2.13把新增entry置affiliated并调用affiliation状态通知helper，然后发送客户端200，最后与媒体平面交互。4xx/5xx/6xx时生成SIP响应，带入收到的Warning header field(s)（若有），再转发响应，再在确曾调用implicit helper时执行§8.2.2.2.14删除此次新增的匹配用户/client/group entry。

- 完成/取消只作用此次implicit过程，不把全部既有affiliation清空。状态通知是§8.2.2.2.5的affiliation通知，不是conference NOTIFY。
- 成功入口写2xx、其中转带字段又写收到200；保留原文口径。chat响应段没有额外显式session identity映射步骤，不从预安排响应段补入。
- MKFC-GKTPs内部算法、通知fanout、RFC响应失败/重试尚未闭合；不得称所有接收方都已得到媒体或密钥。

依据：§9.2.2.3.1.1 response paragraphs;8.2.2.2.13;8.2.2.2.14，印刷页 193、194、258、259。

## 客户端成功及媒体接口

适用条件：客户端收到本chat initial INVITE的2xx，且本页普通状态条件持续成立。

客户端与24.581用户平面交互。普通成功段不要求客户端再等待所有组成员INVITE回答，也没有在这个chat成功段列自动conference订阅；会议订阅仍按独立§9.2.3的参与/ongoing条件。客户端媒体接口发生不等于发送许可已授予。

- 若处于原文列举的优先call状态，另有回调，本页已排除。普通4xx/5xx/6xx完整恢复策略没有在此客户端段给出，不补重试次数。

依据：§9.2.2.2.1.1 response paragraphs;9.2.3.1;9.2.3.2，印刷页 249、275、276。

## 证据边界

- IMS/RFC完整事务/超时/错误恢复、CF PSI发现、302分支、跨系统与预建立扩展未闭合。
- 既有未过期deaffiliating/deaffiliated记录的重入implicit处理、候选expiry区间与N2地方缩减策略、affiliation通知fanout未展开。
- PF状态判定helper的9.2.2.2.2错引/入口名词、client MIG2/MVIG3/MEGC2标签、CF mcvideoinfo MIME拼写及PF响应step14错号均保留。
- TNG3 chat主条MAY与common helper条件SHALL不裁决优先；无自动邀请不推成全规范绝对无TNG1。
- GKTP内部处理、SDP完整编码、媒体安全和不同实际版本完整互操作未验证。

## 按需继续

- [chat-ondemand-admission](chat-ondemand-admission.md)
- [prearranged-call-admission](prearranged-call-admission.md)
- [participant-transmission-control](participant-transmission-control.md)
- [conference-subscription](conference-subscription.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；媒体层按此独立版本核对。

## 普通chat入口与预安排重入的边界

适用条件：讨论本页普通chat进入路径与预安排重入/晚入的区别，而不是扩展优先或NCF路径。

已核普通chat§9.2.2.2.1.1以组ID生成initial INVITE并向serving PF PSI发送，CF区分identity不存在与session ongoing。预安排§9.2.1.2.4.1的session-identity Request-URI改写，以及§9.2.1.4.6在新affiliation/回覆盖通知后主动邀请，均是另有明确条件的预安排入口，不能机械移植为chat规则。chat客户端接收INVITE的§9.2.2.2.1.6明确用于emergency/imminent-peril且affiliated但未joined；它不构成普通chat自动晚入依据。

- 这是已核入口不可类推的边界，不声称全规范绝对禁止chat使用session identity，也不凭目录没有rejoin标题推导完整恢复行为。
- 一般SIP re-INVITE、覆盖探测、自动恢复/重试、NCF与临时组仍未闭合；不把一次普通加入200当恢复旧发送许可。

依据：§9.2.2.2.1.1;9.2.2.2.1.6;9.2.2.4.1.1 steps10–11;9.2.1.2.4.1;9.2.1.4.6，印刷页216、236、248、249、254、262、263。

- [chat离开与存续的对应条件](chat-participant-leave.md)
