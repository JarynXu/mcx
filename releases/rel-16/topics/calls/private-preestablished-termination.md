# 普通私呼终接：被叫已有预建立会话，自动应答和人工应答分别由谁回 200？

控制功能（CF）向被叫侧参与功能（T-PF）发出一份新的初始 INVITE，邀请乙加入一对一私呼。乙的终端（UE）与 T-PF 之间早就建过 SIP 对话。**符合普通复用条件时，自动应答由 T-PF 直接回 CF；人工应答则由 T-PF 在乙的旧对话内发 re-INVITE，收到乙对它的 200 后，再对 CF 的 INVITE 回自己的 200。** 两份请求分属不同的信令腿。只看到 CF 侧的 200，不能登记为乙已经接听。

这里的“终接”是处理来话，不是释放。范围是同一 MC 系统归属网内、有话权控制、以被叫 MCPTT ID 指定一个人的在网私呼。下文的两条普通路径均指正常优先级、没有 Priv-Answer-Mode、没有置真的紧急或迫近危险标志。按需邀请只说明何时分流。替换除分流外，只说明正常优先级下，乙实收并按相应模式处理带 Replaces 的邀请时，怎样应答、怎样核实指定旧会话的释放。

## 先选应答模式，再看旧会话能不能用

T-PF 先处理收到的 CF INVITE。对 `session-type=private`，若 T-PF 尚未从**本次被叫**的 `application/poc-settings+xml` 收到 Answer-Mode Indication，第 3 项要求回 480，Warning 文本中的 MCPTT 码为 146，并停止。即使 INVITE 有应答模式头，也不能靠它跳过这一步。这是 T-PF 的本地答复，不是乙拒接。[TS 24.379 V16.14.0，Rel-16，Stage 3，§11.1.1.3.2 起首及项 3，印 376–377](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=377)

到达第 7、8 项时，按下表核对**收到的 INVITE** 和 **T-PF 已从乙收到的设置**。同一行三格是“或”，不是从左到右的优先级。

| 启动程序 | INVITE 有 Answer-Mode | INVITE 没有 Answer-Mode，且乙的设置为 | INVITE 有 Priv-Answer-Mode |
| --- | --- | --- | --- |
| 自动 | `Auto` | `auto-answer` | `Auto` |
| 人工 | `Manual` | `manual-answer` | `Manual` |

缺少 Answer-Mode 本身不是默认值。“没有 Answer-Mode”这一格只要求没有 **Answer-Mode**，不能另加“也没有 Priv-Answer-Mode”。若所收 INVITE 的字段与已收设置使两行的条件都成立，本条列出两组条件，但没有在这里给出二者的优先顺序；不能从表格补出唯一选择。[§11.1.1.3.2(7–8)，印 377](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=378)

**两种模式都检查同样的三件事。** 乙须有尚未关联 MCPTT 业务会话的预建立会话。本次 offer 中，MCPTT 语音流的媒体级描述要与既有会话对应描述相同，话权控制实体的媒体级描述也要相同。仅有旧对话、某个编解码器相同、或只匹配其中一段，都不够。这两处条款没有给多个合格候选规定排序。[§6.3.2.2.5.1，印 95–96](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)；[§6.3.2.2.6.1，印 98–99](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=99)

- **三项没有同时满足：** 自动走 §6.3.2.2.5.2，人工走 §6.3.2.2.6.2，由 T-PF 向乙另发按需 INVITE。不能单凭改走按需，就给这次 INVITE 加上 Replaces。[自动：项 3–11，印 96–97](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=97)；[人工：项 1–10，印 99](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=100)
- **三项满足：** 自动进入 §6.3.2.2.5.3，人工进入 §6.3.2.2.6.3。两处的第 1 项仍要检查替换条件：若入站 mcptt-info 中 `<mcptt-Params>` 的 `<emergency-ind>` 或 `<imminentperil-ind>` 为 `true`，**或只要入站有 Priv-Answer-Mode 头**，T-PF 就改用本模式的按需程序。发给乙的 INVITE 须带 `Replaces`，写入目标预建立会话的 Call-ID、to-tag、from-tag；SDP offer 须包含这个目标会话当前使用的媒体参数。随后跳过原预建立程序的余步。正常优先级并不能排除这条分支：还得看有没有该头。[§6.3.2.2.5.3(1)，印 97–98](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=98)；[§6.3.2.2.6.3(1)，印 100–101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=101)

<a id="replacement-resource-share"></a>
## 替换已有对话时，共享规则从哪条承载取？

这里只看同一 MC 系统归属网内、按一个被叫 MCPTT ID 发起、有话权控制的普通在网私呼。T-PF **实际收到 CF 的初始 INVITE**，已选自动或人工应答，且同一个目标预建立会话**未关联业务，语音和话权控制两段 SDP 都匹配**。来话是正常优先级，emergency-ind 和 imminentperil-ind 均未置 true，但带了 `Priv-Answer-Mode`。这时进入替换分支：T-PF 向被叫另发按需 INVITE，`Replaces` 标识目标旧对话，新 SDP offer 带该旧会话当前使用的媒体参数。自动和人工在这一步都不再走原预建立复用的余步。若找不到符合三个条件的旧会话，改走普通按需不等于替换，不能仅因支持共享就给它加上下面这套规则。[自动 §6.3.2.2.5.1、§6.3.2.2.5.3 第 1 项，印 95–98 / PDF 96–99](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=99)；[人工 §6.3.2.2.6.1、§6.3.2.2.6.3 第 1 项，印 98–101 / PDF 99–102](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=101)。

