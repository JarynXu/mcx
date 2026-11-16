# 预建立会话承载普通组呼：REFER 寻址、响应与独立通知

TS24.379 V19.4.0，在网普通预安排组呼使用已建立的预建立会话；排除广播、重组、远程发起、紧急及 imminent peril 扩展。

请求不携优先级状态指示，不请求 functional-alias 或应用优先级扩展。本主题不展开位置处理；按 §10.1.2.2.2.1 step3(c)(iii)，当需要隐式话权控制且 allow-location-info-when-talking=true 时仍须携带位置，不能因用户未主动请求而省略。

主叫 REFER 与终接 INVITE 是不同方向；T-PF 条目只适用于该条明确指定的终接处理分支。

## 区分预建立对话与目标组

适用条件：用户要求在预建立会话内发起预安排组呼，且目标组的 preconfigured-group-use-only 不为 true。

客户端发对话外 REFER。Request-URI 是预建立会话 identity，Target-Dialog 标识预建立 dialog；Refer-To 则用 cid 指向 resource-lists，匹配的 Content-ID 与单一 entry 的 URI 承载目标预安排组 ID。entry 的 URI headers 带 MCPTT/ICSI 的 Accept-Contact require/explicit 以及 body，内含 session-type=prearranged 和 originating client ID；需改预建立参数或按 §6.4 需要隐式话权控制时还带 SDP offer。请求含 MCPTT P-Preferred-Service、Contact 的 g.3gpp.mcptt、Supported=norefersub 和 Refer-Sub=false。

依据：§10.1.1.2.2.1;10.1.2.2.2.1 steps1–3,8–12;6.3.1.2。

## 业务检查仍然适用

适用条件：参与功能收到指向预建立 identity 的 REFER，cid 对应 resource-lists 中预安排组 URI，嵌入 body 的 session-type=prearranged，Content-ID 匹配。

预建立可用不免除业务检查。资源不足/拥塞可拒绝 500（可附 Retry-After）；由 PAI 的 PUI 找主叫 MCPTT ID，无绑定或绑定过期为 404/141；本地策略不允许预安排组呼为 403/109；N6 已 exceeded 时为 486/103；无法确定目标组控制功能为 404/142。通过适用前置检查才到 REFER 200；下游控制侧还要执行该次呼叫的组归属与准入。

依据：§10.1.1.3.1.2 entry and steps1–5,9–10,13–14。

## REFER 200 先于业务 INVITE

适用条件：参与功能已经处理本主题普通预安排 REFER 的适用前置门槛且未拒绝请求；REFER 同时带 Refer-Sub=false 和 Supported=norefersub。

不建立 REFER 隐式订阅。原文顺序是先生成并发送 REFER 200，再生成业务 INVITE 并发往目标组控制功能 PSI；组 ID 放入 mcptt-request-uri。REFER 200 中的 Refer-Sub=false 表示没有建立隐式订阅，并不表示下游 INVITE 已被接受；不能为此标准路径强制增造一个 REFER 结果 NOTIFY。

依据：§10.1.1.3.1.2 steps6,13–17,19 and Note11。

## 业务媒体与结果分别处理

适用条件：普通预安排 REFER 已通过适用前置门槛，参与功能按 §10.1.1.3.1.2 生成并发送业务 INVITE。

业务 INVITE 按 §6.3.2.1.4 构造：SDP 依据预建立初始及随后修改的协商结果，并结合 REFER URI body 中若有的 offer；不是将 REFER 不加区别转发成 INVITE。收到业务 INVITE 临时响应须丢弃而不向客户端转发；收到 200 或 4xx/5xx/6xx 后按对应分支与媒体层交互。客户端收到 REFER final 2xx 的独立动作也是媒体交互。

依据：§6.3.2.1.4 steps1–14;10.1.1.3.1.2 response paragraphs;10.1.2.2.2.1 final2xx paragraph via10.1.1.2.2.1。

## 终接业务 Contact 的映射

适用条件：T-PF 已通过终接前置门槛，已经进入 §6.3.2.2.5.3 普通自动预建立分支，或 §6.3.2.2.6.3 普通手动预建立分支的生成上游 INVITE 200 步骤；空闲预建立会话与语音、话权两媒体段匹配等选择条件见既有 group-terminating-mode。

上游业务 INVITE 200 复用 §6.3.2.2.4.2，Contact 的 MCPTT session identity 映射至收到的控制功能 INVITE Contact 所给身份；不是把所有业务会话 Contact 固定成 §8.2 的预建立 URI。自动分支的 200 仍为 Unconfirmed；手动分支另需等客户端 re-INVITE 200，既有接续响应主题保留其完整条件。

依据：§6.3.2.2.4.2 step3(c);6.3.2.2.5.3;6.3.2.2.6.3。

## conference 通知是独立订阅

适用条件：客户端已参与一个进行中的非广播组呼，并选择订阅参与者状态。

