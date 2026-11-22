# 移除预配置重组：各段何时回 200，终端通知为什么不带名单？

操作员要求移除临时重组 T。发端参与功能（O-PF）把 SIP MESSAGE 送给控制 T 的 MCPTT 功能（CF），下游还没回音，CF 却已经回了 200。**这个顺序符合规范：CF 先答复收到的移除请求，再按重组类型发通知。** 这个 200 不是下游签收，更不能证明所有终端已经解除归属。如果是 CF 自己决定移除 T，则没有这笔上游请求需要它答复。〔TS 24.379 V16.14.0，Release 16，Stage 3：[§16.2.3.2 第 1–4 项，印 502](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=503)；[§16.2.3.2 第 4–5 项、§16.2.3.3 第 1 项，印 503](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=504)；[§16.2.3.3 第 1–2 项，印 504](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=505)〕

T 是本次重组的临时组标识，写在 `mcptt-regroup-uri`。提供配置的预配置组 P 是另一个标识，字段为 `preconfigured-group`。移除的是 T，不是 P，也不是 T 的组成组。〔[§16.1，印 494](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=495)〕

## 谁发了 403，谁发了 200？

发端参与功能先按发起人的 MCPTT ID 查用户配置档。如果 `allow-regroup` 没有设为 true，它回 **403，Warning 文本码 161**，不再转给 CF。请求送达 CF 后，若 CF 判定待移除的 T 不存在，它回 **403，Warning 文本码 163** 并停止；这时应核对 T，而非给用户重新授权。CF 若因缺少资源无法处理或存在拥塞风险，可以回 **500**，可带 Retry-After；走拒绝分支就不再下发。〔[§16.2.2.3，印 498](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=499)；[表 4.4.2-2 的 161、163，印 38](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=39)；[§16.2.3.2 第 1–4 项，印 502](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=503)〕

正常分支中，CF 对入站移除 MESSAGE 回 200，随后分发。O-PF 收到它所发 MESSAGE 的 2xx，另向发起客户端回 200。所以客户端看到的 200 和 CF 发出的 200 属于两笔事务。判断某个终端是否处理移除，要查发向它的通知及其响应，见[收到通知的客户端](preconfigured-regroup-notification.md)。若查的是创建失败后的补偿，见[创建时哪些 NCF 才会收到补偿](preconfigured-group-regroup-creation.md)；不要把创建时等齐响应的规则套到正常移除。〔[§16.2.2.3 的响应处理，印 499](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=500)；[§16.2.3.2 第 1–4 项，印 502](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=503)〕

## 移除通知的下一跳：按组成组，还是按归属用户？

两种触发方式都先看 T 的类型。**Request-URI 填下一跳服务器的公共服务标识（PSI）**，不是 T 或某个用户的 MCPTT ID。用户重组的条款明确复用这里的两套控制功能程序。〔[§16.2.3.2 第 1–4 项，印 502](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=503)；[§16.2.3.2 第 4–5 项、§16.2.3.3 第 1 项，印 503](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=504)；[§16.2.3.3 第 1–2 项，印 504](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=505)；[§16.3.3.2–3，印 511](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=512)〕

| T 怎样组成 | CF 如何分发移除 MESSAGE |
| --- | --- |
| **组重组**：组成组是 G1、G2 | 对每个组成组找服务该组的非控制功能（NCF），把这条 MESSAGE 发往这个 NCF 的 PSI。步骤按组成组遍历，不是先去重再对每个 NCF 发一次，也不是由 CF 按终端名单逐个通知。 |
| **用户重组**：甲、乙、丙都属于 T | 先取**属于 T 且已归属 T** 的用户，再按服务他们的终接参与功能（T-PF）分名单。若甲归属 T 且由 X 服务，乙归属 T 且由 Y 服务，丙尚未归属：发往 X 的 PSI 的 MESSAGE 在 `users-for-regroup` 中只列甲；发往 Y 的只列乙。丙不因名册上有他而进入任一名单。 |

## 怎样区分受理请求和 CF 自行移除？

**有入站请求：**CF 构造下游 MESSAGE 时复制入站的 MCPTT 业务正文（`mcptt-info+xml`）、重组正文（`mcptt-regroup+xml`）和 P-Asserted-Identity。入站若带 Accept-Contact 或 Reject-Contact，也复制这些头、特征标签、值和参数。用户重组还须放入该 T-PF 自己的用户名单；不能把同一张全员名单发给所有 T-PF。〔[§16.2.3.2 第 1–4 项，印 502](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=503)；[§16.2.3.2 第 4–5 项、§16.2.3.3 第 1 项，印 503](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=504)〕

**CF 自行决定：**CF 新建重组正文，填 T 和 `regroup-action=remove`；用户重组还填上表中该 T-PF 的用户名单。本程序没有入站移除事务，不列“先向上游回 200”或“从来件复制正文”的步骤；这不等于禁止消息带有其他字段。只看到出站的 T 和 remove，或只缺一段入站抓包，都不能判定触发方式。要找与 T 匹配的入站事务和 CF 响应，或 CF 本地作出移除决定的记录。〔[§16.2.3.2 第 4–5 项、§16.2.3.3 第 1 项，印 503](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=504)；[§16.2.3.3 第 1–2 项，印 504](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=505)〕

