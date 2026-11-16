# 功能别名变更：PUBLISH、续期与位置约束

限MCData客户端§22.2.1.2/.4状态变更过程，涉及用户主动请求、已激活状态临近到期的刷新，以及位置条件触发。

位置触发限制、发布列表和服务端准入仍各自适用；没有因为请求被构造或发出就认定别名状态已改变。

## 变更请求与续期的事务

适用条件：客户端请求激活/停用一个或多个别名，刷新NOTIFY所告知的activated状态临近到期的别名，或因进入/离开位置区域触发状态变化。

这些入口使用SIP PUBLISH，面向服务用户的originating PF；mcdata-info body的mcdata-request-uri取MCData用户ID，并携MCData服务标识。激活请求的Expires取4294967295，停用取0；原文明示激活和停用不能由同一PUBLISH完成。续期入口针对已从NOTIFY得知处于activated状态且临近到期的别名，是刷新用户继续使用的意图，不是PUBLISH一发出就获得新的激活期限。

- 不把PUBLISH请求的最大Expires当成已授予永久激活；服务端响应的candidate expiration和NOTIFY中的别名状态/到期时间需分别判断。
- 本节没有给出客户端“临近到期”的固定提前秒数或完整RFC3903刷新报文算法，本条不补。
- Expires=0的服务端作用范围另受served list处理约束，不能据客户端开头的一或多个措辞自补单别名删除模板。

依据：§22.2.1.2 opening,steps1–5 and NOTES2,3，印刷页 476、477。

## 意图列表、客户端与关联标识

适用条件：客户端构造PUBLISH的per-user application/pidf+xml body。

客户端应列出该MCData ID请求激活的全部功能别名，并携目标MCData client ID；不得在functionalAlias条目中自行填写status或expires属性。p-id-fa必须取全局唯一值，供后续通知与本次PUBLISH关联。只有已经收到可以接管的指示且确实打算接管时，才要求加入值为true的take-over子元素。PIDF的per-user上下文另以presence.entity标识MCData用户、tuple.id标识客户端，不能将别名ID、用户ID、客户端ID和请求关联值混为一种身份。

- 客户端step6a只按请求激活列表描述body；不据此编造停用时的独立target-delete结构。
- take-over=true表达有条件的接管意图，不是服务器已授权或旧用户已经停用的结果。Stage1共享/接管政策另有来源，完整Stage3接管事务未核。
- 保留正文functionalalias/functionalAlias等拼写和属性挂载差异的来源记录，不提供经过schema验证的XML样例。

依据：§22.2.1.2 step6;22.3.1.2 per-user syntax，印刷页 477、495、496。

## 位置触发的手动停用限制

适用条件：MCData用户手动请求停用某功能别名，或客户端发现位置条件满足。

手动停用前，客户端须检查用户profile中对应FunctionalAliasList条目的manual-deactivation-not-allowed-if-location-criteria-met配置。只有该别名确因位置区域触发而激活，且该配置为true时，客户端须抑制用户的停用请求；可向用户显示提示，不是必须显示。另一方面，只要别名激活或停用的位置条件满足，§22.2.1.4要求启动§22.2.1.2状态变更过程，而不是直接宣告别名已在服务器生效。

- 必须保留“因位置触发而激活”和配置true两个条件，不扩大为所有有位置配置的别名都禁止手动停用。
- 抑制规则针对用户手动停用请求，不据此阻断另一个位置触发的停用过程。位置规则来源和完整profile schema依赖24.484，未读取。
- 本条不由配置缺失推定其他授权必然允许；它只限定这一个抑制分支。

依据：§22.2.1.2 manual deactivation paragraph and NOTE1;22.2.1.4，印刷页 477、479。

## 列表省略及零到期的作用范围

适用条件：服务用户的服务器已通过PUBLISH前置检查和PIDF entity匹配，按§22.2.2.2.3生成candidate list；这里只使用该helper解释客户端列表影响。

candidate expiration非零时，已存在且尚未到期的别名若本次仍列出，会被复制并更新到期时间；若本次漏列，且原状态是activated或activating，则被置为deactivating，并以当前时间加两倍timer F设置过渡期限。candidate expiration为零时，步骤13遍历served list的各现有别名条目，而非只遍历body中某一目标，再用candidate list替换所保存的列表。因此更新/刷新时不能把PUBLISH名单当作任意单条增量；也不能把Expires=0解释成已核验的仅停用指定一个别名接口。

- 这里的范围是served MCData用户的既有功能别名列表，不扩成全系统、所有用户或任意其他终端的名单。
- 本条说明必要的列表影响，不完整描述服务器状态机、owner授权、跨域消息或后续最终成功。timer F数值及外部SIP定时器机制未核。
- 步骤13字面使用de-activating，而其他步骤/schema使用deactivating；保留差异，不把该拼写直接当成新的可发送状态枚举。
- 列表遗漏的服务端效果不表示客户端可以绕过22.2.1.2 NOTE3，在同一PUBLISH混合激活与停用意图；本批不消解两处文字的实施边界。

依据：§22.2.1.2 step6a;22.2.2.2.3 steps10–14，印刷页 477、481、482。

## 证据边界

- 没有实现任意单别名删除、部分名单补丁、跨域接管或失败恢复；正文存在列表与编码差异，不输出可直接部署的SIP/XML样例。

## 按需继续

- [functional-alias-state-evidence](functional-alias-state-evidence.md)
- [../identity/functional-alias](../identity/functional-alias.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

- §22.2.1.3 initial steps6/in-dialog step3;22.2.2.2.4 opening4：客户端段写Events header，服务端入口写Event header。 保留字面差异并引用presence事件意图，不无声修订客户端拼写，不据本批生成完整报文。
- §22.2.1.2 step6;22.2.2.2.3 steps12b,13：客户端开头包括停用一个或多个别名，但body step6a按全部请求激活别名描述；服务端nonzero处理漏列条目、zero遍历served list。 不把发布过程解释成任意单条增删补丁；明确完整列表与zero作用范围的边界，不自拟仅停用一个别名的编码。
- §22.2.2.2.3 step13;22.3.1.2 table22.3.1.2-1：step13状态文字为de-activating，表中枚举为deactivating。 解释为原文列表停用过渡处理时保留拼写差异，不增加一个新的wire状态值。
- §22.2.1.2 step6c;22.3.1.2 per-user steps7–9 and table22.3.1.2-1：客户端用functionalalias小写，语法段有fucntionalAlias拼写；per-user step9说status属于functionalAliasID元素，schema则将status定义为functionalAliasType的属性。 正文只保留状态/字段业务用途并定位差异，不冒充该文本已通过XML schema一致性或实现验收。
- §22.2.2.2.3 step12a(ii),step15c：step12a(ii)对现有deactivating/deactivated条目写回activated，step15c后续触发条件则要求candidate为activating。 本批未据此重建完整服务器状态机，列表影响claim只使用没有此冲突的过期更新及遗漏条目分支；不把两处静默统一。

- [后续服务器条件与证据](functional-alias-server-admission.md)
