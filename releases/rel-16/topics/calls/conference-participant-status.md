# 这场 MCPTT 组呼有哪些人参加？查一次和持续观察有何不同？

甲是 G 组成员，想知道乙在不在**眼前这一场通话**。查组成员名单只能说明乙属不属于 G；查归属名单也不能断定乙已经入会。对于自己正在参加、且发起时不是广播组呼的在网会话，甲的 MCPTT 客户端可以订阅会议事件，读取这场会话的参与者状态。不必先断线重入，也不是每个参与者都必须订阅。

## 甲只想看现在，还要收后续变化吗？

两种目的都用 SIP SUBSCRIBE，**另开订阅对话**。请求目标（Request-URI）填这场组呼的 MCPTT **会话标识**；正文的 `mcptt-request-uri` 填 MCPTT **组 ID**。组 ID 说明是哪个组，不能拿来代替这场会话的目标地址。甲声明可接收会议信息（Accept：`application/conference-info+xml`）。

- 只取当前状态：在这次新订阅请求中设 `Expires: 0`。零表示这次只取一回，不是“不需要当前结果”。
- 既取当前状态，也希望之后有人进出时收到通知：设 `Expires: 4294967295`。这是请求的期限值，不是永久有效或每次变化都已送达的证明。客户端需要结束订阅时按 RFC 6665 处理，不是退出这场通话。

依据：[TS 24.379 V16.14.0（Release 16，Stage 3）§§10.1.3.1–2，印刷页 301–302](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=302)。

<a id="establishment-contact"></a>

## 第一次查名单，用建呼 INVITE 的 Contact，还是用 200 的 Contact？

看**本端是发起人还是受邀人，以及哪条消息是服务器发给本端的**。设甲发起、乙受邀，双方正在参加同一系统内 G 组的普通预安排组呼。两端这次建呼各自都走按需信令；乙没有复用预建立会话。组 ID 都是 G，甲和乙发起会议订阅时却各自使用本端收到的会话 URI：

| 要找哪一端的地址 | 从本场建呼记录找哪一条 Contact | 什么时候可以订阅 |
| --- | --- | --- |
| 主叫甲 | 对甲的初始 INVITE，控制功能（CF）发给发起侧参与功能（O-PF）的 200，Contact 给出 CF 托管的会话 URI。O-PF 收到后另向甲发 200；**甲收到的这个 200 的 Contact** 给出与 CF 身份相映射、由 O-PF 托管的会话 URI。 | 甲收到对建呼 INVITE 的 2xx 后可以订阅。这里核对的是最终成功响应，不要求它是抓包中首次出现会话身份的报文。 |
| 受邀乙 | CF 单独邀请乙时，在发给终接侧参与功能（T-PF）的 INVITE Contact 给出 CF 会话 URI。T-PF 给乙另发初始 INVITE；**乙收到的这条 INVITE 的 Contact** 给出与入向 Contact 相映射、由 T-PF 托管的会话 URI。按需的自动、手动应答都使用这条邀请构造规则。 | 乙对该邀请**发出** 200 时可以订阅。这个 200 是乙发的，不是向乙交付会话 URI 的那条消息。 |

发起腿见 [§6.3.3.2.3.2 第 5 项，印 120](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=121)、[§10.1.1.3.1.1 的 2xx 处理，印 232](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=233)；受邀腿见 [§10.1.1.4.1.1，印 240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=241)、[§6.3.3.1.2，印 106](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=107)、[§6.3.2.2.3 第 4 d 项，印 94](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=95)（由[自动，印 96](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=97)或[手动，印 99](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=100)分支调用）。两端何时可订阅分别见 [§10.1.1.2.1.1，印 221](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=222) 和 [§10.1.1.2.1.2 第 9 项，印 223](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=224)。

核实一笔查询，先按呼叫、方法和方向把两条腿配上，再看终端实际发起的**新订阅对话**：SIP Request-URI 填本端会话 URI，MCPTT 信息正文的 `mcptt-request-uri` 填 G。PF 查到会话后才把映射的会话身份用作它向 CF 发出的 SUBSCRIBE 的目标。不是要求甲、乙抄 CF 侧的 URI，也不要求比较三个字符串来证明映射。**SUBSCRIBE 自己的 200 更晚才到，不能用来解释它的初始请求是如何寻址的。** [§4.5，印 38–39](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=39)；[§10.1.3.1–.3，印 301–302](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=302)。

