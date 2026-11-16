# 互通SDS：地址映射与代理回执

TS23.283 V19.5.0，Release19，Stage2。

## MC用户与单个LMR用户之间的SDS；使用信令控制面或媒体面

发往LMR用户时，目标是分配给该LMR用户的MCData ID；LMR用户发起时源地址使用其分配的MCData ID。IWF以对等MCData服务器角色参与，基础发送过程仍依赖TS23.282。 [§10.8.6–7](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## MC用户向包含LMR用户的MCData组发送SDS；使用信令控制面或媒体面，跨侧客户端位于已归属该组的IWF后

消息寻址到MCData组ID。IWF可代表后方客户端回应disposition请求，给出精确值 disposition prevented by system；这种代理结果不是LMR终端已送达或已读的证明。 [§10.8.8](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

仅解释跨侧地址及明确的代理回执例外，不覆盖TS23.282的SDS建立、传输、错误状态机和协议编码。

[scope](scope.md) · [affiliation-results](affiliation-results.md) · [delivery-evidence](../mcdata/delivery-evidence.md) · [结构化条件](sds-addressing.json)
