# 按条件建立 ad hoc 组呼：选人、持续变化与停止

固定 TS24.379 V19.4.0，单一主系统普通在网按需 MCPTT ad hoc 组呼，初建使用 criteria 而非显式用户名单，不接续紧急告警；发起者不在会触发紧急呼叫的 emergency 状态。

本页核 CF/PF 用户确定、结果、持续增删通知及停止接口。初建前序准入、终接应答和媒体处理仍各有条件；错误结果不是共同继承成功。

排除用户主动修改 criteria/名单的完整 re-INVITE 流程、跨系统迁移、预建立、广播、紧急/迫近危险、端到端安全实现和具体 criteria 语义算法。功能别名只记录条文明确的可选名单元数据，不扩别名解析。

## criteria 初建有自己的调用条件

适用条件：用户请求按条件确定受邀者，且本次不接续 ad hoc emergency alert；CF 初建前序检查按其各自条件通过后才进入确定成员步骤。

客户端在初始 INVITE 正文 anyExt 中放入 call-participants-criterias，内容为一项或多项 criteria 的逗号分隔列表；不同时放显式受邀用户列表。O-PF 按主叫用户身份选择 ad hoc 服务 CF，并可依本地策略修改转送的 criteria。CF 的实际入口为 §17.4.2.2 step12(ii)：存在该 criteria 字段才调用 §17.4.6，按指定条件及本地策略确定受邀者；在呼叫建立时限内不能确定任何符合用户时，返回403+Warning187并停止。确定成员后的邀请按 step15 调用 §17.4.2.1.1，不把获得名单当作被叫已经接听。

依据：§17.2.2.1.1 steps11-12,NOTE5；§17.2.2.1.1 step15 (scope comparison: emergency state excluded)；§17.3.2.1.1 step7(a),17A；§17.4.2.2 steps7,10,12(ii),15-17；§17.2.6.1.1 opening,step2a,NOTE (comparison only: user-requested criteria modification excluded)；§17.4.2.2 SIP183/SIP200 response body clauses and17.4.6.1 step5(b) (comparison only: explicit-list criteria source gap)；§17.2.2.1.1 opening service-support check and steps1-2 (dependency: absent/false support stops client procedure; p643)；§17.3.2.1.1 opening,steps1-9 (dependency: O-PF identity binding, local authorization, media, N6, CF selection and absent/false allow; pp654-655)；§17.4.2.2 introductory identity definitions,opening,steps1-6 including3a-3d (dependency/comparison: CF admission before criteria; step4 false only,step5 absent/false support,step6 conditional on resource-list; pp670-672)。

服务开关、用户授权、身份及媒体准入并未因有 criteria 而豁免，依据本 claim 所列客户端、O-PF 和 CF 的前序条款。显式名单页仅用于比较不同输入与角色责任；其显式列表适用条件及列表限额不能移植为 criteria 分支。

本页只处理初建 criteria 及由它产生的持续确定；用户主动改名单/criteria 的 re-INVITE 是另一个入口，不在此展开。实际 criteria 的语义、匹配算法和建立时限数值不补默认。

显式名单初建不会因本页存在而自动调用 criteria helper；原名单页上游200的 criteria 来源缺口仍保留。

## CF 可以本地选人，也可以请求 PF 提供名单

适用条件：CF 实际需按 criteria 确定用户；向 PF 请求的步骤仅在 CF 选择创建供查询的终接 PF 列表时适用。

§17.4.6.1 允许 CF 依本地策略自行确定，也允许另外建立终接 PF 列表。对选入的每个 PF，CF 发 MESSAGE：Request-URI 为该 PF PSI，P-Asserted-Identity 为 CF PSI，P-Asserted-Service 为 MCPTT ICSI；正文 mcptt-request-uri 为 ad hoc group ID，anyExt 内带收到或经本地策略修改的 criteria，以及 req-type=get-userlist-adhoc-group-call-request。收到某请求的4xx/5xx/6xx后，CF 视该 PF 服务的用户不可用并将该 PF 从所建列表移除；NOTE允许依实现先重试再移除。2xx仅交 SIP 规则处理。

