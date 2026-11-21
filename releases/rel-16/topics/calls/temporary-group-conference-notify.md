# 临时组呼的 conference NOTIFY：组标识怎么写，参与者名单从哪来？

临时组 T 把组成组 A、B 拉进同一通 MCPTT 组呼。订阅了 A 组 NCF 会议事件的调度席还能看到本组用户，却看不到 B 组用户。先查服务 A 的非控制功能（NCF）**有没有收到并保存这场会话的控制侧通知，随后发给调度席的通知又用了哪份状态**。不能只凭参与者列表少了一个人，就判断他没加入或没收到语音。这是 [TS 24.379 V16.14.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf) 规定的临时组呼会议事件包处理，不是组成员同步。

## 先用报文方向判断两个组标识

在两个服务器互发、`Event: conference` 的 SIP NOTIFY 中，字段位于 `application/vnd.3gpp.mcptt-info+xml` 正文：

| 这份 NOTIFY 的发送方 → 目标 | `mcptt-calling-group-id` | `mcptt-request-uri` |
| --- | --- | --- |
| T 的控制功能（CF）→ A 的 NCF | 临时组 T | 组成组 A |
| A 的 NCF → T 的 CF | 组成组 A | 临时组 T |

如果通知目标是用户，`mcptt-request-uri` 用目标用户的 MCPTT ID，不套用表里的对端组 ID。不要把这个 **XML 元素**当成 SIP 请求行的 Request-URI，也不要把它或 `mcptt-calling-group-id` 当成另一份正文 `application/conference-info+xml` 的 `conference-info@entity`。[§6.3.3.4，印 124](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=125)；[§6.3.4.3，印 129–130](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=130)。

## 跟着订阅对话查名单经过哪一端

认清**订阅的发起方向和返回通知的方向相反**，再核对这份来向 NOTIFY 是否对应早先发出的 SUBSCRIBE：

- **CF 收到 A 的 NCF 回来的 NOTIFY。** 对 CF 先前向该 NCF 发出的订阅，CF 要处理这份通知，按控制侧规则改写，再转发给**其他订阅了会议事件的参与者**。不能拿收到的 A→T 正文当作随后对外发出的 T→其他接收者正文。此条不规定一个通用的 CF 快照拼接或覆盖算法。[§10.1.3.4.3 的入向处理，印 305](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=306)。
- **A 的 NCF 收到 CF 回来的 NOTIFY。** 对 NCF 先前向 CF 发出的订阅，NCF 要处理并按正文保存会议状态，按非控制侧规则改写，再转发给订阅了会议事件的 **MCPTT 客户端**。非控制侧的会议状态正文要带上从 CF 通知保存的状态，也要带上本侧参与者的状态。若本组可见、外组缺失，逐段比对 NCF 实收的 CF 正文、NCF 保存的状态和 NCF 发给本地客户端的正文；先找哪一段少了记录，不要先断定 B 组用户退呼。[§10.1.3.5.3 的入向处理，印 307](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=308)；[§6.3.4.3，印 130](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=131)。

## 对端服务器参与会话，也应列成一个 user 吗？

**不应。** 临时组会话中的 NCF 在会话程序里算参与者，但 CF 生成 `conference-info` 时不把 NCF 当成 `<user>`。临时组 CF 会作为会话参与者出现，但 NCF 生成该正文时不把 CF 列成 `<user>`。看用户状态时要读实际用户的 `<endpoint>` 与其中的 `<status>`；服务器没被列名不等于链路失败，收到名单也不证明任一客户端实际收听。[§6.3.3.4，印 124](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=125)；[§6.3.4.3，印 130](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=131)。

如果工单查的是[调度席查询或订阅会议状态](conference-participant-status.md)，先核对订阅的对象与对话。若问题是最后一个订阅结束后该停哪条链路，查[临时组 conference 退订](conference-event-subscription-termination.md)。若要查客户端收到重组的创建或移除通知后如何认定归属、保存或回 200，走[预配置重组通知](../groups/preconfigured-regroup-notification.md)，不是用这份会议名单替代重组结果。
