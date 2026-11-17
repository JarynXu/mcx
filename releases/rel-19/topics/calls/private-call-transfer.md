# 未预告私呼转接：三角色、结果与旧呼释放

TS24.379 V19.4.0，主系统在网、直接 MCPTT ID 的未预告私呼转接。A 请求把其正在进行的 A–B 私呼中的 B 转给 C；A、B、C 分别是 requesting、transferred、target 角色。

各 claim 的请求、接收、拒绝、响应和完成事件分别适用，不以控制请求已获准、B 已起呼成功或 C 已接听作为全页前提。

本页只展开转接控制许可、身份与映射、新呼调用、结果和成功后的旧呼释放入口；不展开功能别名、announced 咨询/保持、跨系统网关或完整媒体生命周期。

## A 请求把正在通话的 B 转给 C

适用事件：A 请求将正在进行的 A–B 私呼转接到直接 MCPTT ID 标识的 C，非 announced 转接。

A 是 requesting user，B 是 transferred user，C 是 target user。客户端 allow-call-transfer 缺失或 false 时 SHOULD 提示未授权，并 SHALL 停止。通过后 SHALL 生成并发送 MESSAGE：mcptt-called-party-id=C；anyExt/request-type=transfer-private-call-request；call-to-functional-alias-ind=false；resource-lists 放 B；Request-URI 为服务 A 的 PF PSI。P-Preferred-Service 与 Accept-Contact 携 MCPTT ICSI，后者带 require/explicit；P-Preferred-Identity MAY 携带。

规范强度：未授权提示 SHOULD、停止 SHALL；通过后的请求构造和发送 SHALL；P-Preferred-Identity MAY。

- announced 转接另有保持原通话、与目标的咨询通话及 Replaces 处理，§11.1.8.2.3 调用 RFC5359 §2.1；这些不在本页展开，不能把本页当 announced 实现。
- 这里请求的是转移既有 A–B 通话，不是要求任意远端用户另起一通与旧通话无关的呼叫。

依据：TS24.379 V19.4.0 §11.1.8.1、§11.1.8.2.1 steps1–4、§11.1.8.2.3 (announced scope comparison)、§F.1.3 call-to-functional-alias-ind definition，印刷页 498,499,501,502,730。

## 发送者身份与转接许可分别核对

适用事件：O-PF 收到转接 request 或 response MESSAGE；许可拒绝仅在所述 request-type 分支适用。

PF MAY 因资源或拥塞风险返回 500，MAY 带 Retry-After。它 SHALL 从入站 P-Asserted-Identity 的公共身份取得发送者 MCPTT ID；无绑定或绑定过期时 SHALL 返回 404+Warning141 并停止。request-type=transfer-private-call-request 时，allow-call-transfer 缺失/false，或 allow-call-transfer-to-any-user 缺失/false 且 C 不匹配 AllowedMCPTTIdsForCallTransfer，分别触发 403+Warning170 并停止。可继续分支 SHALL 选择 requesting user 的转接服务 CF PSI，复制 mcptt-info/resource-lists，将 mcptt-calling-user-id 写为已绑定发送者，加入自己的 PAI 与服务标记并发送。下游 2xx 时 SHALL 生成 200 给发送客户端；4xx/5xx/6xx SHALL 转发。

规范强度：身份绑定、条件拒绝、转送及响应处理 SHALL；资源拒绝与 Retry-After MAY。

- 结果 MESSAGE 的发送者是 B，不把 mcptt-calling-user-id 强制保留为 A；request-only 权限不能套到 response。CF PSI 的确定方法由本节 NOTE5 明列在规范范围之外，不补回程服务选择算法。
- 目标名单比较的是 C，不是资源列表内的 B。控制 MESSAGE 的 200 不是 C 接听的证据。

依据：TS24.379 V19.4.0 §11.1.8.3.1 full、§6.3.1.3 transfer private call classifications、§11.1.8.2.2 completion steps1(d),2 (return identity dependency)，印刷页 99,100,500,501,502,503。