依据：§17.4.6 general；§17.4.6.1 opening,steps1-6,response paragraphs,NOTE6；§6.3.1.3 get-userlist request/response classification。

创建 PF 查询列表是 MAY，不是每次 criteria 初建都必须向所有 PF 广播；PF PSI 发现与查询集合选择不补实现算法。

正文关联的是 ad hoc group ID，而非参与者 ID 或会话 Contact URI。普通2xx没有携回资源列表的业务含义，不能据它宣称已确定成员。

请求原始 criteria、O-PF 转送 criteria 和 CF 发给 PF 的 criteria 可能因明确的本地策略步骤不同，不声称端到端字节不变。

## PF 回原请求200后，另发结果并持续保存条件

适用条件：PF 实际收到 get-userlist 请求 MESSAGE；拒绝与成功分支分别适用。

PF 可因资源不足或拥塞风险返回500，可附 Retry-After。它依收到的 criteria 与本地策略确定用户；无法确定符合用户时返回403+Warning187并停止。成功分支先向原 MESSAGE 回200，再确定并保存符合条件的 MCPTT ID 列表，并在适用时保存相关功能别名；保存组 ID 和 criteria，以持续判断用户满足或不再满足条件。随后另发 MESSAGE 给 CF PSI，PAI 为 PF PSI，正文 mcptt-request-uri 为该组 ID、复制 criteria、resp-type=get-userlist-adhoc-group-call-response，并带所确定用户的 resource-lists。

依据：§17.3.6.1 steps1-8 and response paragraph；§6.3.1.3 get-userlist request/response classification。

原请求200、新结果 MESSAGE、持续匹配缓存是三件事；不能把原200当作 CF 已收到名单或所有成员已加入的证明。

功能别名只按原文适用条件和本地策略记录/返回，本页不扩展别名解析及认证。持续判断的采样频率、数据源和版本一致性未规定，不补定时器。

## CF 按组身份接收结果，不把它当逐用户增删通知

适用条件：CF 实际收到 resp-type=get-userlist-adhoc-group-call-response，且 mcptt-request-uri 与已发送请求中的 ad hoc group ID 匹配。

收到的结果中存在符合用户的 resource-lists 时，CF 将每个 entry 对应用户列为待邀请者；同一 MCPTT ID 多次出现只发一个 INVITE。结果处理另写：对已参与会话、但其 ID 未包含在任一所接收相关资源列表中的用户，考虑将其移出会话；存储参与用户的 MCPTT ID 及存在的功能别名，并向结果 MESSAGE 回200。初建时选出受邀者后，仍由 §17.4.2.2 的邀请过程继续。

依据：§17.4.6.1 result MESSAGE reception conditions,steps1,1a,1b,2；§17.4.2.2 steps12(ii),15；§17.4.5.2.1 steps4-5 (comparison only: delta conditions differ)。

此处保留原文 any of the incoming SIP MESSAGE requests 的集合表述；所读段没有完整说明多 PF 返回的批次边界、等待齐全或迟到结果处理，不自创全局快照原子替换算法。

结果列表处理没有重述增删通知中的“手动邀请/手动移除/自行离开”例外；不能把 delta 分支条件无条件补入本段。考虑移出也不等于已完成 BYE 及资源释放。

错误组 ID 或不匹配 resp-type 不符合这里的结果接收条件；本页不补相应错误码。去重邀请只承诺每个 ID 一个 INVITE，不保证到达、接听或媒体成功。

## 持续匹配变化先有通知，实际增删仍受字段和历史条件限制

适用条件：PF 已保存本次组/criteria，并发现新符合或不再符合的用户；或 CF 实际收到相应增删通知。两侧行为按各自事件适用。

