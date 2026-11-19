# Release 16

本版只收录所列固定版本的部分条款，不用其他 Release 补齐。Stage 2 说明功能职责，Stage 3 说明具体信令与媒体处理；两者不能互相替代。

查到标为 `draft` 的主题，不等于其中的条款没有核对。请按具体问题阅读正文与声明，看相应层级实际登记的核验；[主题状态与核验字段的读法](../../CONTRIBUTING.md)列出了区别。

## 按问题查

- [MCPTT 呼叫与设置、MCPTT/MCVideo 跨系统私呼、MCVideo/MCData 区域紧急告警](topics-calls.json)：[普通私呼的服务器怎样检查准入](topics/calls/private-server-admission-routing.md)？紧急呼叫、重入、预建立会话与服务设置分别由谁处理？ [离开预设区域后，谁决定取消 MCVideo 或 MCData 告警](topics/calls/emergency-alert-area-entry-exit.md)？ [MCPTT 或 MCVideo 跨系统私呼时，哪边找系统、哪边找服务器](topics/calls/partner-private-call-routing.md)？
- [MCPTT 话权与跨系统组呼媒体](topics-media.json)：在网由谁授予或撤销话权？[离网参与者](topics/calls/offnetwork-floor-participant.md)怎样请求、排队或交接？ 跨系统组呼由伙伴复制媒体时，[宿主向伙伴发几条流，谁复制给组员](topics/media/partner-group-media-replication.md)？
- [组归属与组动态数据](topics-groups.json)：[协商式归属请求送达](topics/groups/negotiated-affiliation-client.md)是否等于用户同意？怎样观察本客户端的归属或订阅组动态数据？
- [MCData](topics-mcdata.json)：私聊 SDS 走哪条信令或媒体路径？HTTP 文件分发中，[服务器受理](topics/mcdata/http-fd-server.md)和[客户端下载](topics/mcdata/http-fd-client.md)有何区别？离网消息怎样封装？
- [MCVideo](topics-mcvideo.json)：谁能发起视频呼叫，发送和接收许可如何区分？[组呼下行怎样选择组播或单播](topics/mcvideo/mbms-group-downlink.md)？
- [用户身份](topics-identity.json)：[同一用户跨业务或跨终端时，用哪些标识对应](topics/identity/cross-service-user-mapping.md)？
- [公共承载](topics-bearers.json)：[MBMS 承载暂停时，没被要求上报的客户端还要检测吗](topics/bearers/mbms-suspension-reporting.md)？
- [位置服务](topics-location.json)：[初次注册何时可能触发终端上报位置？LMS 是否因此须另发配置？](topics/location/event-reporting-configuration.md)

知道主题名可直接查[全部主题](topics.json)；想对照另一角色或相邻程序，查[相关问题](reading-paths.json)。判断某次通信是否进入某个分支时，再核对该分支的角色、状态与消息。

[业务域](domains.json) · [覆盖边界](coverage.md) · [固定版本与来源](sources.json) · [本版状态](status.json)