**若 SIP 核心支持资源共享**，这份出向替换 INVITE 还须带 `Resource-Share`，值为 `media-sharing`，`origin=session-receiver`，并带 `timestamp` 和 `rules`。不支持共享不取消 `Replaces`，这里只是不触发该头的要求；尚不知道核心是否支持时，不能当作不支持，也不能断言缺头错误。§8.1A 区分经 SIP 核心共享和经 Rx 直接向 PCC 请求共享。PF 可以从**实际收到、与这次判断相关的第三方 REGISTER** 的 `message/sip` 内层请求看到 `Resource-Share: supported`，以判断 SIP 核心支持。仅知 UE 支持或有直接 PCC/Rx 共享，不足以满足 SIP 核心这个条件；替换条款没有要求为了发这次 INVITE 重新注册或重复旧会话建立时的绑定检查。[自动 §6.3.2.2.5.3(1)(c)，印 98 / PDF 99](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=99)；[人工 §6.3.2.2.6.3(1)(a)(iii)，印 100 / PDF 101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=101)；[§8.1A，印 161 / PDF 162](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=162)。

**按这份出向 INVITE 的 SDP offer 排规则。** 一个媒体流一条规则，按对应 `m=` 行的顺序。某一流的 `new-sharing-key` 虽然带“new”，仍是 **Replaces 指向的旧会话中，对应媒体承载建立时用的同一个共享键**；`directionality` 也指该旧承载的方向，不从本请求的发送方向来猜。比如新 offer 先列语音再列话权控制，则先写语音旧承载的键和方向，再写话权旧承载的键和方向。不拿入向 CF 的 offer、另一条预建立会话或别的应答的行序来配。

如果实际在查 **PF 对初次建立预建立会话的 INVITE 所发的 200**，才读[初建时的 Resource-Share 应答](preestablished-session-lifecycle.md)：同样在 SIP 核心支持条件下，这一腿的 `origin=session-initiator`，按这份 200 的 SDP **应答**顺序读，不能照搬到本次替换的 `session-receiver`。替换的头和 `Replaces` 只说明 T-PF 发出了哪些请求和规则，不证明 UE 实收、旧 SIP 对话释放、网络已复用承载或新媒体已通。[自动 (1)(c)(iv)，印 98 / PDF 99](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=99)；[人工 (1)(a)(iii)(D)，印 100 / PDF 101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=101)；[初建 §8.2.2(9d)，印 163 / PDF 164](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=164)。

## 普通自动应答：CF 的 200 来自哪里？

T-PF 为 **CF 本次发来的 INVITE** 生成 200 OK，写入 `P-Answer-State: Unconfirmed`。它不需要一份乙此刻发来的 SIP 响应来凑这份 200：

- SDP answer 依据**乙当初建预建立会话时已协商的 SDP** 和 **CF 本次 INVITE 的 SDP offer**。
- `P-Asserted-Identity`（PAI）取自**乙当初为建那条会话而发送的 INVITE**，不是乙这次应答私呼时提供的身份。

T-PF **先把 200 发给 CF，再按 TS 24.380 §9 与媒体面交互**。§6.3.2.2.5.3(2–7) 没有列出向乙发本次 SIP 请求、或等待乙的 SIP 回答的步骤。这个 200 不能证明乙收到了 Connect、协议栈已回答或用户按了接听。[§6.3.2.2.5.3(2–7)，印 98](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=99)

## 普通人工应答：怎样配对 180 和两份 200？

T-PF 在**与乙既有的预建立 SIP 对话内**生成 re-INVITE，复制 CF 本次 INVITE 的 `application/vnd.3gpp.mcptt-info+xml` 正文内容，以 CF 的 offer 为依据构造 SDP offer，再发给乙。注 1 说明：该 re-INVITE 不能带 Answer-Mode，在这条既有对话里隐含 Manual。不要因此在抓包中寻找一条新对话的 INVITE，或补写一个 `Answer-Mode: Manual`。[§6.3.2.2.6.3(2–5)、注 1，印 101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=102)

| 在乙这一腿，T-PF 实际收到什么 | T-PF 如何答复 CF 那一腿的初始 INVITE |
| --- | --- |
| 乙针对这份 re-INVITE 的 180 Ringing | T-PF 另造 180，带上所收 180 的 PAI，向 CF 发送。这不是最终 200，也不是用户同意的证据。 |
| 乙针对这份 re-INVITE 的 200 OK | 若所收 SDP answer 更改了编解码器或媒体格式，T-PF 须先用新协商的编解码器和媒体参数更新媒体面。T-PF 生成自己的 200，复制所收 200 的 PAI，并以所收 SDP answer 为依据构造自己响应中的 SDP answer；再与媒体面交互，随后把 200 发给 CF。注 4 说明此处发送 MCPC Connect 是为了把 MCPTT 会话身份交给乙。 |

