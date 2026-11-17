# 通话中取消组紧急状态：授权、拒绝与告警结果

TS24.379 V19.4.0，在网已建立的按需预安排MCPTT组呼，当前讨论取消组的 in-progress emergency 状态。不是取消建立中的呼叫，也不是退出组或释放通话。

不包括chat、广播、ad hoc、预建立会话、跨系统/网关、离网或迫近危险主链；不纳入初始紧急起呼和升级。本主题保留本人告警、他人告警及不取消告警的明确替代分支。

每条按其客户端、PF或CF角色及独立事件适用；不把客户端许可、CF许可、媒体状态检查或下游200合并为一个全局成功前提。

以下过程中的动作按原文 SHALL 执行；显示提示为 SHOULD，明确可选动作保留 MAY。

## 先判断取消谁的状态，再形成请求

客户端正在参加按需预安排组呼，用户要求取消该组紧急状态。以下自身与第三方路径是替代分支，各自仍需满足指定状态和授权。

客户端依本地策略判断是否发送组状态取消请求，dispatcher 或紧急呼叫发起者只是策略示例；未授权时 SHOULD 提示，SHALL 停止。对自身发起的紧急呼叫，§6.2.8.1.3 要求 MEGC=3：MEA=1 时放 emergency-ind=false、清自身 emergency state、设 MEG=3；MEA不为1且仅取消组状态时，放 emergency-ind=false、设 MEG=3，保留自身 emergency state。若还要求取消自身告警，另在 allow-cancel-emergency-alert=true 时加 alert-ind=false、设 MEA=4 并清自身 emergency state；无告警取消授权时 SHOULD 提示，不把它当组取消拒绝。两种情况均设 MEG=3。按 §10.1.1.2.1.4 step3 取消他人告警时调用 §6.2.8.1.14：组取消已授权即放 emergency-ind=false、设 MEG=3；只有用户要求且另获告警取消授权，才加 alert-ind=false 及 originated-by=该告警发起者 ID。请求的 session-type=prearranged、mcptt-request-uri=组ID，携带规定 Contact 标记及按需 SDP offer，并按 §6.2.8.1.2 处理 Resource-Priority 后发送 re-INVITE。

MEG=3 是 cancel-pending，不是取消成功。没有 ongoing call 时原入口改用 §12.1.1.5 的 MESSAGE，不属于此处会话内链。

第三方 helper 自身入口较广，但本主题只沿主过程明确调用的“同时取消他人告警”路径，不据此补造 MEGC≠3 的普通参与者只取消组状态的完整构造。

获准取消且 MEG 为 no-emergency 或 cancel-pending 时，§6.2.8.1.2 列普通级 Resource-Priority，取服务配置 normal-resource-priority 的 namespace/priority；不编固定数值。该 helper 同时保留基于 MEGC 的紧急级条件，条件重叠时此处不另造优先顺序。

来源：§10.1.1.2.1.4 opening and steps1-9，印刷页273, 274；§6.2.8.1.3, §6.2.8.1.6 cancellation paragraph, §6.2.8.1.7, §6.2.8.1.14，印刷页76, 77, 78, 79, 82；§6.2.8.1.2 cancellation paragraph, §6.2.8.1.15 normal priority，印刷页76, 83。

## PF 转送请求，但不代替 CF 的取消决定

服务发起客户端的 PF 收到标识该按需预安排会话的 re-INVITE。响应处理分别以收到该转送请求的 2xx 或 403 为事件。

资源不足或拥塞风险时 PF MAY 以500拒绝并可带 Retry-After；媒体参数不可接受或未提供 MCPTT speech codec 时返回488。继续时按 §6.3.2.1.9 复制已有 mcptt-info+xml，加入发起用户 mcptt-calling-user-id，按收到的 offer形成按需SDP，存在 Resource-Priority 时复制其内容，再转送 re-INVITE。收到2xx时生成带SDP、所收 Warning、PF PSI作为P-Asserted-Identity的200，先发向客户端再调用媒体接口；收到403时生成403，复制存在的mcptt-info+xml及Warning，转发后调用媒体接口。

转发完成不是取消获准；Resource-Priority 有效性由CF判断。其他错误的完整 SIP 转发与媒体内部未展开。

原文响应回指 step7，而发送在step8；403分支还使用 INVITE 用语。这里只保留该re-INVITE节已列的有限处理，不把回指改写为规范修订。

来源：§10.1.1.3.1.3，印刷页286, 287；§6.3.2.1.9，印刷页115。

## 获准取消仍可能被正在发送的紧急用户阻止

CF 收到 Request-URI 中会话身份标识该按需预安排组会话的 re-INVITE，正文 emergency-ind=false。以下拒绝分支各自判断，并非全部同时成立。

CF可因资源或拥塞风险以500拒绝。优先级字段组合须校验：emergency-ind=false 时不得包含 imminentperil-ind，alert-ind 可有可无；无效组合返回403+Warning150。组取消授权由CF本地策略判断，不由客户端的通过结果代替。未授权时，或已授权但媒体接口判定另一用户处于 emergency state 且正在发送媒体时，均返回403并带 emergency-ind=true，停止后续处理；在该拒绝分支中，若请求 alert-ind=false 且该MCPTT用户有未结告警，响应另带 alert-ind=true。

另一用户“处于紧急状态”和“正在发送”必须同时成立；不是只要组中还有紧急用户就自动命中step7a，也不是授权能跳过该守卫。

媒体状态判定仅保留 TS24.380 调用依赖，未核其内部算法。step7/7a的未结告警条件原文写该MCPTT用户，不把它静默替换为 originated-by 所指任意用户。

来源：§10.1.1.4.7 steps1,2,7,7a，印刷页304, 306；§6.3.3.1.13.4 group paragraph，印刷页138；§6.3.3.1.17，印刷页142。

