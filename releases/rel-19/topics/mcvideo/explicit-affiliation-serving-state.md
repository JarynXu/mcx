# 服务用户侧显式归属：候选集合、N2和逐组转交

TS24.281 V19.3.0，第8章普通在网显式归属：MCVideo client维护本用户在本client的兴趣组集合，服务该用户的MCVideo server（下称serving/PF）转交拥有目标组的MCVideo server（下称owner/CF）。限定本地普通GMS组；不展开跨系统/gateway、NCF、重组、功能别名/规则触发、合法第三方强制或协商代改/代查、紧急告警及隐式归属。身份或字段不合格的请求仍保留本条明确失败处理。

显式增加、刷新与完整集合中删除/清空的必要分支分别描述；不把service authorization或profile触发的隐式归属当作本显式请求。用户/profile的规则未禁止这里的自主变更；规则触发归属后的手动退出限制另属8.2.1.2开头，不在本页展开。

每条claim独立继承本主题common_conditions及自己的conditions，不继承上一条成功。核读协议条件与状态更新，不声称完整IMS/RFC事务、GMS配置、安全保护、所有超时/恢复或互操作已实现。

## PUBLISH检查与200的边界

适用条件：serving server收到发往其O-PF或T-PF PSI的PUBLISH；mcvideo-info指向其服务的用户，P-Asserted-Service为MCVideo ICSI，Event=presence，且有8.3.1 per-user affiliation PIDF。

先识别served用户及originator（O-PF从PAI绑定的public user identity，T-PF从calling-user-id）。不同用户且无权修改时403并停止。Expires缺失或非零且小于4294967295时423，Min-Expires=4294967295，并停止；非零时依RFC3903确定candidate expiration interval，零时设0。随后先回200并带candidate expiration time；再检查PIDF presence entity，不等于served用户ID即停止余下处理。只有继续下来的请求才按tuple id定位本client并处理其组集合。

- 不把entity检查提前，也不补第二个SIP错误响应；200不是组所有者接受证据。原文interval/time措辞保留，不另推绝对时间编码。
- 此入口没有第7章那条明确的绑定过期404/141分支，不把私呼或MCData错误码移入。serving用户/client存储记录缺失后的初始化或恢复未在这些步骤完整定义。

依据：§8.2.2.2.3 steps1–13，印刷页 180、181。

## 候选集合的增删和到期

适用条件：serving server已通过8.2.2.2.3的身份/Expires/entity检查，已定位served用户/client，并复制原组记录为served list；candidate interval已确定。

interval非零时：原未过期且仍在请求集合的组复制到candidate并延长到current time+interval；若原状态deaffiliating/deaffiliated，则改affiliating并存client PUBLISH的p-id。原未过期但从请求集合省略的组也先复制；其状态若affiliated/affiliating，则改为原文de-affiliating且期限设current time+2×timer F。请求中新增或原记录已过期的组新建为affiliating，期限为current time+interval，并存该p-id。interval=0时，原served list的各组均复制为de-affiliating、期限current time+2×timer F。

- 仍在集合且原状态affiliating/affiliated的记录，不由此步骤重新覆盖已有affiliating p-id。省略且原为其他状态的未过期记录只按复制规则保留，不补状态跃迁。
- 原文混用de-affiliating与deaffiliating；schema列后者而内部状态还使用deaffiliated，本页不悄悄统一词法。2×F不是立即删除或全部通话终止；F数值及RFC事务未另核。

依据：§8.2.2.2.3 steps14a and15，印刷页 181、182。

## 跨client去重的N2计数

适用条件：serving server处理非零candidate interval，已构造当前client的candidate list并保有同用户其他client记录，进入8.2.2.2.3 step14b/c。

candidate数量按不同group ID计数：当前client的candidate list与同一served用户其他client的组列表取并集，只纳入affiliating或affiliated且未过期的条目。数量大于该用户profile Common/MaxAffiliationsN2时，按服务商策略将candidate group IDs缩减至N2；源文举顺序、重要性/优先级等策略例子，但不固定算法。

- 不是每client独立N2，也不是重复组在多client重复计数。不把本流程改成486/102拒绝，200已在此前发出。
- N2缺省、配置获取/校验、怎样把选择落实到不同client记录的完整策略未由本段给出；不擅自删除另一client的实际存储记录。

依据：§8.2.2.2.3 step14b/c，印刷页 182。

## 候选提交与逐组转交

适用条件：8.2.2.2.3此前身份/entity及candidate构造、必要N2缩减已完成；server同时持有更新前served list与最终candidate list。

