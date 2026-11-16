先从[业务域目录](domains.json)选择问题所在领域，读取相应轻量索引；明确问题路径时可直接用[阅读路径](reading-paths.json)。[全量主题索引](topics.json)保留供跨域检索。

# Release 19

本目录是部分覆盖的知识库。先按问题取正文；只有需要机器处理的条件时，才读该页同名 JSON。[主题索引](topics.json)支持问题定位，[读取路径](reading-paths.json)把相关任务连起来，不要求整条路径全部加载。

## 组文档与跨系统配置

- 先判断操作对象：[文档、元素与属性的方法表](topics/groups/resource-operations.md)；并发冲突见[ETag与412](topics/groups/conditional-update.md)。
- 构造请求与排错：[地址和命名空间](topics/groups/xcap-addressing.md)、[替换范围与409校验](topics/groups/xcap-write-validation.md)。
- 持续跟踪文档变化：GMC先看[初始订阅](topics/groups/change-subscription.md)，随后[列表更新与NOTIFY](topics/groups/subscription-refresh.md)；服务端按角色选[MCS服务器订阅](topics/groups/server-subscription.md)或[组成组GMS订阅临时组](topics/groups/constituent-subscription.md)，不要混用身份与Request-URI。
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

话权机制按问题选：[主控归属](topics/interworking/floor-control-owner.md)、[组请求本地过滤](topics/interworking/floor-filtering.md)、[无法通知旧发言者的覆盖](topics/interworking/floor-override.md)。本地预选通过不等于最终获授话权；私呼主控不能一概按组规则推定。

## 互通安全

[LMR安全消息运输](topics/interworking/lmr-security-transport.md)说明透明载荷如何承载；[加密语音转码](topics/interworking/encrypted-transcoding.md)说明媒体处理的密钥前提。运输成功不能证明密钥获取完成；这些主题也不构成完整安全实现。

## 注册、SIP 路由与 EPS 信令

按问题选读：[主系统认证与注册](topics/identity/primary-registration.md)、[注册器寻找及用户绑定](topics/signalling/registrar-routing.md)、[EPS 接入与信令 QoS](topics/network-policy/eps-signalling.md)。这组内容核对的是 TS23.280 V19.9.0 Stage2，不能推定与其他版本等同，也不是完整 REGISTER、分布式黏性或 5GS 映射方案。

对话内请求另读 [SIP 对话标识及路由集](topics/signalling/dialog-routing.md)：外部 RFC 基线，不冒充已核完整 MCX profile。5GS 则读 [QFI、5QI 与 ARP](topics/network-policy/5gs-qos-model.md)，需要判断 GBR 失保留流时再读 [通知控制](topics/network-policy/5gs-notification-control.md)。

伙伴系统另读[迁移授权及重定向门槛](topics/identity/migration-authorization.md)，返回或再迁移时读[旧伙伴去授权](topics/identity/migration-exit.md)。普通互联、用户迁移和 SIP 对话路由是不同问题；这条路径不保证进行中通话连续。

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

单系统采集见[配置触发与按需上报](topics/location/report-acquisition.md)，持续跟踪见[组目标、通知及取消](topics/location/subscription-lifecycle.md)，恢复通信后的积压位置见[历史补报](topics/location/history-recovery.md)。

单系统按需查询可先读[取得位置与回报的顺序](topics/location/on-demand-usage.md)，已核 V19.9.0；不据此升级下列其他版本摘要。

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

接入安全补充：[HTTP-1 与 SIP-1](topics/security/access-transport.md)已核 TS33.180 V19.4.0 的选定条款；外部安全 profile 尚未完整核验；应用令牌的已核部分见下方主题，不代表完整实现验收。

## 认证到私呼保护的按需路径

[原生客户端取令牌](topics/identity/native-authentication.md)解释客户端登记、授权码和PKCE；[服务授权与身份绑定](topics/identity/service-authorization.md)回答无token能否注册及逐条位置授权；[令牌刷新](topics/identity/token-refresh.md)限定scope与grant类型。随后按问题选择[KMS密钥获取](topics/security/kms-provisioning.md)或[在网私呼PCK分发](topics/security/private-key-distribution.md)。密钥交换成功不是业务准入或媒体连通证明。

