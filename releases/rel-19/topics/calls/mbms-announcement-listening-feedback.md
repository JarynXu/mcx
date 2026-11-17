# MCPTT MBMS：公告、监听与暂停反馈

固定 TS24.379 V19.4.0 §14 的 MCPTT MBMS 承载公告、客户端缓存、监听及暂停状态报告、PF接收责任；不含5G MBS §14B，也不是组呼发起、归属或入会程序。

公告发送/接收、监听变化及RAN暂停事件分别触发各角色动作，更新与取消也是替代分支；不要求每个报告者都处于进行中的组呼。各claim的事件与身份守卫独立适用。

Map/Unmap Group To Bearer只作为本条款明确使用的外部事件；完整承载激活、映射消息、话权、媒体切换与安全算法不在本文展开。公告、信令响应、监听报告和实际收到业务音频是不同证据。

## 公告说明可用承载，不是组呼已经接通

适用条件：PF依本地策略决定向某客户端公告已预激活MBMS承载；首次公告构造适用本节。

首次公告包含承载通用MBMS子信道的一个承载，并可附带零个或多个媒体/媒体控制承载。PF用SIP MESSAGE发给第三方REGISTER的To URI，PAI携PF的MBMS PSI，mcptt-request-uri携目标MCPTT ID。正文version=1，每个announcement带TMGI、QCI及服务区列表；多载波支持时带频率，承载通用子信道时带指向SDP媒体行的GPMS。report-suspension可设true或false。SDP包含通用子信道的有效组播地址/端口；媒体子信道的占位地址和端口不能作为最终媒体接收参数。

规范强度：MESSAGE发送、指定身份及必需公告字段为 SHALL；report-suspension为 MAY；音频相关媒体行在step5(b)/(c)为 SHOULD，通用子信道媒体行为 SHALL，其安全与独立话权媒体行另受各自条件限制。

依据：§14.1；§14.2.2.1；§14.2.2.2 steps1-9,NOTE1-9。页码：582,583,584,585。

14.2.2.2 NOTE2/4将媒体最终参数交给Map Group To Bearer等消息；本页不补这些消息或把公告当成映射完成。NOTE8还区分首次映射所需的通用子信道服务区与媒体承载服务区交集，以及成功映射后的接收区域。

发送前密钥材料、MSCCK/MuSiK生成分发按14.2.2.1及33.180依需要执行；要求保护通用子信道控制时，SDP密钥处理按14.2.2.2 step5(d)。本文仅登记该依赖，不把收到公告等同已安全解密。

完整SDP、ROHC和独立话权子信道配置仍按step5/6的条件处理；本文不是可直接发送的完整报文模板。

## 同一TMGI更新或显式取消，未提及不等于删除

适用条件：PF更新或取消先前已发送的公告；同一消息可混合新建、更新和取消项。

更新保留TMGI；QCI及服务区列表可沿用或更新，原先带频率时须保持该频率，GPMS及SDP须与初始公告相同，report-suspension可带原值或新值。取消项保留TMGI但不得带mbms-service-areas；仅当整份usage-info正文全部为取消项时，不得带GPMS及SDP。新公告未提及的旧公告不会隐式删除；新消息若携SDP，14.2.2.1说明其整体替换既有SDP。

规范强度：更新中的固定/可更新字段要求和取消项省略规则为 SHALL/SHALL NOT；更新report-suspension为 MAY；未提及旧公告不删除及SDP整体替换是原文NOTE的解释。

依据：§14.2.2.1 NOTE；§14.2.2.3 steps1-7,NOTE1-2；§14.2.2.4 steps1-4。页码：583,585,586。

不要把“整份正文均取消”加强成“只要有一项取消就去掉SDP/GPMS”。TMGI不能用更新改号。

一般新公告的SDP整体替换说明，不解除更新程序必须携初始相同SDP的具体要求；本文不自行补混合消息的原子回滚或事务提交规则。

## 客户端按TMGI保存、关联或删除，安全失败会停止后续处理

适用条件：客户端收到P-Asserted-Service为MCPTT ICSI且含一个或多个announcement的mcptt-mbms-usage-info SIP MESSAGE。

客户端逐公告处理：有mbms-service-areas时，按TMGI替换已有项或保存新项，并关联所收SDP、GPMS及PAI中的PF MBMS PSI。若通用子信道媒体行包含指定MIKEY-SAKKE I_MESSAGE，则核发起URI和签名；URI不同于服务PF的PSI或认证失败时拒绝488/136并停止后续步骤。通过对应前序后，进入已公告承载可用的MBMS服务区时监听通用子信道，并检查报告条件。没有mbms-service-areas时，丢弃该TMGI的旧公告、解除SDP关联并停止监听通用子信道；仅在无其他公告仍关联该SDP时删除SDP，然后检查报告条件。

规范强度：缓存/关联、满足条件后的认证及失败488停止、进入可用服务区后的通用子信道监听、取消清理为 SHALL；取消末项按原文检查报告条件，不升级为无条件立即报告。

依据：§14.3.2 opening,steps1(a-h),2(a-d)；§14.2.2.4 (comparison: cancellation encoding)。页码：586,589,590。

同消息的SDP和密钥与通用子信道关联；Map Group To Bearer的媒体行号须在收到该Map的通用子信道所关联SDP中解释，不任取最近一次全局SDP。

原文先列保存/关联再列密钥校验；未给出校验失败回滚整个缓存的规则，不自行保证原子性。step1(f)(v)写使用参与功能的KMS配置UID key解密MSCCK，本文保留此角色措辞，不替换成另一实体的密钥。