## CF 按控制收件人路由，终接 PF 保存转接映射

适用事件：CF 接收转接请求或结果；随后 T-PF 处理实际投递用户。可转送实例的资源列表包含一个有效收件 MCPTT ID。

CF 可因资源/拥塞风险返回 500；Accept-Contact 缺 MCPTT ICSI 须 403 并停止，缺资源列表正文或 list 中 entry 总数多于一个须 403+Warning145 并停止。本页直接 ID 分支复制 mcptt-info，取资源列表的用户 ID 写入 mcptt-request-uri，并将 Request-URI 设为服务该用户的 T-PF PSI，携自己的 PAI 与服务标记后发送。去程收件人 B，回程收件人 A，均不以 C 替代。CF 下游 2xx 转为 200 给 O-PF，错误响应转发。T-PF 按 mcptt-request-uri 查公共身份绑定，缺失返回 404 并停止；可资源拒绝 500。通过后调用 §6.3.2.2.11 生成 MESSAGE。其 step5 的转接 request 分支读取 C，并保存收件用户 ID 与 C 的映射；NOTE 说明同一用户多个并发转接需多个映射。随后加入服务标记并发送。

规范强度：CF/TPF 条件拒绝、身份/路由、映射及发送 SHALL；资源拒绝与 Retry-After MAY。

- CF 明列缺正文或多于一个 entry 的拒绝，不自行增加零 entry 的同一拒绝规则。功能别名解析分支不在本页启用。
- T-PF §11.1.8.3.2 step5 写 originating participating 类别，而本节 opening 为 terminating request/response；§6.3.1.3 又将终接 request/response 合为一个类别。保留这些名称差异，不静默修订，也不能把本页当无歧义实现模板。
- MESSAGE helper 以目标公共身份为 Request-URI，按 §6.3.2.2.9 复制 MIME，但排除 MKFC-GKTP；不是无条件复制全部正文。
- 本 T-PF 主段没有另列下游响应转发段；不从其他业务移植。映射寿命、消费删除及并发关联算法不在此补齐。

依据：TS24.379 V19.4.0 §11.1.8.4 full (alias step comparison only)、§11.1.8.3.2 full、§6.3.1.3 transfer classifications、§6.3.2.2.11、§6.3.2.2.9、§11.1.8.2.1 step3(e)、§11.1.8.2.2 completion step1(d)，印刷页 99,100,125,126,499,500,503,504,505,506。

## B 实际发起新呼，映射不能替代准入

适用事件：B 收到转接请求 MESSAGE；或 B 的 O-PF 接收到由该请求触发的新 INVITE/REFER。两个角色按各自事件适用。

B SHOULD 提示收到转接请求，SHALL 从 mcptt-called-party-id 取得 C。本地策略选择按需时 SHALL 调用 §11.1.1.2.1.1；选择预建立且会话可用时 SHALL 调用 §11.1.1.2.2.1。按需新呼 step14A 构造 session-type=private、call-transfer-ind=true，并沿用被转接通话的 Priv-Answer-Mode 值；预建立 REFER 的 step8(c)(ii)(D) 同样携转接标志。新呼的 O-PF 对 private 的 call-transfer-ind=true 且没有 B–C 缓存映射时，按 INVITE §11.1.1.3.1.1 step11(c) 或 REFER §11.1.1.3.1.2 step10(d) 返回 403+Warning170 并停止。这不豁免各自身份、私呼准入及实际接续模式检查。

规范强度：接收提示 SHOULD；目标提取、条件起呼调用、转接字段及映射缺失拒绝 SHALL。

- 预建立不可用不自动等于改走按需；本文没有补 fallback。客户端接收与 PF 拒绝不以映射存在或准入成功为共同前提。
- 按需 allow-private-call 拒绝步骤另写停止；预建立 step9 的 403/107 拒绝没有另写停止，不把前者措辞移植。
- 此处负责转接的实际调用和映射检查，不展开完整新呼 SIP/SDP、安全、媒体实现。普通起呼页的排除条件不能用链接消除。

