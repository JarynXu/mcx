# 取消归属后的互通退出：单用户 leave

TS23.283 V19.5.0，Release 19，Stage 2。

预安排或 chat 组呼正在进行，MCPTT 用户与 IWF 代表的 LMR 用户同在呼叫中。

## 组预先定义在 IWF，已有 MCPTT 用户归属，至少一个 LMR 用户由 MCPTT ID 表示；MCPTT 客户端取消归属

IWF 经 MCPTT server 要求该客户端 leave；用户获通知，客户端响应并退出，server 将响应转交 IWF。 [§10.3.6.1–2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组预先定义在组管理服务器，已有 MCPTT 用户归属，至少一个 LMR 用户由 MCPTT ID 表示；IWF 代表的 LMR 用户取消归属

MCPTT server 向 IWF 发该用户的 leave 请求；IWF 响应并退出对应呼叫，移除该 LMR 用户。 [§10.3.6.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

这里移除的是取消归属的对应用户；不能从 IWF 的 leave 推出全部 LMR 用户或全组呼叫已结束。

## 范围

仅核对列出的 Stage 2 互通段，不覆盖底层注册认证、完整失败处理、超时及 LMR 内部过程。

[预安排组呼晚加入](late-entry.md) · [组主控整体释放](group-call-release.md) · [互通范围](scope.md) · [结构化知识](deaffiliation-exit.json)

整体结束呼叫请按类型读：[chat 释放](chat-release.md) 或 [§10.3.3 组呼释放](group-call-release.md)。

需核对归属本身时见 [取消归属的范围](affiliation-mc-group.md)。

本页是 §10.3.6 的呼叫 leave，不能据此缩小 §10.1.2.3 代理取消归属的影响范围：非逐用户模式的归属取消作用于 IWF 所代表的整个 LMR 系统。归属状态变化和呼叫参与变化应分别判断。