### 伙伴域和组密钥

按问题选择：[伙伴令牌交换](topics/identity/partner-token-exchange.md)、[GMK下发校验](topics/security/group-key-distribution.md)、[成员移除与删钥](topics/security/group-key-membership.md)。三者分别处理授权、密钥接收和成员变化，不能彼此替代。

密钥取得之后，可按问题查看[UE保存与清理](topics/security/ue-key-lifecycle.md)或[组媒体与控制保护边界](topics/security/group-media-control.md)。

### 信令与MCData保护

[信令密钥更新](topics/security/signalling-key-update.md)说明CSK替换与MuSiK拒绝后的信令回退；[XML保护](topics/security/xml-protection.md)区分保护范围和服务器可见性；[MCData保护层次](topics/mcdata/security-layers.md)区分信令密钥和用户payload端到端密钥。

### 配置与通话状态

[预选和活动配置切换](topics/identity/profile-selection.md)区分下次授权生效与当前服务状态清理；[多发言者和预配置重组](topics/security/group-call-media-boundaries.md)说明混音位置和既有GMK前提；[KMS重定向](topics/security/kms-redirection.md)说明政策和信任边界，并保留原文疑义。

[取得主系统或伙伴配置](topics/identity/profile-acquisition.md) → [更新数据](topics/identity/profile-update.md) → [选择生效配置](topics/identity/profile-selection.md)组成用户配置路径。三步的成功不能互相代替。

### 组协议的读取与重组

[默认不取成员表](topics/groups/memberlist-free-retrieval.md)、[临时组检查与通知](topics/groups/temporary-group-lifecycle.md)、[GKTP访问边界](topics/groups/gktp-access.md)分别说明读取范围、形成/拆除条件和密钥资源授权。均限定TS24.481 V19.3.0，不把成功响应扩写为事务或媒体成功。

组协议排障继续看[代理至组拥有方的授权](topics/groups/subscription-proxy.md)和[未知XML条件处理](topics/groups/unknown-extensions.md)；[权限页](topics/groups/document-access.md)同时列出资源联动及所有者仍受限制的操作。

HTTP 请求的入口与身份可分别读取[TLS 端点](topics/identity/http-transport-endpoints.md)和[发送者身份分支](topics/identity/http-sender-identity.md)，再进入具体资源授权。两页限定 TS24.482 V19.0.0，不代表后续版本。

需要消息顺序时，查[IdM授权与令牌端点](topics/identity/idm-protocol-sequence.md)；参数安全约束仍在原生认证页，响应字段差异单列，不用流程概述覆盖条件。

### 私呼被叫的业务结果

密钥分发后可续读[拒绝、应答与取消](topics/calls/private-client-acceptance.md)及[模式选择](topics/calls/commencement-selection.md)。这些 TS24.379 V19.4.0 客户端步骤区分 MIKEY失败、用户拒绝、振铃与最终响应；服务器授权和媒体全流程仍未完整覆盖。

私呼服务器链可从[主叫授权与路由](topics/calls/originating-authorization.md)进入，按问题续读[控制功能的响应含义](topics/calls/control-routing-results.md)、[被叫侧授权](topics/calls/terminating-authorization.md)或[first-to-answer选择与清理](topics/calls/first-to-answer-selection.md)。媒体缓冲条件下存在200/Unconfirmed，不能仅凭200认定被叫已应答。

私呼后续处理可按问题继续：[别名解析与300](topics/calls/functional-alias-selection.md)、[转发触发](topics/calls/forwarding-trigger-limits.md)与[MESSAGE路由](topics/calls/forwarding-message-routing.md)、[取消紧急优先级](topics/emergency/private-downgrade.md)、[结束信令](topics/calls/release-signalling.md)、[无话权控制](topics/calls/without-floor-control.md)。这些页面保留各分支条件，不把信令成功等同于接通或全部资源释放。

