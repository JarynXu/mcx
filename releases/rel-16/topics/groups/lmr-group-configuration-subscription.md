# LMR 定义组：MC GMS 怎样订阅配置，IWF 何时通知更新？

订阅和通知各有一次请求与响应。订阅由 MC 系统的组管理服务器（GMS）发起。已有订阅且 IWF 有该组的新信息时，由 IWF 另发一次通知。

## MC GMS 向 IWF 订阅

§10.2.3.8 有三个前提：组定义在 **LMR 系统**；至少一名组成员定义在 **MC 系统**；MC GMS **已从 IWF 收到该组信息**。

1. MC GMS → IWF：发送 `IWF group information subscribe request`，订阅保存在 IWF 的该组配置。
2. IWF → MC GMS：返回 `IWF group information subscribe response`，报告订阅请求成功或失败。

仅收到组信息不等于订阅已经成功，也不表示 GMS 会自动订阅。若 GMS 还没有该组配置，另查 [§10.2.3.5 的取配置前提与请求](iwf-defined-group-configuration-pull.md)。§10.2.3.8 没有要求先走 §10.2.3.5，也没有指定只能从该流程取得先前的组信息。

依据：TS 23.283 V16.8.0，[§10.2.3.8 条首与前提 1，印刷页 31](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=32)；[前提 2–3、图 10.2.3.8-1 与步骤 1–2，印刷页 32](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=33)。

## IWF 向已订阅的 MC GMS 通知

§10.2.3.9 有两个前提：MC GMS **已在 IWF 订阅该组配置**，而且 **IWF 有该组的新信息**。尚未确认 GMS 已订阅时，不能仅凭收到过组信息或发过订阅请求就按本条预期通知。

1. IWF → MC GMS：发送 `IWF group information notify request`。
2. MC GMS → IWF：返回图中标作 `IWF group information notify response` 的响应，报告本次通知成功或失败。

步骤 2 的正文名称多写了一个 `notify`（`IWF notify group information notify response`）。图和正文给出的响应方向和结果含义一致，不据此区分两类回执或决定线上编码。[§10.2.3.9，前提 1–2、图 10.2.3.9-1 与步骤 1–2，印刷页 32](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=33)

订阅响应回答订阅结果，通知响应回答这次通知的结果。两节没有指定更新时间、刷新间隔、版本机制、失败重试或本地写入；通知成功也不证明终端已拿到配置。若要查[组归属](lmr-hosted-mc-affiliation.md)或[回到覆盖后恢复聊天组媒体](../calls/lmr-chat-return-to-coverage.md)，按各自的程序判断。
