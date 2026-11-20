# 按需首接呼叫：主叫选了两人，为什么控制功能只收到一人？

查发起侧参与功能（O-PF）收到的 INVITE，再查它另发给控制功能（CF）的 INVITE。主叫选乙、丙，O-PF 用的主叫配置档只列乙；若请求走到构造下一笔 INVITE，发给 CF 的资源列表须只保留乙。这一步在 CF 邀请被叫之前，不用等乙或丙回复。本文限同一 MCPTT 系统、普通在网、按需建立、带话权的首接呼叫（`first-to-answer`），目标是明确给出的 MCPTT 用户，不含功能别名、预建立 REFER 或紧急呼叫。[TS 24.379 V16.14.0 §11.1.1.1，印刷页 352](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=353)；[§11.1.1.3.1.1 第 12、15–17 项，印刷页 368](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=369)

## 主叫侧返回 403：先看 Warning

进入名单检查前，O-PF 从入站 `P-Asserted-Identity` 的公共用户身份确定主叫 MCPTT ID，再找与该主叫关联的首接服务 CF 公共业务身份（PSI）。这两个身份都不是请求名单里的被叫。查对应同一份入站 INVITE 的**本地拒绝**，不要把别处看到的 403 套进下表。[§11.1.1.3.1.1 第 3–7 项，印刷页 366–367](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=367)

| O-PF 当时用于检查的主叫配置档 | 对这笔入站 INVITE 的结果 |
| --- | --- |
| `allow-private-call` 不存在或为 `false` | **403 / Warning 107**。这是先查的通用私呼许可，也适用于这条首接过程。 |
| `PrivateCall` 有至少一项，资源列表每个 `entry` 的 `uri` 都不匹配，且配置未允许呼叫名单外用户 | **403 / Warning 153**。拒绝的是这次首接请求。只要有一项匹配，就不满足“全部不匹配”。 |
| 走到首接专用许可检查，`allow-request-first-to-answer-call` 不存在或为 `false` | **403 / Warning 156**。即使名单里有人匹配，也不能代替首接许可。 |

403 是 SIP 状态；107、145、153、156 是 Warning 引号内开头的业务文本码，外层 Warning 码是 399。[§4.4.1–2，印刷页 33–34](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)

三种分支各自停止该次入站处理，不会由该分支给 CF 生成下一笔邀请。这比“没抓到下一腿”更有判定力。缺少资源列表 MIME 正文另走较早的 **403 / Warning 145**，不要当作提供了名单但无人匹配。[§11.1.1.3.1.1 第 8、10 项，印刷页 367](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=368)；[第 12–14 项，印刷页 368](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=369)

## 已有下一腿：用实际清单判断谁进入后续邀请

通用 INVITE 构造程序复制资源列表。首接专用第 15a 项收窄这条规则：只要主叫的 `PrivateCall` 存在且非空，O-PF 给 CF 生成的 `application/resource-lists` 正文只包含入站中 `uri` 匹配的项，并在 MCPTT 信息 MIME 正文把 `session-type` 设为 `first-to-answer`。主叫客户端应向至少两名用户发起，不能把这个起始要求当成过滤后也须保留两项。第 12 项的名单外许可只在拒绝条件里出现；第 15a 项未为它加入例外。如果允许名单外呼叫、却无人匹配，不能据此自动把原名单加回，也不能擅定空结果的最终响应或补选行为。[§11.1.1.1，印刷页 352](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=353)；[§6.3.2.1.3 第 7–8 项，印刷页 85](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=86)；[§11.1.1.3.1.1 第 12、15a 项，印刷页 368](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=369)

核对 O-PF 生成并发出的那份 INVITE：`Request-URI` 是为主叫选的首接服务 CF 的 PSI，`mcptt-calling-user-id` 是主叫的 MCPTT ID；**候选被叫要看正文资源列表**。要确认 CF 看见了哪些项，再查 CF 实际收到的 INVITE。通过该侧前置检查后，这个直接目标分支按实收资源列表邀请，逐被叫的 INVITE 用对应的 MCPTT ID 填 `mcptt-request-uri`。O-PF 发出不等于 CF 收到；CF 收到含乙的清单不等于乙端收到、振铃、接听或媒体已通。没有丙的 200 也不能反推名单曾被过滤。[§11.1.1.3.1.1 第 16–17 项，印刷页 368](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=369)；[第 22 项，印刷页 369](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=370)；[§11.1.1.4.2 第 12 项，印刷页 381](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=382)；[§11.1.1.4.1 第 3–4 项，印刷页 379](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=380)

若查[主叫终端怎样生成候选列表](first-to-answer-on-demand-client.md)，从终端步骤看起；若 CF 已发出邀请，按[谁获选、如何结束其他分支](first-to-answer-controlling.md)逐腿查。普通[一对一私呼的出向和入向名单](private-server-admission-routing.md)另有条件和警告码，不用来解释这两条首接拒绝。若只看到用户[改了预选配置档](../identity/user-profile-switch.md)，先确认 O-PF 这次使用的配置档，不能把改预选当成当前已切换。
