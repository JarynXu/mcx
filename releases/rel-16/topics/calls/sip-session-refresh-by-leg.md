# MCPTT 按需私呼的 SIP 会话刷新：哪一段由谁刷新？

同一场私呼，一处 SIP 200 的 `Session-Expires` 把 `refresher` 写成 `uac`，另一处写成 `uas`，两处可以都对。UAC 指**该段 INVITE 的发起方**，UAS 指该段的应答方。参与功能可以在一段应答 INVITE，又在下一段发起另一份 INVITE。对照刷新责任前，先把每份 200 配到它应答的那份 INVITE。

下表限 Release 16、Stage 3，普通在网、单被叫、带话权控制的按需 MCPTT 私呼。两端都走按需会话，未借用预建立会话。只比较初始 INVITE 的最终 200，不含 PRACK、UPDATE 或 re-INVITE 的应答。O-PF 和 T-PF 分别是发起侧和终接侧的参与 MCPTT 功能；CF 是控制 MCPTT 功能。

| 这一段的初始 INVITE | 谁生成最终 200 | 200 中的刷新责任 |
| --- | --- | --- |
| 主叫终端 → O-PF | O-PF 另生成 200 回主叫；还须启动该侧 SIP 会话定时器。 | 主叫发到 O-PF 的 INVITE 未带 `refresher` 时，须填 `uac`，由**主叫终端**刷新。[§11.1.1.3.1.1 收到 200 后第 1、6、8 项，页 370](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=371)；[§6.3.2.1.5.2 第 1–2 项，页 87](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=88)。 |
| O-PF → CF | CF 为自己的入向 INVITE 生成 200，并监督该 SIP 会话。 | 此处明确要求填 `uac`，由 **O-PF** 刷新。规定不以入向 INVITE 是否省略该参数为条件。[§11.1.1.4.2 普通 private 成功分支，页 382](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=383)；[§6.3.3.2.3.2 第 1–3 项，页 120](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=121)。 |
| CF → T-PF | T-PF 按实际走的按需自动或手动应答程序生成 200。 | CF 生成这份初始 INVITE 时须省略 `refresher`；T-PF 收到的这份 INVITE 未带该参数时，200 须填 `uas`，由 **T-PF** 刷新。[§11.1.1.4.1 第 1 项，页 378](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=379)；[§6.3.3.1.2 第 6–7 项，页 106](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=107)；[§11.1.1.3.2 第 7–8 项，页 377](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=378)；[§6.3.2.2.5.1–2，页 95–97](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)、[§6.3.2.2.6.1–2，页 98–100](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=99)、[§6.3.2.2.4.2 第 1–2 项，页 95](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)。 |
| T-PF → 被叫终端 | 被叫终端自动应答，或手动接受后回 200。 | 被叫终端回的 200 须填 `uas`，由**被叫终端**刷新。它和上一段都可写 `uas`，但两段的应答方不同。[§11.1.1.2.1.2 第 9–10 项，页 358](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=359)；[§6.2.3.1.1 第 2、5 项及 §6.2.3.2.1，页 58–59](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=59)。 |

这四段的最终 200 都须带 `Require: timer` 和 `Session-Expires`。它们各自回答本段的请求；不能把对侧收到的 200 当作本段原样返回的 200。CF 生成给 T-PF 的 INVITE 中，`Session-Expires` 是建议项，若有该头也不得填 `refresher`；`Supported: timer` 是必带项。不要把初始请求和最终响应的要求混用。

## 抓包先对请求，再定刷新方

先核对响应的 CSeq 方法是 INVITE；用该侧的 Call-ID、CSeq 和对话标签对上请求，确认该侧谁发 INVITE、谁回 200。再读**收到的这份 INVITE**有无 `refresher`。不能用主叫一侧的原始请求推定 T-PF 收到的字段，也不能假定四段共用 Call-ID。若 O-PF 或 T-PF 收到的 INVITE **显式带了** `refresher`，表里的两个“未带时”默认值就不是判断依据。两条参与功能的 helper 把响应的生成交由 RFC 4028 的 UAS 规则，并未写成“总是回默认值”或“总是原样复制”。只有一个 200，可以读出该响应写了谁负责，不能凭此证实默认分支适用，或证明负责的一端后来真的发了刷新请求。若 T-PF 收到的初始 INVITE 显式带参数，还应对照 CF 的发出记录定位字段在哪一段出现，不要仅凭收包就断言是谁写入的。

**不要套到聊天组 CF 的 200。** 普通在网按需聊天组用 §10.1.2.4.1.1 第 17–18 项：建议加入 `Session-Expires` 并监督 SIP 会话，建议省略 `refresher`；若填写则须是 `uac`。第 18 项仍要求 `Require: timer`。这是与表中普通私呼 CF 不同的响应程序。[§10.1.2.4.1.1 第 17–18 项，页 290](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=291)。

## 会话刷新和本次私呼的最长时长是两套证据

CF 发起邀请时另启动私呼业务计时器，取为该用户配置的最大私呼时长；到期走私呼释放程序。SIP 的 `Session-Expires` 只属于具体 SIP 对话，不能取代 CF 的业务计时器配置、启动和到期记录。即使某段 SIP 刷新成功，也不能据此排除私呼达到最长时长。仅抓到 BYE 同样不能区分是私呼最长时长、媒体面报告 T4 到期，还是只剩一名或没有参与者。要判断是哪一项触发释放，查 CF 对同一场私呼的记录，再配对应的 BYE。组呼的 TNG3 另见[聊天组 BYE 与单人或整场释放](chat-participant-or-session-release.md)。[§11.1.1.4.1 第 9–10 项与到期段，页 379](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=380)；[§6.3.8.2，页 136](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=137)；[§11.1.4.4，页 390](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=391)。

查私呼如何到达各服务器、控制侧与发起侧怎样应答，见[普通在网按需私呼的服务端受理与续转](private-server-admission-routing.md)。查配置的最长时长真正到了以后 CF 怎么释放，见[服务器发起的私呼释放](server-private-call-release.md)。

来源：[3GPP TS 24.379 V16.14.0 / ETSI TS 124 379 V16.14.0，Release 16](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf)。
