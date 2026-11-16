# EPS 信令承载：接入条件与 QoS 边界

适用：Release 19，TS23.280 **V19.9.0**，Stage2。此版本独立核对，不替代库内其他版本。

在 EPS 中，初始附着的 PDN 若不是 MC services APN，UE 需在用户认证前另建对应 PDN；SIP 注册请求也可触发建立（§5.2.7.2.1）。

适用 §5.2.7.2 时，SIP-1 信令用 QCI 69，HTTP-1 用 QCI 8 或更好；若 HTTP-1 未使用 QCI 8，应谨慎避免合并流量影响高优先级信令或媒体承载（原文为 should，而非 shall）。这里的“更好”不能直接换算成 QCI 数字大小。

另有明确分支：SIP core 属于 PLMN 运营商且复用 IMS APN 时，运营商与 MC 服务提供方须约定采用上述 QoS 规则还是 GSMA IR.92/IR.88 的规则（§5.2.7.0 注）。不能把 QCI 69 无条件推广到所有部署，更不能当作 5GS 的 5QI 映射。

## 依据与延伸

[ETSI 正式文本](https://www.etsi.org/deliver/etsi_ts/123200_123299/123280/19.09.00_60/ts_123280v190900p.pdf)；精确条款与适用条件见[知识记录](eps-signalling.json)。未核完整引用规范或实现。

- [主系统认证及 SIP 注册](../identity/primary-registration.md)
- [Rx 重试边界（未复核原文的整理说明）](rx-retry.md)

另见[5GS QoS 模型（独立于 EPS）](5gs-qos-model.md)。
