# 普通按需私呼：服务器准入与身份路由

## 适用条件

- 固定 TS24.379 V16.14.0 的主系统在网、带话权控制、直接 MCPTT ID 普通 private 私呼；不含 first-to-answer、功能别名、环境监听、转发或转接。
- 本页限定无 emergency-ind/alert-ind 的普通初始请求、无紧急 Resource-Priority 值，且主叫不处于与目标用户的进行中紧急私呼状态；终端使用按需会话，不覆盖预建立或 Replaces 替换。
- 各角色的接收、准入失败、继续构造与响应是分别适用的事件入口，不以全链许可、成功响应或被叫接受作为全页前提。

## 先识别发送者，再选择主叫的私呼服务

适用：O-PF 收到 session-type=private 的初始 INVITE；拒绝与继续构造分别依其到达的步骤适用。

O-PF 由入站 P-Asserted-Identity 的公共用户身份查主叫 MCPTT ID，再确定与该主叫身份关联的私呼 CF 服务 PSI，而不是按资源列表中的被叫身份选择主叫服务。无法确定 CF 时返回 404+Warning142 并停止；缺少资源列表正文或 private 列表多于一个 entry，分别返回 403+Warning145 并停止。到达构造步骤后，Request-URI 写所选 CF PSI，mcptt-calling-user-id 写确定的主叫 MCPTT ID；通用 INVITE helper 复制入站 P-Asserted-Identity。服务目的地址、主叫业务身份和被叫列表不是同一标识。

规范强度：所述身份确定、构造、条件拒绝及停止为 SHALL。

- 边界：主叫绑定与基本私呼/模式许可仍须经过前序检查，见客户端应答页；这里不以通过这些检查作为拒绝分支的共同前提。
- 边界：所列资源列表错误明确是正文缺失或多于一个 entry，不将它改写为所有“非恰好一个 entry”均按同一规则拒绝；这也不证明零 entry 有效。

依据：TS24.379 V16.14.0 §6.3.1.1 O-PF/private-CF classification；§11.1.1.3.1.1 opening,steps3–10,15–17,22；§6.3.2.1.3 steps4,7–8；§11.1.1.4.2 steps6–9 (ordinary scope comparison)；§11.1.1.4.1 step7 (existing emergency state comparison)，印刷页 77, 78, 84, 85, 366, 367, 368, 369, 379, 380, 381。

## 通用私呼许可不代替目标名单和媒体准入

适用：O-PF 到达普通 private 的名单检查或后续 SDP 检查；各检查依程序顺序发生，不要求后续检查已成功。

当主叫配置的 PrivateCall 存在且含 entry、请求目标 URI 不匹配其中任何 entry、又未配置允许呼叫名单外用户时，O-PF 返回 403+Warning144 并停止。这是三项同时成立的拒绝，不把名单缺失等同于禁止所有目标。后续若 SDP offer 未提供任何 MCPTT speech codec，则返回 488；有相应 codec 才继续。CF 还有自己的媒体检查：收到的 offer 须至少有一个媒体流，其参数以及至少一种 codec 或媒体格式可由 CF 接受，否则返回 488 并停止，不能用 O-PF 的检查替代。

规范强度：所述名单条件拒绝、codec 检查及 CF 条件拒绝为 SHALL。

- 边界：未触发某一名单拒绝不等于其余服务许可、CF 授权或被叫入向名单均通过。
- 边界：配置文档如何创建和更新不在此展开；这里依据本版呼叫控制程序使用配置的条件，不补配置缺省。

依据：TS24.379 V16.14.0 §11.1.1.3.1.1 steps10–14 (FTA steps12–13 comparison)；§11.1.1.4.2 step5，印刷页 367, 368, 380。

## 强制自动应答有独立许可，Manual 不照搬

适用：O-PF 已到达 §11.1.1.3.1.1 step18 的 private 头处理；按实际收到的模式头分别适用。

收到 Priv-Answer-Mode=Manual 时，O-PF 不在出站请求包含该 Priv-Answer-Mode。收到 Priv-Answer-Mode=Auto 且 allow-force-auto-answer 缺失或 false 时，返回 403+Warning143 并停止；该配置为 true 且收到 Auto 时，出站才包含 Priv-Answer-Mode=Auto。若出站未包含该 Auto 头且入站存在 Answer-Mode，则复制其内容。这项强制许可不同于普通 Answer-Mode 的 Auto/Manual 发起许可。

规范强度：所述头处理、条件拒绝和停止均为 SHALL。

