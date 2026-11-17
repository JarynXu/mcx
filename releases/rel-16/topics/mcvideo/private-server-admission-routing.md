# 普通按需 MCVideo 私呼：服务器准入、路由与响应边界

## 适用范围

- 固定 TS24.281 V16.12.0，在网、带传输控制、直接 MCVideo ID 的普通一对一 private 初始 INVITE；不含组呼、first-to-answer、功能别名、推拉、ambient 或 re-INVITE。
- 请求不含 emergency-ind、alert-ind 或 imminentperil-ind，没有紧急 Resource-Priority，主叫不处于与目标的进行中紧急私呼状态。所述终端使用按需承载；不覆盖三项匹配条件成立时的预建立分支或 Replaces。
- O-PF、CF、T-PF 是不同职责，接收请求、准入拒绝、继续构造及收到响应分别按其事件进入。安全保护和前序检查仍须执行，不以全链已获准、已收到最终响应或媒体可用作为共同前提。

## O-PF 先查主叫绑定和服务，再核呼叫与模式资格

条件：O-PF 按 §6.3.1.1 收到 originating PF 初始 INVITE，mcvideo-info 的 session-type=private；拒绝和继续构造按实际到达步骤分别适用。

O-PF 可按所携 Resource-Priority 拒绝；资源不足或拥塞风险时可返回 500，并可带 Retry-After，拒绝后停止。随后由 P-Asserted-Identity 的公共用户身份确定主叫 MCVideo ID 并授权；绑定缺失或过期返回 404/141 并停止。按主叫身份确定私呼 CF 的 PSI，无法确定则 404/142 并停止。资源列表正文缺失或 private 列表多于一个 entry，各为 403/145 并停止。allow-private-call 缺失或 false 为 403/107；请求 Answer-Mode=Auto 或 Manual 且相应许可缺失/false，分别为 403/125、403/126，均停止。

强度：资源/优先值拒绝和 Retry-After 为 MAY；其余所述身份、许可检查及条件拒绝、停止为 SHALL。

- 绑定存在不代替业务许可；列表零 entry 不等同于正文缺失，也不由本段证明有效。
- 本页只列普通私呼业务门槛，TS24.484 配置模型、IMS 路由、完整安全保护实现未展开。

依据：TS24.281 V16.12.0 §6.3.1.1 originating/terminating PF and private CF classification；§10.2.2.3.1.1 opening,steps1–11b，印刷页 61, 62, 274, 275。

## 名单与强制自动许可不能互相替代

条件：O-PF 到达 §10.2.2.3.1.1 的目标名单、媒体检查或后续构造步骤；前序准入按程序执行，不以其全部成功作为本条拒绝事件的前提。

PrivateCall 存在且含 entry、目标不匹配其中 entry、又未配置允许名单外呼叫三项同时成立时，返回 403/144 并停止。未提供 MCVideo video codec 则返回 488，否则继续。构造请求时写所选 CF PSI 为 Request-URI、主叫 MCVideo ID 为 mcvideo-calling-user-id，通用 helper 复制入站 P-Asserted-Identity。Priv-Answer-Mode=Manual 不向下游携带；Priv=Auto 且 allow-force-auto-answer 缺失或 false 则 403/143 并停止，许可为 true 时才携 Auto。未向下游写 Priv=Auto 而原请求带 Answer-Mode 时，按该步骤文字复制 Answer-Mode。

强度：所述名单/媒体检查、身份构造和模式处理为 SHALL。

- 名单三项守卫不能缩成“目标不在名单就拒绝”；本段 PrivateCall 原文写 one more entry，不从其措辞补缺省名单政策。
- step13 的名单筛选说明回指 step12，但 step12 是 codec 检查、名单在 step11c；本页不改号或生成可执行筛选算法。step16d 回指 step17，而 step17 是 SDP，本页保留其显式头条件，不修复该回指。
- 通用 helper 的 P-Asserted-Service 与 CF helper 的 P-Asserted-Service-Id 写法不同；不能自行统一。模式许可不等于被叫已接受或媒体已可用。

依据：TS24.281 V16.12.0 §10.2.2.3.1.1 steps11c–19；§6.3.2.1.3 steps4,6–8；§6.3.3.1.2 step3 (service-header comparison)；§6.3.2.1.1.1 (SDP dependency)，印刷页 64, 65, 77, 275, 276。

## CF 独立准入后邀请一个业务目标

条件：CF 收到按 §6.3.1.1 分类为 private CF 的初始 INVITE；各拒绝入口或达到邀请步骤分别适用，不要求被叫已经接受。

CF 检查 Request-URI 的 PSI 是否分配给私呼，未分配按 §6.3.7.1 返回 404 并停止；验证 mcvideo-calling-user-id 并按本地策略授权，不许可则 403 并停止。资源列表缺失或 private 列表超过一个 entry 为 403/145 并停止；SDP 必须至少有一个媒体流，其参数及至少一个 codec 或 media format 被 CF 接受，否则 488 并停止。继续时缓存收到且支持的 Contact feature tags，分配会话身份，并由 §10.2.2.4.1 邀请列表用户：XML mcvideo-request-uri 写业务被叫 ID，SIP Request-URI 写其 T-PF PSI，PAI 复制主叫公共身份；Contact 则是会话身份并带 isfocus 等特征。

强度：所述准入、条件拒绝/停止、缓存、身份和邀请构造为 SHALL。