§4.5 说客户端**可以**缓存会话身份至不再需要。收到建呼 Contact 能说明本端得到过什么，不能证明软件何时写入、重启后还在，或 PF 至今仍能解析。符合本页入口的 SUBSCRIBE 若在 PF 返回 404 / Warning 文本 137，可确认的是 **PF 在这次查询时未能解析请求里的会话身份**。要区分用错旧会话、终端留存问题和 PF 侧状态，需要这次出向请求与对应 PF 的记录；不能只凭 404 倒推终端漏存，也不能靠 G 重造会话 URI。[§4.5，印 39](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=40)；[§10.1.3.3，印 302](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=303)。

## 同样是订阅失败，在哪一步被拒？

服务甲的**参与功能（PF）**收到符合本条入口的请求，即带 MCPTT 服务标识、接受会议信息且正文含组 ID，会先用 Request-URI 查找现有会话。能找到时，PF 按映射后的会话标识转发，并带上甲的 MCPTT 用户 ID。**控制功能（CF）**处理普通参与者的请求时，核对的包括会话的组 ID、参与者的 MCPTT ID、MCPTT 服务标识和可接收的会议信息类型。已在会话里，也不代表获准查看会议信息。

| 接收方遇到的情况 | 对这次 SUBSCRIBE 的响应 | 说明 |
| --- | --- | --- |
| PF 无法把请求目标解析为现有会话 | SIP 404；警告文本编号 137 | PF 在此停止。该处找不到这场通话，不等于 G 组已删除。 |
| CF 收到符合上述条件的非广播订阅，组文档的 `on-network-allow-conference-state` 不允许甲订阅 | SIP 403；警告文本编号 138 | CF 在此停止。拒绝的是订阅，不是把甲踢出通话。 |
| CF 在一场**发起时就是广播组呼**的通话中收到这种请求 | SIP 480；警告文本编号 105 | 这是控制端收到该请求时的专门分支，不表示普通客户端可以在广播组呼中发起订阅。 |

表中 137、138、105 是 Warning **文本中的业务编号**，不是 SIP 响应码。这三种情况也不是一条请求依次收到的三个响应。依据：[§10.1.3.3，印刷页 302–303](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=303)；[§10.1.3.4.1，印刷页 303](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=304)。

## 从 PF 两侧对照：这次 SUBSCRIBE 和 NOTIFY 各把谁写进地址？

