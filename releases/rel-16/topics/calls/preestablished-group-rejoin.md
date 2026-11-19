# 预建立组呼重入：REFER 已回 200，怎么查控制侧是否接纳？

普通在网 MCPTT 预安排组重入时，客户端若使用已有的预建立会话，先向参与功能（PF）发 **REFER**。PF 在本地检查允许继续后，先向客户端发这个 REFER 的最终 **200 OK**，再生成一条新的 **INVITE** 发往控制侧。决定能否重入原组呼的是第二条请求。只见客户端收到 REFER 的 200，可以记“PF 已成功应答 REFER”，不能记“控制功能（CF）已接纳重入”。仅凭这份响应，连第二条请求是否已发出都不能确认。[3GPP TS 24.379 V16.14.0，Release 16，Stage 3，§10.1.1.3.5.2，印 239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)；[§10.1.1.3.1.2 步骤 13–19，印 234–235](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=235)

## 同一通组呼，三处分别查哪个 URI？

设客户端原来参加组 G 的一通呼叫。它现在有预建立会话 P，先前从 PF 拿到那通**业务会话**的身份 S；PF 保存了 S 与控制侧业务会话身份 T 的对应关系。P 用于找到预建立会话，S 和 T 从两侧标识要回去的那通呼叫。字母只标职责，不规定 URI 格式，也不能从一个 URI 的字符串推算另一个。

| 查哪条信令 | 应核对什么 |
| --- | --- |
| 客户端 → PF：REFER 的 Request-URI | **P**，即预建立会话身份。用户要求重入进行中的组呼，或客户端因回到覆盖区而触发重入时，客户端生成的是**对话外** REFER。使用已有预建立会话不等于在原对话内发请求。 |
| 同一 REFER：重入专条描述的 Refer-To | **S**，即客户端已知的待重入业务会话身份。该条还要求 SIP URI 的 headers 部分标明 `application/vnd.3gpp.mcptt-info+xml`，其 `body` 参数内的 `<mcpttinfo>/<mcptt-Params>/<session-type>` 为 `prearranged`。不要把 G 或 P 当作 S。这个描述与通用程序的回指见下文。 |
| PF → 控制侧：新 INVITE 的 Request-URI | **T**。PF 已按下述入口识别这份重入 REFER，且前序检查允许继续时，用与 S 对应的已映射业务会话 URI 填步骤 16。不是把 REFER 的 Request-URI 原样转发，也不是按组 G 做普通初建时使用的控制功能公共服务身份（PSI）。 |

P 来自重入条款调用的[§10.1.1.2.2.1，印 228](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=229)及[§10.1.2.2.2.1 步骤 1，印 273](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=274)；S 见[§10.1.1.2.4.2，印 229](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=230)，T 见[§10.1.1.3.5.2，印 239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)。

**什么样的来话才是这里的 REFER？** 在发端，服务呼叫会话控制功能（S-CSCF）处理初始过滤准则（iFC），把 REFER 路由到 PF；Request-URI 须是标识该 PF 上预建立会话 P 的公共服务身份。这个路由和寻址条件先界定“预建立会话 REFER”这一类输入。在此基础上，PF 再按重入条款核对 Refer-To 的 URI 中 `body` 的 MCPTT MIME 类型和 `prearranged` 会话类型。即便正文一模一样，Request-URI 实际指向别的业务身份，也不能按这条重入程序推出 PF 应答 200 或必须向 T 发 INVITE。[§6.3.1.2 的请求分类，印 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=79)；[§10.1.1.3.5.2 的入站条件，印 239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)

**旧 Contact 是 P、S 还是 T？** 先查哪笔建会和采集方向。若是 PF 对**预建立会话建立**的 INVITE 发给客户端的 200，Contact 里是 PF 为预建立会话分配的 **P**。若是**业务组呼建立**，在这里所述的直接 CF/PF 链上，CF 建会最终响应给 PF 的 Contact 含 **T**，PF 朝客户端发的业务建会 Contact 则含 PF 分配的 **S**。所以仅有“建会 Contact”一行，三者都不能认定。[§8.2.2 步骤 8、9a、11，印 163](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=164)；[§4.5，印 38–39](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=39)

业务会话身份是服务器分配的 GRUU 形式 SIP URI。PF 维护 S 到控制侧 T 的映射；客户端**可以**缓存它拿到的业务身份 S。匹配了业务建会和采集方向的 Contact 能说明当时哪一侧给了哪个身份，但不能证明今天映射仍有效、原呼叫还在或本次已获准重入。

## 先分清哪一侧回了什么

