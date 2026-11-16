# Release 19

本目录是部分覆盖的知识库。先按问题取正文；只有需要机器处理的条件时，才读该页同名 JSON。[主题索引](topics.json)支持问题定位，[读取路径](reading-paths.json)把相关任务连起来，不要求整条路径全部加载。

## 组文档与跨系统配置

- 先判断操作对象：[文档、元素与属性的方法表](topics/groups/resource-operations.md)；并发冲突见[ETag与412](topics/groups/conditional-update.md)。
- 构造请求与排错：[地址和命名空间](topics/groups/xcap-addressing.md)、[替换范围与409校验](topics/groups/xcap-write-validation.md)。
- 持续跟踪文档变化：[订阅者、资源与SIP地址](topics/groups/change-subscription.md)。
- 创建请求被拒：[建组地址、403 与 409](topics/groups/creation.md)。
- 已知组 ID，要判断能读什么：[文档与成员表权限](topics/groups/document-access.md)。
- HTTP 请求要访问另一服务商：[跨服务商转发](topics/groups/forwarding.md)。
- MC/LMR 缺少组配置：[向谁获取](topics/interworking/group-configuration.md)；需要继续跟踪变化，再读[订阅与通知](topics/interworking/configuration-updates.md)。
- 不确定 IWF 是什么或规范管到哪里：[LMR/IWF 范围](topics/interworking/scope.md)。

- [跨系统重组边界](topics/interworking/regroup-boundaries.md)：接纳、用户信息和临时组所有权；语音兼容另见 [LMR 加密与编解码](topics/interworking/regroup-media.md)。

组文档主题依据 Stage 3；互通配置主题依据 Stage 2。它们不是同一个完整协议状态机，不能直接把一侧的信息流名称当成另一侧的 HTTP 消息。

- 互通组呼请求字段：[主叫身份与隐式话权](topics/interworking/group-call-request.md)，仅覆盖 Stage 2 信息要素。



## 互通归属与呼叫

按正在改变的状态选主题，不必依次读取整条链：

- 改变组归属关系：先分清[逐用户与代理](topics/interworking/affiliation-representation.md)，按组定义方选[MC组](topics/interworking/affiliation-mc-group.md)或[LMR组](topics/interworking/affiliation-lmr-group.md)；多个组的成功与失败见[逐组结果](topics/interworking/affiliation-results.md)。
- 预安排组呼中加入或结束：[晚加入](topics/interworking/late-entry.md)、[整体释放](topics/interworking/group-call-release.md)。
- chat 组呼：[初建](topics/interworking/chat-initiation.md)、[进行中加入或回到覆盖](topics/interworking/chat-entry.md)、[释放及归属保留](topics/interworking/chat-release.md)。
- 已取消归属，移除相应呼叫参与者：[取消归属后的退出](topics/interworking/deaffiliation-exit.md)。不能从单用户 leave 反推代理取消只影响一个人的归属；代理范围见上面的 MC 组主题。
- 同一个 LMR 用户涉及多个活跃组：[同时互通呼叫及实现边界](topics/interworking/simultaneous-calls.md)。
- 使用预配置方式重组：[配置来源组、实际重组及冲突](topics/interworking/preconfigured-regroup.md)，不要与§10.2.2重组混用。

互通私呼单独选：[手动建立与振铃/接受](topics/interworking/private-manual.md)、[三种发起方的释放确认](topics/interworking/private-release.md)、[两类加密及密钥前提](topics/interworking/private-encryption.md)。不要套用组呼加入或释放路径。

[话权信息流](topics/interworking/floor-signals.md)区分授予、占用、排队、取消及单播控制；这些状态不是呼叫释放。

## 互通安全

[LMR安全消息运输](topics/interworking/lmr-security-transport.md)说明透明载荷如何承载；[加密语音转码](topics/interworking/encrypted-transcoding.md)说明媒体处理的密钥前提。运输成功不能证明密钥获取完成；这些主题也不构成完整安全实现。

## 身份、紧急行为与媒体业务

以下为 Stage 1 的要求解释，不是可直接运行的协议实现。

- [身份与认证前访问](topics/identity/authentication-boundary.md)：应用身份、选定预认证能力和授权边界。
- [访问控制与终端禁用](topics/security/access-disable.md)：配置停用、暂时禁用和永久禁用的区别。
- [功能别名共享与接管](topics/identity/functional-alias.md)：模式互斥、满额与授权接管。
- [紧急告警、状态与组通信](topics/emergency/alert-state.md)：自动触发配置、状态持续及取消主体。
- MCVideo：[发流许可](topics/mcvideo/transmission-admission.md)、[接受邀请与选流](topics/mcvideo/reception.md)、[无人接收的通知及可选暂停](topics/mcvideo/no-receivers.md)。分别判断每组发送上限和每用户接收上限。
- [MCData 下载、已读与取消](topics/mcdata/delivery-evidence.md)：证据含义与取消范围。

- [MCData 会话与历史](topics/mcdata/conversation.md)：并行会话、关联超时和回执权限。
- [MCData 自动转发与接收邀请](topics/mcdata/transmission-options.md)：在网发送能力、大小上限与可选 TTL。

- [在网取数与无其他归属成员](topics/mcdata/receiving-data.md)：近期邀请列表、通知后发送选择。
- [在网终止通知](topics/mcdata/termination.md)：预告、原因和响应义务。
- [离网私聊](topics/mcdata/off-network-private.md)：授权、距离和生命周期能力，不含建立协议。

互通SDS的Stage2补充见[地址映射与代理回执](topics/interworking/sds-addressing.md)，不要把代理disposition当作终端已读。

## 位置与网络策略

[位置传播权限与保护要求](topics/location/privacy.md)已核对 Stage 1 原文，不能替代下列 Stage 2 机制核验。

跨 MC/LMR 的 [查询与通知](topics/interworking/location-query.md)、[订阅](topics/interworking/location-subscription.md)、[取消订阅](topics/interworking/location-unsubscribe.md)已核对应 Stage 2 条款，可直接进入，无须先读基础位置页。反向订阅响应端点的图文冲突仍保留。

进行中组呼另见[当前发言者位置](topics/interworking/talker-location.md)：话权与位置披露权限分别判断。

这三篇仍为整理说明，尚未重新核验对应规范原件：

- [位置报告与组目标](topics/location/reporting.md)：取消订阅、当前归属、测量时间及 UE label 方向。
- [位置触发覆盖与恢复](topics/location/trigger-override.md)：覆盖对象、期间新请求及恢复内容。
- [Rx 临时拒绝与重试间隔](topics/network-policy/rx-retry.md)：等待义务和永久失败边界。

## 能回答到哪里

[来源清单](sources.json)固定规范版本、条款和核验范围；[覆盖状态](status.json)列出已收录页面。除上面注明的三篇整理说明外，其余页面已核对所列原文条款，但未验证完整协议实现。

当前没有完整的注册认证、安全密钥、呼叫/媒体状态机、QoS/承载映射和各服务 off-network 实现知识。不能从某个子主题推出这些路径已经覆盖。位置配置取消字段集合仍未核清，本目录不提供该行为的确定规则。

Release 19 的条款不得静默用于其他 Release；缺失主题不是“规范没有要求”。
