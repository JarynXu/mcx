# 互通组呼释放：主控侧与请求粒度

适用版本：TS23.283 V19.5.0，Release 19，Stage 2。

组配置双方已知、IWF 身份映射已配置，组呼正在进行且包含 IWF 与 MCPTT 客户端。

## 组主控服务释放呼叫

该流程释放所有参与者的组呼，不是单用户退出。MCPTT 侧释放条件引用 TS23.379；LMR 侧释放条件不在本规范范围。 [§10.3.3.8.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在 MCPTT 系统；MCPTT server 发起释放

MCPTT server 向 IWF 发送释放请求：IWF 代表 LMR 用户统一归属时只发一个；收到逐用户归属时，按每名已归属 LMR 用户各发一个。向 IWF 和 MCPTT 用户发送的先后不限。 [§10.3.3.8.2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在 LMR 系统；LMR 发起释放

IWF 按呼叫中每个 MCPTT 用户发释放请求，server 转发；客户端响应后 server 向 IWF 确认，最终释放相关话权和媒体资源。 [§10.3.3.8.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 边界与相关问题

本页只核验 TS23.283 的互通段；TS23.379 基础呼叫过程、LMR 内部信令及完整失败状态机未核验。

[组配置](group-configuration.md) · [组呼请求字段](group-call-request.md) · [互通范围](scope.md) · [结构化知识](group-call-release.json)

若问题涉及 chat 的可选响应或释放后归属状态，另读 [chat 释放](chat-release.md)；若只是取消归属导致单用户离开，读 [de-affiliation 退出](deaffiliation-exit.md)。
