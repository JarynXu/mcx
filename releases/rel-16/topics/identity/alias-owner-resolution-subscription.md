# MCPTT 功能别名解析：订阅收到 200，就知道谁启用了别名吗？

不知道。以“东区值班”为例，拥有该别名的 MCPTT 服务器用 **200 OK** 答复的是订阅请求。要知道服务器报告了谁成功启用“东区值班”，应看它为这项订阅发送的 **NOTIFY** 里的用户列表。订阅者不因收到 200 就成为别名使用者；一个 200 也不能证明某份通知已经送达。[TS 24.379 V16.14.0，Release 16，Stage 3，§9A.2.2.3.7 步骤 4、§9A.2.2.3.8 步骤 1–4，印刷页 215–216](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=216)。

## 请求发给谁，订阅的又是谁？

服务器收到的 SIP SUBSCRIBE 中，**Request-URI 指向与所请求别名关联的控制 MCPTT 功能**，其中包含该功能的公共服务身份。具体要解析的别名 ID 则在 MCPTT 信息正文（`application/vnd.3gpp.mcptt-info+xml`）的 `mcptt-request-uri` 元素中。这两个名字相似，但不能把服务身份当成目标别名 ID，也不能把正文里的 ID 读成某个人的 MCPTT ID。

本程序还要求：`P-Asserted-Service` 中的业务标识（ICSI）指明 MCPTT，`Event` 指明 `presence` 事件，且过滤正文（`application/simple-filter+xml`）按**功能别名**限制通知内容。这里固定的是“东区值班”，问题是“哪些用户启用了它”；不是固定一个用户，问他启用了哪些别名。[§9A.2.2.3.7 接收条件 1–4、服务器步骤 1，页 215](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=216)。

<a id="alias-resolution-filter"></a>

## 同一个别名、同一个服务器，过滤器里为什么有时填用户 ID？

假设“东区值班”的别名 ID 是 F，甲的 MCPTT 用户 ID 是 U。两笔**服务器发给别名拥有方的初始 SUBSCRIBE** 可以有相同的 SIP Request-URI（与 F 关联的控制功能 PSI），也都在 MCPTT 信息正文的 `mcptt-request-uri` 写 F。只看这两处，分不清是在核实甲，还是在查整个值班名单。看 `application/simple-filter+xml` 正文内 `filter-set/filter/what/include` 的**文本值**：

| 业务问题 | 这份初始请求的识别依据 |
| --- | --- |
| 服务甲的服务器问“甲是否成功启用 F？” | MCPTT 信息正文另写 `mcptt-calling-user-id=U`。过滤器**按用户**，选择式为 `//pidf:presence/pidf:tuple[@id="U"]`，引号内放甲的 MCPTT 用户 ID，不是甲的客户端 ID。 |
| 服务器问“哪些用户成功启用 F？” | 过滤器**按别名**，选择式为 `//pidf:presence/pidf:tuple[@id="F"]`，引号内放 F。此处的标识选中别名，不预先指定名单上的某个人；这条构造步骤没有要求填前一行的 `mcptt-calling-user-id`。 |

**有效期也不能单独区分这两笔初始请求。** 核实用户 U 时，只查当前状态填 `Expires: 0`，同时要后续通知填 `4294967295`。解析 F 的名单时，第 4 项要求填 0；紧接的注允许在还要后续通知时填 4294967295。这里说的是发起端如何构造初始请求。拥有方只凭收到 0 并不能从有效期检查推断业务目的，更不能把它当作已有订阅的退订。[§9A.2.2.2.7 第 4–5 项，印 208](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=209)；[§9A.2.2.2.8 第 4 项及注，印 210](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=211)。

U 和 F 只是不同身份的占位符。两个过程都使用 `presence` 事件并声明接受 `application/pidf+xml`。如果两个过滤器都填 F，即使目标服务器和 MCPTT 正文中的别名都正确，第一笔也没有按其要求选中 U。在拥有方，单用户入口还要求过滤器的值与正文的 `mcptt-calling-user-id` 一致。两处不符，不能据此预判响应码或认定名单为空。[§9A.2.2.3.4 接收条件 5，印 213](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=214)；[§9A.2.2.2.7 初始请求第 1–8 项，印 208](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=209)；[§9A.2.2.2.8 第 1–7 项，印 210](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=211)；[§9A.3.2.2 两种构造，印 218–219](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=219)。

