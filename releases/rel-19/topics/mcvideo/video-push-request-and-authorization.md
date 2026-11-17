# 向另一客户端推视频：服务地址、目标与双边权限

## 适用范围

- 固定 3GPP TS 24.281 V19.3.0，普通在网 one-to-one video push：用户 A 指示自己的客户端向单一指定 MCVideo 用户 B 推送视频。使用按需会话及 transmission control。
- 排除 one-to-server、离网、远程发起、组推送、功能别名、预建立复用、Replaces、ambient viewing、跨系统和紧急/迫近危险扩展。没有 emergency/alert 请求，发起客户端不在 MVEPC 2/3 或该私呼 MVEPP 2，CF 没有 originating→target 的 in-progress emergency private call 状态。
- 每项动作只在所列角色收到对应事件且相应前提成立时适用；此前适用拒绝的停止规则不能因 push 专属澄清而省略。被引用私呼程序中仍带条件的分支不自动转成无条件。
- 这是信令用途及媒体接口边界，不是完整 SIP、配置、安全、push 专属媒体状态机或跨规范版本互通实现。本文不覆盖 TS 24.581 的 push 专属媒体程序，不能从普通媒体页推出 push 发送/接收资格、首帧或完整落盘。

A 是发起推送的用户，B 是指定接收用户。O-PF、T-PF 分别表示发起侧、终接侧参与功能，CF 表示控制功能，PSI 表示公共服务标识。

## 发起 push 时保留目标并使用专属会话类型

适用主体：A 客户端。

适用条件：用户要求把视频推给另一个 MCVideo 客户端；进入 §13.2.2.1。

客户端调用 §10.2.2.2.1，但 mcvideo-info 的 session-type 必须是 one-to-one video push，并与 TS 24.581 §6.2 媒体平面交互。被调用发起程序将 Request-URI 指向服务 A 的 PF 的 PSI，并在 resource-lists 的 entry uri 携带邀请目标；本范围目标是 B 的 MCVideo ID。不能借用 one-to-server 的省略接收用户列表或强制自动开始规则。

- 这里只确认 caller 及字段差异；密钥材料、SDP 编码和媒体内部行为依各自程序，不是完整 INVITE 配方。
- §13.2.2.1 的媒体交互澄清没有独立精确时序，不能推定其发生在 INVITE 200 之前或之后。

规范强度：shall。

依据：3GPP TS 24.281 V19.3.0 §13.2.2.1；§10.2.2.2.1 steps1,7,9–11,13；§13.2.2.4，印刷页 403、404、325、326。

## PF 调用私呼程序，不把条件分支抹平

适用主体：O-PF / T-PF。

适用条件：对应 PF 收到自己角色的 INVITE，session-type 为 one-to-one video push。

O-PF 调用 §10.2.2.3.1.1，T-PF 调用 §10.2.2.3.2。这里没有 one-to-server 分支的跳过 allow-private-call 及自动开始例外。但这两条 push caller 没有像 pull caller 一样明确写出将呼叫判定为 private；所调用 O-PF 程序的入口和 step5a、以及 T-PF 的若干检查仍有 session-type=private 条件。因此这里只确认调用关系和仍存在的条件，不把整个普通私呼条件检查表宣称为已闭合的 push 算法。

- 不自行把 push 字符串改成 private，亦不反推 private 条件检查必然免除。需明确规范解释或后续版本证据才能闭合该接口。
- 同版 §10.2.2.3.1.1 step13a 的有条件改写不能反向补全入口、先前分类或 push 路由；F.1.3 区分 private 与 one-to-one video push 类型。这些后续条件和字段语义仍未消除上述分类疑点。

规范强度：shall。

依据：3GPP TS 24.281 V19.3.0 §13.2.3.1.1；§13.2.3.1.2；§13.2.3.1.4；§10.2.2.3.1.1 opening and step5a；§10.2.2.3.2 step3；§12.2.3.1.1；§12.2.3.1.2，印刷页 404、405、332、341、401。

依据：3GPP TS 24.281 V19.3.0 §10.2.2.3.1.1 step13a；§F.1.3。

## CF 先验服务地址，再分别核两侧 push 权限

适用主体：CF。

适用条件：CF 收到对应 INVITE，session-type 为 one-to-one video push。

