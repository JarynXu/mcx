# MCPTT 组播状态报告：暂停预告与撤回怎么报，PF 何时回 403？

先看**哪一端收到 MESSAGE**，再检查实际携带的 XML 正文。承载通告与终端的监听、暂停报告都可以使用 `application/vnd.3gpp.mcptt-mbms-usage-info+xml`。MIME 类型相同，不代表可以向同一端发送同一种内容。在正常回报路径上，终端从通告取 PF 的 MBMS 公共业务身份（MBMS PSI）；终端发监听或暂停报告时，把这项身份放在 `Request-URI`，在另一份 `mcptt-info` 正文的 `mcptt-request-uri` 中写自己的 MCPTT ID。[TS 24.379 V16.14.0，§14.3.2，印 470–471](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=471)；[§14.3.3.2，印 473](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=474)及[印 474](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=475)。

<a id="suspension-report"></a>
## 告知即将暂停和撤回暂停，各在什么时候报？

先看**同一条承载**的两项记录：终端最近一次上报的监听状态须为 `listening`，并且未收到把 `report-suspension` 设为 `false` 的承载通告。后一个条件不要求通告显式写 `true`。在这两个前提下：

- **`suspending`（即将暂停）。** 无线接入网（RAN）通知终端这条承载将暂停，终端须上报这个决定。计划在下一个 MCCH 修改周期开始时生效；上报时不表示承载已经停了。
- **`not-suspending`（撤回暂停）。** 终端已经上报这条承载即将暂停，尚未检测到实际暂停，又收到 RAN 撤回决定的通知，才须上报这一状态。RAN 撤回的是原定在下一个 MCCH 修改周期开始时生效、尚未生效的决定。已经暂停后恢复传送，是另一种事件。单有一条收包间隙或“现在有流量”的记录，不能补出上述历史。

依据：[TS 24.379 V16.14.0，Rel-16 Stage 3，§14.3.3.1，印刷页 472–473](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=473)；[§F.2.3(2a)、表 F.2.3-2，页 555–556](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=556)。这是 MCPTT 客户端的 SIP 报告规程；若要查公共流程由谁选上报者，读[Stage 2 暂停上报](mbms-suspension-reporting.md)。

## 同一份报告列了两条承载，是不是两条都要停？

**看 TMGI 写在哪个元素里，不要只看总数。** MCH 是多播传输信道，一个 MCH 可以承载多个多播业务逻辑信道（MTCH）。终端用 SIP MESSAGE 上报，MBMS usage 正文的 `version` 为 1。两种状态分开发消息。

| 状态 | 哪些标识进入报告 | `number-of-reported-bearers` 怎样计数 |
| --- | --- | --- |
| `suspending` | 按 MCH 分报。对同一 MCH 中每个即将暂停的 MTCH，程序要求在 `suspended-TMGI` 中给出对应承载的 TMGI。若知道同一 MCH 上其他 MTCH 的 TMGI，可以列为 `other-TMGI`；这不是说它们也将暂停。 | 这份报告实际包含的 `suspended-TMGI` 和 `other-TMGI` 元素个数之和。 |
| `not-suspending` | 用 `suspended-TMGI` 指明撤回决定涉及的各个 MTCH 所对应的承载；元素名不表示曾经发生了暂停。此分支没有要求填 `other-TMGI`。 | 只数这份撤回报告内的 `suspended-TMGI`。 |

例如，MCH 一上的甲将暂停，乙只是同信道的另一条承载；MCH 二上的丙也将暂停。终端可在第一份报告列甲和乙，计数为 2。乙未列出时，计数为 1，两种写法里被报告将暂停的都是甲。丙通过另一份报告上报。若后来只撤回甲，且满足上节撤回条件，撤回报告列甲，计数为 1，不用把上一份报告里的乙照抄过来。[§14.3.3.2 暂停上报段第 1e–g、2 项及注 3、4，页 474](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=475)；[§F.2.3(2b–d)，页 556](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=557)。

