# MC 用户发起互通紧急告警：发起端、IWF 和成员分别回哪一笔？

**server 回给发起端的步骤 4，确认原步骤 2；IWF 的 6 回 server 发出的 5；成员的 9 回各自收到的 7。** NOTE 3 允许 server 向 IWF 发 5 和向成员发 7 任一先做。发起端的位置不可用时，server 在发给 IWF 的 5 中必须标明。查规范不需要抓包。[TS 23.283 V19.5.0 §10.6.4.2 图、步骤和 NOTE 3，印刷页 141–142](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=142)。

## 发起者、所指组和 IWF 权限分开核对

MC 用户发起新告警，不是取消。组先前已在组管理服务器定义，图中两个 MC service client 已归属。IWF 已接入并获准互通，掌握互通组信息并在 IWF 配置组、用户身份映射；组可定义在 MC 或 LMR。NOTE 1 对经过 IWF 的跨 MC/LMR 信令做身份转换及协议翻译，不把这项处理套到 MC 系统内部。[前提和 NOTE 1，印刷页 140](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=141)。

步骤 2 由 client 1 向 MC service server 发告警。步骤 3 由 server 解析组 ID、确定成员归属、判断是否通知 IWF。本场景有已归属成员的本属在 IWF，所以 **IWF 必须参与**。知道某成员已归属不等于核到其本属。server 还得检查**发警者的 MC service 用户 ID 对所指明组的告警权限**；IWF 接入、互通授权、映射或组存在不代替这项检查。本节没给拒绝码或完整异常流程。[步骤 1–4，印刷页 141](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=142)。

## 三条消息腿分别配对

| 步骤 | 看什么 |
| --- | --- |
| **2 → 4：发起端** | server 回给发起的 client 1，确认其原告警，不是 IWF 或成员的回包。不能把这一笔当作 client 1 已收到、其自身状态已改变或全组已通知的证据。 |
| **5 → 6：IWF** | server 向 IWF 发 5。拿不到发起端 client 1 的位置，要明确标明不可用；不拿其他成员的位置代替。IWF 实际代理该组 LMR 用户归属时只发一条；IWF 已逐人送其 LMR 用户归属时，server **经 IWF 向每名已归属的 LMR 组成员**发请求。按实际归属选，不按 MC 人数、静态名册或图的一根箭头定数；本节没规定混合或未知的归属方式。IWF 的 6 确认相应 5。正文把 6 写作 `IWF service emergency alert response`，图和表使用 `IWF emergency alert response`；保留名称差异，不据此增加一笔回包。 |
| **7 → 8 → 9：已归属 MC 成员** | server 向各已归属成员的 MC service client 发 7，步骤 8 告知用户告警，实际收到相应 7 的成员客户端回 9。图在这里画 client 2，正文说各已归属成员，不能据图认定只一人，或补出专给发起端的额外成员请求。步骤 7 要求位置信息、MC service ID、MC service 组 ID 和任务关键组织名称。组 ID 取用户所选组或指定紧急组，按组配置。不从成员侧的信息要求反推上游已有真实位置；本节没有给位置不可用的下游表示。 |

NOTE 3 说 **5 和 7 任一可先发**；成员请求可早于 IWF 请求，不必先收 IWF 的 6。这个相对顺序规则不把 4 写成由 IWF 或成员应答触发。本支的 9 在图中是实线，正文没写组播时省略，不借用 [告警取消](emergency-alert-cancel-mc-origin.md) 的组播 ACK 例外。[图与步骤 2–9、NOTE 3，印刷页 141–142](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=142)。

IWF 请求表 10.6.1.7-1 的发警者 **MCPTT ID** 和**关联组 ID**必带，功能别名、组织名称和 `Location` 标 O。表没有单列不可用指示的字段；`Location` 的可选性不消除步骤 5 的缺位置指示要求，不能把静默省略视为已指示，也不猜字段编码。应答表 10.6.1.8-1 只列两项必带 ID，没有位置、成员清单或 `Result`。通用表描述双向信息流，本支的方向仍按图中 5/6。[两表，印刷页 119](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=120)；[步骤 5，印刷页 141](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=142)。

查现网分别配 **2/4、IWF 5/6、各端 7/9**。同组同发警者可对应多个逐人请求；不能靠两个 ID 配某个 6。实际发出的匹配回复可佐证原请求到达该应答端，不证明反方向回执已送达，更不证明成员实际通知、用户或组状态、位置真实性或媒体。查单跳信令不需要媒体证据。[步骤 2–9，印刷页 141](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=142)。

## 告警、紧急组状态和隐式归属

- **告警不是建呼。** NOTE 2 说只发告警、没有另请求发起紧急呼叫，不把组置为进行中紧急状态；另有呼叫请求也不证明已建呼。NOTE 4 对组随后按紧急呼叫建立的前提，是实际有进行中紧急状态。NOTE 5 不会因发告警把组内其他 UE 置为紧急状态。[NOTE 2、4–5，印刷页 141–142](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=143)。
- **步骤 10 查的是 client 1 对紧急组的归属。** 未归属时由 MC service server 隐式归属 client 1。前提写两个 client 已归属该 MC service 组，步骤 10 写是否已归属紧急组；要核所指组和实际归属，不能默认同组或必不同组，不能据前提重复归属。NOTE 3 说 10 可在 3 后做，没写必须等 9 或最迟在 9 后立即。不能套 [LMR 发起告警 §10.6.4.1](emergency-alert-init-lmr-origin.md) 的组定义限制、代谁归属或 NOTE 4 的时限。[前提与步骤 10，印刷页 140、142](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=143)。

**换入口：**LMR 用户发告警读 [§10.6.4.1](emergency-alert-init-lmr-origin.md)，它是 IWF 向 server 发 2、server 回 IWF 4；MC 用户发的是[告警取消](emergency-alert-cancel-mc-origin.md)读 §10.6.5.2，其 NOTE 3 放开 3/4，不是这里的 5/7。[原生 MCPTT 告警](../emergency/standalone-group-alert.md)另查 Stage 3。若问 MCPTT 用户发起的紧急组呼，按组定义分别读 [MCPTT 定义组 §10.6.2.2.2](emergency-group-setup-mcptt-to-mcptt.md) 或 [LMR 定义组 §10.6.2.2.4](emergency-group-setup-mcptt-to-lmr.md)。只问告警时，即使另请求建呼，仍查告警这笔。本页是通用互通信息流，不定义具体 SIP、位置编码或设备操作。[对照 §§10.6.4.1、10.6.5.2，印刷页 139–140、143–144](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=140)。
