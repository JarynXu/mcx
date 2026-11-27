# MCPTT 按名单发起互通 ad hoc 组呼：逐个回什么，确认超时算谁？

**名单上每个 LMR 用户都有一笔 IWF 请求和应答。建立确认时限看的是 MCPTT 用户的确认，不是这些 IWF 应答。** 本页限 TS 23.283 V19.5.0、Rel‑19 Stage 2 §10.17.3.5：MCPTT client 1 实际按已知的 MCPTT ID 名单发起，名单含 MCPTT 和 LMR 用户。只知道这些 ID、实际却给条件选人，查[MCPTT 按条件发起](adhoc-group-criteria-mcptt-origin.md)；如果是[IWF 代 LMR 按条件发首请求](adhoc-group-criteria-lmr-origin.md)，查 §10.17.3.2。客户端 1 和 2 要已注册，对应用户已认证且获准使用 MCPTT；图在 server 端另标本次授权（Step 2）。注册和已有服务权限不证明这次授权通过。[§10.17.3.5 前提，印刷页 189（PDF 第 190 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=190)。

## 一人一笔 IWF 请求，不按 IWF 个数计

图中 client 1 向 MCPTT server 发起（Step 1）；server 向 MCPTT client 2 发邀请（3a），client 2 本地提示（3b）、回 server（3c）。LMR 另走 4a/4b：**每个被邀 LMR 用户**，server 发一笔 IWF ad hoc group call request，IWF 回同笔应答。图只画一组 4a/4b 和一个 IWF，不能据图减成每个网关一笔，也不限定网关个数。经过 IWF 的两系统间信令由 IWF 转换身份和协议；NOTE 2 允许 IWF 面向 LMR 用户按普通组呼处理。[图 10.17.3.5-1、Steps 1–5、NOTE 2，印刷页 190（PDF 第 191 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=191)。

只看到一个 LMR 目标的 4b，不替另一个目标补结果；只看到 IWF 发出 4b，不证明 server 实收。server 实收与目标匹配的 4b，可确定该次 IWF 请求的 Result，不证明对应 LMR 终端实际回应、加入或收到语音。找不到实收证据也不等于失败。

| IWF-1 消息 | 区分字段与目标 |
| --- | --- |
| **4a：server → IWF 请求** | 主叫 MCPTT ID、临时组 ID、SDP offer 必选。被邀者 MCPTT ID 在另一可选行，预配置组 ID 也是可选，指配置而非本次组。 |
| **4b：IWF → server 应答** | 主叫 MCPTT ID、临时组 ID、Result（success 或 failure）必选。没有被邀者 ID 一行。SDP answer 栏标 O，说明成功时出现；不拿 SDP answer 补 Result，也不从 success 补未见的 SDP answer。 |

[表 10.17.2.2-1 / 10.17.2.3-1，印刷页 182–183（PDF 第 183–184 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=183)。单独看到 4a 或 4b，可按其消息类型查表。若要把 4b 结果归给某个 LMR 用户，要对上这次呼叫的那一笔 4a；同一主叫和临时组可发多笔，两个必选 ID 不能单独决定是哪个目标。§10.17.2.3 表前写 request，标题与表名写 response，按图的 4b 确认方向。不由表猜线级关联键、组 ID 分配者或 ID 寿命。

## Step 6 看是否按时收到必需的 MCPTT 确认

1. 发起用户要求被邀 MCPTT 用户确认；按该次用户 profile 的 ad hoc 组呼策略和配置时限检查，**时限内没确认齐必需的 MCPTT 用户**，才适用原文这条：server 可继续或放弃，随后通知发起用户确认没有覆盖全部必需成员。不能把它读作一缺人就必放弃，或每次都必须发 Step 6。
2. 同一步另写，server **可列出所有在配置时限内未确认该组呼请求的 MCPTT 用户**；名单不只限必需者。通话中有 MCPTT 用户加入或离开时，可多次向发起用户发这种名单通知。它和“必需成员未齐”不是同一种信息；图只画一条 6，不规定两个独立报文，也没给第二种通知脱离本段语境的触发条件。

原文前一句说确认建呼，后一句说未确认组呼请求。不以 SIP ACK、图里的任一 3c、IWF 4b、客户端提示或媒体替代该次按规则生效的 MCPTT 确认。只有非必需 MCPTT 用户未确认、只有 LMR 未回或日志没覆盖时限，都不足以触发第一条。NOTE 3 限定的是通知内容：server 向发起 MCPTT 用户发这种通知时，不能报告某个 LMR 用户未确认。它不排除 IWF 的 4b，也不说明 LMR 用户不能以其他方式回应。按发送和接收端记录分别确定 server 发了哪种信息、发起者是否实际收到。[Step 6、NOTE 3，印刷页 190（PDF 第 191 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=191)。

## 图示次序不要当作等待规则

图里 4b 在 3c 之前，之后画 server 向原 client 1 发 Step 5 建呼应答，再以实线画 Step 6。但本节未规定 4b 和 3c 谁必须先到，也没据图规定 Step 5 要等齐所有应答；Step 6 仍按正文条件。只见发出 5 或 6，不代表原 client 1 实收。Step 7 正文列 client 1、client 2 和 LMR 用户建立媒体面与话权资源，图的横条跨 IWF，不证明任何终端实况。若选择放弃，不能顺着图推 Step 7 必继续；收到主叫应答、成员实际加入、语音已听见与实际授话权，都要各自取证。

§10.17.3.5 总述、Steps 1–3 与 5 引用 TS 23.379 [7] §10.19.3.1.1；§2 对非指定 3GPP 引用按同 Release 最新版本查。本页只核回指，不补 Step 5 汇总、确认起计点和默认时间、原生 SIP 或 IWF 到 LMR 本地实现。不要套 §10.17.3.1 NOTE 3 或该支 Step 11 的已确认且已加入名单；本页也不替代[原生显式名单 Stage 3 入口](../groups/adhoc-explicit-list-establishment.md)。[§10.17.3.5 图与步骤，印刷页 190（PDF 第 191 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=191)；[§2 [7]，印刷页 11（PDF 第 12 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=12)。
