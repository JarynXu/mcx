# Ad hoc组SDS session：显式用户列表如何成为一次组通信

同版§24为ad hoc组提供独立建立过程。这里选普通on-demand SDS session和显式用户列表：客户端提交目标，PF核身份与权限，CF检查列表并创建组，成功响应仍按目标与事务分别判断。

## 共同条件

- TS24.282 V19.7.0 Rel19 Stage3，普通在网on-demand ad hoc SDS session初建，用户直接指定MCData ID收件人列表；不是配置组或单用户调用的扩大。
- 不含standalone、FD、预建立、criteria持续动态确定/修改、功能别名、已知ad hoc身份复用、告警后续、紧急/迫近危险、迁移/跨域或请求端到端安全的分支。
- 角色动作只适用于实际进入相应入口、收到对应消息且前序门槛未拒绝时；身份、安全、配置和SIP/媒体依赖仍须满足。

## 客户端提交用户列表，不冒用已配置组

普通用户要求新建on-demand ad hoc SDS session，并明确给出直接MCData ID列表；不沿用告警组，不携带criteria或已知ad hoc组ID。

客户端检查服务配置on-network/anyExt/adhoc-group-data-comn中的allow-adhoc-group-data-comn-support；缺失或false时SHOULD提示不允许，并SHALL停止。继续时向服务PF的PSI发初始INVITE，使用SDS服务标签、P-Preferred-Service及request-type=adhoc-group-sds-session，mcdata-client-id为发起客户端ID，SDP调用§9.2.4.2.1。用户要求显式列表且非告警后续时，在resource-lists中放被邀请用户ID。NOTE9说明列表与criteria是选择关系，CF另有两者同时存在的拒绝条件。这里无需把一个预配置组ID当成收件人列表。

- 该入口也涉及standalone和FD，本文只取SDS session分支；不会仅因相同request-type将它们合为一种业务。
- Supported timer与Session-Expires为SHOULD；不是所有列出的头都无条件SHALL。
- 配置schema、列表编码/RFC及SDP内部实现仅保留接口，不提供完整报文模板。

依据：§24.2.2.1.1 opening,steps1–5,7–9，印刷页523,524,525,526。列明正文义务按SHALL；SHOULD/MAY及NOTE另行说明，不提升强度。

## PF建立主叫身份并独立检查权限

O-PF实际进入§24.3.2.1.1处理本页初始INVITE；逐项拒绝按各自条件执行，只有未被拒绝的路径继续。

PF可因资源或拥塞回500，可带Retry-After；从PAI的public user identity确定主叫MCData ID，无绑定或绑定过期回404/141并停止。按本地策略未获ad hoc发起权限时回403/237；profile中的allow-adhoc-group-data-comn缺失或false则回403/238并停止。CF无法确定时回404/142并停止。继续时生成面向所确定CF的INVITE，复制mcdata-info并写由绑定确定的mcdata-calling-user-id，PAI为PF自身PSI，SDS P-Asserted-Service及SDP分别按本节和§9.2.4.3.1处理。

- step5在INVITE过程内把所检查请求字面写成SIP MESSAGE；列表分支字面选择服务主叫ID的CF。此差异未协调，不把它修成已经验证的自动路由实现。
- PF profile字段路径和CF的rule/actions路径不同，保留各caller文字，不自行补schema或默认许可。
- 本页未闭合PF对resource-lists的完整复制/转交编码，CF动作以前提“实际收到列表”为准，不把发送者准备好列表当成CF已经收到。

依据：§24.3.2.1.1 steps1–7,8–13,15–17,19，印刷页538,539,540。列明正文义务按SHALL；SHOULD/MAY及NOTE另行说明，不提升强度。

## CF检查列表，建立ad hoc组并邀请参与者

CF实际收到本页SDS session INVITE及显式直接用户ID列表；不带criteria、告警继承或端到端安全请求，且不命中已有criteria会话复用分支。各前置门槛未拒绝才继续到建组和邀请。

