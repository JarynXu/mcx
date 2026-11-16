# 向功能别名发送 SDS：解析选人、300 与直接 ID 重发

限 TS24.282 V19.7.0 普通在网 one-to-one standalone SDS 的信令控制面 SIP MESSAGE，包含其进入前的相关准入检查。正常客户端须经 §9.2.1.1 准入成功且 payload≤max-payload-size-sds-cplane-bytes 才选此分支；拒绝条件用于判断能否继续。不覆盖媒体面、SDS session、FD、组或 ad hoc 分发、紧急/优先级扩展和跨域网关实现。

从功能别名作为目标的初始请求，到 CF 解析/选择及客户端收到 300 后生成直接 MCData ID 请求；不研究激活、接管、别名到组绑定。每条服务器结论只在该入口和前置检查未拒绝时成立。

适用 XML/TLV/密钥处理仍是独立依赖。本页研究标识、授权与路由，不声称已闭合首次端到端安全上下文创建或完整可执行 SIP/XML 实现。

## 目标别名与发送者别名

适用条件：客户端按 §9.2.2.2.1 构造发送到一个功能别名的 one-to-one standalone SDS。

客户端将目标功能别名放入 resource-lists 的 entry.uri，将 request-type 设为 one-to-one-sds，并在 mcdata-Params.anyExt 中携 call-to-functional-alias-ind=true。SIP Request-URI 仍为服务发送用户的 PF 公共服务身份，而非该别名。functional-alias-URI 是客户端已知并选择附带的活动别名信息，不替代 entry.uri 中的被叫目标。

- 此处的三个对象分别是服务路由、目标别名和随发送附带的活动别名；不能仅因发送者自身某别名 activated 就认定目标选定或本次发送获准。
- 本页不生成完整报文模板；service feature tags、SDS payload、必要安全 MIME 仍须由各自步骤构造。

依据：§9.2.2.2.1 steps1,2a,2b;6.2.4.1 steps1,4，印刷页 61、192。

## 选中ID不继承发送许可

适用条件：客户端执行发送准入，或 O-PF 收到初始别名请求/收到按 300 结果重建的直接 ID standalone SDS 请求。

§11.1 的 one-to-one 许可仍适用：allow-transmit-data 缺失或 false 阻断；若 One-to-One-Communication 存在且列有 entry，则按当前 resource-lists.entry.uri 与配置条目比较，不匹配即不允许并停止。O-PF 对收到的请求还验证服务授权绑定并调用 §11.1。因此 CF 选出了一个 ID，不会把别名激活权限自动转成向该 ID 发送数据的权限；直接 ID 新请求到达 O-PF 后仍受其普通检查。

- 不把配置中的别名 URI 自动扩展为对所有解析 ID 的许可，原文未给出这种授权继承规则。
- 此条不新增“收到 300 即再次调用 §9.2.1.1”的客户端步骤；确定的重新检查来自 O-PF 对新入站 MESSAGE 执行相同入口。
- 绑定不存在或过期为 404/141；相关发送拒绝 403/200、403/229 及大小限制详见 sds-server-identities-and-private-admission 与 sds-transmission-selection。Warning 编号不是 SIP 状态码。

依据：§9.2.1.1 steps1–2;9.2.2.3.1 steps2–8;11.1 steps1,1A，印刷页 189、190、195、196、197、310。

## 解析前的MIME与目标数量门槛

适用条件：CF 收到按 standalone SDS 入口分类的请求，request-type=one-to-one-sds；前置资源检查未拒绝。

CF 要求 mcdata-info+xml、mcdata-signalling 和 mcdata-payload 三类 MIME 齐备，否则 403/199 并停止；one-to-one SDS 服务尺寸上限超限时 403/218 并停止。resource-lists 缺失或其 list 集合合计超过一个 entry 时，403/204 并停止。别名解析不豁免这些检查，也不能用一个 one-to-one 请求中列多个别名来请求多目标发送。

- 正文对已存在但含零 entry 的列表没有在这个检查中给出明确同类拒绝；本页可用解析链限定恰好一个别名 entry，不补零 entry 算法。
- 列表 entry 数与单个别名解析出的 MCData ID 数不是同一计数。后者可以不止一个，但后续仍选择一个。

依据：§9.2.2.4.2 steps1–5b(i);11.1 step3，印刷页 201、202、310、311。

## CF选一个用户并返回300

适用条件：CF 已通过前置检查，one-to-one-sds 请求恰好含一个目标别名 entry，且 mcdata-Params.anyExt.call-to-functional-alias-ind=true。

CF 按 §22.2.2.2.8 查找已经激活该被叫别名的 MCData ID(s)。若无法确定任何 ID，回 403/145 并停止；否则选择其中一个 ID，在 SIP 300 的 mcdata-info body 中以 mcdata-request-uri 返回该选中 ID，然后停止本条余下步骤。选择方法由实现决定。因此多个激活者不表示向他们全部发送，300 也不是此原始请求的 202 接受或送达回执。