server先以candidate list替换该client存储组列表，再对以下组调用8.2.2.2.6：原无记录而candidate=affiliating；原记录已过期而candidate=affiliating；原未过期deaffiliating/deaffiliated而candidate=affiliating；或原未过期affiliated而candidate=de-affiliating。随后识别本client PUBLISH的handled p-id并调用8.2.2.2.5通知该served用户。普通范围无outstanding emergency alert，不进入本条step20告警调用。

- 调用转交helper在本地状态通知helper之前，但这里没有规定等待owner确认后才通知；通知可以反映本地待完成状态。
- 不是每个PUBLISH都无条件向owner重发所有组。尤其原affiliating变de-affiliating未列在此step17的第四项；不靠对称性补入。owner临近到期的刷新另有8.2.2.2.6入口。

依据：§8.2.2.2.3 steps16–20，印刷页 182、183。

## 组所有者请求及两层关联标识

适用条件：serving server要向owner发送本用户对某组的归属、去归属或临近到期刷新；需要的用户/client/group记录已存在或由前序过程建立。

生成新的PUBLISH：Request-URI为该组CF PSI；mcvideo-info分别放目标group ID和served用户calling-user-id；P-Asserted-Service为MCVideo ICSI，PAI为发送server的PSI。归属请求Expires=4294967295，去归属=0。生成全局唯一current p-id；对同用户该组未过期、状态affiliating且尚无affiliating p-id的记录赋此值。per-group PIDF列出该用户对此组处于affiliating/affiliated且未过期的全部served client IDs，presence p-id设current p-id，不带affiliation expires，然后发送。

- 此版本不支持用一个这样的PUBLISH同时携带多个served用户的状态变化。CF PSI发现算法不在规范范围内；本页排跨系统路由。
- client PUBLISH处理已给一些条目设置原client p-id；此处只补未设置者，而对owner的presence又用新current p-id。原文未在这步覆盖全部已有值，不能把两层关联ID静默统一；这会限制后续negative NOTIFY的关联判断。
- per-group PIDF在此引用8.2.3.2，实际已核编码段为8.3.1.2；保留错误引用而不把它写成原文已更正。

依据：§8.2.2.2.6，印刷页 184、185、186。

## 所有者请求失败的清理范围

适用条件：serving server已向owner发送本served用户对handled组的(de)affiliation PUBLISH；该事务timer F到期，或收到3xx/4xx/5xx/6xx响应。

serving server删除该served用户全部client记录中group ID等于handled group ID的组条目。删除条件没有再按本次client、原状态、是否过期或p-id限制，因此不能缩写为只清理发起client的一条pending记录。

- 这是serving端的本用户组记录清理，不等于删除GMS组、成员资格或所有通话；也不推导owner已经撤销。
- 该失败段只列删除，没有显式列再调用状态通知helper、自动重试或回滚其它系统；既有订阅的变化通知承诺仍在8.2.2.2.4，但不虚构具体额外同步步骤。

依据：§8.2.2.2.6 response handling，印刷页 186。

## 证据边界

- 状态表只提炼本集合处理的必要规则，不实现完整RFC publication合并、事务重试或规则驱动退出。

## 按需继续

- [explicit-affiliation-request](explicit-affiliation-request.md)
- [explicit-affiliation-owner-confirmation](explicit-affiliation-owner-confirmation.md)
- [chat-ondemand-admission](chat-ondemand-admission.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

## 原文差异与未闭合依赖

- 8.2.2.2.4 step1在SUBSCRIBE入口写PUBLISH；8.2.2.2.5和8.2.2.3.5通知编码写9.3.1；8.2.2.2.6及8.2.2.3.3 per-group构造写8.2.3.2。实际已核编码为8.3.1.2，原文引用不修正。
- 8.2.2.2.3部分位置写group element，其余是group attribute；状态混用de-affiliating/deaffiliating。8.3.1.2 schema列affiliating/affiliated/deaffiliating，不列内部deaffiliated。
- 8.2.2.3.3 zero分支用served MCVideo ID，而前文处理的是handled MCVideo ID；删除记录后的通知helper仍查该user记录。身份与空结果构造不自行补全。
- 8.2.2.3.4订阅期间段用served MCVideo ID并指8.2.2.2.5，而owner通知专段是8.2.2.3.5。
- client PUBLISH处理设置affiliating p-id；向owner发送又生成current p-id且只填原未设置的条目；negative owner NOTIFY则要求匹配。保留两层来源与未解关联，不从隐式流程移入修复。
- owner selected expiration time选择细节、已affiliated记录续期NOTIFY更新next publishing time、本地expiration同步以及完整重试调度，未在所核步骤闭合。
