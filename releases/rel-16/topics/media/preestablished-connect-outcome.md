# 预建立会话里两次看到 Connect 和 Accepted，是两通 MCPTT 呼叫吗？

**报文不能当呼叫计数器。** 同一客户端可以有多条预建立会话，每条各有一个状态机。设 P 正在承接一通呼叫，Q 已建立但还没使用。又来一份要求确认的 Connect：如果到的是 P，客户端要回 Accepted，P 保持在用；如果到的是 Q，客户端可以不接受来呼。不能拿 P 的状态替 Q 作答。参与 MCPTT 功能（PF）也按客户端、按预建立会话分别保存状态。以下只讨论在网 MCPTT：PF 和客户端已经建好预建立会话，现在用它承接预安排组呼、聊天组呼或私呼。[TS 24.380 V16.9.0，Rel-16 Stage 3，§§9.1、9.2.1、9.2.2.1，印 193–194](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=194)；[§§9.3.1、9.3.2.1，印 196–197](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=198)

## 看客户端：这条会话收到 Connect 之前是什么状态？

| 对应预建立会话的前态 | 客户端的动作 |
| --- | --- |
| 未在用，客户端接受来呼 | 回 Accepted，创建基本话权参与者状态机实例，转为在用。若 Connect 带 Media Streams 字段，只使用其中标为本次呼叫使用的流。没有该字段不改变接受、建状态机和转入在用这三项动作。 |
| 未在用，客户端不接受 | 回 Busy 或 Not Accepted；这条会话保持未在用。未在用的这两种应答都不以 Connect 的要求确认位置 1 为条件。 |
| 已在用，又收到 Connect | 如果 subtype 首位为 1（要求确认），回 Accepted；未置位时本条不要求回确认。无论置位与否，这条会话仍在用。 |

因此，第一份 Connect 被接受后，如果确认未到 PF，PF 可能重发原 Connect；客户端对要求确认的重发再回一次 Accepted。这解释了**一通呼叫出现两份 Accepted**，但不能反过来断定每两份确认都是重发。要定案，在客户端找对应预建立会话、收包前状态和回包，在 PF 找同一呼叫的控制通道、Connect 内的 MCPTT Session Identity 及 T55 触发的重发记录。[§9.2.2.3.2，印 195](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=196)；[§9.2.2.4.2，印 196](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=197)；[§9.3.2.4.8，印 201–202](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=202)

确认包本身是 **RTCP APP（PT=204、名称 MCPC）的 Acknowledgement**。表 8.3.6-1 有话权参与者的 SSRC 和 Reason Code，没有 MCPTT Session Identity 字段。Reason Code 的 0 是 Accepted，1 是 Busy，2 是 Not Accepted，其余值保留。仅凭一个 0，连它答的是 Connect 还是 Disconnect 都不能确定。这份确认不是 SIP ACK，也不是 Floor Ack；它不授予话权，更不证明用户开过口。[§8.3.3.8、表 8.3.3.8-1，印 179](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=180)；[§8.3.6、表 8.3.6-1，印 182](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=183)；[§9.2.2.4.5，印 196](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=197)

## 看 PF：本地“在用”和对端答复不是同一步

以受邀侧为例：PF 收到控制 MCPTT 功能（CF）的 SIP INVITE，要在自动应答模式下用一条原未在用的预建立会话承接来呼。PF 在本次呼叫的媒体面控制通道向受邀客户端发 Connect。它取该 INVITE 的 Contact 中的 SIP URI 填入 Connect 的 MCPTT Session Identity 字段内的**身份值**，置要求确认位，启动 T55，把 C55 初始化为 1；若尚未预留媒体通道资源，还要预留。**这条会话在 PF 一侧随即转为在用，不必等客户端答复。** 这里说的是 Connect 里的身份值，不是在规定 SIP ACK 发往哪里。[§9.3.2.3.3，印 198–199](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=199)

| 本次 Connect 所在的预建立会话在 PF 侧处于“在用”，随后发生什么？ | PF 的处理 |
| --- | --- |
| PF 收到客户端对本次 Connect 的 Accepted 确认 | 停 T55。如果未给 CF 的这份 INVITE 回过 SIP 200 OK，就回 200；已经回过，不因该确认再发一份。保持在用。 |
| PF 收到客户端对本次 Connect 的非 Accepted 确认，如 Busy 或 Not Accepted | 停 T55。必须向客户端发 Disconnect，其中 **MCPTT Session Identity 字段的完整内容**必须与原 Connect 相同，包括 Session Type 和 MCPTT Session Identity 值。即使身份 URI 相同，若 Session Type 从 prearranged 改成 chat，也不合此要求。[§8.3.3.3、表 8.3.3.3-1，印 176](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=177)。这份 Disconnect **宜**置要求确认位。启动 T56，将 C56 初始化为 1，向 CF 发呼叫释放指示，转入“正在释放呼叫”（Call releasing）。 |
| 未获确认，T55 到期，未到 C55 上限 | 在该呼叫的媒体面控制通道重发原 Connect，重启 T55，C55 加 1，保持在用。 |
| 未获确认，T55 到期次数达到 C55 上限 | 必须向 CF 发呼叫释放指示；**可以**释放本次呼叫占用、而预建立会话不需要的媒体资源。这条预建立会话在 PF 侧回到未在用。本条不要求向客户端发 Disconnect，也没有拆掉预建立会话。 |

客户端的发送记录和 PF 的接收记录是两件事。即使终端已发 Accepted，也不能据此认定 PF 已收到、停了 T55 或给 CF 回了 200；它发出的 Busy 同样不能单独证明 PF 已开始释放。PF 侧抓包没见确认，也不证明终端拒绝或 PF 已重试到限。客户端返回 Busy 或 Not Accepted 是协议结果，不等于用户亲手按了拒绝。判定到限要查本次 T55/C55 记录，不能从抓包窗口长度猜测秒数或次数。[§9.3.2.4.7，印 201](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=202)；[§§9.3.2.4.8–9，印 201–202](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=203)

