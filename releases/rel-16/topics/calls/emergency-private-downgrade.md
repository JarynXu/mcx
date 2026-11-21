# 在网紧急私呼降级：怎样区分 403、200/149 和撤警结果？

MCPTT 控制功能（CF）收到同一通在网紧急私呼的 re-INVITE，业务正文 `emergency-ind=false` 请求把通话降为普通优先级。它不是 SIP BYE，也不是 SIP CANCEL。若这份请求还写 `alert-ind=false`，CF 要另查撤销紧急告警的权限。两项可以给出不同结果。本页限 TS 24.379 V16.14.0 的在网、带话权控制、一对一私呼程序，不用初始紧急 INVITE、预建立 REFER、离网消息或组呼过程替代。[§11.1.1.4.4，印 384–386](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=385)；[§11.1.1.4.6，印 386–387](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=387)。

## CF 在哪一步拒绝了降级？

先对上 CF 实际收到的 re-INVITE 和该请求的响应，再核对 SDP、业务正文、用户权限和 `Resource-Priority`，不能只看 SIP 状态码：

- SDP offer 中没有一个媒体流同时满足媒体参数可接受、且至少有一种 codec 或媒体格式可接受：回 488，停止后续步骤。
- 正文组合不合法：例如 `emergency-ind=false` 还包含 `imminentperil-ind`，即便后者也是 false；校验程序回 403，Warning 文本码为 150。就组合校验而言，`emergency-ind=false` 时必须没有 `imminentperil-ind`，但 `alert-ind` 可带可不带。
- **用户无权取消私呼紧急状态**：用请求方 MCPTT ID 对应的用户配置，`allow-cancel-private-emergency-call=false` 或缺失均不授权。CF 回 403，`application/vnd.3gpp.mcptt-info+xml` 正文必须有 `emergency-ind=true`；若请求还明确写 `alert-ind=false` 且撤警也未获授权，正文再写 `alert-ind=true`，随后停止。
- **入站优先级头还填着配置的紧急值**：即使私呼取消已获授权，若实际带了这一紧急档，CF 仍回 403 并停止。这一步没有规定前一项的恢复正文，不凭缺正文就推断是哪一条拒绝。CF 这一步没有规定“缺头即拒”。发起客户端另须按自己的步骤带普通档；不能拿服务端的守卫放宽客户端的构造规则。

这些响应拒绝的是本次请求，不能当作已有通话释放或已降级。客户端程序也区分正文：负响应中看到 `emergency-ind=true` 时恢复进行中的紧急优先级；完全没有 MCPTT 业务正文时，恢复紧急优先级并把告警状态恢复到进入程序前的值。这条回退不能替代 CF 的拒绝原因分类。[§11.1.1.2.1.4 步骤 4、负响应步骤 1–3 与注 2，印 360–361](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=361)；[§6.2.8.3.3 普通优先级分支，印 73](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=74)。撤警权限按请求方的 `allow-cancel-emergency-alert` 单独判；该条只列 true 和 false，没有给字段缺失定默认值。[§11.1.1.4.4 步骤 1–4，印 384–385](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=385)；[§6.3.3.1.13.3–.4，印 113](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=114)；[§6.3.3.1.17，印 117–118](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=118)；[表 4.4.2-2 的 150 行，印 37](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=38)。

## 获准降级后，CF 清哪份状态、给对端发什么？

走到授权取消私呼紧急状态的分支，CF 清的是**原紧急私呼发起者与该目标用户之间**的进行中紧急私呼记录。只有请求明确带 `alert-ind=false` 且撤警获准，才另清尚未撤销的紧急告警记录：有 `originated-by` 就用它所指的 MCPTT ID，没有才用本次 re-INVITE 发送者的 MCPTT ID。这个选择决定清谁的记录，不是授权身份的来源。不带 `alert-ind` 不等于请求撤警。该缓存动作发生在给对端发 re-INVITE 之前，不能据此判定对端已接受。[§11.1.1.4.4 步骤 5–6，印 385](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=386)；[§6.3.3.1.13.3–.4，印 113](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=114)。

