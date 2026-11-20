# 预安排组呼复用被叫的预建立会话：谁回 200，谁发 re-INVITE？

控制功能（CF）邀请一名成员加入普通预安排组呼。终接参与功能（T-PF）收到 CF 的 SIP INVITE；T-PF 与被叫终端（UE）之间另有已建立的 SIP 对话。**命中自动复用条件时，T-PF 直接答复 CF；命中人工复用条件时，T-PF 在旧对话内邀请 UE，再按实际收到的 UE 响应处理。** 判读一份 200，先找它回答的是 CF 的 INVITE，还是旧对话里的 re-INVITE。仅有前者，不能证明终端收到邀请、用户接听或语音已通。

以下限于 3GPP TS 24.379 V16.14.0（Release 16，Stage 3）的同系统、在网、普通预安排组呼终接。这里的“终接”指处理被叫来话，不是释放呼叫。UE 主动重入、紧急或迫近危险、广播、私呼和跨系统邀请不在此范围。

## 旧对话存在，T-PF 就能复用吗？

先看 T-PF **实际收到**的 CF INVITE 和它已有的被叫设置。到达终接检查时，Contact 要有 `isfocus`；T-PF 要已从该被叫的 `application/poc-settings+xml` 收到 Answer-Mode Indication，并能用本次 mcptt-info 的 `<mcptt-request-uri>` 中的 MCPTT ID 查到对应公共用户身份。缺 `isfocus` 时回 403 / Warning 104 并停止；尚未收到应答设置时回 480 / Warning 146 并停止。绑定不存在时回 404；只有找到绑定才继续。对**本次 INVITE 没有 Answer-Mode**的入口，以收到的 `auto-answer` 或 `manual-answer` 选择相应的启动程序，不能把缺头本身当成自动应答。[§10.1.1.3.2(2–8)，印刷页 238](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=239)。

两种模式都要看被叫是否有**尚未关联 MCPTT 业务会话**的预建立会话，并核对本次 offer 的两个媒体级描述：MCPTT 语音流、话权控制实体。两者都要与既有预建立会话相应的 media-level section 相同。仅有旧 SIP 对话、只匹配语音编解码器或只匹配话权控制都不够；不满足条件时，各走本模式的按需程序（§6.3.2.2.5.2 或 §6.3.2.2.6.2）。这两条选择规则没有指定多个候选如何排序。[§6.3.2.2.5.1，印刷页 95–96](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)；[§6.3.2.2.6.1，印刷页 98–99](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=99)。

下文只沿普通复用分支：本次请求也没有 `Priv-Answer-Mode`，mcptt-info 的 `<emergency-ind>` 和 `<imminentperil-ind>` 都未置为 `true`。若有该头或任一指示为真，即便有合适的旧会话，两种模式的第 1 步也另走带 `Replaces` 的分支并跳过余步。[§6.3.2.2.5.3(1)，印刷页 97–98](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=98)；[§6.3.2.2.6.3(1)，印刷页 100–101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=101)。

## 自动应答：CF 看到了 200/Unconfirmed，UE 为什么没有下一条 INVITE？

**这份 200 的发送者是 T-PF。** 它按最终响应通则为 CF 的 INVITE 构造 200，`P-Answer-State` 写 `Unconfirmed`。Contact 中的 MCPTT 会话身份映射自 CF 这次 INVITE 的 Contact。两个容易追错的来源是：

- `P-Asserted-Identity`（PAI）取自 **UE 当初建立预建立会话时发出的 INVITE**，不是这次组呼才从 UE 收到的身份。
- SDP answer 以**预建立时的协商结果和 CF 本次 offer** 为依据，按 §6.3.2.2.2.2 生成。不能把旧 SDP 原样视作本次应答，也没有一份本次 UE 200 供 T-PF 抄取。

T-PF **先向 CF 发送 200，再与媒体面交互**。本分支没有规定再向 UE 发一条 INVITE 或 re-INVITE，也不等待 UE 的 SIP 200；注 2 说明 UE 在此流程收不到通常随 mcptt-info MIME 传送的数据。只靠 UE 抓包没看到下一条 INVITE，还不能反证 T-PF 已选这个分支：要对上前述入站设置、空闲关联状态、两个媒体描述及这份 200 所答的请求。[§6.3.2.2.5.3(2–7)、注 2，印刷页 98](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=99)；[§6.3.2.2.2.2，印刷页 94](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=95)；[§6.3.2.2.4.2，印刷页 95](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)。

要判 UE 是否实际收到 MCPC Connect，应查同一预建立会话上的媒体控制收包、收包前状态和确认，再看 PF 是否实收该确认。[Connect 与 Accepted 的判读](../media/preestablished-connect-outcome.md)处理这些证据。SIP 200、MCPC 确认、话权许可和 RTP 收发各回答不同的问题；前一个不能替代后一个。

