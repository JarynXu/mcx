# Release 19

本目录仅部分覆盖 MCX Release 19。它按业务问题解释职责、条件、流程与规范依据，不是完整协议实现或互通认证。先查问题所在业务域，再读命中的主题，无须按本页顺序阅读或加载整库。

## 从问题进入

- **找某项行为或响应含义：**从下表选择业务域；域索引列出问题、主题正文、结构化记录及来源。
- **需要连接几个步骤：**查[按问题组织的阅读路径](reading-paths.json)，仅在所列条件满足时继续下一页；相关主题不是必经流程。
- **想判断能回答到哪里：**查[覆盖边界](coverage.md)，区分已能回答的问题、只到条件或接口的部分和尚未建立的结论。机器可读形式见 [coverage.json](coverage.json)。
- **不知道属于哪个域：**查[业务域目录](domains.json)或[全量主题索引](topics.json)。[收录状态](status.json)用于核对已收录页面，不代表 Release 已完成。

| 问题所在领域 | 查什么、注意什么 |
| --- | --- |
| [MCPTT 通话与话权](topics-calls.json) | 私呼、预安排组呼、chat、预建立会话、加入与释放；普通、优先撤销、多发言者、双话权（含同一获准者再次请求的有限D回应及原主路退出接续）及有限离网路径（普通BASIC同类型合并按身份和时间守卫；排队主链另须判为非抢占，查询/等待出口按事件读取）。先分清呼叫控制与话权、客户端与服务器状态。 |
| [组管理与 MCPTT 组呼入口](topics-groups.json) | 组文档、XCAP 方法与权限、并发修改、订阅、显式/隐式归属和会议状态；文档权限、归属与入呼许可分别判断；[按需广播](topics/groups/broadcast-ondemand-signalling.md)另按版本限制与终接条件读取，不套非广播主链。MCData、MCVideo 专有归属到各自业务域查。 |
| [MCData 数据业务](topics-mcdata.json) | SDS、HTTP/媒体面 FD、IP Connectivity、MBMS 公告与有限MB2组FD映射、有限 MBS 组播接收意愿反馈、Message Store、功能别名，以及本业务授权、设置、归属、保护、紧急条件和释放。先区分在网与离网、控制面与媒体面、单条消息与会话；[显式列表ad hoc SDS session](topics/mcdata/adhoc-sds-explicit-list-establishment.md)另按列表与身份条件进入，不套配置组流程；服务器[criteria选人与集合变化](topics/mcdata/adhoc-criteria-membership-lifecycle.md)按独立入口读取，不作显式列表初建的必经后续；已有预建立承载上的[普通组SDS业务](topics/mcdata/pre-established-group-sds-use.md)另分REFER接受、业务响应与承载身份。 |
| [MCVideo 视频业务](topics-mcvideo.json) | 私呼、预安排组呼、chat、广播、video pull/push、有限离网自动/手动私呼和普通组呼探测、自动或需用户应答的有限加入及BASIC同类型条件合并；本业务授权、归属、会议/组动态观察、发送接收许可、紧急条件和释放。不套用 MCPTT 话权规则；[功能别名私呼](topics/mcvideo/private-call-functional-alias.md)另按权限、目标选择与300重试条件进入。 [独立纯告警取消](topics/mcvideo/standalone-emergency-alert-cancellation.md)另按本人/他人、实际 caller 和回执事件读取，不套 MCPTT 的 ongoing 守卫。 |
| [身份、注册与配置](topics-identity.json) | 身份认证、SIP 注册、服务授权、令牌、HTTP 身份、伙伴系统迁移和用户配置取得/更新/切换。各步骤的成功不能互相代替；主系统已注册且已有token时，MCPTT另查[PUBLISH服务授权与设置](topics/identity/mcptt-publish-service-authorization.md)，不以通用安全授权或INVITE绑定检查替代。 |
| [安全与密钥](topics-security.json) | 接入保护、KMS、私呼/组密钥、成员变化、保存清理及信令/媒体保护。取得密钥不等于业务准入或媒体连通；[离网两用户私呼密钥](topics/security/offnetwork-private-key-protection.md)按独立分发与验证入口读取，不套在线登录或组GMK步骤。 |
| [MCX 与 LMR 互通](topics-interworking.json) | IWF 范围、组配置与归属、重组、组呼/私呼、SDS 映射、话权和位置。Stage 2 信息流不是原生 MCX Stage 3 消息配方。 |
| [位置服务](topics-location.json) | 位置获取、报告、订阅、取消、历史补报与传播权限。当前归属、测量时间和报告可用信息分别判断；跨 MC/LMR 位置到互通域查。 |
| [网络策略与 QoS](topics-network-policy.json) | EPS 信令、Rx 重试与 MCData 预建立共享边界、5GS 的 QFI/5QI/ARP、GBR 通知、MCPTT 资源模型和通用 N5 创建、更新、终止及GBR目标变化通知。资源结果不是话权或媒体交付结果；[MCData 预建立共享](topics/network-policy/mcdata-preestablished-resource-sharing-boundary.md)的注册、Rx绑定和执行证据也须分开。 |
| [SIP 路由](topics-signalling.json) | 注册器寻找及用户绑定、对话标识、remote target 与 route set。RFC 基线不等于完整 MCX SIP profile。 |
| [紧急与优先状态](topics-emergency.json) | 通用紧急要求、MCPTT 私呼升级/降级，以及[已建组呼紧急升级](topics/emergency/group-inprogress-upgrade.md)与[取消紧急状态](topics/emergency/group-inprogress-cancel.md)各自的条件入口；没有正在进行的组通话时，已归属用户另查 [DedicatedGroup 独立告警](topics/emergency/standalone-group-alert.md)的请求、分发与确认边界；MCData、MCVideo 的专有告警与取消须回到各自业务域，不跨业务搬用规则。 [独立 MESSAGE 告警取消](topics/emergency/standalone-alert-cancellation.md)另分客户端与 CF 入口；无通话纯取消的 CF caller 未闭合，不接成发起后的必经链。 |