CF 向入站 `resource-lists` 所列用户发出新的 re-INVITE。复制收到的 MCPTT 业务正文后，获准降级时写 `emergency-ind=false`，并用 MCPTT 业务配置里的 `normal-resource-priority`（namespace 与 priority），不是透传原紧急档或填一个固定数值。入站明确请求撤警时，获准则出站 `alert-ind=false`，有 `originated-by` 则按该分支复制；未获准则出站改写为 `alert-ind=true`。所以即使两端日志里 `emergency-ind` 都是 false，`alert-ind` 仍可能一端为 false、另一端为 true。 §11.1.1.4.6 的 3b、3c 字面写的是入站 SIP INVITE；这里按该节入口和步骤 2 讨论同一次降级的 re-INVITE，不另假定一份初始 INVITE。[§11.1.1.4.4 步骤 6，印 385](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=386)；[§11.1.1.4.6 步骤 1–5，印 386–387](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=387)；[§6.3.3.1.19，印 118–119](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=119)。

## 200 上有 149，再查哪个对话？

客户端取消过程明列按需和预建立两种会话，取消仍发 re-INVITE；不要因通话原用预建立会话，就拿初始 REFER 的应答代替本次应答。客户端收到本次 re-INVITE 的 2xx 时，步骤 2、3 分别把私呼优先级和紧急私呼状态置为 `MEPP 1`、`MEPC 1`；另列的撤警判断不能并入这两步。[§11.1.1.2.1.4 入口及 2xx 步骤 2–4，印 360–361](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=361)。

先分两段。CF 收到它向对端发出的 re-INVITE 的 200 时，按 §11.1.1.4.6 缓存该响应的 Contact；若尚未给邀请客户端回这笔响应，CF 另行生成上游的 200，写对入站 offer 的 SDP answer，再按程序与媒体面交互并发出响应。在**入站确实写了 `alert-ind=false`、而撤警未获授权**的分支，回给邀请客户端的 200 要带 Warning 文本码 **149**。这个码不是 SIP 状态码，也不是 Warning 头的外层 399；该 200 不能确认告警已撤，更不能证明已收到后续 INFO 或媒体。[§11.1.1.4.4 的 200 分支，印 385–386](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=386)；[§11.1.1.4.6 的 200 分支，印 387](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=388)；[§4.4.1，印 33](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[表 4.4.2-2 的 149 行，印 37](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=38)。

CF **实际收到对这份带 149 的上游 200 的 ACK**后，才进入这里的 INFO 步骤。向邀请客户端的同一对话发 `Info-Package: g.3gpp.mcptt-info` 的 SIP INFO；对未获准撤警的分支，正文写 `alert-ind=true`，不从别的 INFO 分支附加 `emergency-ind=true`。若接收端确实进入 §6.2.8.3.7 的 INFO 处理且在 `MPEA 4`（等待撤警结果），true 使它回到 `MPEA 3`（告警仍在），false 才使它进 `MPEA 1`（无告警）；本拒绝分支的值是 true。别用 CF 的发送记录、对端 200、任意 ACK 或其他对话的 INFO 替代客户端实际收到的结果。[§11.1.1.4.4 的 ACK 分支，印 386](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=387)；[§6.3.3.1.18，印 118](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=119)；[§6.2.8.3.7 步骤 2，印 75](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=76)。

**原文的接收入口有一处不能省略的差异。** §11.1.1.2.1.4 是私呼取消程序，但注 1 的预建立会话说明写到“组会话”，2xx 步骤 4 写成“优先组呼”的请求响应，末段的 INFO 入口又把 Request-URI 写成标识进行中的“组会话”。上段可确认 CF 该发什么、以及真正进入通用 INFO 处理后的状态转移；不能把“组”直接改成“私”来宣布终端一定会分派这条 INFO，也不能把无 149 当作无需核对条件的撤警成功。[§11.1.1.2.1.4 的注 1、2xx 步骤 4 及末段，印 361](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=362)。

如果实际是[初建紧急私呼时请求发告警](emergency-private-call-alert.md)，看发警授权和等待确认状态 `MPEA 2`。若抓到的是[释放整通在网私呼的 BYE](server-private-call-release.md)，查释放而非降级。离网使用[另一套紧急私呼降级流程](offnetwork-private-emergency-downgrade.md)。本页不推断全部终端和媒体状态已同步，不补 SIP 核心网或媒体面的外部接口实现。
