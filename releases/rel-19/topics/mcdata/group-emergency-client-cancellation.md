# MCData 组会话客户端取消：紧急条件、告警与对端状态分开判断

限 TS24.282 V19.7.0，在网、已有 on-demand SDS 预安排组 session；本页说明的是客户端过程，不是端到端组服务器升级/取消实现。不是 standalone SDS、pre-established session、FD、IPCONN、adhoc 或 regroup。

MED 是客户端自身紧急状态，MDEG 是客户端跟踪的组紧急状态，MDEGC 是该客户端的组通信紧急状态，MDEA 是告警状态；CF 的 in-progress emergency group 状态另有维护者。来源为 §4.10 pp45–46，不用任一客户端状态代表全组提交。

本版 §16.2.2.1 p383、§16.2.2.2 p385、§16.2.3.2 p402 的编辑说明保留紧急组/组通信支持可能缺失、部分提供或仅为告警服务的限制。这里仅说明具体已列出的客户端步骤，不将全部步骤抹为FFS，也不保证服务器、媒体或实际优先承载已经完成。

现有SDS预安排组session仍在进行；本用户取消自身的紧急组通信条件，可选择是否同时取消自己的告警。排除替他人取消告警，不生成originated-by。

## 取消权限与会话内请求

适用条件：用户在ongoing预安排组通信中请求取消in-progress emergency条件，进入§6.2.7.2。

客户端按 §6.2.8.1.7 的本地策略判断是否可发送组紧急状态取消请求，原文举dispatcher或发起者为例，并未规定这些身份自动足够。未获授权时SHOULD提示、SHALL停止。通过后使用会话内re-INVITE，填session-type=prearranged和目标组mcdata-request-uri，带g.3gpp.mcdata Contact特征、SDS SDP offer以及按helper确定的Resource-Priority。取消的是紧急条件，不是发BYE离开或终止SDS会话。

- 组取消的客户端local policy不等同用户自己的告警取消许可；服务器§6.3.7.2.3又有allow-cancel-group-emergency输入。这里不声称客户端决定已替代服务器授权。
- §6.2.7.2 NOTE1说明calling user身份由上游PF插入，但本页未核出适用于组re-INVITE的完整PF入口，不由该NOTE补出其每一步行为。
- 无ongoing通信的MESSAGE分支不在此claim；原文回指16.2.1.4实际是地理区域通知，不能静默替换为告警取消过程。

依据：§6.2.7.2 opening,steps1,2,4–9;6.2.8.1.7;6.2.8.1.2/.15，印刷页 63、64、70、73、77。

## 是否保留自身告警

适用条件：组紧急条件取消已获客户端授权，执行§6.2.8.1.3，且MDEGC3（已获准）；只处理本用户告警。

若MDEA1（无告警），客户端写emergency-ind=false，先清MED，再把MDEG置3（取消待确认）。若有告警但用户只取消组紧急通信，仍写emergency-ind=false并置MDEG3，但保留MED。若用户要求组紧急条件与自己的告警一并取消，emergency-ind=false照常发送；仅在告警取消授权也通过时，才再写alert-ind=false、置MDEA4并清MED。无权取消告警时SHOULD告知，组取消请求仍依本分支继续准备并置MDEG3。

- 这些MED清除发生在发送结果之前，不能将其解释为服务器已接受。失败分支未提供统一MED恢复动作，不自行补。
- MDEA“不是1”与用户是否只取消组紧急条件/同时取消告警是必要分支，不能把任何emergency-ind=false都解释成取消告警。
- Resource-Priority helper的紧急分支要求MDEGC2/3且本请求满足§6.2.8.1.8的紧急通信授权，或另由MDEG2进入；正常分支则要求本请求满足§6.2.8.1.7的取消授权且MDEG为no-emergency或cancel-pending。取消准备后的MDEGC3/MDEG3本身不足以证明两分支冲突。只有另满足前述紧急请求授权且同时满足取消授权，文字条件才可能重叠；§6.2.8.1.8在取消请求上的适用性及重叠裁决未闭合，不把它写成实际必现冲突。

依据：§6.2.7.2 step2;6.2.8.1.3 all three branches;6.2.8.1.6 cancellation paragraph;6.2.8.1.2/.7/.8，印刷页 64、70、71、73、74。

## 取消2xx与延后告警结果

适用条件：客户端收到§6.2.7.2所发取消re-INVITE的2xx。

客户端调用24.582用户面接口，随后将MDEG置1、MDEGC置1。若自己的告警处MDEA4、发出的请求没有originated-by，且该2xx不含Warning149，才将MDEA置1。带149时不能从这个2xx推定告警已取消；后续本对话内、Request-URI含标识ongoing group session的MCData session ID，且符合INFO包/MIME/指示入口条件的消息先获200，再在“发出的请求无originated-by且MDEA4”条件下按alert-ind判定：true回MDEA3，false置MDEA1。

- INFO还须符合§6.2.8.1.13的入口：位于优先通信对话内，Info-Package含g.3gpp.mcdata-info，带与该package关联的mcdata-info MIME，且至少包含一个规定指示；这些条件不能替代调用点的Request-URI session ID条件。
- 这里是会话内取消的2xx/INFO规则，不是独立MESSAGE告警取消所要求的alert-ind-rcvd=true与client-id匹配；两者不得互换。
- 取消INFO的step4不以MDEGC3为条件，不能误套升级INFO的step2；取消2xx已经把MDEGC置1仍可处理本条列出的MDEA4反馈。
- 这些客户端迁移不证明所有参与者、CF IPEG或媒体承载已同步，也不证明任何历史SDS消息被撤销。

