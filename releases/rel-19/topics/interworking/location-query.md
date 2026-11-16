# 互通位置：按需查询与通知

TS23.283 V19.5.0，Release 19，Stage 2。LMS是位置管理服务器，LMC是位置管理客户端；IWF按需转换MC与LMR身份。

## MC服务服务器或LMC请求LMR用户位置

LMS依据请求信息及配置检查许可、确定LMR目标，再向IWF请求。IWF可另作授权检查，取得与请求中MC身份对应的LMR位置，报告经LMS返给请求方。 [§10.11.4.2.1.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## IWF需要MC用户位置

IWF确定MC目标后请求LMS；LMS授权、取得位置并返给IWF。图称返回消息为response，正文称report并引用§10.11.4.1.1，不能据此杜撰两个协议消息。 [§10.11.4.2.1.2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## LMS或IWF判断有可通知的位置

双方均可向另一方发送位置通知。该过程未要求每次通知重新测量，不能单凭通知断言位置新鲜。 [§10.11.4.2.2.1–2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

§10.11.4.1的信息字段转引TS23.280，本页未核验这些字段或Stage3编码。

伙伴系统位置限制的配置机制不在§10.11.4.2范围；请求机会不等于无条件授权，也不保证获取新测量。

相关：[location-subscription](location-subscription.md) · [location-unsubscribe](location-unsubscribe.md) · [privacy](../location/privacy.md) · [结构化条件](location-query.json)