## 人工应答：旧对话的 re-INVITE 为什么没有 Answer-Mode？

T-PF 按 §6.3.2.2.6.3(2–5) 在**同一个预建立 SIP 对话**内向 UE 发 re-INVITE，把这次 CF INVITE 的 `application/vnd.3gpp.mcptt-info+xml` 正文内容复制进去，并根据**本次入站 offer** 构造 SDP offer。该条引用 §6.3.2.2.3 的请求构造规则；通则虽写 initial INVITE，这个调用点明确要求 re-INVITE，不是另起一个对话。注 1 说 re-INVITE 不能带 `Answer-Mode`；在这个对话内隐含 Manual。不要补一个线上没有的 `Answer-Mode: Manual`。[§6.3.2.2.6.3(2–5)、注 1，印刷页 101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=102)；[§6.3.2.2.1，印刷页 93](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=94)；[§6.3.2.2.3，印刷页 94–95](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=95)。

**服务器选了人工，不等于已经观察到终端执行人工应答。** UE 的 §10.1.1.2.2.2 将这条空闲预建立会话中 re-INVITE 的接收与响应引到 §10.1.1.2.1.2，并要求把文中的 INVITE 换读为 re-INVITE。但所引第 8 步的两种明文条件都是请求**带值为 Manual 的 Answer-Mode**，再判断 UE 设置为人工，或设置为自动但允许人工。本条引用没有说明如何让“不带头、隐含 Manual”满足那个显式字段检查。两处文字应各按自己的角色保留；不能据此替 UE 决定默认接受、默认拒绝、弹窗或用户已按键。[§10.1.1.2.2.2 及注，印刷页 228–229](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=229)；[§10.1.1.2.1.2(8)，印刷页 223](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=224)。

## 人工分支里，183 和两个 200 分别回答什么？

| T-PF 实际收到什么 | T-PF 对 CF 的 INVITE 做什么 | 这条记录不能证明什么 |
| --- | --- | --- |
| UE 对旧对话的 re-INVITE 回 **183** | 按临时响应通则生成并向 CF 转发相应的 183，PAI 用 UE 这份 183 的值；收到的 183 若含 mcptt-info MIME，才按通则复制该体。 | 组呼**可能**有 183。若 UE 已进入人工组呼程序，可在用户确认前自动生成 183。§6.2.3.2.2 这一步没规定何时发送；生成不等于已发送或 T-PF 实收。183 不代表用户接受，也不是所有组呼必经；本段 180 的注 2 指私呼。 |
| UE 对旧对话的 re-INVITE 回 **200** | 若实收的 SDP answer 改变编解码器或媒体格式，先与媒体面交互以更新参数。随后按最终响应通则另造给 **CF INVITE** 的 200：复制此 UE 200 的 PAI；如含 mcptt-info MIME 则复制该体。出站 SDP answer 基于此 UE 200 的 SDP answer，按 §6.3.2.2.2.1 生成（原文引用标题为 On-demand session）。T-PF 与媒体面交互后，再向 CF 发送这份 200；注 4 说明 MCPC Connect 用于把 MCPTT 会话身份给 UE。 | 旧对话的 200 只回答 UE 实收的 re-INVITE；给 CF 的是另一事务的响应，不能当成同一条 200 或 ACK。PF 执行了媒体面步骤，不证明 UE 实收 Connect、用户按过接听、已获话权或已有 RTP。 |

人工分支及其最终响应通则没有像自动分支那样在上述步骤中指定 `P-Answer-State` 的值，不把自动的 `Unconfirmed` 移过来，也不替人工填 `Confirmed`。临时响应通则仅在入站 INVITE 的 Supported 含 `100rel` 且本地策略允许时，容许加入 `Require: 100rel`；这里不以 PRACK 作为所有人工组呼的接受门槛。实查时分两腿记下请求、响应和各自的收发端：只有 CF 侧的 183/200，不能当成 UE 实收 re-INVITE 或已执行人工处理的记录；若要断言用户操作，须另有终端侧对应事件。[§6.3.2.2.6.3 对 180、183、200 的处理及注 2–4，印刷页 101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=102)；[§6.3.2.2.4.1–2，印刷页 95](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)；[§6.3.2.2.2.1，印刷页 94](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=95)；[§6.2.3.2.2，印刷页 59](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=60)。

如果问题是 CF 为何邀请这名成员，查[普通预安排组的服务器准入及邀请路由](prearranged-server-admission-routing.md)。若实际走的是按需新建邀请，查[普通按需预安排组呼的客户端建立](prearranged-client-establishment.md)。若旧对话只是空闲改参，没有这次组呼邀请，查[预建立会话的建立、空闲修改与释放](preestablished-session-lifecycle.md)。
