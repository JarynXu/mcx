# 普通按需 MCVideo 预安排组呼：客户端请求、应答与媒体初始化

## 适用范围

- 固定 Release16 TS24.281 V16.12.0 与 TS24.581 V16.9.0；普通在网、按需、带传输控制的预安排组呼初始建立或受邀客户端应答。不是 chat、广播、临时重组、预建立会话、Replaces 替换、离网或 MBMS。
- 主叫未请求紧急或 imminent peril 呼叫，未置 MCVideo emergency state，该组不处于 MVEG2、MVIG2/MVIG4，也不处于 MVEGC2/3 或 MVIGC2/3 的优先呼叫入口；终接 INVITE 不含值为 true 的 emergency-ind 或 imminentperil-ind。本页不处理既有组呼重入。
- 发起请求、接收初始邀请、拒绝、模式选择、发送或收到响应，以及媒体初始化，按各角色实际事件分别适用。身份、安全、资源与业务授权仍须按实际程序检查，不把全部检查已通过或已收到 200 预置为所有事件的前提。

## 向服务 PF 请求预安排组，组身份留在业务体中

条件：用户要求建立本页范围的预安排组会话；隐式传输请求只在需要该请求时构造。

客户端生成初始 INVITE，Request-URI 为服务自己的 PF 公共服务标识。mcvideo-info 中 session-type=prearranged，mcvideo-request-uri 为组身份，mcvideo-client-id 为主叫客户端 ID；客户端不在该体中填写主叫用户的 MCVideo ID，该用户身份由主叫 PF 插入。请求携 MCVideo 特征、ICSI 及相应 Accept-Contact，按 §6.2.1 提供 SDP offer；需要隐式传输请求时按 §6.4 标识，然后发送。

强度：所列构造与发送 SHALL；Supported 的 timer 和 Session-Expires 为 SHOULD；P-Preferred-Identity 为 MAY。

- 组身份不是初始 SIP Request-URI，也不是私呼单用户 resource-lists 的替换写法。§6.3.1.1 的 PF/CF 分类有各自初始过滤、PSI 与 isfocus 条件，不能把客户端构造当完整服务器路由。
- §6.4 的本页初始、非远程 ambient 会话须在传输控制 UDP 流携 mc_implicit_request 才作为主叫隐式发送请求；这只是请求，不是获准。§14.2.5 在未明确要求携带时保留实现选择；§14.3.5 对加入已有预安排组另有限制，本页不覆盖该入口。
- §6.5 的多 MIME/SDP 首体及 §6.6 的收发保护义务仍适用。完整 XML schema、配置、密钥服务、RFC/SIP core、服务器逐成员邀请与资源分配算法不在本页。

依据：3gpp-ts-24.281-v16.12.0 §9.1；§9.2.1.2.1.1 steps1–17 and notes；§6.2.1；§6.3.1.1 (classification comparison)；§6.4 initial non-ambient branch；§6.5;6.6.1.1–4 (protection obligations)，印刷页 42,43,61,62,107,108,109,161,162,163；3gpp-ts-24.581-v16.9.0 §14.2.5;14.3.5 (implicit-request scope)，印刷页 224,225。

## 拒绝可先发生，模式选择另按收到的头与本地设置

条件：客户端收到本页初始 INVITE；资源拒绝适用 steps1–2，只有到达模式处理时才判断 Auto/Manual 对应条件。

资源不足或规范范围外原因允许客户端拒绝；选择拒绝后须返回适当错误码及 Warning，或者在用户获准限制失败原因时返回无 Warning 的 480，并跳过该节余下步骤。到达模式处理时，收到 Answer-Mode=Auto，且（本地自动，或本地手动但允许自动）时，应调用组自动 helper；收到 Answer-Mode=Manual，且（本地手动，或本地自动但允许手动）时，应调用组手动 helper。检查 Resource-Priority 是独立义务，其规范外进一步动作不是本页的优先业务算法。

强度：资源/其他原因拒绝 MAY；选择拒绝后的响应及停止、符合模式条件后的 helper、Resource-Priority 检查 SHALL；该头的规范外后续动作 MAY。

- 不能把本地配置为 Auto 当作客户端缺少 Answer-Mode 时的通用回退，也不从相邻私呼入口移植 Priv-Answer-Mode 分支。
- TPF 的 §9.2.1.3.2 在自己的入口检查 Contact URI 的 isfocus，缺失返回 403/Warning104；它还检查保存的 AnswerModeIndication，缺失返回 480/Warning146。这些不是客户端本段另写的一组检查，也不证明本客户端邀请已经满足全部服务端权限。
- 按需与预建立承载不能仅凭应答模式混为一条流程。本页只处理已到达客户端的初始按需 INVITE，不展开服务器承载选择或预建立替换。

