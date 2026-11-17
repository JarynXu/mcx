# 已有组呼升级紧急：权限、组状态与告警反馈

TS24.379 V19.4.0，在网已建立的按需预安排MCPTT组呼，研究普通状态升级紧急及该请求的反馈；初始紧急起呼不在范围内。

不含chat、广播、ad hoc、预建立、离网、跨系统/网关或迫近危险主链。各角色按自己的事件与状态判断，不把本端授权、CF授权或告警成功设为所有声明的共同前提。

各段动作按原文SHALL执行；显示提示保留SHOULD，资源拒绝等可选动作保留MAY。

## 紧急升级和本人告警分别取得许可

客户端在已有按需预安排组呼中收到用户升级紧急的请求。此处构造分支限定本端 emergency state 原为clear、MEGC=1；未授权出口不以授权成功为共同前提。

组呼升级要求 allow-emergency-group-call=true，且（EmergencyCall/MCPTTGroupInitiation 的 entry-info=DedicatedGroup并包含目标组ID，或 entry-info=UseCurrentlySelectedGroup）。不满足时 SHOULD提示无权升级，SHALL停止。通过后调用§6.2.8.1.1：设置自身emergency state，置emergency-ind=true和MEGC=2；MEG原不为2时置MEG=4。用户未要求告警时置alert-ind=false；用户要求告警且另获授权时置alert-ind=true、MEA=2，并附§6.2.9.1规定的位置。客户端告警授权要求allow-activate-emergency-alert=true，且（EmergencyAlert的DedicatedGroup包含目标组，或UseCurrentlySelectedGroup且组allow-MCPTT-emergency-alert=true）。使用re-INVITE，携紧急级Resource-Priority及按需SDP offer；需要隐式话权请求才按§6.4指示，其下allow-location-info-when-talking=true时加入Report位置正文，然后发送。

请求了告警但未授权，不是helper中“未请求告警”的false分支；不自行补alert-ind=false。CF对字段组合仍有独立要求。

本端紧急状态已设置的另一个helper分支不在本条构造范围；MEG是本端对组状态的认识，MEGC是本端紧急组呼请求状态，MEA是本端告警状态，不能合成一个布尔值。

Resource-Priority取配置值而非固定数字；位置编码、完整SDP及隐式话权授予不在此展开。

来源：§10.1.1.2.1.3 steps1,3,5,7,8，印刷页272, 273；§6.2.8.1.1 emergency-state-clear branch, §6.2.8.1.2, §6.2.8.1.6 alert-initiation, §6.2.8.1.8 emergency branch，印刷页75, 76, 78, 79。

## 客户端通过后，PF与CF仍各自检查

PF收到该会话的re-INVITE；或CF收到会话身份标识该按需预安排组呼的re-INVITE。按各角色独立入口判断，不要求客户端授权结果能约束CF。

PF资源不足或拥塞风险时MAY以500拒绝并可携Retry-After；媒体参数不可接受或未提供MCPTT speech codec时返回488。继续时复制mcptt-info+xml、加入发起用户mcptt-calling-user-id，按来话offer形成SDP，复制存在的Resource-Priority后转送。CF亦可因资源/拥塞以500拒绝；紧急标记true不是免检承诺。CF要求emergency-ind=true时不含imminentperil-ind且必须含alert-ind，无效组合返回403+Warning150。CF升级授权要求用户allow-emergency-group-call=true、目标组allow-MCPTT-emergency-call=true，且（DedicatedGroup包含目标组，或UseCurrentlySelectedGroup）；失败以403及emergency-ind=false、alert-ind=false拒绝并停止。

客户端§6.2.8.1.8未列组allow-MCPTT-emergency-call检查，CF列有；不能把客户端通过当CF也通过。

PF传递Resource-Priority，CF判断其有效性；此处不是所有头字段与SIP拒绝情形清单。PF响应段回指step7而实际发送列step8，保留引用差异。

来源：§10.1.1.3.1.3 steps1-8, §6.3.2.1.9，印刷页115, 286, 287；§10.1.1.4.7 steps1-3, §6.3.3.1.13.2 group branch, §6.3.3.1.14, §6.3.3.1.17，印刷页137, 138, 141, 142, 304。

## CF改变组状态，参与者与未参与者接收不同通知

CF收到emergency-ind=true且升级已授权的re-INVITE，前序检查未拒绝；本条状态改变分支进一步要求组in-progress emergency state原为false。告警子分支还要求收到alert-ind=true且告警获CF授权。

CF缓存紧急呼叫发起用户ID；告警获准时另缓存告警发起用户ID。CF告警授权要求allow-activate-emergency-alert=true、组allow-MCPTT-emergency-alert=true，且（EmergencyAlert/DedicatedGroup包含目标组，或UseCurrentlySelectedGroup）。CF把组紧急状态设true、启动TNG2并调用其到期处理；向其他通话参与者发送§6.3.3.1.6的re-INVITE，向其他已归属但未参与通话的成员发送MESSAGE，后者携主叫ID、emergency-ind=true，仅告警子分支获准时带alert-ind=true。收到所发re-INVITE的200后调用媒体接口。

