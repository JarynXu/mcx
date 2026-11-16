# 组成组GMS订阅临时组：跨服务商寻址

ETSI正式发布的TS24.481 V19.3.0，Release19，Stage3。

本页MCPTT ICSI值为 `urn:urn-7:3gpp-service.ims.icsi.mcptt`；Contact使用 `g.3gpp.icsi-ref`。

前提：订阅方GMS拥有临时MCS组的一个组成组；目标临时组有MCS group ID。

## 订阅临时组文档、该组GKTP文档的GKTPs元素或两者

初始SUBSCRIBE含application/resource-lists+xml正文，每个目标文档或元素一个entry；GKTPs目标由对应GKTP文档选择器加GKTPs节点选择器定位。采用AS发起SUBSCRIBE。目标组属于本服务商时，相对entry基址用本方XCAP root，Request-URI用本GMS文档访问公共服务身份；目标属于其他服务商时，两者分别从组ID路由库与目标组ID导出，不能一律发给本方订阅代理。 [§6.3.13.2.3 items a/c](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)

## 构造该组成组GMS的初始SUBSCRIBE

P-Asserted-Identity为自己的文档访问公共服务身份；mcptt-info的mcptt-calling-group-id标识组成组，而非目标临时组。P-Asserted-Service及Contact携带规定的MCPTT ICSI信息。 [§6.3.13.2.3 items d–g](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)

## 边界

仅覆盖组成组GMS充当订阅者的初始请求；不覆盖GMS代表GMC代理订阅，两种角色不可混用。

GKTP文档内容和密钥处理不由本页定义；只描述资源寻址。

[server-subscription](server-subscription.md) · [forwarding](forwarding.md) · [change-subscription](change-subscription.md) · [结构化条件](constituent-subscription.json)

进一步核对：[代理和拥有方授权](subscription-proxy.md)、[未知扩展处理](unknown-extensions.md)。
