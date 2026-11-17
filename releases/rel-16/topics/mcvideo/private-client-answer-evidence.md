# 普通按需 MCVideo 私呼：客户端请求、应答与结果证据

## 适用范围

- 固定 TS24.281 V16.12.0 的在网、带传输控制、直接 MCVideo ID 一对一私呼；不含组呼、离网、功能别名、视频推拉或远程 ambient。
- 主叫不处于 MVEPC2、MVEPC3 或该私呼 MVEPP2 的优先入口，接收请求没有 emergency-ind=true；本页是普通按需初始 INVITE，不是 re-INVITE、预建立承载或 Replaces 替换。
- 发起、接收、拒绝、应答、结果和取消按各角色实际事件分别适用；不把全链检查成功或最终收到 200 作为共同前提。

## 主叫请求一个用户，路由到自己的服务 PF

条件：主叫用户要求建立本页范围的私呼；端到端安全上下文、隐式媒体发送请求各按自己的条件触发。

初始 INVITE 的 Request-URI 是服务主叫的参与功能 PSI，资源列表携一个被叫 MCVideo ID，mcvideo-info 的 session-type 为 private。请求带 MCVideo 特征及服务标识，并按 §6.2.1 提供音频、视频和媒体传输控制流的 SDP offer。用户要求强制自动应答时写 Priv-Answer-Mode=Auto；未要求强制时，按用户请求写 Answer-Mode=Auto 或 Manual。需要建立端到端安全上下文时执行本段 PCK/MIKEY-SAKKE 构造依赖。要求隐式发送时须满足 §6.4：本页非远程 ambient 会话的传输控制 UDP 流带 mc_implicit_request，才作为主叫隐式发送请求。请求不等于媒体发送已获许可。

强度：上述条件构造和发送 SHALL；P-Preferred-Identity 为 MAY。

- 不把业务被叫 ID 当作初始 Request-URI。§6.3.1.1 的 PF/CF INVITE 分类是服务器路由角色，不能用 MESSAGE 分类代替客户端初始 INVITE 入口。
- 模式头是请求，不证明服务器已授权强制应答；本页不展开完整 PF/CF 许可矩阵。
- 安全上下文条件不等于每次呼叫都重新取密钥；§6.2.8.3.9、TS33.180 的完整密钥服务与算法未展开。§6.6 的 XML 保护义务仍适用，不因本页只列部分构造而省略。

依据：TS24.281 V16.12.0 §10.1;10.2.1;10.2.2.1；§10.2.2.2.1 steps1–13；§6.2.1；§6.3.1.1 INVITE classification (role comparison)；§6.4 initial non-ambient branch；§6.5;6.6.1.1–3 (protection dependencies)，印刷页 42, 43, 61, 62, 107, 108, 267, 268, 269。

## 被叫拒绝和密钥检查是应答前的不同事件

条件：被叫收到本页初始 INVITE。资源拒绝按 steps1–2；密钥验证仅在 SDP a=key-mgmt 含 MIKEY-SAKKE I_MESSAGE 时适用；不要求先通过这些检查才进入本条。

正占用其他会话且同时会话数超过 Max-Simul-Call-Nc10、资源不足或规范范围外原因时，客户端可拒绝。拒绝应返回适当响应及 Warning；若获准限制失败原因，可用不带 Warning 的 480，随后跳过本节其余步骤。携所述 MIKEY 时按发起者 ID 派生 UID 并验签；失败返回 488 和 Warning136，成功才解封 PCK 并取得 PCK-ID。密钥验证成功不等于用户接受邀请。

强度：所列资源/其他原因拒绝为 MAY；选择拒绝后的响应及停止、条件性密钥处理为 SHALL。

- §10.2.2.2.2 step4 的失败分支未另写 skip-rest，不能把 step2 的明示停止文字移到该分支来补事务算法。
- Warning136 原文写 MIKEY-SAKE，而同段消息名称为 MIKEY-SAKKE；本页不据此创建另一算法。缺少该 MIKEY 输入时，不从此条件分支推导统一接受或拒绝规则。
- TS24.484 配置与 TS33.180 完整安全实现未在本页展开。

依据：TS24.281 V16.12.0 §10.2.2.2.2 steps1–4 (step3 emergency scope comparison)，印刷页 269, 270。

