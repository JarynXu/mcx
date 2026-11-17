# Release 16

当前仅覆盖九项固定规范版本的局部范围，包括独立的 Stage 2 功能解释和 Stage 3 程序，整版尚未完成。

- [普通按需私呼：客户端应答与建立证据](topics/calls/private-client-answer-evidence.md)：TS 24.379 V16.14.0。
- [普通私聊 SDS 控制面：发送资格、请求与接收证据](topics/mcdata/sds-control-client.md)：TS 24.282 V16.13.0。

- [普通按需私呼：服务器准入与身份路由](topics/calls/private-server-admission-routing.md)：与对应客户端主题分开核对实际角色和事件。
- [普通私聊SDS控制面：服务器准入、目标路由与响应证据](topics/mcdata/sds-control-server.md)：与对应客户端主题分开核对实际角色和事件。

- [普通按需预安排组呼：客户端发起与应答证据](topics/calls/prearranged-client-establishment.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。
- [私聊HTTP文件分发客户端：上传、URL通知、下载决定与完成证据](topics/mcdata/http-fd-client.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。
- [普通按需 MCVideo 私呼：客户端请求、应答与结果证据](topics/mcvideo/private-client-answer-evidence.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。

- [显式组归属：本客户端的建立、解除与状态观察](topics/groups/explicit-affiliation-client.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。
- [私聊HTTP文件分发服务端：准入、目标转送与受理证据](topics/mcdata/http-fd-server.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。
- [普通按需 MCVideo 私呼：服务器准入、路由与响应边界](topics/mcvideo/private-server-admission-routing.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。

- [普通在网话权：客户端请求、排队确认与释放](topics/media/on-network-floor-client.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。
- [私聊 SDS 会话：客户端建立、应答与结束证据](topics/mcdata/sds-session-client.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。
- [在网 MCVideo 客户端：请求传输、获准与结束](topics/mcvideo/transmission-client-request-grant-end.md)：按该业务的实际角色和事件读取，不借其他业务闭合流程。

- [普通按需预安排组呼：服务器准入与邀请路由](topics/calls/prearranged-server-admission-routing.md)：按该主题网络模式、角色和实际事件读取。
- [私聊 SDS 会话：服务器准入、目标邀请与响应证据](topics/mcdata/sds-session-server.md)：按该主题网络模式、角色和实际事件读取。
- [普通离网组呼：探测、加入与本地退出](topics/calls/offnetwork-group-client.md)：按该主题网络模式、角色和实际事件读取。
- [私聊 SDS 会话媒体：连接、逐条发送与收件证据](topics/mcdata/sds-session-media-client.md)：按该主题网络模式、角色和实际事件读取。

- [私聊 SDS 会话媒体：服务器路径、绑定与逐跳响应](topics/mcdata/sds-session-media-server.md)：Stage 3，仅对应职责与事件。
- [在网 MCVideo 接收客户端：通知、接收许可与结束](topics/mcvideo/reception-client-permission-and-end.md)：Stage 3，仅对应职责与事件。
- [MCData 服务能力与功能角色](topics/mcdata/service-capability-and-functional-roles.md)：Stage 2，仅对应职责与事件。

- [MCVideo 功能职责：会话、传输接收控制与媒体分发](topics/mcvideo/functional-media-control-roles.md)：Stage 2，按对应业务及网络模式读取。
- [普通离网私呼：手动应答、建立证据与退出](topics/calls/offnetwork-private-manual-client.md)：Stage 3，按对应业务及网络模式读取。

- [预安排组 standalone SDS 控制面：客户端发送、接收与处置](topics/mcdata/group-sds-control-client.md)：仅对应网络模式、业务对象及事件。
- [普通按需 MCVideo 预安排组呼：客户端请求、应答与媒体初始化](topics/mcvideo/prearranged-group-client-establishment.md)：仅对应网络模式、业务对象及事件。
- [离网话权：请求、排队确认、发送与交接](topics/calls/offnetwork-floor-participant.md)：仅对应网络模式、业务对象及事件。

- [普通在网话权服务器：Idle 请求处理与条件授予](topics/media/on-network-idle-floor-server.md)：仅已成立Idle U/G的对应角色和事件。

- [普通预安排组呼：服务器显式传输请求、许可与结束职责](topics/mcvideo/prearranged-group-transmission-server.md)：仅普通预安排组服务器对应角色、状态和事件。

- [在网紧急预安排组呼：客户端发起、本人取消与结果证据](topics/calls/emergency-group-client.md)：按发起、升级、本人取消或反馈事件进入，不由普通呼叫或话权流程推定适用。

- [普通预安排组呼：接收服务器逐流许可与结束职责](topics/mcvideo/prearranged-group-reception-server.md)：仅普通预安排组服务器对应角色、状态和事件。

- [已有按需预安排组会话：CF紧急升级、取消与分层反馈](topics/calls/emergency-group-server.md)：按已有会话CF re-INVITE及对应响应事件进入；初始服务器或客户端请求不保证进入本页成功分支。

- [在网单话权：显式抢占请求与撤销事件责任](topics/media/on-network-preemption-revoke.md)：仅已成立的Taken/permitted及后续pending角色事件，不把队首或撤销当许可。

- [普通离网组：single 参与者的请求、媒体与本地结束](topics/mcvideo/offnetwork-single-participant.md)：仅普通离网组single终接/晚加入参与者，不接在网或私呼链。

- [独立组紧急告警：本人发起、取消与反馈证据](topics/calls/standalone-group-alert-client.md)：独立MESSAGE告警入口，按本人请求、响应、匹配回执或通知分别读取，不借紧急组呼推定适用。

- [普通离网组 single 仲裁者：非抢占授予、重发与发送者记录](topics/mcvideo/offnetwork-single-arbitrator.md)：仅普通离网组single实际仲裁状态，不补上游自任或交接成功。

- [普通预安排组重入与晚入：会话身份、准入和恢复证据](topics/calls/rejoin-late-entry.md)：按定向主动重入或实际CF晚入通知分别进入，200不等于获话权。

- [同用户多客户端的服务设置：读取、观察与停止观察](topics/calls/settings-observation.md)：按同用户设置读取、观察或停止观察的实际事件进入，不把通知缓存当作设置发布或呼叫采用。

- [普通在网组显式抢占：满容量撤销、等待与 End 证据](topics/mcvideo/onnetwork-preemption-revoke.md)：各角色按实际状态和事件进入，撤销、入队与 End 不证明完整抢占成功。

- [MCPTT 服务设置发布：身份守卫、当前设置与删除边界](topics/calls/settings-publication.md)：按构造、拒绝、实际成功处理与删除事件进入，不将设置传达等同服务授权、通知或呼叫成功。

- [预建立会话：建立、空闲修改与无业务使用时释放](topics/calls/preestablished-session-lifecycle.md)：按建立、无关联会话修改或无呼叫使用时释放分别进入，不将容器建立视为呼叫或话权成功。

- [协商式组归属：单目标请求、用户确认与状态证据](topics/groups/negotiated-affiliation-client.md)：按单目标请求、目标确认和接受后的状态守卫进入，不将交付200或用户接受视为归属完成。

- [组动态数据：订阅许可、通知内容与状态边界](topics/groups/group-dynamic-data.md)：按读取/订阅、角色准入与实际通知进入，不把组动态数据等同本人的归属或会议参与状态。

- [离网 MCData 消息在 MONP 中的识别与封装](topics/mcdata/offnetwork-monp-carrier.md)：根据外层类型码定位内层 MCData 消息。

- [同一用户跨业务、跨终端时，怎样辨认身份？](topics/identity/cross-service-user-mapping.md)：辨别认证、业务和路由身份，并按信任域判断何时可用公共用户身份标识业务用户。

- [MCVideo 组呼下行：组播子信道如何映射，哪些成员仍走单播](topics/mcvideo/mbms-group-downlink.md)：解释共用一条 MBMS 承载时的组映射、按监听状态分流和客户端收包。

先读主题共同条件，再按实际角色与事件选取结论；不把拒绝、应答、取消或后续数据处理拼成同时必备的条件。这些主题均不构成完整端到端实现，也不证明版本组合互通。

[业务域](domains.json) · [主题索引](topics.json) · [条件阅读路径](reading-paths.json) · [覆盖边界](coverage.md) · [来源](sources.json) · [状态](status.json)

仅所列版本与条款作为依据，不继承 Release 19 的结论或核验状态。未覆盖的服务端链、媒体、安全与其他业务须另查对应版本的规范。
