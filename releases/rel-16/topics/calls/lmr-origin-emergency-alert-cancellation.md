# LMR 用户撤销紧急告警：IWF 发给哪一组，谁回执？

IWF 代表原发起的 LMR 用户，向此前成功发送告警请求的 **同一 MC 业务组**发送撤警请求。MC 业务服务器回 IWF 确认撤警，另向有归属的组员客户端发撤警请求。这两段各有自己的响应；组播例外只涉及组员客户端回给服务器的回执。[3GPP TS 23.283 V16.8.0，Release 16，Stage 2，§10.6.5.1，步骤 1–5，印刷页 139](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=140)

## 先找原告警和它的组

这名 LMR 用户此前已通过 IWF 成功发起告警，现在由他发起撤警。IWF 已有该互通组的资料，并配置了组和用户的身份映射。组可在 LMR 或 MC 系统定义，图中的两个 MC 业务客户端已归属。MC 业务服务器可能已为 LMR 用户办理显式或隐式归属；条款没有把已经办理归属列成必备条件。两系统间经 IWF 的信令由 IWF 做身份转换和协议转换。[§10.6.5.1 前提、注 1 和图 10.6.5.1-1，印刷页 138](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=139)

步骤 1 的 `IWF emergency alert cancel request` 对准 IWF 当时代表该用户成功发送告警请求的组。请求中可加一项指示，**另外请求取消组的进行中紧急状态**。该项是可选的附带请求，不是撤警已取消组状态的证明。[步骤 1 和注 2，印刷页 139](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=140)

## 分开看确认和下发

- **服务器 → IWF（步骤 2）**：用 `IWF emergency alert cancel response` 确认 IWF 的撤警。这份确认不证明组员客户端已收到。
- **服务器 → 有归属的 MC 组员客户端（步骤 3–4）**：下发 `MC service emergency alert cancel request`，通知相应用户这名 LMR 用户的紧急告警已取消。
- **收件客户端 → 服务器（步骤 5）**：用 `MC service emergency alert cancel response` 确认客户端收到的撤警请求。组播呼叫场景不发送这些客户端回执，条款没有把例外扩大到步骤 2。

步骤 2 和步骤 3 可以任一顺序执行。不能把先给 IWF 确认当作向组员下发的前提，也不能把此处的响应当成 LMR 无线终端实收的证据。该节没有定义取消组紧急状态的执行程序、与通话有关的结果或线上报文。[步骤 2–5 和注 3，印刷页 139](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=140)

查同一 MC 系统内在网 MCVideo、MCData 的撤警和成员回执，读[在网组告警取消](onnetwork-group-alert-cancel.md)。查跨业务的撤警对象要求，读[共用紧急告警取消](common-emergency-alert-cancellation.md)（Stage 1）。两个页面都不是本 IWF 流程的必经步骤。