判断私呼是否完成某一步，可查[回呼确认](topics/calls/callback-confirmation.md)、[转发客户端续呼](topics/calls/forwarding-client-reorigination.md)与[结果报告](topics/calls/forwarding-client-results.md)、[紧急升级](topics/emergency/private-upgrade.md)、[服务器释放链](topics/calls/server-release-chain.md)。每页按消息、角色和当前状态限定成功含义。

普通预安排组呼可从[发起寻址](topics/groups/prearranged-origination.md)进入，按需核对[成员、归属与权限](topics/groups/prearranged-admission.md)、[已有会话加入许可](topics/groups/join-authorization.md)、[确认与人数门槛](topics/calls/group-acknowledged-start.md)、[超时或拒绝](topics/calls/group-acknowledgement-failure.md)、[释放定时器](topics/calls/group-release-timers.md)和[隐式话权请求](topics/calls/implicit-floor-request.md)。这条路径区分准入、信令应答、媒体与话权，不把组密钥或单个成功码当成完整接通证明。

组呼被邀请侧可从[参与功能寻址与检查](topics/calls/group-terminating-addressing.md)进入，按需读[模式与预建立选择](topics/calls/group-terminating-mode.md)、[客户端接收与应答](topics/groups/terminating-client-acceptance.md)或[183、PRACK、200的含义](topics/calls/group-terminating-responses.md)。客户端手动183与参与功能自动Unconfirmed不是同一个条件，单腿Confirmed也不证明全组完成。

## 显式归属与加入进行中组呼

从[兴趣组PUBLISH](topics/groups/explicit-affiliation-publish.md)请求建立或刷新，[SUBSCRIBE/NOTIFY](topics/groups/explicit-affiliation-observation.md)用于观察结果。部分[退组请求](topics/groups/explicit-deaffiliation-request.md)必须保留其他兴趣组；[服务器撤销状态](topics/groups/explicit-deaffiliation-state.md)说明失败清理及同用户多客户端的未闭合处。PUBLISH200不能单独证明逐组变更成功。

已归属后，按[组ID加入及服务器late entry](topics/groups/active-call-entry.md)或[已有会话身份重入](topics/groups/rejoin-session.md)选择入口；两者还须通过各自通话准入。本文不把归属成功、被邀请与通话已建立合成一个状态。

## 归属后如何观察和退出通话

- [请求触发隐式归属的资格](topics/groups/implicit-affiliation-eligibility.md)与[候选记录及结果处理](topics/groups/implicit-affiliation-state.md)。
- [订阅会话参与者状态](topics/groups/conference-state.md)，需要合并增量通知时读[版本与合并规则](topics/groups/conference-state-merge.md)。
- [主动退出本次组呼](topics/calls/group-participant-leave.md)与[服务器移除参与者](topics/calls/group-participant-removal.md)。

归属状态、会话名单、呼叫接受和媒体可用性分别判断，不用一个200响应代替所有结果。

## 预建立与业务会话

- [建立、空闲修改和拆除](topics/calls/preestablished-session-lifecycle.md)
- [预建立承载组呼：REFER、Contact 与通知](topics/calls/preestablished-group-association.md)

## 普通在网 Chat

[按需加入入口](topics/calls/chat-ondemand-entry.md)与[控制侧准入](topics/groups/chat-ondemand-control.md)分开判断；已有对话见[会话更新](topics/calls/chat-existing-session-update.md)，离开或移除见[释放链](topics/calls/chat-participant-release.md)。这些是原生 Stage 3 程序，不替换 MC/LMR 互通主题。

### 媒体控制与话权证据

- [预建立 Connect 与客户端接受](topics/calls/mcpc-connect-evidence.md)
- [Disconnect、超时与保留承载](topics/calls/mcpc-disconnect-evidence.md)
- [入会、请求与授予](topics/calls/floor-participant-entry-request.md)
- [排队确认、撤销与释放](topics/calls/floor-participant-queue-release.md)

限 TS24.380 V19.1.0 指定分支；SIP成功、媒体收到、用户接受与发送许可不能互相替代。

### 服务器话权决策

