# 普通私呼下游没有主叫别名：O-PF 何时保留，何时省略？

Rel-16、Stage 3。以主系统普通在网、带话权的按需私呼为例。甲用乙的 MCPTT ID 发起一对一私呼，另外想带**甲自己的功能别名**。先查甲发给起始参与功能（O-PF）的 INVITE，再查 O-PF 另发给私呼控制功能（CF）的 INVITE。

## 被叫 ID、主叫 ID 和主叫别名不在同一位置

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

排查时对齐两段实际 INVITE、O-PF 确定的主叫 MCPTT ID、收到的别名和当时这对身份的状态。O-PF 发出带别名的 INVITE 不证明 CF 实收，别名省略也不证明被叫拒接。这里不判被叫客户端的显示、人是否应答或媒体是否到达，不适用于预建立 REFER、应急或以别名确定被叫的流程。

依据：[§6.3.2.1.3(7/8)，印 85](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=86)；[§11.1.1.3.1.1(19a) 及注 4，印 369](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=370)；[§9A.2.2.2.7，印 208–209](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=209)。若告警是普通私呼本身的准入或拒绝，见[普通私呼各腿的准入](private-server-admission-routing.md)；按候选被叫 ID 发首接的许可另见[首接发起侧准入](first-to-answer-originating-admission.md)。
