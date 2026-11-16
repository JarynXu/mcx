# LMR 定义组：显式与隐式归属通知

TS23.283 V19.5.0，Release 19，Stage 2。

组定义在 LMR，IWF 已配置 MC/LMR 组及用户身份映射。

## IWF 已连接且获与 MC 系统互通授权

客户端请求经 server 转 IWF；成功响应后 server 存状态并回复客户端。IWF 可因组 ID 未知或无 LMR 映射而拒绝。隐式归属仅执行跨侧请求、响应及存状态步骤，仍通知 IWF。 [§10.1.2.4](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 先前已执行 §10.1.2.4 归属

显式请求携发起 ID 与组列表；server 按订阅/策略检查归属及互通组，经 IWF 请求/响应后，仅在用户获取消授权时移除状态。隐式取消只执行跨侧请求/响应及有条件移除状态。 [§10.1.2.5](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

LMR 内部归属和 TS23.280 显隐式基础机制未核验。这里不是完整失败状态机或 Stage 3 编码。

[晚加入](late-entry.md) · [取消归属后的呼叫退出](deaffiliation-exit.md) · [配置获取](group-configuration.md) · [结构化知识](affiliation-lmr-group.json)

按需补充：[代理或个人身份](affiliation-representation.md)、[MC定义组方向](affiliation-mc-group.md)、[LMR定义组方向](affiliation-lmr-group.md)、[逐组结果](affiliation-results.md)。无需全部加载。
