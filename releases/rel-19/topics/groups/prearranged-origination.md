# 普通预安排组呼：客户端目标与参与功能入口

在网 MCPTT，按需会话；用户请求发起 prearranged 组呼。

本主题只展开 GMS 管理的普通组；不展开 TGI、组重组或用户重组，初始 INVITE 不含 associated-group-id。

不展开广播、紧急/迫近危险、远程发起呼叫及隐式归属分支；相关指示不触发这些分支。

## 预配置重组专用组不能直接发起

适用条件：客户端已取得所用组文档。

list-service/preconfigured-group-use-only 存在且为 true 时，客户端 SHOULD 告知该组不允许呼叫，SHALL 停止本发起过程。

依据：§10.1.1.2.1.1 opening。

## 业务组目标与 SIP 下一跳分开

适用条件：preconfigured-group-use-only 并非存在且为 true。

初始 INVITE 的 Request-URI 指向服务该用户的参与功能 PSI，而非组 ID；mcptt-info+xml 的 mcptt-Params 带 session-type=prearranged、mcptt-request-uri=目标组 ID、mcptt-client-id=发起客户端 ID。主叫 MCPTT ID 由发起参与功能加入，不由客户端放入此正文。

依据：§10.1.1.2.1.1 steps 10, 14(a–c), NOTE 2。

## 参与功能先检查用户绑定与本地条件

适用条件：O-PF 收到其发起侧 INVITE，session-type=prearranged。

O-PF 从 P-Asserted-Identity 公共用户标识映射主叫 MCPTT ID。绑定不存在或有效期已过：404 + Warning 141 并停止；本地策略不允许用户发起预安排组呼：403 + 109。缺少 MCPTT speech codec：488；已超过 MaxSimultaneousCallsN6：486 + 103。

依据：§10.1.1.3.1.1 steps 2–5。

## 资源不足的可选拒绝

适用条件：O-PF 无资源处理或存在拥塞风险。

O-PF MAY 以 500 拒绝，MAY 带 Retry-After；不是所有过载请求都必须拒绝。

依据：§10.1.1.3.1.1 step 1。

## 向控制功能转发

适用条件：前序检查未拒绝；INVITE 不含 associated-group-id。

O-PF 查找目标组的控制功能 PSI；无法确定时 404 + 142 并停止。发往控制功能的 INVITE 以该 PSI 为 Request-URI，加入映射出的 mcptt-calling-user-id，不复制来话 Answer-Mode 或 Priv-Answer-Mode。

依据：§10.1.1.3.1.1 no-associated-group-id branch steps 1–5。

## 证据边界

- 这里只给业务寻址/身份字段，非完整 SIP/SDP 编码模板；Contact、Accept-Contact、服务标识和 SDP 仍依原条款。
- 原文判断 N6 为 exceeded，Warning 文本为 reached，不改写成达到上限必拒。优先呼叫的可选例外不在本普通呼叫主题范围。
- step 3 明确拒绝，但不像 step 2a 那样另写停止剩余步骤。
- PSI 发现机制及跨系统网关路由不由本条提供。原文 step 3 引用 determined in step 8，但本分支识别 PSI 在 step 1；保留该交叉引用异常。
- 未完成整套组呼建立；仅有界发起、准入与邀请选择入口，后续答复/接听、TNG1/TNG3、媒体/话权/安全协商不是本稿覆盖。
- 未展开 9.2.1/9.2.2 全套显式或隐式 affiliation 注册、刷新、撤销；只验证消费其记录的判定入口和存储层次。
- TS24.484 配置的生成/合法性、TS24.229 与 RFC SIP 实现依赖未独立展开。
- 未由普通组流程推导跨系统重组、广播、远程发起或紧急呼叫的完整成功/失败状态机。

## 按需继续

- [prearranged-admission](prearranged-admission.md)
- [server-subscription](server-subscription.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页268、269、270、279、280、281、282；仅本版本。
