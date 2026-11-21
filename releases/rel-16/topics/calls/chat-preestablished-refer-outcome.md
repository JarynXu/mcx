# 用预建立会话加入聊天组：REFER 的 200 算入会成功吗？

不算。甲已有一条空闲的预建立会话 P，想发起或加入普通 MCPTT 聊天组 G。终端发给发起侧参与功能（O-PF）的 **REFER** 和 O-PF 随后发给控制功能（CF）的 **INVITE** 是两笔请求。REFER 的 200 是前一笔的答复；若后一笔 INVITE 已发，应对上 CF 的应答来判本次触发的隐式归属；O-PF 在本地决定拒绝原请求时另有取消入口。这段主叫流程限同一系统内、在网、直接组身份的普通聊天组，不套入紧急、迫近危险或临时组程序。[TS 24.379 V16.14.0，Rel-16 Stage 3，§10.1.2.2.2.1，印 273–275](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=274)；[§10.1.2.3.2.1，印 282–285](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=283)。

## REFER 明明在对话外，为什么还带 Target-Dialog？

因为发出一条新请求与指明要用哪条旧会话，是两件事。

- **SIP 请求行**的 `Request-URI` 写预建立会话 P 的会话身份，不填聊天组 G。`Target-Dialog` 也标识要用的预建立会话，但不把这条 REFER 变成原对话内的请求。
- **`Refer-To`** 放 `cid`，对上 `application/resource-lists` 正文的 `Content-ID`；列表只有一项，`entry@uri` 标识聊天组 G。该 URI 的头部参数内，`body` 所载的 MCPTT 信息正文带 `session-type=chat` 和发起终端的 `mcptt-client-id`。预建立参数需要修改，或根据 §6.4 需要隐式话权时，才适用本处的嵌入 SDP offer 条件。
- 终端还带 `Refer-Sub: false` 和 `Supported: norefersub`。O-PF 按相应组合处理，不建立隐式 REFER 订阅；这不是在禁止聊天组其他独立的订阅。

同一版在聊天组小节写 `application/vnd.3gpp.mcptt-info`，通用的 REFER 转 INVITE 规则写 `application/vnd.3gpp.mcptt-info+xml`。这里保留两处字面，不把它们当成已规定可互换的两种 MIME。聊天组条款从 `entry@uri` 取组身份，通用隐式归属程序写从收到的 SIP 业务正文的 `mcptt-request-uri` 取组 ID。本版这些文字未说明 O-PF 怎样把嵌套输入交给通用程序，不因此要求终端在嵌入正文再填一份组 ID。[§10.1.2.2.2.1 第 3(c)(ii) 项，印 274](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=275)；[§6.3.2.1.4 第 11 项，印 86](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=87)；[§9.2.2.2.12 第 1–2 项，印 184](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=185)。

这些位置分别解决使用哪条会话、呼叫哪个组和按哪类程序处理的问题。此处不是终端直接对聊天组发起一条按需 INVITE。[§10.1.2.2.2.1 第 1–3、9–10 项，印 273–275](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=274)；[§10.1.2.3.2.1 第 12 项及注 8，印 283–284](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=284)。

## O-PF 构造了 REFER 200，不等于已经发出

O-PF 经过前序检查后先构造 REFER 的 200，**发送之前仍要用 G 查 CF 的公共服务身份（PSI）**。若无法识别 CF，O-PF 须拒绝原 REFER，回 404 和 Warning 文本 `142 unable to determine the controlling function`，不走后面的成功发送步骤。不要把构造日志写成已发出；该条也不规定 CF 的发现算法。[§10.1.2.3.2.1 第 11–14 项及注 6–7，印 283](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=284)。

另看本地拒绝：如果这个 REFER 已触发隐式归属，通用 §9.2.2.2.14 也把 O-PF 决定拒绝这笔原请求列为取消入口，不必等 CF 应答。它移除的是该请求实际新增的条目。聊天组第 13 项本身没有重复写这条调用；仅见 404/142 不能证明先前添加了条目或实际做了取消。[§9.2.2.2.14，印 185](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=186)。

成功路径上，O-PF 先把这份 REFER 200 发给终端，随后构造并向 CF 发送**另一条 INVITE**：请求行的 `Request-URI` 写 CF 的 PSI，正文的 `mcptt-request-uri` 写 G。终端实际收到 REFER 的最终 2xx 后与媒体面交互，但这不能替 CF 的 INVITE 应答、入会、授权发言或实际媒体结果作证。[§10.1.2.3.2.1 第 14–19 项，印 283–284](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=285)；[§10.1.2.2.2.1 的 REFER 2xx 分支，印 275](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=276)。

