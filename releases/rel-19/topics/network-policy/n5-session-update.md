# N5 会话更新：媒体变更、订阅替换与生效证据

## 适用范围

- 固定 3GPP TS 29.514 V19.5.0，Release 19，Stage 3；对象为已创建的 Individual Application Session Context，NF service consumer 已获使用该服务的授权。
- 仅普通 IP 类型、单播、单接入的通用 AF/PCF 用途；不把该 API 等同于 MCX 已部署绑定，也不保证与 TS 23.289 或其他精确版本互通。
- 不覆盖 Ethernet、ATSSS、多模态、TSC、紧急/优先化、内容版本、SIP forking、替代 QoS、完整错误/重定向处理及 TS 29.512/29.513 下层执行。API 响应、PCC 操作和实际媒体收发分别判断。
- 更新主题仅适用于 PatchCorrection 特性受支持；不借 Annex D 的旧结构补齐。

## 更新请求的前提和载荷

适用主体：NF service consumer。

适用条件：PatchCorrection 特性受支持；已有 AF 会话需修改，或存在消费者内部触发。

可向该 Individual Application Session Context URI 发送 PATCH；请求体必须为按 JSON Merge Patch 编码的 AppSessionContextUpdateDataPatch，变更位于 ascReqData。medComponents 可提供更新后的服务信息；相关 medSubComps 内的流过滤器值可由新值替换。

规范强度：发起和更新字段为 MAY；请求体类型及编码为 SHALL。

- 不将不支持 PatchCorrection 的 Annex D 路径套入本结构；RFC 7396 全部合并语义、媒体组件 map 的逐字段可删除性和完整 schema 未核。

依据：3GPP TS 29.514 V19.5.0 §4.2.3.2，印刷页 57、58。

依据：3GPP TS 29.514 V19.5.0 §5.3.3.3.2 Tables 5.3.3.3.2-1/2，印刷页 125。

## 修改闸门状态时保留 RTCP 例外

适用主体：NF service consumer / PCF。

适用条件：共同范围及 PatchCorrection；要修改允许或禁止通过 PDU 会话的流。

消费者以 PATCH 的 ascReqData.medComponents 在媒体和/或媒体子组件层提供 fStatus。若子组件 flowUsage 为 RTCP，该子组件所描述 IP 流必须双向启用，不受对应媒体组件 fStatus 值影响。PCF 应按此操作设置相关活动 PCC 规则的 gate status，并按更新过程响应。

规范强度：列明操作为 SHALL。

- RTCP 例外针对对应媒体组件的 fStatus，不能扩成绕过子组件层所有限制；不证明网络闸门已实际执行或媒体已到达。

依据：3GPP TS 29.514 V19.5.0 §4.2.3.3，印刷页 61、62。

## 事件列表是整体替换，不是追加

适用主体：NF service consumer / PCF。

适用条件：PatchCorrection；通过上下文 PATCH 修改会话层持续事件订阅，不包括 ONE_TIME 或 EnQoSMon 子组件订阅。

建立订阅时在 ascReqData.evSubsc 提供事件列表与通知 URI。修改订阅时 events 必须提供新的完整订阅列表；需更新的事件附加信息整体替换原值。删去 events 中某项即取消该事件；即便对应附加信息未置 null，PCF 也移除该信息并停止相关过程。事件仍列出而附加信息置 null 时，订阅仍有效但相关过程不再适用。将整个 evSubsc 置 null 则移除该订阅信息。

规范强度：列表及移除动作为 SHALL；两个附加信息处理分支为 NOTE 2/3。

- 不能把 events 当增量追加列表；删除订阅不等于删除 AF 上下文。ONE_TIME 重建行为与 EnQoSMon 并存约束未纳入本页。

依据：3GPP TS 29.514 V19.5.0 §4.2.3.2，印刷页 58、59。

## 区分拒绝原因与重试等待

适用主体：PCF / NF service consumer。

适用条件：PatchCorrection；PCF 已收到更新请求；按各分支的失败条件判断。

更新信息不获授权时返回 403/REQUESTED_SERVICE_NOT_AUTHORIZED，可附 acceptableServInfo；无效或不足的信息为 400/INVALID_SERVICE_INFORMATION。临时网络条件导致服务信息暂不可授权时，PCF 可返回 403/REQUESTED_SERVICE_TEMPORARILY_NOT_AUTHORIZED，并可给 Retry-After。消费者收到该间隔后，在到期前不得向同一 PCF 为同一上下文重送相同服务信息。已有上下文不存在时，PCF 必须拒绝并给适用原因。

规范强度：信息无效/不获授权及不存在上下文的拒绝为 SHALL；暂不可授权分支和叙述中的 Retry-After 为 MAY；收到间隔后的等待为 SHALL。

- TEMPORARY_NETWORK_FAILURE 是另一失败原因，不能与 REQUESTED_SERVICE_TEMPORARILY_NOT_AUTHORIZED 混用；未穷举错误。表中 Retry-After 为 M/1，与正文 MAY 差异未裁决；不推所有 403 必带头、缺头默认间隔或到期后必成功。

依据：3GPP TS 29.514 V19.5.0 §4.2.3.2，印刷页 59、60、61。

依据：3GPP TS 29.514 V19.5.0 §5.3.3.3.2 Table 5.3.3.3.2-4，印刷页 125。

## 上下文更新成功不等于承载已生效

适用主体：PCF / NF service consumer。

适用条件：更新请求被接受。

PCF 更新服务信息，并可能需要按 TS 29.513 创建、修改或删除相关 PCC 规则，再依 TS 29.512 向 SMF 提供更新。200 响应返回修改后的上下文表示，204 表示上下文已修改而无响应体。面向消费者的响应 SHOULD 在所需 PCC 规则配置之前或与之并行发生。

规范强度：上下文更新及响应为 SHALL；规则变化依需要；响应时序为 SHOULD，不提升为 SHALL。

- 因此 200/204 不能单独证明资源分配、QFI 绑定或 UPF 执行完成；不是所有更新都要求改变 PCC 规则。无上下文拒绝不授权自动重建。

依据：3GPP TS 29.514 V19.5.0 §4.2.3.2，印刷页 60、61。

依据：3GPP TS 29.514 V19.5.0 §5.3.3.3.2 Table 5.3.3.3.2-3，印刷页 125。

## 条款差异

正文与响应头表的 Retry-After 强度差异尚未裁决。已收到间隔时不得提前重送相同服务信息；缺少该头时，本页不给出默认等待值或自动重试结论。

## 证据边界

- RFC 7396、TS 29.500、TS 29.512、TS 29.513 和 TS 29.214 引用机制未在本次独立核原文；不提供可运行 API 请求模板。
- 没有实网操作或跨版本互操作测试；更新成功、资源删除、PCC 移除请求及终端媒体状态不能合并。

## 按需继续

- [N5 会话终止：删除请求、PCF 通知与资源清理](n5-session-termination.md)
- [N5 授权请求：应用、媒体和流如何区分](n5-af-session-input.md)
- [N5 授权结果：201 与资源分配通知分别证明什么](n5-authorization-result-boundary.md)

[3GPP TS 29.514 V19.5.0，ETSI 官方发布版](https://www.etsi.org/deliver/etsi_ts/129500_129599/129514/19.05.00_60/ts_129514v190500p.pdf)；仅适用于所列版本和条款。
