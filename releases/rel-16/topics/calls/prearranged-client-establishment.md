# 普通按需预安排组呼：客户端发起与应答证据

## 适用条件

- 固定 TS24.379 V16.14.0，普通在网预安排组、直接组身份、按需会话；不是 chat group、广播、临时重组、功能别名或离网流程。
- 本页不含紧急/迫近危险请求或会触发这些处理的既有客户端/组状态，也不含预建立承载或 Replaces 替换；服务器承载选择的比较边界见对应条目。
- 发起、终接、服务器前置失败和响应为不同事件入口，各自依条目条件适用；不以全链准入成功、用户已确认或全组已经加入作为公共前提。

## 发起的是预安排组会话，不是把成员逐一当作私呼目标

适用：用户请求建立本页范围内的预安排组会话。

客户端生成初始 INVITE，Request-URI 写服务自己的参与功能 PF 的 PSI；mcptt-info 的 session-type 写 prearranged，mcptt-request-uri 写组身份，mcptt-client-id 写发起客户端 ID。客户端不在该正文加入发起用户的 MCPTT ID，该值由 O-PF 根据主叫身份填入。O-PF 实际按组身份确定组 CF 并设置其路由 PSI；CF 向个别用户发出邀请时，mcptt-request-uri 已用于该被邀用户的 MCPTT ID，组身份另在 mcptt-calling-group-id。因此不能把同名字段在不同方向的对象含义混用。

规范强度：所述请求生成、身份填写及路由字段构造为 SHALL。

- 边界：本页不处理 TGI、重组、功能别名、chat group、广播或离网组呼；预安排组并不等于所有组呼类型。
- 边界：客户端请求构造不是服务器准入已通过。O-PF 的用户绑定、本地授权、媒体与并发限制，以及 CF 的组管理和成员选择另有程序，本页不把发送 INVITE 当成获准加入。
- 边界：CF 地址发现和 T-PF 地址发现分别由所引 NOTE 明示为本 Release 范围外；这里不补发现算法。

依据：TS24.379 V16.14.0 §10.0;10.1.1.2.1.1 opening,steps1–14 (priority/broadcast/TGI/alias scope comparison)；§10.1.1.3.1.1 opening,steps2,2a,8–12；§10.1.1.4.1.1 opening,steps2–4,NOTE1–3；§6.3.1.1 O-PF/T-PF/group-CF classification，印刷页 77, 78, 219, 220, 221, 230, 231, 240。

依据：TS24.379 V16.14.0 §6.6.1.1–6.6.1.4 (security dependency boundary)，印刷页 138, 139。

## 媒体 offer 与隐式话权请求各有条件

适用：客户端为该初始组呼构造 SDP；隐式话权标记仅在需要该请求时适用。

客户端按 §6.2.1 构造 SDP offer 并发送 INVITE。其语音媒体段需包含 MCPTT speech；发起组呼、组文档包含带 name 的 preferred-voice-encodings/encoding，且客户端支持该 encoding 时，须把其名称用于 a=rtpmap。需要隐式话权请求时，按 §6.4 作相应指示；普通初始语音 INVITE 中相应话权 UDP 流带 mc_implicit_request 标记时，服务器将其视为发起客户端的隐式话权请求。这是请求识别，不是已获发言权的证据。

规范强度：offer 构造、符合条件的编码填写、所需隐式请求指示及发送为 SHALL；§6.2.1 的媒体控制段为 MAY，使用媒体控制消息时其构造为 SHALL。

- 边界：编码偏好需要组文档存在并且客户端支持，不能把未配置偏好解释为没有可用编码。
- 边界：完整媒体段、话权授予、语音质量及 TS24.380 实现不在此展开；本页不以 SIP 结果替代话权结果。

依据：TS24.379 V16.14.0 §10.1.1.2.1.1 steps15–17；§6.2.1 full (ambient/private comparison)；§6.4 initial INVITE and other-cases rules，印刷页 56, 57, 136, 137, 221。

## 服务器按保存设置生成终端模式头，不能照搬私呼入口

适用：T-PF 收到本页组呼邀请，或已到达相应模式 helper；接收失败和后续构造是分别适用的事件。

T-PF 未收到被邀用户的 Answer-Mode Indication 时返回 480+Warning146 并停止；此前 step2 检查 isfocus；仅未在 step3 因缺少设置而停止时，才继续 step4–5 的被叫公共身份绑定处理。§10.1.1.3.2 的自动与手动分派都要求入站没有 Answer-Mode，保存设置分别为 auto-answer 或 manual-answer。自动/手动通用 helper 先检查是否有空闲预建立会话且语音、话权媒体段均匹配；满足时走预建立，否则走按需。在本页按需、且入站两个模式头均缺失的自动路径，helper 写 Answer-Mode=Auto；手动路径在无 Answer-Mode 且保存设置 manual-answer 时写 Manual。O-PF 组呼程序明确不向 CF 复制入站 Answer-Mode 和 Priv-Answer-Mode，这与让主叫直接指定被叫最终应答方式不同。