- 边界：step18(d) 原文把“未包含 Auto”的前序回指为 step17，而 step17 实际设置 calling-user-id；此处保留该号次差异，不默改规范引用。
- 边界：本页不补冲突模式头的通用优先算法，也不把主叫有强制许可解释为已经完成客户端应答。

依据：TS24.379 V16.14.0 §11.1.1.3.1.1 steps11(a–b),17–18；§6.3.3.1.2 steps8–10 (downstream and ambient comparison)，印刷页 367, 368, 369, 106。

## CF 分开校验服务、授权主叫与邀请被叫

适用：CF 收到 private 初始 INVITE，或通过其前序检查而到达实际邀请动作；这两个阶段分别适用。

CF 检查 Request-URI 的 PSI 是否分配给私呼，未分配则调用未分配 PSI 错误过程返回 404 并停止；同时按 calling-user-id 验证主叫并作本地授权，未获授权返回带 Warning 的 403 并停止。资源列表缺失或 private 多 entry 各为 403+Warning145 并停止。通过相应前序检查后，CF 按接收 helper 缓存收到且支持的 Contact feature tags，分配会话身份，并由 §11.1.1.4.2 step12 的 otherwise 分支调用 §11.1.1.4.1 邀请列表中的用户。下行 mcptt-request-uri 写被叫 MCPTT ID，Request-URI 写服务该被叫的 T-PF PSI；P-Asserted-Identity 仍复制主叫公共身份。CF 通用 INVITE helper 在 Contact 放会话身份及 isfocus，并复制 mcptt-info，因此 calling-user-id 得以随请求传递。

规范强度：所述校验、条件拒绝、缓存、会话身份分配及邀请字段构造为 SHALL。

- 边界：§11.1.1.4.2 step4 在 CF 程序内将被拒请求称为 originating participating function 的请求；这是本版称谓差异，不据此迁移执行角色。
- 边界：§11.1.1.4.1 NOTE2 明确 T-PF 地址如何发现不在本 Release 范围；本页不提供发现算法。
- 边界：通用 helper 及 caller 还涉及 SDP、计时等责任；本节说明身份与实际调用，不是可直接照抄的完整 INVITE 模板。

依据：TS24.379 V16.14.0 §6.3.1.1 private-CF classification；§11.1.1.4.2 steps1–12 (FTA/emergency comparison)；§6.3.7.1；§6.3.3.2.2 full；§11.1.1.4.1 opening,steps1,4–6,NOTE1–3；§6.3.3.1.2 steps1,11，印刷页 77, 78, 105, 106, 120, 136, 378, 379, 380, 381。

## T-PF 看被叫绑定和入向主叫名单

适用：T-PF 收到本页 private 初始 INVITE；模式选择前的各拒绝入口分别适用，不以被叫已接受为前提。

T-PF 检查 Contact 的 isfocus，缺失则返回 403+Warning104 并停止；从 mcptt-request-uri 取被叫 MCPTT ID 来查公共用户身份绑定。被叫绑定和服务设置的前置检查之后，入向名单检查比较的是 calling-user-id：IncomingPrivateCallList 存在且非空、主叫不匹配任何 entry、又未配置允许名单外主叫呼入时，返回 403+Warning159 并停止。出向 Warning144 与入向 Warning159 检查不同用户的配置和不同对象，不能因主叫名单允许目标便跳过被叫的入向限制。到达模式分派后才调用自动或手动 helper；按需承载选择与最终客户端应答见客户端应答页。

规范强度：所述 isfocus 检查、绑定检索、条件名单拒绝和模式 helper 调用为 SHALL。

- 边界：不存在或空的入向名单不满足本条 Warning159 守卫，但不据此推导呼入必然成功。
- 边界：§11.1.1.3.2 step6 的不能参与配置拒绝为 403+Warning127，原段未另写停止；不从相邻步骤补出停止措辞。

依据：TS24.379 V16.14.0 §6.3.1.1 T-PF classification；§11.1.1.3.2 steps2–8；§11.1.1.3.1.1 step11(c) (outgoing comparison)；§6.3.2.2.5.1 full;6.3.2.2.6.1 full (on-demand selection dependency)，印刷页 77, 78, 95, 96, 98, 367, 368, 376, 377。

## 可靠 183 的 PRACK 和被叫最终响应：哪个 200 要等？

