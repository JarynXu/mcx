# MCVideo预安排组呼：客户端寻址与两级准入

TS24.281 V19.3.0 的普通在网、带 transmission control、按需预安排组呼初次建立；使用 GMS 维护的普通 MCVideo group ID，不是 TGI、重组、预配置重组、chat、广播、ad hoc、功能别名、远程/ambient 或离网。本页不处理已在进行的组呼加入/重入；CF 以 session identity 已分配且 session active 两项同时成立判断 ongoing。

请求不含 emergency-ind、imminentperil-ind、alert-ind 或优先级/功能别名扩展，发起客户端 emergency state 未置位，该组不处于 MVEG2、MVIG2/MVIG4，响应时不在 MVEGC2/3 或 MVIGC2/3；CF 组 in-progress emergency 和 imminent-peril 均为 false。没有待处理的优先级升级/取消。普通条件不能仅由用户这次未选择紧急推断。

各段均为按需会话，终接客户端没有可供本呼叫复用的空闲预建立会话。精确 helper 分流条件是：存在未绑定业务会话的预建立会话、video media-level sections 匹配、transmission-control media-level section 匹配三项同时满足才走预建立；本页选择没有此可复用组合的分支。

每条 claim 独立继承本主题 common_conditions，并叠加自身 conditions；不继承前一条 claim 的成功。这里核的是信令主干，不代表 IMS/RFC、媒体编码、密钥下发或全部异常已经实现。跨规范条文分别标明实际核读版本。

## 客户端发起与路由字段

适用条件：用户要求发起本普通预安排组会话；在客户端生成初始 INVITE。

若组文档 list-service/preconfigured-group-use-only 存在且为 true，客户端 SHOULD 告知不能呼叫并 SHALL 停止后续步骤。否则按本页范围生成 INVITE：Request-URI 是 serving PF 的 PSI；mcvideo-info 中 session-type=prearranged，mcvideo-request-uri=目标组 ID，mcvideo-client-id=发起客户端 ID。携带 MCVideo/ICSI 的 Contact 和带 require、explicit 的 Accept-Contact、P-Preferred-Service，按§6.2.1提供 SDP offer；需要隐式发送请求时才按§6.4指示。主叫 MCVideo user ID 由 O-PF 填入，不是客户端在此步骤填入。

- 这是路由/身份字段最小链，完整 SIP/SDP 编码仍依赖§6.2.1、TS24.229；Supported timer/Session-Expires 在此客户端请求中是 SHOULD，不改成无条件 SHALL。
- 组 ID、用户 ID、client ID 与 SIP PSI 不能互换；客户端知道组成员身份也不等于 CF 已确认 affiliation。

依据：§9.2.1.2.1.1;6.4，印刷页 208、209、140、141。

## 发起PF的准入与转发

适用条件：O-PF 收到 session-type=prearranged 的初始 INVITE；无 associated-group-id。

O-PF 可因资源不足或拥塞风险拒绝500并可带 Retry-After；否则从 P-Asserted-Identity 的 public user identity 确定主叫 MCVideo ID 并授权。地方策略禁止发起预安排组呼时403/Warning109；未提供 MCVideo codecs 时488；MaxSimultaneousCallsN6 已 exceeded 时486/103。通过后按组 ID 确定 CF PSI，生成转发 INVITE，把 Request-URI设为该 PSI，加入 mcvideo-calling-user-id 和基于原请求的 SDP offer，且不复制收到的 Answer-Mode/Priv-Answer-Mode，再转发。普通链不触发本条仅为获准 priority call 设置的隐式 affiliation。

- 原文 exceeded 与 Warning 的 reached 措辞不同，保留 exceeded，不自行改成≥。
- 本条没有私呼中那条明确的绑定过期404/141规则，不移植；service authorization 绑定建立另属§7.3。N2的486/102只在本条确实执行过隐式 affiliation 且因N2失败时触发，本页普通链不据此自动产生 N2 错误。
- 设置CF Request-URI 的步骤写“determined in step8”，但本分支确定CF PSI实际在step1，step8是 Resource-Priority 转带；保留错引，不改编号。CF PSI发现算法在规范范围外。

依据：§9.2.1.3.1.1，印刷页 217、218、219。

## CF先核媒体服务和文档

适用条件：CF 收到发起本组呼的 INVITE；group ID 取 mcvideo-request-uri，主叫取 mcvideo-calling-user-id；组文档由 GMS 维护。

CF 可因资源不足/拥塞风险拒绝500并可带 Retry-After。媒体参数不接受或未提供 MCVideo codecs 时拒绝488；Accept-Contact 缺 MCVideo tag 或缺相应 ICSI tag 任一成立即403。随后获取并初步处理组文档：尚未订阅时订阅 xcap-diff；该订阅收到404时返回404/113，其他4xx/5xx/6xx返回相应最终响应并带114。主流程发现初步处理已发4xx/5xx/6xx后停止，不继续建立。

