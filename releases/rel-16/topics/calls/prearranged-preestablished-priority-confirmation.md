# MCPTT 预建立组呼：REFER 已回 200，紧急或迫近危险状态如何确认？

**REFER 的 200 不能确认紧急或迫近危险优先级。** 主叫终端要看起始参与功能（O-PF）后来发到**同一预建立会话**的 re-INVITE，结合原 REFER 请求的业务、本机当前状态和实际收到的指示判断。这里限 TS 24.379 V16.14.0（Release 16，Stage 3）在网预安排组呼，主叫用已有的预建立会话发起。不是给被叫的组呼邀请，也不是把已进行的按需业务通话升级。

## 先把 200 配回它回答的请求

终端先发对话外 REFER。Request-URI 和 `Target-Dialog` 指向现有预建立会话；`Refer-To` 的 `cid` 指向资源列表，列表里的 URI 标识本次要呼叫的预安排组，内层信息体的 `session-type` 为 `prearranged`。引用旧对话没有让 REFER 变成对话内请求。[§10.1.1.2.2.1，印 228 / PDF 229](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=229)；[§10.1.2.2.2.1 第 1–3 项，印 273 / PDF 274](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=274)、[第 10 项和回包入口，印 275 / PDF 276](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=276)。

O-PF 的前置检查走到成功分支后，须先生成并发送给终端的 REFER 200，再另建业务 INVITE 发给组控制功能（CF）。终端实收对这条 REFER 的最终 2xx 后须与媒体面交互；该分支不确认请求的优先状态。若 O-PF 实收 CF 对业务 INVITE 的临时响应，本节要求丢弃，不转给终端。终端没看到临时响应，不能据此断定控制侧没发。[§10.1.1.3.1.2 入口，印 233 / PDF 234](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=234)、[第 13 项，印 234 / PDF 235](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=235)、[第 14–19 项和临时响应，印 235 / PDF 236](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=236)；[§10.1.2.2.2.1，印 275 / PDF 276](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=276)。

## 控制侧的 200：什么时候发 re-INVITE，什么时候等 INFO？

`149` 是 SIP `Warning` 文本开头的 MCPTT 码，不是 SIP 状态码，也不是 `Warning` 头自己的警告码。先在 O-PF 侧找对**本次业务 INVITE** 的匹配响应。[§4.4.1–2，印 33 / PDF 34](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)、[表 4.4.2-1，印 34 / PDF 35](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=35)；[表 4.4.2-2，印 37 / PDF 38](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=38)。

- **匹配业务 200 没有 149，且原业务 INVITE 的 `Resource-Priority` 按 §6.3.2.1.8.4 填的是紧急或迫近危险组呼优先级：** O-PF 须在终端旧预建立对话中发送 re-INVITE。SDP offer 基于旧会话已协商的 SDP；`Resource-Priority` 用原业务 INVITE 的值。这一路不等 INFO，也不要求补造三个业务指示。响应可以有别的 Warning；没有 149 本身还不够，须核原请求的优先级头。
- **O-PF 实收 CF 对本次紧急或迫近危险业务 INVITE 的 200，且 Warning 文本含 149：** O-PF 须等 CF 的 INFO。149 不交代请求的最终状态；业务 INVITE 的失败响应即使带 149，也不进入这条等待分支。

**实收 INFO 是另一入口。** O-PF 实收 CF 在本次紧急或迫近危险组呼的业务 INVITE 对话内发来的 INFO，须先向 CF 发送本笔 INFO 的 200，再生成并发出终端旧对话内的 re-INVITE。逐项复制 INFO 中实际存在的 `emergency-ind`、`alert-ind`、`imminentperil-ind` 值，缺项不补成 `false`。SDP offer 仍基于旧会话已协商的 SDP，`Resource-Priority` 仍取先前业务 INVITE 的值。若记录只覆盖这次匹配实收，缺前一条 149 不妨碍判定本步，也不能反推 149 一定出现过。本条不规定 CF 可以脱离对应业务程序发送 INFO；另一业务对话的 INFO 不适用，终端回 re-INVITE 的 200 也不是 O-PF 给 CF 的 INFO 应答。

