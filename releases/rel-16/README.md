# Release 16

当前仅覆盖八项固定规范版本的局部范围，包括独立的 Stage 2 功能解释和 Stage 3 程序，整版尚未完成。

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

先读主题共同条件，再按实际角色与事件选取结论；不把拒绝、应答、取消或后续数据处理拼成同时必备的条件。这些主题均不构成完整端到端实现，也不证明版本组合互通。

[业务域](domains.json) · [主题索引](topics.json) · [条件阅读路径](reading-paths.json) · [覆盖边界](coverage.md) · [来源](sources.json) · [状态](status.json)

仅所列版本与条款作为依据，不继承 Release 19 的结论或核验状态。未覆盖的服务端链、媒体、安全与其他业务须另查对应版本的规范。