## 几类容易选错的入口

- **已入会，为什么还不能发送？**MCPTT 先看[话权状态所有者](topics/calls/floor-state-ownership.md)；MCVideo 看[会话与媒体许可](topics/mcvideo/session-media-permission-boundary.md)。在网双话权、多发言者和离网仲裁不是同一状态机，分别查[双话权](topics/calls/dual-floor-entry-and-media.md)、[多发言者](topics/calls/multi-talker-admission-and-media.md)和[离网话权入口](topics/calls/offnetwork-floor-entry.md)。
- **收到成功响应，数据真的送到了吗？**SDS 先查[响应、送达与已读](topics/mcdata/sds-disposition-timing.md)；FD先确认HTTP还是媒体面，再按响应所在事务段和角色选页：HTTP查[信令与实际取得文件](topics/mcdata/fd-http-file-and-signalling-evidence.md)，接收决定与已请求的完成更新查[下载与通知](topics/mcdata/fd-download-decision-and-completion.md)；媒体面先分[发送端结果](topics/mcdata/fd-msrp-start-and-originator-result.md)、[逐跳确认与PF暂存](topics/mcdata/fd-msrp-hop-ack-and-storage.md)和[有条件完成报告](topics/mcdata/fd-media-reception-and-signalling-report.md)。需要判断哪些目标完成时，按报告关联、目标及聚合条件读取，不能由CF 202或计时放行推出全员完成；HTTP共享文件何时能删另查[目标集合与可用期守卫](topics/mcdata/fd-file-availability-and-expiry.md)。媒体面SDS仍查[MSRP响应与终端交付](topics/mcdata/sds-msrp-response-boundary.md)。不要把服务器响应、下载、阅读或应用完成合成一个结果。
- **归属、会话名单和通话接受有什么区别？**MCPTT 查[归属结果观察](topics/groups/explicit-affiliation-observation.md)及[会议通知合并](topics/groups/conference-state-merge.md)；MCData、MCVideo 在本业务域中查“归属”和“conference/group dynamic”。PUBLISH 200 或一份成员名单不证明已经参加通话。
- **一个参与者退出，会不会结束整场通信？**MCPTT 查[组呼参与者退出](topics/calls/group-participant-leave.md)；MCVideo 查[组成员离开](topics/mcvideo/group-participant-leave.md)；MCData先区分承载与意图：媒体SDS的[授权参与者释放](topics/mcdata/authorized-user-media-release.md)不用于媒体FD。HTTP FD按[原主叫终止](topics/mcdata/http-fd-originator-termination.md)、[服务器停止](topics/mcdata/http-fd-server-stop.md)或[其他授权用户释放](topics/mcdata/authorized-user-http-release.md)选页；一个接收者拒绝或想删除共享文件，另查[可用期与拒绝集合](topics/mcdata/fd-file-availability-and-expiry.md)，不当作原主叫取消。媒体FD服务器主动无预告释放查[逐段BYE与资源收尾](topics/mcdata/media-fd-server-release.md)；其他授权参与者要求无预告释放媒体FD，另查[授权INFO与CF权限判断](topics/mcdata/media-fd-authorized-user-release.md)；该信令入口不证明完整媒体收尾或文件删除，不能从SDS页补齐媒体实现。预告延期还须分服务器与授权者发起，见[HTTP停止/延期条件入口](reading-paths.json)。停止单源、单腿 BYE、整场释放和资源回收分开判断。
- **离网如何建立并取得本地许可？**MCPTT 已知双用户普通私呼先分模式：手动等待、应答、取消与正常释放查[手动主链](topics/calls/offnetwork-private-manual-answer.md)，自动路径查[基本P与类型Q控制](topics/calls/offnetwork-private-auto-control.md)，自动建立等待中的重传、拒绝和取消另查[P2有限出口](topics/calls/offnetwork-private-auto-setup-exits.md)，自动终接已发ACCEPT后的等待另查[P5重传与失败](topics/calls/offnetwork-private-auto-accept-wait.md)，自动已建呼叫正常释放另按[逐端清理](topics/calls/offnetwork-private-release.md)，组呼则从[普通组呼探测与建立](topics/calls/offnetwork-group-probe-and-start.md)进入，成功建呼后才按条件查[话权竞争](topics/calls/offnetwork-floor-request-contention.md)；已判非抢占的排队与移交另看[逐角色事件](topics/calls/offnetwork-floor-queue-and-handoff.md)，排队后的查询与等待另看[条件出口](topics/calls/offnetwork-floor-queue-query-and-exit.md)；MCPTT参与中遇到同组另一普通BASIC呼叫，另查[有限合并](topics/calls/offnetwork-group-basic-merge.md)，不据此证明话权许可或全网收敛；MCVideo 按模式区分[自动私呼](topics/mcvideo/offnetwork-private-auto-setup.md)、[手动应答、取消与有限释放](topics/mcvideo/offnetwork-private-manual-answer.md)及[普通组呼探测及无需用户确认加入](topics/mcvideo/offnetwork-group-probe-and-join.md)，组呼终接需用户应答时另查[S4/S5](topics/mcvideo/offnetwork-group-user-confirmation.md)，公告回应和本地离开另按[对应条件](topics/mcvideo/offnetwork-group-announcement-and-leave.md)读取，参与中遇到同组另一BASIC呼叫时查[条件合并](topics/mcvideo/offnetwork-group-merge.md)，已在会且本地授权的用户请求另查[有限紧急类型升级](topics/mcvideo/offnetwork-group-emergency-type-upgrade.md)，BASIC在会接收同组同call紧急公告另查[改变者与时间守卫](topics/mcvideo/offnetwork-group-emergency-announcement.md)，返回普通类型另按[用户、END或计时到期入口](topics/mcvideo/offnetwork-group-emergency-downgrade.md)；MCData 先分[离网SDS首次上下文](topics/mcdata/offnetwork-sds-initial-context.md)与[重发](topics/mcdata/offnetwork-sds-retransmission.md)。这些入口不能拼成通用离网实现，也不证明唯一仲裁者或全员接收。
- **5GS 分配成功能否证明业务成功？**先区分[MCPTT Stage 2 资源模型](topics/network-policy/mcptt-5gs-server-resource-request.md)与[通用 N5 Stage 3 授权结果](topics/network-policy/n5-authorization-result-boundary.md)。通用 API 不证明 MCX 已绑定该接口，201、逐流通知和媒体可用性也不是同一证据。[GBR目标变化通知](topics/network-policy/n5-gbr-qos-notification.md)另区分不再保证、恢复保证与受影响流，不等于媒体恢复。已有上下文的[更新](topics/network-policy/n5-session-update.md)与[终止/删除](topics/network-policy/n5-session-termination.md)另按事件读取，响应不等于承载执行完成。