设甲正在参加同一 MC 系统内的一场普通预安排或聊天组呼，想查这场通话的参加状态。甲发出 SUBSCRIBE 时，SIP 的 Request-URI 是已有组呼的会话标识。§10.1.3.2 规定订阅请求使用什么目标；普通按需预安排组呼两端从哪里收到该身份，见[建呼 Contact 对照](#establishment-contact)。

PF 收到甲的 SUBSCRIBE 时，先认清入口：`P-Asserted-Service` 携带 MCPTT ICSI，`Accept` 含 `application/conference-info+xml`，`application/vnd.3gpp.mcptt-info+xml` 正文的 `<mcptt-request-uri>` 是组 ID。PF 要解析的是 **SIP 的 Request-URI**，不是这个 XML 元素。下面按请求种类对照两侧报文，不按两个 200 出现的先后判断：

| PF 实际收到什么 | 在 PF 发出的对应报文中查什么 |
| --- | --- |
| 客户端侧：上述 SUBSCRIBE，且请求目标已解析到现有会话 | PF 向 CF 侧发出新的 SUBSCRIBE。Request-URI 填与收到的会话标识相映射的会话标识；MCPTT 信息正文加入 `<mcptt-calling-user-id>`，值为甲的 MCPTT ID；`Record-Route` 加入标识 PF 自己地址的 URI。 |
| CF 侧：对该 SUBSCRIBE 的响应 | PF 复制收到的响应内容并向客户端侧转发。若是 **SUBSCRIBE 的 200**，PF 在**发出响应的 Contact** 中放入与收到的 Contact 内会话标识相映射的 MCPTT 会话标识。 |
| CF 侧：由该 SUBSCRIBE 建立的对话内、发往其所服务的甲客户端的 NOTIFY | PF 发给甲的 NOTIFY 以**甲的公共服务标识（PSI）**为 Request-URI，复制收到的通知内容。这个 SIP 地址标明要通知谁，不是订阅时的会话地址，也不是从参与者名单里选出的地址。 |
| 客户端侧：对该 NOTIFY 的响应 | PF 复制收到的响应内容并向 CF 侧转发。若是 **NOTIFY 的 200**，PF 根据**收到的 Contact** 中的 MCPTT 会话标识构造会话标识，放入发出的响应。此处条款没有指明发出时使用哪个字段，不能套用 SUBSCRIBE 的 200 响应规则。 |

两个 200 回答不同的请求，都不能替代甲端收到的会议状态正文。比对时要找同一次订阅中相应的方法和方向；条款给出映射或构造关系，不能靠两侧地址字符串是否相同来判定。依据：[§10.1.3.2，印刷页 301](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=302)、[§10.1.3.3，印刷页 302–303](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=303)。

## 哪条记录才告诉甲，乙在这场通话里的状态？

通过检查后，CF 按会议事件程序处理请求，缓存订阅信息，发送会议状态通知。**对 SUBSCRIBE 的 200 表明订阅请求成功，不是参与者名单。** 要判断乙的状态，应看甲端是否收到了本订阅对话的 SIP NOTIFY，以及相应的会议信息是否报告了乙的状态。PF 向所服务的客户端转送 NOTIFY；甲端须处理，**可以**显示。若只有 CF 的发送记录，不能说甲已收到；即便甲端收到了，也不能由此认定甲看过、听过语音或拿到了话权。

收到按前述规定处理的订阅是一个通知触发点。对于**预安排组呼或聊天组呼（chat）**，CF 收到一位参与者的 BYE，或有新参与者被加入，也是触发点。通知送给**已订阅的参与者**，不是 G 组全体成员，也不是这场通话里每个人。不要把一次读取当成持续订阅；只拿到甲先前的一次结果，也不能断言乙后来仍在通话中。见 [§10.1.3.4.2，印刷页 304](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=305)及 §10.1.3.2 末段（印刷页 302）。

## 通知的收件人是甲，正文里哪一项才是乙？

CF 向订阅者甲生成会议通知时，SIP 头的 `P-Asserted-Identity` 是 **CF 自己的 PSI**，`Event` 是 `conference`，`P-Preferred-Service` 携带 MCPTT 的 ICSI（`urn:urn-7:3gpp-service.ims.icsi.mcptt`）。这条 **NOTIFY 的 Expires 默认值是 3600 秒**；甲在 SUBSCRIBE 中请求只读一次或持续接收，见上文的 0 和 4294967295。不能拿 NOTIFY 的默认值算订阅实际有效多久。

| 要找什么 | 在 CF 生成的通知中看哪里 |
| --- | --- |
| 哪个组？通知发给哪个用户？ | 在 `application/vnd.3gpp.mcptt-info+xml` 正文中，`<mcptt-calling-group-id>` 是 G 的 MCPTT 组 ID；目标为用户时，`<mcptt-request-uri>` 是收件人甲的 MCPTT ID。同名 XML 元素在甲发起的 SUBSCRIBE 里填的却是组 ID。 |
| 哪个组的会议信息？里面的用户是谁？ | 在 `application/conference-info+xml` 正文中，`<conference-info>` 的 `entity` 是 G 的组 ID。每个会话参与者各有一个 `<user>`，非控制 MCPTT 功能（NCF）除外。对发起、加入或重新加入的客户端，`<user>` 的 `entity` 是发出相应 SIP INVITE 的用户的 MCPTT ID；在预安排或聊天组呼中，对受邀客户端填被邀请用户的 MCPTT ID。 |
| 怎样判断通知报告了乙的什么状态？ | 找 `entity` 为乙的 MCPTT ID 的 `<user>`。该项内有且仅有一个 `<endpoint>`，带 `entity` 属性和 `<status>` 元素。读这项的 `<status>`，才知道通知为乙报告了什么会话状态。此处没有规定 `<endpoint>` 的 `entity` 必须取哪个值。 |

通知列出的是这场会话报告的参与者，不能把列出的用户或 endpoint 数量当作注册设备数、在线人数或实际收听人数。甲的收件人 ID 也不是乙的状态证据。依据：[§6.3.3.4，印刷页 124](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=125)；向已订阅参与者发送见 [§10.1.3.4.2，印刷页 304](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=305)。

若问题是断线后如何**重新加入**，先确认原来是什么组呼。普通按需聊天组中，用户回到覆盖后主动请求加入，读[聊天组的按组加入与原场判断](chat-establish-join.md)；普通按需预安排组才读[预安排组重入与晚入](rejoin-late-entry.md)。关心谁属于 G、谁已归属，读[组名单查询](../groups/group-list-query.md)或[组动态数据](../groups/group-dynamic-data.md)。这里不展开临时组中控制与非控制功能之间的互订、两个 MIME 正文的完整语法、RFC 订阅生命周期或话权流程。

临时组呼还在进行，退订或计时器到期后要判断哪条服务器间订阅会结束，查[最后一笔 conference 事件订阅怎样收尾](conference-event-subscription-termination.md)。

临时组涉及 CF 与组成组 NCF 互发会议通知时，查[临时组呼的 NOTIFY 组标识和名单来源](temporary-group-conference-notify.md)。普通用户订阅和服务器互发通知要分开看。
