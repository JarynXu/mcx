# 功能别名结果：PUBLISH 200、NOTIFY 与后续归属

限本批已核的per-user功能别名状态观察；原文列出的状态、到期与请求关联分别解释。

未完整核服务器到别名拥有者的准入和结果链，因此状态通知不是跨系统完整互通证明，也不能直接代表一次SDS/FD通信已完成。

## PUBLISH成功不等于别名成功

适用条件：服务用户的MCData服务器满足§22.2.2.2.3入口条件并已通过到步骤8之前的检查。

服务器步骤8先向PUBLISH返回SIP200，并在响应Expires中给出candidate expiration；步骤9随后仍检查PIDF presence.entity是否等于served MCData ID，不匹配就停止后续步骤。正常路径之后才处理别名列表和触发进一步状态过程。因此这个200不能单独证明别名已激活、已停用或接管完成。客户端应按已先发起的状态确定过程解释后续NOTIFY，而不是把PUBLISH事务成功升级成最终别名状态。

- 这是按原文顺序得出的证据边界，不把entity不匹配改成200之前的额外拒绝，也不补第二个SIP最终响应。
- 未展开所有PUBLISH拒绝码或RFC3903发布状态管理；本条只证明200不充分。

依据：§22.2.1.1;22.2.2.2.3 steps5–9,10–17，印刷页 476、480、481、482。

## 通知状态、过期和关联证据

适用条件：客户端收到含按§22.3.1构造的per-user application/pidf+xml body的SIP NOTIFY。

客户端须逐个判断body中别名对该用户的状态；p-id-fa若出现，指出触发此NOTIFY的PUBLISH。schema列出的状态包括activating、activated、deactivating和take-over-possible，不能把它们都解释为激活成功；expires是单个别名激活的到期时间，类型为dateTime。服务用户服务器的通知过程不包含已过期或状态为deactivated的条目，所以不能等待一个本schema未列的deactivated状态字段来确认结果；条目缺席本身也不能唯一证明本次停用成功，它还可能因到期而被省略。

- p-id-fa在客户端NOTIFY处理段是条件性字段；没有它时不能凭本条唯一归因于某次PUBLISH。服务器由22.2.2.2.3调用且已识别handled p-id-fa时才明确要求回填该值。
- 状态和expires说明别名激活关系，不是SDS/FD的Message ID、DELIVERED、READ或文件下载完成证据。
- 不编造拒绝原因字段、缺席条目的确定原因或跨多次通知的完整差分恢复算法；没有状态值时也不自行设为activated。

依据：§22.2.1.3 NOTIFY handling;22.2.2.2.5;22.3.1.2 per-user syntax and table22.3.1.2-1，印刷页 479、483、495、496。

## 别名变化与规则式组归属

适用条件：客户端在状态观察中检测到功能别名激活或停用。

§22.2.1.3要求调用§8.2.6的规则式归属变化过程。该过程根据用户profile中的RulesForAffiliation/RulesForDeaffiliation规则，在位置改变或别名激活/停用时重新评估，若任一定义规则满足，则须发起§8.2.2归属变化；组配置中的地理范围规则仍适用。因此别名激活通知不直接证明用户已经归属到某个组，也不意味着每次别名变化都必须对所有组发归属请求。

- §8.2.6.2对规则满足的文字为位置条件中任一项与别名条件中任一项均满足；本条不擅自改成任一类满足即可。对不包含某类条件的规则如何求值，未从本段补默认逻辑。
- 这里只核被调用过程及条件，不扩展8.2.2的完整归属交互、接受结果、跨组批次或服务端授权。
- 组配置给出的permitted地理范围是允许归属的条件；mandatory地理范围存在且用户在范围外时要求退出归属。不能以别名状态覆盖这些条件。

依据：§22.2.1.3 final paragraph;8.2.6.1–8.2.6.3，印刷页 161、162、479。

## 证据边界

- 未展开通知丢失后的重建、别名拥有者拒绝/接管全链、跨域状态一致性或完整组归属实现验收。

## 按需继续

- [functional-alias-observation](functional-alias-observation.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

- §22.2.2.2.3 step13;22.3.1.2 table22.3.1.2-1：step13状态文字为de-activating，表中枚举为deactivating。 解释为原文列表停用过渡处理时保留拼写差异，不增加一个新的wire状态值。
- §22.2.1.2 step6c;22.3.1.2 per-user steps7–9 and table22.3.1.2-1：客户端用functionalalias小写，语法段有fucntionalAlias拼写；per-user step9说status属于functionalAliasID元素，schema则将status定义为functionalAliasType的属性。 正文只保留状态/字段业务用途并定位差异，不冒充该文本已通过XML schema一致性或实现验收。

## 别名状态之后能否发送并确认收到

别名状态不替代SDS业务准入或送达证据。[私聊身份与准入](sds-server-identities-and-private-admission.md)只核直接MCData ID，不补功能别名解析和目标选择；[送达与已读证据](sds-disposition-timing.md)解释SIP响应与带外回执的区别。不能把别名直接代入已核的直接ID链。[功能别名目标SDS](sds-functional-alias-target-routing.md)另列CF选人和客户端300后新请求；该链仍保留中间响应传递与过滤语法依赖。

- [后续服务器条件与证据](functional-alias-lifecycle-results.md)

- [规则满足后调用的显式归属变更](explicit-affiliation-request.md)：兴趣发布与结果观察仍分开判断。
