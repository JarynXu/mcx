# SDS 别名解析：owner 查询、当前状态与协议缺口

限 §9.2.2.4.2 调用 §22.2.2.2.8 发现已激活目标别名的用户这一用途，及其 owner 入口 .3.7/.3.8。

查询不是激活或接管；SIP查询响应、PIDF状态、SDS选择和SDS回执分开解释。适用安全/身份处理仍由各自程序完成，本页不以查询入口替代全链授权。

## 向别名owner查询

适用条件：MCData 服务器为 §9.2.2.4.2 的目标解析调用 §22.2.2.2.8，拟发现已成功激活某 handled functional alias 的用户。

服务器生成初始 SUBSCRIBE，Request-URI 为关联该别名的 CF 公共服务身份；mcdata-info+xml 的 mcdata-request-uri 携别名 ID。请求用 MCData ICSI 的 P-Asserted-Service、presence 事件、Accept:application/pidf+xml，并携针对别名的 simple-filter+xml。这里不是直接向某个接收客户端发送 SDS，查询的服务标识也不是前一段 MESSAGE 使用的 SDS ICSI。

- owner CF PSI 的发现方法及经 gateway 的跨信任域出口路由被 NOTES4–5 明列为规范范围外；本页不编造 DNS/目录/缓存算法。
- step6 字面为 Events header；owner 入口使用 Event。调用要求 per-functional-alias filter，而 §22.3.2 实际提供 per-user 过滤语法，见本页来源问题，不把它们静默拼成可执行 XML。

依据：§22.2.2.2.8 opening and steps1–3,5–7，印刷页 488。

## 一次查询与持续观察

适用条件：服务器按 §22.2.2.2.8 构造初始解析 SUBSCRIBE。

step4 要求 Expires=0；NOTE6 又说明如要当前状态和后续通知，可请求 4294967295。应区分一次当前解析查询与选择持续观察，不能把该 helper 写成必然永久订阅，也不能把初始 Expires=0 写成向别名 owner 发停用请求。

- 值是订阅请求值，不是授予的永久有效期。此段没有完整续订、NOTIFY 丢失恢复、超时回退或选中结果缓存有效期算法。
- PUBLISH 激活/停用意图、SUBSCRIBE 查询生命周期和 PIDF expires 是不同对象，不可仅按 0/最大数值类比。

依据：§22.2.2.2.8 step4 and NOTE6，印刷页 488。

## owner查询响应与错误边界

适用条件：owner 收到 §22.2.2.3.7 入口的 SUBSCRIBE：Request-URI 指向关联别名的 CF PSI，P-Asserted-Service 为 MCData ICSI，Event 为 presence，且含 per-functional-alias simple-filter body。

owner 的 step1 从 mcdata-info+xml.mcdata-request-uri 确定 requested alias。Expires 缺失或为非零且小于4294967295时，返回 423，Min-Expires=4294967295，并停止；别名不存在的分支规定 403 和停止，但句内错误地写向 PUBLISH 响应。通过这些步骤后生成 SUBSCRIBE 的200，并在订阅期间按 .3.8 通知。该200不是一个目标用户 ID，也不代表 SDS 发送获准或消息送达。

- 保留不存在分支的 SUBSCRIBE/PUBLISH 冲突，不据此生成一条向另一个事务响应的实现规则。
- 入口四项未重复列 mcdata-info body，但 step1 实际读取它；本页不补缺失该字段时的错误码。
- 该查询段没有完整列出 owner 对查询者的权限算法；“本段未写”不代表任意查询者获准，也不能用激活授权规则替代查询或 SDS 发送授权。
- 0 不落入“非零且小于最大值”的 423 条件，但这只表示未触发此项拒绝。

依据：§22.2.2.3.7，印刷页 494、495。

## 状态结果不等于数据送达

适用条件：owner 按 §22.2.2.3.8 为解析订阅发送通知，或解析调用方收到含按 §22.3.1 构造的 per-functional-alias PIDF body 的 NOTIFY。

owner 为所请求别名的已成功激活用户生成 per-functional-alias PIDF 并发 NOTIFY；该语法以 presence.entity 标识别名，tuple.id 标识 MCData ID，functionalAlias 的 user 属性按原文标识 MCData client ID，expires 可选。§22.2.2.2.8 的接收段要求确定激活该别名的用户 ID(s)及激活状态，之后由 SDS CF 的选人分支决定一个目标；通知本身不是发给这些人的 SDS，也不是 DELIVERED/READ。

- 接收段处在服务器过程，却以 MCData client 为主语；保留角色文字冲突，不静默宣称该段已给出完整服务器接收状态机。
- .3.8 的入口目的称已成功激活用户，但其内部步骤没有像 .2.5 那样显式重述过期/deactivated 条目过滤。不能从相邻通知过程搬来过滤、排序、去重或实时一致性算法。
- per-functional-alias 语法对 tuple 数量和成员呈现存在文字限制，本页不据此自拟多用户 XML 编码。实际 0 个或多个 ID 的 SDS 处理只按 §9.2.2.4.2 的明确分支。

依据：§22.2.2.3.8;22.2.2.2.8 NOTIFY paragraph;22.3.1.2 per-functional-alias syntax，印刷页 488、495、496。

## 证据边界

- 限所列普通控制面standalone SDS与别名解析条款，不覆盖完整端到端安全上下文、RFC事务行为或可执行XML过滤器验证。
- 别名解析、数据发送授权与送达/已读证据是不同步骤；来源异常不由本页静默修复。

## 按需继续

- [sds-functional-alias-target-routing](sds-functional-alias-target-routing.md)
- [functional-alias-observation](functional-alias-observation.md)
- [functional-alias-state-evidence](functional-alias-state-evidence.md)
- [xml-inbound-validation](xml-inbound-validation.md)
- [xml-server-forwarding](xml-server-forwarding.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

- §22.2.2.2.8 NOTIFY paragraph：服务器解析过程的接收段以 MCData client 为主语。 保留角色差异，不静默改为server。
- §22.2.2.2.8 step6;22.2.2.3.7 entry3：Events与Event字面不一致。 说明presence意图，不宣称可直接发送的正确头字段模板。
- §22.2.2.2.8 step7;22.2.2.3.7 entry4;22.3.2：解析调用要求per-functional-alias限制，22.3.2标题内容实际为per-user过滤，include由MCData ID构造。 不把该用户ID路径静默替换为alias路径；只核查询意图、结果和差异，RFC4661及可执行filter未验。
- §22.2.2.3.7 step3：SUBSCRIBE不存在别名拒绝分支句内写response to SIP PUBLISH及RFC3903。 保留请求名称/引用冲突；不构造向PUBLISH事务回包的算法。
- §22.3.1.2 per-functional-alias steps3,5,7,8：文字写one tuple，并以tuple.id承载MCData ID、其下functionalAlias按MCData ID提供信息，user属性又为client ID。 如实区分身份；多用户编码不补模板。