先读[状态所有者](topics/calls/floor-state-ownership.md)，再按问题选择[空闲请求](topics/calls/floor-server-idle-request.md)、[他人持有时的排队](topics/calls/floor-server-queue-admission.md)、[取消与释放后选择](topics/calls/floor-server-release-selection.md)，或[授予后的媒体计时](topics/calls/floor-server-media-timers.md)。规范的条件衔接问题在对应页保留，不以推测补成实现算法。

### SDS 协议路径与回执证据

[发送准入与控制面/媒体面选择](topics/mcdata/sds-transmission-selection.md)区分大小上限与分流阈值；[回执时序与原消息关联](topics/mcdata/sds-disposition-timing.md)区分 SIP 响应、送达、已读和未送达。依据 TS24.282 V19.7.0 指定 Stage 3 分支；普通服务器路径见下文；媒体交付及配置依赖仍按页注明。

### MCVideo 客户端发送与接收

[发送控制](topics/mcvideo/participant-transmission-control.md)区分请求、排队、授予及结束；[接收控制](topics/mcvideo/participant-reception-control.md)区分来流通知、自动许可、主动接收与单源结束。依据 TS24.581 V19.2.0 指定 Stage 3 分支，不代表完整 MCVideo 信令或服务器策略。

### MCVideo 服务器发送授权与接收筛选

[发送仲裁](topics/mcvideo/server-transmission-grant.md)连接请求、源标识、许可与无人接收；[接收仲裁和用户接口](topics/mcvideo/server-reception-permission.md)说明普通组手动模式、按 SSRC 筛选以及停止下行。客户端和服务器的同名状态不共用实例；普通组不能依据客户端 Mode=0 分支自行选择自动模式。限 TS24.581 V19.2.0 所列分支，内部路由及编码疑义未以猜测补全。

### SDS 服务器准入与通知

按问题选择[身份与私聊准入](topics/mcdata/sds-server-identities-and-private-admission.md)、[普通组文档与归属](topics/mcdata/sds-group-controller-admission.md)或[路由及202/200](topics/mcdata/sds-server-responses-and-routing.md)。通知另经[参与功能路由与暂存](topics/mcdata/sds-notification-routing.md)、[控制功能关联与聚合](topics/mcdata/sds-disposition-aggregation.md)。TDC1窗口到期允许聚合发送，不证明全员成功；普通原请求与回执的SIP事务不能合并解释。

### MCVideo 计时与源终止

[发送/接收空闲](topics/mcvideo/server-idle-timers.md)区分T1、T2和T5；[排队授予重传](topics/mcvideo/server-queued-grant-retry.md)说明T4达到上限仍保留Taken；[无人接收源的终止](topics/mcvideo/server-stream-idle-termination.md)连接T11、结束命令、T3宽限及确认。默认值可配置；源终止、停止转发和通话释放分别判断。

### MCData XML的先行安全处理

[启用范围与配置默认](topics/mcdata/xml-protection-activation.md)、[入站验证及139/140](topics/mcdata/xml-inbound-validation.md)、[复制和出口重加密](topics/mcdata/xml-server-forwarding.md)分别回答发送前、业务处理前和服务器转发时的问题。身份绑定成功不能替代密码验证；XML、TLV及用户数据保护分别判断。

### SDS 按需媒体面的信令与结果

超过控制面阈值后，按[INVITE与SDP建链](topics/mcdata/sds-media-session-setup.md)、[建链和传输证据](topics/mcdata/sds-media-setup-and-transfer-evidence.md)、[结果BYE与资源释放](topics/mcdata/sds-media-result-and-release.md)选择问题。TS24.282指定的媒体接口不展开TS24.582内部成功判据，不能据此断言全组数据交付已核；用户主动释放也不无条件替代自动结果收尾。

### MCData TLV信令与用户Data

[逐段信令保护](topics/mcdata/tlv-signalling-hop-protection.md)说明PF/CF如何按各段条件处理；[用户Data与客户端验证](topics/mcdata/protected-data-client-verification.md)说明服务器安全透明转发和客户端签名职责。两类内容不可互换，CPK/CSK原文差异仍待裁决。

### HTTP 文件分发的接收与可用期

