# 加入活跃组呼：组ID入口、会话重入与服务器邀请

TS24.379 V19.4.0，普通在网预安排组呼；限定非重组，非远程发起，不含紧急或迫近危险指示。

本页区分三种入口，不将显式affiliation成功等同已经加入通话。

## 请求组呼时发现同组呼叫已在进行

适用条件：控制功能按§10.1.1.4.2处理针对普通组的请求，前序检查通过，且该组呼叫已经ongoing，进入step15而非新建step14。

普通分支仍检查本用户在请求客户端的组归属，未归属403+120并停止；再按§6.3.5.3判断加入许可，未授权403+121并停止。此处检查join-handling，不是新建分支的allow-initiate-conference；不能把拥有GMK当任一检查已通过。

依据：§10.1.1.4.2 step15a–b。

## 已有呼叫仍受参与人数上限约束

适用条件：加入活跃组呼的前序检查通过，且on-network-max-participant-count已达到。

本地策略认为新用户比现有用户优先时，可以移除一名现有参与者并跳过满员拒绝；否则486+122并停止。不是每次满员都强制抢占；具体策略可考虑用户优先级、参与者类型等，没有在本条定义统一排序。

依据：§10.1.1.4.2 step15c–d。

## 200加123表示加入既有会话

适用条件：普通活跃组呼加入通过准入且未被满员等条件拒绝。

控制功能生成200及SDP answer，带Warning123（会话已经存在）；完成规定媒体处理后发送，再通知已订阅conference event的客户端有用户加入，随后不继续该条后续建组响应处理。因此123不是呼叫失败码，也不是新建另一通组呼的证据。

依据：§10.1.1.4.2 step15h–r。

## 新归属或恢复覆盖可由服务器发起邀请

适用条件：控制功能被告知客户端新归属或从覆盖外返回，且有进行中的MCPTT组呼。

控制功能须按§10.1.1.4.1邀请该客户端加入已有组呼；获知恢复覆盖的方法在规范范围外。邀请走被邀侧终接处理，仍不能把触发邀请或affiliation通知视为用户已接受。

依据：§10.1.1.4.6;10.1.1.4.1.1。

## 已有session identity的重入是另一入口

适用条件：客户端主动重入且使用要重入的MCPTT session identity。

按需使用指向会话身份的initial INVITE，预建立使用REFER中的会话目标；控制侧走§10.1.1.4.5.1。它与本页组ID请求进入step15、服务器发邀请是不同入口，不能互换寻址或推定各分支都带Warning123。

依据：§10.1.1.2.4;10.1.1.4.5.1。

## 证据边界

- §10.1.1.4.2 step15a含特殊优先/重组/远程混合条件。本主题明确排除这些条件，不将简化的普通分支扩成通用布尔表达式。
- step15k/l在初始INVITE流程中写received re-INVITE，属本版文字疑义；本普通范围不展开其中Warning149与优先状态分支。
- 这里不补造恢复覆盖检测、重复邀请消重、并发新建/加入竞争、IMS fork或媒体/话权算法。

## 按需继续

- [rejoin-session](rejoin-session.md)
- [join-authorization](join-authorization.md)
- [prearranged-admission](prearranged-admission.md)
- [../calls/group-terminating-addressing](../calls/group-terminating-addressing.md)
- [../calls/group-terminating-responses](../calls/group-terminating-responses.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页278、297、298、299、303、304；仅本版本。

- [先分清归属通知与加入通话](explicit-affiliation-observation.md)

- [conference-state](conference-state.md)