- **在 PF 就停了。** 若已查到主叫公共身份没有有效的 MCPTT ID 绑定，PF 对 REFER 回 **404** 并停止，Warning 的**文本**以 MCPTT 码 **141** 开头；若已取到组身份却无法识别组的控制功能，PF 也对 REFER 回 **404** 并停止，文本以 **142** 开头。诊断时先看 SIP 状态码 404，再读 Warning 文本开头的三位业务码。不要拿 141/142 去匹配 Warning 头开头的 SIP 警告码：例如首码是 399、文本以 141 开头的记录，仍应按绑定问题读。不应把这两种本地拒绝记作“CF 找不到原呼叫”。[§4.4.1–2 及表 4.4.2-1，印 33–34](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[§10.1.1.3.1.2 步骤 2–3、9–10，印 233–234](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=234)
- **PF 已发 REFER 200。** 接着查 PF 出站是否有目标为 T 的新 INVITE，再查 CF 对这条 INVITE 的最终响应。只见 PF 收到该 INVITE 的临时响应，不表示已接纳；按这条预建立程序，PF 丢弃临时响应，不转给客户端。反过来，客户端没见到临时响应也不能判定 INVITE 没发。[§10.1.1.3.1.2 步骤 13–19 及临时响应处理，印 234–235](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=236)
- **CF 收到指向 T 的 INVITE。** CF 在步骤 1 若资源不足、无法处理，或有拥塞风险，可以先对 **INVITE** 回 **500**，也可以附 Retry-After；这并不证明 T 有效或无效。若继续到步骤 2 并查明 T 所指原组呼不存在，才须对 **INVITE** 回 **404**。这与先前 PF 对 **REFER** 回 200 完全相容。若查到原组呼仍在，CF 也要另查媒体和所需标记、加入许可、归属、容量等条件。相应检查通过后，CF 才按成功路径生成带 SDP answer 的 200，完成规定的媒体面处理后发出这个 **INVITE 200**。它可以作为控制侧接纳这次重入的依据；它不是客户端收到语音或已经取得发言权的证据。PF 对该 INVITE 的 200 与 4xx/5xx/6xx 也分别处理，不能把下游错误回填成先前 REFER 的结果。[§10.1.1.4.5.1，印 252–253](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=253)；[§10.1.1.3.1.2 的 INVITE 响应处理，印 236](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=237)

## 为什么不能据此拼一份 REFER，或抄历史 Contact 写 ACK？

固定版保留了两种写法。通用客户端程序明确写 **Refer-To 的 `cid` 指向 `application/resource-lists`，正文的 `entry` 含 `uri`**；普通预安排组初建用组身份 G。重入专条沿用这套程序，却在说明通用步骤 3 时直接写 Refer-To 含待重入会话身份 S 及上述 `body`。PF 重入条款的输入须是前述发端 iFC 路由至 PF、Request-URI 标识该 PF 上预建立会话的 REFER，且它的 Refer-To 含所述 MCPTT 正文、`session-type=prearranged`。条款调用通用程序，点名改的是**出站步骤 16**。通用 PF 程序开头仍列出：Refer-To 中的 `cid` 指向含组 `entry` URI 的清单，该 URI 的 `body` 含指定的预安排组信息，请求的 Content-ID 与 `cid` 对应。步骤 9、10 仍据组身份识别控制方，步骤 17 仍从组 `entry` 取 G 填出站 INVITE 正文的 `mcptt-request-uri`。**G 是组，T 是会话**；不能以重入替换了请求目标为由，顺手把正文组身份也改成 T。[§10.1.1.2.2.1，印 228](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=229)；[§10.1.2.2.2.1 步骤 2–3，印 273–274](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=274)；[§10.1.1.3.1.2，印 233–235](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=234)；[重入专条，印 229](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=230)、[印 239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)

这些回指足以核对 P、S、T 的职责和两个事务的先后，不足以从中裁定唯一的线上封装。既不能只见一个会话 URI 就宣布组身份检查可以跳过，也不能把一份只有通用 `cid` 和组条目的初建请求自动认成重入。要核现场 ACK，先找**要确认的那条 INVITE、它的最终响应及对应的对话和路由信息**。只有先前建会的 Contact 或本次 REFER 200，不能还原这条 INVITE 的实际 ACK、Route、代理下一跳或 NAT 可达性。

本页限[在网普通预安排组的范围，§10.0/10.1/10.1.1，印 219–220](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=221)，且**已有预建立会话、不请求隐式话权**；不讨论广播、紧急、危急或多系统逐跳转发。客户端若发起的是 initial INVITE 而非 REFER，请转[按需重入与服务器晚入](rejoin-late-entry.md)。要查的是 P 如何建立、何时能拆，见[预建立会话生命周期](preestablished-session-lifecycle.md)。两篇解释不同程序，不是今天这个 REFER 之后的下一步。