依据：§6.2.7.2 2xx and INFO paragraphs;6.2.8.1.13 opening,steps1,4，印刷页 64、75、76。

## 取消失败的状态条件

适用条件：客户端的§6.2.7.2取消re-INVITE收到4xx、5xx或6xx。

客户端将MDEG设为2（进行中）。若错误响应含alert-ind=true且发出的请求没有originated-by，则将MDEA置3；若错误响应没有含alert-ind的mcdata-info，也没有originated-by，则把MDEA恢复到进入本次过程前的值。原文NOTE3说明组紧急状态取消被拒后，会话继续保持紧急级优先。不能把取消失败写成SDS会话终止、告警统一清零或全部本地变量回滚。

- step2的originated-by条件明确落在sent请求；step3语法则落在错误响应。按原文分别保留，不能为对称而把step3也改成sent请求。
- 错误响应中alert-ind=false、3xx、无响应及MED恢复未在此段给出完整处理，不补默认分支。
- 此处的MDEG恢复与升级失败helper不同，后者只在confirm-pending条件下清组视图，不能共用一个“失败全部复位”规则。

依据：§6.2.7.2 error-response paragraph,steps1–3 and NOTE3，印刷页 64、65。

## 接收端本地动作及媒体接口

适用条件：另一个客户端在已有on-demand SDS组session中按§6.2.7.4接到re-INVITE；本条只述emergency-ind=true/false，不处理第三方告警originated-by。

收到emergency-ind=true，客户端SHOULD显示发起用户和紧急组通信提示，若还带alert-ind=true则SHOULD显示告警；随后设MDEG2，并复位imminent-peril相关组/通信状态。收到emergency-ind=false，则SHOULD显示取消者，设MDEG1；只有MDEGC原为3才将其置1。之后检查Resource-Priority，原文允许在规范范围外采取进一步动作；接受请求、生成含规定Contact特征与SDS SDP answer的200、发送200，最后调用24.582媒体接口。

- 此接收helper把本地状态动作列在200之前；发送200之后调用媒体接口。不要把初始SDS session“先已发200再收到ACK”的独立条件强行移植到这里，也不由此断言媒体已经成功。
- 无originated-by的alert-ind=false可触发显示取消提示，但本接收分支没有据此统一清除本用户MDEA；本人的取消反馈仍按前面专门响应/INFO条件判断。
- Contact里本条原文用g.3gpp.mcdata及MCData ICSI，不静默改成初始SDS请求的其他标签。SHOULD显示不是人已读；规范范围外的Resource-Priority动作不是已核QoS算法。

依据：§6.2.7.4 steps1,3,5–12;9.2.4.2.2，印刷页 66、67、225。

## 证据边界

- 服务器组re-INVITE完整准入、IPEG提交、成员分发与响应收敛未闭合。本页不能拿§9.2.4.3.5/.6或§9.2.4.4.5–.8的one-to-one wrappers替代；§6.3.7.1.1/.14是组侧生成helper，不足以补caller。
- 纯组状态、无ongoing通信的取消仍未闭合：§6.2.7.2 p63错指地理通知16.2.1.4 p382；§6.2.7.5 p68的生成步骤未列client-id却在反馈要求匹配，等待emergency-ind-rcvd，而已核告警CF取消使用alert-ind-rcvd且入口依赖alert-ind=false。不能把两链无条件拼成可执行过程。

## 按需继续

- [emergency-alert-self-cancellation](emergency-alert-self-cancellation.md)
- [sds-session-message-evidence](sds-session-message-evidence.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§6.2.7.1 step3;6.2.7.2 step8;6.2.8.1.1/.2：调用方发送re-INVITE，被调紧急指示/Resource-Priority helper正文多写INVITE或REFER。 按明确调用关系陈述客户端义务，不增发一个初始INVITE/REFER，不宣称完整编码互通已经验证。

§6.2.7.2 step8;6.2.8.1.2/.3/.7/.8：取消准备后的MDEGC3/MDEG3本身不足以判定Resource-Priority分支重叠。紧急分支除MDEGC2/3外还要求本请求满足§6.2.8.1.8紧急通信授权（另有MDEG2入口）；正常分支要求§6.2.8.1.7取消授权及no-emergency/cancel-pending组状态。只有两种请求授权条件也同时成立时，文字条件才可能重叠；原文未闭合§6.2.8.1.8如何适用于取消请求及如何裁决重叠。 完整保留两分支条件及配置值来源，不把状态组合写成实际必现冲突，也不自行确定取消请求必定满足紧急请求授权或补分支优先级。

§6.2.7.2 error step2 versus step3：step2以sent请求无originated-by作条件，step3却以错误响应未含originated-by作条件。 保留各自承载对象，不静默统一。

§6.2.7.2 opening;6.2.7.5;16.2.1.4;16.2.3.1/.2：无通信取消的错误回指、生成步骤未明列client-id、emergency-ind-rcvd与告警取消alert-ind-rcvd不一致、CF入口对alert-ind的条件未闭合。 本页只说明ongoing session客户端链，不把专门MESSAGE过程或告警过程强行接上。

§6.2.8.1.17 versus6.2.8.1.1/.3：release helper写MDEG3:confirm-pending，与其他条款MDEG4:confirm-pending/MDEG3:cancel-pending不一致，而且只明确特定建立中状态。 不把该helper推广成所有通信释放都清除组状态的规则；这里的紧急条件取消不是release。

§4.10;6.2.8.1.8;16.2.2.1/.2;16.2.3.2：概述称支持紧急组流程，告警部分Editor note又保留部分/有限支持；授权服务种类限制另有FFS。 按具体条款给客户端结论，同时公开支持/依赖边界；不因编辑说明抹去已列过程，也不因概述宣称实现全部闭合。
