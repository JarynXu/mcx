# 首接呼叫：主叫选了两人，为什么控制功能只收到一人？

先看主叫发的是哪种请求。**按需建立**时，主叫发 INVITE；**复用预建立会话**时，主叫发对话外 REFER。两条路都由发起侧参与功能（O-PF）另发业务 INVITE 给控制功能（CF）。如果 O-PF 的出站清单比入站少，先核对这个节点使用的主叫配置档；不要用某个被叫有没有接听来猜名单。本页限同一 MCPTT 系统、普通在网、带话权、直接指定用户的呼叫，不含功能别名或紧急呼叫。[TS 24.379 V16.14.0（Release 16，Stage 3），§11.1.1.1，印 352](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=353)

## 预建立会话：REFER 内写了谁？

甲要打给乙、丙，谁先接就和谁通话。甲发出的 REFER 以预建立会话的公共业务身份（PSI）为 Request-URI，Target-Dialog 指向原对话；**被叫不在这两个字段里**。沿 Refer-To 的 `cid:` 找到对应的资源列表正文：每个目标各占一项，URI 是其 MCPTT ID，URI 的 `body` 参数内的 MCPTT 信息标为 `first-to-answer`。客户端发起首接时至少选两名用户。[§11.1.1.2.2.1 起首、项 1、7、9、12，印 362–364](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=363)

O-PF 用实收 REFER 的 P-Asserted-Identity 里的公共身份查主叫的 MCPTT ID。到达名单检查时，区分名单的内容：

| O-PF 实际收到什么 | 本地怎样处理 |
| --- | --- |
| 没有 Refer-To 中 cid 所引用的资源列表正文 | 对这份 REFER 回 403，Warning 文本码 145，停止。 |
| 引用的名单只有一项，且该项标为 `first-to-answer` | 单项只有标为 `private` 才识别为普通一对一。单项标首接，O-PF 对 **REFER** 回 403/145 并停止；没有生成给 CF 的业务 INVITE。 |
| 引用的名单有多项，各项的类型都不是 `first-to-answer` | 也对 REFER 回 403/145 并停止；不能只数人头。 |
| 引用的名单有多项，且每项都标为 `first-to-answer` | 识别为首接，再找与**主叫**关联的首接服务 CF 的 PSI。找不到该 CF 时，对 REFER 回 404，Warning 文本码 142，停止。 |

这几项在[§11.1.1.3.1.2 起首及项 2–8，印 370–371](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=371)。Warning 文本码不是 SIP 状态码。仅凭一条 403，无法从这些原因中选定一个。两个名字不等于两个合格条目；这里不替本版条文裁决多项类型混杂的处理。

## REFER 给了两人，为何下一份 INVITE 只有一人？

在前置检查允许继续的情况下，O-PF **先向甲发这笔 REFER 的 200，再生成发给 CF 的 INVITE**。如果甲的配置档里 `PrivateCall` 存在且有条目，O-PF 在新 INVITE 的资源列表中只保留 URI 匹配的候选，并在 MCPTT 信息正文中标明 `first-to-answer`。例如甲的 REFER 列乙和丙，名单只匹配乙，出站 INVITE 就只列乙；它仍是首接，不因过滤后只剩一人改作普通私呼。新请求的 Request-URI 是**首接服务 CF 的 PSI**，不是乙的地址。[§11.1.1.3.1.2 项 14–17、20，印 373–374](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=374)

不要把“允许呼叫名单外的人”读成“发送时保留名单外的人”。第 11 项的拒绝条件是 `PrivateCall` 非空、**每一项都不匹配**，且未配置名单外许可；第 12 项另查首接许可 `allow-request-first-to-answer-call` 是否缺失或为 false。两项各列 403、Warning 文本码 153 或 156，并要求停止。**这段在处理 REFER，项 11 和 12 的拒绝对象却写作 INVITE**；项 9 在通用私呼许可缺失或为 false 时列出 403/107，既写拒绝 REFER，也写响应 INVITE，没有像第 11、12 项那样明写停止。不要据此把这几个码指定给实际的某笔线上请求；须对上请求和响应。第 16(a) 项过滤并没有名单外许可例外；准许名单外且零匹配也不能自行补回候选或推定最终响应。[§11.1.1.3.1.2 项 9、11、12、16(a)，印 371–373](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=372)

