# MCData 紧急告警发起：用户许可、目标组与本地状态

限 TS24.282 V19.7.0 在网 MCData，用户明确给出普通配置组 ID；不是 adhoc、regroup 或 off-network。目标组没有正在进行的组通信，不将本批成员通知覆盖推广到所有已加入会话的成员。

本批仅展开独立紧急告警 SIP MESSAGE，不等同紧急 SDS/FD 通信建立或升级，也不推出媒体、逐消息送达或人员已读。相关服务授权绑定及用户/profile/组文档是各检查的输入，不从未读的配置规范补默认值。

## 客户端发起许可

适用条件：用户请求向已明确给出的组发送紧急告警，客户端执行 §6.2.8.1.6。

客户端须同时满足用户 profile 的 ruleset/rule/actions/allow-activate-emergency-alert=true，以及目标组文档未含值为 true 的 list-service/preconfigured-group-use-only。还须满足 Common/GroupEmergencyAlert/entry 的一种配置：entry-info=DedicatedGroup 时 uri-entry 包含目标组；或 entry-info=UseCurrentlySelectedGroup 且目标组文档规则 actions 中 mcdata-allow-emergency-alert=true。其他情况判为未授权，客户端告知用户该组不允许告警并终止。

- 本客户端 DedicatedGroup 分支没有另列 mcdata-allow-emergency-alert 条件；CF 的同名分支却列了，不能合并成一个“客户端通过则服务器必通过”的检查。
- §16.2.1.1 还规定未指定组时的 profile/最近通信或归属请求回退，但本主题用明确目标避免将其授权先后关系自行改写为完整选择算法。

依据：§6.2.8.1.6 initiation conditions;16.2.1.1 opening，印刷页 72、73、377。

## 告警消息与待确认状态

适用条件：客户端授权通过，进入 §16.2.1.1 生成步骤。

客户端生成对话外 SIP MESSAGE，使用 MCData ICSI，并在 mcdata-info 中给出目标组 mcdata-request-uri、alert-ind=true 和发起客户端的 mcdata-client-id；另须带 location-info 的 Report，包含该告警位置触发配置要求的位置资料。客户端设置自身 MCData emergency state，并将告警状态设为 MDEA2（待确认），再发送到原文所称服务该组身份的 PF 公共服务身份。配置位置资料随发起发送，告警状态待确认，均不说明 CF 已接受。

- 本条不展开可选 active functional alias、用户请求应用优先级或完整 SIP/XML 编码；不能据本页构造已验证报文。
- 原文用服务 group identity 的 PF，不能静默改成其他过程中的 user-serving PF。位置 Report 是 SHALL；具体配置内容/缺少可用位置时如何编码不在已核范围。

依据：§16.2.1.1 steps1–10，印刷页 377、378。

## 响应和通信失败的区别

适用条件：对应 §16.2.1.1 发出的告警 MESSAGE 已有响应，或出现无响应/通信失败。

收到该请求的 2xx，客户端须把告警状态设为 MDEA3（已发起）并向用户指示成功；收到 4xx/5xx/6xx，须置 MDEA1（无告警）并指示失败。无响应超过实现决定的时间或发生通信失败时，NOTE 允许通知用户、清除告警状态或重发，但 MCData emergency state 保持不变，由用户按需要手动清除。这里的成功是本告警发起过程的结果，不是全组终端已收到或已读。

- 不把无响应写成强制重试、固定超时或必然失败；不为本条未列出的 3xx 补状态迁移。
- MCData emergency state、MDEA 告警状态、组 MDEG 状态和组通信 MDEGC 状态是不同对象；本告警响应不能证明紧急组通信已建立。

依据：§16.2.1.1 response paragraphs and NOTE;16.2.3.1 step4b(ii–vi)，印刷页 378、401。

## 证据边界

- 本版 §16.2.2.1、§16.2.2.2、§16.2.3.2 的编辑说明（印刷页383、385、402）指出，紧急组及紧急组通信的支持可能缺失、部分提供，或仅限于支持紧急告警。本主题仅说明已列明的告警流程；不能由这些 MESSAGE、200 或告警状态推定完整紧急组通信、emergency-ind 处理或媒体能力已经定义并验证。
- 本主题不展开缺省目标选择、位置触发自动发起或紧急会话升级。

## 按需继续

- [emergency-alert-admission-and-results](emergency-alert-admission-and-results.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§6.2.8.1.6 versus6.3.7.2.1：客户端与CF使用不同告警profile路径，且DedicatedGroup的组许可条件不完全一致。 按各角色原文保留，不以客户端通过推定服务器通过；未核配置schema，不据此消解差异。

§8.3.2.11 step1a;8.3.2.12 step7;8.3.2.2：本地判定先找用户却在缺席分支称group entry；候选期限未赋来源；复制旧过期同组后再新增的唯一性疑点仍在。 只总结明确的查找/状态与新增条件，不自补缺省期限、清理或去重。

§16.2.2.1 2xx paragraph：响应段回指step12，实际发送列在step13。 定位为本次转发的业务MESSAGE响应，不编造第二个发送或把它改为PUBLISH响应。

§16.2.3.1 step4b(ii);6.3.7.1.2 opening：主调用说其他已归属成员，helper概述限已归属但未参与成员。 本批限定无正在进行组通信，保留有会话时的范围差异，不推广为所有紧急组通信通知算法。

§16.2.2.3 opening,step2,step4b：入口Request-URI为PF PSI，step2从body取目标MCData ID，step4b却称从incoming Request-URI的MCData ID确定公共身份。 保留binding与404证据，不把正文静默修成已验证端到端寻址报文。

§16.2.3.2 step1 versus step2;6.3.7.2.2;16.2.1.2：取消的否定分支错引发起授权helper；肯定分支才引取消helper；CF取消权限路径/缺失值规则也与客户端不完全相同。 明确限制为step2条件成立后的动作；否定分支保留原文和403/alert=true，不凭直觉修成统一准入算法。

§16.2.1.1 step4d;16.2.1.2 step4d;6.3.7.1.2 step6：客户端可选FA字段描述把anyExt/functional-alias-URI包含次序写得与常见用法不同，通知helper头名写P-Asserted-Service-Id。 本批不输出XML/完整报文或以常见名称替换；可选别名与服务头编码仍非本次验收范围。