从[分段响应与实际文件取得](topics/mcdata/fd-http-file-and-signalling-evidence.md)区分URL、SIP成功和下载成功；按[自动/接受/延期及完成通知](topics/mcdata/fd-download-decision-and-completion.md)处理用户决定，再看[文件可用期与删除条件](topics/mcdata/fd-file-availability-and-expiry.md)。等待用户的TDU2和文件可用期TDC2不互相续期，过期通知也不证明文件已被物理删除。

### MCData 注册、授权绑定与设置

[REGISTER/PUBLISH入口](topics/mcdata/service-authorization-entry.md)区分能力标签和授权请求；[绑定建立与并发上限](topics/mcdata/service-authorization-binding.md)说明多client及处理顺序；[设置刷新和退出](topics/mcdata/service-settings-validity.md)连接后续SDS有效绑定检查。设置Expires不等于令牌或绑定寿命，200响应也不证明后续隐式归属全部完成。

### 观察设置与验证 CSK 更新

[设置订阅](topics/mcdata/service-settings-observation.md)按同一用户及client标识获取通知，不把SUBSCRIBE取消当作服务退出。[CSK下载验证](topics/mcdata/csk-key-download-validation.md)要求匹配服务PF、验签并成功提取后才替换该PF关联密钥；服务器切换确认和失败恢复的完整时序仍未核。

### 发送额度与 SDS session 的独立门槛

[FD大小准入](topics/mcdata/fd-size-admission.md)区分文件上限与单次额度，以及PF/CF各自责任；组HTTP的同一403/208不唯一对应一个根因。[SDS session准入](topics/mcdata/sds-session-admission.md)保留later-use的双方发送许可和组服务元素缺失时的拒绝，不能套用单条standalone SDS媒体传输流程。

### MCVideo 私呼从信令到媒体许可

[客户端邀请和应答](topics/mcvideo/private-call-client-signalling.md)、[服务器逐段准入和响应](topics/mcvideo/private-call-server-admission.md)使用TS24.281 V19.3.0普通单ID按需私呼。再从[会话与媒体许可边界](topics/mcvideo/session-media-permission-boundary.md)进入既有TS24.581 V19.2.0发送/接收状态机；200、PCK、SDP控制通道和隐式请求均不能单独证明发送或接收许可。

### SDS session 的建立与逐消息证据

[建立入口](topics/mcdata/sds-session-establishment.md)说明双向媒体协商和两端交接事件；[分段响应与参与者](topics/mcdata/sds-session-responses-and-participants.md)区分目标应答、全组加入和后来归属；[消息证据](topics/mcdata/sds-session-message-evidence.md)连接业务 UUID、释放后回执和未核媒体依赖。不能把 session 建立 200 当作单条数据送达。

### IP Connectivity

[目标与准入](topics/mcdata/ipconn-target-and-admission.md)说明如何从目标 IP 信息取得业务标识及角色权限；[服务器路径](topics/mcdata/ipconn-server-path.md)区分用户、下一跳和会话身份；[媒体与结果证据](topics/mcdata/ipconn-media-and-success-evidence.md)限定 200、ACK、应用字段和失败 BYE 的含义。本版双客户端在网过程明确不兼容 Rel16，未展开媒体规范内部实现。

### MCVideo 私呼释放

[客户端BYE](topics/mcvideo/private-call-client-release.md)区分停流和信令判定后的资源回收；[服务器逐段释放](topics/mcvideo/private-call-server-release.md)说明各段200、私呼策略及未消解的原文错引。不能将某一段200或某个源停止发送视为全部会话已释放。

### Message Store

[访问与对象](topics/mcdata/message-store-access-and-objects.md)区分客户端认证与服务器存入；[文件落点](topics/mcdata/message-store-file-locality.md)说明 retrieveFile 缺省获取和重复 retrieve 的结果；[通知同步](topics/mcdata/message-store-notification-sync.md)区分创建通道、变更订阅和本地对象更新。这里的文件“本地保存”指 Message Store，不是用户终端。

### 通信存储启停

