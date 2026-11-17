# N5授权结果：201与资源分配通知分别证明什么

## 适用范围

- 固定TS29.514 V19.5.0；通用Stage3 AF/NF service consumer与PCF间的IP类型PDU会话授权，AF已获使用服务的授权。
- 只讨论普通单播、单接入和基本创建/结果通知；不覆盖Ethernet、TSN/TSC、MA PDU、紧急/优先呼叫及其专用优先化、替代QoS和内容版本扩展。
- 用于理解MCX可采用的N5授权接口，不证明某MCX实现已绑定该API或已验证版本组合；不提供完整可运行请求或安全接入配置。

## 服务拒绝与无效信息

适用主体：PCF。

适用条件：已收到服务信息，按运营商策略处理；服务被拒或信息无效/不足。

服务不获授权时403/REQUESTED_SERVICE_NOT_AUTHORIZED，可带acceptableServInfo；无效或不足时400/INVALID_SERVICE_INFORMATION。

- 不穷举错误；可接受参数不是资源已经分配，也不授权自动改请求。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2，印刷页 24。

## 201只确认上下文已创建

适用主体：PCF。

适用条件：Individual Application Session Context资源已经创建。

返回201、Location及AppSessionContext资源表示；Location指向创建的上下文。PCF另须检查PCC规则创建/配置需求并按引用规范向SMF配置。

- 201证明上下文创建，不单独证明资源分配、QFI绑定成功或媒体到达；TS29.512/29.513下层流程未核。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2，印刷页 25、26。

## 订阅与资源结果分开

适用主体：NF service consumer/PCF。

适用条件：请求资源分配成功和/或失败通知。

evSubsc带events和通知notifUri；按所需结果订阅SUCCESSFUL_RESOURCES_ALLOCATION和/或FAILED_RESOURCES_ALLOCATION。PCF设置相应PCC规则结果订阅。

- 订阅成功不是结果通知；UEUnreachable扩展不在本页范围。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2;4.2.2.10，印刷页 23、32、33。

## 成功通知只覆盖所报告流

适用主体：PCF/NF service consumer。

适用条件：先前订阅成功事件，PCF获知一个或多个SDF资源已分配；无替代QoS或内容版本扩展。

PCF向订阅notifUri追加notify后POST EventsNotification，带evSubsUri及evNotifs成功事件；非全部流受影响时带flows；消费者以204确认。

- 成功只覆盖所报告流；204仅确认通知。不能据此证明MCX业务权限、发送权、RTP到达或可听/可见媒体。
- 这里的204限于正常资源结果通知：§4.2.5.8 p94规定收到后确认；§4.2.5.2 p88另区分接受时回204、不接受时按§5.7报告拒绝原因，以及支持ES3XX且消费者判断需要重定向时的重定向响应。不能扩成任意不可接受POST一律204；§5.7完整错误处理未核，204仍不证明媒体或业务成功。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.2，印刷页 87、88。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.8，印刷页 93、94。

## 失败通知不等于全会话释放

适用主体：PCF/NF service consumer。

适用条件：先前订阅失败事件，PCF获知一个或多个SDF资源无法分配；单接入、无内容版本扩展。

通知FAILED_RESOURCES_ALLOCATION，并在failedResourcAllocReports中以mcResourcStatus报告相关PCC规则active/inactive状态；非全部流受影响时带flows；消费者以204确认。

- 不能推全会话已释放、所有流均失败或客户端必须挂断；消费者后续处置未在此规定。
- 这里的204限于正常资源结果通知：§4.2.5.8 p94规定收到后确认；§4.2.5.2 p88另区分接受时回204、不接受时按§5.7报告拒绝原因，以及支持ES3XX且消费者判断需要重定向时的重定向响应。不能扩成任意不可接受POST一律204；§5.7完整错误处理未核，204仍不证明媒体或业务成功。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.2，印刷页 87、88。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.8，印刷页 93、94。

## 证据边界

- TS29.513绑定/PCC流程、TS29.512到SMF的执行、TS29.500安全与错误框架、TS29.214过滤约束及完整schema未核，不能生成声称可运行的请求。
- 尚未建立MCX媒体SDP到全部API字段、授权PCC规则到QFI/包过滤器、实际UPF转发的验证链；资源通知也不能替代业务或媒体收发证据。
- 未声称本版最新；不以Rel19标签推定与TS23.289 V19.7.0及其他已发布版本组合互通。

## 按需继续

- 要解释GBR目标不再保证/恢复保证，而不是资源分配成功或失败，查[N5 GBR 目标通知：不再保证、恢复保证与受影响流](n5-gbr-qos-notification.md)。
- 需区分 terminate 确认、删除响应与资源清理时，查[N5 会话终止：删除请求、PCF 通知与资源清理](n5-session-termination.md)。
- 需区分更新响应与 PCC 执行结果时，查[N5 会话更新：媒体变更、订阅替换与生效证据](n5-session-update.md)。
- [N5授权请求：应用、媒体和流如何区分](n5-af-session-input.md)
- [MCPTT 语音进 5GS：语音 QoS 与 SIP 信令的边界](mcptt-5gs-voice-qos-scope.md)
- [MCPTT 服务器请求单播资源：端点与完成证据](mcptt-5gs-server-resource-request.md)

[3GPP TS 29.514 V19.5.0](https://www.etsi.org/deliver/etsi_ts/129500_129599/129514/19.05.00_60/ts_129514v190500p.pdf)；仅所列版本和条款。
