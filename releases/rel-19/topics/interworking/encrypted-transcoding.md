# 加密语音转码：密钥前提与双向处理

适用版本：TS23.283 V19.5.0，Release 19，Stage 2。

MCPTT 会话已建立且媒体正在传输；IWF/server 已协商编解码及安全参数；IWF 配置支持转码，并按 TS33.180 取得 MCPTT 密钥材料。

## MCPTT 客户端持有话权并发媒体

IWF 解密 MCPTT 语音、转为 LMR 编解码，必要时按 LMR 安全过程重新加密后发往 LMR。 [§10.3.3.6 steps 1–4](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 话权空闲后 IWF 请求并获授话权

LMR 语音若已加密，先按 LMR 过程解密；转为 MCPTT 编解码，再按 TS33.180 加密，经 MCPTT server 转发。 [§10.3.3.6 steps 5–10](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 理解部署位置

该流程假设转码位于 IWF 内部，但转码实际位置不由本规范规定；不能把示例假设当部署强制要求。 [§10.3.3.6 NOTE](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 边界与相关问题

本页没有核验 TS33.180 密钥过程或 LMR 安全过程；不能据此推断端到端密文透传或任意加密组都允许转码。

[组配置](group-configuration.md) · [组呼请求字段](group-call-request.md) · [互通范围](scope.md) · [结构化知识](encrypted-transcoding.json)