- CF 的媒体检查不是 O-PF video codec 检查的同义替代。CF step3 在本 CF 段仍称被拒请求为 originating PF request，本页保留角色上下文，不补另一跳。
- T-PF 地址如何取得，§10.2.2.4.1 NOTE2 明确在本 Release 范围外；不把已知地址输入当作已证明发现算法。
- CF offer helper 描述新会话一个 video media-level section，O-PF offer helper 描述两个；本页仅登记实际调用，不裁决数量差异或宣称完整 SDP 互通。普通 private 的强制 Auto 是否经 CF 向后传递不能从 ambient 专用分支推定，CF 非 ambient 分支明写复制 Answer-Mode。

依据：TS24.281 V16.12.0 §10.2.2.4.2 steps1–11 (steps5–8 priority scope comparison)；§10.2.2.4.1 opening,steps1,3–9 and NOTE2；§6.3.7.1；§6.3.3.2.2；§6.3.3.1.2 steps1,3,8–10；§6.3.3.1.1;6.3.2.1.1.1 (SDP comparison)，印刷页 64, 76, 77, 78, 89, 106, 283, 284, 285。

## T-PF 的被叫准入不因主叫获准而省略

条件：T-PF 按 §6.3.1.1 收到终接 PF 初始 INVITE；按需承载限定见共同条件。

资源不足或拥塞风险时 T-PF 可返回 500，可带 Retry-After，拒绝后停止。Contact 缺 isfocus 返回 403/104 并停止。private 请求但尚未收到被叫的 Answer-Mode Indication 时返回 480/146 并停止；由 XML mcvideo-request-uri 的被叫 MCVideo ID 查公共身份绑定，缺失则返回 404，否则继续。配置表明被叫不能参加私呼时返回 403/127。后续模式选择按本用户保存设置及实际模式头进入对应 helper，不能以主叫许可代替。

强度：资源拒绝及 Retry-After 为 MAY；所述其余检查、响应与模式调用为 SHALL。

- step6 的 403/127 没有另写 skip-rest，不将邻近停止文字移入以补调度。缺绑定的本段 404 未带 O-PF 的 Warning141。
- 本版此段没有 MCPTT 式 IncomingPrivateCallList/Warning159 检查，不能从同类业务移植；这不是宣称所有其他安全义务均不存在。
- 具体客户端应答和 PF 自动/手动及预建立选择条件见配套客户端页，本页不重复这些 helper 的动作。

依据：TS24.281 V16.12.0 §10.2.2.3.2 steps1–8；§6.3.1.1 terminating PF classification；§6.3.2.2.5.1;6.3.2.2.6.1 (on-demand boundary comparison)，印刷页 61, 62, 71, 73, 281, 282。

## 各跳的 180、200 和媒体调用分别取证

条件：以下为替代事件：O-PF 收到 180 或 200；CF 收到 180 且尚未发送 180 或最终响应；CF 收到 private INVITE 的 200 且尚未向邀请者发最终响应；O-PF 或 CF 收到其他不含 SDP 的 SIP 响应。不得将各跳响应合成一个全局已成功前提。

O-PF 的 180 分支带回收到的 PAI 和 Warning；200 分支带回 PAI、Warning、映射收到 Contact 的会话身份，按所列 SDP 依赖发送 200，再交接媒体并启动会话计时。CF 的受守卫 180 分支向邀请者发送 180；受守卫 private 200 分支先生成响应、列出 SDP answer 调用，交接媒体并在该处理完成后发送 200。CF 最终响应 helper 的 PAI 是 CF PSI，Contact 是 CF 会话身份，不是被叫业务 ID。两段对其他不含 SDP 的响应均要求沿信令路径转发。

强度：所述响应构造、字段、转发、媒体调用及程序顺序为 SHALL。

- O-PF 主程序对 180/200 回指 §6.3.2.1.5.1/.2；本版 §6.3.2.1.5 是 BYE，实际响应章节为 .4.1/.2。仅比较，不擅自替换调用。
- CF 200 分支把 SDP answer 回指 §6.3.3.2.2，但该节是 feature-tag 缓存；SDP answer 实际标题为 .2.1。不能凭此页宣称完整响应构造已闭合。
- CF 邀请侧另有 Contact 缓存、媒体调用及最大私呼时长计时器；本页不把这些旁支与上游 200 任意排序或扩为完整释放实现。成功信令和媒体调用不是已验证发送许可、呈现或完整端到端媒体成功。

依据：TS24.281 V16.12.0 §10.2.2.3.1.1 180/200/other-without-SDP response branches；§10.2.2.4.2 private 180/200 and other-without-SDP response branches；§10.2.2.4.1 timer/200 branches (boundary comparison)；§6.3.2.1.2.1；§6.3.2.1.4.1–2;6.3.2.1.5 (mismatched response reference comparison)；§6.3.3.2.1–2 (SDP reference comparison)；§6.3.3.2.3.2，印刷页 64, 65, 66, 89, 90, 91, 276, 277, 284, 285, 286。

## 边界与关联

- 本页配套客户端页，但只承担服务器普通准入、身份及有限响应职责；未闭合的回指不以其他版本或业务规则补齐。
- §6.5 MIME 与 §6.6 保护义务仍适用。TS24.229、TS24.484、TS33.180、TS24.581 与 RFC 完整实现未在此展开。

目标客户端怎样处理普通按需初始 INVITE，见[客户端请求与应答证据](private-client-answer-evidence.md)。服务器转送不等于对端收到或接受。
