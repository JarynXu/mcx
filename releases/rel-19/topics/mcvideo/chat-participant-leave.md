# MCVideo chat离开与移除：BYE确认不等于全组结束

TS24.281 V19.3.0，普通在网、带 transmission control、已建立的 on-demand chat group (restricted)；普通GMS组、client–PF–CF路径。排除预安排、broadcast、ad hoc、NCF/gateway、临时或预配置重组、别名、远程/ambient、预建立会话和离网。TNG3 claim另明确回溯同类会话建立阶段。

无紧急/迫近危险状态及其升级、取消或告警处理。单人离开、撤销 affiliation、取消 conference 订阅、停止发送源、全组 session 释放是不同事件；不把其中一个事件直接作为其余事件已完成的证据。

每条claim独立继承本主题common_conditions和自身conditions，不继承前条成功。仅复用源文明示的公共helper或直接读取其事件入口，不从预安排页面整体继承条件。

## 客户端离开和收到BYE

适用条件：用户要求离开已按需建立的chat session，或客户端收到释放该chat session的BYE；分别进入§9.2.2.2.2.1或.2。

主动离开明确调用6.2.4.1：先与媒体平面交互，生成BYE，Request-URI为要离开的MCVideo session identity，发送后在收到BYE的200时再与媒体平面交互。收到服务器BYE则明确调用6.2.6：先媒体交互，再发送200。主动离开调用Leaving helper，不是私呼Releasing helper6.2.5.1；一个客户端挂断不自动构成所有chat成员已结束。

- 若离开是因为migration，6.2.4.1才要求Reason: protocol=SIP、cause=200、reason-text=User migration；该行[ref1]未修。普通挂断不固定携带此原因。
- 没有从这些BYE步骤推导自动de-affiliation或conference退订。BYE失败、超时、并发处理依赖24.229，未在这里闭合。

依据：§9.2.2.2.2.1/.2;6.2.4.1;6.2.6;6.2.5.1，印刷页 63、64、256。

## PF双向BYE

适用条件：按公共PF helper直接规定的入口，PF收到客户端BYE，或在on-demand路径收到CF BYE；不声称chat专节另列了相同的PF end-call调用。

客户端方向的6.3.2.1.5先媒体交互，再向CF生成BYE，Request-URI采用收到的session identity，PAI为PF PSI；收到200后向客户端转发并释放与CF段相关的媒体资源。CF方向的6.3.2.2.8.1先处理CF段媒体，再向客户端发BYE；收到客户端200后先向CF回200，再处理客户端段媒体资源。两方向若收到mcvideo-info MIME均按各自helper复制。

- 这是公共helper的直接事件入口，不是将预安排§9.2.1.3.3.1的6.3.2.1.6错引移入chat；6.3.2.1.6实际为Priority call conditions。
- 6.3.2.1.5响应句主语仍写terminating MCVideo function；保留原文异常，不据此改变角色路由。字段完整性、事务重传和失败恢复见其外部24.229依赖，单个200不表示全链资源回收完成。

依据：§6.3.2.1.5;6.3.2.2.8.1，印刷页 91、92、101。

## CF先应答再判断存续

适用条件：CF收到普通chat BYE，经§9.2.2.4.2进入6.3.3.2.4。

CF先与媒体平面交互以释放该客户端SIP session相关资源，生成并发送BYE的200，然后才检查session release policy。若整会话需要释放，调用6.3.3.1.4，并在入站BYE有mcvideo-info时向出站BYE复制；若不需整会话释放，SHALL向仍在会话且订阅conference事件的客户端发送NOTIFY。因此离开者收到200既不证明全组已经释放，也不保证剩余会话继续。

- 本页排除ad hoc专用的授权用户+Reason User requested release分支，不把它当chat用户强制结束全组的权限。
- 人数统计更新的具体时刻未在此给出；不能自行补BYE到达前后临界计数算法。通知只向剩余订阅者，不向所有组名单成员；payload另见conference-state-notification。

依据：§9.2.2.4.2;6.3.3.2.4，印刷页 124、271。

## 主动移除与全组释放

适用条件：按chat的§9.2.2.4.3.2，组会话需要依6.3.8.1释放；或按§9.2.2.4.3.3，某客户端需要移除，例如de-affiliation或准入更高优先级用户。

这两个chat入口都明确调用6.3.3.1.4。该helper对待移除participant先媒体交互再发BYE；若要释放整个group session，则对全体participants发BYE；收到某BYE的200后处理相应SIP session媒体资源。单客户端成功移除后，chat专节只规定MAY向已有conference订阅者通知用户已移除，不升级为所有移除必发。

- 与预安排§9.2.1.4.4.2/.3指向紧急re-INVITE的6.3.3.1.5不同，chat这两个独立入口的引用是正确的。不能把预安排错引照搬成chat错引。
- 但chat容量替换§9.2.2.4.1.1 step11a实际仍引用预安排§9.2.1.4.4.3，后者仍错指6.3.3.1.5；不能用chat正确的主动移除段静默修复容量支路。
- 本段成功移除后的MAY通知，与接收BYE且不释放整会话时6.3.3.2.4的SHALL通知不同；未声明单人BYE200即所有人均已被移除。

依据：§9.2.2.4.3.2/.3;6.3.3.1.4;9.2.2.4.1.1 step11a;9.2.1.4.4.3，印刷页 104、235、262、263、271。

## 证据边界

- 24.229完整BYE错误、超时、重传与并发释放未核；不补全局回滚或原子完成。
- affiliation撤销和conference退订不是本BYE链的自动副作用，未补相应状态机。
- chat容量替换仍引用有错引的预安排移除段，不能用chat主动释放段替换；普通主动移除正确引用另列。
- TNG3 MAY/SHALL、T4/T1跨规范命名保留；不裁决规范优先级或声称已验证跨版本互操作。

## 按需继续

- [chat-release-policy](chat-release-policy.md)
- [private-call-server-release](private-call-server-release.md)
- [group-participant-leave](group-participant-leave.md)
- [conference-state-notification](conference-state-notification.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；媒体来源独立标版。