排查乙、丙在哪一步变成乙，比较 O-PF 实收 REFER 的列表、当时用的主叫配置档和另发 INVITE 的列表。要说 **CF 收到了乙**，还得看到 CF 收到的 INVITE；要说**乙已接听**，还要查乙这一腿的应答；要说乙胜出，再查 CF 选中了谁。即使甲已收到 REFER 的 200，也不能仅凭它证明另发的 INVITE 已离开 O-PF。

## 按需建立：哪项配置使入站 INVITE 被拒绝？

进入名单检查前，O-PF 从入站 `P-Asserted-Identity` 的公共用户身份确定主叫 MCPTT ID，再找与该主叫关联的首接服务 CF 公共业务身份（PSI）。这两个身份都不是请求名单里的被叫。查对应同一份入站 INVITE 的**本地拒绝**，不要把别处看到的 403 套进下表。[§11.1.1.3.1.1 第 3–7 项，印刷页 366–367](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=367)

| O-PF 当时用于检查的主叫配置档 | 对这笔入站 INVITE 的结果 |
| --- | --- |
| `allow-private-call` 不存在或为 `false` | **403 / Warning 107**。这是先查的通用私呼许可，也适用于这条首接过程。 |
| `PrivateCall` 有至少一项，资源列表每个 `entry` 的 `uri` 都不匹配，且配置未允许呼叫名单外用户 | **403 / Warning 153**。拒绝的是这次首接请求。只要有一项匹配，就不满足“全部不匹配”。 |
| 走到首接专用许可检查，`allow-request-first-to-answer-call` 不存在或为 `false` | **403 / Warning 156**。即使名单里有人匹配，也不能代替首接许可。 |

403 是 SIP 状态；107、145、153、156 是 Warning 引号内开头的业务文本码，外层 Warning 码是 399。[§4.4.1–2，印刷页 33–34](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)

三种分支各自停止该次入站处理，不会由该分支给 CF 生成下一笔邀请。这比“没抓到下一腿”更有判定力。缺少资源列表 MIME 正文另走较早的 **403 / Warning 145**，不要当作提供了名单但无人匹配。[§11.1.1.3.1.1 第 8、10 项，印刷页 367](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=368)；[第 12–14 项，印刷页 368](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=369)

## 按需 INVITE 的下一腿：谁进入后续邀请？

通用 INVITE 构造程序复制资源列表。首接专用第 15a 项收窄这条规则：只要主叫的 `PrivateCall` 存在且非空，O-PF 给 CF 生成的 `application/resource-lists` 正文只包含入站中 `uri` 匹配的项，并在 MCPTT 信息 MIME 正文把 `session-type` 设为 `first-to-answer`。主叫客户端应向至少两名用户发起，不能把这个起始要求当成过滤后也须保留两项。第 12 项的名单外许可只在拒绝条件里出现；第 15a 项未为它加入例外。如果允许名单外呼叫、却无人匹配，不能据此自动把原名单加回，也不能擅定空结果的最终响应或补选行为。[§11.1.1.1，印刷页 352](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=353)；[§6.3.2.1.3 第 7–8 项，印刷页 85](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=86)；[§11.1.1.3.1.1 第 12、15a 项，印刷页 368](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=369)

核对 O-PF 生成并发出的那份 INVITE：`Request-URI` 是为主叫选的首接服务 CF 的 PSI，`mcptt-calling-user-id` 是主叫的 MCPTT ID；**候选被叫要看正文资源列表**。要确认 CF 看见了哪些项，再查 CF 实际收到的 INVITE。通过该侧前置检查后，这个直接目标分支按实收资源列表邀请，逐被叫的 INVITE 用对应的 MCPTT ID 填 `mcptt-request-uri`。O-PF 发出不等于 CF 收到；CF 收到含乙的清单不等于乙端收到、振铃、接听或媒体已通。没有丙的 200 也不能反推名单曾被过滤。[§11.1.1.3.1.1 第 16–17 项，印刷页 368](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=369)；[第 22 项，印刷页 369](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=370)；[§11.1.1.4.2 第 12 项，印刷页 381](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=382)；[§11.1.1.4.1 第 3–4 项，印刷页 379](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=380)

若是**按需**首接，可查[主叫终端怎样生成候选列表](first-to-answer-on-demand-client.md)，或在 CF 发出邀请后查[怎样选中一人、结束其他分支](first-to-answer-controlling.md)。这两页不说明预建立会话上后续的接听或获选程序。普通[一对一私呼的出向和入向名单](private-server-admission-routing.md)另有条件和警告码，不用来解释这两条首接拒绝。若只看到用户[改了预选配置档](../identity/user-profile-switch.md)，先确认 O-PF 这次使用的配置档，不能把改预选当成当前已切换。