## 按被叫模式条件选择应答，180 不是最终 200

条件：被叫已到达 §10.2.2.2.2 steps7–8 的模式处理；其后的自动处理、手动拒绝、发送最终响应分别是事件入口。服务器按需承载边界见本条限制，不要求所有模式同时成立。

Answer-Mode=Auto 且本地自动，或本地手动但愿意自动应答，进入自动 helper；Priv-Answer-Mode=Auto 也是入口。Manual 对应本地手动，或本地自动但允许手动，以及 Priv-Answer-Mode=Manual。自动 helper 构造并发送 200，带 timer、会话计时和 SDP answer 等要求，然后交接 TS24.581 媒体过程；本页无 Replaces 时使用 §6.2.2 的 answer。手动 helper 中用户拒绝则返回 480/Warning110 并停止；其余生成并发送 180，发送最终 200 时调用同一自动 helper。这个调用不把原来的人工选择改成自动应答。

强度：所述模式条件成立后的 helper、响应及媒体交接 SHALL。

- 终接 PF 的模式入口另见 §10.2.2.3.2：Answer-Mode 指定值、缺少该头且保存设置对应、或 Priv-Answer-Mode 指定值，分别进入对应 helper；这不替代客户端自身条件。
- §6.3.2.2.5.1 与 .6.1 在空闲预建立会话、视频参数匹配、传输控制参数匹配三项同时成立时选预建立分支，否则才选按需。本页不展开预建立或 Replaces 替换。
- 不补冲突模式头的优先算法。相邻组呼手动 helper 的 183/Unconfirmed 不能移植为本私呼客户端行为。完整会话计时、NAT/RFC 事务实现未闭合。

依据：TS24.281 V16.12.0 §10.2.2.2.2 steps7–8；§6.2.2；§6.2.3.1.1 full (Replaces comparison)；§6.2.3.2.1 full;6.2.3.2.2 (group comparison)；§10.2.2.3.2 steps7–8 (server-mode comparison)；§6.3.2.2.5.1;6.3.2.2.6.1 (bearer selection comparison)，印刷页 43, 44, 45, 46, 71, 73, 270, 271, 282。

## 主叫进展提示、建立提示和媒体结果分开

条件：主叫收到其初始 INVITE 的 183，或收到该 INVITE 的 200；两个事件分别适用，不要求先收到 183 才处理 200。

收到 183 时主叫可向用户提示建立进展；收到 200 时须交接 TS24.581 媒体过程，并提示私呼已成功建立。这是信令结果及后续调用，不是已经验证视频传输、接收呈现或完整媒体许可。

强度：183 的进展提示 MAY；200 的媒体交接与建立提示 SHALL。

- 不据此保证被叫人工接听；自动应答同样会产生最终响应。本页不从主叫提示反推全部服务端、媒体或用户动作。
- 普通错误恢复、ACK/PRACK 全事务及建立后生命周期不在本页。§10.2.2.2.1 的优先状态后续分支不纳入普通主链。

依据：TS24.281 V16.12.0 §10.2.2.2.1 183/200 response branches (priority-state comparison)；§6.2.3.1.1;6.2.3.2.1 (client answer comparison)，印刷页 44, 45, 269。

## 取消事务的 200 不接受原 INVITE

条件：被叫收到取消该 INVITE 的 CANCEL；本地已有该 INVITE 对话，且尚未向 INVITE 发送 200。

客户端向 CANCEL 返回 200，向原 INVITE 返回 487。这两个响应属于不同请求，取消事务成功不能记成私呼建立成功。

强度：满足条件后的两个响应 SHALL。

- 已向 INVITE 发出 200 不满足此分支；本页不从 CANCEL 推导建立后 BYE 释放、媒体清理或完整竞争时序。

依据：TS24.281 V16.12.0 §10.2.2.2.2 CANCEL branch，印刷页 271。

## 本页边界

- 本页覆盖客户端建立主链和必要的模式/承载范围对照，不是完整端到端服务器实现、媒体许可或全部生命周期。
- 技术依据只取本固定 Release16 版本。TS24.229、TS24.484、TS33.180、TS24.581 及 RFC 的完整实现仍是依赖；本页不以其他 Release 或 MCPTT 规则补足。

[固定版本来源](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/16.12.00_60/ts_124281v161200p.pdf)
