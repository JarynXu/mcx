# 互通位置取消：仅撤销相应订阅

TS23.283 V19.5.0，Release 19，Stage 2。LMS是位置管理服务器，LMC是位置管理客户端；IWF按需转换MC与LMR身份。

## MC侧取消先前向LMR侧建立的事件触发位置订阅

MC服务器或LMC向LMS提出取消；LMS检查许可并定位LMR目标后转IWF。IWF可检查许可，取消订阅并响应LMS；LMS可依TS23.280转发响应。仅取消相应订阅，不代表停止全部位置报告。 [§10.11.4.2.4.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## IWF取消先前向MC侧建立的位置订阅

IWF确定需取消及MC目标，向LMS请求；LMS检查许可、取消后向IWF响应。此流程处理相应订阅，未规定关闭其他订阅或全部位置报告。 [§10.11.4.2.4.2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

§10.11.4.1的信息字段转引TS23.280，本页未核验这些字段或Stage3编码。

伙伴系统位置限制的配置机制不在§10.11.4.2范围；请求机会不等于无条件授权，也不保证获取新测量。

相关：[location-query](location-query.md) · [location-subscription](location-subscription.md) · [privacy](../location/privacy.md) · [结构化条件](location-unsubscribe.json)
