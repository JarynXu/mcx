# 互通当前发言者位置：话权不等于公开许可

TS23.283 V19.5.0，Release19，Stage2。

## MC客户端1、客户端2及IWF参与进行中组呼；客户端1为当前发言者且服务器已取得其位置

客户端1取得话权后，服务器检查发言者的位置共享隐私策略；允许时才向客户端2及IWF提供位置。floor taken携带位置是可选途径，不是获得话权后的无条件披露。 [§10.11.2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## MC客户端1、客户端2及IWF参与进行中组呼；LMR用户通过IWF作为当前发言者

IWF取得话权后，服务器检查当前IWF用户的位置共享隐私策略，以决定能否提供给其他MCPTT用户。服务器如何获取LMR用户位置不在此条款范围，不能把该过程补写成自动测量。 [§10.11.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 使用边界

TS23.280位置分发与TS23.379隐私配置、floor taken编码仅被引用，未在本主题核验。

§10.11.3可选floor taken一句列出客户端2与IWF，和该节总体LMR到MC叙述不完全一致；本主题不据此确定反向可选消息的精确接收集合。

[location-query](location-query.md) · [privacy](../location/privacy.md) · [late-entry](late-entry.md) · [结构化条件](talker-location.json)
