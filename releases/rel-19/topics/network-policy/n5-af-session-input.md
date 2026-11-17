# N5授权请求：应用、媒体和流如何区分

## 适用范围

- 固定TS29.514 V19.5.0；通用Stage3 AF/NF service consumer与PCF间的IP类型PDU会话授权，AF已获使用服务的授权。
- 只讨论普通单播、单接入和基本创建/结果通知；不覆盖Ethernet、TSN/TSC、MA PDU、紧急/优先呼叫及其专用优先化、替代QoS和内容版本扩展。
- 用于理解MCX可采用的N5授权接口，不证明某MCX实现已绑定该API或已验证版本组合；不提供完整可运行请求或安全接入配置。

## 创建上下文与UE地址

适用主体：NF service consumer。

适用条件：新AF应用上下文；媒体信息可用且需要PCC控制。

向PCF的Application Sessions集合POST AppSessionContext，含AppSessionContextReqData；IP场景提供ueIpv4或ueIpv6，并提供上下文删除通知用notifUri。

- 此notifUri与evSubsc内事件通知URI用途不同；本条不是完整必填字段清单。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2，印刷页 21、22、23。

## 媒体组件与流过滤器

适用主体：NF service consumer。

适用条件：媒体组件及流过滤信息可用。

medComponents承载服务信息；每个已提供组件用fStatus表示启用/禁用要求；过滤器放在medSubComps，每个子组件一个上行和/或下行过滤器；IP端点信息可用时在fDescs提供源、目的IP及端口。

- fStatus是请求信息，不能当作网络闸门已打开。过滤语法及TS29.214限制未核。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2，印刷页 22、25。

## 应用标识的两层优先关系

适用主体：AF。

适用条件：需要标识AF会话所属服务；提供afAppId。

afAppId可在请求和媒体组件两层提供；两层都有时组件值优先。

- 不把MCPTT用户ID直接填成afAppId；实际应用标识配置未核。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2，印刷页 22。

## 会话绑定输入与绑定失败

适用主体：NF service consumer/PCF。

适用条件：有效POST进入session binding；IP场景。

UE地址为绑定输入；可补dnn/supi/gpsi/sliceInfo/ipDomain。已提供属性须匹配；绑定失败返回500及PDU_SESSION_NOT_AVAILABLE。

- 重复私网地址场景单靠IP不足；S-NSSAI取得及非IMS消费者取得UE私网地址仍有范围缺口。完整绑定算法转引TS29.513，未核。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2，印刷页 23、24。

## 请求优先级不等于承载QoS

适用主体：NF service consumer。

适用条件：选择提供resPrio。

会话层resPrio表示AF会话相对优先级，组件层表示会话内流优先级，两者不冲突；未指定时请求优先级为PRIO_1。

- 不能将resPrio数值当作ARP、5QI或QFI；本页不覆盖MCPTT/MCVideo/MCS优先化专门调用。

依据：3GPP TS 29.514 V19.5.0 §4.2.2.2，印刷页 25。

## 原文差异与适用限制

§4.2.2.2 NOTE6，印刷页 23：NOTE6文字回指NOTE3，但相邻讨论为IP域/NAT，NOTE3实际为MediaSubComponent事件使用。保留这一原文回指疑点，不据此改写NOTE6适用条件。

## 证据边界

- TS29.513绑定/PCC流程、TS29.512到SMF的执行、TS29.500安全与错误框架、TS29.214过滤约束及完整schema未核，不能生成声称可运行的请求。
- 尚未建立MCX媒体SDP到全部API字段、授权PCC规则到QFI/包过滤器、实际UPF转发的验证链；资源通知也不能替代业务或媒体收发证据。
- 未声称本版最新；不以Rel19标签推定与TS23.289 V19.7.0及其他已发布版本组合互通。

## 按需继续

- AF 会话结束或收到 PCF 终止通知时，查[N5 会话终止：删除请求、PCF 通知与资源清理](n5-session-termination.md)。
- 已有 AF 上下文且需修改媒体信息或订阅时，查[N5 会话更新：媒体变更、订阅替换与生效证据](n5-session-update.md)。
- [N5授权结果：201与资源分配通知分别证明什么](n5-authorization-result-boundary.md)
- [MCPTT 语音进 5GS：语音 QoS 与 SIP 信令的边界](mcptt-5gs-voice-qos-scope.md)
- [MCPTT 服务器请求单播资源：端点与完成证据](mcptt-5gs-server-resource-request.md)

[3GPP TS 29.514 V19.5.0](https://www.etsi.org/deliver/etsi_ts/129500_129599/129514/19.05.00_60/ts_129514v190500p.pdf)；仅所列版本和条款。