先认事务：**PRACK 的 200** 是 T-PF 对可靠临时响应确认请求的答复；**INVITE 的 200** 是建立呼叫的最终响应。再认方向：被叫终端向 T-PF 回的 INVITE 200、T-PF 向 CF 发的 INVITE 200、CF 向主叫方向发的 INVITE 200，各应答本段的请求。本节限同系统、双方都按需建立、直接按 MCPTT ID 呼叫且有话权控制的普通一对一私呼。

**T-PF 何时生成 183？** 入向检查通过并选中自动模式后，若被叫有空闲预建立会话、语音媒体段匹配、话权控制媒体段匹配三项不同时成立，T-PF 执行按需程序。以下任一条件成立，T-PF 须为入向 INVITE 生成 P-Answer-State 为 Unconfirmed 的 183：

- 收到 Priv-Answer-Mode: Auto。
- 两种模式头都未收到，且 T-PF 此前从被叫终端收到的应答设置为 auto-answer。
- 收到 Answer-Mode: Auto，且该被叫设置为 auto-answer。

这份 183 不带 SDP，可靠或不可靠发送都一样。若入向 INVITE 含 Supported: 100rel，临时响应条款允许 T-PF 按本地策略加 Require: 100rel，并非必须加。规范还规定 T-PF 生成并发送给被叫终端的 INVITE。**生成 183** 不等于**已经发送**或 **CF 已收到**；这些步骤没有写明必须先发出 183 才能向终端发 INVITE。[§11.1.1.3.2，印刷页 376–377](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=377)；[§6.3.2.2.4.1(3)、§6.3.2.2.5.1，印刷页 95–96](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)；[§6.3.2.2.5.2(1)及注、(3)、(11)，印刷页 96–97](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=97)。

**T-PF 已收到被叫终端对本次 INVITE 的 200，何时向 CF 发 INVITE 200？** 要看 T-PF 先前实际发送的 183。

| T-PF 此时的记录 | T-PF 的动作 |
| --- | --- |
| 183 已不可靠发送 | 立即发送 INVITE 200。 |
| 183 已可靠发送；对应的 PRACK 已收到，且 PRACK 的 200 已发出 | 立即发送 INVITE 200。 |
| 183 已可靠发送；对应的 PRACK 尚未收到 | 等到该 PRACK 实际到达，先生成并发送 **PRACK 200**，再发送 **INVITE 200**。 |

可靠 183 的 PRACK 一到，T-PF 就有单独的应答义务，不以先收到终端的 INVITE 200 为条件。若没有实际发送过 183，或 PRACK 已收到但还没发出它的 200，上表没有为这两种情况另定发送时刻。

发给 CF 的 INVITE 200 由 T-PF 重新生成：依据终端所回答的 SDP 生成本段 SDP 应答，复制入向 200 的 P-Asserted-Identity；先前**实际发送**了带 Unconfirmed 的 183 时，须在本段最终响应设置 P-Answer-State: Confirmed。随后与媒体面交互并发送。该条件不是对其余情形一律禁止带头的规定。手动按需模式另按被叫实际返回的 180 或 INVITE 200 重建相应响应，不把自动模式的等待表套到手动模式，也不据此断言手动模式禁用 PRACK。[§6.3.2.2.5.2，印刷页 97](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=98)；[§6.3.2.2.6.2，印刷页 99–100](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=100)。

**CF 在什么条件下向主叫方向发首个最终响应？** 这与它是否要向 T-PF 发 PRACK 是两个判断。CF 实际收到对其出向 INVITE 的 183，且同时有 Require: 100rel 和 P-Answer-State: Unconfirmed，须向终接网络发 PRACK。此条件不要求 CF 支持媒体缓冲。[§11.1.1.4.1，印刷页 379](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=380)。

- **由 183 触发：**CF 实收对应的 183/Unconfirmed、会话类型是 private、CF 支持媒体缓冲，且尚未向主叫方向发最终响应。它须生成 INVITE 200，加入对入向 offer 的 SDP 应答和 Unconfirmed，与媒体面交互并发向主叫方向。这个 200 是**最终响应**，不是另一份临时响应。该分支不要求 Require: 100rel、PRACK 的 200 或被叫终端的 INVITE 200；不能据此反推被叫终端当时一定还没回包。[§11.1.1.4.2，印刷页 381–382](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=382)。
- **由被叫方向的 INVITE 200 触发：**CF 实收与出向 INVITE 匹配的 200，对话由 session-type=private 的初始 INVITE 建立，并且 CF 尚未向主叫方向发最终响应。CF 生成对入向 INVITE 的首个 200，加入 SDP 应答；注 2 明说本次媒体面处理完成后才发响应。本分支的 SDP 回指写作 §6.3.3.2.2（该节是接收初始 INVITE 时缓存受支持的 Contact 特性），SDP 应答专节则是 §6.3.3.2.1；保留两处差异。若此前已发过 Unconfirmed 最终响应，不能用本分支再发第二个最终响应。CF 按 §11.1.1.4.1 实收出向 INVITE 的 200，仍须缓存收到的 Contact 并与媒体面交互。[§11.1.1.4.2，印刷页 382](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=383)；[§6.3.3.2.1–2，印刷页 119–120](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=120)；[§11.1.1.4.1，印刷页 379](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=380)。

