# 预建立会话上的私聊 SDS：REFER、业务 INVITE 与结果反馈

## 适用范围

- 同版§9.2.5.2，已有可用预建立会话，本页限普通非紧急、非imminent-peril、直接MCData ID私聊；不含别名、ad hoc、组激活或149后续紧急反馈。
- 选择media standalone SDS或SDS session时，SDP和request-type按各自分支；必要端到端安全上下文仍按§9.2.5.2.1.1 step3处理。本页不把预建立成功当成逐业务许可或密钥已满足。
- 各handler只在自身输入和前序校验成立时使用。客户端单entry与PF数量文字、MIME名称及关联判定的Editor note保留，不据本页声称完整编码/路由实现。

## REFER 如何指定会话和业务

适用条件：用户要求在既有预建立会话中发起普通直接用户私聊SDS。

客户端生成dialog之外的REFER，Request-URI为预建立会话身份，Target-Dialog也识别该预建立会话。Refer-To是cid URL，指向包含单一目标entry的resource-list；目标URI的body参数承载按standalone或session分支生成的SDP，以及相应one-to-one-sds或one-to-one-sds-session request-type和本端client-id。Supported包含norefersub，Refer-Sub=false。预建立会话用于定位复用对象，目标用户仍由单独entry表达，不能用预建立URI代替目标MCData ID。

- “在预建立会话中发起”不意味着REFER自身在dialog内；正文明确outside a dialog，再以Target-Dialog关联。
- 本client步骤写application/vnd.3gpp.mcdata-info（无+xml），PF生成helper却写复制mcdata-info+xml；resource-list文字也有MIME+xml排列差异。保留承载字面，不假定编码验证通过。
- required安全上下文不存在/过期时有独立PCK生成/保护步骤；不以本页普通场景跳过。密钥算法和外部33.180细节未核。

依据：§9.2.5.2.1.1 opening,steps1–10;9.2.5.2.0，印刷页 244、245、246。

## REFER 准入先于业务 INVITE

适用条件：O-PF收到Request-URI识别预建立会话、cid/resource-list/body与request-type符合§9.2.5.2.2.1入口的REFER，且所有前序条件已通过。

PF从REFER的PAI确定MCData用户，绑定缺失或过期回404/141；§11.1不准发起则403/200。所需cid引用缺失可403/145，无法确定服务主叫的CF则404/142。按norefersub与Refer-Sub=false条件不建隐式订阅后，PF先为REFER生成并发送最终200，再按§9.2.5.1.1生成业务INVITE并发给CF。该INVITE按已协商预建立SDP及请求中的SDP形成offer，复制业务目标/内容。故REFER200发生在业务INVITE之前，不能当成对端已接通。

- 资源不足/拥塞风险可500并停止，Retry-After可带；当前预建立已存在不免除此逐业务资源处理。
- PF step6仅在resource-list有more than one entry时写确定私聊类型，而客户端要求single entry。不能将原文改成exactly one，也不能据此补出单entry拒绝码或完整分类算法。
- PF step4(ii)/(iii)还列紧急及imminent-peril授权拒绝，未在该条文字外再写仅相应请求时才适用。本页不静默删去这些检查，也不据普通场景推定会自动跳过；结论仅用于所有前置检查已通过的路径。
- §9.2.5.1.1的SDP helper引用§9.2.3.3.1（standalone），而客户端对SDS session选择§9.2.4.2.1。保留所引接口，不能直接宣称其对两类业务已完整对齐。

依据：§9.2.5.2.2.1 opening,steps1–14;9.2.5.1.1;9.2.5.2.3.1/.2，印刷页 242、243、248、249、250、251、252。

## 通过已有对话回报建立结果

适用条件：PF收到业务INVITE的200且无Warning149，或发起客户端收到发送REFER所针对预建立会话内的建立结果re-INVITE。

普通无149分支中，PF在收到网络INVITE200后调用媒体过程，随后在预建立dialog内发re-INVITE；通用helper把mcdata-communication-state设为establish-success。客户端据该值通知业务建立成功；若实际收到establish-fail，则通知失败、恢复发起尝试前的状态变量并退出。PF收到该re-INVITE的2xx后再调用媒体过程。这是业务建立状态回流，与此前预建立INVITE200和REFER200分别发生，也不等于某条SDS已送达/已读。

- helper定义收到业务INVITE错误时的establish-fail取值，客户端也定义其接收处理；本次§9.2.5.2.2.1具体caller没有单列普通错误响应后如何调用该helper，不能由两端存在就证明失败通知必达。
- 149存在时是另一路等待INFO的紧急通信处理，本页无149结论不可扩到它。
- 客户端REFER2xx、建立结果re-INVITE以及PF对应响应均有媒体调用点，但详细发送条件/资源绑定属于24.582；不把反复调用等同每次都新建一条业务或无条件可发数据。

依据：§9.2.5.2.2.1 SIP200 response steps1,2;9.2.5.1.2;9.2.5.2.1.1 final2xx andre-INVITE procedures，印刷页 243、244、246、247、250。

## 终接重邀请与业务关联

适用条件：T-PF收到普通私聊standalone media SDS或SDS session的INVITE，并采用已有预建立会话终接；客户端收到其re-INVITE。

T-PF先处理资源与目标用户绑定，无绑定回404停止；成功路径向预建立会话URI发送re-INVITE，若入站请求带所列业务信息MIME，则复制并设establish-request，并在Contact提供与入站业务session identity映射的MCData session identity。客户端在预建立会话尚无关联MCData session且state=establish-request的入口下，按request-type调用standalone接收§9.2.3.2.4或SDS session接收§9.2.4.2.4。T-PF在re-INVITE2xx后调用媒体过程。Request-URI定位预建立会话，Contact所给映射标识定位具体业务，不能直接等同。

- 若已关联one-to-one通信，正文转§6.2.8.4.2，而不是作为一个新的普通业务；本页不展开该紧急升级/取消handler。
- p247 Editor note明确要求核实终接客户端判断是否有关联session的能力。该判定是前提，不能写成实现已经可靠识别。
- 本T-PF子节在客户端2xx后列媒体交互，未另列如何生成/回送原CF INVITE的200；不能把按需T-PF的完整响应过程无声拼进来。
- 绑定检索、Contact映射和媒体接口调用不能证明传输数据已与原conversation/message UUID全部关联。

依据：§9.2.5.2.2.2;9.2.5.1.3;9.2.5.2.1.2，印刷页 244、247、248、251。

## 证据边界

- §9.2.5.2.1.2 p247明确留下关联判定能力待核的Editor note，§9.2.5.2.2.1 p248又提示预建立身份可能需澄清。它们限制身份/关联链，不能把所有已列动作一概判成未定义。
- CF仍调用普通SDS session helper；本页不重新证明其全部授权、路由、媒体和成功范围。

## 按需继续

- [SDS session 后续使用：会话标识、消息证据与媒体边界](sds-session-message-evidence.md)
- [预建立会话的退出：离开 SDS 业务与销毁会话](pre-established-leave-and-release.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
