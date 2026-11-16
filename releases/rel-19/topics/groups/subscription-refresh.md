# GMC订阅更新与通知：资源列表和保护上下文

ETSI正式发布的TS24.481 V19.3.0，Release19，Stage3。

本页MCPTT ICSI值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`；Contact使用 `g.3gpp.icsi-ref`。

前提：GMC已有由初始SIP SUBSCRIBE建立的组文档或GKTPs元素订阅。

## 收到与该订阅关联的SIP NOTIFY

需要身份隐藏时先按TS24.379执行保密及完整性保护程序，再按RFC5875处理NOTIFY；不能把收到通知直接等同于可以无条件使用未校验内容。 [§6.3.13.2.1 notification paragraph](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)

## 修改所订阅的文档或GKTPs元素列表

发送re-SUBSCRIBE，resource-lists中按每个待订阅对象放entry，以GMC配置XCAP root为相对URI基址；GKTPs还需对应节点选择器。Contact保留MCPTT ICSI媒体特征标签。 [§6.3.13.2.1 re-subscription paragraph](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)

## 修改订阅列表且需要身份隐藏

对mcptt-info和resource-lists正文按TS24.379保护，并使用初始SUBSCRIBE所含CSK；本条不要求每次列表更新重新协商一把CSK。 [§6.3.13.2.1 re-subscription item b](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)

## 边界

引用的TS24.229、TS24.379及RFC5875完整处理规则未核验；此处不提供订阅到期、终止、重传或xcap-diff应用算法。

[change-subscription](change-subscription.md) · [server-subscription](server-subscription.md) · [xcap-addressing](xcap-addressing.md) · [结构化条件](subscription-refresh.json)
