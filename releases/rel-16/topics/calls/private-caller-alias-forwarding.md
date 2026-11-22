# 普通私呼下游没有主叫别名：O-PF 何时保留，何时省略？

Rel-16、Stage 3。以归属网内普通在网、带话权的一对一私呼为例。甲用乙的 MCPTT ID 发起一对一私呼，另外想带**甲自己的功能别名**。按需发起时，甲发给起始参与功能（O-PF）的是 INVITE；使用预建立会话时，甲发的是 REFER，别名所在的位置也不同。两种情况都要核对 O-PF 另发给私呼控制功能（CF）的 INVITE。

## 按需发起：被叫 ID、主叫 ID 和主叫别名不在同一位置

甲把乙的 MCPTT ID 写到资源列表。该初始 INVITE 的 MCPTT-info 正文使用 `session-type=private`。甲需要带自己使用的已启用别名时，须把同一正文的 `functional-alias-URI` 设为实际使用的别名 URI。该字段与主叫业务身份一起使用，不是被叫身份，也不是用功能别名寻找被叫的首接呼叫。

O-PF 从**入站请求**的 `P-Asserted-Identity` 取公共用户身份，按业务授权所建绑定认出甲的 MCPTT ID。若此检查时找不到绑定，或绑定已到期，O-PF 对甲的 INVITE 返回 404，带 Warning 文本 141，并停止其余步骤。这个早期拒绝不能当作别名被省略。

流程走到构造下一请求时，O-PF 用为甲选定的私呼 CF 公共业务身份（PSI）填下一 INVITE 的 SIP Request-URI，用已确定的甲的 MCPTT ID 填正文的 `mcptt-calling-user-id`。被叫乙仍由资源列表标识。公共用户身份、服务器的 PSI、主叫业务 ID 和主叫别名各有用途，不能互换。

依据：[TS 24.379 V16.14.0 §11.1.1.2.1.1(9)、(14c)，印 353–354](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=354)；[§11.1.1.3.1.1(3/4/6/15–17)，印 366、368](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=367)；[附录 F.1.3(k)，印 551](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=552)。

## 两段发布都回了 200，为什么第二笔 INVITE 还能不带别名？

先确认 O-PF **实际收到的这笔 INVITE** 在 MCPTT-info 正文含 `functional-alias-URI`。第 (19a) 项才要求核对 O-PF 在处理这笔请求时、**对主叫甲和这个别名**所记的状态。

- 该别名对甲是 `activated`：第二笔 INVITE 写入收到的原值。
- 不是 `activated`：第二笔不带该元素。若还只是 `activating`，也不带。这一步没有规定因此拒绝整通私呼，其他私呼准入和响应仍须另查。
- 入站正文没带该字段：这一步没有要求 O-PF 补上一个别名。只见出站缺字段，分不清甲没带还是 O-PF 按状态省略；更不能从没抓到某段报文断言它没有到达。

通用 INVITE 生成过程会复制已有的 MCPTT-info 正文。具体的 (19a) 决定要不要保留这个元素，并不要求删掉整个正文或换掉甲、乙的业务身份。O-PF 学习别名状态是另一条过程。对甲手动首次启用的场景，须核对 O-PF 实收的相符按别名 NOTIFY 和同一主叫、同一别名的本地记录；两段 PUBLISH 的 200 不能代替状态更新。详见[参与功能怎样登记 activated](../identity/mcptt-functional-alias-activation-servers.md)。第 (19a) 项没有规定因收到这笔呼叫就现发 SUBSCRIBE 或等待通知。

排查时对齐两段实际 INVITE、O-PF 确定的主叫 MCPTT ID、收到的别名和当时这对身份的状态。O-PF 发出带别名的 INVITE 不证明 CF 实收，别名省略也不证明被叫拒接。这里不判被叫客户端的显示、人是否应答或媒体是否到达，以上是按需初始 INVITE 的规则，不用于应急或以别名寻找被叫。

依据：[§6.3.2.1.3(7/8)，印 85](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=86)；[§11.1.1.3.1.1(19a) 及注 4，印 369](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=370)；[§9A.2.2.2.7，印 208–209](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=209)。若告警是普通私呼本身的准入或拒绝，见[普通私呼各腿的准入](private-server-admission-routing.md)；按候选被叫 ID 发首接的许可另见[首接发起侧准入](first-to-answer-originating-admission.md)。

## 预建立会话：REFER 顶层没有别名，应该去哪里找？

甲已有预建立会话，要用自己的值班别名呼叫乙。乙仍按本人的 MCPTT ID 寻址。O-PF 收到甲的 REFER 后，先沿 `Refer-To` 的 `cid:` 找到 Content-ID 对应的资源列表正文。普通一对一私呼只有**一个** `entry`：其 `uri` 指向乙。沿这个 SIP URI 的 headers 部分，找到名为 `body` 的参数，里面的 MCPTT 信息体才是要查的地方。它的 `session-type` 是 `private`；甲需要携带自己已启用的别名时，就把 `functional-alias-URI` 设为实际使用的别名 URI。不要去 REFER 的 Request-URI 找它，也不要给甲的别名另加一个被叫条目。只查顶层没看到，不等于甲没带。[普通私呼客户端 §11.1.1.2.2.1(1、7、8c ii)，印 363](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=364)；[O-PF 的入口及单条目分类 §11.1.1.3.1.2，印 370–371](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=371)。

**拿到内层正文后，再看 O-PF 发出的 INVITE。** 通用的 REFER 转 INVITE 程序要求把该参数内的 MCPTT 信息体复制到新 INVITE；若拷入的别名不是 active，须删去该元素。新正文另写入甲的 `mcptt-calling-user-id`。私呼专条又明确了查谁的状态：O-PF 从实收 REFER 的 `P-Asserted-Identity` 确定甲的 MCPTT ID；若入站含该别名，且 O-PF 此时对**甲和这个别名**记为 `activated`，出向正文必须保留原值，否则不带该元素。仍是 `activating` 不够。若入站就没有，专条不要求替甲补一个。原文在客户端构造项写作 `application/vnd.3gpp.mcptt-info`，复制及别名检查项写作带 `+xml` 的名称；这不是要求发送两份别名正文。[§6.3.2.1.4(11、11A、12)，印 86](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=87)；[§11.1.1.3.1.2(2–3)，印 370–371](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=371)；[同条 (19a)，印 373–374](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=374)。

**REFER 的 200 不能回答别名是否传出。** O-PF 对 REFER 回 200 之后才另建业务 INVITE，目标是服务甲的私呼 CF 的公共业务身份。要区分甲没带和 O-PF 省略，须比对 O-PF 实收 REFER 的内层正文、处理时甲的别名状态，以及同一次发起产生的出向 INVITE 正文。在 O-PF 实际发出的这笔 INVITE 中看到原值，可以确认 O-PF 带上了它；要证明 CF 收到或乙的屏幕显示了什么，分别查 CF 入站和乙的终端。若关心 REFER、业务 INVITE 两笔事务的成败，见[预建立私呼发起](private-preestablished-origination.md)。[§11.1.1.3.1.2(14–17、19a、20)，印 373–374](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=374)。
