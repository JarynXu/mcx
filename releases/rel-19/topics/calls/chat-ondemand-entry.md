# 按需 chat 组呼入口：新建与加入都从组 ID 的 initial INVITE 开始

限 TS24.379 V19.4.0 在网、on-demand、普通非重组 chat MCPTT 组；不是预建立会话 REFER，不含 associated-group-id，不覆盖 TGI 或基于预配置组的重组。

客户端未请求 emergency、imminent-peril 或 alert；自身及该组相关紧急/迫近危险状态未触发 §10.1.2.2.1.1 steps1–2、11–12，且控制侧该组当前 in-progress emergency 与 imminent-peril 状态均为 false；请求不携带这些指示或 Resource-Priority。 客户端也不处于响应处理所列 MEGC 2/3 或 MIGC 2/3 状态；这些状态的成功/失败回调不在本页普通分支中。

为使请求构造有界，本页展开不携带 functional alias、不请求 application priority、不要求 implicit floor request、也不携带位置正文的普通分支。其他分支未被宣布为不支持。

O-PF 为服务该用户的 originating participating MCPTT function；CF 为负责目标组的 controlling MCPTT function。

## 发起与加入使用同一入口

适用条件：用户以 chat 组 ID 要求发起或加入组呼，客户端进入 §10.1.2.2.1.1。

客户端先检查组文档 list-service/preconfigured-group-use-only；存在且为 true 时，应提示该组不允许呼叫，并必须停止本过程。否则按 TS24.229 的 originating session 程序生成 initial INVITE。这里发起和加入共用同一入口，不把加入已有 chat 会话改写成以既有会话 ID 寻址的 re-INVITE。

依据：§10.1.2.2.1.1 opening paragraphs。

## 请求身份和基础字段

适用条件：组文档的 preconfigured-group-use-only 不存在或不为 true，客户端生成本主题范围的 initial INVITE。

Request-URI 为服务用户的 participating PSI；正文 application/vnd.3gpp.mcptt-info+xml 的 mcptt-Params 含 session-type=chat、mcptt-request-uri=组 ID、mcptt-client-id=本客户端 ID。Contact 含 g.3gpp.mcptt 和 MCPTT ICSI 的 g.3gpp.icsi-ref；Accept-Contact 分别含这两种标签及 require/explicit，P-Preferred-Service 为 MCPTT ICSI。Supported 的 timer、Session-Expires 均为 SHOULD；建议省略 refresher，若带则为 uac；P-Preferred-Identity 为 MAY。附 §6.2.1 的 SDP offer 后发送。用户 MCPTT ID 由 O-PF 加入，不由此客户端正文代填。

依据：§10.1.2.2.1.1 steps3–10,13(a–c),14,16; Note4。

## 参与功能逐项检查

适用条件：O-PF 收到属于 originating participating function 的 INVITE，目标标识 chat 组且正文 session-type=chat。

O-PF 先可因资源不足或拥塞风险以 500 拒绝，Retry-After 亦可选。再由 P-Asserted-Identity 中 PUI 求用户 MCPTT ID：绑定缺失或已过期返回 404/Warning141 并停止；本地策略不准该用户进行 chat 组呼则 403/108；媒体参数不接受或未提供 MCPTT speech codec 则 488；检查 profile 中 MaxSimultaneousCallsN6，已 exceeded 时返回 486/103。不能用组文档成员身份代替用户绑定或 O-PF 本地业务授权。

依据：§10.1.2.3.1.1 steps1,2,2a,3–5。

## 普通 Chat 的隐式归属触发

适用条件：O-PF 已通过本节前序检查，且按 §9.2.2.2.11 判断本用户/client 未归属 mcptt-request-uri 所指普通 chat 组。

O-PF 必须调用 §9.2.2.2.12 隐式归属，不要求先出现预安排入口中的优先呼叫或远程发起条件。若该调用因用户已经有 N2 个同时归属而未能完成本次归属，返回 486/Warning102 并停止。helper 的候选表与计数规则复用现有隐式归属主题，不把调用等同于控制侧已经准入。

依据：§10.1.2.3.1.1 steps6–7。

## 路由与可信主叫身份

适用条件：O-PF 前序检查未拒绝，且 incoming INVITE 不含 associated-group-id。

O-PF 解析负责该组的 CF PSI；无法确定则 404/Warning142 并停止。生成 §6.3.2.1.3 INVITE，Request-URI 设为该 CF PSI，在 mcptt-info 正文加入由 PAI 绑定得到的 mcptt-calling-user-id，并基于 incoming SDP 按 §6.3.2.1.1.1 构造 offer，再转发。组 ID、O-PF/CF 的路由 PSI 和用户 MCPTT ID 是不同层次。

依据：§10.1.2.3.1.1 no-associated-group-id branch steps1–5,9; Notes6–12。

## 成功响应中的会话身份映射

适用条件：O-PF 收到自己依 §10.1.2.3.1.1 向目标 chat 组控制功能转发的 INVITE 的 2xx；该请求符合本页普通按需、非重组范围。

按 §6.3.2.1.5.2 生成给客户端的 200，附 §6.3.2.1.2.1 SDP answer；若收到 MKFC-GKTPs，不纳入生成的 200。保留 incoming 200 的 Warning，PAI 设为 O-PF PSI，并包含由 incoming 200 Contact 所给会话 identity 映射而来的 MCPTT session identity。Note14 将不转发 MKFC-GKTPs 与该发起客户端使用单播媒体关联，不能把控制侧 Contact URI 原样视为客户端侧会话 identity。

