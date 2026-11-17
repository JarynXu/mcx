# Release 19：能回答的问题与覆盖边界

本目录仅覆盖所列问题和条件，不是Release 19整版完成声明。主题数量不是完成率，也不代表条款、实现或互通场景的覆盖比例。
“能回答”指可从已列主题找到有来源的条件化答案；“只到条件或接口”指出不能直接跨越的步骤；“尚未建立的结论”是本知识库的边界，不是断言标准没有相关规定。
先选业务，再读链接主题的共同条件、角色、事件、条款和限制。本页只是导航，不替代原主题的shall/should/may、否定条件或源文疑义。
同属Rel19不代表不同规范的精确版本已验证互通。Stage1是需求层，Stage2是架构/信息流层，Stage3是协议层；Stage3片段也不自动构成完整可运行实现。RFC依赖不是Rel19规范。

[业务域目录](domains.json) · [按问题阅读](reading-paths.json) · [全部主题](topics.json) · [来源版本](sources.json)

## MCData数据业务

[查看本域全部主题](topics-mcdata.json)

### SDS：在网发送、会话与回执

- **能回答：**可按控制面/媒体面入口查准入、逐段响应、会话标识与消息标识，以及送达/已读通知的不同证据。
- **只到条件或接口：**MSRP响应、分块接收、standalone收尾及session带内通知只在各页角色和事件条件内成立；来源侧200不是全组送达。
- **尚未建立的结论：**完整MSRP/RFC错误恢复、逐消息可靠性及24.282 V19.7.0与24.582 V19.0.0的完整接口映射、组合互通未建立。

入口：[SDS发送准入与承载选择：控制面阈值不是发送上限](topics/mcdata/sds-transmission-selection.md)；[SDS回执：SIP响应、送达与已读的不同证据](topics/mcdata/sds-disposition-timing.md)；[SDS session 后续使用：会话标识、消息证据与媒体边界](topics/mcdata/sds-session-message-evidence.md)；[SDS媒体确认：CF受理与终端交付分开判断](topics/mcdata/sds-msrp-response-boundary.md)；[Standalone SDS媒体收尾：最后响应与停止发送](topics/mcdata/sds-msrp-standalone-release.md)；[SDS session回执：业务类型与MSRP响应不同](topics/mcdata/sds-session-inband-notification.md)。

所列入口的来源：3GPP TS24.282 V19.7.0；3GPP TS 24.582 V19.0.0。具体Stage、条款及跨源差异以各主题为准。

### 离网SDS：消息与通知各自重发

- **能回答：**可区分TFS1/CFS1消息重发、TFS2/CFS2通知重发、TFS3等待显示及原消息关联。 普通初发另可查目标、conversation与新消息标识、UTC时间及可选回复/应用/处置上下文。
- **只到条件或接口：**仅离网standalone SDS所列信令分支；计数含初发、停止重发不是收到确认，READ仍需相应事件。 初发须通过适用的AllowedSDS守卫；保存SHALL与携带MAY分开，表O不取消目标字段的过程SHALL。
- **尚未建立的结论：**不覆盖完整发现、地址配置、安全、通知聚合或可靠交付；目标状态名称缺口不补成完整路由。

入口：[离网SDS重发：次数上限不是送达确认](topics/mcdata/offnetwork-sds-retransmission.md)；[离网SDS接收：重复消息与已读等待](topics/mcdata/offnetwork-sds-reception-and-read.md)；[离网SDS通知：原消息关联与独立重发](topics/mcdata/offnetwork-sds-notification-retry.md)。 另查[离网SDS：首次发送的目标与关联上下文](topics/mcdata/offnetwork-sds-initial-context.md)。

所列入口的来源：3GPP TS24.282 V19.7.0。具体Stage、条款及跨源差异以各主题为准。

### FD：HTTP与MSRP媒体面分别判断

- **能回答：**可查文件上限、HTTP存入/可用/下载证据，以及MSRP空SEND、分块收尾、服务器先响应、暂存和终端重组。另可查PF条件完成通知、CF直接或条件聚合路由、目标PF及客户端通知交付；普通媒体面FD服务器无预告释放另按类型策略及CF/PF/客户端事件区分BYE、原因与逐段资源收尾。 其他已参与授权用户的媒体FD无预告请求另可查INFO生成、PF条件转发及CF配置授权/释放调用。
- **只到条件或接口：**终端内部下载完成指示不同于PF有条件的完成通知；PF暂存完成不等于终端下载。HTTP调用不能补到媒体面。 路由从实际PF完成事件及完成更新请求起，CF/目标PF各按实际收到与入口守卫执行；不补helper未逐项列出的CF入口字段。 授权者INFO200只表示请求接受，不证明媒体停止、跨段收尾或文件删除。
- **尚未建立的结论：**媒体面ACK错引、SDP/MIME差异及普通转发中PF如何获知终端完整下载仍未闭合；未给完整文件系统、断点续传或全端交付保证。聚合策略选择、TDC1表的SDS实例范围与FD正文差异、晚到通知、PSI发现、完整事务恢复及客户端专门200/关联算法仍未闭合；NOTE6为容量说明，聚合放行及202不证明全员下载或原主叫已看到结果。

入口：[FD 发送准入：文件上限、单次额度与拒绝来源](topics/mcdata/fd-size-admission.md)；[HTTP 文件分发：文件已存、URL 已通知与下载成功](topics/mcdata/fd-http-file-and-signalling-evidence.md)；[FD 接收决定：自动下载、接受、延期与完成通知](topics/mcdata/fd-download-decision-and-completion.md)；[媒体面 FD：何时能发文件，响应如何触发收尾](topics/mcdata/fd-msrp-start-and-originator-result.md)；[媒体面 FD：服务器 200、转发与暂存分别证明什么](topics/mcdata/fd-msrp-hop-ack-and-storage.md)；[媒体面 FD：收齐文件、信令面完成指示与业务通知](topics/mcdata/fd-media-reception-and-signalling-report.md)。 另查[媒体面FD的服务器主动释放：BYE、原因与逐段资源收尾](topics/mcdata/media-fd-server-release.md)。 另查[媒体面FD：授权参与用户请求无预告释放](topics/mcdata/media-fd-authorized-user-release.md)。

所列入口的来源：3GPP TS24.282 V19.7.0；3GPP TS 24.582 V19.0.0。具体Stage、条款及跨源差异以各主题为准。

### IP Connectivity：建立、隧道与释放

- **能回答：**可查直接双客户端IPCONN的信令准入、端点/锚点参数、条件中继、GRE-in-UDP约束及逐段释放证据。
- **只到条件或接口：**媒体路径不必经过每个信令服务器；200/ACK、隧道建立和应用成功分开。用户主动与服务器无预告释放按各自入口适用。
- **尚未建立的结论：**sport/s-port语法差异、失败探测及逐隧道销毁未闭合；无完整RFC实现或精确版本互通保证，不能搬用SDS的MSRP成功收尾。

入口：[IP Connectivity 的服务器路径与分段响应](topics/mcdata/ipconn-server-path.md)；[IP Connectivity 的媒体协商、应用信息和失败证据](topics/mcdata/ipconn-media-and-success-evidence.md)；[IPCONN媒体路径：隧道建立、逐跳中继与IP交付](topics/mcdata/ipconn-tunnel-and-delivery.md)；[MCData 会话的服务器释放：无预告 BYE、原因与参与者范围](topics/mcdata/session-server-release.md)。

所列入口的来源：3GPP TS24.282 V19.7.0；3GPP TS 24.582 V19.0.0。具体Stage、条款及跨源差异以各主题为准。

### MBMS：公告与监听反馈

