# 预建立私呼：主叫的 REFER 收到 200，怎样查这通私呼的结果？

主叫甲已有一条预建立会话，现在要呼叫乙。先看 200 回答了什么请求：**回答甲的 REFER，只表示发起侧参与功能（O-PF）已接受这份请求。** O-PF 接下来才另发一份业务 INVITE；仅看 REFER 的 200，连这份 INVITE 是否已经发出都不能确认，更不能记为乙已接听。

这里限同一 MC 系统、归属网、在网、有话权控制的普通 MCPTT 私呼，甲直接指定乙的 MCPTT ID。甲还可以附上自己的功能别名，字段的位置和保留条件见[预建立私呼怎样携带主叫别名](private-caller-alias-forwarding.md)。这里查发起侧的事务结果，不讨论按别名寻找被叫、首个应答者呼叫、紧急私呼、无话权控制、转接、Replaces 或被叫侧处理。[TS 24.379 V16.14.0，Rel-16，Stage 3，§11.1.1.1，印 352](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=353)

## 甲要找乙，为什么 REFER 的 Request-URI 不是乙？

甲要让服务自己的 O-PF **用已有会话发起业务**，所以发的是对话外 REFER，另用字段标出旧对话和被叫。读这份请求时，三处不能互换：

| 在 REFER 中看哪里 | 标识什么 |
| --- | --- |
| Request-URI | O-PF 上标识这条预建立会话的公共业务身份（PSI）。这不是乙的地址。 |
| Target-Dialog | 所指的既有预建立 SIP 对话。该头出现在新发的 REFER 中，不表示 REFER 在旧对话内发送。 |
| Refer-To → `cid:` → Content-ID 对应的 `application/resource-lists` 正文 | 普通私呼只有一个 `<entry>`；其 `uri` 是乙的 MCPTT ID。该 URI 的 `body` 参数（hname）内，MCPTT 信息体的 `<session-type>` 为 `private`。 |

甲须带 `Require: multiple-refer`；这个标签不表示要呼叫多个人。甲还须带 `Refer-Sub: false` 和 `Supported: norefersub`；O-PF 收到两者且走到对应步骤时，不建立 REFER 隐式订阅。[§11.1.1.2.2.1，起首及项 1–4、7–8、12，印 362–364](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=363)；[§6.3.1.2，印 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=79)；[§11.1.1.3.1.2 项 13，印 373](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=374)

## O-PF 会拒绝 REFER，还是另发 INVITE？

O-PF 按预建立会话 REFER 的入口处理。它从收到的 REFER 的 `P-Asserted-Identity` 取公共用户身份，用绑定找出**甲**的 MCPTT ID。资源列表中的单条 `private` 让它识别这是一通普通私呼。O-PF 再确定**与甲的 MCPTT ID 关联、提供私呼服务的控制功能（CF）**的 PSI。这是下一份 INVITE 的 Request-URI，不是从乙的 `entry.uri` 复制，也不是照抄上一份 REFER 的 Request-URI。规范没有规定 O-PF 怎样发现这个 CF 的 PSI。[§11.1.1.3.1.2 项 2–8、注 2，印 370–371](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=371)

下表只列主叫绑定、被叫资源列表和 CF 识别三类检查中，原条款明写**拒绝 REFER 并停止后续步骤**的情况，不是完整的拒绝清单。Warning 后的数字是警告文本中的 MCPTT 码，不是 SIP 状态码。

| O-PF 在该步发现什么 | 对这份 REFER 的答复 |
| --- | --- |
| 找不到主叫公共身份到 MCPTT ID 的绑定，或绑定已过期 | 404，Warning 141 |
| 没有 Refer-To 的 cid 所引用的资源列表正文；或引用的列表只有一个 entry，其 MCPTT 信息体的 session-type 不是 private | 403，Warning 145 |
| 不能识别与主叫 MCPTT ID 关联的私呼 CF | 404，Warning 142 |

这些是各步骤的明文条件，不是任意头字段缺失、报文解析失败时的通用返回码。原文另有几处请求名不一致：资源不足或有拥塞风险的项 1 写的是**可**用 500 拒绝 INVITE，500 响应可带 `Retry-After`。同一项还明写不得继续后续步骤。项 9 的 403/107 一处说拒绝 REFER，一处说响应 INVITE，未明写停止；项 10(c)、(d) 的 403/143、403/144 写拒绝 INVITE，并各自明写停止。这些都出现在处理 REFER 的段落里，不能据此给线上某笔 INVITE 指派这些错误；应以实际请求、响应和所在步骤区分。[§11.1.1.3.1.2 项 1、3–10，印 370–372](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=371)

若各项检查允许继续，O-PF **先**生成最终 200 并就 REFER 朝甲发送，**再**生成一份初始业务 INVITE，以甲的私呼 CF 的 PSI 为 Request-URI 发出。它不是把甲的 REFER 原样转发，也不是在旧对话里给甲发 re-INVITE。甲实际收到 REFER 的最终 2xx 时，须按 TS 24.380 与媒体面交互；这是甲自己的收件，不能替代 O-PF 对业务 INVITE 的收发记录。[§11.1.1.3.1.2 项 14–17、20，印 373–374](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=374)；[§6.3.2.1.4，初始 INVITE，印 85–86](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=86)；[§11.1.1.2.2.1，REFER 最终应答，印 364](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=365)

## O-PF 收到业务 INVITE 的响应，会不会转给主叫？

先在 O-PF 找到发给私呼 CF 的那份 INVITE，再把实收的响应与它配对。只凭相同的状态码会把两笔事务混起来；不要假定 REFER 与另发的 INVITE 必须使用相同 Call-ID。

| O-PF 实际收到对这份 INVITE 的什么响应 | O-PF 在这个分支做什么 |
| --- | --- |
| 临时响应，例如 180、183 | 丢弃，不转给主叫；主叫侧没看到 183，不能反推 CF 没发过。 |
| 200 OK，且对应普通私呼 | 按 TS 24.380 与媒体面交互。此处入口写的是 INVITE **200**，不是对所有 2xx 作同一规定。 |
| 4xx、5xx 或 6xx | 按 TS 24.380 与媒体面交互。这是业务 INVITE 的失败，不能把已经回过 200 的 REFER 改判为失败，也不能把这个错误码记作主叫实收的 SIP 响应。 |

若只抓到 REFER 的 200，缺的是 O-PF 侧这份业务 INVITE 及其响应；若只抓到 INVITE 的临时响应，还缺最终响应。抓包缺项不能判成功或失败。上述媒体接口没有给出本次具体发了哪种媒体控制消息、用户看到了什么、话权是否已授或 RTP 是否已到；也不能据此要求普通私呼一定再发 re-INVITE。本页不为 3xx 或超时推定结果。[§11.1.1.3.1.2，项 20 后临时响应与 200、4xx/5xx/6xx 各段，印 374–375](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=375)

若是在核对更早的建会 INVITE，查[预建立会话本身的建立](preestablished-session-lifecycle.md)。若另有实际收发的 MCPC Connect 或 Accepted，要判断是哪条会话得到确认，查[预建立会话的媒体控制应答](../media/preestablished-connect-outcome.md)。
