# 归属信息流：服务类型与逐组结果

TS23.283 V19.5.0，Release 19，Stage 2。

TS23.283 IWF-1 Stage 2 信息流；不是线级编码。

## 归属或取消归属请求

必需信息含 MC service ID、至少一个组 ID 的列表和服务类型；IWF 代理时使用配置的 MC service ID。 [§10.1.1.2, 10.1.1.4](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 归属或取消归属响应

必需信息含发起者 ID、组列表及每个组的结果，不能用收到一个响应替代逐组结果判断。 [§10.1.1.3, 10.1.1.5](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

LMR 内部归属和 TS23.280 显隐式基础机制未核验。这里不是完整失败状态机或 Stage 3 编码。

[晚加入](late-entry.md) · [取消归属后的呼叫退出](deaffiliation-exit.md) · [配置获取](group-configuration.md) · [结构化知识](affiliation-results.json)

按需补充：[代理或个人身份](affiliation-representation.md)、[MC定义组方向](affiliation-mc-group.md)、[LMR定义组方向](affiliation-lmr-group.md)、[逐组结果](affiliation-results.md)。无需全部加载。