[§6.3.2.1.8.4–.5，印 90–91 / PDF 91–92](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=91)；[INFO 构造第 1–4 项，印 91 / PDF 92](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=92)；[§10.1.1.3.1.2 的业务响应与 INFO 入口，印 236 / PDF 237](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=237)。本版组呼专条的响应入口写 **200 (OK)**，下级分支和通用构造条款写 **2xx**，不据此把专条套给所有非 200 的 2xx。印 91 第 3 项有一段 `Resource-Priority` 文字重复，句末指明先前发给 CF 的 INVITE，不能改从 INFO 取值。

## 主叫实收 re-INVITE 后，再看本机状态

这里的状态处理还要满足两个入口条件：主叫之前发送的 REFER **请求发起紧急或迫近危险组呼**；主叫在该 REFER 所指的预建立会话内**实际收到** re-INVITE。普通 REFER 进入已处于紧急或迫近危险状态的组，也可能触发 O-PF 的无 149 分支，但不能用那条 re-INVITE 直接判该终端自己的优先呼叫请求已经获准。[§6.3.2.1.8.5 注 1，印 90 / PDF 91](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=91)；[§6.2.8.1.16，印 70 / PDF 71](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=71)。

| 本机前态 | 实收指示 | 本机动作 |
| --- | --- | --- |
| `MEGC 2`，紧急组呼请求待确认 | `emergency-ind` 缺失或为 `true`，且**没有** `imminentperil-ind` 元素 | 须将该组的 `MEG` 置 2（若还不是 2），将 `MEGC` 置 3。`imminentperil-ind=false` 仍是元素存在，不满足这项条件。 |
| `MEGC 2`，且告警也在 `MEA 2` 待确认 | `alert-ind` 缺失或为 `true` / 为 `false` | 缺失或 `true` 须置 `MEA 3`；`false` 须置 `MEA 1`。这是单独的告警判断，不以表中上一行已经命中为前提。 |
| `MIGC 2`，迫近危险组呼请求待确认 | `imminentperil-ind` 缺失或为 `true` | 须置 `MIGC 3` 和 `MIG 2`。 |
| `MIGC 2`，迫近危险组呼请求待确认 | `imminentperil-ind=false`，且 `emergency-ind=true` | 须将该组的 `MEG` 置 2。本项没有置 `MIGC 3` 或回退 `MIGC 1` 的动作。注释解释的是请求的迫近危险优先级未获准，按组已有的紧急优先级参加。 |

符合客户端入口时，终端还须检查 `Resource-Priority` 是否存在，须接受这条 re-INVITE 并回自己的 200；SDP answer 基于该预建立会话已协商的参数。缺优先级头不是该步骤列出的拒绝条件。终端这笔 200 不代替上面的状态判断，也不证明已获话权、媒体已通或其他人收到告警。[§6.2.8.1.16 第 1–2 项及注，印 70 / PDF 71](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=71)；[§10.1.2.2.2.1 收到 re-INVITE 后第 1–5 项，印 275 / PDF 276](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=276)。

若只想重入一场仍存在的普通组呼，查[普通预建立重入](preestablished-group-rejoin.md)。若 CF 已在按需业务对话内收到优先级升级、取消的 re-INVITE，查[已有按需组呼的控制侧处理](emergency-group-server.md)。若是同系统、在网、普通预安排组呼，终接参与功能（T-PF）实收 CF 为本场发来的终接 INVITE，要判断能否复用被叫的预建立会话及自动或人工分支，读[终接侧参与功能](prearranged-preestablished-termination.md)。CF 发出不等于 T-PF 收到，也不等于被叫直接收到 CF 的 INVITE。若原 REFER 请求的是带话权控制的紧急私呼，读[预建立紧急私呼的确认](preestablished-emergency-private-confirmation.md)，不要套用组呼状态。
