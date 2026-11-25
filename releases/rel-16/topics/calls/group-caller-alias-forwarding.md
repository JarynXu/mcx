# 普通 MCPTT 组呼：终端带了主叫功能别名，CF 为何可能看不到？

甲用自己的“北站值班”别名（F）呼叫组 G。**F 标识主叫；G 才是目标组。** 终端带 F，不代表起始参与功能（O-PF）发给组控制功能（CF）的 INVITE 也带 F。先认出终端用的是按需 INVITE，还是利用已有预建立会话的 REFER，再核对 O-PF 实收的内容和检查结果。

下文限同一 MC 系统、普通在网 MCPTT，以直接组身份发起预安排组或受限聊天组，包含按组身份加入。原请求和目标组状态均非紧急或迫近危险，不含广播、临时组或重组；不处理按既有业务会话身份重入、服务器迟入邀请、已在场通话升级或以别名作被叫。依据 TS 24.379 V16.14.0，Rel-16 Stage 3。

## 按需：查终端 INVITE 自带的正文

甲的初始 INVITE 发给服务它的 O-PF。组 G 写在 `mcptt-info+xml` 的 `mcptt-request-uri`，业务类型是 `prearranged` 或 `chat`。终端知道有哪些别名已启用，且本次要带其中一个时，须把实际使用的 F 写入同一正文的 `functional-alias-URI`。

O-PF 从**实收入站**的 `P-Asserted-Identity` 里的公共用户身份确定甲的 MCPTT ID，走到组业务 INVITE 构造时，将甲的 ID 写入 `mcptt-calling-user-id`。新 INVITE 的 SIP Request-URI 是服务 G 的 CF 公共业务身份（PSI），不是 G，也不是 F。别名与主叫 ID 一起使用；它既不替换主叫 ID，也不是拿 F 解析被叫的 `call-to-functional-alias-ind`。

| 这次处理的实际证据 | 对应检查 |
| --- | --- |
| O-PF 实收 F，且认定 **对甲的 MCPTT ID**，F 的状态为 `activated` | 出向业务 INVITE 保留收到的 F 原值。 |
| O-PF 实收 F，但对同一个甲与 F 查到的状态不等于 `activated` | 新 INVITE 不带该元素。乙也使用 F、甲正在 `activating`，都不能代替甲的 `activated`。省略别名不是拒绝整通组呼。 |
| 完整的 O-PF 入站正文没有 F | 这一步不要求另找一个别名补上。若只是没抓到完整入站包，不能判定甲没带。 |

按需预安排见[客户端第 10、14(e) 项，印 220–221 / PDF 221–222](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=221)、[O-PF 第 2、2a、3 项，印 230 / PDF 231](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=231)及[第 9–13a 项、注 8，印 231 / PDF 232](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=232)，即 §§10.1.1.2.1.1、10.1.1.3.1.1。按需聊天组见[§10.1.2.2.1.1 第 9、13(d) 项，印 266 / PDF 267](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=267)、[§10.1.2.3.1.1 第 2、2a、3 项，印 276 / PDF 277](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=277)及[第 9–11a 项、注 8，印 277 / PDF 278](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=278)。通用正文复制见[§6.3.2.1.3 第 8 项，印 85 / PDF 86](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=86)，身份用途见[F.1.3(k)、(o)，印 551 / PDF 552](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=552)。

## 预建立：查 REFER 内层，再查另外生成的 INVITE

甲发的是**对话外 REFER**。它的 Request-URI 和 `Target-Dialog` 指明要用的预建立会话。沿 `Refer-To` 的 `cid:` 找到 Content-ID 对应的资源列表，列表的单一 `entry` 的 URI 标识 G；进这个 URI 的 headers 部分，找到 `body` 参数中的 MCPTT 信息正文。本次若要带终端已知的已启用别名，就在那份内层正文写 F，不是在 REFER 请求行或顶层另写一个目标。预安排组条款复用聊天组的构造，改用预安排组的条目及 `session-type=prearranged`，没有取消该别名项。

O-PF 实收相应 REFER 并通过前序检查，向组 CF 另建业务 INVITE。通用规则先把内层 MCPTT 信息正文复制到新 INVITE，**拷入的正文有 F 时**才检查别名；原文是状态 **`not active`** 时须删除该元素。查为 active 时，这一步不删除已拷入的 F；条文没有要求换上另一个别名。主叫仍从实收 REFER 的 `P-Asserted-Identity` 确定，按规则将实际主叫的 MCPTT ID 写入新正文。新 INVITE 的 SIP Request-URI 写组 CF 的 PSI，正文 `mcptt-request-uri` 从 `entry` 取 G。REFER 的 200 不是出向 INVITE 的字段记录。

