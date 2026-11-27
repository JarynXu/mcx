# IWF 组呼的 join、leave 和 release：用户 ID 指谁？

**先认这条信息流，再读用户 ID。** 同一个组 ID 加一个用户 ID，可能出现在 join 应答、leave 的两条信息流或 release 应答里。两个值相同，不代表它们是同一条消息，也不表示用户已加入、离开或结束了呼叫。

这里读 **TS 23.283 V19.5.0，Rel‑19 Stage 2**，只看 **IWF 和 MCPTT server 之间的 IWF‑1**。下列六条信息流都写了两个方向；不能只用 IWF→server 或 server→IWF 判请求／应答。表里的 M 是必带，O 是可选，但还要读对应的 NOTE。查规范或一条已识别的消息，不用先找到对向报文。[接口范围 §10.3.2.1，印刷页 35（PDF 第 36 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=36)。

| 已识别的信息流 | MCPTT ID 指谁？ | 这张表还有什么？ |
| --- | --- | --- |
| **Group join request（表 .8‑1）** | **M，请求发起者**。功能别名 O，指 calling party。 | MCPTT group ID M，指本次请求通信的组；发起者媒体参数的 SDP offer M。隐式话权请求 O，仅在发起客户端请求话权时才包含。 |
| **Group join response（表 .9‑1）** | **M，仍是请求发起者**，不是应答方自己的 ID。 | MCPTT group ID M，仍指请求通信的组；选定媒体参数的 SDP answer M。 |
| **Group call leave request／response（表 .10‑1／.11‑1）** | **M，正在离开的组成员**，不是必然发送消息的用户。 | 两张表同样只列 M 的 MCPTT ID 与 MCPTT group ID；后者是该用户要退出的组。两张表没有单独的 Result。 |
| **Group call release request（非广播，表 .12‑1）** | **O，发起释放的组成员**。NOTE 写明 server 发起释放时不带此项，例如超时。 | MCPTT group ID M，指释放呼叫所在组；Release reason O。缺用户 ID 不能倒推一定是 server 发起，缺原因不等于没有原因。 |
| **Group call release response（表 .13‑1）** | **M，目标组成员**，不按请求里的发起者回填。 | MCPTT group ID M，指释放呼叫所在组。表没列 Release reason 或 Result；不能把请求的原因或用户 ID 可选规则搬过来。 |

[Join 字段和 NOTE，§10.3.2.8–.9，印刷页 37–38（PDF 第 38–39 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=38)；[Leave 与 release 字段和 NOTE，§10.3.2.10–.13，印刷页 38–39（PDF 第 39–40 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=39)。

### 怎样读代理身份、话权和实际结果？

- **Join 的代理 ID。** 两张 join 表的 NOTE 都说，IWF 在代表 LMR 系统给自己作组归属时，有一个配置好的 MCPTT ID 可用。这个 ID 仍在请求发起者的位置，不因应答方向改成另一个设备或用户。只看某个 ID 值，不能断定 IWF 采用了这种方式、拿到了具体 LMR 用户身份，或归属已生效。不要照搬初始建呼：表 .2‑1 在 LMR 发起且未提供主叫身份时允许预留 ID，表 .3‑1 的应答 ID 指目标成员，不是 join 应答的请求发起者。[§10.3.2.2–.3，印刷页 35–36（PDF 第 36–37 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=36)。
- **区分通用表和具体步骤。** 对照表 .8‑1，已知合规的 join 请求带隐式话权请求，就可读出发起客户端请求了话权；通用表的 O 与 NOTE 2 不给反向条件。实际若是 **IWF 进入进行中的、MCPTT 定义的 chat 组呼**，§10.3.5.9 步骤 1 另写：有发送请求时，join 带隐式话权请求；带此指示时**可**带位置。表 .8‑1 未列 Location，不用这一缺项否定该步骤，也不为所有 IWF join 加上位置。隐式申请不是已授话权。[§10.3.5.9 步骤 1，印刷页 69（PDF 第 70 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=70)。
- **离开与释放不是一回事。** Leave 的组 ID 指成员所离开的组；这里的非广播 group call release 的组 ID 指释放呼叫所在的组。释放作用于整通呼叫，但组 ID 不标识具体通话或释放尝试。读真实记录，先确认消息类型、所在端、该次呼叫或动作。只有将一对请求与应答归为同一次时，才核各自对应的证据。相同两个 ID 或缺某个字段不能决定它是 leave、release、请求还是应答；也不能证明消息到了另一端，或参加状态、媒体和话权资源已变化。
- **对照 release 的可选身份。** 只看到 server 发出一条请求不等于它发起释放。若已确认 .12 请求由 server 发起，就按 NOTE 省略发起成员 ID；反过来，只有在已经确认请求符合此表且字段确实存在时，才能据此排除 NOTE 所述的 server 发起。不能靠未经核验的字段给实况定性。另一次 .13 应答仍用必带的目标成员 ID。例如同一组里 A 发起释放，而某条 IWF‑1 应答的目标成员是 B；不要把应答的 B 当作发起者，也不要据此说 B 的终端已收到。

如果要查**什么动作使人加入、离开或整通释放**，按场景读 [chat 加入](chat-entry.md)、[取消归属后的用户退出](deaffiliation-exit.md)、[预安排组呼释放](group-call-release.md) 或 [chat 组呼释放](chat-release.md)。后者在 §10.3.5.4 的步骤 1／5 和 §10.3.5.5 的步骤 2／5 也用 IWF group call release request／response；问这条已识别的 IWF‑1 消息字段仍查 .12／.13。两端的确认及是否实际释放仍分别看流程。[§10.3.5.4–.5，印刷页 66–67（PDF 第 67–68 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=67)。[初始组呼请求](group-call-request.md)、[广播组呼释放](group-broadcast-release.md) 和 [临时 ad hoc 组呼释放](adhoc-group-release.md) 都有各自信息流，不套这一表。§10.3.2.1 对 IWF‑1 之外的参考点仅指向 TS 23.379；本页不定义 SIP、状态码、超时值或实际报文字段。
