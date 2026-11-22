# 移除预配置重组：控制功能何时回 200，移除通知发给谁？

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

如果操作方是组管理服务器（GMS），问题是何时结束 T 上的组呼、何时拆组，请查[Stage 2 临时重组拆除](temporary-regroup-teardown.md)，不要用这里的 CF 响应代替 GMS 的业务结果。