**同一 MCH 有两个 MTCH 均将暂停时，要区分程序要求和 XML 能表达什么。** §14.3.3.2 要求逐个给出受影响的 TMGI；但 §F.2.2 的 `mbms-suspension-statusType` 中，`suspended-TMGI` 未写 `maxOccurs`，默认上限为 1；可重复的是 `other-TMGI`。在同一个状态容器放两个同名的 `suspended-TMGI`，不符合所列 XSD；把第二个改叫 `other-TMGI` 又改了它的含义。计数字段也有文字差异：XSD 类型是 `xs:integer`，§F.2.3(2b) 却用十六进制二进制数描述它。可以按上表解释个数，但不能据此给出本版已证明互通的多目标拆包方案或任选十六进制线格式。[§F.2.2，页 553–554](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=555)；[§F.2.3，页 555–556](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=557)。XSD 能查元素次数和类型；即使校验通过，也要另核计数是否与实含元素一致、标识是否属于对应 MCH，以及终端是否满足上报条件。这些差异不改变报告的寻址规则，也不能用来推定 PF 必回 403。

## 参与功能 PF 收到的是通告，还是有身份问题的上报？

§14.2.4 针对 PF 收到带上述 MBMS usage 正文的 SIP MESSAGE。**以下任一条件成立，PF 须回 SIP 403：**

| 完整来件及 PF 的绑定记录 | 按这条规范怎样判 |
| --- | --- |
| `P-Asserted-Identity` 指出的公共用户身份未关联到任何由这个 PF 服务的 MCPTT 用户。 | 满足第一项。不要求另有 mcptt-info 正文，也不要求 usage 正文含通告、监听或暂停状态。 |
| MBMS usage 正文有一个或多个 `announcement`，同时 `mcptt-info` 正文的 `mcptt-request-uri` 指出这个 PF 服务的 MCPTT 用户。 | 满足第二项。有服务对象也不能把这条消息作为有效的终端报告；不要求第一项同时成立。 |

所以，截到一笔 PF 回的 403，不能只凭状态码断言用户未注册、绑定查不到，或通告发反了。若只截到 `announcement`，没拿到另一份正文，也不能说已经证实第二项。终端收到符合 §14.3.2 的承载通告，走的是另一套程序，不能把 PF 的 403 倒用到终端。[§14.2.4、§14.3.2，印 470](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=471)。

## 同一个 PF 服务甲和乙，两边名字都查得到，报告就能接收吗？

**仍要核对那一对身份是否绑定。** 正常报告用 `mbms-listening-status` 或 `mbms-suspension-status`；其 `mcptt-info` 正文须给出这个 PF 服务的 MCPTT ID。§14.2.3 要求 PF 查这次来件里 `P-Asserted-Identity` 的公共用户身份是否绑定到**正文中的这个 MCPTT ID**。例如，头指向甲，正文写乙，两人都由这个 PF 服务，且两者没有这项绑定。若这一笔不含通告，不能套 §14.2.4 的两项条件断言必须回 403；也不能按 §14.2.3 的绑定通过分支处理乙的状态。§14.2.3 的绑定检查没有为这一种失败单列 SIP 状态码。[§14.2.3，印 468–469](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=469)及[印 469](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=470)；[§14.2.4，印 470](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=471)。

排查时把三项分开记录：**这段 MESSAGE 寻址的 PF**（看 `Request-URI`，再核实际收件记录）、**谁在上报**（PF 收到的 `P-Asserted-Identity`）、**上报指向谁**（`mcptt-request-uri`）。§4.2 的配置假定中，MBMS PSI 与服务该用户的 PF PSI 是同一 URI；这不是头部用户身份和正文身份可以互换的理由。查完路由与身份也不能拿 SIP 响应代替终端实际监听或承载切换的证据。[§4.2，印 33](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[§6.3.1.3，印 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=79)；[§14.2.3，印 468–469](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=469)。

已有正常监听报告，需复核中继切换前后的承载／报告链路，查[锚定会话的接入转移](anchored-session-transfer.md)。若收件方确是终端，查[如何处理通告和撤告](mcptt-mbms-announcement-sdp.md)。若要确认无线暂停、恢复及客户端该不该上报，查[MBMS 暂停上报](mbms-suspension-reporting.md)。