客户端告警DedicatedGroup分支没有另列组allow-MCPTT-emergency-alert，而CF有；这可导致升级获准但告警未获准。

组原已true且另一用户新报紧急时，step6(c)另向其他已归属成员发MESSAGE；它不是本条false→true转换，不据此重启TNG2或套全部参与者re-INVITE。

TNG2/TNG3切换已有独立主题；这里只保留真实调用。发送MESSAGE不证明该成员已加入或看到提示。缓存设置先于反馈，本段没有下游失败的完整回滚算法。

来源：§10.1.1.4.7 steps6(a,b,c,d)，印刷页305, 306；§6.3.3.1.13.1 group branch，印刷页136, 137。

## 收到升级更新不需要重新人工接听

CF已按普通→紧急分支调用§6.3.3.1.6，当前组紧急状态true；或参与客户端在已有按需组呼内收到正文emergency-ind=true的re-INVITE。每段分别以自己的事件适用。

CF下发re-INVITE采用与终接端当前已建立的媒体参数，带发起用户ID、紧急级Resource-Priority及emergency-ind=true。原请求alert-ind=true且CF告警授权通过时调用§6.3.3.1.12填告警及位置正文，否则下发alert-ind=false。参与客户端收到emergency-ind=true后 SHOULD显示紧急呼叫与发起者；若alert-ind=true，SHOULD另显示告警信息。客户端SHALL设MEG=2、MIG=1、MIGC=1，接受re-INVITE，发带规定Contact特征标记及按需SDP answer的200，再调用媒体接口。

接收端这条更新没有重新套初始Manual/Auto接听流程，也没有把其他成员的MEA设成自己的告警。

只证明收到更新的本端处理；完整T-PF转送及未参与成员MESSAGE接收算法未展开。此范围原无迫近危险，不把所列MIG清理扩成迫近危险升级主链。

来源：§6.3.3.1.6 steps1-3, §6.3.3.1.12，印刷页131, 132, 136；§10.1.1.2.1.6 steps1,5-12，印刷页276, 277。

## 升级200与告警成功是两项证据

分别处理CF收到所发re-INVITE的200，或PF收到下游2xx，或请求客户端收到本次升级2xx。INFO分支另须本次带Warning149的200已收到ACK；客户端INFO接收另有包名、正文和状态条件。

CF按响应段调用媒体接口、生成上游200及SDP，原请求alert-ind=true但CF告警授权未通过时加入Warning149；按列出的后续媒体调用后发送200。PF返回含下游Warning的200，先发送再调用媒体接口。请求客户端收到2xx先调用用户面；在MEGC=2或3时，设MEG=2、MEGC=3、MIGC=1、MIG=1；仅MEA=2且响应不含149时设MEA=3。CF收到对带149响应的ACK后发INFO：告警请求true但未授权的分支置emergency-ind=true、alert-ind=false。客户端在该priority-group对话中收到Info-Package=g.3gpp.mcptt-info、关联mcptt-info+xml且至少设置alert-ind/imminentperil-ind/emergency-ind之一的INFO时回200；MEGC=3且MEA=2时，alert-ind=false使MEA=1，true使MEA=3。

CF响应段没有全员re-INVITE或MESSAGE确认计数、聚合/去重规则，不把上游200说成全组同步完成。

带149的200仍更新紧急呼叫状态，但不能将等待中的告警当已成功。INFO不是任意包名或任意对话都能清MEA。

媒体面只到调用接口，不证明获话权、优先级承载已全部落实或语音送达；完整PF的INFO转送未展开。

来源：§10.1.1.4.7 response steps1-5,8-9 and ACK paragraph，印刷页307, 308；§10.1.1.3.1.3 2xx paragraph，印刷页287；§10.1.1.2.1.3 response/INFO paragraphs，印刷页273；§6.2.8.1.4 step1, §6.2.8.1.13 opening,steps1-2, §6.3.3.1.18 steps1-3(a)，印刷页77, 81, 142, 143。

## 升级失败不等于释放原组呼

请求客户端收到本次升级re-INVITE的4xx、5xx或6xx，且本端MEGC=2或3。若PF收到CF的403，其转发是独立事件。

PF收到403时生成403，复制存在的mcptt-info+xml和Warning后转发，并调用媒体接口。客户端将MEGC设1；只有MEG原为4时才设MEG=1。原请求含alert-ind=true时将MEA设1。这些动作没有列出清除自身整体emergency state，也没有列出对原组呼发送BYE。

不能把MEG原为2也清成1，不能借取消失败恢复规则或私呼规则补动作。

这不是所有SIP超时、无响应或服务器缓存回滚的算法；失败的本地状态处理不证明远端全局事务回滚。

来源：§10.1.1.3.1.3 403 paragraph，印刷页287；§10.1.1.2.1.3 error paragraph，印刷页273；§6.2.8.1.5 step1，印刷页78。

## 范围边界

这是已有会话升级的有限主链；不展开完整位置/SDP编码、配置文档验证、媒体/话权内部及全部失败恢复。

组紧急状态、用户自身emergency state、MEGC和MEA是不同对象；升级取消另见组取消主题，不以BYE代替状态更新。

来源：[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
