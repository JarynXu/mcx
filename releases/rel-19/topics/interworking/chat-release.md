# 互通 chat 释放：会话结束不取消归属

TS23.283 V19.5.0，Release 19，Stage 2。

进行中的互通 chat 组呼包含 MCPTT 客户端与 IWF。

## 组定义在 LMR 系统；LMR 发起释放

IWF 按呼叫中每个 MCPTT 用户发送释放请求；server 转发并通知用户。客户端确认可选，流程释放话权和媒体资源，不改变客户端归属状态。 [§10.3.5.4](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在 MCPTT 系统；MCPTT server 决定释放

IWF 代理全组加入时 server 向 IWF 发一条；逐用户加入时按每名已加入 LMR 用户发一条。IWF 须响应所收释放请求，MCPTT 客户端确认可选；成功释放不改变客户端归属状态。 [§10.3.5.5](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 范围

仅核对列出的 Stage 2 互通段，不覆盖底层注册认证、完整失败处理、超时及 LMR 内部过程。

[预安排组呼晚加入](late-entry.md) · [组主控整体释放](group-call-release.md) · [互通范围](scope.md) · [结构化知识](chat-release.json)

单用户因取消归属退出另见 [leave 流程](deaffiliation-exit.md)。