规范强度：所述条件拒绝、分派、承载选择及模式头构造为 SHALL。

- 边界：组呼分派不列入站已带 Answer-Mode 时的同类自动/手动选择，不从私呼入口或更宽的通用 helper 倒推并补上该入口。
- 边界：本页不把预建立路径强行改成按需。两个模式头缺失是所述自动按需补头动作的条件，不是资源或设置拒绝的前提。

依据：TS24.379 V16.14.0 §10.1.1.3.2 full；§10.1.1.3.1.1 step11；§6.3.2.2.5.1 full;6.3.2.2.5.2 steps3–11；§6.3.2.2.6.1 full;6.3.2.2.6.2 steps1–10；§6.3.2.2.3 full，印刷页 94, 95, 96, 97, 98, 99, 231, 238。

## 手动组呼可先报 183，最终应答仍另有事件

适用：以下入口分别适用：终接客户端收到初始 INVITE；到达自动或手动模式分派；手动用户拒绝；或发送最终 200。不以用户接受作为共同前提。

终端资源不足或存在规范范围外原因时可拒绝；决定拒绝后，向 PF 返回适当错误及 Warning，或在获准限制失败原因时返回不带 Warning 的 480，并停止本节。通过前序处理后，Answer-Mode=Auto 且本地自动，或本地手动但允许自动，调用组自动 helper；Manual 与本地手动或允许手动的本地自动配置对应调用组手动 helper。手动组 helper 可在用户确认前自动生成 183，并包含所要求的 Contact feature tags；用户拒绝则返回 480+Warning110 并停止。组自动 helper 调用 §6.2.3.1.1 生成并发送最终 200；手动组在发送最终 200 时也调用组自动 helper。因此 183 不能替代用户确认或最终 200，手动组也不应照搬私呼手动的 180 流程。

规范强度：资源/其他原因拒绝和手动组确认前生成 183 为 MAY；决定拒绝后的响应与停止、模式条件满足后的 helper 调用、最终 200 构造和发送为 SHALL。

- 边界：终端最终 200 helper 还要求 timer、Session-Expires/refresher=uas、Contact tags、SDP answer 与媒体交接，不是只发送一个状态码。
- 边界：这里的终端模式入口明确检查 Answer-Mode；不从私呼另加 Priv-Answer-Mode=Auto/Manual 的组呼客户端入口，也不补模式头冲突优先级。
- 边界：Replaces 替换、紧急/迫近危险状态改变与完整安全实现不在本页范围。

依据：TS24.379 V16.14.0 §10.1.1.2.1.2 full (priority/alias comparison)；§6.2.3.1.2 full;6.2.3.1.1 full；§6.2.3.2.2 full；§6.2.3.2.1 full (private comparison)；§6.2.2 full，印刷页 57, 58, 59, 60, 222, 223。

## 发起方的 2xx、应答状态和会议订阅不是同一证据

适用：替代事件：发起客户端收到对应 INVITE 的 2xx；收到 4xx/5xx/6xx；或终接客户端已经发送最终 200。不要求这些事件同时发生。

发起客户端收到 2xx 时须交接用户面；若收到 P-Answer-State，可向用户提示 Confirmed 或 Unconfirmed，并可订阅 conference event package。终接客户端发送 INVITE 的最终 200 后也可订阅该事件包。订阅是可选后续动作，不是所有成员均已应答的前提或证明。普通范围内不能把发起分支对紧急/迫近危险状态的错误响应处理搬来当作普通失败恢复：§10.1.1.2.1.1 的 4xx/5xx/6xx 后续动作仅在所列 MEGC/MIGC 状态时调用其专用 helper。本页不补普通失败的 UI、重试或状态复位算法。

规范强度：收到 2xx 的用户面交接为 SHALL；有应答状态时的提示及两端 conference event 订阅为 MAY。

- 边界：发起程序写的是 2xx，不将它收窄为只有 200，也不导入私呼客户端“必须提示已建立”的措辞。
- 边界：本页不核完整 CF 成员聚合门槛、conference NOTIFY 成员状态、可靠临时响应或媒体闭环，因此不能由本页单个响应推出全组已应答或全部媒体已就绪。

依据：TS24.379 V16.14.0 §10.1.1.2.1.1 2xx/4xx/5xx/6xx response and INFO branches (priority comparison)；§10.1.1.2.1.2 step9；§10.1.1.3.2 steps7–8 (mode scope comparison)，印刷页 221, 222, 223, 238。

## 范围边界

- 本页承担客户端初始请求、终接应答及必要模式/身份依赖，不是完整组呼生命周期。服务器完整准入、成员选择、晚入/重入、退出、优先状态及媒体实现另属责任范围。
- 完整 SIP、配置、保密性和完整性处理仍须遵循被调用规范及本版 §6.6；本文不把字段示意作为完整可发送报文，不以私呼或其他 Release 补组呼未列规则。
