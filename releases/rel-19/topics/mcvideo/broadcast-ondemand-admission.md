# MCVideo在网广播发起：指示字段、服务准入与邀请范围

TS24.281 V19.3.0 与媒体TS24.581 V19.2.0分别标版。普通在网、有transmission control、以broadcast发起的新组呼；普通GMS组，client–O-PF–CF–T-PF–client。不是chat、system、ad hoc、NCF/gateway、临时/预配置重组、功能别名、远程/ambient、预建立、重入、广播升级或离网。

请求broadcast-ind=true，但不含emergency-ind、imminentperil-ind、alert-ind、user-requested-priority或优先Resource-Priority；客户端既有emergency/group-priority/call-priority状态均未置位，CF组emergency和imminent-peril状态为false。广播不被当成紧急呼叫，亦不由本次未点紧急按钮推定全部既有状态为普通。

每条claim只继承本主题common_conditions及自身conditions，不继承前条成功。本版9.2.1.2.1.1 step3明确调用6.2.8.2，才构成这里使用prearranged signalling入口的依据；不因名字类似就继承既有普通非广播页面的全部结论。

建立范围限CF确认会话不ongoing（不是已分配identity且active），无affiliated且on-network-required的成员，TNG1不运行；至少有可邀请的普通affiliated成员。终接小链限定T-PF已存auto-answer、目标完全没有预建立会话、无入站Answer-Mode/Priv-Answer-Mode、客户端允许自动接听。提前200 claim另以CF支持media buffering且当时尚未向主叫发最终响应为条件，不把该时点前提继承到后续响应处理claim。其他模式/required/无缓冲分支不补完整实现。

## 广播指示与会话类型

适用条件：用户通过在网on-demand入口请求发起broadcast group call，使用普通MCVideo group ID。

客户端9.2.1.2.1.1 step3明确调用6.2.8.2，在mcvideo-info加入broadcast-ind=true；session-type仍为prearranged，不新造broadcast session-type。若preconfigured-group-use-only存在且true，SHOULD提示不能呼叫并SHALL停止。否则initial INVITE的Request-URI为serving PF PSI，XML含组ID和client ID，主叫MCVideo ID由O-PF加入；带MCVideo/ICSI标签和6.2.1 SDP offer。F.1规定broadcast-ind=false或缺失表示非广播，不是广播请求成功的替代证据。

- 客户端Supported timer与Session-Expires在该段为SHOULD；refresher建议省略，若有则uac。完整SDP编码、MIME保护和客户端授权配置取得未在此重写。
- 6.2.8.2位于Priority call conditions标题下，但本段只是广播指示生成，不能因此附加紧急/迫近危险授权或优先例外。离网9.4完全不在此链。

依据：§9.2.1.2.1.1;6.2.8.2;F.1，印刷页 76、77、208、209、580、584。

## PF准入与路由

适用条件：O-PF收到上述session-type=prearranged的broadcast INVITE；本页无associated-group-id，目标不是重组。

O-PF可因资源不足/拥塞风险500并可带Retry-After；按PAI public-user-identity确定并授权主叫MCVideo ID。本地策略不准发起prearranged组呼则403/109，未提供MCVideo codecs则488，MaxSimultaneousCallsN6已exceeded则486/103。通过后确定CF PSI并路由，加入calling-user-id，复制mcvideo-info（故保留broadcast指示）；明确不转带入站Answer-Mode和Priv-Answer-Mode。信令服务准入与广播发送者/接收者媒体角色不是同一检查。

- PAI绑定来自7.3服务授权；本页不编造额外broadcast专用授权字段或把它替代本地策略。N6正文exceeded与Warning文本reached保留差异。
- 普通广播不满足本段priority授权的implicit affiliation入口，不能搬chat普通隐式归属。CF PSI发现方法在范围外；Request-URI段所指step8错号保留。

依据：§9.2.1.3.1.1 steps1–7 and no-associated-group-id branch;6.3.2.1.3，印刷页 90、217、218、219。

## CF服务及组文档检查

适用条件：CF收到目标普通GMS组的broadcast/prearranged INVITE，进入9.2.1.4.2，尚未通过初步检查。