[控制请求](topics/mcdata/message-store-control-request.md)、[PF准入](topics/mcdata/message-store-control-admission.md)与[执行结果](topics/mcdata/message-store-control-result.md)解释获准范围、全体开关和指定名单，以及200的含义。停用不是删除历史对象；指定名单body的原文差异尚未裁决。

### 普通 MCVideo 预安排组呼

[发起与准入](topics/mcvideo/prearranged-call-admission.md)连接组文档、归属和发起许可；[终接应答](topics/mcvideo/prearranged-call-terminating.md)解释模式、183和PRACK；[建立结果](topics/mcvideo/prearranged-call-setup-result.md)分开 required 成员、TNG1、缓冲支持与媒体许可，不把某个200当全员已接听。

### MCData 功能别名客户端

- [功能别名观察：变更前订阅与当前状态查询](topics/mcdata/functional-alias-observation.md)
- [功能别名变更：PUBLISH、续期与位置约束](topics/mcdata/functional-alias-change-request.md)
- [功能别名结果：PUBLISH 200、NOTIFY 与后续归属](topics/mcdata/functional-alias-state-evidence.md)

### MCVideo 进入已有组呼

- [MCVideo重入：session identity寻址、加入许可与TC边界](topics/mcvideo/rejoin-session.md)
- [MCVideo按组ID进入已有呼叫：join检查与Warning123](topics/mcvideo/active-call-entry.md)
- [MCVideo服务器主动晚进入邀请：触发、接受与媒体许可](topics/mcvideo/server-late-entry.md)

### MCData 功能别名服务器与结果回流

- [功能别名服务器准入：用户身份、owner 许可与两段 200](topics/mcdata/functional-alias-server-admission.md)
- [功能别名状态回流：owner 订阅、匹配状态与请求关联](topics/mcdata/functional-alias-owner-observation.md)
- [功能别名失效与对外结果：发布失败、到期和通知边界](topics/mcdata/functional-alias-lifecycle-results.md)

### MCVideo 会议状态

- [MCVideo会议状态订阅：会话寻址、授权、转发与终止](topics/mcvideo/conference-subscription.md)
- [MCVideo会议状态通知：何时发送、字段含义与成功证据](topics/mcvideo/conference-state-notification.md)

### MCData 功能别名目标SDS

- [向功能别名发送 SDS：解析选人、300 与直接 ID 重发](topics/mcdata/sds-functional-alias-target-routing.md)
- [SDS 别名解析：owner 查询、当前状态与协议缺口](topics/mcdata/sds-functional-alias-resolution.md)

### MCVideo 组成员离开与全组释放

- [MCVideo组成员离开：BYE不等于全组结束](topics/mcvideo/group-participant-leave.md)
- [MCVideo全组释放：五项策略、TNG3和公共BYE边界](topics/mcvideo/group-release-policy.md)

### MCData 显式归属与组观察

- [MCData 显式归属变更：完整兴趣列表、刷新与撤销](topics/mcdata/explicit-affiliation-request.md)
- [MCData 归属结果：先启动观察，再区分 200、状态与请求关联](topics/mcdata/explicit-affiliation-observation.md)
- [MCData group dynamic：独立组观察，不是归属或会话参加证明](topics/mcdata/group-dynamic-observation.md)


### 普通视频chat怎样新建或加入，何时归属和获得发送许可？

- [MCVideo普通chat入口：客户端寻址、PF准入与隐式归属结果](topics/mcvideo/chat-ondemand-entry.md)
- [MCVideo普通chat控制侧：资格、初建/已有分支与媒体许可](topics/mcvideo/chat-ondemand-admission.md)

### 归属请求怎样到组owner，哪些通知可以确认结果？

- [MCData 显式归属到组 owner：聚合记录、成员检查与接受边界](topics/mcdata/explicit-affiliation-owner-admission.md)
- [MCData owner 状态回流：独立订阅、匹配确认与缺席条件](topics/mcdata/explicit-affiliation-owner-state.md)
- [MCData 归属失败与结果回到客户端：清理范围及期限边界](topics/mcdata/explicit-affiliation-lifecycle-results.md)