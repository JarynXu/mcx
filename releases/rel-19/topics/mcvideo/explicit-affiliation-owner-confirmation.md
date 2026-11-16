# 组所有者的归属准入、异步确认与续期边界

TS24.281 V19.3.0，第8章普通在网显式归属：MCVideo client维护本用户在本client的兴趣组集合，服务该用户的MCVideo server（下称serving/PF）转交拥有目标组的MCVideo server（下称owner/CF）。限定本地普通GMS组；不展开跨系统/gateway、NCF、重组、功能别名/规则触发、合法第三方强制或协商代改/代查、紧急告警及隐式归属。身份或字段不合格的请求仍保留本条明确失败处理。

显式增加、刷新与完整集合中删除/清空的必要分支分别描述；不把service authorization或profile触发的隐式归属当作本显式请求。用户/profile的规则未禁止这里的自主变更；规则触发归属后的手动退出限制另属8.2.1.2开头，不在本页展开。

每条claim独立继承本主题common_conditions及自己的conditions，不继承上一条成功。核读协议条件与状态更新，不声称完整IMS/RFC事务、GMS配置、安全保护、所有超时/恢复或互操作已实现。

## 所有者准入及200后的检查

适用条件：owner收到发往目标组CF PSI的PUBLISH，mcvideo-info含group request-uri及user calling-user-id，P-Asserted-Service为MCVideo ICSI，Event=presence，且有per-group affiliation PIDF。

owner先识别group/user。Expires缺失或非零且小于4294967295时423并带相同Min-Expires后停止；GMS中组不存在、或handled用户不是该组成员，任一成立即403并停止。通过后先回200并带selected expiration time；再检查presence entity须匹配group ID，tuple id须匹配handled用户，任一不符即停止后续状态更新。

- 不能把owner的200升级为PIDF已通过或记录已落地，也不能省略GMS成员资格。源文没有为这些403列Warning码，不移植呼叫的116/120。
- 请求入口仍错引8.2.3.2。selected expiration time的选择细节未在该顺序中给出；不从隐式过程移入local-policy期限。

依据：§8.2.2.3.3 steps1–8，印刷页 197、198。

## client列表和期限更新

适用条件：owner已通过8.2.2.3.3所有前置检查，含200后的entity与tuple身份检查，已定位存在的served组记录。

selected expiration time非零时，owner定位handled用户记录，缺失则插入；把client ID列表设为收到的affiliation client属性集合，并据selected expiration time设置该用户记录期限。随后识别PUBLISH的handled p-id并调用8.2.2.3.5。selected expiration time为0的分支要求移除组下相应用户记录，但该步原文使用served MCVideo ID而非前文handled MCVideo ID，本页保留身份名不一致。

- owner视图是group→user→client列表，期限在user记录；不照搬serving端user→client→group各自状态/期限。client列表是按收到集合设置，不是只追加本次client。
- 0分支的served/handled命名及删除后8.2.2.3.5再查该user记录的构造细节未解；不能据此宣称完整去归属通知/原子回滚已经闭合。此处没有直接调用通话BYE或媒体释放。

依据：§8.2.2.3.2;8.2.2.3.3 steps9–13，印刷页 197、198、199。

## 向所有者订阅结果

适用条件：serving server要确定本served用户在某handled组的owner侧是否归属成功，使用8.2.2.2.7；owner接收的订阅满足其8.2.2.3.4入口。

serving server向组CF PSI生成SUBSCRIBE，mcvideo-info放group ID和served用户calling-user-id，P-Asserted-Service为MCVideo ICSI，Accept含PIDF，simple-filter按该served用户限制；当前及未来通知用Expires=4294967295，仅当前用初始0，对话内0表示取消订阅。owner入口还要求presence Event及filter用户与calling-user-id一致；Expires缺失或非零小于4294967295时423/Min-Expires，组不存在或用户非成员时403，均停止；通过则生成200并在订阅期间通知变化。

- 本版不支持一次SUBSCRIBE订阅多个served用户的归属变化。此server订阅与client订阅是两层，不能把一个200当两层都成立。
- 原文没有在8.2.2.2.3每次转交PUBLISH时明确列必须先完成此订阅的调用顺序；这里以“需要发现owner结果”为独立入口，不补隐含触发器。
- owner的订阅期间通知段写served MCVideo ID并引用8.2.2.2.5；相邻owner通知专段是8.2.2.3.5。保留错引，不擅自裁决两个helper等价。

依据：§8.2.2.2.7 subscription portion;8.2.2.3.4，印刷页 186、187、199。

## 所有者NOTIFY内容

适用条件：owner需要按8.2.2.3.5向handled用户对应的订阅者通知served组的归属变化，所需组/用户记录可定位。

