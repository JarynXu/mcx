# 取消归属后的互通退出：单用户 leave

TS23.283 V19.5.0，Release 19，Stage 2。

预安排或 chat 组呼正在进行，MCPTT 用户与 IWF 代表的 LMR 用户同在呼叫中。

## 组预先定义在 IWF，已有 MCPTT 用户归属，至少一个 LMR 用户由 MCPTT ID 表示；MCPTT 客户端取消归属

IWF 经 MCPTT server 要求该客户端 leave；用户获通知，客户端响应并退出，server 将响应转交 IWF。 [§10.3.6.1–2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组预先定义在组管理服务器，已有 MCPTT 用户归属，至少一个 LMR 用户由 MCPTT ID 表示；IWF 代表的 LMR 用户取消归属

MCPTT server 向 IWF 发该用户的 leave 请求；IWF 响应并退出对应呼叫，移除该 LMR 用户。 [§10.3.6.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

这里移除的是取消归属的对应用户；不能从 IWF 的 leave 推出全部 LMR 用户或全组呼叫已结束。

## 用户取消归属后，哪条消息让谁离开组呼？

先看**组由哪一侧定义、取消归属的是谁**。这两支都适用于预安排和 chat。开始退出前，MCPTT 用户和经 IWF 接入的 LMR 用户已在同一通组呼中。组已有 MCPTT 用户归属，至少一名 LMR 用户由 MCPTT ID 表示。步骤 1 都从取消归属已经发生开始，没有给出由谁发起或怎样完成归属变更。[§10.3.6.1–.3 前提，印刷页 70–71（PDF 第 71–72 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=71)。

| 场景 | Leave 请求和应答 | 退出动作 |
| --- | --- | --- |
| **组定义在 LMR，已在 IWF 上预先定义；MCPTT 客户端已取消归属（.2）** | **2** IWF 向该客户端发 leave 请求，通过 IWF→server 这一腿；**3** server→MCPTT 客户端转为原生 leave 请求。**5** 客户端→server 回原生应答；**6** server→IWF 再发 IWF leave 应答。 | **4** 客户端向用户提示离开，提示不是确认已退出。**5** 同一步写客户端回应和离开，没给两者的实际先后；**7** 是该客户端从进行中的呼叫移除。6 是转发应答，不是另一次终端退出。 |
| **组定义在 MCPTT，已在 GMS 上预先定义；IWF 代表的 LMR 用户已取消归属（.3）** | **2** MCPTT server 经 IWF 向该 LMR 用户发 IWF leave 请求；**3** IWF→server 回 IWF leave 应答。图虽画 MCPTT 客户端，没有为它画 leave 往返。 | **3** 正文写 IWF 回应并离开组呼；**4** 具体移除的是 IWF 代表的**这名 LMR 用户**。不据此认定该 IWF 代表的其他用户都退出，或整个呼叫结束。 |

[§10.3.6.2 步骤 1–7 及图 10.3.6.2‑1，印刷页 71（PDF 第 72 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=72)；[§10.3.6.3 步骤 1–4 及图 10.3.6.3‑1，印刷页 71–72（PDF 第 72–73 页）](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=73)。

**核对的是哪一件事？** 在 .2，若只见 server 发出 6，可确认这端发了应答，不能确认 IWF 已收到；在 .3，只见 IWF 发出 3，也不能确认 server 已收到或该用户已经移除。查是否实际退出，看同一通呼叫中对应客户端或用户的参与状态，不要求找齐报文。只查单条消息的角色也无需全链；要把前后腿配成同一次，才核实际操作、当事人、组、呼叫和端点。方向不能单独判消息类型，例如 IWF→server 在 .2 的 2 是请求，在 .3 的 3 是应答。

已知是 IWF leave，再查[字段与标识](group-call-operation-elements.md#怎样读代理身份话权和实际结果)；表不是本节原生客户端腿的编码。单用户 leave 与[取消归属状态](affiliation-mc-group.md)、[结束整通预安排组呼](group-call-release.md)和[结束整通 chat 组呼](chat-release.md)各有证据。本节不规定 SIP、LMR 内部如何转送或媒体何时停止；.3 没另列通知 LMR 用户的动作。

## 范围

仅核对列出的 Stage 2 互通段，不覆盖底层注册认证、完整失败处理、超时及 LMR 内部过程。

[预安排组呼晚加入](late-entry.md) · [组主控整体释放](group-call-release.md) · [互通范围](scope.md) · [结构化知识](deaffiliation-exit.json)

整体结束呼叫请按类型读：[chat 释放](chat-release.md) 或 [§10.3.3 组呼释放](group-call-release.md)。

需核对归属本身时见 [取消归属的范围](affiliation-mc-group.md)。

本页是 §10.3.6 的呼叫 leave，不能据此缩小 §10.1.2.3 代理取消归属的影响范围：非逐用户模式的归属取消作用于 IWF 所代表的整个 LMR 系统。归属状态变化和呼叫参与变化应分别判断。