## 看发起侧 PF：REFER 的响应与主叫 Connect 来自两件事

主叫已经有预建立会话，用 REFER 请求发起业务。对 PF 侧原未在用的会话，PF 收到 REFER 后按发起入口预留尚未预留的用户面资源，转为在用。对客户端侧原未在用的对应会话，客户端实际收到这份 REFER 的 SIP 2xx 后转为在用。这两个状态动作不能证明控制功能（CF）已接受另发的业务 INVITE。〔§9.3.2.3.2，印 198；§9.2.2.3.5，印 195〕

**再看发起侧 PF 是否实际收到 CF 对本次业务 INVITE 的 200 OK。** 收到这份响应时，已经在用的 PF 须经本次呼叫的媒体面控制传输通道向**发起呼叫的主叫客户端**发送 MCPC Connect，用来确认这次业务呼叫的建立。Connect 在网使用，走单播承载。身份值取这份 INVITE **200 响应**的 Contact，不取 REFER 的 200，也不取受邀侧收到的 INVITE 请求里的 Contact。前一份 SIP 响应先到，不是用它填身份的理由。〔§8.3.4，印 180–181；§9.3.2.4.10，印 202〕

| 抓到的字段 | 发起侧 Connect 怎样处理 |
| --- | --- |
| CF 的 INVITE 200 有含 `session-type` 的 MCPTT 信息体（`application/vnd.3gpp.mcptt-info+xml`） | 用该值对应的 Session Type。 |
| CF 的 INVITE 200 没有含 `session-type` 的这类信息体 | Session Type 写 `no session type`（0）。仍写从这份 200 的 Contact 取到的 SIP URI。不能因为业务已知是私呼就把类型补成 `private`，也不能删掉整个 MCPTT Session Identity 字段。 |
| CF 的 INVITE 200 有 `P-Answer-State` | 把其中 `answer-type` 对应到 Connect 的 Answer State。没有这个头时，此步骤不要求写 Answer State；若实际收到的 **Connect** 没有这个字段，则接收端按 `confirmed` 解读。这个缺省与 Session Type 取 0 无关，也不证明用户手动接听。 |
| CF 的 INVITE 200 有 `warn-code=399` 的 Warning | 按本步骤取 `warn-text` 填入 Connect 的 Warning Text，不把 SIP Warning 整行或数字 399 当作那段文本。 |

这次向主叫发的 Connect **宜**置 subtype 首位为 1（要求确认）；PF **须**启动 T55、将 C55 加 1，保持在用。条文没说把发起侧 C55 初始化为 1。上文受邀侧自动应答分支不同：那一侧收到的是 CF 的 INVITE **请求**，发送 Connect 时**须**置要求确认位，并把 C55 初始化为 1。不要因报文都叫 Connect 就把一边的规则套给另一边。

上述字段和计时取自[§9.3.2.4.10，印 202](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=203)、§8.3.3.3–.4（印 176–177）、§8.3.3.6（印 178）、[§8.3.4，印 180–181](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=181)，受邀侧对照 §9.3.2.3.3（印 198–199）。Connect 的发送、MCPC 确认、SIP ACK、话权许可和 RTP 到达不是同一事件。如果要查[普通私呼如何从 REFER 另发业务 INVITE](../calls/private-preestablished-origination.md)，读发起侧信令页；本段不规定 Contact 缺失、会话失败或其他 SIP 响应的处理。

## 另案是“我要重新加入组呼”，该查哪一页？

下面两个入口指**普通在网预安排组、客户端主动重入、不请求隐式话权**。先看这一次采用的会话方式，不是看终端名下有没有预建立会话。

- **这次通过已有预建立会话重入：**客户端向 PF 发对话外 REFER。PF 收到符合重入入口的请求，本地检查允许继续时，先答这份 REFER 的 200，再由 **PF 向 CF** 另发 INVITE。这与上文自动应答来呼的 **CF 向受邀侧 PF** 发 INVITE 方向相反。只凭 REFER 的 200 或旧 Contact，不能认定后续重入 INVITE 已发、已送达或被 CF 接纳。查[通过预建立会话重入组呼](../calls/preestablished-group-rejoin.md)。
- **这次采用按需会话主动重入：**客户端发起 initial INVITE，以待重入的业务会话身份为目标。查[普通按需组呼的主动重入与晚入](../calls/rejoin-late-entry.md)中的主动重入分支。这并非客户端发 REFER，也不是 CF 主动发来的晚入邀请。
- **方式未知：**“用户正在重入”、一条旧 Contact 或终端另有一条预建立会话，都不能决定这一次用哪个流程。先找本次客户端发出的请求、请求指向的身份及所选会话；还原不了，就保留“方式未知”，不要先记为 REFER 或认定 CF 已接纳。

如果要判**普通在网且采用话权控制的客户端**能否讲话，或排队后的授予是否还需用户确认，读[普通在网话权](on-network-floor-client.md)。MCPC Accepted 本身不是话权许可；该话权页不适用于无话权控制的私呼或双话权等特殊情形。

如果要查**预建立会话本身的建立、无关联业务会话时的修改，或无业务使用时的释放**，读[预建立会话生命周期](../calls/preestablished-session-lifecycle.md)。还有业务在用时，不能把空闲释放程序套过来；结束一次业务呼叫也不能代替容器释放的证据。

若这通呼叫已建立，后来用 Disconnect 结束它，见[媒体面释放时确认、重试与会话保留](preestablished-release-outcome.md)。