owner按其组下该用户记录构造per-group affiliation PIDF并发送NOTIFY；该过程要求affiliation中包含expires。若由8.2.2.3.3调用且已识别handled p-id，presence p-id设为该值。独立编码8.3.1.2说明per-group entity为group ID、tuple id为用户MCVideo ID、每个affiliation的client为client ID；per-group编码不靠status属性声明serving端的affiliating/affiliated状态。

- 通知过程原文引用9.3.1并有“served list of the served ...”措辞，未静默修成另一过程。expires在通用编码可选，但此通知过程明确要求包含，保留专门条件。
- 不是每条NOTIFY都有p-id；只有列明调用条件才要求带入。owner记录已移除时如何构造该用户空信息，正文未在此给完整细节。

依据：§8.2.2.3.5;8.3.1.2，印刷页 199、200、203。

## 正向确认与半寿命

适用条件：serving server收到符合引用SIP/RFC过程及8.3.1的per-group PIDF NOTIFY；对某served用户/client，正文含对应tuple id、affiliation client及expires；本地handled组条目存在、尚未过期、状态为affiliating，且位于该用户和client记录下。

serving server把该本地组条目改为affiliated，并把next publishing time设置为原文所述current time and half of the time between current time and expiration of affiliation，即剩余寿命中点。正向确认条件未要求p-id匹配。client自己的刷新入口是其收到affiliated状态通知后临近到期；server向owner临近已发布信息到期的刷新则可使用8.2.2.2.6。

- 该step1仅明确处理未过期affiliating条目，不把它扩成每次已affiliated的续期通知都重新设置next publishing time。正文也没有在此明确覆盖本地expiration time。
- 半寿命字段不等于client必须在半寿命重新PUBLISH；此处不补具体时钟算法、定时任务触发、丢通知重试或已经affiliated记录的续期更新步骤。
- profile隐式归属的调用和提交不经过这里的client显式p-id建立链，不混合两套时序。

依据：§8.2.2.2.7 NOTIFY step1;8.2.2.2.6 opening;8.2.1.2 opening，印刷页 174、184、187。

## 负向确认的状态和p-id条件

适用条件：serving server收到符合8.2.2.2.7入口的owner per-group NOTIFY；handled组的本地条目未过期，所属served用户/client可定位，但PIDF未含该用户/client的列明tuple-id/affiliation-client结构。

若本地状态为affiliated或deaffiliating，server将其改为deaffiliated并把expiration time设为current time。若本地仍为affiliating，另须NOTIFY存在p-id且该值匹配条目的affiliating p-id，才适用本段所列同样处理。缺失结构与p-id条件需同时保留，不能把所有未列出的pending条目一律判失败。

- 本条描述这两项条件分支，不声称它们是全规范唯一可终止pending的原因。原文未替无p-id/不匹配pending条目给出新的状态处理，不补超时或永久保留结论。
- client侧p-id与server新current p-id的保留差异可能影响这里的匹配，见serving-state主题；不自动修复为统一ID。该段未直接列一次额外的client NOTIFY调用，不能伪造其步骤号或即时完成保证。

依据：§8.2.2.2.7 NOTIFY steps2–3，印刷页 188。

## 证据边界

- owner记录成功、serving端affiliated与client已收到确认是不同观察点，不给跨角色原子性保证。明确未闭合的zero分支和刷新算法不得用其它服务默认填补。

## 按需继续

- [explicit-affiliation-request](explicit-affiliation-request.md)
- [explicit-affiliation-serving-state](explicit-affiliation-serving-state.md)
- [prearranged-call-admission](prearranged-call-admission.md)
- [server-late-entry](server-late-entry.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

## 原文差异与未闭合依赖

- 8.2.2.2.4 step1在SUBSCRIBE入口写PUBLISH；8.2.2.2.5和8.2.2.3.5通知编码写9.3.1；8.2.2.2.6及8.2.2.3.3 per-group构造写8.2.3.2。实际已核编码为8.3.1.2，原文引用不修正。
- 8.2.2.2.3部分位置写group element，其余是group attribute；状态混用de-affiliating/deaffiliating。8.3.1.2 schema列affiliating/affiliated/deaffiliating，不列内部deaffiliated。
- 8.2.2.3.3 zero分支用served MCVideo ID，而前文处理的是handled MCVideo ID；删除记录后的通知helper仍查该user记录。身份与空结果构造不自行补全。
- 8.2.2.3.4订阅期间段用served MCVideo ID并指8.2.2.2.5，而owner通知专段是8.2.2.3.5。
- client PUBLISH处理设置affiliating p-id；向owner发送又生成current p-id且只填原未设置的条目；negative owner NOTIFY则要求匹配。保留两层来源与未解关联，不从隐式流程移入修复。
- owner selected expiration time选择细节、已affiliated记录续期NOTIFY更新next publishing time、本地expiration同步以及完整重试调度，未在所核步骤闭合。