## 读取条件、版本与证据

先读命中主题的正文；需要机器处理时，再读同名 JSON。每条 claim 继承该主题全部 `common_conditions`，并叠加自己的 `conditions`。角色、当前状态、触发事件、例外和证据边界不得在摘取时丢失。

Stage 1 是业务要求，Stage 2 是架构或信息流，Stage 3 是协议程序；它们不能互相替代。各页的 `standard_stage`、固定来源及具体条款决定结论范围。多来源页面按每条 `source_id` 或 `source_references` 追溯，不能把主来源的版本和页码套给其他来源。

本目录同时使用下列固定快照，详细条款、发布者、URL 及核验范围见[来源清单](sources.json)。表中并列不表示已经验证组合互通，也不表示整部规范已经读完。

| 用途 | 固定规范版本 |
| --- | --- |
| 通用、视频及数据业务要求 | TS 22.280 V19.7.0；TS 22.281 V19.0.0；TS 22.282 V19.0.0 |
| 公共架构与位置 | TS 23.280 V19.9.0、V19.10.1，按各主题分别适用，不以较新版本覆盖较旧结论 |
| MCX/LMR 互通 | TS 23.283 V19.5.0 |
| MCPTT 通话与媒体控制 | TS 24.379 V19.4.0；TS 24.380 V19.1.0 |
| 组文档与 HTTP 身份 | TS 24.481 V19.3.0；TS 24.482 V19.0.0 |
| MCVideo 信令与媒体控制 | TS 24.281 V19.3.0；TS 24.581 V19.2.0 |
| MCData 信令与媒体 | TS 24.282 V19.7.0；TS 24.582 V19.0.0 |
| 安全 | TS 33.180 V19.4.0 |
| 网络策略 | TS 23.501 V19.8.0；TS 23.289 V19.7.0；TS 29.214 V19.3.0；TS 29.514 V19.5.0 |