- **能回答：**可查按TMGI保存/取消公告、SDP关联、保护验证、listening/not-listening分支及PF身份校验；NOTE5另说明初始映射交集与映射后接收区域。MB2组FD另可查Map/Unmap角色、关联字段和MSRP仍进行时的单播回归。
- **只到条件或接口：**公告与监听仅按24.282 V19.7.0第19章；MB2组FD映射按24.582 V19.0.0第7.4节的终止侧、MSRP/SDP及公告前提。两版本分别取证，公告、监听、映射、业务数据到达分别判断。
- **尚未建立的结论：**§19A multicast join/leave通知仍见独立有限主题；MB2组FD映射不扩为SDS或5GS MBS。完整承载创建、媒体处理、密钥、重传修复、无线检测及端到端交付链未建立，也不保证两个固定快照完整互通。

入口：[MBMS公告与终端监听条件](topics/mcdata/mbms-announcement-and-listening-conditions.md)；[MBMS监听反馈：触发、对象与证据边界](topics/mcdata/mbms-listening-feedback-boundary.md)。 另查[FD MBMS：组到承载的映射与解除](topics/mcdata/fd-mbms-group-bearer-mapping.md)。

所列入口的来源：3GPP TS24.282 V19.7.0。具体Stage、条款及跨源差异以各主题为准。

### 授权、归属、存储、别名及终止

- **能回答：**可按业务对象查服务绑定、设置有效期、归属结果、Message Store对象与文件落点、功能别名结果、HTTP FD取消及延期。
- **只到条件或接口：**各主题只覆盖所列角色、条件与结果；存储确认、PUBLISH 200、NOTIFY、归属及通话参加不可互换。
- **尚未建立的结论：**不把对象存在当作内容已下载；未建立所有跨域、配置schema、存储实现或所有子服务的统一终止算法。紧急变更须另查专门主题。

入口：[MCData 服务授权如何建立绑定：身份来源、并发上限和响应边界](topics/mcdata/service-authorization-binding.md)；[MCData 归属结果：先启动观察，再区分 200、状态与请求关联](topics/mcdata/explicit-affiliation-observation.md)；[对象与文件落点：存入、迁存和重复请求](topics/mcdata/message-store-file-locality.md)；[功能别名结果：PUBLISH 200、NOTIFY 与后续归属](topics/mcdata/functional-alias-state-evidence.md)；[HTTP FD 主叫取消：定位原分发、202与终止结果](topics/mcdata/http-fd-originator-termination.md)；[MCData 会话释放预告：剩余量、TDC3 与延期决定](topics/mcdata/session-release-extension.md)。

所列入口的来源：3GPP TS24.282 V19.7.0。具体Stage、条款及跨源差异以各主题为准。

### 5G MBS：组播接收意愿通知

- **能回答：**可区分两个join与三个leave替代触发、PF目的地址与业务/MBS会话标识，以及绑定成立且含session-id时的媒体意愿指示。
- **只到条件或接口：**仅§19A multicast MBS；join/leave表达接收意愿，不将公告、映射、网络加入或数据接收合成一次成功。无conversation触发与消息session-id关联仍未闭合。
- **尚未建立的结论：**不提供完整MBS公告/监听、下层加入或交付链；mvdata/角色文字、successfully joining前提和相邻listening错引/状态矛盾不裁决，不从意愿报告证明承载完成。

入口：[5G MBS 组播接收意愿：join/leave触发与PF反馈边界](topics/mcdata/mbs-multicast-join-feedback-boundary.md)。

所列入口的来源：3GPP TS24.282 V19.7.0。具体Stage、条款及边界以主题为准。

### 预建立会话上的普通组SDS业务

- **能回答：**可查普通组SDS session的REFER身份、PF准入与有限业务reINVITE和终接结果钩子。
- **只到条件或接口：**已存在预建立会话；REFER200、业务响应与预建立承载身份分别判断。客户端与PF按实际事件处理，不以一段成功证明后段成功。
- **尚未建立的结论：**不补CF分发、完整安全/SIP、资源共享或全端交付；不扩私聊、standalone、FD或紧急过程。

入口：[预建立会话内发起组SDS session：身份、接入与业务结果](topics/mcdata/pre-established-group-sds-use.md)。

固定来源及具体条款以主题为准。

### Ad hoc SDS session：显式列表初建

- **能回答：**可查显式用户列表的客户端、PF与CF有限初建责任，列表/业务身份、各角色配置门槛及成功返回。
- **只到条件或接口：**普通在网按需ad hoc SDS session显式列表；不是私聊或配置组的扩大。缺失配置规则逐角色判断，可选conference动作在媒体步骤之后。
- **尚未建立的结论：**不补完整终接、全员交付、criteria动态确定/修改、预建立、standalone、FD或安全实现。

入口：[Ad hoc组SDS session：显式用户列表如何成为一次组通信](topics/mcdata/adhoc-sds-explicit-list-establishment.md)。

固定来源及具体条款以主题为准。

### 指定他人的独立紧急告警取消

- **能回答：**可查指定他人告警的客户端许可/请求、CF已授权取消分支与接收通知的有限处理。
- **只到条件或接口：**普通配置组、明确另一告警原发起者、无ongoing组通信且无emergency-ind；请求客户端、CF及通知接收者各按条件判断。
- **尚未建立的结论：**不补旧组servercaller、完整PF转交、通知关联、安全或批量取消；不当作SDS/FD通信降级或MCPTT组取消的后续。

入口：[指定他人的MCData紧急告警怎样取消](topics/mcdata/emergency-alert-third-party-cancellation.md)。

固定来源及具体条款以主题为准。

### ad hoc SDS criteria用户集合生命周期

- **能回答：**可查普通在网按需ad hoc SDS服务器criteria查询、结果、持续成员增删及停止职责。
- **只到条件或接口：**CF/PF按各自入口处理，CF增删须ongoing；200先于应用增删，选中用户、邀请对象、参与者和交付结果不同。
- **尚未建立的结论：**不把criteria作为显式列表初建必经步骤；初建15c回指.5而非.6.1未闭合，不覆盖用户主动改criteria、迁移或完整邀请/移除与全员交付。

入口：[ad hoc SDS按条件选人与持续成员变化](topics/mcdata/adhoc-criteria-membership-lifecycle.md)。

固定来源及具体条款以主题为准。

### 普通组 HTTP FD 的控制侧准入与目标选择

- **能回答：**可查 HTTP 分类与 FD SIGNALLING PAYLOAD/group-fd 条件、组文档成功门槛、组配置/成员/发送权限，以及前序通过后的归属目标和出站身份。
- **只到条件或接口：**普通在网本地非重组 HTTP group-fd，按实际 CF 步骤顺序及停止条件读取；前置 MIME/FILEURL 之后才进入组分支，大小与主叫归属门槛仍由既有主题承载。
- **尚未建立的结论：**不把成员资格当发送许可、大小通过或归属；保留 supported-services 量词、元素存在判断和目标回指差异，不替未归属者创建记录，不套媒体面FD、终止或完整下载算法，202不证明交付。

入口：[普通组 HTTP 文件分发：控制侧业务准入与目标身份](topics/mcdata/http-group-fd-controller-admission.md)。

### 私聊媒体面 FD 的 CF 邀请与建会证据

- **能回答：**可查普通单目标媒体面FD的INVITE排队/准入、大小门槛后的唯一目标邀请、出站身份、CF offer/answer方向及正常匹配与暂存200的不同入口。
- **只到条件或接口：**普通在网本地、直接单目标one-to-one媒体面FD，无紧急/迫近危险、Resource-Priority或alert请求；各前序检查未停止才继续，文件大小仍查已有owner。
- **尚未建立的结论：**不搬HTTP202或HTTP-only下载决定到媒体链；§11.2只确认实际caller，保留P-Asserted-Service-Id、request-type复制、角色及跨快照SDS引用/MIME差异，不把CF200当下载完成或完整端到端接通。

入口：[私聊媒体面FD：控制侧邀请与建会响应证据](topics/mcdata/media-fd-private-controller-setup.md)。

### 媒体面 FD 自动接收与终端下载决定

