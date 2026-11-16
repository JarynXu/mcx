# IWF 归属表示：逐用户与代理可以并存

TS23.283 V19.5.0，Release 19，Stage 2。

组定义在 MCPTT 系统，适用 TS23.283 §10.1.2.1。

## LMR 侧报告归属

可逐用户报告，也可在首成员归属时由 IWF 代理归属、末成员取消时代理取消，中间不另发归属信令；两种方式可以对不同成员同时使用。 [§10.1.2.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## IWF 配置为代理归属

组成员表须配置 IWF 的 MCPTT ID 并识别其代理能力；IWF 归属后，其关联 LMR 用户被视为归属，无需预列全部用户；不允许向未配置该 IWF ID 的组代理归属。 [§10.1.2.1 a–d, g](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 处理关联 LMR 用户请求

LMR 用户自身请求使用转换后的个人 MCPTT ID；另有 IWF 代表组内用户、以 IWF ID 发请求的情形，二者不得混同。代理归属后不因呼叫请求再生成重复归属。IWF 未归属时，该用户呼叫请求只有在个人 ID 列于组表且已归属时才可接纳。 [§10.1.2.1 d–f, h](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

LMR 内部归属和 TS23.280 显隐式基础机制未核验。这里不是完整失败状态机或 Stage 3 编码。

[晚加入](late-entry.md) · [取消归属后的呼叫退出](deaffiliation-exit.md) · [配置获取](group-configuration.md) · [结构化知识](affiliation-representation.json)

按需补充：[代理或个人身份](affiliation-representation.md)、[MC定义组方向](affiliation-mc-group.md)、[LMR定义组方向](affiliation-lmr-group.md)、[逐组结果](affiliation-results.md)。无需全部加载。