[聊天组终端 §10.1.2.2.2.1 第 1–3、10 项，印 273–275 / PDF 274–276](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=274)，[第 3(c)(ii)(C) 项，印 274 / PDF 275](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=275)，[预安排组 §10.1.1.2.2.1，印 228 / PDF 229](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=229)；[预安排组 O-PF §10.1.1.3.1.2，印 233–235 / PDF 234–236](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=234)，[聊天组 O-PF §10.1.2.3.2.1，印 282–284 / PDF 283–285](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=283)；[通用 §6.3.2.1.4 第 11、11A、12 项，印 86 / PDF 87](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=87)。

这里有两处不能替规范补齐。其一，客户端构造项把 MIME 写作 `application/vnd.3gpp.mcptt-info`，通用复制和检查项写作 `application/vnd.3gpp.mcptt-info+xml`；不据此认定两者应互换。其二，按需专条核对状态是否等于 `activated`，预建立通用规则则只写 `not active` 时删除。[§3.1，印 30 / PDF 31](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=31)把 `deactivating` 列成一个不同的状态，同时说明此时别名仍为该用户启用。只有这个过渡状态的名字时，不把按需的判断替预建立规则，也不把观察者不知道状态当成服务器已判未启用。

## 只看一条记录，容易判错什么？

- **已知 O-PF 因主叫身份绑定缺失或到期回了 404/141。** 这是前序拒绝，尚未走到别名检查，不能据此判 F 无效。反过来，发出的 INVITE 里没有 F，也不是这条身份拒绝。
- **知道终端发过启用请求，或者两腿 PUBLISH 都成功。** 仍要核 O-PF 当时对甲与 F 的状态。按需组呼的注 8 指向[§9A.2.2.2.7，印 208–209 / PDF 209–210](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=209)的别名状态学习。手动新增时，查[参与功能实际收件与更新](../identity/mcptt-functional-alias-activation-servers.md)；组呼条文没有要求每次临时发 SUBSCRIBE 或等新通知。公共业务服务器或 LMS 的[别名名单订阅](../identity/functional-alias-subscriber-list.md)是另一项 Stage 2 操作：订阅响应不含名单，即使 LMS 已收到名单，也不是本次 O-PF 的状态记录。见[TS 23.280 V16.7.0 §§10.13.2.11–13、10.13.10.1–3，印 195–196、203–204 / PDF 196–197、204–205](https://www.etsi.org/deliver/etsi_ts/123200_123299/123280/16.07.00_60/ts_123280v160700p.pdf#page=204)。
- **确认 O-PF 已发带 F 的业务 INVITE。** 这能证明该腿写入 F；证明 CF 收到要查同一笔 CF 入站。若另问普通在网预安排组的被邀终端，可在其实际收到的初始邀请检查别名；[§10.1.1.2.1.2 第 6A 项，印 222–223 / PDF 223–224](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=224)只说可以显示。不能从发出或没显示反推另外两腿，也不证明已归属、已应答或媒体已通。

若要判断[普通按需预安排组的准入与邀请](prearranged-server-admission-routing.md)，须确认是**同一 MC 系统内、GMS 管理、按直接组身份发起的普通在网按需预安排组**。组文档不含 temporary/regrouped，目标既不是临时组的组成组（constituent），也不是预配置重组。按待判断的角色查它**实际收到的本次初始 INVITE**：查 O-PF 看它收到的终端请求，查 CF 看它收到的业务请求。无需证明两边均已收到才查其中一边，O-PF 仅有出站记录也不能代替 CF 实收。若核的是**同系统用直接受限聊天组身份发起的普通在网按需呼叫**为何被拒，查[普通聊天组准入](chat-establish-join.md)。若实际是**同系统直接普通在网 MCPTT 聊天组用预建立会话**，要核 REFER 200 与业务应答及隐式归属，看[两腿响应的边界](chat-preestablished-refer-outcome.md)。若已确认是**同系统归属网内、用对方 MCPTT ID 发给普通一对一、带话权的在网私呼**，才转到[私呼主叫别名](private-caller-alias-forwarding.md)。这些不是查普通组呼别名的必经步骤。