- 不是先分配会话再做授权。收到 priority indication 元素即触发另行验证，因此本页明确排除元素本身，不能只把其值写false来绕过该入口。
- 24.481的完整订阅授权、缓存一致性与失败重试不在本页闭合；不把订阅200当组呼200。

依据：§9.2.1.4.2 steps1–5;6.3.5.2，印刷页 135、136、226、227。

## 组文档的独立拒绝条件

适用条件：CF 已收到组文档通知或已有缓存，按普通未重组组身份进行初步检查；请求 session-type=prearranged。

文档含 on-network-disabled 元素即403/115并停止；list-service/list 没有匹配主叫 MCVideo ID 的 entry 即403/116并停止；on-network-invite-members=false 而本请求不是chat，返回404/118并停止。主流程另检查 preconfigured-group-use-only=true，返回403/167并停止。成员资格、组是否可调用、组类型是不同检查，不能靠一个 list entry 全部通过。

- disabled 的条件原文是元素 present，不是值true；未读取外部 schema 来改写这一条件。
- §6.3.5.2 step4b(ii) 用“does not include ... temporary OR ... regrouped”，且写 MCVideo ID，而其他段使用 group ID。本页只取两元素均无的普通组，不据此裁决分类歧义。

依据：§6.3.5.2 steps4–5;9.2.1.4.2 step5，印刷页 136、137、227。

## 归属包括用户客户端和期限

适用条件：CF 处理尚未 ongoing 的普通组呼；不存在 constituent-group affiliation 豁免且请求没有 emergency/imminent-peril indication。

CF 按§6.3.6依次查匹配 group ID 的组记录、该组下匹配 MCVideo ID 的用户记录、该用户下本 client ID 的客户端记录，再检查用户记录的 expiration time。任一记录缺失或用户记录已到期，均判本用户在本客户端未 affiliated；全部满足才判 affiliated。普通新建分支未 affiliated 时403/120并停止。客户端 ID 来自请求的 mcvideo-client-id，不是以用户属于组名单替代。

- expiration 检查对象原文是 applicable MCVideo user information entry；不改成client记录期限。
- §9.2.1.4.2 step13a 的 i–iv 布局在 iii/iv 间给出 or，未为其他子项逐个重写逻辑连接词。本页仅描述普通、无constituent豁免、无priority indication的适用交集，不扩张到priority分支。

依据：§6.3.6;9.2.1.4.2 step13a，印刷页 139、140、228。

## 发起许可不等于组成员资格

适用条件：CF 已通过前置检查，普通未重组组呼尚未 ongoing；进入§6.3.5.4的CF发起权限检查。

普通组发起许可需要同时满足：组文档 list 有主叫 MCVideo ID entry；存在允许 allow-initiate-conference=true 的规则，且规则以 is-list-member 条件或匹配该主叫的 identity 条件适用；supported-services 必须存在，含 enabler=MCVideo ICSI 的 service，且 group-media 含 MCVideo video media。否则不获准；主流程返回403/119并停止。通过后 CF 创建预安排会话、分配 session identity，并按§6.3.3.5处理TNG3。

- 不把支持服务字段的存在要求降为可选；不照搬ongoing加入授权。TNG3具体值、重置、到期释放另依赖§6.3.3.5，本页不写算法。

依据：§6.3.5.4 CF branch;9.2.1.4.2 step13b/e，印刷页 138、139、228、229。

## 选择已归属邀请者

适用条件：普通新建准入已通过，CF按§9.2.1.4.2 step13g选择并邀请成员。

CF从组文档名单中按§6.3.6找 affiliated 成员，只邀请 affiliated 成员。组成员数超过 on-network-max-participant-count 时只邀请该上限人数，优先选择 entry 中存在 on-network-required 的成员；其他选择规则不在该规范范围内。CF需要时先启动TNG1，再逐一执行§9.2.1.4.1.1邀请，并与24.581媒体平面交互。名单成员、已affiliated、被邀请和已回答四者不同。

- 隐式affiliated成员也属于候选集合，但本条不创建新的affiliation，也不授予发送媒体权限。
- 规范假定GMS已验证人数上限不低于required用户数；这里不重新定义校验算法。原文NOTE2使用audio transmission措辞，不把它扩写成所有视频分发都必须等全员。

依据：§6.3.5.5;9.2.1.4.2 step13g，印刷页 139、229、230。

## 证据边界

- 限普通初建和所列成功分支；原文错引与门槛差异未裁决，不代替完整组呼实现。

## 按需继续

- [prearranged-call-terminating](prearranged-call-terminating.md)
- [prearranged-call-setup-result](prearranged-call-setup-result.md)
- [private-call-server-admission](private-call-server-admission.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。
