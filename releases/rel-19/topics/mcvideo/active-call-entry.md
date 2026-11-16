# MCVideo按组ID进入已有呼叫：join检查与Warning123

TS24.281 V19.3.0，普通在网、带 transmission control、按需预安排组呼的进行中会话进入路径；普通 GMS 组，不含TGI/重组/预配置重组、NCF/gateway、chat、广播、ad hoc、功能别名、远程/ambient、离网或预建立会话。目标会话是否仍存在/active由各入口实际检查，客户端认为会话还在不代表CF一定找到它。

客户端 emergency state 未置位，组不处于MVEG2、MVIG2/MVIG4，客户端响应时不在MVEGC2/3或MVIGC2/3；请求不含emergency-ind、imminentperil-ind、alert-ind、用户请求优先级扩展或优先通信Resource-Priority；CF组的in-progress emergency与imminent-peril均为false。没有待处理的优先升级/取消。

每条claim只继承本主题common_conditions及自身conditions，不继承前条成功。以下三个入口必须分开：客户端用session identity重入、组ID发起链到CF后发现ongoing、CF收到通知后主动邀请晚进入者；不能把一个入口的检查/Warning自动移到另一个入口。

本页保留正文错引及独立版本边界；只把真实正文列出的状态与顺序当结论。IMS/RFC、媒体编码/密钥、配置schema及完整失败恢复依赖未全部闭合。

## 按组ID请求发现已有会话

适用条件：客户端采用普通按组ID发起链，Request-URI由serving PF PSI路由到CF PSI，而不是直接使用已知session identity；CF执行§9.2.1.4.2。

CF在完成该主条共用的资源、媒体/feature-tag、组文档初步处理等检查后，只有session identity已分配且MCVideo session active同时成立才判ongoing，转入step14而非新建step13。普通无constituent豁免、无priority indication范围内，未affiliated按§6.3.6返回403/120并停止；随后用join规则§6.3.5.3而不是发起规则§6.3.5.4，未获许可403/121并停止。

- 共用检查不因存在会话而跳过；具体组文档失败条件见prearranged-call-admission，不能直接把其“初建”common_conditions套到本入口。
- step14a与初建13a一样保留i–iv混合列项及or布局；本页只取未affiliated、无constituent豁免、无priority indication的普通交集，不裁决priority分组。

依据：§9.2.1.4.2 steps1–14;6.3.6，印刷页 139、140、226、227、228、230。

## 已有会话的容量检查

适用条件：按组ID到达CF的请求已判ongoing，已通过前置检查、affiliation与join许可；on-network-max-participant-count已经reached，且没有执行地方策略允许的可选移除participant分支。

CF返回486/122并跳过剩余步骤。地方策略若判请求者高于某现有用户，原文允许MAY移除一个participant并跳过该拒绝步骤；本页不展开替换。这个入口不用初建时“只选上限人数优先required”的名单筛选替代已进行会话的容量检查。

- 用户是否能被地方策略视为更高优先级，与其是否发起紧急通信不是同一条件。移除helper错引见rejoin-session，本页不静默修复。

依据：§9.2.1.4.2 step14c–d;9.2.1.4.4.3，印刷页 230、235。

## 成功响应中的Warning123

适用条件：按组ID到达CF的请求被判ongoing；通过共用检查、affiliation、join许可，容量未到上限；普通状态持续，无priority升级/告警分支。

CF生成200和SDP answer，必须带Warning123（MCVideo session already exists）；完成媒体处理后向发起者发送200，再通知conference订阅者该用户加入，最后不继续执行本主条后面的初建响应分支。123在这里是成功响应中的既有会话说明，不是404、拒绝、或让客户端自行另建一呼。

- 生成200的step14h引用6.3.3.2.4.2，但已读正文6.3.3.2.4是BYE处理且其后直接为6.3.3.3，未见所指子节；final-response标题实际是6.3.3.2.3.2。保留错引，不静默替换。
- 本页不把Warning123添加到session-identity重入成功或服务器主动邀请的响应中；也不据此跳过媒体授权。

依据：§9.2.1.4.2 step14h–r，印刷页 231、232。

## 证据边界



## 按需继续

- [rejoin-session](rejoin-session.md)
- [prearranged-call-admission](prearranged-call-admission.md)
- [prearranged-call-setup-result](prearranged-call-setup-result.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。