## CF 清组状态，告警按授权和身份另清

CF 的该 re-INVITE 已通过所有适用前序拒绝，emergency-ind=false、组取消已授权，且组当前 in-progress emergency state=true。若同时清告警，还须 alert-ind=false、告警取消已授权且存在原文所指未结告警。

CF把组紧急状态设false，清除有未结紧急组呼的MCPTT用户ID缓存。告警清理另按条件进行：有 originated-by 就清该ID的告警缓存，否则清请求发送者的告警缓存，不是清全组告警。CF调用 §6.3.3.1.6 向其他参与者发送 re-INVITE；该helper采用与终接端当前已建立的媒体参数，带发起用户ID，组状态false时使用普通级Resource-Priority，并在获准取消条件下携带 emergency-ind=false。收到相应200后调用媒体接口。CF停止TNG2，并向已归属但未参与通话的成员发MESSAGE，emergency-ind=false，只有相应告警取消分支成立才带alert-ind=false。

CF告警取消helper明确 true为授权、false为未授权；未列缺失配置的结果，不补成与客户端完全相同的缺省拒绝算法。

§6.3.3.1.6 step4(b)(ii) 对告警取消授权回指 §6.3.3.1.15，而该条是 imminent peril re-INVITE；主过程step8(c)则回指 .13.3。保留两处差异，不据此声称下发 alert-ind/originated-by 的授权调用已经无疑义闭合。helper在其所写授权条件下要求携带alert-ind=false，并复制存在的originated-by。

这里没有BYE或结束全组呼叫的动作。TNG2/TNG3切换另见组呼释放计时主题；不重复定时器数值、超时取消或竞态。

来源：§10.1.1.4.7 step8，印刷页306, 307；§6.3.3.1.6 steps1,2,4，印刷页131, 132；§6.3.3.1.13.3，印刷页138。

## 收到状态更新，不意味着自己的告警总被取消

参与客户端在该按需组呼中收到 re-INVITE，mcptt-info+xml 内 emergency-ind=false。告警子分支另要求 alert-ind=false，且清本端MEA时还要求 originated-by 匹配本端MCPTT ID。

接收端 SHOULD 显示取消组紧急状态的用户ID，SHALL设MEG=1；仅MEGC原为3时设MEGC=1。若还带alert-ind=false，SHOULD显示告警取消及取消者；有originated-by时 SHOULD显示原告警发起者，仅该ID就是本端用户时 SHALL设MEA=1。接收端接受re-INVITE，生成并发送带规定Contact特征标记及按需SDP answer的200，然后与媒体接口交互。

不是重新执行初始人工接听模式。未匹配 originated-by 不可从组状态false推导本端告警也已清除；此处没有统一清所有客户端紧急状态的步骤。

这是以已收到更新为前提的接收行为，不证明所有参与者都已收到。完整T-PF逐跳传递和未参与者MESSAGE接收状态处理未展开。

来源：§10.1.1.2.1.6 step3,steps5-12，印刷页276, 277。

## 200 确认组状态，不包办告警结果

分别处理：CF收到所发re-INVITE的200；PF收到下游结果；请求客户端收到本次取消re-INVITE的2xx或4xx/5xx/6xx；或客户端在该priority-group对话内收到满足指定包名和正文条件的INFO。这些是独立事件，不要求同时发生。

CF在收到re-INVITE的200分支调用媒体接口，构造上游200及SDP；若请求alert-ind=false但告警取消未授权，携Warning149。按列出的动作在发上游200前再次调用媒体接口；收到对该带149响应的ACK后调用 §6.3.3.1.18 发INFO，此取消拒绝分支置alert-ind=true。客户端收到取消2xx时调用用户面，设MEG=1、MEGC=1；仅MEA原为4、原请求无originated-by且响应无Warning149三项同时成立，才设自身MEA=1。收到4xx/5xx/6xx时设MEG=2；错误响应带alert-ind=true且原请求无originated-by时设MEA=3。原文另列错误响应不含带alert-ind的mcptt-info正文且不含originated-by时，MEA恢复进入本过程前的值。有效INFO须处于该priority-group请求对话，Info-Package=g.3gpp.mcptt-info，关联mcptt-info+xml中至少设置alert-ind、imminentperil-ind或emergency-ind之一；客户端回200。原请求无originated-by且MEA=4时，INFO的alert-ind=true使MEA=3，false使MEA=1。

CF原文把上游200构造放在收到re-INVITE的200之后，但未在本段给全员响应计数、失败聚合或去重条件；不能把一个上游200解释为全体成员均已更新，也不自行改成等待所有200。

错误响应最后一条的“不含originated-by”在原文句法上随错误响应描述；不把它无说明改成原请求条件，也不借私呼的无正文恢复规则替代。

这里确认的是会话信令与条件式本地状态；不证明媒体优先级实际完成、话权已获准、告警已全清或原呼叫已释放。PF对INFO的完整转送未展开。

来源：§10.1.1.4.7 response/ACK paragraphs，印刷页307, 308；§10.1.1.2.1.4 response/INFO paragraphs，印刷页274；§6.3.3.1.18 steps1-3(b)，印刷页142, 143；§6.2.8.1.13 opening,steps1,4，印刷页81, 82。

## 范围边界

组状态取消与告警取消是不同授权和状态；本地策略例子不等于 dispatcher 必然获准。

TS24.380仅为媒体/话权调用依赖，TS24.229事务、完整SDP、配置文档合法性及全部异常恢复未展开。

§6.3.3.1.6告警授权回指、错误响应originated-by归属和CF响应聚合边界均保留，不按私呼或其他业务修补。

来源：[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，对应3GPP TS24.379 Rel19。