CF可因资源/拥塞回500；媒体参数不接受或缺MSRP URI回488；缺本业务SDS Accept-Contact标签回403。CF检查发起者profile授权字段为false时回403/238，系统ad hoc支持字段缺失或false回403/239。邀请人数超配置max-no-participants时回403/242；列表与criteria同时存在回403/240，均停止相应后续。继续时缓存支持的Contact标签、启动会话计时器、将目标200计数置0；未带或不接受所给ad hoc身份，且告警组指示false或缺失时，创建ad hoc组并生成关联组ID。CF把列表中每个用户entry作为邀请对象，按§24.4.2.1.1邀请，并把所有被邀请成员视为隐式affiliated。出站mcdata-request-uri是被叫用户ID，mcdata-calling-group-id是新ad hoc组ID，mcdata-calling-user-id是主叫ID，Contact另携带MCData业务session identity，Request-URI指向服务被叫的PF；这些身份不能互换。

- CF授权字段false与系统支持字段缺失/false不是同一个守卫；不补CF未明列的授权字段缺失处理。
- 隐式affiliation发生于邀请阶段，不等于每人已接听、收到数据或被写入永久预配置组。
- 列表人数计数、重复ID去重等实现不借功能别名分支规则补齐；配置数值与身份生成算法未核。
- 端到端安全会另选择预配置组的安全材料，不在本页范围，不能把新ad hoc组ID等同安全材料组ID。

依据：§24.4.2.2 opening,steps1,3–4,6–13,15a,16–18;24.4.2.1.1 steps4,6–8，印刷页557,558,560,561,562。列明正文义务按SHALL；SHOULD/MAY及NOTE另行说明，不提升强度。

## 匹配目标200、会议通知与业务交付分开

分别判断独立事件，不要求同时：CF收到其被邀目标200；CF在目标ID匹配对应邀请且尚未向主叫发送最终响应时处理成功；O-PF收到业务INVITE2xx；主叫客户端实际收到INVITE2xx。本页排除Warning232稍后投递结果。

CF收到被邀目标200时调用SDS session媒体接口、计数加1，并向已订阅conference事件的参与者发NOTIFY。NOTE7明确该通知可能早于回主叫200，不表示会话必定建立成功。CF成功响应入口要求目标MCData ID匹配对应邀请且主叫最终响应尚未发送，不要求先等全部目标200；它调用§6.3.7.1.23生成SDS session响应并带ad hoc组ID，发送后对订阅者通报主叫加入。O-PF收到2xx后生成200及SDS session SDP answer，复制收到的Warning和存在的mcdata-info，包含映射到入站Contact业务ID的session identity，发回客户端并调用媒体接口。客户端实际收到2xx后发送ACK、启动会话计时器，可显示收到的ad hoc组ID，随后按本条所写24.582接口交互，再可订阅conference。局部200或NOTIFY都不证明所有被邀者已接通，更不证明单条SDS送达或已读。

- CF成功入口把所响应INVITE回指24.4.2.2，而实际发送在24.4.2.1.1，保留回指差异；不宣称完整调度验证。
- 客户端本节媒体调用字面为24.582 §6.1.1.2，CF/PF的SDS session调用则分别为§6.3.2/§6.2.2.4；本页不改号，也不证明媒体接口匹配。
- 终接PF/客户端的完整准入与接受、错误/稍后投递路径、criteria持续调整和跨域迁移未在本页闭合。

依据：§24.4.2.1.1 SIP200 andNOTE7;24.4.2.2 matching-ID SIP200 procedure;24.3.2.1.1 SIP2xx procedure;24.2.2.1.1 SIP2xx procedure，印刷页526,540,541,559,562,563。列明正文义务按SHALL；SHOULD/MAY及NOTE另行说明，不提升强度。

## 使用边界

建立列表驱动ad hoc组的有限信令路径，不是全接收端、全成员交付或动态criteria生命周期实现。[配置组session](sds-session-establishment.md)与[预建立组使用](pre-established-group-sds-use.md)有各自条件，不能作为此处的默认补全。

[官方固定版本](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)。