**发出不等于对端已分派。** §6.3.1.3 的 NCF 移除分类在重组正文中查 `preconfigured-group`，T-PF 移除分类的原文却在 `mcptt-info+xml` 正文中查这个元素；两项还区分 S-CSCF 路由方向、目标 PSI，并要求动作为 remove。CF 自行移除时列出的 T、remove 和适用的用户名单，并不足以证明对端实际匹配了接收分类。不能据此断言一定拒绝，或自行规定该补哪个字段；应查接收侧看到的 MIME 正文、分派记录及该笔事务的结果。〔[§6.3.1.3 的移除 MESSAGE 接收分类，印 82](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=83)；[§16.2.3.2 第 4–5 项、§16.2.3.3 第 1 项，印 503](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=504)；[§16.2.3.3 第 1–2 项，印 504](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=505)〕

## 给终端的移除通知：先选收件人，再看正文

**组重组比用户重组多一跳。** 组重组的 NCF 收到移除请求，若因资源不足或拥塞风险拒绝，可回 500，可带 Retry-After，并停止。正常时它先回 200，再按 T 找出自己负责的组成组，找服务这些组成员的 T-PF。发给每个 T-PF 的 MESSAGE 以该 T-PF 的 PSI 为 Request-URI，`users-for-regroup` 列的是该 T-PF 服务且已归属 T 的 MCPTT ID。用户重组则由 CF 直接发到相应 T-PF；**到了 T-PF，两类移除用同一套程序**。这解释了为什么服务器之间会看到用户名单。〔[§16.2.4.2 第 1–4 项，印 505](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=506)；[§16.2.4.2 第 4 项续，印 506](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=507)；[§16.3.2.5，印 510](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=511)〕

**T-PF 的收件人是自己服务且已归属 T 的每个 MCPTT ID。** 例如上游名单只列甲，而 T-PF 当时服务的甲、乙都已归属 T；丙只是成员，未归属。若这条 MESSAGE 已进入移除程序，正常分支须分别向甲、乙发通知，不因上游漏列乙就跳过乙，也不向丙发。名单不同可以促使你核对两侧在当时的归属记录；这项程序没有把上游名单规定为本地名单的替代品，也没规定怎样修复不一致。〔[§16.2.2.5 第 1–3f 项，印 500](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=501)；[§16.3.2.5，印 510](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=511)〕

T-PF 也可因缺少资源而无法处理或有拥塞风险，回 500、可带 Retry-After，并停止。正常时它**先回上游 200**，再逐人构造新的 MESSAGE：

- Request-URI 是与该用户 MCPTT ID 关联的公共服务标识（PSI），不是服务器的 PSI 或临时组 T。
- 从来件复制 MCPTT 业务正文和 P-Asserted-Identity。来件若带 Accept-Contact 或 Reject-Contact，要带上全部相应的头、特征标签、值和参数。
- 复制重组正文，**不复制其中的 `users-for-regroup` 和 `groups-for-regroup`**。不是把整份正文删掉。对每个收件人，T-PF 发出 MESSAGE 后就在本侧把该 ID 视为已解除对 T 的归属；步骤没有要求等客户端回 200。〔[§16.2.2.5 第 1–3f 项，印 500](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=501)；[§16.2.2.5 第 3g–h 项，印 501](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=502)〕

**终端包没有名单，不能据此判定截包，也不能据此宣布整份 XML 合规。** 上面的逐人构造明确排除复制两种名单。客户端识别移除 MESSAGE 时看消息是否路由到本端、Request-URI 是否为该用户的 PSI、重组正文是否有 `preconfigured-group`，以及 `regroup-action` 是否为 `remove`；接收分类没要求名单。另一方面，附录 F.7.2 的 XSD 把两种名单分别设为可选，F.7.3 的通用语义却明文要求二选一，没为终端移除通知写例外；同节又规定 remove 时按 T 执行移除程序。不要据 XSD 或其中一项程序断言所有接收端必定接受、必定拒绝，或自行补一份名单。〔[§6.2.0.1，印 56](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=57)；[§16.2.2.5 第 1–3f 项，印 500](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=501)；[§F.7.2，印 580](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=581)；[§F.7.3，印 581](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=582)〕

排查时按 T 和每一笔 MESSAGE 对照 T-PF 的入站、上游响应、逐人出站及本侧归属；再查目标客户端是否收到、按哪一类处理，是否回了**它自己那一笔** 200。客户端收到相应通知后须回 200、在本端视为已解除归属，宜提醒用户。没抓到终端回执不能证明它没处理，T-PF 的 200 也不能替终端作证。[客户端收件后的处理](preconfigured-regroup-notification.md)同样适用于用户重组。〔[§16.2.1.4，印 497](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=498)；[§16.3.1.4，印 508](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=509)〕

如果操作方是组管理服务器（GMS），问题是何时结束 T 上的组呼、何时拆组，请查[Stage 2 临时重组拆除](temporary-regroup-teardown.md)，不要用这里的 CF 响应代替 GMS 的业务结果。
