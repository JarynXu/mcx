# MCVideo广播自动接听与缓冲结果：Unconfirmed 200不证明收看

TS24.281 V19.3.0 与媒体TS24.581 V19.2.0分别标版。普通在网、有transmission control、以broadcast发起的新组呼；普通GMS组，client–O-PF–CF–T-PF–client。不是chat、system、ad hoc、NCF/gateway、临时/预配置重组、功能别名、远程/ambient、预建立、重入、广播升级或离网。

请求broadcast-ind=true，但不含emergency-ind、imminentperil-ind、alert-ind、user-requested-priority或优先Resource-Priority；客户端既有emergency/group-priority/call-priority状态均未置位，CF组emergency和imminent-peril状态为false。广播不被当成紧急呼叫，亦不由本次未点紧急按钮推定全部既有状态为普通。

每条claim只继承本主题common_conditions及自身conditions，不继承前条成功。本版9.2.1.2.1.1 step3明确调用6.2.8.2，才构成这里使用prearranged signalling入口的依据；不因名字类似就继承既有普通非广播页面的全部结论。

建立范围限CF确认会话不ongoing（不是已分配identity且active），无affiliated且on-network-required的成员，TNG1不运行；至少有可邀请的普通affiliated成员。终接小链限定T-PF已存auto-answer、目标完全没有预建立会话、无入站Answer-Mode/Priv-Answer-Mode、客户端允许自动接听。提前200 claim另以CF支持media buffering且当时尚未向主叫发最终响应为条件，不把该时点前提继承到后续响应处理claim。其他模式/required/无缓冲分支不补完整实现。

## 终接PF接听方式

适用条件：T-PF收到CF的on-demand广播邀请；无Answer-Mode/Priv-Answer-Mode，目标无预建立会话，且已保存auto-answer设置。

T-PF可因资源/拥塞500；缺isfocus→403/104，未收到Answer-Mode Indication→480/146，无MCVideo ID到public user identity绑定→404。通过后由存储的auto-answer选择6.3.2.2.5.1/.5.2，向绑定的public user identity发INVITE，PAI为T-PF PSI、Answer-Mode=Auto，并带SDP及入站MIME。这是SIP接听方式选择，不是媒体Reception Mode=0的授权。

- 选择on-demand的完整一般条件是“无未关联且媒体/video及TC sections匹配的预建立会话组合”；本页用更窄的完全无预建立会话满足该边界。
- 若带MKFC-GKTPs仍执行6.3.2.3.2；信令绑定、用户设置和媒体安全不能互相替代。未带入手动、Priv强制或预建立分支。

依据：§9.2.1.3.2;6.3.2.2.5.1/.5.2;6.3.2.2.9，印刷页 97、98、101、220、221。

## 客户端自动应答与拒绝

适用条件：终接客户端收到本广播邀请，Answer-Mode=Auto，且本地设置自动或本地手动但允许自动覆盖；不含优先/别名/重组。

客户端仍MAY因资源不足或规范范围外其他原因拒绝；若拒绝，通常给适当响应码和Warning，仅用户获准隐藏失败原因时可用不带Warning的480并停止。未拒绝且自动模式条件成立，按6.2.3.1.2/.1.1回200，带SDP answer、timer/Session-Expires及MCVideo/ICSI标签，MAY带P-Answer-State=Confirmed；发送200后与媒体平面交互。广播指示本身不取消此接听条件。

- 本页排除了紧急functional alias并发上限和临时组195分支，不能把那些拒绝条件误记为所有普通广播必查。
- 没有用户手动同意并不等于所有用户已收到RTP；接听和实际媒体接收是后续不同状态。SIP/RFC错误恢复未闭合。

依据：§9.2.1.2.1.2;6.2.3.1.2;6.2.3.1.1，印刷页 61、62、210、211、212。

## 183与PRACK门槛

适用条件：T-PF按auto-answer的on-demand helper处理本邀请，且收到客户端INVITE的200时判断如何向CF完成应答。

该helper生成无SDP的183并置P-Answer-State=Unconfirmed；可靠或不可靠取决于实际请求/策略。若CF收到带100rel的183 Unconfirmed则发送PRACK。T-PF收到客户端200后：183不可靠时立即回最终200；183可靠时，只有收到PRACK并已回PRACK的200后才回INVITE的200。生成最终响应时使用客户端SDP answer、PAI为PF PSI，先媒体交互再转发。PRACK的200不能替代INVITE的200。

- helper正文先写生成183，后文按was sent区分可靠性，本页不补源文未列的发送步骤细节。
- 本条只核自动接听可靠应答门槛，不推断自动accept与实际接收、组建立的相同完成时点。

依据：§6.3.2.2.5.2;9.2.1.4.1.1 provisional response，印刷页 98、99、224。

