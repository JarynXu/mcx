# 查询另一位 MCPTT 用户的组归属：订阅送给谁，结果按哪台客户端读

甲想知道乙已归属哪些 MCPTT 组。两人属于同一 MC 系统，在网使用 MCPTT，由不同的参与功能（PF）服务。本页只讨论甲发起的归属状态订阅，不改变乙的归属。按组查有哪些成员，用[组名单查询](group-list-query.md)；判断乙是否已经参加某一场组呼，用[会议参与者状态](../calls/conference-participant-status.md)。

## 甲先把 SUBSCRIBE 发给自己的参与功能

查询的首个 SIP SUBSCRIBE 以**服务甲的起始 PF 公共业务标识（PSI）**为 Request-URI，MCPTT 信息正文 `<mcptt-request-uri>` 填目标**乙的 MCPTT ID**。客户端在 P-Preferred-Service 中标识 MCPTT 服务，声明接受 `application/pidf+xml`。只取当前状态用 `Expires: 0`，还想接收之后变化用 `Expires: 4294967295`。后者是请求的期限，不是通知永远有效的保证。查询自己在某台客户端的归属时才有该条所列按客户端 ID 限制的 simple-filter 要求；不能把该要求抄成查询乙的必填项。

起始 PF 处理的是寻址到自己、正文指向自己不服务的乙、带 MCPTT P-Asserted-Service 且 Event 为 `presence` 的 SUBSCRIBE。实际进入 §9.2.2.2.10 的转发分支时，它从入站 P-Asserted-Identity 的公共用户身份识别甲，再向服务乙的**终接 PF PSI**发出 SUBSCRIBE：

| 发往乙侧 PF 的请求字段 | 放入什么 |
| --- | --- |
| SIP Request-URI | 乙的终接 PF PSI |
| P-Asserted-Identity | 甲的起始 PF PSI |
| 正文 `<mcptt-request-uri>` | 乙的 MCPTT ID |
| 正文 `<mcptt-calling-user-id>` | 甲的 MCPTT ID |

到乙侧后，P-Asserted-Identity 标识的是甲侧 PF；终接 PF 按正文识别发起用户甲。起始 PF 转发收到的订阅响应、NOTIFY 及 NOTIFY 的响应。这里不规定用什么算法查到乙侧 PF 的 PSI。第 9 章还适用 §6.6 的通用保护规则，字段对照不是信任任意自报身份的办法。

固定版在 MIME 类型写法上有一处差异。§9.2.1.3 的客户端正文、§9.2.2.2.10 的转发出站正文和 §9.2.2.2.4 的终接入口都写 `application/vnd.3gpp.mcptt-info+xml`，§9.2.2.2.10 的入站检查和目标识别却写 `application/vnd.3gpp.mcptt-info`。不能只凭客户端按前一写法发送，就断言起始 PF 一定进入该转发分支；这里不裁定两种写法在实现中如何匹配。

依据：TS 24.379 V16.14.0 §6.6.1.1、§9.2.1.3、§9.2.2.2.4、§9.2.2.2.10，印刷页 138、169–170、176、182–183。

## 乙侧可以拒绝只读查询；200 不含各组的结果

乙侧 PF 收到寻址到自己、正文指向它所服务的乙、带 MCPTT P-Asserted-Service 及 `presence` Event 的订阅后，按两人的 MCPTT ID 核对。若发起用户与被查询用户不同，且甲**未获授权修改乙的归属状态**，服务器须返回 403 并停止；通过该检查才按此分支生成 200。条款用修改权限决定是否允许这次订阅，订阅本身不修改归属。

甲收到 **SUBSCRIBE 的 200** 只知道该订阅请求被接受。要确认乙在哪台客户端归属某个组，须看甲端实际收到携有效 per-user `application/pidf+xml` 正文的 NOTIFY。在正文按三层身份找：`<presence entity>` 是乙的 MCPTT ID，`<tuple id>` 是乙的一台 MCPTT 客户端的 ID，`<affiliation group>` 是这台客户端上的组 ID。同一通知若列了两台客户端，应分别读各自的组和 `status`，不要把它们合成一个用户级的已归属状态。缺少可选的 `status` 不能当成 `affiliated`。

生成通知时，服务器不列已到期或处于 `deaffiliated` 的组条目；订阅若带适用的客户端过滤，生成正文还须遵循该过滤。正文未列某组，只说明这份通知没有报告该项，不能反推乙何时解除归属、从来没归属或不再是组成员。由归属变更处理调用通知程序且已识别该次 PUBLISH 的 p-id 时，服务器须写入该值。甲收到的正文若有 `<p-id>`，它标识触发通知的 PUBLISH，不是 SUBSCRIBE 的对话标识；没有该元素，不能靠两条消息的先后给它配一个 PUBLISH。查到归属也不证明乙已进入某场通话或正在收听。

依据：TS 24.379 V16.14.0 §9.2.1.3、§9.2.2.2.4–.5、§9.2.2.2.10、§9.3.1.2（含表 9.3.1.2-1），印刷页 169–170、176–177、182–183、194–196。
