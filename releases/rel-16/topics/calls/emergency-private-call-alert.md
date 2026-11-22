# 在网紧急私呼：通话已获准，随呼告警也发出了吗？

先分开两件事：主叫终端是否获准发起紧急私呼，以及用户若同时要求告警，终端是否获准对同一个人发出告警。前一项成立不替代后一项；收到通话的成功响应，也不一定已得到告警结果。这里讨论 TS 24.379 V16.14.0（Release 16，Stage 3）中带话权控制、普通按需、非 first-to-answer 的在网一对一 MCPTT 紧急私呼。从主叫客户端的实际请求、响应和同一对话内的消息判断，不用组呼、离网私呼或独立告警的处理代替。[§11.1.1 标题及 §11.1.1.1，印刷页 352](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=353)；[§11.1.1.2.1.1，印刷页 353、355–356](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=354)。

## 同一个被叫，为什么可以打紧急私呼却不能告警？

查主叫的用户配置档，两项权限各用自己的开关和接收者规则：

| 用户要求的操作 | 开关必须为 true | 接收者规则 |
| --- | --- | --- |
| 发起紧急私呼 | `allow-emergency-private-call` | `PrivateCall / EmergencyCall / MCPTTPrivateRecipient` |
| 向该用户发紧急告警 | `allow-activate-emergency-alert` | `OnNetwork / PrivateEmergencyAlert` |

两行各按自己的 `entry-info` 判断：`UsePreConfigured` 要求相应 `uri-entry` 含目标用户的 MCPTT ID；`LocallyDetermined` 是另一条允许分支，不要求在对应名单里匹配，但仍要开关为 true。比如，被叫在紧急私呼名单内，却不在按 `UsePreConfigured` 检查的告警名单内，这次可以通过私呼授权，不能通过告警授权。[§6.2.8.3.1.1、§6.2.8.3.1.3 发起部分，印刷页 71–72](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=72)。

主叫处在 `MEPC 1: emergency-pc-capable` 且紧急私呼请求已获准时，客户端设置尚未设置的 MCPTT 紧急状态，在这一 SIP 请求的 `application/vnd.3gpp.mcptt-info+xml` 正文中写 `emergency-ind=true`，使私呼进入 `MEPC 2`。若本次私呼的紧急优先级还不是 `MEPP 2: in-progress`，客户端置为等待确认的 `MEPP 3`。这几步不以同时获准告警为前提。

- 用户**请求了告警且该项获准**：写 `alert-ind=true`，使私呼告警进入等待确认的 `MPEA 2`，并按 §6.2.9.1 纳入该告警所需的位置信息。
- 用户**没有请求告警**：明确写 `alert-ind=false`。
- 用户**请求了告警但该项未获准**：不满足写 true 的条件，也不属于没有请求。§6.2.8.3.2 没给这个分支另定 `alert-ind` 的值，不能把它写成必须 false、必须省略，或因此拒绝已经获准的紧急私呼。

这里只说明这一请求的构造及本地状态，不补配置档文档的完整格式，也不从发出请求推出被叫收到了告警或位置。[§6.2.8.3.2，印刷页 72–73](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=73)；[§11.1.1.2.1.1 第 3 项，印刷页 353](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=354)。

## 收到成功响应却带 149，哪个状态已经变了？

