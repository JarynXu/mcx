# MC 定义组：归属校验与取消范围

TS23.283 V19.5.0，Release 19，Stage 2。

IWF 已配置 MC/LMR 组及用户身份映射。

## 组定义在 MC，IWF 已连接且获互通授权，拥有组信息

IWF 请求归属；MC server 缺缓存时取组策略，检查组未禁用及给定 ID 的归属授权，按策略/订阅处理并按个人或代理模式存状态，更新 GMS 后响应。 [§10.1.2.2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 先前已执行 §10.1.2.2 归属；IWF 请求取消

预期逐用户取消时，server 根据组策略与订阅可取消成员并可存状态；不预期逐用户取消时，该信令取消 IWF、从而取消整个 LMR 系统对此组的归属。随后更新 GMS 并响应。 [§10.1.2.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

LMR 内部归属和 TS23.280 显隐式基础机制未核验。这里不是完整失败状态机或 Stage 3 编码。

[晚加入](late-entry.md) · [取消归属后的呼叫退出](deaffiliation-exit.md) · [配置获取](group-configuration.md) · [结构化知识](affiliation-mc-group.json)

按需补充：[代理或个人身份](affiliation-representation.md)、[MC定义组方向](affiliation-mc-group.md)、[LMR定义组方向](affiliation-lmr-group.md)、[逐组结果](affiliation-results.md)。无需全部加载。

本页处理归属状态，不是完整呼叫清理；对应用户退出正在进行的呼叫见 [call leave](deaffiliation-exit.md)。代理取消归属范围不能直接等同单用户 leave 或整组 call release。
