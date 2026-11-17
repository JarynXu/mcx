# N5 会话终止：删除请求、PCF 通知与资源清理

## 适用范围

- 固定 3GPP TS 29.514 V19.5.0，Release 19，Stage 3；对象为已创建的 Individual Application Session Context，NF service consumer 已获使用该服务的授权。
- 仅普通 IP 类型、单播、单接入的通用 AF/PCF 用途；不把该 API 等同于 MCX 已部署绑定，也不保证与 TS 23.289 或其他精确版本互通。
- 不覆盖 Ethernet、ATSSS、多模态、TSC、紧急/优先化、内容版本、SIP forking、替代 QoS、完整错误/重定向处理及 TS 29.512/29.513 下层执行。API 响应、PCC 操作和实际媒体收发分别判断。

## Delete 操作使用 POST，删除父子资源

适用主体：NF service consumer / PCF。

适用条件：AF 会话结束；其上下文由 §4.2.2 或 §4.2.6.3 创建。

消费者须调用 Npcf_PolicyAuthorization_Delete，但 HTTP 方法是 POST，目标为 {apiRoot}/npcf-policyauthorization/v1/app-sessions/{appSessionId}/delete。该自定义操作删除 PCF 中既有的 Individual Application Session Context 及其子 Events Subscription 资源。

规范强度：调用、方法及 URI 为 SHALL；删除资源范围为操作定义。

- 服务操作名称 Delete 不表示 HTTP DELETE；不是仅删除订阅，也不是直接删除 PDU 会话。

依据：3GPP TS 29.514 V19.5.0 §4.2.4.2，印刷页 81、82。

依据：3GPP TS 29.514 V19.5.0 §5.3.3.4.1;5.3.3.4.2.2，印刷页 126。

## 删除响应与所请求事件信息

适用主体：NF service consumer / PCF。

适用条件：消费者发起终止请求；PCF 接受该 POST。

消费者可在请求体附 EventsSubscReqData 以请求删除时的事件报告。需要报告事件信息时，PCF 返回 200 及包含 evsNotif/evNotifs 的上下文部分表示；所需信息尚不可用时，必须推迟响应并立即请求 SMF 提供。否则返回 204。200 与 204 均属于该上下文资源已删除的成功情况。

规范强度：请求事件信息为 MAY；接受后的分支响应及待取信息时延迟响应为 SHALL。

- 具体 sponsored usage、ANI、RAN-NAS 事件产生规则未核，不据可选请求体断言任意事件可取；拒绝时依 §5.7 报原因。

依据：3GPP TS 29.514 V19.5.0 §4.2.4.2，印刷页 81、82。

依据：3GPP TS 29.514 V19.5.0 §5.3.3.4.2.2 Tables 5.3.3.4.2.2-1/2，印刷页 126、127。

## 响应之后的 PCC 清理义务

适用主体：PCF。

适用条件：§4.2.4.2 终止请求已接受并按规定响应。

随后 PCF 必须释放与已删除 AF 上下文对应 SDF 的网络资源；为此，若尚未执行，须按 TS 29.512 向 SMF 发起相关 PCC 规则的移除请求。

规范强度：释放义务及尚未执行时发起规则移除为 SHALL。

- 资源删除响应不是 SMF/UPF 清理完成、全部 PDU 会话释放或终端停播的确认；下层请求的完成、失败恢复和计时未核。

依据：3GPP TS 29.514 V19.5.0 §4.2.4.2，印刷页 82。

## PCF 终止通知的地址与载荷

适用主体：PCF。

适用条件：PCF 判断 AF 应用上下文已不再有效。

PCF 使用创建上下文时收到的通知 URI，并在末尾追加 terminate，通过 POST 发送 TerminationInfo。载荷包含 resUri 和 termCause，用于触发消费者请求上下文终止；这是与事件通知 URI 的 notify 路径不同的用途。

规范强度：发送及标识/原因字段为 SHALL。

- 原因各自有条件；例如 ALL_SDF_DEACTIVATION 指全部 SDF 停用或全部资源分配失败且不是 PS_TO_CS_HAN 原因，不能从单个流失败推导整上下文无效。本页不穷举 termCause 或特性门槛。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.3，印刷页 89、90。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.2，印刷页 87。

## 接受终止通知后仍须调用 Delete

适用主体：NF service consumer。

适用条件：收到 PCF 的上下文终止 POST；按是否接受分别处理。

接受时消费者须以 204 确认该终止请求，并另向 PCF 调用 Npcf_PolicyAuthorization_Delete。不接受时按 §5.7 返回拒绝原因；支持 ES3XX 且判断需要重定向时，按所引 TS 29.500 处理。

规范强度：接受后的确认及 Delete 调用为 SHALL；拒绝与有条件重定向分别处理。

- 204 是收到并接受终止请求的确认，不替代后续 Delete 操作的响应或网络清理证明；未断言这两个请求的网络交付顺序或未规定的超时重试算法。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.3，印刷页 90。

## 证据边界

- RFC 7396、TS 29.500、TS 29.512、TS 29.513 和 TS 29.214 引用机制未在本次独立核原文；不提供可运行 API 请求模板。
- 没有实网操作或跨版本互操作测试；更新成功、资源删除、PCC 移除请求及终端媒体状态不能合并。

## 按需继续

- [N5 会话更新：媒体变更、订阅替换与生效证据](n5-session-update.md)
- [N5 授权请求：应用、媒体和流如何区分](n5-af-session-input.md)
- [N5 授权结果：201 与资源分配通知分别证明什么](n5-authorization-result-boundary.md)

[3GPP TS 29.514 V19.5.0，ETSI 官方发布版](https://www.etsi.org/deliver/etsi_ts/129500_129599/129514/19.05.00_60/ts_129514v190500p.pdf)；仅适用于所列版本和条款。
