# 存储启停请求：用户授权与全体、指定名单

限TS24.282V19.7.0§21.3的在网通信存储控制，由MCData用户请求客户端发起；不把用户操作等同于修改授权profile。

本页描述协议的范围选择和必要字段，不提供完整SIP/XML报文；PF存在独立检查，尤其指定名单body要求的原文差异。

## 用户选择仍受配置许可约束

适用条件：用户请求开启或关闭私人和/或组通信在Message Store中的存储。

§21.3.1先区分profile是否允许控制通信存储，再区分私人和组通信的控制许可。只有在获准的范围内，用户才选择是否存储。启用与停用入口都要求客户端检查ruleset中的allow-store-comms-in-msgstore；该元素缺失或false时，客户端须告知用户并退出。因此disable也不绕过这一入口许可，用户选择不会自行授予存储控制权限。

- 这里只列24.282明确使用的profile字段和行为，未读取24.484的完整配置schema或配置管理过程。
- 不把profile总体许可解释为所有组均获准，也不自行增加客户端未明列的逐组错误码。

依据：§21.3.1;21.3.2.1;21.3.2.2 opening;21.3.2.3 opening，印刷页 472、473。

## 控制请求发往PF而非对象URL

适用条件：客户端通过入口许可检查，生成本次启用或停用请求。

客户端使用SIP MESSAGE，Request-URI指向服务本用户的originating PF公共服务身份；这不是向Message Store对象URL发HTTP请求。请求携MCData的P-Preferred-Service和Accept-Contact服务标识，后者带require、explicit；可携P-Preferred-Identity。mcdata-info XML中的request-type取store-comms-in-msgstore-ctrl-req，并携发起客户端的mcdata-client-id。若需要携活动功能别名，按该节的functional-alias-URI扩展规则处理。

- mcdata-client-id用于指出发起客户端，不代替PF从可信P-Asserted-Identity取得用户身份。
- 这里只说明服务标识及字段用途，不展开24.229、RFC3428/3841/6050或功能别名完整过程。D.1的字段扩展位置不能凭概念性列表改写成任意直接子元素。

依据：§21.3.2.2 steps1–5;21.3.2.3 steps1–5;D.1.3 request-type and mcdata-client-id，印刷页 472、473、474、586、587。

## 全体开关与指定名单分开

适用条件：用户分别选择私人或组通信的全部获准范围，或指定用户/组名单；客户端按相应启用或停用入口生成请求。

全体私人/组范围分别使用store-all-private-comms-in-msgstore或store-all-group-comms-in-msgstore，启用值为true，停用值为false。指定名单则使用对应store-specific-private-comms-in-msgstore或store-specific-group-comms-in-msgstore，值为enable或disable；只要包含任一specific字段，客户端步骤6要求再携application/vnd.3gpp.mcdata-msgstore-ctrl-request+xml body，根为msgstore-ctrl-command-list，在相应enable或disable下列private MCData ID或group MCData Group ID。客户端步骤及D.7允许列表零项或多项，但这不等于PF一定会对空名单改变任何目标。

- D.7允许根包含enable、disable或二者；本条不据此自定同一目标同时启停时的优先级。
- PF步骤4f另写resource-lists MIME body，与这里指定控制body不同；不能仅依本条构造一个已证明可互通的请求。

依据：§21.3.2.2 steps5b,5c,6;21.3.2.3 steps5b,5c,6;D.1.2 storageCtrlType;D.1.3 anyExt o–r;D.7.2;D.7.3，印刷页 473、474、584、589、624、625。

## 证据边界

- 未展开已存对象删除、HTTP访问令牌、对象内容保存或控制指令的重试算法。

## 按需继续

- [message-store-control-admission](message-store-control-admission.md)
- [message-store-control-result](message-store-control-result.md)
- [message-store-access-and-objects](message-store-access-and-objects.md)
- [service-authorization-binding](service-authorization-binding.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§21.3.2.2/.3 step5;D.1.2;D.1.3 anyExt o–r：客户端步骤概括mcdata-Params包含控制字段；D.1.3将这些字段列在anyExt说明下，schema另给全局字段类型和anyExt容器。 本页只描述字段语义和操作关系，不把概括性body列表强行展开成直接子元素XML；完整编码需同时遵循D.1并澄清正文/编码层级，未进行schema验证。
