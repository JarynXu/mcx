# 控制功能：确定目标、邀请被叫与解释上游响应

TS24.379 V19.4.0 §§11.1.1.4.1–4.2，选定在网、带话权控制的私呼/first-to-answer控制功能流程。原文的originating/terminating在这里是同一控制角色的发出邀请与接收请求方向。

## 进入控制功能仍须做业务和媒体检查

适用条件：收到控制功能的private或first-to-answer INVITE。

分别检查Request-URI的PSI是否分配给对应业务，未分配转§6.3.7.1。private分支另校验主叫MCPTT ID并依本地策略授权，未授权403。缺resource-lists或private的resource-lists中一个list含多个entry：403+Warning145；没有至少一条参数及编解码/格式可接受的媒体流：488。不能将private特有的步骤1b当作first-to-answer完整授权规则。

依据：§11.1.1.4.2 步骤1–5。

## 向被叫参与功能发邀请，不等于直接呼叫UE

适用条件：控制功能执行邀请被叫的过程。

目标用户写入mcptt-request-uri，SIP Request-URI设为目标terminating participating功能PSI，PAI设为控制功能自己的PSI。PSI可指本域或伙伴域的相应功能；终接功能位于不同信任域的伙伴系统时，可使用伙伴入口网关PSI；如何找到PSI以及出口网关路由，规范明确留在范围外。

依据：§11.1.1.4.1 步骤4–6。

## 振铃响应会按呼叫类型转换

适用条件：尚未向主叫发送180或最终响应。

private收到180则向主叫生成180；first-to-answer在尚未收到其他相应180时，将这次180转成上游183。不能认为两端必须逐码透传。

依据：§11.1.1.4.2 收到180分支。

## 媒体缓冲允许先返回未确认的200

适用条件：private；收到P-Answer-State=Unconfirmed的183；控制功能支持media buffering；尚未向主叫发最终响应。

控制功能生成带SDP及P-Answer-State=Unconfirmed的200，并按规范与媒体层交互后发向主叫。这个200不是被叫用户已经应答的证据，应同时检查角色、方向和应答状态。

依据：§11.1.1.4.2 收到183 Unconfirmed分支。

## 被叫最终响应仍有媒体处理顺序

适用条件：private收到对应SIP INVITE的200响应，且尚未向主叫发最终响应。

构造上游200及SDP，执行媒体层处理并完成该处理后，才发送上游200。这里只描述该响应生成分支，不提供通用的“用户已应答”充分判据，也不是对实际端到端音频可听性的测试，也不覆盖已提前发Unconfirmed最终响应的后续状态更新。

依据：§11.1.1.4.2 private的200分支。

## 证据边界

- §11.1.1.4.2步骤8的紧急Resource-Priority条件包含neither与否定条件的文字张力，本页不据其构造紧急授权算法。
- 功能别名解析/300与全部媒体、ACK、紧急状态流程未完整收录。
- SIP核心、话权/媒体规范依赖未完整核验；按角色标识不等于部署节点或实例发现方案。

## 按需继续

- [originating-authorization](originating-authorization.md)
- [terminating-authorization](terminating-authorization.md)
- [private-client-acceptance](private-client-acceptance.md)
- [first-to-answer-selection](first-to-answer-selection.md)

[ETSI 官方 TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页452、453、454、455、456、457；仅本版本。

- [functional-alias-selection](functional-alias-selection.md)

- [../emergency/private-downgrade](../emergency/private-downgrade.md)

- [release-signalling](release-signalling.md)