- 本分支没有要求客户端从一组候选中自行挑选；返回体带的是 CF 已选出的一个 ID。
- “未能确定任何 activated ID”不等于已证明别名不存在；owner 查询中的别名不存在拒绝与这里的 SDS 403/145 是不同协议步骤。
- CF 明确停止，不能继续沿同一次原始别名请求执行 step5b(iii) 直接发送或 steps7–8 的 202。

依据：§9.2.2.4.2 step5b(ii) and NOTE2，印刷页 202。

## 客户端新建直接ID请求

适用条件：客户端收到了针对其初始 one-to-one standalone SDS MESSAGE 的 SIP 300，响应 mcdata-info body 带 mcdata-request-uri 选中 ID。

客户端以返回 ID 作为被邀用户 ID，依 §9.2.2.2.1 生成新的 SIP MESSAGE：resource-lists.entry.uri 改为该 ID；不再携 call-to-functional-alias-ind；另在 mcdata-Params.anyExt 的 called-functional-alias-URI 保留初始请求的目标功能别名。这里是新请求和目标重写，不是重发未改变的别名请求，也不是证明接收者已收到 SDS。通过普通检查后，直接 ID 分支才按 §9.2.2.4.1.1 发往该用户的 T-PF。

- O-PF 的 §9.2.2.3.1 响应段显式列出 200、202、4xx/5xx/6xx，未列 300 专门转发步骤。本页只串接 CF 发出及客户端收到后的明确动作，不补中间 SIP 响应传递算法；该依赖须由 24.229/RFC 事务规则另核。
- 300 段的 MIME 名字写 application/vnd.3gpp.mcdata-info，其他步骤使用 +xml，保留差异，不输出自称规范完备的编码模板。
- 直接 ID 后的服务绑定、入站名单及送达/已读证据复用既有直接 ID 主题；解析时的活动状态不保证后续时刻仍保持激活，也不证明任何应用消费完成。

依据：§9.2.2.2.1 SIP300 handling steps1–3;9.2.2.4.2 step5b(iii);9.2.2.4.1.1 steps5a,6，印刷页 194、195、199、200、202。

## 发送者附带别名的独立检查

适用条件：one-to-one SDS 请求另外含 functional-alias-URI；客户端仅在知道活动别名且选择附带时加入，O-PF 处理该字段。

O-PF 检查该 functional-alias-URI 是否对已确定的发送用户 MCData ID 处于 activated 状态；是则沿用收到的值，否则不包含该字段。这是发送用户附带别名的检查，与 CF 对 entry.uri 中被叫别名解析后选人的过程不同；其通过不能替代目标许可或送达。

- §9.2.2.3.1 step12A 位于 MESSAGE 流程却把出站写作 INVITE。本页保留该原文异常，仅提取该字段的 activated 检查和不包含分支，不默默修正请求方法。
- 该字段被省略的分支未规定因此拒绝整个 SDS 请求，不能自行加上拒绝码。

依据：§9.2.2.2.1 step2b(ii)B;9.2.2.3.1 steps2,12A，印刷页 192、195、197、198。

## 证据边界

- 限所列普通控制面standalone SDS与别名解析条款，不覆盖完整端到端安全上下文、RFC事务行为或可执行XML过滤器验证。
- 别名解析、数据发送授权与送达/已读证据是不同步骤；来源异常不由本页静默修复。

## 按需继续

- [functional-alias-state-evidence](functional-alias-state-evidence.md)
- [sds-functional-alias-resolution](sds-functional-alias-resolution.md)
- [sds-server-identities-and-private-admission](sds-server-identities-and-private-admission.md)
- [sds-server-responses-and-routing](sds-server-responses-and-routing.md)
- [sds-transmission-selection](sds-transmission-selection.md)
- [sds-disposition-timing](sds-disposition-timing.md)
- [xml-inbound-validation](xml-inbound-validation.md)
- [protected-data-client-verification](protected-data-client-verification.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

- §9.2.2.3.1 step12A：MESSAGE流程的发送者 functional-alias-URI 检查分支把出站写成 INVITE。 不改请求方法；只陈述该字段 activated 检查及不包含分支。
- §9.2.2.4.2 step5b(ii);9.2.2.2.1 SIP300 handling：300相关正文使用 application/vnd.3gpp.mcdata-info，而一般字段构造用 +xml。 保留原文差异，不输出经过schema验证的模板。
- §9.2.2.3.1 response handling：显式列200/202/4xx–6xx而未列300转发；CF发送和客户端接收300另有明确步骤。 不造中间事务传播行为；24.229/RFC依赖未核。
