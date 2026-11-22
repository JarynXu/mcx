# 临时组呼的 conference NOTIFY：组标识怎么写，参与者名单从哪来？

临时组 T 把组成组 A、B 拉进同一通 MCPTT 组呼。订阅了 A 组 NCF 会议事件的调度席还能看到本组用户，却看不到 B 组用户。先查服务 A 的非控制功能（NCF）**有没有收到并保存这场会话的控制侧通知，随后发给调度席的通知又用了哪份状态**。不能只凭参与者列表少了一个人，就判断他没加入或没收到语音。这是 [TS 24.379 V16.14.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf) 规定的临时组呼会议事件包处理，不是组成员同步。

## 先用报文方向判断两个组标识

在两个服务器互发、`Event: conference` 的 SIP NOTIFY 中，字段位于 `application/vnd.3gpp.mcptt-info+xml` 正文：

| 这份 NOTIFY 的发送方 → 目标 | `mcptt-calling-group-id` | `mcptt-request-uri` |
| --- | --- | --- |
| T 的控制功能（CF）→ A 的 NCF | 临时组 T | 组成组 A |
| A 的 NCF → T 的 CF | 组成组 A | 临时组 T |

如果通知目标是用户，`mcptt-request-uri` 用目标用户的 MCPTT ID，不套用表里的对端组 ID。不要把这个 **XML 元素**当成 SIP 请求行的 Request-URI，也不要把它或 `mcptt-calling-group-id` 当成另一份正文 `application/conference-info+xml` 的 `conference-info@entity`。[§6.3.3.4，印 124](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=125)；[§6.3.4.3，印 129–130](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=130)。

## 上游会议订阅还没发出，先查两边各自触发条件

临时组 T 的 CF 向组成组 A、B 的 NCF 订阅会议状态，不必等所有 NCF 都接受邀请。§10.1.3.4.3 有两个入口：

- **先有参会者订阅，后来有 NCF 回应：** CF 实收发给某个 NCF 的 INVITE 的 200，并且本场已有至少一位参会者按 §10.1.3.4.1 向这个 CF 订阅会议事件。只有组成组 NCF 上的客户端订阅，不满足这个入口。
- **先有 NCF 加入，后来有首个订阅：** CF 实收符合 §10.1.3.4.1 的首个参会者订阅，且本场已有至少一个 NCF 参与。

进入任一分支后，CF **逐个检查 NCF**：对这场会话发给它的 INVITE 已实收 200，且尚未向它发送这项订阅，才发一条新的 SUBSCRIBE。比如，首个订阅到达时甲的 200 已到、乙的还没到，就先给甲发；乙的 200 后到且这个 CF 上仍有参会者订阅，才轮到乙，甲不会因乙的 200 再发一遍。若两边的 200 先到、之后才有首个合格订阅，两边都符合条件。已发出 INVITE、收到其他方法的 200 或 NCF 在别处留下“已发送 200”的日志，都不能代替 CF 本机实收这条腿的应答。[TS 24.379 V16.14.0 §10.1.3.4.1 步骤 5，印 303](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=304)；[§10.1.3.4.3 入口及步骤，印 304](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=305)。

