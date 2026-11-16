# MCS服务器订阅：服务器身份而非GMC令牌模板

ETSI正式发布的TS24.481 V19.3.0，Release19，Stage3。

本页MCPTT ICSI值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`；Contact使用 `g.3gpp.icsi-ref`。

前提：MCS服务器订阅MCS组文档变化；本角色此条款不包括GKTPs订阅。

## 发送初始SUBSCRIBE

采用AS发起程序；resource-lists逐文档列entry，以本服务器配置XCAP root为相对URI基址。Request-URI为GMS配置的订阅代理公共服务身份；P-Asserted-Identity为MCS服务器公共服务身份，不照抄GMC的access-token身份模板。 [§6.3.13.2.2 initial subscription](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)

## 发送初始SUBSCRIBE

P-Asserted-Service携带MCPTT ICSI，Contact携带对应g.3gpp.icsi-ref标签。MCPTT标识的历史使用不把组管理限定成MCPTT业务。 [§6.3.13.2.2 initial subscription items e/f](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)

## 收到关联NOTIFY或修改文档列表

NOTIFY按RFC5875处理；更新列表以re-SUBSCRIBE携带逐文档resource-lists相对URI和Contact服务标签，仍按AS发起程序。这里不重新列出初始全部头字段，不应推断其他SIP规范要求被免除。 [§6.3.13.2.2 notification/re-subscription paragraphs](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)

## 边界

这里只描述请求角色与构造；不提供GMS代理端授权分支或RFC5875完整通知状态机。

[change-subscription](change-subscription.md) · [subscription-refresh](subscription-refresh.md) · [constituent-subscription](constituent-subscription.md) · [结构化条件](server-subscription.json)

- [组文档获取之后的呼叫准入](prearranged-admission.md)
