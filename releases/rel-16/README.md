# Release 16

当前仅覆盖两项固定规范版本的 Stage 3 局部流程，整版尚未完成。

- [普通按需私呼：客户端应答与建立证据](topics/calls/private-client-answer-evidence.md)：TS 24.379 V16.14.0。
- [普通私聊 SDS 控制面：发送资格、请求与接收证据](topics/mcdata/sds-control-client.md)：TS 24.282 V16.13.0。

- [普通按需私呼：服务器准入与身份路由](topics/calls/private-server-admission-routing.md)：与对应客户端主题分开核对实际角色和事件。
- [普通私聊SDS控制面：服务器准入、目标路由与响应证据](topics/mcdata/sds-control-server.md)：与对应客户端主题分开核对实际角色和事件。

先读主题共同条件，再按实际角色与事件选取结论；不把拒绝、应答、取消或后续数据处理拼成同时必备的条件。这些主题均不构成完整端到端实现，也不证明版本组合互通。

[业务域](domains.json) · [主题索引](topics.json) · [条件阅读路径](reading-paths.json) · [覆盖边界](coverage.md) · [来源](sources.json) · [状态](status.json)

仅所列版本与条款作为依据，不继承 Release 19 的结论或核验状态。未覆盖的服务端链、媒体、安全与其他业务须另查对应版本的规范。
