# 互通 chat 加入与回到覆盖区

TS23.283 V19.5.0，Release 19，Stage 2。

TS23.283 §10.3.5 的 chat 组呼；不能直接套用预安排组呼触发条件。

## 组归属 LMR，呼叫正在进行；MCPTT 客户端已注册，用户已认证且获服务授权；客户端尚未加入，用户表示要加入

客户端携组 ID 发 join，经 server 到 IWF；IWF 接纳响应返回后建立媒体。只有请求发言时才携隐式话权请求。 [§10.3.5.8](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组定义在 MCPTT 系统，MCPTT 用户已加入且呼叫进行中；IWF 尚未加入

IWF 以 LMR 成员对应 ID 或代理用预配置 ID 发 join；server 对尚未归属者生成隐式归属，并验证 IWF 归属授权，接纳后建立媒体。 有发送请求才携隐式话权请求；携该请求时，位置信息仍为可选。 [§10.3.5.9](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 组归属 LMR；客户端在进行中 chat 呼叫期间离开无线覆盖，随后回到覆盖

客户端或 server 检测恢复后重建客户端与 IWF 媒体面；有人占话权时 IWF 经 server 转交 floor taken。检测机制不在规范范围。 [§10.3.5.10](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

隐式话权请求是请求，floor taken 是现有占用状态，二者都不等于新加入者已获授话权。回覆盖流程也未要求重新创建组。

## 范围

仅核对列出的 Stage 2 互通段，不覆盖底层注册认证、完整失败处理、超时及 LMR 内部过程。

[预安排组呼晚加入](late-entry.md) · [chat 整体释放](chat-release.md) · [互通范围](scope.md) · [结构化知识](chat-entry.json)

若是初次发起而非加入进行中的呼叫，先读 [chat 初建](chat-initiation.md)。
