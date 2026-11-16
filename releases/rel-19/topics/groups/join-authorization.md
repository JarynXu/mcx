# 加入已有组会话：成员、许可规则与服务字段

适用 TS24.379 V19.4.0 §6.3.5.3：控制功能判断用户加入已有组会话的组文档授权。

本主题只解释授权判定，不取代父流程的归属、媒体、会话状态和响应处理。

## 成员和加入规则须同时成立

适用条件：控制功能针对来话 INVITE 中的 MCPTT 用户执行加入授权判定。

组文档 list 中必须存在该用户的 entry；还必须有一条匹配 rule，其 actions/join-handling=true。匹配方式是 conditions 含 is-list-member，或者 identity 含匹配该 MCPTT ID 的 entry。identity 规则不能免除成员 entry 要求，allow-initiate-conference 也不能替代 join-handling。

依据：§6.3.5.3 steps 1–2。

## 缺少服务字段不等于缺少加入规则

适用条件：执行加入已有组会话的服务条件检查。

supported-services 存在时须含 enabler=MCPTT ICSI 的 service；在这一条件内，group-media 存在时须含 MCPTT speech。缺失这些可条件检查的元素，不单独触发该项拒绝，但成员与匹配加入许可仍必需。这与普通预安排组呼发起分支明确要求 supported-services 和 group-media 存在不同；不能把发起检查的缺字段规则套给加入。

依据：§6.3.5.3 step 3; 6.3.5.4。

## 证据边界

- 这里不据缺字段分支判断任意组文档在配置规范中是否合法。
- 未定义多个冲突规则的合并优先级；不补充 first-match 或 deny-overrides。
- 组文档授权通过不证明本次客户端已归属、已被邀请、已接通或已获话权。
- 本页未给父流程全部 SIP 失败码或加入进行中呼叫的完整状态机。

## 按需继续

- [prearranged-admission](prearranged-admission.md)
- [../calls/group-acknowledged-start](../calls/group-acknowledged-start.md)
- [../security/group-key-membership](../security/group-key-membership.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页161、162、163；仅本版本。