依据：§10.1.2.3.1.1 2xx handling steps2–6; Note14。

## 结果回调和归属状态

适用条件：O-PF 收到本次转发 INVITE 的最终响应；分别判断 2xx 和 4xx/5xx/6xx，隐式归属回调仅在本过程已调用 §9.2.2.2.12 时发生。

成功分支先完成 §9.2.2.2.13，再向客户端发送生成的 200，随后与 TS24.380 媒体层交互并启动 RFC4028 SIP session timer。失败分支先生成响应、复制收到的 Warning 并转给客户端，再调用 §9.2.2.2.14。成功或失败回调均针对同一触发请求，失败不表示清空所有归属或完整恢复 N2 策略裁减的旧表。

依据：§10.1.2.3.1.1 2xx handling steps7–10;4xx/5xx/6xx handling steps1–4;9.2.2.2.13–.14。

## 自身成功不代表全体成员接听

适用条件：客户端收到自己按 §10.1.2.2.1.1 发出的 initial INVITE 的 2xx，且保持本主题普通状态范围。

客户端按 TS24.380 与用户面交互，并可选择按 §10.1.3.1 订阅 conference 事件。此处未要求先收齐预安排 TNG1 的 required 用户应答，也未把自身 INVITE 成功定义为所有组成员已被邀请、已接听或已获话权。普通失败分支没有在此给出自动重呼算法。

依据：§10.1.2.2.1.1 2xx and4xx/5xx/6xx handling。

## 初始来呼的适用边界

适用条件：需要决定能否把10.1.2.2.1.6用作普通chat初始来呼客户端接听规则。

不能：该小节开头明确限于已经归属、但尚未加入chat的客户端，且呼叫为emergency或imminent peril。普通chat页面不能从该优先呼叫程序抽出接受200步骤、删去前提后称为普通自动接听；也不能因此反向断言所有普通chat INVITE必被拒。

依据：§10.1.2.2.1.6 introductory scope。

## 不能搬用预安排重入规则

适用条件：需要在普通chat中解释晚加入、用户重新加入或回到覆盖；拟引用现有groups/rejoin-session。

已发布rejoin-session的session identity寻址规则来源10.1.1.2.4、10.1.1.3.5、10.1.1.4.5，属于预安排组呼。chat的已核客户端入口10.1.2.2.1.1按组ID请求加入，不能未经来源把预安排重入规则改session-type后套用。此处未找到独立普通chat回覆盖检测/重入算法，不构造自动恢复策略。

依据：§10.1.1.2.4.1–2;10.1.2.2.1.1。

## 证据边界

- 这是客户端发起/加入到 O-PF 的有界主链；未研究广播、远程发起、预建立、跨系统信任和重组完整程序。
- 不声明所有 SIP INVITE 组成要素或整个 TS24.229 事务实现已经完整覆盖。
- 完整可组合成功路径限 CF 已按 §6.3.6 确认本 user/client/组归属的情况。O-PF 未归属调用本身已核，但 CF 新增隐式归属路径有原文冲突。
- 不把预安排 §10.1.1.2.4 的 session-ID rejoin 自动套给 chat；退出后恢复、其他类型 incoming INVITE 另行判断。
- MCPTT ICSI 为 urn:urn-7:3gpp-service.ims.icsi.mcptt。SDP、TS24.229 SIP 程序不在本页扩展；需要隐式话权请求时，另依 step15 与 §6.4 判断，不由发起 INVITE 推定已获话权。
- N6 的触发正文是 exceeded，Warning 文本却用 reached；保留区别，不自行改为当前数量等于 N6 就拒绝。优先呼叫的本地策略例外不在普通范围。
- CF 对尚未归属用户的 step6 存在 eligible 文字异常，见本页证据边界；本 claim 仅确认 O-PF 的明确调用条件，不据此宣称普通未归属用户必能完整进入 chat。
- 确定 CF 或 gateway PSI、选择跨信任域 exit gateway 的方法原文明确未定义；本页不构造发现算法。该分支的失败句误称 prearranged，在此保留该措辞差异，不把本节改归预安排。
- step6 只写 include mapped identity，未单独写其在 outgoing 200 的字段位置；不靠推测补字段。媒体保护、MKFC 机制及一般应答 helper 的全部字段未重新展开。
- helper 的逐记录语义由既有 groups/implicit-affiliation-state 承担；本页不增加 3xx、事务超时或自动重试的回调规则。
- 其中明确列出的 4xx/5xx/6xx 状态动作针对特定 MEGC/MIGC 状态，不能迁移成普通 chat 的通用重试。普通 chat incoming INVITE 的接听程序不能借用优先范围条款补齐；交由本页接收边界整合。
- §10.1.2.3.1.1 no-associated-group-id branch step1（印刷页329、330）：本节为 chat，无法确定 CF 的失败句却写 on demand prearranged group call。 记录原文不一致，仍以本节标题、入口和本分支定位解释 404/142，不静默改原文。

## 按需继续

- [../groups/chat-ondemand-control](../groups/chat-ondemand-control.md)
- [../groups/implicit-affiliation-eligibility](../groups/implicit-affiliation-eligibility.md)
- [../groups/implicit-affiliation-state](../groups/implicit-affiliation-state.md)
- [../groups/conference-state](../groups/conference-state.md)
- [../calls/implicit-floor-request](../calls/implicit-floor-request.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页224、225、278、317、318、319、324、328、329、330、331、332；仅本版本。
