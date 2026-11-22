# MCPTT 组播状态报告：谁在监听，哪条承载将暂停，PF 何时回 403？

先看**哪一端收到 MESSAGE**，再检查实际携带的 XML 正文。承载通告与终端的监听、暂停报告都可以使用 `application/vnd.3gpp.mcptt-mbms-usage-info+xml`。MIME 类型相同，不代表可以向同一端发送同一种内容。在正常回报路径上，终端从通告取 PF 的 MBMS 公共业务身份（MBMS PSI）；终端发监听或暂停报告时，把这项身份放在 `Request-URI`，在另一份 `mcptt-info` 正文的 `mcptt-request-uri` 中写自己的 MCPTT ID。[TS 24.379 V16.14.0，§14.3.2，印 470–471](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=471)；[§14.3.3.2，印 473](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=474)及[印 474](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=475)。

<a id="listening-report"></a>
## 收到 Map 就要报正在监听吗？撤告就要报不再监听吗？

先看**这台终端**遇到的事件和它此前上报过的状态。以下每一行都是单独的上报条件；满足一行的全部条件，客户端就须发送该状态的 SIP MESSAGE。

| 终端遇到的情况 | 还要核对什么 | 应报状态 |
| --- | --- | --- |
| 在通用 MBMS 信道收到 Map Group To Bearer | 终端正在参加 Map 指明的组会话，且尚未报过相应的 `listening`。例如，第一次 Map 后已报过该状态，第二次收到相同 Map，不因重发而再报。 | `listening` |
| 收到符合 §14.3.2 的承载通告，进入有通用 MBMS 可用的服务区 | MBMS 承载无线条件良好。只知道终端入区还不够；本分支未列“尚未报过”的条件。 | `listening` |
| 正在通话，收到符合 §14.3.2 的撤告 | 被撤通告的 TMGI 与该通话先前收到的 Map 中的标识一致，且尚未报过相应的 `not-listening`。 | `not-listening` |
| 没有进行中的通话，收到符合 §14.3.2 的撤告 | 此前正是因为**被撤项**所列的通用子信道可用才报过 `listening`，且尚未报过相应的 `not-listening`。 | `not-listening` |
| MBMS 承载无线条件差 | 这一项未附撤告、Map 或先前上报状态的条件。一次没抓到语音包不能代替无线条件判定。 | `not-listening` |

[TS 24.379 V16.14.0 §14.3.3.1，印刷页 471–472](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=473)。[§14.3.3.2 第 1(g) 项，页 473](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=474) 以 Unmap 为例说明怎样填写会话身份；这不是 §14.3.3.1 另列的无条件上报触发器。Map 的重发和终端的监听报告不是一对请求与确认。

<a id="listening-scope"></a>
## 同一句“不再监听”，指一通会话还是整个通用子信道？

先找 MBMS usage 命名空间 `urn:3gpp:ns:mcpttMbmsUsage:1.0` 的根元素 `mcptt-mbms-usage-info`。根下的 `version` 是必有的子元素，本程序填 1。根下的 `mbms-listening-status` 是容器，里面**同名的子元素**才是状态字符串。其后依次是可省的 `session-id`（URI，最多一个）、可省的 `general-purpose`（布尔值，最多一个），以及一个或多个 `TMGI`（十六进制二进制值）。这些都是子元素，不是属性。所列承载共用同一个监听状态。发送步骤把这个名字印作 `TGMI`；附录 F 的 XSD 和字段说明都是 `TMGI`。[§14.3.3.2 第 1(e)–(g) 项，页 473](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=474)；[§F.2.2，页 553](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=554)。

- **报的是会话子信道**：用 `session-id` 标明进行中的那一通会话。`listening` 报的是终端正在该会话的 MBMS 子信道接收 RTP 媒体包和话权控制消息；`not-listening` 报的是终端已停止监听该子信道。状态说明并非某个指定 RTP 包的收条。没有 `general-purpose` 时，`session-id` 必须存在；不应反推两字段必然互斥。F.2.3 对按需建立的会话指向建会时控制功能 Contact 中的 URI，对经预建立会话建成的通话则指向参与功能在 Connect 中给出的 URI。[§4.5（页 39）](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=40) 另规定，参与功能收到控制侧的会话身份后，会在发给终端的 Contact 中填入自己分配的会话身份，并保留它与控制功能所给身份的映射。核对[建会两侧的 Contact](../calls/session-gruu-sensitive-identity.md)，不要用组 ID 顶替，也不要假定两侧 URI 字面相同。
- **报的是通用子信道**：`listening` 配 `general-purpose=true` 表示终端在听所列承载的通用子信道，尚未为自己参与的任何会话收到 Map；不能据此把会话甲登记为已监听。`not-listening` 配 `general-purpose=false` 表示终端已不再听通用子信道。

例如，甲、乙仍在通话，同一终端此前对两通都报过正在监听。参与功能收到该终端的报告，确认另一份 `mcptt-info` 正文指向自己服务的 MCPTT ID，并核实该 ID 与请求的 `P-Asserted-Identity` 公共用户身份绑定。若报告仅指名甲不再监听，参与功能向媒体面指明的就是甲。若报告的是通用子信道 `false`，参与功能须通知媒体面该终端不再听通用子信道。其含义也覆盖甲、乙两通此前报过的会话子信道，不用逐一重列；这不涵盖别的终端或未曾这样上报的通话。`not-listening` 还要求参与功能按 TS 24.380 与媒体面交互，不表示会话已释放或某个语音包已转成单播；后者要查该包的实际下行发送。[§14.2.3，印刷页 468–469](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=470)；[§14.3.3.2 注 2，页 473](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=474)；[§F.2.3(1) 及表 F.2.3-1，页 555](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=556)。

**同一正文能否同时报告这两种监听状态？** §14.3.3.2 注 1 说可以，但所列 XSD 在根下最多允许一个监听状态容器，容器内只有一个状态值。可以重复的是 `TMGI`，不是状态；列两个 TMGI 只把同一状态用于两条承载。不能把重复容器、在字符串里拼两个值或用扩展字段当成本版已规定且互通的混合写法。[§14.3.3.2 注 1，页 473](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=474)；[§F.2.2，页 553](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=554)；[§F.2.3 表 F.2.3-1，页 555](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=556)。

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

若这份监听 MESSAGE 还携带位置 `Report`，查[同一请求里的两项上报怎样分别取证](../location/mcptt-participating-location-signaling.md#location-on-mbms-listening)。本页的 MBMS 绑定、状态更新或 403 不代替位置报告的处理结果。
