# LMR 按条件发起互通 ad hoc 组呼：谁选人，IWF 收到哪一步？

**IWF 代 LMR 用户发请求；MCPTT server 按请求的条件确定邀请名单。** 这里是 TS 23.283 V19.5.0、Rel‑19 Stage 2 §10.17.3.2。IWF 在 MCPTT 侧按一个 MCPTT client 行事。如果实际主叫是 [MCPTT 用户且按条件选人](adhoc-group-criteria-mcptt-origin.md)，查 §10.17.3.1；MCPTT 主叫给出显式名单查 §10.17.3.5，已建呼释放查 §10.17.3.3/.4。首次请求、选人输入比后续是否出现 IWF 更能区分分支。[§10.17.3.2 前提，印刷页 186（PDF 第 187 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=187)；[§10.17.3.5 显式名单，印刷页 189–190（PDF 第 190–191 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=190)。

## IWF 发起，server 验权和选人

LMR 用户须有发起 ad hoc 组呼的权限，并希望邀请符合条件的 MCPTT 用户；该流程涉及 MCPTT 和 LMR 用户。IWF 已配好两系统的组和用户 ID 映射，转换经过它的两系统间信令的身份和协议。图中 IWF 在 Step 1 向 server 发带条件的建呼请求；server 在 2 核本次授权、在 3 向 IWF 返回 request return、在 4 按 Step 1 条件确定邀请名单。映射不是这次授权的凭据。Step 4 也不证明某人已收到邀请；NOTE 1 把 LMR 用户实际如何确定和邀请留在本规范范围外。[图 10.17.3.2-1，印刷页 187（PDF 第 188 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=188)。

## 同为 server → IWF，先看是 3、8 还是 9

| 步骤 | 图上的消息 | 能读到哪一步 |
| --- | --- | --- |
| **3** | IWF ad hoc group call request return | 对首请求的返回。不要拿它当 Step 8 的建呼应答。 |
| **8** | IWF ad hoc group call response | 本次 IWF 建呼请求的应答。Result 属于此请求，不是逐被叫结果或实收名单。 |
| **9** | IWF ad hoc group call notify（虚线） | 另一个通知。§10.17.3.2 不单独规定它的触发、名单或完整载荷。不要从虚线自行裁定必发或可省，也不要把 §10.17.3.1 Step 11 当作这里的规则。 |

[图 10.17.3.2-1，印刷页 187（PDF 第 188 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=188)。只有 server 端发件记录，能判断它发出了哪条消息；IWF 是否实收，分别找与这次尝试及相应步骤匹配的接收证据。IWF 收到 3 或 9，仍不能替代 8；没看到 8 的接收记录也不能判失败。IWF 实际收到 8 success，也不说明它已通知 LMR 用户，或某个 LMR 终端已加入、已听到音频。

Step 1 的 IWF-1 请求表要求主叫 MCPTT ID、本次 ad hoc group ID、SDP offer。表的被邀者 ID、预配置组 ID、criteria 另列可选；条件可由细节、标签或两者表达。字段 O 不取消本分支由 server 按 Step 1 条件选人的前提；只有主叫位置或组 ID 不能补成选人条件。预配置组 ID 也不替代本次 ad hoc group ID。Step 8 应答表要求主叫 MCPTT ID、本次 ad hoc group ID 和 Result（success 或 failure）。SDP answer 栏为 O，说明写在 Result 成功时出现；不拿 SDP answer 替 Result，也不补写没看到的 answer。§10.17.2.3 的引导句写 request；该节标题、表名与图的 Step 8 是 response。两张表只用于这两条建呼请求/应答。不在这里给 Step 3、9 加字段，也不猜组 ID 分配与寿命。[表 10.17.2.2-1 / 10.17.2.3-1，印刷页 182–183（PDF 第 183–184 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=183)。

## 被叫回应与媒体分别确认

图示 server 向被叫 2、3 发 5a/5b，两端各提示组呼（6a/6b），再回 server（7a/7b）。图把它们画在 8/9 前，不足以推出 Step 8 必须等待每个被邀用户，或无需任何响应。也不把 §10.17.3.1 NOTE 3 用于本支：那一支 Step 8 是 server 发的**请求**，本支 Step 8 是 server 发的**应答**。显式名单 §10.17.3.5 的逐 LMR 用户发送和指定 MCPTT 用户应答超时也不移过来。

在记录里分别确认被叫发送、server 实收、IWF 对应消息实收、真实成员加入。图的 Step 10 另建媒体面和话权控制资源；Step 8 success 或 Step 9 通知不能替代媒体、已听见或获话权的证据。§10.17.3.2 图后指 TS 23.379 [7] §10.19.3.1.1，IWF 扮 MCPTT client；这不是 §10.17.3.1 分步引用的 §10.19.3.1.3。§2 [7] 未标修订，按同 Release 的最新版本查阅；本页未核被引正文。§10.17.2.1 也把 IWF-1 之外的参考点交给 TS 23.379，不能由这张图补齐汇总/超时规则、线级 SIP 或 LMR 本地处理。[§10.17.3.2 图与引用，印刷页 187（PDF 第 188 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=188)；[§2 [7]，印刷页 11（PDF 第 12 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=12)；[§10.17.2.1，印刷页 181（PDF 第 182 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=182)。