- **能回答：**可查媒体CF缺IE时调用§11.2的自动接收判定，以及终端实际收到媒体FD INVITE后的资源/安全检查、强制接收或用户决定。
- **只到条件或接口：**普通在网、本地、单播私聊或非重组普通组媒体FD；CF缺IE入口与终端已带强制IE入口分别读取，前序准入仍有效，终端接受限定无关联CANCEL。私聊CF关联页仅适用于one-to-one，组caller另据原文。
- **尚未建立的结论：**不把自动接收阈值当发送许可；缺metadata不借HTTP URL回退，不搬TDU2。保留§11.2无括号条件及403/480重叠，不裁决唯一响应算法，不以200证明文件完成或修复ACK媒体引用差异。

入口：[媒体面文件分发：自动接收判定与终端下载决定](topics/mcdata/media-fd-download-decision.md)。

## MCVideo视频业务

[查看本域全部主题](topics-mcvideo.json)

### 在网通话、发送与接收

- **能回答：**可区分私呼、预安排组、chat、广播的信令结果，以及按用户/源的发送与接收控制、单源停止和通话释放。
- **只到条件或接口：**所列普通在网transmission-control及单源接收/停止分支按各页条件读取；SIP 200、发流许可、收流许可、首帧显示不能互作成功，不推广到所有MCVideo模式。
- **尚未建立的结论：**不代表所有会话模式、异常恢复和媒体编解码已覆盖；不得把MCPTT话权或一个源停止扩成整通话结束。

入口：[MCVideo 按需私呼：客户端邀请、应答与接通证据](topics/mcvideo/private-call-client-signalling.md)；[MCVideo预安排组呼：required、最低人数与Unconfirmed成功](topics/mcvideo/prearranged-call-setup-result.md)；[MCVideo普通chat控制侧：资格、初建/已有分支与媒体许可](topics/mcvideo/chat-ondemand-admission.md)；[MCVideo广播媒体角色：发起者发送、接收者Mode0与拒绝反向发送](topics/mcvideo/broadcast-media-roles.md)；[普通在网 MCVideo 发送：入会不等于可发送](topics/mcvideo/participant-transmission-control.md)；[普通在网 MCVideo 接收：按源通知、许可与结束](topics/mcvideo/participant-reception-control.md)；[某个源无人接收：T11到期、停止命令与T3确认](topics/mcvideo/server-stream-idle-termination.md)。

所列入口的来源：3GPP TS24.281 V19.3.0；3GPP TS24.581 V19.2.0。具体Stage、条款及跨源差异以各主题为准。

### 拉取另一客户端视频

- **能回答：**可查A拉B的角色、pull类型、CF双边许可、被叫隐式媒体请求及用户/服务器释放入口。
- **只到条件或接口：**仅普通在网按需one-to-one、使用transmission control；被叫拒绝仍有效，隐式请求不是授予。
- **尚未建立的结论：**不覆盖one-from-server或pull专属完整媒体状态机；未建立隐式请求相对200的独立时序、首帧或同步停止证明。

