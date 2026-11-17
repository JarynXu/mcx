# 已有按需预安排组会话：CF紧急升级、取消与分层反馈

## 共同适用条件
- 固定TS24.379 V16.14.0，在网已有按需预安排组会话，直接组身份，由其controlling MCPTT function处理re-INVITE。排除初始建立、chat/预建立、临时/重组、广播/system、离网、跨系统及完整媒体/话权算法。
- 聚焦emergency-ind升级或取消；不发起新的emergency alert，已有告警取消和拒绝反馈按各自条件保留。imminent字段只用于验证/原文分支比较，不展开其业务；无效请求仍能进入对应拒绝检查。
- 每条按实际角色、请求/响应/ACK事件及旧组状态分别适用；不以已获授权、组状态false、已取消成功或所有下游已响应为共同前提。CF组状态与客户端MEG/MEGC/MES/MEA不可互换。

## 已有会话先验证字段组合，再按用户与组配置判断升级权限

适用条件：CF收到以MCPTT session identity识别已有按需预安排组会话的re-INVITE；各拒绝检查和相应权限分支分别适用，不预设请求有效或已获授权。

资源不足或有拥塞风险时CF MAY用500拒绝，MAY带Retry-After并跳过后续步骤；紧急请求可被选择接受。含emergency-ind或imminentperil-ind时须调用字段验证：emergency=true要求alert存在且imminent不存在，emergency=false允许alert存在或缺失但imminent须不存在；无效组合须403/150。升级权限要求调用用户allow-emergency-group-call=true，且（DedicatedGroup配置匹配目标组并且目标组allow-MCPTT-emergency-call=true，或UseCurrentlySelectedGroup并且目标组allow-MCPTT-emergency-call=true）。其余升级请求未授权，须403携emergency=false及alert=false并停止。若Resource-Priority为紧急值、请求未含emergency且组当前紧急状态false，也须403并停止。

规范强度：资源/拥塞拒绝及Retry-After为MAY；字段验证、授权判定和所列403分支为SHALL。

- §6.3.3.1.17的无效组合段写发送403，未另写统一skip-rest；不能把其他拒绝分支的停止措辞补到该段。
- 入口为已有会话的re-INVITE，不借初始INVITE的PSI分类、成员准入或客户端已授权证明CF再次授权；组业务形态为预安排不等于其当前紧急状态必须false。
- §6.6收取保护处理先于业务过程，发送保护及多MIME/SDP首体义务仍适用；本页不实现XML验证、配置获取、密钥或完整SIP事务。字段不存在与false按各条款区别处理。

依据：TS24.379 V16.14.0 §10.1.1.4.7 opening, steps1–5；§6.3.3.1.13.2;6.3.3.1.14;6.3.3.1.17；§6.3.1.1 (initial INVITE classification comparison)；§6.5;6.6.1.1–4；§F.1.3 relevant identities/boolean fields，正文页 78,112,113,116,117,118,137,138,139,253,254,547,548,549。

## 已紧急与首次升级使用不同分发及计时分支

适用条件：请求emergency=true且CF按§6.3.3.1.13.2判为授权；本文不发起新告警，alert=false。另一个事件是所发下行re-INVITE收到200，其媒体动作只在该事件发生时适用。

CF缓存发起紧急呼叫的MCPTT ID。组已紧急时，按caller为其他已归属成员生成并发送emergency=true的MESSAGE；若组迫近危险状态true则清为false。组原非紧急时，置紧急状态true，启动TNG2，按§6.3.3.1.6向其他参与者生成并发送re-INVITE；收到对应200才调用媒体接口。该helper采用当前与终接客户端建立的媒体参数、发起者ID及紧急Resource-Priority，携emergency=true；本页无新告警时携alert=false。若TNG3正在运行且发生升级，停止TNG3，TNG2取服务配置group-time-limit；启动TNG2时不启动TNG3。

规范强度：所列缓存、分支状态、构造发送及定时动作为SHALL；媒体调用为收到对应响应后的SHALL。

- §10.1.1.4.7 step6(iii)写each other affiliated member，而被调用§6.3.3.1.11描述affiliated but not participating，不能擅自统一收件集合。helper以目标用户的终接PF为Request-URI，体内分别标目标用户和业务组，身份与路由不是同一个字段。
- 已true分支未重列启动TNG2，不能把false→true分支的重启条件加给所有重复升级。B.2.1-1的概括性启动行不能抹掉程序分支。TNG2实例关联单组的紧急状态，不是全系统唯一计时器。
- §6.3.3.1.6按紧急状态选择Resource-Priority，namespace/priority取§6.3.3.1.19服务配置，不硬编码。升级若含mc_implicit_request仅被识别为隐式话权请求，不证明话权获准或RTP送达。
- CF管理组in-progress emergency状态；MEG是客户端对该状态的视图，MEGC为客户端本人请求状态。Annex G为informative，不据其表格造CF状态变量或全设备原子同步。

依据：TS24.379 V16.14.0 §10.1.1.4.7 step6；§6.3.3.1.6;6.3.3.1.11；§6.3.3.1.13.1 (excluded new-alert comparison)；§6.3.3.1.19;6.3.3.5.2；§B.2.1 Table B.2.1-1 TNG2/TNG3；§6.4 re-INVITE implicit-request branch；§G.3–4 (informative perspective text)，正文页 107,108,110,111,112,118,119,125,137,254,533,585,586。