外部 IETF RFC 只作为各页标明的基线或依赖，本身没有 3GPP Release。Release 19 条款不得静默用于其他 Release；MCData 的[IP Connectivity 版本限制](topics/mcdata/ipconn-media-and-success-evidence.md)还须单独读取，不能推定与 Rel16 兼容。

页面或 Git 提交存在，不证明完整实现验收。来源身份核对、指定条款原文复核、独立复核与使用验证按实际状态区分；[覆盖边界](coverage.md)仍应与命中页一起判断。缺少主题不表示规范没有要求。

## 未闭合或有原文差异时

当前尚未提供完整的注册认证、安全密钥、呼叫/媒体状态机、QoS/承载映射和各服务 off-network 实现知识。下面列出影响使用的差异入口；其他条件化接口和缺口按[覆盖边界](coverage.md)及主题内说明读取，不以常识补成可编码的协议。

- **位置取消与互通端点：**[TS 23.280 V19.10.1 的来源记录](sources.json)保留表 10.9.2.1-1 与 §10.9.3.4 的取消字段措辞差异，不能据此确定完整取消载荷；报告接收者与组目标另查[位置报告](topics/location/reporting.md)。[互通位置订阅](topics/interworking/location-subscription.md)保留反向响应端点的图文冲突。触发覆盖与恢复另见[对应主题](topics/location/trigger-override.md)。
- **令牌和安全：**[令牌响应字段](topics/identity/token-response-obligations.md)不把 TS 24.482 与 TS 33.180 的义务静默合并；[KMS 重定向](topics/security/kms-redirection.md)保留信任边界及疑义。MCData 的 [TLV 信令](topics/mcdata/tlv-signalling-hop-protection.md)与[用户 Data 验证](topics/mcdata/protected-data-client-verification.md)保留 CPK/CSK 差异，[CSK 更新](topics/mcdata/csk-key-download-validation.md)不补齐未核的服务器切换确认和失败恢复时序。
- **MCData 存储与媒体接口：**[存储控制请求](topics/mcdata/message-store-control-request.md)保留指定名单 body 的差异，停用不等于删历史；[IPCONN 隧道](topics/mcdata/ipconn-tunnel-and-delivery.md)保留源端口语法差异，[媒体与结果](topics/mcdata/ipconn-media-and-success-evidence.md)保留失败/销毁接口缺口。TS 24.582 与 TS 24.282 各自已核部分不等于全部接口映射已验证。
- **MCVideo 路由、释放及紧急状态：**[发送仲裁](topics/mcvideo/server-transmission-grant.md)和[接收仲裁](topics/mcvideo/server-reception-permission.md)保留内部路由及编码疑义；[私呼服务器释放](topics/mcvideo/private-call-server-release.md)与[私呼紧急服务器路径](topics/mcvideo/private-emergency-server-path.md)保留错引和未闭合字段，不把信令成功视为全部媒体已停。[Video push](topics/mcvideo/video-push-request-and-authorization.md)保留 PF 分类、PSI 用途与两类目标字段边界，[提示、录制与释放](topics/mcvideo/video-push-observation-and-release.md)不证明首帧或同步停止。
- **MCPTT 仲裁与停止：**[服务器释放后选择](topics/calls/floor-server-release-selection.md)、[优先撤销](topics/calls/floor-preemption-decision.md)保留排队及后继授予的条件缺口；[离网话权入口](topics/calls/offnetwork-floor-entry.md)保留发起者 explicit/implicit 请求差异，[离网停止](topics/calls/offnetwork-floor-release-boundary.md)保留空队列分支未显式列出停止 RTP 的差异，不推导仍可继续发送。双话权的[第二路停止与原主路退出后的接续](topics/calls/dual-floor-stop-evidence.md)仅覆盖列明的服务端分支，不补完整终端 G-bit/Ack 路由。

- **紧急取消授权：**[MCPTT 私呼降级](topics/emergency/private-downgrade.md)保留服务器授权的 FFS，[MCData 私聊取消](topics/mcdata/private-emergency-server-cancellation.md)保留本业务的未决授权及部分接受边界；不把一种业务的规则移到另一种。无ongoing组通信且无emergency-ind时，MCData[指定他人告警取消](topics/mcdata/emergency-alert-third-party-cancellation.md)另按许可、CF处理与通知事件判断，不补组服务器降级缺口。

授权不等于可达，归属不等于参加，会话建立不等于媒体许可，发送或排队不等于交付，单端释放不等于所有参与者同步停止。需要端到端结论时，沿条件化阅读路径逐项取得证据，不能用一个成功码或一个本地状态替代。