入口：[向另一客户端拉视频：请求角色与双边授权](topics/mcvideo/video-pull-request-and-authorization.md)；[拉视频的开始与结束：媒体请求、通话成功和释放分开判断](topics/mcvideo/video-pull-start-and-release.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体Stage、条款及跨源差异以各主题为准。

### 推送本端视频给另一客户端

- **能回答：**可查 push 会话类型、服务 PSI 与目标、CF 双边权限、被叫提示、可选保存及用户/服务器释放入口。
- **只到条件或接口：**仅普通在网按需 one-to-one、使用 transmission control；私呼 helper 仍保留各自条件，提示、接受、通话成功、媒体许可和实际接收分别判断。
- **尚未建立的结论：**不覆盖 one-to-server、完整 PF 分类/准入或 push 专属媒体状态机；PSI 用途及两类目标字段差异无消解规则，释放错引保留，不证明首帧、文件落盘或同步停止。

入口：[向另一客户端推视频：服务地址、目标与双边权限](topics/mcvideo/video-push-request-and-authorization.md)；[收到推视频邀请：提示、接听、可选录制与释放证据](topics/mcvideo/video-push-observation-and-release.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体Stage、条款及跨源差异以各主题为准。

### 普通离网自动私呼

- **能回答：**可查已确定两用户间的自动建立、拒绝、P2/P5到P4的端点事件，以及RELEASE、超时、P1保留标识与P0清理。
- **只到条件或接口：**MONP信令入口；发起端媒体调用角色称谓及clause a.b占位引用保留。自动终接端按原文以terminating MCVideo client调用；RELEASE接收分支不另加originating发送者限制，完整消息分派和鉴权未核。
- **尚未建立的结论：**本项仅自动路径；手动等待、应答、建立前取消及有限本地释放另按手动主题条件读取，不自动继承本项。不是离网组呼或完整发现/安全/媒体控制实现；未闭合发送与接收许可、首帧、双端同步停止或重叠超时优先级。

入口：[离网自动私呼：发起资格、接受与拒绝](topics/mcvideo/offnetwork-private-auto-setup.md)；[离网私呼接通：双方状态和媒体许可缺口](topics/mcvideo/offnetwork-private-media-entry.md)；[离网私呼结束：逐端响应、超时和清除标识](topics/mcvideo/offnetwork-private-release.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体Stage、条款及跨源差异以各主题为准。

### 普通离网基本组呼：探测与无需确认加入

- **能回答：**可查探测与超时创建、主动加入和终接无需用户确认的加入判据，以及条件公告回应、本地离开和探测取消。
- **只到条件或接口：**仅既定普通BASIC GROUP CALL、emergency state=false，按S/T各自状态和事件；公告回应另需stored probe response已满足所列条件，不推断初值。
- **尚未建立的结论：**本项仅探测及无需确认加入；S4/S5需用户应答另见独立主题，同组另一BASIC呼叫的条件合并另见独立主题；其他类型/优先级及跨过程调度仍未闭合。probe初值、媒体a.b占位与发送错引保留；S3不证明媒体许可、首帧或全组同步，本地离开不结束全组。

入口：[离网组呼：探测、创建与加入判据](topics/mcvideo/offnetwork-group-probe-and-join.md)；[离网组呼：公告回应与本地离开](topics/mcvideo/offnetwork-group-announcement-and-leave.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体Stage、条款及跨源差异以各主题为准。

### 离网组呼终接：需用户应答

- **能回答：**可查S1进入S4/S5、用户接受、拒绝或TFG4超时，以及S6保留身份的有限衔接。
- **只到条件或接口：**普通BASIC GROUP CALL且本地要求用户应答；有无Confirm indication独立决定S5/S4，只有所列S5接受支发送ACCEPT。基本控制S状态与类型控制T状态分别判断。
- **尚未建立的结论：**不补配置默认、并发调度、重新加入或完整媒体状态机；a.b占位保留，ACCEPT收发不证明全组加入、接收许可或首帧。

入口：[离网组呼来话：等待用户、接受与拒绝后的状态](topics/mcvideo/offnetwork-group-user-confirmation.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体Stage、条款及边界以主题为准。

### 离网普通组呼：同类型条件合并

- **能回答：**可查同组另一BASIC呼叫的身份差异守卫、较早start time或同时间较小call ID选择，基本控制的存储/媒体调用及TFG6/TFG2重启，以及类型侧字段更新。
- **只到条件或接口：**基本控制S3、类型控制T2各自适用守卫；普通同类型，不按originator ID大小或最后类型变更时间决胜。采用被选呼叫SDP不等于同一呼叫期间任意改流。
- **尚未建立的结论：**跨过程调度/取值、平局兜底、其他类型和优先级、全网收敛未闭合；媒体a.b占位不补号，不以保持S3证明媒体许可或首帧，不把重启TFG6当作从合并时刻给满额时长。

入口：[离网普通组呼合并：选择另一通话与本地切换](topics/mcvideo/offnetwork-group-merge.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体Stage、条款及边界以主题为准。

### 普通离网手动私呼：等待与应答

- **能回答：**可查manual commencement发起授权、RINGING等待、终接P5用户接受/拒绝或超时及本地完成；另分P2建立前取消、终接P5/P1接收取消、P4释放及后续P3/P1有限出口。
- **只到条件或接口：**两个已确定用户的普通PRIVATE CALL，MONP而非SIP；逐端状态、call id、模式和事件条件分别判断。用户接受仍留P5，RINGING不启动自行补造的等待算法。
- **尚未建立的结论：**P2取消与P4释放不互补CFP3初始化或清理步骤；取消路径完整重传次数、重叠超时调度、媒体a.b、安全、完整异常分派、双端计时同步和首帧未闭合。自动相关页的适用条件不自动继承到手动模式。

入口：[离网手动私呼：响铃等待、用户应答与有限失败](topics/mcvideo/offnetwork-private-manual-answer.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体Stage、条款及边界以主题为准。

### 离网MCVideo组呼：本地授权紧急升级

- **能回答：**可查已在会T2本用户请求且EmergencyCallChange=true时的BASIC到EMERGENCY类型动作、优先级引用、TFG13/TFG14及公告身份字段。
- **只到条件或接口：**仅本地类型控制的正向授权分支；基本控制并行，原发起用户与本次改变者分开。TFG13先启后更新时间，helper Z如何衔接仍未闭合。
- **尚未建立的结论：**不覆盖初始紧急建立、接收传播、降级、迫近危险或完整告警；不承诺完整X时长、配置默认、媒体许可或全组结果。

入口：[离网MCVideo组呼：已在会用户请求紧急升级](topics/mcvideo/offnetwork-group-emergency-type-upgrade.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体条款及边界以主题为准。

### 离网MCVideo组呼：BASIC在会接收紧急公告

- **能回答：**可查T2且保存BASIC收到同组同call紧急公告时，同改变者与不同改变者两分支的时间守卫、类型/优先级更新及计时器调用。
- **只到条件或接口：**同改变者须公告时间严格更新；不同改变者step2b不继承step1或2a时间比较。TFG13只保留helper调用，不借本地升级配置或不同call合并。
- **尚未建立的结论：**不覆盖初建T0、T1/T3其他接收、转发确认、降级或告警；不证明完整配置时长、媒体许可、所有状态或全组传播。

入口：[离网组呼：BASIC参与者收到紧急类型公告](topics/mcvideo/offnetwork-group-emergency-announcement.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体条款及边界以主题为准。

### 离网MCVideo组呼：紧急类型降级

- **能回答：**可查T1用户明确降级、T1接收END、T1的TFG13到期三类独立入口，及明确降级后T2的TFG11重发；区分自身、原始发起者及接收改变者字段来源。
- **只到条件或接口：**用户资格和配置只用于明确用户降级，不限制END接收或TFG13到期；小于上限只限制重启TFG11。保留END关联、安全依赖以及helper中的PRIORITY ENDED命名差异。
- **尚未建立的结论：**不证明完整接收鉴权、配置默认、重放策略、全组同步、媒体释放或用户紧急告警取消；T2仍是普通组呼类型，不等于整通呼叫结束。

入口：[离网MCVideo紧急组呼：谁触发降级，以及降级结束什么](topics/mcvideo/offnetwork-group-emergency-downgrade.md)。

所列入口的来源：3GPP TS24.281 V19.3.0。具体条款及边界以主题为准。

### 在网TC私呼：功能别名目标

- **能回答：**可查别名初始目标、客户端/O-PF权限字段、CF条件查询与目标选择、300业务目标及重试。
- **只到条件或接口：**普通在网按需TC单一别名，角色按各自事件判断；300 target与Contact分开，不把解析成功当终接接受。
- **尚未建立的结论：**查询互配缺口、激活生命周期、完整发现/安全/SIP及媒体许可未闭合；不继承直接ID私呼页排除别名的条件。

入口：[在网私呼拨功能别名：权限、目标选择与 300 重试](topics/mcvideo/private-call-functional-alias.md)。

固定来源及具体条款以主题为准。

### 独立 MCVideo 紧急告警取消

- **能回答：**可查本人或他人取消的许可与对象字段、PF/CF 实际调用入口、指定告警缓存，以及本人回执和接收者通知的不同状态动作。
- **只到条件或接口：**本系统在网预安排组、请求用户已授权且已归属、无 ongoing 组会话且不携 emergency-ind；这是本页范围，CF 的 alert-ind=false 分派本身不要求 ongoing 会话。各角色与授权结果分别判断。
- **尚未建立的结论：**不从 MCPTT 移植 ongoing 守卫或权限字段；保留取消授权、通知/回执生成错引和 client-id 构造匹配缺口，不补完整路由、组状态取消、re-INVITE 或全员同步。

入口：[独立紧急告警取消：本人、他人及不同成功证据](topics/mcvideo/standalone-emergency-alert-cancellation.md)。

### 离网远程发起 MCVideo 视频推送

- **能回答：**可查请求者 A、实际 caller B、接收者 C 的控制消息、TRYING、私呼调用、结果通知与实际通话端释放责任。
- **只到条件或接口：**固定本版离网单用户到单用户、已授权角色的事件接口；各端按实际收到消息或用户事件读取。调用私呼 helper 不抹去 P0/P1、用户指示、授权、模式及关联守卫。
- **尚未建立的结论：**不将 TRYING 当接通、NOTIFY 当首帧或完整失败通知，也不把 A 的请求权当远程释放权；随机 call identifier 关联、存储恢复、TRYING 编码和失败触发缺口保留，不借在网 push 或未核媒体/配置来源闭合。

入口：[离网远程推视频：三方请求、接通通知与释放边界](topics/mcvideo/offnetwork-remote-video-push.md)。

## MCPTT通话与话权

[查看本域全部主题](topics-calls.json)

### 在网MCPTT通话与普通话权

- **能回答：**可按私呼、组呼、chat及预建立入口查准入、应答、参加/移除、释放，并区分终端、服务端接口与仲裁者的话权状态。
- **只到条件或接口：**普通话权的请求、排队、授予和媒体计时按各自入口读取；入会不等于可发声。
- **尚未建立的结论：**不提供完整SIP/RFC或全部话权状态机；multi-talker有限服务端路径另列，完整准入、排队后继及端到端控制仍未闭合；dual floor、audio cut-in完整控制链未覆盖。

入口：[在网按需私呼：被叫客户端的拒绝、应答和取消](topics/calls/private-client-acceptance.md)；[组呼建立门槛：归属、required应答与最少人数](topics/calls/group-acknowledged-start.md)；[预建立会话承载普通组呼：REFER 寻址、响应与独立通知](topics/calls/preestablished-group-association.md)；[按需 chat 组呼入口：新建与加入都从组 ID 的 initial INVITE 开始](topics/calls/chat-ondemand-entry.md)；[话权状态归谁：客户端、服务器接口与呼叫仲裁分开读取](topics/calls/floor-state-ownership.md)；[入会与请求话权：SIP 成功、接收媒体和发送许可分别判断](topics/calls/floor-participant-entry-request.md)；[服务器授予后的媒体计时：T20 重传、T1 静默与 T2 超时撤销](topics/calls/floor-server-media-timers.md)。

所列入口的来源：3GPP TS24.379 V19.4.0；3GPP TS24.380 V19.1.0。具体Stage、条款及跨源差异以各主题为准。

### 优先话权：撤销而非完整交接

- **能回答：**可查同时协商queueing与mc_priority、有效pre-emptive且策略选revoke的有限分支，队首、T3/T8、旧RTP及G-bit=0终端停止请求。
- **只到条件或接口：**撤销通知、接口转态与终端实际停止分开；队首不等于Granted，媒体组件停止请求不等于已完成。
- **尚未建立的结论：**已协商queueing范围下的下一位Granted与单话权超时交接未闭合；不覆盖override without revoke、dual floor或multi-talker的完整流程。

入口：[优先请求：何时触发撤销，为什么队首仍不等于获权](topics/calls/floor-preemption-decision.md)；[撤销传递：服务端宽限、终端停止请求与交接证据](topics/calls/floor-revoke-observation.md)。

所列入口的来源：3GPP TS24.380 V19.1.0。具体Stage、条款及跨源差异以各主题为准。

### Multi-talker：有限服务端准入、授予与逐人退出

- **能回答：**可查未满额且在允许名单时的接口转交、并发Granted列表/SSRC、已获准RTP处理，以及逐人Release、T1断流和满额优先撤销。
- **只到条件或接口：**固定TS24.380 V19.1.0 Stage3，在网已配置multi-talker的普通组；仲裁者实际收到请求、容量及有效优先级分别判断。满额撤销选择最低优先级许可者并将新请求排队，不是立即Granted；其他talker独立退出。
- **尚未建立的结论：**全部准入、同优先级择人、排队后继、配置互通及完整端到端控制仍未闭合。pending中的其他人Release与T1出口差异保留；不推全组停发、混音/解码或接收端已听到，也不覆盖dual floor或audio cut-in。

入口：[多talker：容量、授予列表与媒体分发](topics/calls/multi-talker-admission-and-media.md)；[多talker：逐人退出与满额撤销](topics/calls/multi-talker-release-and-revoke.md)。

所列入口的来源：3GPP TS24.380 V19.1.0。具体Stage、条款及跨源差异以各主题为准。

### 双话权：保留原发言者的第二路

- **能回答：**可查策略选择同时发言后的 D 仲裁、G-bit 授予、第二路媒体接收集合，以及 T11、T12 和 Release 三种退出。 原主路先退出时另可查 G 的条件接续与 D Terminate；另可区分 D 内部 call release 两阶段动作，不代表完整信令层释放。 同一已获准overriding者再次请求已经到达D时，可查有限Granted回应及接口转交边界。
- **只到条件或接口：**限普通在网组呼所列抢占条件；区分基本 G 与双话权 D，按事件保留计时器条件、通知顺序及接收集合。服务器请求不证明终端已收到或停止。 原主路退出接续保留 D 是否在用、计时器及待处理内容的条件，不将 Terminate 当作新的 Granted。
- **尚未建立的结论：**不覆盖完整终端 G-bit/Ack 路由、接口G/D选择、重发Granted完整回程、其他请求者处置、配置 N7、安全或混音；原文未列的 G-bit 不补默认值。身份与 SSRC 指向差异、接口事件归属及 D 释放后继续发言的解释边界仍未闭合，不推导剩余时长转移或显式资源重绑定。

入口：[双话权：保留原发言者的第二路许可与媒体](topics/calls/dual-floor-entry-and-media.md)；[双话权：第二路停止与原主路退出后的接续](topics/calls/dual-floor-stop-evidence.md)。

所列入口的来源：3GPP TS24.380 V19.1.0。具体Stage、条款及跨源差异以各主题为准。

### 普通离网MCPTT组呼

- **能回答：**可查每组状态机的PROBE、超时发起/加入已有呼叫、用户应答与Confirm mode、周期公告、本端退出和忽略窗口。 话权另可查终接者初始化、silence 请求、T201/C201 竞争与本地许可，以及无排队释放、取消和呼叫停止。 普通BASIC到BASIC合并另可查身份与时间排序守卫、所选SDP与本地话权调用、TFG6/TFG2及独立类型信息存储。
- **只到条件或接口：**呼叫控制按 TS 24.379 V19.4.0，有限 O 话权路径按 TS 24.380 V19.1.0，各自条件不可省略；话权要求离网呼叫已成功建立。本地状态或已发送消息不是全员一致的证明。 合并的S3与T2各自检查完整守卫；话权重启仅到24.379引用接口，不证明旧许可延续或取得新许可。
- **尚未建立的结论：**不覆盖离网私呼、广播、类型变化、普通BASIC有限合并以外的合并、完整 ProSe、安全或话权排队实现；发起者隐式与显式请求入口差异保留，本端退出不等于全组结束。不能与离网 MCVideo 自动私呼合成一个状态机。 跨状态机调度、时钟异常、配置细节及合并后全网收敛未闭合。

入口：[离网MCPTT组呼：先探测，已有则加入、超时则发起](topics/calls/offnetwork-group-probe-and-start.md)；[离网MCPTT组呼：用户接受、确认消息与周期公告](topics/calls/offnetwork-group-acceptance-and-announcement.md)；[离网MCPTT组呼：本端退出、忽略窗口与最大时长](topics/calls/offnetwork-group-local-leave.md)；[离网话权入口：组呼参与者与临时仲裁者](topics/calls/offnetwork-floor-entry.md)；[离网请求竞争：重试、计数复位与本地取得话权](topics/calls/offnetwork-floor-request-contention.md)；[离网停止边界：空队列释放、静默与呼叫退出](topics/calls/offnetwork-floor-release-boundary.md)。 另查[离网MCPTT普通组呼合并：选择另一呼叫与本地切换](topics/calls/offnetwork-group-basic-merge.md)。

所列入口的来源：3GPP TS24.379 V19.4.0；3GPP TS 24.380 V19.1.0。具体Stage、条款及跨源差异以各主题为准。

### 普通离网话权：条件排队与移交观察

- **能回答：**可按逐角色状态查非抢占判定、排队能力与开关、排位匹配、队首授予、用户接受、匹配RTP观察，以及所列重试与取消事件。
- **只到条件或接口：**呼叫已成功建立；普通请求仍须另判非抢占。排位更新、current/candidate调整、Granted、用户接受和旧仲裁者收到RTP各按自身事件，不能合为一次成功。
- **尚未建立的结论：**Queue Position的User ID/Queued User ID冲突、T233表与实际启动入口差异保留；O:queued查询与所列等待出口另见独立主题，仍未闭合队列导入/排序、T204全状态、配置、安全或全员唯一持权。

入口：[离网话权排队与移交：收到授予、用户接受和首包观察](topics/calls/offnetwork-floor-queue-and-handoff.md)。

所列入口的来源：3GPP TS24.380 V19.1.0。具体Stage、条款及跨源差异以各主题为准。

### 离网排队后：查询与条件出口

- **能回答：**可查O:queued排位查询、回复匹配、T204/C204有限重试及到限出口，并区分Deny、他人授予、媒体更新与T203超时重申请。
- **只到条件或接口：**普通离网呼叫已建立，逐角色状态/事件/身份条件分别适用；字段254/255的语义不能自动变成本地退出动作，计数含初发。
- **尚未建立的结论：**current/candidate字段差异及出口未列的清理保持；不覆盖完整状态机、T204全状态、排序/导入、在网Ack或调度员取消移植，不证明远端已移除排队者。

入口：[离网排位查询与等待失效：重试后是否还在排队](topics/calls/offnetwork-floor-queue-query-and-exit.md)。

所列入口的来源：3GPP TS24.380 V19.1.0。具体Stage、条款及边界以主题为准。

### 普通离网MCPTT自动私呼

- **能回答：**可查已知双用户普通自动私呼的发起、自动接受、列明验签失败及基本P/类型Q各自完成事件。 已建呼叫另可查用户释放、RELEASE/ACK正常确认、各端本地清理及P1定时清标识。 发起端P2另可查TFP1/CFP1小于或等于上限、匹配拒绝及用户取消到P3；不闭合取消对端或后续P3算法。 自动终接已发ACCEPT后的P5等待另可查TFP4一般重传与等于上限失败；两入口重叠，不补调度、媒体清理或Q0转换。
- **只到条件或接口：**固定24.379 V19.4.0 PRIVATE CALL、自动模式且发起关联紧急状态false；位置IE按本业务守卫，媒体/话权仅到所引接口。P5因RTP进P4不等于Q0进Q1。 正常释放按基本P与类型Q各自状态和事件，Q0或ACK不证明媒体和所有资源已清理。
- **尚未建立的结论：**MONP接收port TBD及8809 messages措辞、发现/配置、安全和话权内部许可未闭合；不覆盖手动、紧急、完整重传/取消/释放，也不与组呼、在网私呼或MCVideo拼成同一状态机。

入口：[离网MCPTT自动私呼：建立、终接等待与两种控制状态](topics/calls/offnetwork-private-auto-control.md)。 另查[普通离网MCPTT私呼：已建呼叫的释放与本地清理](topics/calls/offnetwork-private-release.md)。 另查[普通自动离网MCPTT私呼：建立等待中的重传、失败与取消](topics/calls/offnetwork-private-auto-setup-exits.md)。 另查[普通自动离网MCPTT私呼：接受响应的重传与等待失败](topics/calls/offnetwork-private-auto-accept-wait.md)。

所列入口的来源：3GPP TS24.379 V19.4.0。具体Stage、条款及边界以主题为准。

### 普通离网MCPTT手动私呼

- **能回答：**可查自动优先后的手动发起资格、两端等待、人工接受/拒绝及超时Reason、P/Q独立完成与接受后TFP4重传/失败。 另按各自状态事件查建立取消、终接收RELEASE、已建正常释放确认及P/Q清理。
- **只到条件或接口：**普通已知双用户、非紧急PRIVATE CALL；按端点、模式和实际状态事件读取。用户接受不等于两端已完成，P的RTP完成不补Q转换；TFP4重叠入口保留。
- **尚未建立的结论：**无ACK重传、竞态调度、完整安全、配置取得、媒体/话权许可和TFP4调度仍未闭合；旧自动主题不能自动成为手动后续流程。

入口：[普通离网MCPTT手动私呼：等待、人工应答与控制完成](topics/calls/offnetwork-private-manual-answer.md)。

所列入口的来源：3GPP TS24.379 V19.4.0。具体条款及边界以主题为准。

### 远程请求另一用户发起普通 MCPTT 私呼

- **能回答：**可查 A 请求 B 向 C 起呼时的角色、请求许可、PF/CF 控制消息路由、B 的实际按需私呼调用及结果返回；A=C 且起呼成功时另有免发结果条件。
- **只到条件或接口：**主系统在网普通按需私呼；角色和 request/response 分支分别适用，B 本地策略选择按需后才调用相应起呼过程。A、B、C 不要求是三个不同身份。
- **尚未建立的结论：**不把控制 MESSAGE 的 200 当作 C 已接听或媒体可听；私呼 helper 仅到本页所列调用契约，排除预建立、组呼、紧急、ambient listening 及优先级/接续覆盖，不把相关私呼页串成完整实现。

入口：[远程请求私呼：谁发起、拨给谁、结果回给谁](topics/calls/remotely-initiated-private.md)。

## 组管理与MCPTT组呼入口

[查看本域全部主题](topics-groups.json)

### 组文档、归属及会议状态

- **能回答：**可查文档/节点操作、XCAP校验与并发、订阅，以及MCPTT组呼入口、显式/隐式归属和会议状态合并。
- **只到条件或接口：**文档权限、成员、归属、入呼权限分别判断；Stage3组文档与业务归属按各自来源，RFC会议合并按订阅版本解释。
- **尚未建立的结论：**不是完整schema/RFC实现或跨域部署算法；归属确认不证明呼叫接受，会议通知不是媒体到达。MCData/MCVideo专有归属须查各自域。

入口：[组文档操作：先选资源层级，再选 HTTP 方法](topics/groups/resource-operations.md)；[XCAP 并发修改：ETag 与 412](topics/groups/conditional-update.md)；[显式归属服务器记录：两侧建立、刷新与通知确认](topics/groups/explicit-affiliation-server-state.md)；[显式归属结果：先订阅状态，再用NOTIFY关联请求](topics/groups/explicit-affiliation-observation.md)；[参与者通知合并：全量、增量与版本断档](topics/groups/conference-state-merge.md)。

所列入口的来源：3GPP TS24.379 V19.4.0；3GPP TS 24.481 V19.3.0；IETF RFC 4825（May 2007）；IETF RFC4575（2006-08）。具体Stage、条款及跨源差异以各主题为准。

### 在网MCPTT按需广播有限信令

- **能回答：**可查普通GMS组无活跃会话时，客户端请求、O-PF转发、CF邀请与有限响应接续。
- **只到条件或接口：**固定24.379 V19.4.0，保留§4.12版本限制；终接Answer-Mode与本端设置/许可按AND(OR)组合。各角色独立检查，Unconfirmed200不等于全员接听。
- **尚未建立的结论：**不覆盖完整广播组创建层级、已有会话加入、预建立广播、重组/紧急/远程、完整失败和媒体/话权内部实现。

入口：[在网广播组呼：按需请求、邀请与接续证据](topics/groups/broadcast-ondemand-signalling.md)。

固定来源及具体条款以主题为准。

### 显式名单初建 MCPTT ad hoc 组呼

- **能回答：**可查客户端、PF、CF 和受邀客户端的独立资格、显式名单与实际组/会话身份、逐成员邀请，以及上游应答与被叫确认的区别。
- **只到条件或接口：**单一主系统普通在网按需初建，显式 MCPTT ID 列表，无已有 ad hoc group ID 或告警后续；各角色按事件与前序判断，发起端不处于会触发优先呼叫的 emergency 状态。
- **尚未建立的结论：**不套预安排组呼 required/最少人数门槛，不把名单、隐式归属或 Unconfirmed200当全员确认；保留显式名单成功响应 criteria 字段来源缺口，不补完整媒体、安全、失败回滚或 criteria 过程。

入口：[显式名单建立 ad hoc 组呼：资格、邀请与应答证据](topics/groups/adhoc-explicit-list-establishment.md)。

### MCPTT ad hoc 按条件选人与持续变化

- **能回答：**可查 criteria 初建的实际调用入口、CF本地选人或PF查询、独立名单结果、持续增删通知及停止确定的状态责任。
- **只到条件或接口：**单主系统普通在网按需 criteria 初建，各角色前序准入仍适用；PF查询列表是可选选择。结果快照、增删通知与释放策略触发的停止是不同事件，不共同继承成功。
- **尚未建立的结论：**不把criteria变成显式名单初建的必经后续，也不修复旧页响应字段来源缺口；保留req-type/resp-type差异、增员历史OR条件及多PF结果边界，不补全局原子替换、实际criteria算法或完整释放。

入口：[按条件建立 ad hoc 组呼：选人、持续变化与停止](topics/groups/adhoc-criteria-membership-lifecycle.md)。

## 身份、注册与配置

[查看本域全部主题](topics-identity.json)

### 身份、注册、令牌与用户配置

- **能回答：**可区分客户端登记、用户认证、SIP注册、服务授权，查令牌刷新、伙伴系统及配置取得/更新的选定边界。
- **只到条件或接口：**配置更新含Stage2信息流，认证/HTTP按对应规范；24.482与33.180的token字段义务差异保留。
- **尚未建立的结论：**未提供完整OIDC/RFC、安全实现或跨版本统一token模板；配置存储确认不证明所有通话即时同步。

入口：[原生客户端认证：注册、授权码与令牌分别做什么](topics/identity/native-authentication.md)；[SIP 注册之后：服务范围、令牌校验与身份绑定](topics/identity/service-authorization.md)；[刷新 access token：不能借刷新扩大授权](topics/identity/token-refresh.md)；[令牌响应字段：两个 Rel19 规范版本不能静默合并](topics/identity/token-response-obligations.md)；[用户配置更新：通知取回与客户端提交](topics/identity/profile-update.md)。

所列入口的来源：3GPP TS 23.280 V19.9.0；3GPP TS24.482 V19.0.0；3GPP TS33.180 V19.4.0。具体Stage、条款及跨源差异以各主题为准。

### MCPTT PUBLISH服务授权与设置

- **能回答：**可查主系统已注册且已有token时，授权加设置PUBLISH的保护、并发上限、身份绑定及客户端/服务器反馈。
- **只到条件或接口：**默认保护与139/140调用层次分别判断；用户上限存在时不再同时取服务上限。绑定先于RFC处理，200先于后续模式/profile/隐式归属处理。
- **尚未建立的结论：**不覆盖完整REGISTER、外部IdM/token校验、配置取得或原子回滚；服务授权不替代具体通话权限、归属或媒体许可。

入口：[MCPTT注册后的服务授权：PUBLISH、身份绑定与设置结果](topics/identity/mcptt-publish-service-authorization.md)。

固定来源及具体条款以主题为准。

## 安全与密钥

[查看本域全部主题](topics-security.json)

### 保护层次与密钥生命周期

- **能回答：**可查组密钥验证、用户切换时材料保存/隔离、私呼与组保护、信令/媒体保护边界。
- **只到条件或接口：**安全专题说明所列条件下的密钥及保护责任；多发言者安全片段仅解释保护/混音限制，不等于完整多发言者控制。
- **尚未建立的结论：**不提供完整密码编码、KMS部署、擦除算法或所有安全失败映射；取得密钥不代表归属、通话或发流获准。

入口：[组密钥下发：收到GMK之前要验证什么](topics/security/group-key-distribution.md)；[UE密钥生命周期：保存、换用户与失效清理](topics/security/ue-key-lifecycle.md)；[在网私呼：PCK 分发完成不等于通话获准](topics/security/private-key-distribution.md)；[多发言者与预配置重组：服务器混音和组密钥前提](topics/security/group-call-media-boundaries.md)。

所列入口的来源：3GPP TS33.180 V19.4.0。具体Stage、条款及跨源差异以各主题为准。

### 离网两用户私呼密钥与保护

- **能回答：**可查普通离网MCPTT/MCVideo私呼的直接UE密钥分发、接收验证及媒体/控制保护材料关系。
- **只到条件或接口：**发现可选；分发、验签、业务应答、媒体许可各有独立入口，不从在线登录/REGISTER推定离网认证步骤。
- **尚未建立的结论：**不覆盖MCData、组GMK、完整呼叫状态机、配置或媒体实现；9.4.4回指差异不据此补齐控制实现。

入口：[离网私呼的密钥分发、验证与保护边界](topics/security/offnetwork-private-key-protection.md)。

固定来源及具体条款以主题为准。

## MCX与LMR互通

[查看本域全部主题](topics-interworking.json)

### MCX与LMR互通

- **能回答：**可查IWF边界、组配置/归属、重组、组呼/私呼、SDS地址映射、话权过滤与位置的信息流。
- **只到条件或接口：**TS23.283 V19.5.0 Stage2；IWF前的本地选中不等于最终Granted，互通MCData范围为SDS。
- **尚未建立的结论：**不代表IWF内部实现、LMR协议编码、全部SIP或媒体互通测试；不能直接当原生MCX Stage3消息配方。

入口：[LMR 互通：IWF 的规范边界](topics/interworking/scope.md)；[归属信息流：服务类型与逐组结果](topics/interworking/affiliation-results.md)；[互通私呼释放：发起方与确认次序](topics/interworking/private-release.md)；[互通SDS：地址映射与代理回执](topics/interworking/sds-addressing.md)；[组话权本地过滤：通过预选不等于最终授予](topics/interworking/floor-filtering.md)。

所列入口的来源：3GPP TS 23.283 V19.5.0。具体Stage、条款及跨源差异以各主题为准。

## 位置服务

[查看本域全部主题](topics-location.json)

### 位置采集、订阅与历史

- **能回答：**可查配置触发/按需采集、按当前归属用户的订阅、通知、取消及恢复报告后的历史补报。
- **只到条件或接口：**相关采集、订阅和历史流程限TS23.280 V19.9.0所列单MC系统Stage2场景；报告可用信息不保证新测量或精度，位置传播权限单独判断。
- **尚未建立的结论：**不覆盖完整定位算法、配置IE/Stage3编码、历史容量/保留/删除策略或每次移动都被记录的保证。

入口：[位置采集：配置触发与按需上报](topics/location/report-acquisition.md)；[位置订阅：动态组目标、通知与取消](topics/location/subscription-lifecycle.md)；[恢复位置上报后：历史补报与取消](topics/location/history-recovery.md)；[位置：传播权限与保护要求](topics/location/privacy.md)。

所列入口的来源：3GPP TS 22.280 V19.7.0；3GPP TS 23.280 V19.9.0。具体Stage、条款及跨源差异以各主题为准。

## 网络策略与QoS

[查看本域全部主题](topics-network-policy.json)

### EPS/5GS QoS与MCPTT用途

- **能回答：**可区分QFI/5QI/ARP、GBR通知，及MCPTT语音和MCPTT-4/9的5QI65与SIP-1的69；按部署选择SIP core或服务器资源模型。
- **只到条件或接口：**MCPTT用途固定TS23.289 V19.7.0 Stage2；服务器模型区分客户端/锚点参数，客户端确认早于资源请求与分配结果。
- **尚未建立的结论：**通用N5 Stage3授权输入与结果另列，仍未建立MCX实际接口绑定、完整可运行N5/Rx/N33请求、PCC到QFI/包过滤器及UPF执行链或语音质量验收；不保证与23.501 V19.8.0等快照的组合互通。

入口：[5GS QoS：QFI、5QI 与 ARP 分别决定什么](topics/network-policy/5gs-qos-model.md)；[GBR 无法保障时：通知不等于立即释放](topics/network-policy/5gs-notification-control.md)；[MCPTT 语音进 5GS：语音 QoS 与 SIP 信令的边界](topics/network-policy/mcptt-5gs-voice-qos-scope.md)；[MCPTT 服务器请求单播资源：端点与完成证据](topics/network-policy/mcptt-5gs-server-resource-request.md)。

所列入口的来源：3GPP TS 23.289 V19.7.0；3GPP TS 23.501 V19.8.0。具体Stage、条款及跨源差异以各主题为准。

### 通用N5：AF上下文与资源结果

- **能回答：**可查IP类型PDU会话的AF上下文创建、UE地址及绑定输入、媒体组件/流过滤器、应用标识优先关系、服务拒绝，以及201、订阅、成功/失败资源通知和204的不同证据。
- **只到条件或接口：**固定TS29.514 V19.5.0 Stage3，AF已获使用服务授权，限普通单播、单接入和所列基本创建/通知。成功通知只覆盖所报告流；正常通知204是接收确认，不把所有不可接受POST都强制解释为204。
- **尚未建立的结论：**不等于MCX已绑定该API；完整安全、schema、过滤语法、session binding、PCC/SMF执行及UPF转发未建立。未验证MCX SDP到全部字段、PCC到QFI/包过滤器的完整链；201、资源通知均不能证明业务权限、话权或媒体交付，失败也不等于全会话释放。

入口：[N5授权请求：应用、媒体和流如何区分](topics/network-policy/n5-af-session-input.md)；[N5授权结果：201与资源分配通知分别证明什么](topics/network-policy/n5-authorization-result-boundary.md)。

所列入口的来源：3GPP TS 29.514 V19.5.0。具体Stage、条款及跨源差异以各主题为准。

### 通用 N5：已有 AF 会话的更新与终止

- **能回答：**可查 PATCH 修改媒体与门控、会话级订阅全量替换和移除、更新拒绝，以及 POST 删除、PCF terminate 通知和条件资源清理请求。
- **只到条件或接口：**固定 TS 29.514 V19.5.0 的普通 IP、单播、单接入及已有上下文；更新页要求支持 PatchCorrection。200/204、终止确认、上下文删除和 PCC/SMF 清理分别判断。
- **尚未建立的结论：**Retry-After 正文与表格强度差异不裁决；完整 schema、RFC 合并语义、全部错误/特性和下游执行未建立。通用 API 不证明 MCX 媒体绑定、QFI 映射、UPF 已执行或媒体已停。

入口：[N5 会话更新：媒体变更、订阅替换与生效证据](topics/network-policy/n5-session-update.md)；[N5 会话终止：删除请求、PCF 通知与资源清理](topics/network-policy/n5-session-termination.md)。

所列入口的来源：3GPP TS 29.514 V19.5.0。具体Stage、条款及跨源差异以各主题为准。

### MCData预建立共享：支持、绑定与执行

- **能回答：**可区分SIP-core与直接Rx路径、逐流Resource-Share应答、ResShare特性交集、IP-CAN绑定和方向共享键，并判断AAA、停止共享及AF终止的有限证据。
- **只到条件或接口：**MCData限普通在网SDS预建立用途；Rx限所列AF/PCRF语境，P-CSCF规则不直接套给PF。注册UE绑定不替代IP-CAN绑定，支持共享不证明独立媒体资源。
- **尚未建立的结论：**24.229的头语法/映射/触发、29.212/213的共享执行和完整绑定未闭合；不提供完整共享实现、N5/5GS适配或媒体交付保证。

入口：[MCData 预建立共享资源：SIP 支持、Rx 绑定与完成证据](topics/network-policy/mcdata-preestablished-resource-sharing-boundary.md)。

所列入口的来源：3GPP TS24.282 V19.7.0；3GPP TS 29.214 V19.3.0。具体Stage、条款及跨源差异以各主题为准。

### N5：GBR目标变化与流范围

- **能回答：**可区分QOS_NOTIF订阅、PCF获知目标不再保证或恢复保证后的报告，以及qncReports和Flows内两层省略范围。
- **只到条件或接口：**固定TS29.514 V19.5.0普通IP、单播、单接入；恢复是GBR目标又可保证，不是资源分配结果。无MediaComponentVersioning时省略flows才按全会话解释；Flows项省略fNums仅该组件全部流。
- **尚未建立的结论：**不覆盖方向、替代QoS、内容版本或完整QoS测量、SMF检测执行链。204只确认通知，PATCH可选；不证明QFI绑定、MCX媒体恢复或交付。

入口：[N5 GBR 目标通知：不再保证、恢复保证与受影响流](topics/network-policy/n5-gbr-qos-notification.md)。

所列入口的来源：3GPP TS 29.514 V19.5.0。具体Stage、条款及边界以主题为准。

## SIP路由

[查看本域全部主题](topics-signalling.json)

### SIP注册器与对话路由

- **能回答：**可区分注册器寻找/绑定责任与RFC3261的对话标识、remote target和route set。
- **只到条件或接口：**注册器模型是TS23.280 V19.9.0 Stage2；对话规则为RFC基线，RFC本身没有3GPP Release。
- **尚未建立的结论：**不覆盖完整MCX SIP profile、事务匹配、连接复用、负载均衡亲和、故障切换或注册状态复制。

入口：[SIP 路由：寻找注册器与保存用户绑定](topics/signalling/registrar-routing.md)；[SIP 对话内请求：标识、目标与路由集](topics/signalling/dialog-routing.md)。

所列入口的来源：3GPP TS 23.280 V19.9.0；IETF RFC 3261（June 2002）。具体Stage、条款及跨源差异以各主题为准。

## 紧急与优先状态

[查看本域全部主题](topics-emergency.json)

### 紧急状态、告警与优先变更

- **能回答：**可区分Stage1紧急状态要求与MCPTT/MCData/MCVideo已覆盖的升级、本人取消、告警和服务器结果。
- **只到条件或接口：**业务、对象与入口分别适用；紧急优先级取消不是BYE，200、Warning149、INFO、ACK也不是同一结果。
- **尚未建立的结论：**不把一种业务的组/私呼规则移到另一种；取消授权FFS、错引和部分状态路径仍保留，不代表完整紧急媒体、远程取消或所有优先模式已覆盖。

入口：[紧急告警、状态与组通信](topics/emergency/alert-state.md)；[已有私呼升级紧急：呼叫与告警的不同结果](topics/emergency/private-upgrade.md)；[紧急私呼取消：降级、告警与失败恢复](topics/emergency/private-downgrade.md)；[私聊 SDS 紧急取消：权限未决说明与部分接受结果](topics/mcdata/private-emergency-server-cancellation.md)；[私呼本人取消：通话、告警与用户状态分开处理](topics/mcvideo/private-emergency-client-cancellation.md)。

所列入口的来源：3GPP TS 22.280 V19.7.0；3GPP TS24.281 V19.3.0；3GPP TS24.282 V19.7.0；3GPP TS24.379 V19.4.0。具体Stage、条款及跨源差异以各主题为准。

### 已建MCPTT组呼取消紧急状态

- **能回答：**可查普通按需预安排已建组呼取消in-progress emergency的客户端、PF、CF责任，许可/拒绝及本人、他人或不取消告警的替代分支。
- **只到条件或接口：**固定24.379 V19.4.0 Stage3，各角色和事件独立；响应、下游通知与用户告警状态不是单一全局成功。
- **尚未建立的结论：**不覆盖私呼、chat、广播、预建立、离网或完整组状态机；不是Stage1要求的直接实现证明，也不是退出或释放通话。

入口：[通话中取消组紧急状态：授权、拒绝与告警结果](topics/emergency/group-inprogress-cancel.md)。

固定来源及具体条款以主题为准。

### 已建MCPTT组呼升级紧急状态

- **能回答：**可查普通已建按需预安排组呼升级紧急的客户端/PF/CF权限、组状态与alert字段，以及响应、INFO和失败反馈。
- **只到条件或接口：**各角色按独立事件与状态检查；客户端许可、CF许可与告警成功不合并为全局前提。
- **尚未建立的结论：**不覆盖初始紧急起呼、chat/广播/预建立/离网或完整组状态机；不与私呼、Stage1或组取消拼成必经链。

入口：[已有组呼升级紧急：权限、组状态与告警反馈](topics/emergency/group-inprogress-upgrade.md)。

固定来源及具体条款以主题为准。

### 独立 MCPTT 组紧急告警

- **能回答：**可查 DedicatedGroup 独立告警的客户端许可与目标、PF 绑定检查、CF 独立授权与通知，以及 MEA 响应和成员提示的证据边界。
- **只到条件或接口：**主系统在网、目标非 ad hoc 既有组无正在进行的通话，发起者已归属；各角色权限及事件独立适用，不把原请求 2xx、CF 接收指示和全员接收混为一项结果。
- **尚未建立的结论：**不覆盖 UseCurrentlySelectedGroup 的构造缺项、隐式归属、取消、跨系统或完整 SIP/保护/失败恢复；独立指示的身份回指差异保留，不推导组呼建立或用户已读。

入口：[独立组紧急告警：MESSAGE 发起、分发与确认边界](topics/emergency/standalone-group-alert.md)。

### 独立 MESSAGE 取消 MCPTT 组告警

- **能回答：**可查本人或指定他人告警取消的请求字段、PF 身份检查、CF 实际分派与指定缓存清理，以及请求者和通知接收者的状态条件。
- **只到条件或接口：**各角色分别进入；CF 的明确取消分支要求组已有 ongoing 通话且存在未结告警，客户端与接收者不共同继承这两个守卫。仅取消告警，不附带 emergency-ind=false 的组状态取消。
- **尚未建立的结论：**无通话纯告警取消的 CF caller 未闭合，不能由客户端可发起就跳入 helper；取消授权回指、通知收件人范围和接收指示身份差异保留，不证明全组同步、通话释放或完整互通。

入口：[独立 MESSAGE 取消组告警：本人、他人与结果条件](topics/emergency/standalone-alert-cancellation.md)。

## 阅读结果时仍须分开的证据

授权不等于可达；归属不等于参加；会话建立不等于媒体许可；发送/转发/排队不等于交付；收到或下载不等于阅读与应用完成；单端释放不等于所有参与者同时停止。完整的端到端结论需要各阶段对应证据，不能用一个响应码或一个状态替代。
