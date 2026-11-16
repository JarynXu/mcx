# MCVideo chat存续：三项释放条件与可选组时长

TS24.281 V19.3.0，普通在网、带 transmission control、已建立的 on-demand chat group (restricted)；普通GMS组、client–PF–CF路径。排除预安排、broadcast、ad hoc、NCF/gateway、临时或预配置重组、别名、远程/ambient、预建立会话和离网。TNG3 claim另明确回溯同类会话建立阶段。

无紧急/迫近危险状态及其升级、取消或告警处理。单人离开、撤销 affiliation、取消 conference 订阅、停止发送源、全组 session 释放是不同事件；不把其中一个事件直接作为其余事件已完成的证据。

每条claim独立继承本主题common_conditions和自身conditions，不继承前条成功。仅复用源文明示的公共helper或直接读取其事件入口，不从预安排页面整体继承条件。

## 三项chat释放条件

适用条件：CF依§6.3.8.1评估本普通chat group session的存续。

原文五项OR中，第1项T4(Inactivity)报告和第3项发起人离开且符合地方策略均明确限定pre-arranged。对chat，直接适用的是其余三项：只剩一人或无人、最低数量的affiliated组成员不在场、TNG3到期；任一成立，CF SHALL释放组session。不能因chat发起人离开就套第3项，也不能据此保证发起人离开后一定继续，因为其余三项仍可能成立。

- 这三个条件是该条对本范围的直接要求，不声称它穷尽所有外部或其它功能的释放入口。
- 最低affiliated人数在本条未给具体配置字段或算法，不等同于初建required全部应答、on-network-minimum-number-to-start或静态成员总数。
- 排除prearranged专用T4条件不等于媒体永不超时；24.581的T1报告/信令决定另按其角色处理，见独立bridge claim及server-idle-timers。

依据：§6.3.8.1;9.2.2.4.3.2，印刷页 140、271。

## TNG3的配置及停止条件

适用条件：CF收到发起chat session的INVITE且已分配session identity，或该chat session的TNG3已经运行；不含临时组merge/split及优先TNG2交互。

6.3.3.5.1规定maximum-duration字段存在则SHALL按其值启动TNG3，缺失则SHALL不启动；NOTE明确chat配置此字段可选。chat主条9.2.2.4.1.1 step10另外使用MAY handle TNG3措辞，两处分别保留，不擅自消解。最后客户端离开时停止TNG3；BYE helper也要求未到期的TNG3在最后客户端被移除时停止。到期按6.3.3.1.4释放会话。

- 没有字段时不虚构默认最大时长；即使不启TNG3，人数或最低affiliated条件仍可导致释放。
- 单个成员离开但并非最后一人，不是本条停止或重置TNG3的条件；新成员加入不由本条推导每人独立计时或重启全组计时。
- 配置schema、实际duration值与主条MAY/helper条件SHALL的规范优先关系未进一步裁决。

依据：§6.3.3.5.1;6.3.3.1.4;9.2.2.4.1.1 step10，印刷页 104、128、262。

## 媒体回收与不活动报告

适用条件：普通chat中应用/信令决定单participant退出但通话继续，或决定全call释放；另对照general transmission控制的T1到期事件。实际读取24.581 V19.2.0，不与24.281 V19.3.0混为同版。

24.581的单人退出分支先停止向该客户端发送transmission control/RTP并丢弃来自它的对应消息，信令确定该participant已释放后才回收其basic transmission/reception实例。全call释放分支则先停止向全体发送，再在信令确定全call已释放后终止该call的general和全部basic实例。T1(Inactivity)到期本身仍按可配置服务商策略报告应用/信令：发起release才进入Releasing；未发起时SHOULD重启T1，并SHALL保持G: Transmit Idle。媒体报告或单源停止不单独证明chat全部成员已释放。

- 24.281写T4(Inactivity)且该项只适用于prearranged；24.581文字为T1，不能将其自动等同或据此为chat补一项强制不活动释放条件。
- 本claim不重写既有server-idle-timers和group-participant-leave的完整状态机；从信令到媒体的具体接口、跨版本集成与并发回收未验证。

依据：§24.581 V19.2.0:6.3.3;6.3.4.3.5;24.281 V19.3.0:6.3.8.1，印刷页 53、54、58、140。

## 证据边界

- 24.229完整BYE错误、超时、重传与并发释放未核；不补全局回滚或原子完成。
- affiliation撤销和conference退订不是本BYE链的自动副作用，未补相应状态机。
- chat容量替换仍引用有错引的预安排移除段，不能用chat主动释放段替换；普通主动移除正确引用另列。
- TNG3 MAY/SHALL、T4/T1跨规范命名保留；不裁决规范优先级或声称已验证跨版本互操作。

## 按需继续

- [chat-participant-leave](chat-participant-leave.md)
- [group-release-policy](group-release-policy.md)
- [server-idle-timers](server-idle-timers.md)
- [chat-ondemand-admission](chat-ondemand-admission.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；媒体来源独立标版。