本页仅说明条件安全接口，不声称完整33.180验证。公告接收段未在这里给出全部SIP成功响应行为，不补200成功即已接收媒体的结论。

## 监听和不监听报告各有事件组合

适用条件：客户端实际收到公告、映射/取消事件或经历无线条件变化；分别判断下列替代分支。

报告listening有两条入口：收到通用信道上的Map Group To Bearer、已参加其标识的组会话且尚未报告listening；或收到公告、进入有通用MBMS可用的服务区且无线条件良好。报告not-listening有三条入口：进行中会话收到与Map相同承载身份的取消且尚未报not-listening；或无进行中会话、取消了此前因通用子信道可用而报listening的公告且尚未报not-listening；或无线条件差。每个分支按自己的条件判断，不能把正在参加组呼设为所有报告的前提。

规范强度：任一列出分支的完整条件成立时，按14.3.3.2报告对应状态为 SHALL；不同分支之间为替代关系。

依据：§14.3.2 steps1(g-h),2(d) (actual preceding calls)；§14.3.3.1 listening/not-listening conditions。页码：590,591。

状态未报告守卫出现在所列映射或取消分支，不能补到所有无线条件分支。收到公告本身不足以满足第二条listening入口，仍需服务区和良好无线条件。

该层报告监听状况，不建立组会话，也不自行完成Map/Unmap。原文取消条件写TGMI而公告用TMGI，本文按承载身份描述，不把文字异常当成已修复的线缆字段定义。

## 报告发回公告给出的MBMS PSI，PF先核用户绑定

适用条件：客户端发送监听状态报告；或PF收到相应usage-info及标识其所服务用户的mcptt-request-uri。

客户端用SIP MESSAGE发往公告PAI提供的PF MBMS PSI，正文version=1并携用户MCPTT ID。listening/not-listening按实际状态编码，并带相应承载身份；报告进行中会话子信道时另带session-id，报告通用子信道时分别用general-purpose=true/false；接收质量扩展可选。同一正文可包含两种监听状态。PF核PAI公共用户身份与正文MCPTT ID绑定后，依据session-id通知媒体层该会话客户端的监听状态，依据general-purpose通知通用子信道状态；not-listening还调用媒体接口。

规范强度：报告必需字段和发送、PF绑定验证及匹配后的媒体通知为 SHALL；客户端P-Preferred-Identity为 SHOULD，质量扩展为 MAY；14.2.4所列异常403为 SHALL。

依据：§14.3.3.2 listening-report steps1(a-h),2,NOTE1-2；§14.2.3 listening-status branch,NOTE1-3；§14.2.4。页码：587,588,591,592。

通用子信道not-listening隐含此前报告listening的进行中会话子信道也不再监听；不等于用户退出组呼或解除归属。

PF异常条款对PAI不属于其服务用户，以及服务用户发来announcement的指定组合回403。正文用户为本PF所服务但PAI绑定不匹配时，14.2.3只有匹配后动作；不将14.2.4第一条件泛化成所有不匹配都已规定同一错误响应。

14.3.3.2两种监听报告的承载字段原文写TGMI；本页未将其静默改为TMGI或声称已完成F.2 schema一致性核对。质量扩展的服务器用途为实现相关，报告也不是音频成功证明。

## 即将暂停、撤销暂停与已经不监听不能混为一谈

适用条件：客户端最近已报告某承载listening并收到RAN暂停相关事件；或PF收到暂停状态报告及所服务用户身份。

最近状态为listening、RAN通知即将暂停且未收到report-suspension=false时，客户端报告suspending。撤销暂停报告还要求先前已报即将暂停、尚未检测到实际暂停、RAN通知不再暂停，并同样未被false禁止报告。消息发往公告中的MBMS PSI并带用户ID；suspending携同一MCH上的suspended-TMGI，可附可用的other-TMGI，计数为两类元素总数；not-suspending只按suspended-TMGI计数。不同MCH的暂停及暂停/撤销暂停分别发消息。PF核PAI与用户ID绑定后记录“即将暂停”或“不再即将暂停”，可按实现/配置采取减流、切单播或恢复等措施。

规范强度：完整触发条件成立后的报告、必需计数/身份字段、PF绑定验证及状态理解为 SHALL；P-Preferred-Identity为 SHOULD，other-TMGI及PF实现/配置应对为 MAY。

依据：§14.2.2.2 step6(e),NOTE9 (report control)；§14.3.3.1 suspension/not-suspending conditions；§14.3.3.2 suspension-report paragraph,steps1(a-h),2,NOTE3-4；§14.2.3 suspension branch,NOTE4-6；§14.2.4 (abnormal identity condition)。页码：585,588,591,592,593。

report-suspension缺失不等于禁止；原文门槛是未收到false。该开关不取消普通listening/not-listening报告。

即将暂停时实际暂停尚未发生；PF应理解状态，但具体应对措施为MAY，不保证一定切单播。随后报告相关子信道not-listening被解释为暂停实际发生；不能把suspending直接当成已停止接收。

RAN事件和MCH/MTCH信息是此流程输入，本页不展开无线承载算法；媒体接口被调用不证明传输连续性已经完成。

## 阅读边界与导航

范围止于24.379明确的公告/报告信令责任及媒体接口。MuSiK完整下载、映射/话权、5G MBS join/leave与业务通话建立均不由本页替代。

[组呼成立门槛](group-acknowledged-start.md)与本页承载监听反馈不是同一事件；[信令密钥更新](../security/signalling-key-update.md)也不能替代公告和反馈条件。

来源：[TS24.379 V19.4.0 官方原文](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