依据：3gpp-ts-24.281-v16.12.0 §9.2.1.2.1.2 steps1–8；§9.2.1.3.2 (TPF isfocus/mode comparison)；§6.2.3.1.2;6.2.3.2.2，印刷页 44,45,46,164,165,173,174。

## 组呼手动进展 183 与最终 200 分开

条件：已按前条模式守卫进入相应组 helper；用户拒绝、生成 183、发送最终 200 各是该 helper 内自己的条件事件，不要求全部同时发生。

组手动 helper 可在用户确认前自动生成 183；用户不接受时须返回 480/Warning110 并停止。若生成 183，须带 MCVideo 与 ICSI 的 Contact 特征，P-Answer-State=Unconfirmed 可选。发送最终 200 时调用组自动 helper。组自动 helper 使用 §6.2.3.1.1 的响应构造和发送程序，并可增加 P-Answer-State=Confirmed；本页无 Replaces，故按 §6.2.2 构造 SDP answer，按 helper 的 timer/Session-Expires 要求构造并发送 200，然后交接 TS24.581。

强度：组手动的 183、Unconfirmed 及组自动的 Confirmed 为 MAY；拒绝后的 480/110 与停止、条件性 Contact、最终应答 helper 与媒体交接为 SHALL。

- 组手动 helper 不等于私呼手动 helper 的 180 流程；183 或 Unconfirmed 不证明用户已接受。调用自动响应 helper 不抹去此前的人工接受条件。
- 本页不把某个客户端的 200/Confirmed 当作全部成员已应答，也不从主叫收到 2xx 反推每个成员的邀请或接收状态。完整 server 响应汇聚未展开。
- 客户端建立段对可选 conference 订阅写出 §9.1.3.1，而 §9.1 在本版为 General；本页保留该回指，不据此补全订阅、名单或参加算法。

依据：3gpp-ts-24.281-v16.12.0 §6.2.3.1.1–2；§6.2.3.2.1 (private comparison);6.2.3.2.2；§6.2.2；§9.1;9.2.1.2.1.1 2xx branch;9.2.1.2.1.2 concluding paragraph，印刷页 43,44,45,46,161,163,165。

## 建立响应触发初始化，不自动证明媒体已获准或已呈现

条件：主叫收到 INVITE 的 2xx 触发信令到媒体的调用；以下状态入口按 TS24.581 所写的主叫收到 200、终接发送 200 及已协商控制条件分别适用。主叫隐式请求分支另须确有已协商隐式请求。

主叫收到 2xx 须调用媒体过程。TS24.581 按建立协商创建传输与接收控制实例；终接发出 200 时，传输进入无发送许可，通用接收进入 reception controller。主叫收到 200 后通用接收也进入 reception controller。主叫隐式请求成立时，传输按 §6.2.4.2.2 启动 T100、C100=1，进入 pending request；此前缓存的传输控制消息在进入该状态后再按该状态处理。

强度：所述条件初始化、缓存与重放以及状态动作 SHALL。

- 普通 200 的响应码本身不表示发送许可。§14.2.4/14.3.4 另允许在 offer 有 mc_granted、非临时组等条件下由 CF 在 200 的 SDP answer 指示隐式请求获准；本页不把这一可选指示当作每个 200 的默认内容，也不补完整 grant 消费算法。
- §6.2.4.2.2 正文将无隐式请求的显式无许可分支写给 chat，另列隐式请求、广播及重入；图6.2.4.1-1则有一般主叫初始化到无许可的箭头。本页不凭图替普通新建预安排组的无隐式请求情形补齐正文守卫或实现时序。
- reception controller 是通用接收控制入口，不等于某一路已获接收许可、收到 RTP 或呈现给用户。本页不展开组呼自动接收配置、逐路接收/发送、排队、撤销或完整释放。既有私呼接收页的 private-only 前提不能被本页解除。

依据：3gpp-ts-24.281-v16.12.0 §9.2.1.2.1.1 2xx branch；§6.2.3.1.1–2 media handoff，印刷页 44,45,163；3gpp-ts-24.581-v16.9.0 §6.2.1；§6.2.4.1 figure6.2.4.1-1;6.2.4.2.1–3；§6.2.5.1 figures6.2.5.1-1/2;6.2.5.2.1–3；§14.2.4–5;14.3.4–5，印刷页 33,35,36,44,45,46,224,225。

## 边界

- 只覆盖客户端建立职责与必要的实际接口对照，不是完整组呼服务器、邀请策略、资源分配、安全配置或媒体实现。所有条件均以本页固定 Release16 版本为依据。
- 没有将普通私呼、Stage2 能力描述或其他 Release 作为本组呼程序证据。完整 TS24.229、TS24.481、TS24.484、TS33.180 和 RFC 依赖未在此展开。