**A 的 NCF 何时反向订阅 T 的 CF？** 在 NCF 接收订阅的正常分支，触发的是来自**本侧 MCPTT 客户端**的首个会议事件订阅，不是 CF 发来的一条服务器订阅。另一个入口是已有预安排组呼或[已有聊天组呼](trusted-regroup-refused-uri-list.md#chat-ncf-ongoing-invite)并入临时组：NCF 实收该并入流程的 ACK，且组成组会话内至少有一台客户端已有会议事件订阅，才按反向程序订阅 CF。不能仅凭一个 ACK、CF 已发订阅或没有跨组名单判断反向订阅已发或已获准。[§10.1.3.5.1 步骤 5、§10.1.3.5.3，印 306–307](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=307)；[§10.1.1.5.2.3，印 262](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=263)；[§10.1.2.5.1.3，印 298–299](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=300)。

## 发出的 SUBSCRIBE 和接收入口写了不同的字段

下面是**服务器间订阅请求**的构造，不是上文的 NOTIFY。两个方向各建一个新 SIP 对话，请求的 `Expires` 均为 `4294967295`；该值不能证明订阅获准或会一直有效。

| SUBSCRIBE 方向 | SIP 请求行的 Request-URI | MCPTT 信息正文的 `mcptt-request-uri` | 正文的 `mcptt-calling-group-id` |
| --- | --- | --- | --- |
| CF → A 的 NCF | 服务组成组 A 的 NCF 公共服务标识（PSI） | 组成组 A | 临时组 T |
| A 的 NCF → CF | 先前发给该 NCF 的 INVITE 的 Contact 中的临时会话标识 | 临时组 T | 组成组 A |

NCF 面向本地客户端另用自己生成的会话标识，不能放到反向订阅的 Request-URI。两个发送条款讲的是 **`mcptt-calling-group-id`**。在相关接收条款中，CF 核对正文中的组会话组 ID，再读 **`mcptt-calling-user-id`** 中的参会者 ID 或组成组 ID；NCF 核对正文中的组成组 ID，再读 **`mcptt-calling-user-id`** 中的参会者 ID 或临时组 ID。这里不合并两种字段拼写，也不推定中间节点自动转换。[§10.1.3.4.3，印 304](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=305)；[§10.1.3.5.3，印 306–307](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=307)；[§10.1.3.4.1，印 303](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=304)；[§10.1.3.5.1，印 305–306](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=306)。

**不能把没收到 NOTIFY 定性为 403/138。** 找到这笔服务器订阅实际发出的请求，再查另一端实收的正文、目标、`P-Asserted-Service` 中的 MCPTT 服务标识和 `Accept: application/conference-info+xml`。符合该非广播接收入口后，若组文档的 `on-network-allow-conference-state` 检查不允许，才是这两条中的 **403 / Warning 文本 138** 分支。只知道实收请求缺少 `mcptt-calling-user-id`，不能凭这两条推出同一拒绝，也不能把两种字段都加上当成规范要求。原文未裁定这里的互通处理；不要用另一方向的 NOTIFY 或一笔普通客户端订阅的成功替代这笔 SUBSCRIBE 的实际结果。[§10.1.3.4.1、§10.1.3.5.1，印 303、305–306](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=304)。

## 跟着订阅对话查名单经过哪一端

认清**订阅的发起方向和返回通知的方向相反**，再核对这份来向 NOTIFY 是否对应早先发出的 SUBSCRIBE：

- **CF 收到 A 的 NCF 回来的 NOTIFY。** 对 CF 先前向该 NCF 发出的订阅，CF 要处理这份通知，按控制侧规则改写，再转发给**其他订阅了会议事件的参与者**。不能拿收到的 A→T 正文当作随后对外发出的 T→其他接收者正文。此条不规定一个通用的 CF 快照拼接或覆盖算法。[§10.1.3.4.3 的入向处理，印 305](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=306)。
- **A 的 NCF 收到 CF 回来的 NOTIFY。** 对 NCF 先前向 CF 发出的订阅，NCF 要处理并按正文保存会议状态，按非控制侧规则改写，再转发给订阅了会议事件的 **MCPTT 客户端**。非控制侧的会议状态正文要带上从 CF 通知保存的状态，也要带上本侧参与者的状态。若本组可见、外组缺失，逐段比对 NCF 实收的 CF 正文、NCF 保存的状态和 NCF 发给本地客户端的正文；先找哪一段少了记录，不要先断定 B 组用户退呼。[§10.1.3.5.3 的入向处理，印 307](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=308)；[§6.3.4.3，印 130](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=131)。

## 对端服务器参与会话，也应列成一个 user 吗？

**不应。** 临时组会话中的 NCF 在会话程序里算参与者，但 CF 生成 `conference-info` 时不把 NCF 当成 `<user>`。临时组 CF 会作为会话参与者出现，但 NCF 生成该正文时不把 CF 列成 `<user>`。看用户状态时要读实际用户的 `<endpoint>` 与其中的 `<status>`；服务器没被列名不等于链路失败，收到名单也不证明任一客户端实际收听。[§6.3.3.4，印 124](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=125)；[§6.3.4.3，印 130](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=131)。

如果工单查的是[调度席查询或订阅会议状态](conference-participant-status.md)，先核对订阅的对象与对话。若问题是最后一个订阅结束后该停哪条链路，查[临时组 conference 退订](conference-event-subscription-termination.md)。若要查客户端收到重组的创建或移除通知后如何认定归属、保存或回 200，走[预配置重组通知](../groups/preconfigured-regroup-notification.md)，不是用这份会议名单替代重组结果。

## 临时聊天组的组成组身份：本地 INVITE 200 写哪个 Contact？

组成聊天组 A 所在的非控制 MCPTT 功能（NCF）正在以非控制连接模式参与临时聊天组呼。先查它**实际收到的初始 INVITE**：请求属于送组控制功能的 INVITE（经 PSI 路由，SIP Request-URI 为服务该组的 PSI，请求 Contact 不带 `isfocus`），MCPTT-info 正文中的 `mcptt-request-uri` 标识临时组呼里的组成聊天组 A。这里的业务组 ID 不等于 SIP 请求行的 Request-URI，也不是临时组 T 的标识。满足这些条件时，NCF 面向这个客户端按 §10.1.2.4.1.1 执行聊天组建立或加入程序。该笔请求若成功得到 200，响应 `Contact` 中的 MCPTT 会话身份须由 **A 的 NCF 自己生成**。不要把临时组 CF 发来的临时会话身份抄进客户端腿，也不要据此为每个加入者都新分配会话身份。NCF 反向订阅临时组 CF 时，用的是上文所列的临时会话身份。

**组成组服务器实收本地终端同一对话的 re-INVITE 时，按聊天组 CF 的更新程序处理。** 确认请求指向该聊天会话的 MCPTT 会话身份，再查 §10.1.2.4.1.2 的适用检查和响应。§10.1.2.5.1.6 要求 NCF 在这次处理中充当 CF；不能把整个程序改成 O-PF 向临时组 CF 透传后等待回包，也不能把初始 INVITE 的 Contact 澄清当作所有 re-INVITE 都必回 200 的规则。这里说的是 NCF 面向本地客户端的角色，不是临时组的全局控制移交。

**会议 NOTIFY 单独取证。** §10.1.2.5.1.5 在这个加入入口指定非控制侧通知程序 §10.1.3.5.2。查这次加入是否应按 §10.1.2.4.1.1 第 25 项发送通知时，先核聊天会话先前已在进行，且至少一位参与者已订阅。非控制侧通知程序以实际新增参与者，或实际收到一个参与者的 BYE 为触发，按 §6.3.4.3 生成会议通知，发给订阅了会议事件包的参与者。初始 INVITE 的 200 不能单独证明本地已实际新增参与者、NOTIFY 已发或对端收到；一份 NOTIFY 也不能证明全局控制移交、临时组拆分或媒体送达。若抓到的是 **临时组 CF 发给 NCF 的 BYE**，先查[组成聊天组拆分](chat-participant-or-session-release.md)，不要按本地客户端更新分支判角色。

依据：[TS 24.379 V16.14.0 §10.1.2.5.1.5–.6，印 299](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=300)；[§10.1.2.4.1.1，印 286–290](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=287)；[§10.1.2.4.1.2，印 291–294](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=292)；[§10.1.3.5.2、.5.3 注，印 306](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=307)；[§6.3.1.1，印 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=79)；[§6.3.4.3，印 129–130](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=130)。