## 取消失败与取消组状态、告警缓存是不同分支

适用条件：收到emergency=false的re-INVITE；未授权拒绝分支与条文所写授权且组当前紧急的正向分支为替代分支。正向授权回指存在下述缺口，不能假定其已得到修复；收到下行200是另一个独立事件。

§6.3.3.1.13.4将allow-cancel-group-emergency=true/false分别判为授权/未授权。未授权时CF须403携emergency=true；仅请求alert=false且该用户有未结告警时另携alert=true，发送后停止。正向step8在其所写授权判断且组状态true时要求清组紧急状态、清该用户未结紧急组呼缓存。仅请求alert=false、告警取消权限成立且该用户有未结告警时，按originated-by存在则指定目标、缺失则请求发送者清告警缓存。向其他参与者发送§6.3.3.1.6 re-INVITE，收到对应200才调用媒体；停止TNG2；向已归属但未参与成员发送emergency=false的MESSAGE，仅已满足上述告警取消条件才另携alert=false。TNG2运行中取消时，§6.3.3.5.2还要求停止TNG2并按组on-network-maximum-duration启动TNG3。

规范强度：授权true/false判定、拒绝、满足各自条件的缓存/状态/分发/计时动作为SHALL；正向分支保留原文授权回指，不把缺口改写成实现保证。

- §10.1.1.4.7 step8正向授权回指§6.3.3.1.16，但.16实际是TNG2到期处理；负向step7才引用.13.4。不能静默更正、据此宣称取消授权到成功的完整可执行链已闭合。
- 组取消和告警取消helper分别只列true/false，没有定义缺配置元素的结果；同页private分支写false or not present，不可移植到组。告警取消权限与组取消权限不合并。
- §6.3.3.1.6 step4(b)(ii)的告警取消权限回指.15，实际.15为imminent-peril re-INVITE生成，不是.13.3。helper仍写满足其条件才携alert=false，存在originated-by时复制；不能删掉该差异以保证所有接收端清告警。
- TNG2到期的.16是另一个事件：降低组状态并通知；不证明等同用户取消的缓存清理。TNG3到期才调用会话释放，本页不展开其BYE链。取消紧急状态不等于结束会话、清所有用户MES或清所有告警。

依据：TS24.379 V16.14.0 §10.1.1.4.7 steps7–8；§6.3.3.1.13.3–4；§6.3.3.1.6;6.3.3.1.11；§6.3.3.1.15–16 (cross-reference/expiry comparison)；§6.3.3.5.1–2;B.2.1 Table B.2.1-1；§F.1.3 originated-by，正文页 107,108,110,113,116,117,124,125,254,255,533,549。

## 200、149和ACK后的INFO不能合并为业务全部完成

适用条件：分别观察：p256明确的收到下行re-INVITE之200事件；发往邀请客户端的200携149后收到其ACK事件；或发出的MESSAGE收到2xx事件。三者互不作为全局AND前提。

p256先以收到re-INVITE之200为事件要求调用媒体，随后列生成并向MCPTT客户端发送200、按§6.3.3.2.1生成SDP应答、Supported包含norefersub和tdialog等步骤。SDP对被接受媒体及控制通道使用CF的IP/端口，控制通道fmtp交给媒体规范接口。若请求alert=false但告警取消未授权，200须带149 SIP INFO request pending。只有该200携149且收到客户端ACK，才调用§6.3.3.1.18，在原dialog发送Info-Package=g.3gpp.mcptt-info的INFO；未授权告警取消分支携alert=true。对发出MESSAGE的2xx则按SIP规范处理。

规范强度：满足各自事件与字段条件时，200构造/发送、149、ACK后INFO及相关媒体调用均为SHALL；不把这些事件写成必然发生。

- p256的Upon receiving a SIP200是独立正文行，不能改成收到原请求即无条件生成200，也不能推导等待全部下游200的算法。组已紧急而仅发MESSAGE等路径与该200段怎样衔接，所读段未完整说明，本页不补时序。
- 同一200段还列alert=true未授权发起告警的149分支及imminent请求比较分支；本页不发起新告警或imminent业务，不把它们当本页共同前提。§6.3.3.1.18对应分支也不能互相套用。
- 媒体规范与完整SIP/RFC接口未展开；200/ACK/INFO、通知2xx均不等于全部成员状态同步、告警已取消、获话权或媒体交付。客户端状态按其自身接收事件处理，不能用客户端common为CF成功背书。

依据：TS24.379 V16.14.0 §10.1.1.4.7 p256 response/ACK/MESSAGE branches；§6.3.3.2.1；§6.3.3.1.18;6.3.3.1.13.1/.13.3 (149 branches)；§F.1.3;6.5;6.6.1.1–4，正文页 111,112,113,118,119,120,137,138,139,256,547,548,549。

## 范围与相关主题
- 这是CF局部职责与真实接口边界，不是完整全组紧急生命周期；配置、身份建立、SIP事务、告警服务及媒体实现各有外部依赖。
- 正向取消授权错回指、通知收件范围和响应事件衔接差异均保留，不据有效输入假定这些缺口已经解决。

- [客户端紧急请求与状态](emergency-group-client.md)：按客户端事件读取，不证明CF授权。
- [普通预安排组初始服务器准入](prearranged-server-admission-routing.md)：仅比较初始入口，不能解除其普通组共同条件。