**怎么核对 XML？** 在这两种过滤正文里，根 `filter-set` 下的 `ns-bindings` 都有两条 `ns-binding`：`prefix="pidf"` 对应 `urn="urn:ietf:params:xml:ns:pidf"`，`prefix="mcpttPIFA10"` 对应 `urn="urn:3gpp:ns:mcpttPresInfoFA:1.0"`。选择式只出现 `pidf:`，并不省掉第二条绑定。另一个子元素 `filter` 自己有按 RFC 4661 构造的 `id`，没有 `uri` 或 `domain` 属性；它的 `what/include` 中，`include` 没有 `type` 属性。**选 U 还是 F，改的是选择式中和 `tuple/@id` 比较的值，不是 `filter/@id`。** 这里给的是过滤正文的字段，不是某份通知的内容或完整 SIP 报文。[§9A.3.2.2 按用户，印 218](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=219)；[按别名，印 218–219](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=220)。

**按用户限制过滤范围，并不把通知改成按用户格式的 PIDF。** 拥有方给核实甲的订阅和给解析 F 的订阅，都生成按别名组织的 PIDF；前者按 F 找甲的条目，后者取 F 下的用户清单。只看 MIME 类型或 F 这个值还不够，要查**同一订阅实际收到的 NOTIFY**。[§9A.2.2.3.5，印 214](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=215)；[§9A.2.2.3.8，印 216](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=217)。选中 F 和收到 SUBSCRIBE 的 200，只能说明请求选了什么、是否得到了成功答复，不能说明无人值班。核实甲本人时，看[服务甲的参与功能收到通知后怎样判定](mcptt-functional-alias-activation-servers.md#alias-user-filter)，不要把按 U 筛过的通知当作 F 的全员名单。用户终端自己[查询一个用户的别名状态](mcptt-functional-alias-client.md)是另一条客户端程序，§9A.2.1.3 的初始请求未列上述服务器过滤正文；不能因两者都订阅 presence 就把它加作终端必填项。[§9A.2.2.3.7–.8，印 215–216](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=216)；[§9A.2.1.3，印 200–201](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=202)。

## 服务器先查有效期，再查别名

1. **先看订阅期限。** 如果没有 `Expires`，或其值非零且小于 4294967295，服务器须返回 **423（间隔太短）**，在响应中把 `Min-Expires` 设为 4294967295，然后停止。即使目标别名并不存在，也走不到后面的别名检查。因此，423 不能用来判断别名是否存在。值为 **0** 不命中这个条件；仅凭这一步不能说它必然表示退订或一次性查询。
2. **没被前一步挡住，才检查目标别名。** 如果该别名在服务器上不存在，第 3 步规定拒绝订阅、给出 **403（禁止）** 并停止。固定版本在同一句中先写拒绝 SUBSCRIBE，却又把 403 写成对 PUBLISH 的答复。这是原文对请求名称的冲突；它没有要求订阅者再发一条 PUBLISH。一个存在但当前无人启用的别名，不等于别名不存在。
3. **未命中上述拒绝条件时，服务器为 SUBSCRIBE 生成 200 OK。** 这说明订阅请求走到了成功答复，不说明已有任何人启用了别名，也不说明服务器替谁执行了启用。[§9A.2.2.3.7 服务器步骤 2–4，页 215](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=216)。

## 通知里列出谁，通知发给谁？

服务器按别名保存记录：外层用别名 ID 找到“东区值班”，内层才是这个别名的 MCPTT 用户记录，每个用户条目在该列表中由 MCPTT ID 标识。[§9A.2.2.3.2，页 211](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=212)。订阅持续期间，所订别名的信息发生变化时，服务器须通知订阅者。§9A.2.2.3.7 末句留下的条款号是未写全的 `9.2.2.3.y`；可从反方向核对：§9A.2.2.3.8 步骤 4 明确说明，它发送的 NOTIFY 对应 §9A.2.2.3.7 创建的订阅。[§9A.2.2.3.7 末段，页 215](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=216)。

生成通知时，服务器选出 ID 与请求相同的别名条目，用它下面的用户列表生成按别名组织的 `application/pidf+xml` 正文，再为这项订阅发送带该正文的 NOTIFY。比如通知里列出甲和乙，表示服务器报告两人已成功启用“东区值班”；它不是获准使用该别名的全员名册，也不是给甲、乙各发一份的收件人清单。只有发送记录，还不能说订阅者已收到。[§9A.2.2.3.8 引言及步骤 1–4，页 216](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=217)。

如果问题是一次性查看当前使用情况，见[按别名或用户查询](active-functional-alias-lookup.md)；如果要判断服务器何时移除某人的别名关联，见[服务器自动停用别名关联](owner-alias-auto-deactivation.md)。这两项都不是收到本次订阅成功答复的含义。

若这笔解析是为了按需首接呼叫，下一步查[控制功能收到哪份通知才向值班人员发邀请](../calls/first-to-answer-controlling.md)。
