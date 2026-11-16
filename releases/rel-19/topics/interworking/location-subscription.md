# 互通位置订阅：双向授权与原文冲突

TS23.283 V19.5.0，Release 19，Stage 2。LMS是位置管理服务器，LMC是位置管理客户端；IWF按需转换MC与LMR身份。

## MC服务器或LMC订阅LMR用户事件触发位置

请求先到LMS；LMS核查信息和配置、识别LMR目标后转IWF。IWF可检查许可，应用订阅并响应LMS；LMS可依TS23.280回应发起方。 [§10.11.4.2.3.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## IWF需要订阅MC用户位置通知

IWF确定MC目标并请求LMS；LMS核查信息和配置后应用订阅。此处不能据引言的反向描述改写这五步。响应端点存在图文冲突，见本主题的conflict条目。 [§10.11.4.2.3.2 steps 1–5](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 需要确定反向订阅响应端点

图示响应为LMS到IWF，但引言描述正向流程，step 6写LMS到LMS。保留来源冲突，不把推测修正当作已确定的接口契约。 [§10.11.4.2.3.2 figure and step 6](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

§10.11.4.1的信息字段转引TS23.280，本页未核验这些字段或Stage3编码。

伙伴系统位置限制的配置机制不在§10.11.4.2范围；请求机会不等于无条件授权，也不保证获取新测量。

相关：[location-query](location-query.md) · [location-unsubscribe](location-unsubscribe.md) · [privacy](../location/privacy.md) · [结构化条件](location-subscription.json)