conference NOTIFY 来自另建的 conference SUBSCRIBE dialog，不是上述已抑制的 REFER 隐式订阅。客户端 SUBSCRIBE Request-URI 用业务组会话 identity，mcptt-request-uri 用组 ID，Accept 为 application/conference-info+xml；需要当前和后续状态则 Expires=4294967295，只取当前则初始 Expires=0。客户端对关联 NOTIFY 按 RFC 处理，可据正文处理/显示参与者状态；不能据收到一个 NOTIFY 判断所有组员已接受呼叫。

依据：§10.1.3.1;10.1.3.2;6.3.1.4。

## 通知路由与权限分别检查

适用条件：已参与的非广播普通组呼客户端向服务自己的参与功能发 conference SUBSCRIBE；请求符合 §6.3.1.4 的会话身份/Event=conference 定义，且带 MCPTT P-Asserted-Service、conference-info Accept、正文组 ID。

参与功能先把 Request-URI 解析到既有业务会话，失败为 404/137；成功后以映射的业务会话 identity 作下游 SUBSCRIBE Request-URI，插入 calling-user-id 和自己的 Record-Route。组主控还检查 on-network-allow-conference-state，不允许则 403/138 并停止；允许才处理、缓存订阅并发状态通知。参与功能转发 SUBSCRIBE 200 时映射 Contact；收到该订阅 dialog 中面向服务客户端的 NOTIFY 时复制内容并转送。

依据：§10.1.3.3;10.1.3.4.1 steps1–4。

## 结束业务仍保留预建立会话

适用条件：T-PF 收到控制功能对该预安排业务组呼的 BYE，且 MCPTT session id 对应与参与功能已有预建立会话的用户。

按 §6.3.2.2.8.2，先断开朝控制功能的媒体资源，再回该 BYE 的 200，然后解除客户端侧与控制侧媒体资源的连接，并保留客户端侧预建立会话。业务呼叫结束不自动等于第 8 章预建立 dialog 被拆除。

依据：§10.1.1.3.4.2;6.3.2.2.8.2。

## 证据边界

- 本主题选普通预安排组呼，不把私呼、first-to-answer、chat 的业务授权或优先级特例混为同一 REFER 流程。
- 预建立 INVITE 200、REFER 200、业务 INVITE 200、SUBSCRIBE 200 与 NOTIFY 的响应分别属于不同对象，不能用其中一个替代另一层结果。
- 未验证 TS24.380 的 MCPC Connect/Disconnect 等消息如何把最终业务结果呈现给客户端；不得以本主题没有 REFER NOTIFY 推断客户端永远不知道业务失败。
- preconfigured-group-use-only=true 时应提示且必须停止，不能发起本链。被引用的 chat 程序在本条按原文改为预安排组 URI 和 prearranged 类型，不把 chat 的业务准入规则移植过来。URI 转义、MIME 组装及 SDP 全量语法仍依引用标准。
- N6 触发词为 exceeded，不因 Warning 文本 reached 就改成等于上限即拒绝。主控准入转到已有 groups/prearranged-admission，本条不重述。
- 若不同时具备两个抑制字段，本条不推导完整 RFC REFER 订阅状态机。私呼 functional-alias 等其他分支可能延后 REFER 响应，本结论只适用于此处预安排组呼。
- 隐式话权请求判断链接已有 calls/implicit-floor-request，不从成功响应推出实际授予。302、优先级 INFO/re-INVITE、完整媒体失败通知与用户界面状态不在本条展开。普通范围没有隐式归属触发；原文条件性的归属完成/撤销不外推为每次必做。
- 这是基于本条映射对象的身份区分，不声称两个 URI 字符串在任何实现中必须不同，也不定义物理节点黏性。T-PF 初始 INVITE Contact 映射已由 group-terminating-addressing 覆盖，这里仅补 200 路径。
- 这是业务参与者状态入口，不覆盖 RFC4575 增量合并算法、通知正文全部字段或跨系统非主控组聚合。
- 正文 §10.1.3.3 的下行 NOTIFY Request-URI 写成 MCPTT user 的 public service identity；本稿保留这个措辞异常，不静默改为 public user identity。主控入口还要求 calling-user-id 是组会话参与者；不以组成员身份或 REFER 200 代替。
- 客户端用 REFER method=BYE 离开普通组呼的程序见 group-participant-leave；服务器移除及保留预建立见 group-participant-removal。TS24.380 的媒体断开细节仍未核。

## 按需继续

- [preestablished-session-lifecycle](preestablished-session-lifecycle.md)
- [group-terminating-mode](group-terminating-mode.md)
- [group-terminating-responses](group-terminating-responses.md)
- [../groups/conference-state](../groups/conference-state.md)
- [../groups/prearranged-admission](../groups/prearranged-admission.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页95、103、106、107、108、118、120、121、123、124、125、277、282、283、284、285、286、289、325、326、327、356、357、358、359；仅本版本。

- [group-participant-leave](group-participant-leave.md)

- [group-participant-removal](group-participant-removal.md)