T-PF 设置 Confirmed，不等于 CF 的普通最终响应条款要求把它原样复制。O-PF 是在自己的入向 200 **确实带** P-Answer-State 时才须按第 5A 项带回该值。主叫一侧没见到 Confirmed，不能据此判定被叫没回 200 或某个服务器漏传。要辨别是哪一支，分别核对 INVITE 和 PRACK 的对应响应、T-PF 的收发及 CF 此前是否已发最终响应；即使已见某一侧发出 200，也不能单凭它确认另一侧实收、用户人工接听、获得话权或已有 RTP 收发。[§11.1.1.3.1.1 最终响应第 5A 项，印刷页 370](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=371)。

## O-PF 重建响应并映射会话身份，不是一律透传

适用：替代事件：O-PF 收到该 INVITE 的 180；收到 200；或收到其他不含 SDP 的响应。不要求三类响应都出现，也不以被叫人工接受为共同前提。

收到 180 时，O-PF 调用临时响应 helper，带入收到的 P-Asserted-Identity 和 Warning 后返回主叫。收到 200 时，调用最终响应与 SDP answer helper，带入收到的 Warning 和 P-Asserted-Identity，并包含与收到的 Contact 会话身份相映射的 MCPTT 会话身份；收到 P-Answer-State 时也带入其值，发送后交接媒体并启动会话计时。其他响应的通用转发规则明确限于不含 SDP，并包含其中的 MIME 正文，不是所有响应无条件原样透传。最终 helper 还要求 timer/Session-Expires、Contact tags、tdialog/norefersub 及条件复制 mcptt-info，Resource-Share 则可选。

规范强度：所述条件响应构造、身份/状态携带、发送、媒体交接和计时为 SHALL；helper 中 Resource-Share 为 MAY。

- 边界：会话身份映射不把业务用户 ID、服务器 PSI 和 Contact 会话身份变为同一值。200 与被叫人工接受的证据区别由客户端应答页说明，本条不替代该判断。
- 边界：CF 在 private、收到 200 且尚未向主叫发送最终响应的分支，将 SDP answer 回指 §6.3.3.2.2；该段实际为接收 INVITE 时缓存 feature tags，SDP answer 专节是 §6.3.3.2.1。此处保留引用差异，不替规范补出完整 CF SDP 实现。
- 边界：不据这条 O-PF 规则推导其他角色、含 SDP 错误响应或完整恢复流程。

依据：TS24.379 V16.14.0 §11.1.1.3.1.1 response branches；§6.3.2.1.5.1 full;6.3.2.1.5.2 full；§6.3.2.1.2.1 full；§11.1.1.4.2 private 183/Unconfirmed and private 200 branches (response evidence comparison)；§6.3.3.2.1;6.3.3.2.2 (SDP reference comparison)，印刷页 84, 86, 87, 119, 120, 370, 381, 382。

## 主叫收到 480：服务器拒绝了邀请，还是被叫用户拒接？

先找**哪一方对哪份 INVITE 生成了 480**。终接侧参与功能（T-PF）既接收控制功能（CF）的 INVITE，也可能另发一份 INVITE 给被叫终端。它回给 CF 的 480，可能由它自己生成，也可能来自被叫方向。以下限同系统、双方按需、直接用 MCPTT ID 呼叫、带话权控制的普通一对一私呼。

**T-PF 本地拒绝，不需要被叫终端先收邀。** T-PF 实收 CF 侧初始 INVITE，到 §11.1.1.3.2 第 3 项时，会话类型为 private，而且 T-PF 还没有从被叫终端发布的 application/poc-settings+xml 收到 Answer-Mode Indication（该项引用 §7.3.3 或 §7.3.4），就必须向这份入向 INVITE 回 480，在 Warning 文本中给出 146，并停止本程序。此处缺的是**被叫的服务设置**，不是 INVITE 缺少 Answer-Mode 头，也不是在判定 IMS 注册失败。按来件 mcptt-request-uri 中的被叫 MCPTT ID 去查公共用户身份绑定，是后面的第 4、5 项；不能用绑定缺失解释第 3 项的 146。这条本地拒绝不执行后面的被叫侧 INVITE 发送步骤。[§11.1.1.3.2，第 3–5、7–8 项，印刷页 376–377](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=377)。

