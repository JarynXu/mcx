# 预安排组呼离会：为什么 REFER 的 200 早于控制侧 BYE？

手持台通过预建立会话参加一通普通的在网预安排组呼，想离开这通组呼。**服务它的参与功能（PF）先给终端的 REFER 回 200，再另向控制功能（CF）发业务 BYE。** 这两份应答对应不同请求。这个先后说的是 PF 的发送顺序，不保证终端先收到 200，也不保证各处抓包按这个顺序出现。REFER 的 200 不能证明控制侧 BYE 已有结果或整场已释放。以下限普通、单系统、已经建立的预安排组呼。[§10.1.1.2.3、§10.1.1.3.3，印刷页 229、239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)；[§6.3.2.1.7 第 4–7 项，印刷页 88](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=89)

## 终端只想离会，目标写在哪？

终端先与媒体面交互，再在对话外发初始 REFER。Request-URI 是服务端标识**预建立会话**的 PSI（公共业务身份），Target-Dialog 也标识这项预建立会话。Refer-To 中才放**要离开的业务会话标识**，并把这一 URI 的 method 参数设为 BYE；请求方法仍是 REFER。终端要带 Refer-Sub: false 和 Supported: norefersub；实际收到这条 REFER 的 2xx 后再与媒体面交互。[§6.2.4.2，印刷页 60](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=61)

按需建立的组呼离会使用终端发出的业务 BYE，Request-URI 指业务会话。若终端实际要拆**整项预建立 SIP 会话**，它在预建立会话自己的对话内发 BYE，Request-URI 是预建立会话的 URI。不能只看是否出现 BYE 字样，就把三种操作填成同一种。[§6.2.4.1–2，印刷页 60](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=61)；[§8.4.1.1，印刷页 165](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=166)

## 两个 200 分别回答什么？

1. **PF 回终端的 REFER。** PF 从 P-Asserted-Identity 中的公共用户身份查 MCPTT ID 绑定。找不到时回 403，Warning 文本编号 141，并停止。没有被这项检查挡住，PF 须先生成并发送 REFER 的 200。正常来件带上述两项头时，PF 不建这次 REFER 的隐含订阅；200 带 Supported: norefersub，请求有 Refer-Sub: false 时也带同样的值。不必等这次 REFER 引起的订阅 NOTIFY；另行订阅的会议事件不受这句话排除。
2. **PF 发给 CF 的业务 BYE。** PF 把收到的 Refer-To 里的业务会话标识用作新 BYE 的 Request-URI，复制原 REFER 的 P-Asserted-Identity，发往 CF。PF 实际收到这条 BYE 的 200 后，须与媒体面交互释放它与 CF 之间这条 SIP 会话关联的媒体资源。排障要分别找 PF 的发包、对端对本次 BYE 的答复和 PF 的媒体处理；第一份 200 不能代替后两项。[§6.3.2.1.7，印刷页 88](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=89)

## 发起人退出后，其他人为什么还能说？

CF 收到业务 BYE 后，先与媒体面交互释放离会这条 SIP 会话关联的资源，并发该 BYE 的 200，然后才检查整场释放策略。发起人走了会不会结束整场，要看**本地策略是否要求这样处理预安排组呼**。以下是其他独立触发条件：CF 从媒体面收到本场 T4 不活动计时器到期指示；只剩一名或没有参与者；在场的已归属组成员不足所需下限；本场 TNG3 到期。只看到发起人离开，不能替这几项作判断。[§6.3.3.2.4 第 1–5 项，印刷页 121](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=122)；[§6.3.8.1，印刷页 136](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=137)

需要结束整场时，CF 按释放程序向本场所有参与方发送 BYE；不需结束时，CF 向仍在本场且订阅了会议事件的客户端发 NOTIFY。要认定整场结束，要查 CF 的决定和各条业务腿的处置，不拿一名离会者收到的 200 或一条会议通知代替。要查某台终端是否收到请求、完成释放，再看它这一腿及媒体处理的记录。[§6.3.3.1.5，印刷页 106–107](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=107)；[§6.3.3.2.4，印刷页 121](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=122)；[§10.1.1.4.3、§10.1.1.4.4.2，印刷页 251](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=252)

实际收的是预建立对话内的 BYE，读[拆正在使用的预建立会话](preestablished-session-in-use-release.md)。实际是聊天组，读[聊天组一人离开与整场结束](chat-participant-or-session-release.md)。若手头只有会议事件的 NOTIFY，读[会议参与者通知](conference-participant-status.md)。
