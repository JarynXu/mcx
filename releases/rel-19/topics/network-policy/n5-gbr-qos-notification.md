# N5 GBR 目标通知：不再保证、恢复保证与受影响流

## 适用范围

- 固定 3GPP TS 29.514 V19.5.0，Release 19，Stage 3；通用 AF/NF service consumer 与 PCF 的 N5 授权接口，消费者已获使用服务的授权。
- 仅普通 IP、单播、单接入的 AF 会话及 GBR 目标通知；不覆盖替代 QoS、ExtQoSR19 方向扩展、MediaComponentVersioning、EnQoSMon 子组件订阅、紧急/优先化或完整 QoS Monitoring 测量链。
- 所有声明继承本范围，再加各自事件条件。通知用于解释网络报告，不证明 MCX 已绑定该接口、跨规范版本互通、媒体权限、QFI 映射或端到端媒体交付。

## 订阅的是目标变化，不是分配结果

适用主体：NF service consumer / PCF。

适用条件：消费者在创建请求中要求获知一个或多个 SDF 的 GBR QoS 目标不再能保证或又能保证。

消费者使用 evSubsc 的 EventsSubscReqData，在 events 中提供 event=QOS_NOTIF，并提供事件通知 notifUri。PCF 按创建过程响应，并为相应 PCC 规则设置 QoS notification control 订阅。

规范强度：所选订阅的事件、URI 及 PCF 设置义务为 SHALL；不意味着每个 AF 会话都必须订阅。

- 订阅配置不是 GBR 目标已满足的报告；PCC/SMF 设置转引 TS 29.512，下层实际检测机制未核。
- QOS_NOTIF 不是资源分配成功/失败事件的别名；不能用既有 allocation 订阅代替它。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2 event-subscription paragraph，印刷页 23。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.6，印刷页 28。

- §4.2.2.6 NOTE 说明无线接入网中的不能保证可能是暂时或永久；通知本身不给出持续时间或恢复期限。

## PCF 获知变化后报告什么

适用主体：PCF。

适用条件：已有 AF 上下文；AF 已先订阅 QoS notification control；PCF 获知一个或多个 SDF 的 GBR 目标不能保证或又能保证。

PCF 必须通知消费者：向订阅通知 URI 追加 notify 后发送 POST，体为 EventsNotification，带 evSubsUri 和 evNotifs 中 event=QOS_NOTIF；qncReports 中的 notifType 以 NOT_GUARANTEED 或 GUARANTEED 表达相关 SDF 的目标不再保证或恢复保证。

规范强度：通知、载荷及所列字段为 SHALL；notifType 表中为 M/1。

- 触发是 PCF 获知事件，不是消费者发出订阅请求。不能从未收到通知反推目标一直可保证。
- 这里的恢复是所报告 GBR 目标又可保证，不是资源重新分配成功、流重新激活、呼叫恢复或 RTP 首包到达。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.2 notification dispatch，印刷页 87。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.4 basic notification branch，印刷页 90。

依据：3GPP TS 29.514 V19.5.0 §5.6.2.15 Table 5.6.2.15-1 notifType，印刷页 177。

## 先判断报告覆盖会话还是组件

适用主体：PCF / NF service consumer。

适用条件：收到本页范围内的 qncReports；MediaComponentVersioning 不受支持。

不是全部流受影响时，报告须按适用情况在 flows 标出受影响流；若报告没有 flows，notifType 适用于该 AF 会话内全部流。若提供了 Flows 项，medCompN 必填，标识媒体组件编号；fNums 是可选流标识列表。该项未提供 fNums 时，指该媒体组件匹配的全部流，不是整个 AF 会话的全部流。

规范强度：过程中的范围标识为有条件 SHALL；表中 medCompN 为 M/1，fNums 为 O/1..N；两种省略语义是表定义。

- 未给 flows 与某个 Flows 项未给 fNums 是不同层级；不能把单组件报告扩大为全会话。
- 这些编号是本 API 的媒体组件/流标识，不自动等于 QFI 或 MCX 用户、会话、发送权标识。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.4 flows branch，印刷页 90。

依据：3GPP TS 29.514 V19.5.0 §5.6.2.15 Table 5.6.2.15-1 flows，印刷页 177。

依据：3GPP TS 29.514 V19.5.0 §5.6.2.21 Table 5.6.2.21-1 fNums and medCompN，印刷页 180。

## 确认通知不等于恢复媒体

适用主体：NF service consumer。

适用条件：收到并接受 PCF 的正常 QoS notification control POST；拒绝或需重定向时另按通用通知分支。

消费者以 204 No Content 确认通知；也可以发送 PATCH 更新 AF 上下文，但更新是 MAY，不是每次 NOT_GUARANTEED 后都必须执行的动作。通用通知过程规定：不接受时报告拒绝原因；支持 ES3XX 且判断需重定向时走相应重定向响应。

规范强度：正常确认及通用响应分支为 SHALL；后续 PATCH 为 MAY。

- §4.2.5.4 写收到后回 204，§4.2.5.2 另列接受、拒绝和条件重定向；不能扩成所有 POST 一律返回 204。
- 204 仅确认通知，不是 GBR 修复、媒体恢复、删除会话或下层执行完成的证明；本条不规定消费者必须挂断、降码率或重建资源。
- §5.7 完整错误处理及 TS 29.500 重定向机制未核；如选择 PATCH，还须符合更新过程及其特性条件。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.4 acknowledgement and optional update，印刷页 91。

依据：3GPP TS 29.514 V19.5.0 §4.2.5.2 response branches，印刷页 88。

## 与资源分配结果的区别

§4.2.5.8 的 SUCCESSFUL_RESOURCES_ALLOCATION 回答资源已分配；FAILED_RESOURCES_ALLOCATION 回答资源不能分配，并报告相关 PCC 规则 active/inactive 状态。§4.2.5.4 的 QOS_NOTIF 回答 GBR 目标是否仍可保证。这些事件可能涉及同一服务流，但不是同一个结果，不能互相替代。这里没有建立它们的必然先后顺序。比较依据为同版 §4.2.5.8，印刷页 93。

## 证据边界

- TS 29.512、TS 29.513 的检测、SMF 上报、PCC 执行和完整信令链未核；本页从 PCF 已获知结果处描述通知，不补网络如何测得结果。
- 不把 QOS_NOTIF 等同于数值时延/丢包测量。替代 QoS、方向性失败值和内容版本有另外的特性条件，本页不借省略相关字段推导这些扩展的结果。
- 没有实网、QFI、UPF 或 MCX 媒体验证；不能提供声称可直接运行的完整请求或用通知替代业务与媒体证据。

## 按需继续

- 要判断 201 和资源分配结果，查[N5 授权结果](n5-authorization-result-boundary.md)。
- 收到报告后选择修改服务信息或事件列表时，查[N5 会话更新](n5-session-update.md)，保留 PatchCorrection 与完整事件列表替换条件。
- 真正结束 AF 会话或收到 terminate 通知时，查[N5 会话终止](n5-session-termination.md)；QoS 目标不能保证本身不等于该过程已发生。

[3GPP TS 29.514 V19.5.0，ETSI 官方发布版](https://www.etsi.org/deliver/etsi_ts/129500_129599/129514/19.05.00_60/ts_129514v190500p.pdf)；仅适用于所列版本和条款。