这两行各以实收相应响应为条件，不能把观察到 180 当成处理 200 的前提。注 2 把 180 对应到私呼，注 3 说组呼可能收到 183；不能把 183 填成普通私呼的默认步骤。自动路径是**先发 CF 200** 再进入媒体面接口；人工路径是**先收到乙的 200**，按本分支的顺序交互后才发 CF 200。只有 CF 一侧的 180 或 200，不足以还原乙实际收发的报文；Connect 的发送也不等于乙已收到，更不能证明用户操作、已获话权或 RTP 已通。[§6.3.2.2.6.3，对 180、183、200 的处理及注 2–4，印 101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=102)

**从终端条款能不能反推 T-PF 一定发 re-INVITE？** §11.1.1.2.2.2 从被叫终端一侧写，新的正常优先级私呼收到 re-INVITE 而非 INVITE，并引用 §11.1.1.2.1.2。被引用的第 10 项明列收到 `Answer-Mode: Manual` 及相应本地设置或允许条件，或收到 `Priv-Answer-Mode: Manual`；T-PF 的人工预建立程序注 1 却说明对话内 re-INVITE 不带 Answer-Mode、隐含 Manual。这些条文的视角与条件不同。不能把终端描述改作 T-PF 自动分支的发包要求，覆盖上面的替换条件，或据此推定终端如何解析一份没有该头的请求。[§11.1.1.2.2.2，印 366](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=367)；[§11.1.1.2.1.2(10)，印 358](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=359)；[§6.3.2.2.6.3 注 1，印 101](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=102)

## 替换邀请到了乙：新 200 答哪份请求，谁释放旧会话？

这里从乙实收的新初始 INVITE 讲起：来话为正常优先级，两项紧急指示均未置真，T-PF 因 Priv-Answer-Mode 走了前述替换分支。乙收到的 `Replaces` 标识目标旧预建立会话，且乙已进入适用的私呼应答程序。单看 T-PF 一侧的头或出站请求，不能认定乙已收件，也不能用来消除前述正常优先级终端条款与替换条款在请求方法上的差异。

**自动应答时，是乙释放 Replaces 指定的那条旧会话。** 乙在**新 INVITE** 的 200 OK 中写入 SDP answer，其中须包含**指定旧会话所用的参数**。第 8 至 10 项依次要求乙向 MCPTT 服务器发送这个 200，释放指定的旧预建立会话，再按 TS 24.380 §6.2 与媒体面交互。这里的 200 不是对旧对话的释放应答。[§6.2.3.1.1(6)、(8–10)，印 58–59](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=59)

**人工应答有两个不同的结果。** 乙发送最终 200 时，适用同一套应答和释放步骤。若用户明确拒绝，乙向服务器回 480，Warning 文本中的 MCPTT 码为 110，并停止本次人工应答程序。与新 INVITE 配对的这份 480 表示乙以用户拒绝为由答复了这份邀请；它不要求成功路径中的释放，也不保证旧会话此后一直保留。仅仅没看到最终响应，不能记为替换失败。[§6.2.3.2.1，印 59](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=60)

核查一次实际替换，要分开看新邀请、旧对话和媒体。Replaces 与 offer 只说明 T-PF 想替换谁、提出了哪些参数。查乙是否应答，要在乙这一腿把最终响应配到新 INVITE；只有 CF 腿的 200，不能证明乙收到了邀请。即使看到乙对新 INVITE 发了 200，也不能用它证明乙已经结束旧对话或清除了旧媒体。

若另有证据表明乙在主动释放按 §8.2.1 建立的旧预建立会话，查**旧对话**：乙在这条 SIP 对话内向参与功能发 BYE，Request-URI 为标识该旧会话的 URI。乙实收**这份 BYE 的 200** 时，须与媒体面交互。按 Replaces 中的 Call-ID 和两个 tag 核对旧对话，再把响应配给旧 BYE；没看到这些记录，不等于旧会话仍在。要判断旧媒体已停或新 RTP 已通，还要查相应会话、流向的媒体记录。第 9 项只要求释放，并未直接引用这套主动释放程序，也没有规定旧 BYE 与新 INVITE 的 ACK 谁先谁后。本页不据此补出目标匹配算法、其他失败响应或回滚规则。[§8.4.1.1(1–4)，印 165](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=166)；[§6.2.3.1.1(9)，印 58](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=59)

只有主叫侧的 REFER 和响应时，查[主叫请求与业务 INVITE 的区别](private-preestablished-origination.md)。若 T-PF 在选择前已拒绝或转入普通按需私呼，查[服务器检查和按需邀请](private-server-admission-routing.md)。若已有 Connect 或 Accepted，要确认乙是否收到，查[媒体控制消息的收件证据](../media/preestablished-connect-outcome.md)。