## 同一笔 CF INVITE 后来成功或失败，归属记在哪？

| O-PF 实际收到的对应 INVITE 响应 | 若本次已调用隐式归属程序 |
| --- | --- |
| CF 回 2xx | O-PF 完成这次隐式归属。已为本次添加的待定组记录设为 `affiliated`，并执行相应通知程序。 |
| CF 回 4xx、5xx 或 6xx | O-PF 调用取消程序，移除该用户、该客户端下本次新增的目标组记录。不是把同一用户所有终端的归属清掉。 |

O-PF 收到上表对应的 CF 应答后，即使本次未做隐式归属，也须按相应分支与媒体面交互。这两支不要求再用一个成功或失败码去改写已经发出的 REFER 200。若用户原本已归属且本次没有调用该程序，不能套这张表另造一项完成或取消。CF 的 302 在本条另有流程，不能当成上表的失败入口。要验证终端确实进入媒体通话，还须对上预建立会话及实际控制报文、应答或终端状态。[§10.1.2.3.2.1 的 CF 2xx、302 与 4xx–6xx 分支，印 284–285](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=285)；[§§9.2.2.2.13–14，印 185](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=186)。

若客户端**不用预建立**，以初始 INVITE 发起或加入直接聊天组，查[按需聊天组的建立与加入](chat-establish-join.md)。若要核对 O-PF 对同一用户各端的候选组记录和 N2 上限，读[隐式归属的 N2 计算](../groups/implicit-affiliation-n2.md)。若已在核对媒体面的 Connect、Accepted 与所用预建立会话，读[预建立会话的 Connect 结果](../media/preestablished-connect-outcome.md)，不要拿这里的 SIP 200 替代。

## 终接 T-PF 已收到邀请：语音段匹配，话权段不同，能复用旧会话吗？

不能。看的是**发给终接参与功能（T-PF）的聊天组初始 INVITE**。T-PF 若未在前置资源检查中拒绝，先查来向 `Contact` 的 `isfocus`。缺这个标记就回 SIP **403，Warning 文本码 104**，不走 SDP 复用检查。标记存在才继续。要复用，受邀客户端的预建立会话不能已关联 MCPTT 会话；来向 SDP 的**语音媒体段**和**话权控制媒体段**还要分别与现有会话的对应段相同。两项媒体检查都通过，T-PF 才可以按本地策略复用，不是必须复用。语音段相同、话权段不同，不是 403/104；未选复用的请求继续走新建终端腿。[TS 24.379 V16.14.0，§10.1.2.3.1.3 第 1、2、4 项，印刷页 280–281](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=281)。

**新建终端腿。** T-PF 向受邀用户的关联公共用户身份发初始 INVITE，依据来向业务正文的 `mcptt-request-uri` 定位这名用户。复制来向的 `P-Asserted-Identity`；来向带 `Resource-Priority` 才复制该字段。匹配到客户端对这笔 INVITE 的 200 后，T-PF 用该应答构造上游 SDP answer，按这条分支先与媒体面交互，再把 200 转发给上游。[§10.1.2.3.1.3 第 5–11 项及终端 200 分支，印刷页 281](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=282)。

**复用终端腿。** T-PF 在已有的预建立 SIP 对话内向客户端发 **re-INVITE**。offer 依据来向 offer；有来向 `Resource-Priority` 才复制。收到终端对这笔 re-INVITE 的 200 后，T-PF 按预建立会话的 SDP answer 规则构造、发送上游 200。这里没有另列新建终端腿的回复前媒体交互步骤，不能从这段省略推导禁止媒体交互。核对现有对话和此笔 re-INVITE 的对应应答；主叫 REFER 的 200、别处的 200 或媒体 Connect 都不能代替它。[§10.1.2.3.2.2，印刷页 285–286](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=286)；[§6.3.2.2.2.2，印刷页 94](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=95)。

这三段从 T-PF **确已收到**邀请起算。终端侧 §10.1.2.2.1.6 所述初始邀请用于已归属但未加入聊天组的紧急或迫近危险呼叫。不能由 T-PF 的收包处理反推普通聊天组也会向未加入者主动发邀，不能由 SIP 200 反推终端已收到媒体。[§10.1.2.2.1.6，印刷页 272](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=273)。
