# MCPTT 按条件发起互通 ad hoc 组呼：谁选人，何时发 IWF 请求？

**主叫给条件，MCPTT server 确定邀请名单。** 选完后，server 就可以向 IWF 发请求，不必等本侧被叫的响应。这里是 TS 23.283 V19.5.0、Rel‑19 Stage 2 §10.17.3.1，限 MCPTT client 1 的用户按条件邀请 MCPTT 和 LMR 用户。如果由 IWF 代表 LMR 用户发首请求，查 [§10.17.3.2 的 LMR 发起路径](adhoc-group-criteria-lmr-origin.md)；如果 MCPTT client 1 已直接给出双方参与者的 MCPTT ID 名单，查 [§10.17.3.5 显式名单路径](adhoc-group-explicit-list-mcptt-origin.md)。后者的逐 LMR 用户请求和有条件的应答超时，不套进本页。[LMR 按条件发起，印刷页 186–187（PDF 第 187–188 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=187)；[MCPTT 直接给名单，印刷页 189–190（PDF 第 190–191 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=190)。

## 先选人，再发 IWF 请求

主叫须有发起 ad hoc 组呼的权限，IWF 已配置两套系统的组和用户 ID 映射。图中 client 1 发带条件的请求（Step 1）；MCPTT server 核这次请求的授权（2），向 client 1 回送 request return（3），再按 Step 1 的条件确定邀请名单（4）。映射提供标识转换，不替代验权。Step 3 是对请求的返回，不是 Step 10 的建呼响应。

MCPTT server 在 Step 8 向 IWF 发 IWF ad hoc group call request。虽然图把 8 画在 7a/7b 之后，NOTE 3 允许它在 4 之后任何时候发，不必等本侧被叫 client 2/3 的响应。IWF 在 Step 9 回 server。经过 IWF 的两系统间消息由 IWF 转换身份和协议；NOTE 4 允许 IWF 向 LMR 用户按普通组呼处理。NOTE 1 没定义 LMR 侧怎么选人和发出邀请。表中的 criteria 可以由 IWF 与 LMR 系统使用；总述列一名代表 GSM-R 组的 LMR 用户，也不是逐个 LMR 终端的名单。[§10.17.3.1 前提、图 10.17.3.1-1 与 Steps 1–10，印刷页 184–185（PDF 第 185–186 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=185)；[§10.17.1 与 IWF-1 入口，印刷页 181（PDF 第 182 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=182)。

## IWF 应答说的是哪一段

| 观察到的消息 | 看这条消息本身 |
| --- | --- |
| **8：server → IWF，请求** | 必带主叫 MCPTT ID、关联本次通信的 MCPTT ad hoc group ID 和 SDP offer。被邀者的 MCPTT ID 是另一行、可选；预配置 MCPTT group ID 也是可选，指供本次使用的组配置。选人条件可用详情、可标识条件的标签或两者，不等于主叫位置；该 IWF-1 字段是可选的，不把 Step 1 的按条件入口变成可省。只有发起客户端请求话权才带隐式话权请求，此时必须带；广播、迫近危险、紧急指示如使用，只能有一种。 |
| **9：IWF → server，应答** | 必带主叫 MCPTT ID、关联本次组呼的 MCPTT ad hoc group ID、Result（success 或 failure）。SDP answer 栏标 O，说明写在 Result 成功时出现；不从 success 补写未见的 SDP answer。表不提供被邀用户名单。 |

[表 10.17.2.2-1、10.17.2.3-1，印刷页 182–183（PDF 第 183–184 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=183)。§10.17.2.3 的节标题和表名写 response，表前说明却写 request；用图中 Step 9 的方向及应答字段辨认，不拿请求表解释应答。两张表适用于 IWF-1，不能直接给 client 1 → server 的 Step 1 配字段。本段没规定 ad hoc group ID 的分配、有效期或重用，预配置组 ID 也不等于本次 ad hoc group ID。

只见 IWF 发出同次 Step 9 success，只能确认它发出了成功结果。server 是否实际收到 Step 9，要另有与这次尝试匹配的 server 端接收证据。同样，只见 server 发出 Step 10，不等于原 client 1 已实际收到。Step 9 不代替被邀 MCPTT client 的 Step 7、主叫的 Step 10，也不证明 LMR 用户实际加入。§10.17.3.1 的总述回指 TS 23.379 [7] §10.19.3.1.1，Steps 1–7 和 10 写同 §10.19.3.1.3（10 对应该条 Step 10）。保留两种回指；本页不判断被引条文正文，也不从图推出 server 怎样等待或汇总 Step 7 与 9 才发 Step 10。§2 [7] 未指定修订，按同 Release 最新版本查引用。[图及回指，印刷页 185（PDF 第 186 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=186)；[§2 [7]，印刷页 11（PDF 第 12 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=12)。

## 被邀请、加入、收到通知是不同事实

Step 11 只列**已确认请求且已加入**的 MCPTT 用户。server 可以把这份信息通知发起用户；通话中 MCPTT 用户加入或离开时，可以多次通知。另一条规则适用于获授权且已配置接收参与者信息的用户：MCPTT 用户迟到加入或离开时，server 向这些用户通知相关 MCPTT ID。这条通知不沿用发起用户分支的“可以”。图没画出这些收件人；不凭标准规定或发送记录判某个用户已实际收到。NOTE 5 不把 LMR 用户纳入确认组呼请求的通知；没看到某个 LMR 用户的确认通知，不能判它没有加入。

Step 12 是另一步，建立媒体面和话权控制资源。正文列 client 1、client 2 和 LMR 用户；图还画出 client 3 的邀请与响应，资源建立的横条跨过它。不凭这处差异判断 client 3 必被排除或已建资源。有成员通知也不证明媒体已达、已听见或某人已取得话权。[Steps 11–12 与 NOTE 5，印刷页 185–186（PDF 第 186–187 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=186)。

原生 Stage 3 的[条件选人和持续增删](../groups/adhoc-criteria-membership-lifecycle.md)、[显式名单初建](../groups/adhoc-explicit-list-establishment.md)另读。本页不由 IWF Stage 2 图推 SIP 字段、全员成功门槛或实际播放。
