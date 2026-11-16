# MCVideo 按需私呼：客户端邀请、应答与接通证据

TS24.281 V19.3.0 §§10.1/10.2.2；在网、有 transmission control、直接呼叫一个 MCVideo ID 的私呼。双方使用按需会话，不含 Replaces，也不走可复用预建立会话分支。

本次无 emergency/alert 请求或紧急 Resource-Priority；发起客户端不处于 MVEPC 2/3 或本私呼的 MVEPP 2，控制侧也没有 originating→target 的 in-progress emergency private call 状态。不包含组呼、first-to-answer、功能别名、ambient viewing、远程发起或无 transmission control 私呼。

以下列出关键信令条件，不替代 TS24.229 的完整 SIP 事务、身份信任和媒体安全规则；服务器仍有独立准入。

## 邀请地址与目标

适用条件：用户要求建立本范围私呼，客户端构造 initial INVITE。

Request-URI 指向服务发起用户的 PF 的 PSI；被叫 MCVideo ID 放在 resource-lists 的 entry uri，mcvideo-info 的 session-type 为 private。INVITE 带 MCVideo/ICSI 标识及 SDP offer 和 transmission-control stream。请求强制自动应答用 Priv-Answer-Mode=Auto；未请求强制时，按用户要求用 Answer-Mode=Auto 或 Manual。这些是请求内容，不证明服务器已授权或对方已接听。

- 若需要新建端到端安全上下文，step8 另要求必要 KMS 材料、生成/面向被叫封装 PCK/PCK-ID 并签名 MIKEY I_MESSAGE；不能仅因没有在本 claim 展开就省略该条件分支。算法与 UID/KMS URI 确定依赖 TS33.180 和6.2.8.3.9。
- 服务标识和特性标签不是用户授权；不把 PSI 当被叫 MCVideo ID。

依据：§10.2.2.1;10.2.2.2.1 initial steps1,3–7,9–11,13，印刷页 324、325、326。

## 终端资源拒绝

适用条件：终接客户端收到本范围 initial INVITE；判定是否拒绝邀请。

客户端可因正在另一会话且同时会话数超过 Max-Simul-Call-Nc10、资源不足，或规范外其他原因拒绝。拒绝时返回相应 SIP 错误和 Warning；仅用户获准限制失败原因时，可改用不带 Warning 的480，然后不再执行本条款后续步骤。

- 原文阈值是 exceeds，不改成大于等于；may reject 不改成所有达到阈值必须拒绝。
- 失败原因隐藏权限来自 allow-failure-restriction；其配置文档 TS24.484 未在本页展开。

依据：§10.2.2.2.2 steps1–2，印刷页 327。

## 验签成功才解封PCK

适用条件：本范围终接 INVITE 的 SDP 含 a=key-mgmt:mikey，且其中为 MIKEY-SAKKE I_MESSAGE。

从 I_MESSAGE 的 IDRi 取发起 MCVideo ID，转为 UID 后验签。认证验证失败拒绝 INVITE，返回488和 Warning136；只有签名验证成功，才按该分支提取并用终接用户 KMS provisioned UID key 解封 PCK，再取 PCK-ID。共享 PCK 支持端到端 SRTP/SRTCP，不等于传输许可。

- step4d 明写拒绝但未写停止本条款余下步骤；不补造统一停止语句。step4e 本身的成功验签前提必须保留。
- 本段未给缺少 I_MESSAGE、解封失败或密钥过期的完整通用错误算法；不能借用 MCData CSK download 的规则。

依据：§10.2.2.2.2 step4 and NOTE2，印刷页 328。

## 应答模式与用户拒绝

适用条件：终接客户端继续处理本范围 INVITE，且进入相应 automatic 或 manual commencement 分支；没有互相冲突的 Answer-Mode/Priv-Answer-Mode 值。

Auto 分支要求 Answer-Mode=Auto 且本地 auto，或本地 manual 但愿意 auto，或 Priv-Answer-Mode=Auto。Manual 分支对应 Answer-Mode=Manual 且本地 manual，或本地 auto 但允许 manual，或 Priv-Answer-Mode=Manual。自动分支生成含 SDP answer 的 INVITE 200，发送后调用媒体平面；手动分支用户拒绝则480/110并停止，否则发180，发送最终200时复用自动分支的构造步骤。

- 180 不是最终接通；自动200也不是用户点击接听的证明。手动 helper 未定义全部 UI 动作及最终200触发细节。
- 客户端此段没有直接规定缺 Answer-Mode 的默认；T-PF 的已接收服务设置处理见 mcvideo/private-call-server-admission。冲突 header 的优先级不在此自造。
- Priv-Answer-Mode=Manual 在发起 O-PF 会被删除；保留终端文字不代表该值必能从本普通发起链送达。

依据：§10.2.2.2.2 steps7–8;6.2.3.1.1;6.2.3.2.1，印刷页 61、62、328。

## 进度和接通分别判断

适用条件：发起客户端收到针对本 initial INVITE 的183或200；不是 PRACK、其他事务或更新请求的200。

183 时客户端可以提示建立进度；收到 INVITE 200 后必须与 TS24.581 媒体平面交互并通知用户通话建立成功。这是 SIP 通话结果，不证明用户人工接听、已获发送许可、已获某个源的接收许可或已显示视频。

- 媒体发送/接收控制的实际状态转移须分别进入关联的 TS24.581 主题；不能把所有 SIP200 都当本事件。
- 普通失败事务重试/回退、CANCEL/BYE、会话刷新和通话持续时间不在本主题闭合。

依据：§10.2.2.2.1 response183 and response200 branches，印刷页 326。

## 证据边界

- 仅指定普通私呼分支；不覆盖全套 SIP、媒体安全、预建立、网关及优先通信行为。来源疑义按下列说明保留。

## 按需继续

- [private-call-server-admission](private-call-server-admission.md)
- [session-media-permission-boundary](session-media-permission-boundary.md)
- [participant-transmission-control](participant-transmission-control.md)
- [participant-reception-control](participant-reception-control.md)

[3GPP TS 24.281 V19.3.0 / ETSI TS 124 281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

## 原文疑义

- 10.2.2.2.2 step4d没有显式stop，而step4e限定成功验签才解封；错误Warning文字使用MIKEY-SAKE拼写，不据此改认证机制。
