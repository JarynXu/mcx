# 收到推视频邀请：提示、接听、可选录制与释放证据

## 适用范围

- 固定 3GPP TS 24.281 V19.3.0，普通在网 one-to-one video push：用户 A 指示自己的客户端向单一指定 MCVideo 用户 B 推送视频。使用按需会话及 transmission control。
- 排除 one-to-server、离网、远程发起、组推送、功能别名、预建立复用、Replaces、ambient viewing、跨系统和紧急/迫近危险扩展。没有 emergency/alert 请求，发起客户端不在 MVEPC 2/3 或该私呼 MVEPP 2，CF 没有 originating→target 的 in-progress emergency private call 状态。
- 每项动作只在所列角色收到对应事件且相应前提成立时适用；此前适用拒绝的停止规则不能因 push 专属澄清而省略。被引用私呼程序中仍带条件的分支不自动转成无条件。
- 这是信令用途及媒体接口边界，不是完整 SIP、配置、安全、push 专属媒体状态机或跨规范版本互通实现。本文不覆盖 TS 24.581 的 push 专属媒体程序，不能从普通媒体页推出 push 发送/接收资格、首帧或完整落盘。

A 是发起推送的用户，B 是指定接收用户。O-PF、T-PF 分别表示发起侧、终接侧参与功能，CF 表示控制功能，PSI 表示公共服务标识。

## 显示 push 提示是义务，保存文件是选择

适用主体：B 客户端。

适用条件：收到 one-to-one video push 的 initial INVITE；进入 §13.2.2.2。

B 调用 §10.2.2.2.2，并须向用户显示这是 one-to-one video push 呼叫；B 可以把 MCVideo 媒体流保存为文件。该 MAY 不是必须录制、文件完整性承诺或已经落盘的证据。

- 提示本身不是用户接受，也不是收到首帧；所调用终接过程的拒绝与停止规则仍需按自身条件处理。
- 源条文未给提示动作相对拒绝检查的独立时序；不强制插入一个未规定的先后。
- 这是接收客户端可保存，不是 one-to-server 中 CF 必须存档的规则。

规范强度：display shall; save may。

依据：3GPP TS 24.281 V19.3.0 §13.2.2.2，印刷页 404。

## push 不自动绕过终端拒绝或人工接听

适用主体：B 客户端。

适用条件：进入所调用 §10.2.2.2.2；应答模式头与本地设置满足相应分支，没有冲突模式值。

终端仍可因占用且同时会话数超过配置上限、资源不足或规范外原因拒绝；选择拒绝后按规定返回错误和 Warning，只有用户获准隐藏失败原因时才可用不带 Warning 的 480，并停止。未被停止的路径中，Auto 头加本地 auto，或本地 manual 但愿意 auto，或 Priv-Answer-Mode=Auto，进入自动 helper；Manual 头加本地 manual，或本地 auto 但允许 manual，或 Priv-Answer-Mode=Manual，进入手动 helper。手动分支用户拒绝时 480/110 并停止，否则发 180；发送最终 200 时复用自动 helper。

- push 专属条款没有强制自动接听。显示 push 提示与接受、允许录制不是同一个判断。
- 保留 exceeds 而非改成大于等于；既有私呼安全分支也没有被 push 取消。
- 模式缺失、冲突头与完整 UI 时序不在此推导；Priv-Manual 在终端文本出现不证明它能经本发起 PF 路径传到终端。

规范强度：resource rejection may; chosen rejection/conditional commencement shall。

依据：3GPP TS 24.281 V19.3.0 §13.2.2.2；§10.2.2.2.2 steps1–2,7–8；§6.2.3.1.1；§6.2.3.2.1，印刷页 404、327、328、61、62。

## INVITE 200 与视频接收、保存分别判断

适用主体：A 客户端。

适用条件：收到针对本 push 初始 INVITE 的 183 或 200，普通非紧急范围成立。

继承发起程序：183 时可以提示建立进度；200 时须与媒体平面交互并通知用户通话已成功建立。信令成功不等于发送已获准、B 已获接收许可、已解码首帧或可选文件已完整保存。

- §13.2.2.1 指向 TS 24.581 §6.2，实际 push 专属媒体状态转移不在本页覆盖范围；不从私呼、pull 或广播媒体角色推导唯一接收集合。

规范强度：183 notification may; 200 interaction/notification shall; delivery distinction is bounded inference。

依据：3GPP TS 24.281 V19.3.0 §13.2.2.1；§10.2.2.2.1 response183 and response200，印刷页 403、326。

## 客户端与服务器释放沿各自入口，不等于录制完成

适用主体：客户端 / PF / CF。

适用条件：对应客户端处于 ongoing one-to-one video push 并收到用户释放指示；PF 收到相应方向 BYE；或 CF 判定需释放。各条件分别应用。

用户释放调用 §10.2.4.1；按需客户端 helper 先与媒体平面交互，再向服务器发送以待释放 session identity 为 Request-URI 的 BYE，收到本 BYE 的 200 后再次交互。PF 从客户端收到 BYE 时调用 §10.2.4，从 CF 收到 BYE 时调用 §10.2.5。CF 则由 §13.2.3.2.2 调用 §10.2.5.4；其政策依据 §6.3.8.2，在媒体 T4(Inactivity) 到期指示、超过私呼最长时长或仅剩一人/无人时要求释放。

- 不把 BYE 的 200 当作双端播放器停止、清缓存或文件写入完成；建立前 CANCEL 不在此用途。
- 保留原文 T4(Inactivity) 称谓，不与既有媒体授权重传 T4 或单流 T11 自动对应。
- §10.2.5.4 指向 §6.3.3.1.5，但该编号为紧急组 re-INVITE，BYE helper 在 §6.3.3.1.4；只保留政策与实际引用，不静默纠正而宣称完整 CF 释放链。

规范强度：shall。

依据：3GPP TS 24.281 V19.3.0 §13.2.2.3；§13.2.3.1.3；§13.2.3.2.2；§10.2.4.1.1.1；§6.2.5.1；§10.2.5.4；§6.3.8.2，印刷页 404、405、352、63、353、140。

## 条款差异与解释边界

§10.2.5.4 → 6.3.3.1.5，印刷页 353、104：释放 caller 指到紧急组 re-INVITE 条款；同页 BYE helper 的编号是 6.3.3.1.4。 在 push 使用处保留该引用歧义，不擅自修正规范或据此宣称完整 CF 释放链。

## 未覆盖的行为

- PF 分类及 push 专属 PSI 的发现、映射仍未闭合。
- 本页未覆盖 TS 24.581 的 push 专属媒体许可、实际发送和接收控制、首帧交付与文件完整性。
- 不覆盖配置 schema 和默认值、完整 KMS/SRTP、SIP 事务实现、one-to-server、远程或离网推送。

## 按需继续

- [向另一客户端推视频：服务地址、目标与双边权限](video-push-request-and-authorization.md)
- [MCVideo 私呼释放：客户端 BYE 与媒体停止、资源回收](private-call-client-release.md)
- [MCVideo 私呼逐段释放：PF、CF的BYE处理与引用边界](private-call-server-release.md)
- [MCVideo 会话、媒体协商与发流/收流许可的边界](session-media-permission-boundary.md)

[3GPP TS 24.281 V19.3.0，ETSI 官方发布版](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅适用于所列版本和条款。