依据：TS24.379 V19.4.0 §11.1.8.2.2 steps1–5、§11.1.1.2.1.1 step14A、§11.1.1.2.2.1 opening and step8 (transfer construction; Replaces comparison)、§11.1.1.3.1.1 steps3–11(c)、§11.1.1.3.1.2 steps2–10(d)、§F.1.3 call-transfer-ind definition，印刷页 417,418,428,429,430,436,437,441,442,443,500,730。

## 180 或最终响应触发结果，但不直接定义成功

适用事件：B 所调用的按需或预建立起呼过程已经收到 SIP 180 或 SIP final response。

B SHALL 生成结果 MESSAGE：resource-lists/entry@uri 为收到请求的 mcptt-calling-user-id，即 A；mcptt-called-party-id 仍是 C；anyExt/response-type=transfer-private-call-response；按起呼过程是否成功设置 transfer-call-outcome=success 或 fail。请求携 MCPTT ICSI，Accept-Contact 带 require/explicit，P-Preferred-Identity MAY 携带。Request-URI SHALL 指服务 B 的 PF PSI并发送。结果再走上述 PF/CF 控制路径。F.1.3 的 outcome 定义对应成功或失败地发起被请求的呼叫。

规范强度：触发后的结果构造与发送 SHALL；P-Preferred-Identity MAY。

- 180 是报告触发之一，不据此写成 C 已接听或 180 必为 success，也不额外规定每个后续响应都重复上报。
- 客户端分类 §6.2.0.1 写 responset-type，结果构造 §11.1.8.2.2 写 response-type；保留拼写差异，不修成统一模板。
- 没有从 outcome 推导媒体可听、话权已获或服务持续可用。

依据：TS24.379 V19.4.0 §11.1.8.2.2 completion paragraph and steps1–3、§F.1.3 transfer-call-outcome definition、§6.2.0.1 transfer response classification、§6.3.1.3 transfer response classifications，印刷页 68,99,100,500,501,730。

## A 只在成功结果分支结束旧呼

适用事件：A 收到原控制 MESSAGE 的 4xx/5xx/6xx；或 A 收到转接结果 MESSAGE。两者是替代入口，不以 B 成功或完成作为共同前提。

A 收到原请求错误响应时 SHOULD 提示请求失败并退出其余步骤。A 收到结果 MESSAGE 时 SHALL 从 transfer-call-outcome 判断成功/失败，生成并发送 200；SHOULD 提示结果。只有 outcome=success 分支 SHALL 调用 §11.1.3.1 结束 A 与 B 的旧私呼。按需旧呼的客户端发起释放调用 §6.2.5.1；预建立旧呼调用 §6.2.5.2。这个成功分支不能提前到控制事务 200，也不能施加给 fail。

规范强度：错误响应提示并退出按原文 SHOULD；结果判定、200 及 success 条件下调用旧呼释放 SHALL；结果提示 SHOULD。

- §6.2.5.1 是按需 BYE；§6.2.5.2 是预建立业务释放 REFER，Refer-To 带 method=BYE。这里只定位调用，不把业务释放等同删除预建立承载，或声称全部媒体清理已完成。
- 原文错误响应句以 should 表述提示并退出，不额外提高为 SHALL 停止。fail 没有本成功分支的旧呼释放动作，不能据此保证旧呼永远保持或补重试算法。
- announced 成功分支还涉及 A 与 C 的咨询通话释放，不属于本页未预告范围。

依据：TS24.379 V19.4.0 §11.1.8.2.1 response paragraphs (including announced comparison)、§11.1.3.1.1.1、§11.1.3.1.2.1、§6.2.5.1、§6.2.5.2、§11.1.8.3.1 response paragraphs、§11.1.8.4 response paragraphs，印刷页 74,463,499,500,503,506。

## 相关入口

- [remotely-initiated-private](remotely-initiated-private.md)
- [forwarding-client-results](forwarding-client-results.md)
- [originating-authorization](originating-authorization.md)
- [preestablished-private-origination](preestablished-private-origination.md)