CF 依次检查 Request-URI 中的 PSI 是否分配用于 one-to-one video push；若不是，调用 §6.3.7.1 并停止余下步骤。该 helper 对本功能未分配的 PSI 返回 404。随后分别核 mcvideo-calling-user-id 所示用户能否发起 push，以及 mcvideo-called-party-id 所示用户能否接收 push 呼叫；任一未授权，返回 403 和规定 Warning，并停止。通过后分配 MCVideo session identity，并按 §10.2.2.4.1 邀请 resource-lists 的 entry uri 所列用户。

- PSI 检查是 push 服务用途检查，不能从普通 private CF 地址可达反推通过。
- 授权检查读取 called-party-id，而邀请读取 resource-lists；本段未定义两者冲突的消解策略，不能只保留一个字段。
- 本段没有列出 push 专属配置叶或具体 Warning 数字，不从其他业务借值。
- §6.3.7.1 的文字前提是 PSI 未分配于该 PF/CF；对已分配但用于不同用途的 PSI，保留 caller→helper 的条件差异，不补错误码规则。

规范强度：shall。

依据：3GPP TS 24.281 V19.3.0 §13.2.3.2.1 steps1–5；§6.3.7.1，印刷页 405、140。

## 通过准入后，邀请路由与接通观察分开

适用主体：CF。

适用条件：§13.2.3.2.1 step5 已进入 §10.2.2.4.1；本页的普通、单一直接 ID 范围成立。

CF 按所调用程序生成 INVITE，把收到的资源列表目标 MCVideo ID 放入出站 mcvideo-request-uri，并将 Request-URI 指向该目标用户的 T-PF PSI；出站 P-Asserted-Identity 为 CF PSI，SDP offer 基于入站 offer。发送 INVITE 后，以用户配置的最大私呼时长启动 private call timer。收到该 INVITE 的 200 时保存 Contact 并与媒体平面交互；计时器到期进入 §10.2.5.4。

- CF 专属 push 准入没有调用 §10.2.2.4.2；不能复制 pull 的整个 CF helper 关系。
- 不提供 T-PF PSI 的发现算法、最大时长默认值或 Contact 保存之外的完整应答转发规则。
- 进入邀请或收到该段 200 不证明 B 已显示或保存视频。

规范强度：shall。

依据：3GPP TS 24.281 V19.3.0 §13.2.3.2.1 step5；§10.2.2.4.1 steps1,3–5,7–9 and response200/timer branches，印刷页 405、343、344。

## 条款差异与解释边界

§13.2.3.1.1/.2 versus 10.2.2.3.1.1 opening/step5a and 10.2.2.3.2 step3，印刷页 404、405、332、341：push 只调用私呼程序，未像 pull §§12.2.3.1.1/.2 明写判定为 private；被调用程序仍保留 private 字符串/分类条件。 保留精确调用，不把条件抹平或自行改 session-type；不声称完整 PF 分类/准入算法已闭合。 同版 §10.2.2.3.1.1 step13a 的有条件改写不能反向补全入口、先前分类或 push 路由；F.1.3 区分 private 与 one-to-one video push 类型。这些后续条件和字段语义仍未消除上述分类疑点。

§13.2.3.2.1 step1 versus 6.3.7.1，印刷页 405、140：caller 检查是否分配用于 push，helper 文字检查是否分配于该功能；后者明确 404，前者已分配但用途不同的具体规则未另写。 保留两个前提及调用关系，不额外定义跨用途 PSI 的响应。

§13.2.3.2.1 steps3,5，印刷页 405：被叫授权读取 called-party-id，实际邀请读取 resource-lists entry uri；本段没有给不一致消解规则。 保留两字段，不能把它们合成一个未经验证的目标身份或另造拒绝码。

## 未覆盖的行为

- PF 分类及 push 专属 PSI 的发现、映射仍未闭合。
- 本页未覆盖 TS 24.581 的 push 专属媒体许可、实际发送和接收控制、首帧交付与文件完整性。
- 不覆盖配置 schema 和默认值、完整 KMS/SRTP、SIP 事务实现、one-to-server、远程或离网推送。

## 按需继续

- [收到推视频邀请：提示、接听、可选录制与释放证据](video-push-observation-and-release.md)
- [MCVideo 按需私呼：客户端邀请、应答与接通证据](private-call-client-signalling.md)
- [MCVideo 私呼服务器链：身份准入、终接设置与逐段应答](private-call-server-admission.md)
- [向另一客户端拉视频：请求角色与双边授权](video-pull-request-and-authorization.md)

[3GPP TS 24.281 V19.3.0，ETSI 官方发布版](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅适用于所列版本和条款。