先对上主叫实际收到的是这笔紧急私呼请求的响应。按需初始 INVITE 的客户端程序写明收到 200 (OK) 后，若该私呼处在 `MEPC 2` 或 `MEPC 3`，执行 §6.2.8.3.4；后者是接收相应紧急私呼请求的 SIP 2xx 的状态规则，不适用于其他事务的 2xx。主叫将私呼置为 `MEPC 3: emergency-pc-granted`、紧急优先级置为 `MEPP 2`（若尚未设置）。告警若正等确认（`MPEA 2`），还要查这份响应的 Warning 文本：没有 §4.4 所定义的业务文本号 149，才在这一步把告警置为 `MPEA 3: emergency-alert-initiated`；带 149 则这一步不改变等待确认的告警状态，并不撤销私呼获准。INVITE 响应里的 149 是 Warning 文本中的业务号码，不是 SIP 状态码，也不是 Warning 字段的外层 399。[§11.1.1.2.1.1 接收 200 后第 3 项，印刷页 355–356](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=356)；[§6.2.8.3.4，印刷页 73](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=74)；[§4.4.1–.2，印刷页 33–34](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[表 4.4.2-2 的 149 行，印刷页 37](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=38)。

**后续查主叫实收的同对话 SIP INFO。** Request-URI 中的 MCPTT session ID 要标识进行中的会话；INFO 还须位于该优先私呼请求的对话内，`Info-Package` 为 `g.3gpp.mcptt-info`，并带与包关联的 `application/vnd.3gpp.mcptt-info+xml` 正文。该程序要求正文至少设置 `alert-ind`、`imminentperil-ind` 或 `emergency-ind` 之一。若主叫处理时告警仍在 `MPEA 2`，按实际 `alert-ind` 值分流：true → `MPEA 3`，false → `MPEA 1: no-alert`。若只设置了其他字段，不能当作 `alert-ind=false`；也不能把另一对话的 INFO、发端发送记录或定时猜测代替本次实收。这里的状态是主叫的告警结果，不是被叫实际收到告警或媒体的证明。[§11.1.1.2.1.1 的 INFO 入口，印刷页 356](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=357)；[§6.2.8.3.7 前提及第 1 项，印刷页 75](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=76)。

## 同样收到 480 或 5xx，主叫要清哪些紧急状态？

先对上**主叫发出的那份初始 INVITE**。主叫收到该请求的 4xx、5xx 或 6xx 最终响应时，只有私呼处在 `MEPC 2`（已请求）或 `MEPC 3`（已获准），才按以下规则处理。480 在这里是一个 4xx；不需要靠它的 Warning 文本选择清理动作。[§11.1.1.2.1.1，印 356](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=357)。

| 查哪项证据 | 这次失败要求主叫做什么 |
| --- | --- |
| 这通私呼是 MEPC 2 或 3 | 将私呼置为 `MEPC 1`（可发起紧急私呼）。 |
| **本通**私呼的紧急优先级 | 若是程序所称的 `MEPP 3: confirm-pending`（等待确认），置为 `MEPP 1`（无紧急优先级）。若已是 `MEPP 2: in-progress`，这一步不要求重置。 |
| **原 INVITE** 的 MCPTT 信息正文（`application/vnd.3gpp.mcptt-info+xml`） | 其中 `alert-ind=true` 才把私呼告警置为 `MPEA 1`（无告警）。这项不以旧告警状态为 MPEA 2 为条件。原请求写 false 或没有该元素，这一步没有要求清告警。 |

例如，两次都收到 480，只要进入上述分支，私呼都回到 MEPC 1。一次原请求明确要求告警，另一次没有，只有前者须按这次失败清告警。回包正文、用户曾按过告警键、告警恰在等待确认，都不能代替原请求里的值。此处也没有清除**用户自身的 MCPTT 紧急状态**的动作；不能用 MEPC 1 判定用户已脱离紧急状态。[§6.2.8.3.5 第 1–3 项，印 73–74](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=74)；[资料性附录表 G.11-1 对 MEPC 1 的说明，印 592](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=593)。

**只记了 MEPP 数字的日志要谨慎。** 这版的程序 §6.2.8.3.5 把等待确认写成 `MEPP 3: confirm-pending`；资料性表 G.10-1 则把 3 写为 `cancel-pending`、4 写为 `confirm-pending`。上表按程序保留编号和名称。单看日志里的 3，不能断定实现记录的就是待确认，也不能据附表把本步骤改成检查 4。[§6.2.8.3.5 第 2 项，印 74](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=75)；[表 G.10-1，印 591](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=592)。

若事件是**预建立会话的媒体面报告释放**，应改查[释放发生时的本地状态](preestablished-emergency-private-confirmation.md)。该程序在 MEPC 2 下按当时的 MPEA 2 清告警；这里按失败 INVITE 中的 `alert-ind=true` 清告警，两个条件不能互换。

若问题发生在[普通按需私呼](private-client-answer-evidence.md)或[在网紧急预安排组呼](emergency-group-client.md)，要按该通呼叫的角色和状态取证。本页不规定告警的实际投递、媒体结果、重试或取消程序。

若主叫通过预建立会话发起紧急私呼，查[REFER 2xx、同会话 re-INVITE 与释放前的紧急状态](preestablished-emergency-private-confirmation.md)，不套此处的按需 INVITE 应答规则。

若同一通在网紧急私呼已经接通，现收到 `emergency-ind=false` 的 re-INVITE 或遇到取消后的 200/149，查[私呼降级及撤警结果](emergency-private-downgrade.md)，不要套这里发警的 MPEA 2 条件。