PF 向 CF PSI 发 MESSAGE，正文 mcptt-request-uri 为所存组 ID，req-type 设 adhoc-group-call-add-participants-request 或 adhoc-group-call-remove-participants-request，resource-lists 列相应用户；发送前更新本地存储。CF 通知入口先检查资源列表正文，缺失返回403+Warning187；按组 ID 找正在进行会话的 ad hoc 组，无法确定返回403+Warning195。通过后先回200。其后原文 step4/5 却检查 resp-type：若实际满足增员分支，则用户须尚未被邀请，且“未被手动移除 OR 未自行离开”，才列为待邀请；加入组、调用邀请过程并视受邀者隐式归属。移除分支对不再符合且未被手动邀请的用户，从组中移除，并在会话仍进行时调用 §17.4.3.1.2 移出该会话。

依据：§17.3.5.2.1 opening,steps1-5,response paragraph；§6.3.1.3 add/remove notification classification (comparison: req-type)；§17.4.5.2.1 opening,steps1-5；§17.4.3.1.2.1 (removal caller dependency)；§17.2.6.1.1 steps2(a-b) (comparison: manual membership changes)；§17.2.4.1.1 (comparison only: user leave reference)。

PF 构造和 §6.3.1.3 消息分类都使用 req-type，CF step4/5 使用 resp-type。保留不一致，不把仅携 req-type 的合规通知写成必然进入增删动作，也不擅自改字段或同时补两字段。

新增的逻辑按原文为“尚未邀请 AND（未手动移除 OR 未自行离开）”；不是两个历史条件都要满足。移除的“未手动邀请”只限所列 delta 分支。

CF 在动作前已经回200；PF 也在发送前更新缓存，均不是远端成员变化完成的证据。§17.4.3.1.2.1 仅在成功移出后 MAY 发订阅者通知，本页不展开全部 BYE/媒体依赖和补偿协议。

## 停止确定清的是查询状态，不等于通话已经释放

适用条件：CF 需要停止本次 criteria 用户确定，或 PF 实际收到对应停止 MESSAGE；已核实际 caller 为 CF 整组释放路径。

§17.4.3.1.1.1 的整组释放入口先调用 §17.4.6.2 再继续会话释放；§17.4.3.2 收到 BYE 时也只有按释放策略应释放 ad hoc 组呼才调用该停止过程。停止 helper 对所建列表中的每个 PF 发 MESSAGE，Request-URI 为 PF PSI，PAI 为 CF PSI，正文 mcptt-request-uri 为组 ID，req-type=adhoc-group-call-release-notification-request；发送后删除所建终接 PF 查询列表。PF 收到对应停止消息后，停止满足/不再满足条件的用户确定，清除所存组 ID、criteria 和已确定用户 ID 列表，再回200。

依据：§17.4.3.1.1.1 opening and final paragraph；§17.4.3.2 steps1,3 and final paragraph；§17.4.6.2 steps1-7 and response paragraph；§17.3.6.2；§6.3.1.3 stop-determination MESSAGE classification。

CF 删除查询 PF 列表的步骤在发送之后，不以全体停止200为前提；不补全员确认屏障或失败重试算法。PF 的200只对应该停止处理，不证明所有用户已退出、所有媒体已释放。

释放 caller 另规定：需要释放会话且该组无未结 ad hoc emergency alert 时才删除组及关联信息。停止 helper 的清理不能替代此条件，也不能扩成清除所有组/告警。本页不展开完整释放策略或迁移分支的占位回指。

## 阅读边界与导航

持续增删存在 req-type/resp-type 原文差异，CF 新增历史条件使用 OR；本文不修规范，也不提供无歧义的可执行状态机。

criteria 分支的新覆盖不会修复显式名单页原有的 criteria 回指缺口；两种初建入口不能互相补造必经步骤。

[显式名单初建](adhoc-explicit-list-establishment.md)用于比较不同输入与角色责任，不把该页受显式列表条件限定的 claims 直接套入 criteria。

来源：[TS24.379 V19.4.0 官方原文](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