CF资源/拥塞可500；媒体参数或MCVideo codecs不接受则488；Accept-Contact缺MCVideo标签或相应ICSI任一则403并停止。按6.3.5.2取得组文档并检查：订阅404→404/113，其余最终4xx/5xx/6xx转对应响应加114；disabled元素存在→403/115，名单无主叫→403/116，invite-members=false而session-type为prearranged→404/118。主条还在preconfigured-group-use-only=true时403/167。broadcast指示没有豁免这些条件。

- 这里只取普通未重组组；组文档后续更新/订阅缓存完整生命周期未闭合。disabled的判断是present，不改成true。
- 若使用已重组身份，另有403/148等分支，本页不处理；不能把broadcast写成直接调用chat的group-document顺序。

依据：§9.2.1.4.2 steps1–7;6.3.5.2，印刷页 135、136、137、226、227。

## 归属与发起许可

适用条件：CF已通过普通组文档和媒体检查，缓存受支持Contact tags并把邀请成功计数置0；本目标session并非identity已分配且active。请求无优先指示、不是constituent/TGI路径。

在13a普通非constituent、无优先指示且主叫未affiliated的交集中，CF返回403/120并停止；不把原复杂枚举扩成所有情况一个布尔式。另按6.3.5.4检查发起权限：普通组名单包含主叫，存在is-list-member或匹配identity的allow-initiate-conference=true规则，并且supported-services含MCVideo ICSI及MCVideo video media；不授权则403/119。affiliation判断还要求匹配group/user/client记录且用户记录未到期，名单成员资格不等于affiliation或可发起权限。

- 13a的i–iv连接方式有复杂优先分支，本页只取明示条件的安全交集，不修成全局AND/OR算法。
- 发起权限不是ongoing加入的join-handling规则；也不意味着接收者获得媒体发送资格。其它机构/服务策略与安全校验依赖未穷尽。

依据：§9.2.1.4.2 steps7–13b;6.3.3.2.2;6.3.5.4;6.3.6，印刷页 123、138、139、140、227、228、229。

## 邀请对象与逐段寻址

适用条件：CF的新组呼准入成功；普通MCVideo group ID、无required成员，不是NCF或重组。

CF建立session并分配identity，处理TNG3；按6.3.5.5只选affiliated成员，超过on-network-max-participant-count时限量邀请。对每名目标调用9.2.1.4.1.1：SIP Request-URI为T-PF PSI、PAI为CF PSI，XML request-uri为被叫用户ID、calling-group-id为组ID，并按收到offer生成SDP；公共INVITE helper复制mcvideo-info，保留broadcast指示。CF随后与媒体平面交互。

- 广播不是向所有静态组名单成员无条件分发；目标仍须affiliated，超过容量的选择策略未在本页补算法。required场景另有优先邀请和TNG1，不在本页小链。
- 若存在该组GKTP document且含MKFC-GKTPs，CF须逐项重生成，仅成功项装入邀请；T-PF收到该元素调用6.3.2.3.2。算法/失败闭合另留依赖，不能以INVITE已发证明密钥可用。
- TNG3采用公共6.3.3.5；不在本页重写释放链或给具体最大时长。

依据：§9.2.1.4.2 step13e/13g;6.3.5.5;9.2.1.4.1.1;6.3.3.1.2，印刷页 103、104、139、223、224、229。

## 证据边界

- 未核23.281业务语义或24.484全部广播专用配置，不从不存在的查找命中断言“没有其它授权”。
- 无required/TNG1未运行、自动接听、支持缓冲且未发final是本成功小链边界；手动、required聚合、无缓冲最终成功和全部失败/超时恢复未闭合。
- originating广播step5与同时implicit的step4均保留；初始媒体SSRC、服务器全部初态与客户端状态的端到端映射尚未闭合。
- 广播升级、恢复/晚入、停止广播及全组释放未展开；不能把普通非广播的permission/terminated结论直接类推。
- GKTP/MIKEY算法、安全验证、媒体端口/完整SDP、GMS配置schema、跨系统与跨版本互操作仍是外部依赖。

## 按需继续

- [broadcast-auto-setup-result](broadcast-auto-setup-result.md)
- [broadcast-media-roles](broadcast-media-roles.md)
- [prearranged-call-admission](prearranged-call-admission.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；按条目单独标示媒体来源。
