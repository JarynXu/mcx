# SDS通知经过参与功能：身份绑定、重交付与目标路由

TS24.282 V19.7.0普通在网SDS带外通知；请求已按相应SDS disposition notification命名入口进入12.2.2.1或12.2.2.2。服务器入口分类见6.3.1.1 p89，终接客户端请求分类见6.2.1.1 p54。

入站XML按适用6.5程序处理后才进入本文步骤；发出XML也受6.5约束。本文只核6.5.1的适用和先后关系，不替代完整密码验证、密钥或配置过程。

本文讨论通知转发与暂存证据，不把任一SIP响应当作原SDS已显示、应用完成或重交付成功。

## 通知发出者先通过身份绑定

适用条件：PF收到来自MCData用户的SDS disposition notification，执行12.2.2.1。

资源不足或拥塞风险可触发500拒绝，可带Retry-After并停止。未因此拒绝时，PF从P-Asserted-Identity中的public user identity确定通知发出者MCData ID；绑定不存在或已过期，必须404加Warning 141并停止，不能先转发或暂存再补身份。



依据：§12.2.2.1 steps1–3 and NOTE1，印刷页 315。

## UNDELIVERED停止普通转发链

适用条件：PF处理来自用户的SDS disposition notification；资源及通知发出者绑定检查未终止处理，通知类型为UNDELIVERED。

PF按step5暂存message用于重交付，启动正文称TD1的计时器，然后停止剩余步骤。它不沿本次普通通知转发链进入CF；计时到期后的尝试不证明实际送达。

- 正文只称message，未在此给出如何保留或取回原SDS载荷、重建请求的完整算法；不得把SDS NOTIFICATION自身当成原始数据载荷。
- step5未明写此停止分支独立的最终SIP响应，不套用后面针对已发出转发请求的响应处理。
- TD1与F.2.1的TDP1名称差异保留。

依据：§12.2.2.1 step5 and NOTE2，印刷页 316。

## 成功通知清除适用的暂存

适用条件：PF处理来自用户的SDS disposition notification；资源及绑定检查通过；类型为DELIVERED、READ或DELIVERED AND READ，且message此前已暂存用于重交付。

PF删除临时存储中的message并停止正文称TD1的计时器。该步骤没有要求停止后续通知转发。F.2.1另以TDP1列出默认60秒、可配置、每个SDS可有独立实例；本稿不裁决两名称，也不从该表推导无限重试或送达保证。

- 未暂存时不适用step6的删除条件；不把收到任意2xx替代这里指定的通知类型。
- 重试次数、重复通知去重和最终放弃条件未由所核条款给出。

依据：§12.2.2.1 step6;F.2.1 TableF.2.1-1 and NOTE，印刷页 316、638。

## 发出侧参与功能转往控制功能

适用条件：PF处理来自用户的SDS disposition notification；12.2.2.1的资源和绑定门槛未阻断，UNDELIVERED停止分支不适用，已执行适用的暂存清理。

PF生成新MESSAGE，Request-URI指向CF的public service identity，复制收到的MIME bodies，附SDS的P-Asserted-Service，并以PF自己的PSI作为P-Asserted-Identity后发送。收到此转发请求的202或200时，分别生成相同类别响应给通知发出客户端；收到4xx/5xx/6xx则转送响应并保留收到的Warning字段。

- step10还规定在其所述条件下补mcdata-info和通知发出者MCData ID，但其交叉引用step8与step8内容不对应（step8实际设置Request-URI）；不据此宣称已存在的XML身份一定被覆盖或重新绑定。
- CF PSI发现与跨域网关路由在原文NOTE6/7中列为范围外。

依据：§12.2.2.1 steps7–15 and response handling，印刷页 316、317。

## 回执目标另行检查绑定

适用条件：PF收到来自CF、面向终接MCData客户端的SDS disposition notification，执行12.2.2.2。

资源不足或拥塞风险可触发500拒绝并停止，可带Retry-After。继续时，PF用mcdata-request-uri中的目标MCData ID查找其public user identity绑定；不存在则404并停止。这里检查通知接收目标，不是再次把CF的P-Asserted-Identity当作原SDS用户。

- 本分支未重述12.2.2.1的过期条件或Warning 141；不据此声称过期一定可用，也不移植为此分支明文错误码。

依据：§12.2.2.2 steps1–3，印刷页 317。

## 终接以公共用户身份寻址

适用条件：PF处理来自CF的SDS disposition notification，12.2.2.2的资源和目标绑定门槛未终止处理。

PF调用6.3.2.1：出站Request-URI为目标MCData用户所绑定的public user identity，保留收到的Accept-Contact/Reject-Contact及其参数，按6.4组织MIME，并用PF自己的PSI作P-Asserted-Identity。随后补SDS P-Asserted-Service并发送；收到该请求的2xx/4xx/5xx/6xx，转给CF。目标用户ID、用户public identity、服务器PSI不是可互换的地址。

- 不把helper的MIME封装规则扩写成未明示的全部body逐字复制算法；安全处理仍适用6.5。

依据：§12.2.2.2 steps4–6 and response handling;6.3.2.1;6.4，印刷页 95、123、317。

## 证据边界

- 仅限本页指定SDS通知分支，安全子程序、完整事务行为与部署配置另行核验。

## 按需继续

- [sds-disposition-timing](sds-disposition-timing.md)

[ETSI TS124282 V19.7.0 / 3GPP TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

### 相关服务器路径

- [SDS通知控制功能：原消息关联、组成员检查与聚合窗口](sds-disposition-aggregation.md)

## MCData具体XML程序

- [xml-inbound-validation](xml-inbound-validation.md)
- [xml-server-forwarding](xml-server-forwarding.md)

这些指定程序依据TS24.282 V19.7.0；不从其他安全架构页的可选机制表述推导MCData配置缺项即关闭。

## TLV信令与用户数据

- [MCData TLV 信令逐段保护：谁解密，何时为下一段重新加密](tlv-signalling-hop-protection.md)

本组职责依据TS24.282 V19.7.0，不用XML程序替代TLV或用户Data验证。

- [设置刷新、退出与绑定失效](service-settings-validity.md)
