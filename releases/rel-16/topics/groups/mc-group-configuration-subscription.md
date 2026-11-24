# MC 定义组：IWF 怎样订阅配置，主 MC GMS 何时发更新？

仅凭 `IWF group information subscribe request` 或 `IWF group information notify request` 的消息名，不能判断发送方。先核对组定义在哪一侧。本页说的是 **MC 定义组**：IWF 向该组的主 MC 系统的组管理服务器（主 MC GMS）订阅；IWF 已订阅且主 MC GMS 已收到并保存该组的新配置时，由主 MC GMS 向 IWF 发通知。

## IWF 向主 MC GMS 订阅

§10.2.3.6 有三个前提：

1. MC 业务组定义在其 MC 系统。
2. 至少一名组成员定义在 LMR 系统。
3. IWF 已从**该组的主 MC GMS** 收到该组信息。

IWF 向该主 MC GMS 发送 `IWF group information subscribe request`，订阅保存在该 GMS 的组配置。主 MC GMS 向 IWF 返回 `IWF group information subscribe response`，报告订阅请求成功或失败。收到过组信息不是订阅成功的证据；本条没有指定获得先前组信息的唯一流程。

依据：TS 23.283 V16.8.0，[§10.2.3.6 条首和三个前提，印刷页 30](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=31)；[图 10.2.3.6-1 与步骤 1–2，印刷页 31](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=32)。

## 主 MC GMS 向已订阅的 IWF 通知

§10.2.3.7 有两个前提：

1. IWF 已在该组的主 MC GMS 订阅该组配置。
2. 该主 MC GMS 已**收到并保存**该组的新配置。

这时主 MC GMS 向 IWF 发送 `IWF group information notify request`。IWF 向该主 MC GMS 返回 `IWF group information notify response`，报告本次通知成功或失败。**只收到新配置、还没有保存**，不满足上述第二项；不能按本条认定已到通知条件。依据：[§10.2.3.7、图 10.2.3.7-1 与步骤 1–2，印刷页 31](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=32)。

订阅和通知各有自己的成败响应。主 MC GMS 的发送记录不代证 IWF 实收。通知响应不证明 IWF 已保存配置、终端已收到配置，也不能据此判断订阅已终止、组归属已变更或通话已经结束。这两节没有规定刷新间隔、重试或具体线上协议。

若组定义在 **LMR 系统**，同名请求的方向相反，查 [LMR 定义组的订阅和通知](lmr-group-configuration-subscription.md) 的前提。仅知道消息标签时，先确认定义方，再选对应流程。
