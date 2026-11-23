# Release 16

本版只收录所列固定版本的部分条款，不用其他 Release 补齐。Stage 1 写业务需求，Stage 2 写功能职责与流程，Stage 3 写具体信令与媒体处理；不能互相替代。

查到标为 `draft` 的主题，不等于其中的条款没有核对。请按具体问题阅读正文与声明，看相应层级实际登记的核验；[主题状态与核验字段的读法](../../CONTRIBUTING.md)列出了区别。

## 按问题查

- [MCPTT 呼叫与设置、MCPTT/MCVideo 跨系统私呼、MCVideo/MCData 在网区域告警、在网组告警位置与取消与离网组紧急告警](topics-calls.json)：[普通私呼的服务器怎样检查准入](topics/calls/private-server-admission-routing.md)？ [谁能远程发起或终止从另一位用户终端开展的通信](topics/calls/remote-communication-control.md)？[在网组通信没人预先确认，还能继续吗](topics/calls/onnetwork-group-acknowledgement.md)？紧急呼叫、重入、预建立会话与服务设置分别由谁处理？ [LMR 互通组呼已开始，另一侧怎样晚入](topics/calls/lmr-interworking-group-late-entry.md)？ [MCPTT 和 LMR 自动开始私呼，谁能重试、谁管话权](topics/calls/lmr-interworking-private-auto-setup.md)？ [离开预设区域后，谁决定取消 MCVideo 或 MCData 告警](topics/calls/emergency-alert-area-entry-exit.md)？ [MCPTT 或 MCVideo 跨系统私呼时，哪边找系统、哪边找服务器](topics/calls/partner-private-call-routing.md)？
- [MCPTT 话权与预建立会话的 Connect 应答、MCPTT/MCVideo 跨系统组呼媒体](topics-media.json)：在网由谁授予或撤销话权？[离网参与者](topics/calls/offnetwork-floor-participant.md)怎样请求、排队或交接？ 跨系统组呼由伙伴复制媒体时，[宿主向伙伴发几条流，谁复制给组员](topics/media/partner-group-media-replication.md)？ 在网 MCPTT 预建立会话里[第二份 Connect/Accepted 是另一通呼叫吗](topics/media/preestablished-connect-outcome.md)？ [LMR 互通组的话权由谁最终决定](topics/media/lmr-interworking-group-floor-arbitration.md)？ [不同 MC 业务并行时，终端资源冲突怎么办](topics/media/concurrent-services-ue-resources.md)？ [用户收到媒体后能转给谁](topics/media/user-media-forwarding.md)？ [实时通信发送者能否收到接收或显示通知](topics/media/realtime-receipt-notification.md)？
- [组归属与组动态数据](topics-groups.json)：[在网组通信怎样比较传输和呈现优先级](topics/groups/onnetwork-group-communications-priority.md)？ [谁能远程改其他用户的归属组或选定组](topics/groups/onnetwork-remote-group-change.md)？ [谁能查已归属名单或自动收变化](topics/groups/onnetwork-affiliated-member-list.md)？ [哪些广播组能自动归属，业务何时须能阻止撤销](topics/groups/onnetwork-affiliation-and-revocation.md)？ [在网组的归属、接收状态和所选组怎么看](topics/groups/onnetwork-group-status-information.md)？ [跨域临时重组的组密钥怎样发给两侧成员](topics/groups/partner-regroup-gmk.md)？ [协商式归属请求送达](topics/groups/negotiated-affiliation-client.md)是否等于用户同意？怎样观察本客户端的归属或订阅组动态数据？ [LMR 电台呼叫 MCPTT 定义的组，要逐人归属吗](topics/groups/mc-hosted-lmr-affiliation.md)？ [同组一次选两项业务，能只准一项吗](topics/groups/common-group-service-affiliation.md)？
- [MCData](topics-mcdata.json)：[有 LMR 用户的组短数据，组地址和收件人怎样区分](topics/mcdata/lmr-group-standalone-sds.md)？ 私聊 SDS 走哪条信令或媒体路径？HTTP 文件分发中，[服务器受理](topics/mcdata/http-fd-server.md)和[客户端下载](topics/mcdata/http-fd-client.md)有何区别？离网消息怎样封装？[数据负载保护和发送者认证怎样区分](topics/mcdata/payload-protection-and-authentication.md)？
- [MCVideo](topics-mcvideo.json)：谁能发起视频呼叫，发送和接收许可如何区分？[组呼下行怎样选择组播或单播](topics/mcvideo/mbms-group-downlink.md)？
- [用户身份](topics-identity.json)：[在网组通信给接收端哪些身份，给用户看哪些别名](topics/identity/onnetwork-group-sender-identification.md)？ [多个任务关键组织共用系统时谁能看或改参数](topics/identity/shared-system-organization-management.md)？ [同一用户能登录几台终端，谁能让谁远程退出](topics/identity/multiple-device-login.md)？[同一用户跨业务或跨终端时，用哪些标识对应](topics/identity/cross-service-user-mapping.md)？[终端重启或换人登录后，哪些密钥要留、哪些要删](topics/identity/ue-key-persistence.md)？ [查到对端 KMS URI，为什么还会收到 KRR](topics/identity/kms-redirect-response.md)？
- [公共承载](topics-bearers.json)：[执行优先级决定时怎样管理不同 MC 业务的数据流](topics/bearers/cross-service-priority.md)？[MBMS 承载暂停时，没被要求上报的客户端还要检测吗](topics/bearers/mbms-suspension-reporting.md)？ [LTE 站回传断了，IOPS 要保留哪些本地 MCPTT 能力](topics/bearers/iops-local-mcptt-service.md)？
- [位置服务](topics-location.json)：[LMC 发位置消息怎样带令牌，LMS 验不过怎么办](topics/location/lmc-lms-access-token.md)？ [一条周期位置消息适用于哪些业务或组](topics/location/periodic-message-scope.md)？[初次注册何时可能触发终端上报位置？LMS 是否因此须另发配置？](topics/location/event-reporting-configuration.md)

知道主题名可直接查[全部主题](topics.json)；想对照另一角色或相邻程序，查[相关问题](reading-paths.json)。判断某次通信是否进入某个分支时，再核对该分支的角色、状态与消息。

[业务域](domains.json) · [覆盖边界](coverage.md) · [固定版本与来源](sources.json) · [本版状态](status.json)
