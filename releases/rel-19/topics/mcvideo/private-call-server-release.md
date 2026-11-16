# MCVideo 私呼逐段释放：PF、CF的BYE处理与引用边界

TS24.281 V19.3.0，已经建立的普通在网、带 transmission control、单一直接 MCVideo ID 按需私呼。双方不使用预建立会话；不含功能别名、FTA、组呼、远程/ambient、无TC和离网。

本私呼不在紧急或迫近危险流程；没有未决的优先级升级/取消、紧急告警或其状态处置。本页不把取消尚未接受的 INVITE 与释放已建立会话混为一事。

每条规则独立继承本主题条件，再叠加自身 conditions；涉及24.581时仅指实际核读的V19.2.0，不声称与24.281 V19.3.0同版或完整互操作已验证。

逐段区分PF面向客户端的SIP session、PF面向CF的SIP session及整个MCVideo call。只有所列入口和条件成立才应用该claim；不据一段200宣布所有段已完成。

## 客户端方向PF入口的错引

适用条件：独立读取§6.3.2.1.5本身“PF收到客户端BYE”的正文；私呼入口§10.2.4.2.1.1的交叉引用冲突尚未消解。

该common helper规定先与媒体平面交互，再生成向CF的BYE；Request-URI沿用收到BYE中的session identity，PAI设为PF PSI；收到mcvideo-info时复制它。响应段写收到BYE的200后向客户端转带200，并交互以释放与CF的SIP session关联的媒体资源。

- §10.2.4.2.1.1实际指向6.3.2.1.6（Priority call conditions），不是这里的6.3.2.1.5；本页不静默改号或声称该入口已规范闭合。
- 6.3.2.1.5响应段主语原文为terminating MCVideo function，与前面的participating命名不同；不据此重新分配角色。
- 这里不沿用建立阶段的Contact映射自行发明新的BYE Request-URI转换。

依据：§6.3.2.1.5;6.3.2.1.6;10.2.4.2.1.1，印刷页 91、92、352。

## CF先响应再评估全会话策略

适用条件：CF收到本私呼BYE，由§10.2.4.3.1进入§6.3.3.2.4。

CF先与媒体平面交互以释放与该客户端SIP session关联的资源，再生成并发送BYE的200，之后检查session release policy是否需为每个participant释放会话。因此该上行200先于本条的全会话策略处理，不能证明其余participant已经应答释放。

- 不套用同helper的ad hoc group专用Reason条件。
- 不推断未在本段定义的participant计数更新时刻；后续释放取决于策略条件。

依据：§10.2.4.3.1;6.3.3.2.4 steps1–3，印刷页 124、352。

## 私呼释放策略的三个备选条件

适用条件：CF评估§6.3.8.2的private-call release policy；仅按该版本原文识别触发。

原文三个条件任一成立即要求CF释放私呼：收到媒体平面报告T4(Inactivity)到期、会话时长超过私呼最大时长、或会话中只剩一人/无人。人数不足不是同时要求时长超限；时长比较保留超过。

- 24.281写T4(Inactivity)，而已读24.581 V19.2.0 §6.3.4.3.5用T1(Inactivity)，§6.3.4.4.1/.4.2用T4监督排队授予。24.581图6.3.4.1-1又保留T4(inactivity)文字。不能静默替换号码，也不能把授予重传到期当私呼挂断条件。
- 配置值及全部计时器初始化未在本页闭合；请分别查server-idle-timers与server-queued-grant-retry。

依据：§6.3.8.2，印刷页 140。

## 策略后的BYE调用与主动入口缺口

适用条件：CF已在§6.3.3.2.4处理收到的BYE，且策略判定需要释放MCVideo session；通过其step4进入§6.3.3.1.4。

CF按BYE helper先与媒体平面交互，再生成并发送BYE；原收到BYE带mcvideo-info时也复制到出站。收到相应BYE的200后，另交互释放与该participant SIP session关联的媒体资源。这个有条件调用不能被解释为所有服务器主动释放入口都已核通。

- 服务器主动释放入口10.2.5.3.1/.4写6.3.3.1.5；该条实际是emergency-group re-INVITE，真正BYE helper标题在6.3.3.1.4。此处只描述已由6.3.3.2.4明确调用的路径，不替它修号。
- 6.3.3.1.4的TNG3和向组内所有participant发送规则属于组呼文字，不移入本私呼条件。
- 不自行补BYE Request-URI/Reason、错误响应处理或剩余participant枚举算法。

依据：§6.3.3.2.4 step4 and BYE200 branch;6.3.3.1.4;10.2.5.3.1;10.2.5.4，印刷页 104、124、353。

## 终接PF两段资源分别释放

适用条件：T-PF收到CF发来的本按需私呼BYE，按§10.2.4.2.2.1或§10.2.5.3.2.1调用§6.3.2.2.8.1；返回分支只在收到其向客户端发出BYE的200时。

T-PF先交互以释放与CF的SIP session关联的媒体资源，再生成客户端方向BYE，PAI设PF PSI，收到mcvideo-info才复制，然后发送。收到客户端BYE的200后，先向CF回复该BYE的200，再交互释放与客户端SIP session关联的媒体资源。两个资源范围和先后次序不同。

- 这里不是简单原包透传，也未写任何BYE失败都可以回成功；失败和超时依赖未展开。
- 第一处24.581引用具体到6.4；不能把CF的general/basic仲裁实例当作PF自己的实例。

依据：§10.2.4.2.2.1;10.2.5.3.2.1;6.3.2.2.8.1，印刷页 101、352、353。

## PF停发与按需资源回收

适用条件：TS24.581 V19.2.0 PF分别收到应用/信令的“session release initiated”或“session is released”指示；会话为on-demand。

收到释放开始指示时，PF停止向participant和control server发送 transmission control 消息，并停止向客户端和CF发送RTP。收到会话已释放指示后才释放相关媒体资源。预建立会话的另一分支不适用于本页。

- 这里只说停止发送和按需资源回收，不为未规定的迟到包、缓存清除、错误恢复补动作。
- 与24.281媒体交互调用形成关联，不声称两个不同版本的全部SIP与媒体接口映射已验证。

依据：§24.581 V19.2.0:6.4.4，印刷页 103。

## 控制服务器整通话两阶段释放

适用条件：TS24.581 V19.2.0 transmission control server正在释放整个MCVideo call，而不是仅移除一个participant并让其余通话继续。

step1停止向本通话所有participant发送 transmission control 消息和RTP。应用/信令判定通话已释放后，step2终止本通话的general transmission/reception实例，以及各participant的basic transmission/reception实例。先停流不等于通话级和各用户实例已经一起销毁。

- 同条另有“某客户端离开而通话继续”的两阶段分支；不能拿其只回收对应basic实例的范围替代整个私呼释放。
- 本claim不重复已有单源Transmission End/Media Reception End规则，也不改变它们可能保持通话存续的事实。

依据：§24.581 V19.2.0:6.3.3 whole-call branch，印刷页 54。

## 证据边界

- 仅所列已核入口；交叉引用疑义保留，不构成无歧义完整释放实现。

## 按需继续

- [private-call-client-release](private-call-client-release.md)
- [private-call-server-admission](private-call-server-admission.md)
- [participant-transmission-control](participant-transmission-control.md)
- [participant-reception-control](participant-reception-control.md)
- [server-idle-timers](server-idle-timers.md)
- [server-queued-grant-retry](server-queued-grant-retry.md)
- [server-stream-idle-termination](server-stream-idle-termination.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

媒体释放另据 [TS24.581 V19.2.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf) 的上述具体条款；与信令标准分开追溯，不能据此宣称互通已验证。
