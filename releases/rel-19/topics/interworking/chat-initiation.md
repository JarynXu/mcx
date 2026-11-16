# 互通 chat 初建：授权、位置与按需媒体

TS23.283 V19.5.0，Release 19，Stage 2。

TS23.283 §10.3.5.1–3 的初建路径；与已在进行中呼叫的新成员加入分开。

## 组定义在 LMR，server 与 IWF 已知组配置，IWF 身份映射已配置；MCPTT 用户发起 join

server 将 join 转往 IWF，IWF 接纳并选择媒体参数；server 转回响应。请求发言/发送媒体且媒体面尚未建立时，server 建立媒体面。 [§10.3.5.2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在 LMR，server 与 IWF 已知组配置，IWF 身份映射已配置；MCPTT 用户发起 join，且 join 携主叫位置

server 核对请求用户的位置隐私策略，判断能否向其他 MCPTT 用户及 IWF 提供位置，依结果决定转给 IWF 的请求是否携位置，不能仅因原请求有位置就无条件转发。 [§10.3.5.2 steps 2–3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在 MCPTT，IWF 已知配置且身份映射已配置，MCPTT 用户已加入/归属；LMR 用户发起 join

IWF 向 server 请求 join；server 核验 MCPTT ID 的归属授权，未归属时生成隐式归属，接纳并选媒体参数。IWF 请求发言/发送媒体且媒体未建时，server 才建立媒体面。 [§10.3.5.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

Join 接纳不是话权授予；也不能把 MC→LMR 的位置隐私处理步骤擅自补到另一方向。

## 边界

只核验所列互通条款；TS23.280/23.379 引用的配置字段、隐私策略及基础过程未独立核验，不能据此形成完整实现。

[进行中呼叫加入与回覆盖](chat-entry.md) · [chat 释放](chat-release.md) · [位置传播权限](../location/privacy.md) · [结构化知识](chat-initiation.json)

需核对归属本身时见 [显隐式归属通知](affiliation-lmr-group.md)。