**被叫终端实际收到了 T-PF 为它发送的 INVITE。** 此时还要区分谁作了拒绝决定：

- **用户明确拒接。** 终端进入手动应答程序，用户明确拒绝这份邀请，终端必须向服务器回 480，Warning 文本给出 110，并停止该手动应答程序。不要求先有 180；看到过 180 也不说明用户后来拒接。[§11.1.1.2.1.2 第 10 项，印刷页 358](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=359)；[§6.2.3.2.1，印刷页 59](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=60)。
- **终端自行拒绝。** 终端因正在另一会话且并发数超过 MaxCall、资源不足，或本规范范围外的其他原因，**可以**在初始检查拒绝。若确实选择拒绝，它须回适当拒绝码及 Warning 文本；只有用户获准限制失败原因（allow-failure-restriction）时，才可选择以不带警告文本的 480 作答，然后跳过本条余下步骤。这个选择属于初始检查，不覆盖手动程序明确拒接时的 110。[§11.1.1.2.1.2 第 1–2 项，印刷页 356](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=357)。

**怎样从主叫的记录追到源头？** 对同一次呼叫，分别关联各段的入向 INVITE、响应和下一段的收发记录，不假定各段使用同一个事务标识：

| 响应实际到达哪一方 | 向主叫方向的转发规则 |
| --- | --- |
| 被叫终端产生响应，T-PF 在终端侧收到 | 自动和手动按需程序均规定：对不含 SDP 的“其他 SIP 响应”，T-PF 沿信令路径向主叫网络转发。若是 T-PF 自己在第 3 项生成的 480，则无需有这次终端侧收件。[§6.3.2.2.5.2，印刷页 97](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=98)；[§6.3.2.2.6.2，印刷页 100](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=101)。 |
| CF 收到 T-PF 方向的响应 | 属于不含 SDP 的其他 SIP 响应时，CF 沿信令路径向主叫网络转发，包含其中实际携带的 MIME 正文。[§11.1.1.4.2，印刷页 383](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=384)。 |
| 主叫侧参与功能（O-PF）收到 CF 方向的响应 | 对同类不含 SDP 的其他响应，O-PF 也须向主叫方向转发，包含其中实际携带的 MIME 正文。这里没有逐项重述 180 或 200 分支中的 Warning 携带要求。[§11.1.1.3.1.1，印刷页 370](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=371)。 |

只看到主叫一侧的 480、未见 Warning 文本、见过 180，或只缺少一份最终响应，都不能区分“被叫拒接”和“被叫未应答”。这些转发条款不要求把所有含 SDP 的失败响应原样透传，也不能用来断言本次 Warning 一定被复制或删除。若 CF 已向主叫发送过早期 INVITE 最终响应 200，也不能据这些转发条款再给同一份主叫 INVITE 发第二个最终响应；它们没有规定这种情况下的后续时序。要认定 110 所指的人工拒接，核对被叫终端实收邀请、用户拒绝和终端对该邀请发出 480/110 的记录；要认定 146，则查 T-PF 的入向邀请、当时收到的被叫设置以及它的本地响应。首接呼叫（first-to-answer）忙时 486、实现所定时间内无人应答时 480，属第 8 项，不是普通私呼的通用超时规则。若实际发生 CANCEL，另查[客户端对 CANCEL 与原 INVITE 的分别应答](private-client-answer-evidence.md)。[§11.1.1.2.1.2 第 8 项与 CANCEL 分支，印刷页 358](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=359)。

## 关联与边界

[普通按需私呼：客户端应答与建立证据](private-client-answer-evidence.md)

- 本页回答服务器准入、身份路由和 O-PF 响应接口问题；客户端模式、取消与成功证据见关联页，不在此重述完整客户端过程。
- 不是完整 SIP/SDP、媒体、安全、配置管理或恢复实现。被调用 TS24.229、TS24.380、TS24.484 与相关 RFC 的全部实现不在此展开；未以其他 Release 补本版条件或引用差异。

若要辨认实际生成失败响应的功能，以及 403 和文本 145 为什么还不能区分 O-PF 与 CF，见 [MCPTT 的 Response-Source 与 Warning](failure-response-source.md)。
