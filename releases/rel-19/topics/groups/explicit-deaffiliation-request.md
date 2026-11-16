# 显式退组：移除部分兴趣组与本客户端全部退出

在网显式affiliation状态变更；排除隐式取消、重组移除、退出登录及协商MESSAGE确认流程。

请求构造仍遵循§9.2.1.2：PUBLISH发往服务用户的O-PF PSI，正文业务目标为MCPTT用户ID，PIDF按用户→客户端→组编码；本页只说明退组差异。

## 规则满足时可能禁止手动退组

适用条件：用户手动表示不再对组感兴趣，且该组affiliation由满足规则触发，且对应用户profile的manual-deaffiliation-not-allowed-if-affiliation-rules-are-met=true。

客户端必须抑制该用户请求；显示提示仅为可选。配置位置是OnNetwork/anyExt/GroupList/entry/anyExt内对应组元素，不是所有手动撤销一律禁止。

依据：§9.2.1.2 opening。

## 部分退组仍发布全部剩余兴趣组

适用条件：目标用户在目标客户端仍对至少一组感兴趣，包括撤销部分组而保留其他组的情况。

Expires必须4294967295；PIDF包含该用户在该客户端仍感兴趣的全部组，而不是仅被删组列表。该规则也可能同时变更加入与退出；仅撤销任务不应擅自添加兴趣组。

依据：§9.2.1.2 steps4,6。

## Expires零只表示该客户端全部退出

适用条件：目标用户在目标客户端不再对任何MCPTT组感兴趣。

Expires必须0。该请求表达目标用户在这个客户端不再感兴趣，不表示其他客户端也请求退出，也不保证服务器处理不影响其他客户端。

依据：§9.2.1.2 step5。

## 退组状态不证明呼叫已拆除

适用条件：已发显式PUBLISH撤销或已观察到deaffiliating/deaffiliated。

本次核查的§9.2.1.2和§9.2.2.2.3/.6/.7、§9.2.2.3.3未给出可据此宣称已发送BYE或已完成进行中呼叫退出的步骤。必须另查相应呼叫释放程序；不能把状态记录变化当呼叫拆除完成，也不能据此断言呼叫必然继续。

依据：§9.2.1.2;9.2.2.2.3;9.2.2.3.3。

## 证据边界

- §9.2.2.3.3先200后禁止FA时403的顺序冲突。
- §9.2.2.3.3 step10a使用served MCPTT ID而该处理路径此前识别handled MCPTT ID。
- 一个client撤销但其他client仍保留同组时，§9.2.2.2.6撤销Expires0与正文仍包含其他client，组端零expiry删除用户整体记录之间有张力；不可声称跨client撤销安全已闭合。
- 本次未核RFC3903完整ETag/条件发布/重试、24.229传输认证、GMS与FA配置取得过程。
- 本次未从第9章得出进行中呼叫退出时序；不要把未见BYE当作必须保持通话的肯定命题。
- 客户端应先启动状态确定过程观察变更结果。不得只凭PUBLISH200认定逐组撤销完成；PUBLISH Expires0和初始SUBSCRIBE Expires0的含义不同。
- 完整PIDF构造、p-id关联与授权检查分别见发布、状态观察及服务器处理主题。

## 按需继续

- [explicit-affiliation-publish](explicit-affiliation-publish.md)
- [explicit-affiliation-observation](explicit-affiliation-observation.md)
- [explicit-deaffiliation-state](explicit-deaffiliation-state.md)
- [../calls/group-release-timers](../calls/group-release-timers.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页206、207、211、212、213、214、228、229、230；仅本版本。