## 缓冲与Unconfirmed 200

适用条件：CF收到9.2.1.4.1所发邀请的183，P-Answer-State=Unconfirmed；TNG1不运行、CF支持media buffering、尚未向主叫发送SIP最终响应四条件同时成立。

CF按6.3.3.2.3.2生成200，提供SDP answer并置P-Answer-State=Unconfirmed；当组成员数大于on-network-max-participant-count时带Warning122。CF先完成媒体平面处理，再向主叫发送200。因此此200可能早于任何终接客户端的INVITE 200，不证明某个接收者已接受、更不证明全组均已看见视频。广播并未自动抹掉本主条的缓冲条件。

- 四条件缺一，不能直接使用本提前200规则。required/TNG1运行、无缓冲、其他final-response分支均未由本页补完成。
- 普通范围排除Warning149及优先SDP例外。此段也列通知已有conference订阅者，但不能据此授权broadcast订阅；该业务明确有480/105拒绝入口，见独立claim。
- 不把P-Answer-State=Unconfirmed解释为实际媒体发送许可；广播originating participant自身另有明确的状态规则。

依据：§9.2.1.4.2 unconfirmed-183 response branch;6.3.3.2.3.2，印刷页 123、124、232。

## 响应逐段转发与成功计数

适用条件：O-PF收到CF对本建立INVITE的2xx或最终4xx/5xx/6xx；另独立地，CF实际收到邀请目标的INVITE 200。

O-PF收到2xx时条件处理MKFC-GKTPs，生成客户端200/SDP，带入收到的Warning（若有）、PAI为PF PSI及映射后的session identity，先发200再媒体交互并启动SIP session timer；4xx/5xx/6xx则生成对应响应并转带收到的Warning。客户端收到2xx后与媒体平面交互。CF实际收到被邀请客户端INVITE 200时，另执行媒体交互、通知已有订阅者并将邀请200计数加1；这个计数事件不同于先前向主叫发出的Unconfirmed 200。

- 本普通范围没有触发priority implicit affiliation，不调用其完成/取消。成功入口写2xx而内部部分字段句写200，保留原口径。
- 不将O-PF的“200后媒体”与T-PF/CF的“媒体后200”合并为一个时序。通话级SIP成功、某目标accept与媒体流真正到达仍须分开。
- 后续全部失败、超时、替补邀请、释放和缓冲溢出不是此claim的结果；这些缺口不被“已经有一个200”填补。

依据：§9.2.1.3.1.1 response paragraphs;9.2.1.2.1.1 response paragraphs;9.2.1.4.1.1 response paragraphs，印刷页 210、219、224。

## 广播会议订阅限制

适用条件：客户端想订阅本broadcast发起的ongoing组会话，或CF实际收到该会话的conference SUBSCRIBE。

9.2.3.2客户端可订阅的前提包括会话不是以broadcast发起；CF对broadcast组会话的conference SUBSCRIBE明确返回480并带Warning105。不能机械使用普通组订阅状态来确认广播接收名单，也不能把一般组建立段的“可订阅/通知订阅者”解释成broadcast订阅已获准。

- 9.2.1.2.1.1成功段引用9.1.3.1，正文实际conference程序在9.2.3；保留错引，不让一般MAY覆盖明确broadcast条件。
- Warning105不能替换成普通非广播用户无权限的403/138。媒体自动接收通知也不是conference状态通知。

依据：§9.2.3.2;9.2.3.4.1;9.2.1.2.1.1，印刷页 210、276、278。

## 证据边界

- 未核23.281业务语义或24.484全部广播专用配置，不从不存在的查找命中断言“没有其它授权”。
- 无required/TNG1未运行、自动接听、支持缓冲且未发final是本成功小链边界；手动、required聚合、无缓冲最终成功和全部失败/超时恢复未闭合。
- originating广播step5与同时implicit的step4均保留；初始媒体SSRC、服务器全部初态与客户端状态的端到端映射尚未闭合。
- 广播升级、恢复/晚入、停止广播及全组释放未展开；不能把普通非广播的permission/terminated结论直接类推。
- GKTP/MIKEY算法、安全验证、媒体端口/完整SDP、GMS配置schema、跨系统与跨版本互操作仍是外部依赖。

## 按需继续

- [broadcast-ondemand-admission](broadcast-ondemand-admission.md)
- [broadcast-media-roles](broadcast-media-roles.md)
- [prearranged-call-terminating](prearranged-call-terminating.md)
- [prearranged-call-setup-result](prearranged-call-setup-result.md)
- [conference-subscription](conference-subscription.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；按条目单独标示媒体来源。

- [广播停止与会话释放的适用条件](broadcast-call-exit.md)
