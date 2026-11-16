# MCVideo全组释放：五项策略、TNG3和公共BYE边界

TS24.281 V19.3.0，普通在网、带transmission control、按需预安排MCVideo组呼；普通GMS组、客户端-PF-CF路径。本页重点是已建会话离开/释放，TNG3生命周期claim另明确回溯同会话的建立阶段。不含chat、broadcast、ad hoc、NCF/gateway、临时/预配置重组、远程/ambient、预建立会话或离网。

没有紧急/迫近危险状态及其升级、取消或告警处理；不以私呼的最大时长条件替代组呼TNG3，也不将停止一个媒体源、退出一个SIP会话、撤销affiliation、取消conference订阅与释放整个组呼混为一件事。

每条claim独立继承本主题common_conditions和自身conditions，不继承前一条成功。区别离开客户端对应的SIP session、PF-CF/客户端两段资源、CF整个组会话及其每participant的媒体实例。

普通用户选择离开是本页主线；如涉及User migration，仅保留源文Reason条件，不研究迁移流程。地方策略移除高优先级替换者、去affiliation等只作为明确的成员移除入口示例，不额外执行相关状态机。

## 全组释放的五项条件

适用条件：CF评估§6.3.8.1的本普通预安排组呼释放策略。

以下五项任一成立即SHALL释放本预安排组会话：CF收到媒体平面报告T4(Inactivity)到期；会话只剩一人或无人；发起人离开且地方策略要求在该情形释放；最低数量的affiliated组成员不在场；TNG3到期。其中原文第1项和第3项明确只适用于pre-arranged，不能直接用于chat。一个人挂断并不自动等于全组结束，但可能触发人数不足或发起人策略等条件。

- 五项是OR，不是同时满足；发起人离开必须保留according to local policy前提，不改成所有发起人退出都结束全组。
- “minimum number of affiliated MCVideo group members is not present”在本段没有给出具体配置字段或算法，不能擅自等同于初建on-network-minimum-number-to-start、required成员全部应答或客户端名单总数。
- T4名称与实际核读24.581 V19.2.0的T1/T4不一致，见独立计时器边界claim；本页不靠改名消除冲突。

依据：§6.3.8.1，印刷页 140。

## TNG3的组级生命周期

适用条件：CF收到用于发起组会话的INVITE，已分配session identity；或TNG3在本普通组会话中运行/到期。

组文档存在on-network-maximum-duration时，CF使用该值启动TNG3；字段不存在时SHALL不启动。原文同时注明该字段对预安排组配置为mandatory，chat才optional，不能把缺字段分支当成预安排组可自由省配。最后一个客户端离开时停TNG3；TNG3到期则按6.3.3.1.4释放会话。另在BYE helper中，TNG3未到期且最后客户端被移除时必须停止它，不是任何一名成员离开都重置或停止组时钟。

- 只核本普通组路径，合并/拆分临时组及TNG2优先状态交互被排除。未读取配置实际值，不给固定组呼最大秒数。
- 配置mandatory的说明来自24.281本段NOTE；未进一步核24.481 schema。一般重入/晚进入是否影响时钟不能靠猜测补出，本段未给按每次加入重新启动的规则。

依据：§6.3.3.5.1;6.3.3.1.4，印刷页 104、128。

## 单成员与全体BYE范围

适用条件：独立读取§6.3.3.1.4的公共BYE helper；其中“需要移除participant”或“需要释放整个MCVideo group session”的条件已经成立。合法明确调用包括收到BYE后策略要求释放的§6.3.3.2.4 step4，以及TNG3到期§6.3.3.5.1。

需要移除participant时，CF先与媒体平面交互，再生成并发送BYE；需要释放整个组session时，将该BYE过程用于全体participants。收到某个BYE的200后，再与媒体平面交互以释放对应SIP session的媒体资源。单成员的完成响应不替代其余成员的完成。

- §9.2.1.4.4.2全组主动释放与.4.3单成员移除均实际指向6.3.3.1.5，而该条是emergency-group re-INVITE；真正BYE helper为6.3.3.1.4。这里分别列出helper本身和明确调用，不把错误入口静默修复。
- 原文未在此逐字段列BYE寻址/Reason或全部错误恢复，不凭私呼或通用SIP知识增补。公共PF与客户端处理链参见既有释放主题，不据一个200宣称全链原子完成。

依据：§6.3.3.1.4;6.3.3.2.4 step4/response;6.3.3.5.1;9.2.1.4.4.2/.4.3，印刷页 104、124、128、235。

## 不活动与授予重传计时器分开

适用条件：对照24.281 V19.3.0组释放策略的T4(Inactivity)与实际核读24.581 V19.2.0媒体程序；不把计时器编号跨版本自动视为等价。

24.281 §6.3.8.1把媒体报告T4(Inactivity)到期列为组释放条件；24.581 V19.2.0 §6.3.4.3.5实际处理的是T1(Inactivity)，按可配置服务商策略通知应用/信令，并仅在其发起call release时进入Releasing，否则SHOULD重启T1且留Idle。同版24.581的T4在Transmit Taken中监督曾排队请求的Transmission Grant交付，不能把它的授予重传到期当组呼不活动释放。

- 24.581图6.3.4.1-1仍有T4(inactivity)文字，版本内部也有标签差异；本页不将其裁决为某个编号优先，不声称已完成这两个独立版本的集成。
- T5接收不活动、T4计数上限、默认配置等已有独立timer主题，不在本页复制或推导“一段时间无人发流必全组结束”。

依据：§24.281 V19.3.0:6.3.8.1;24.581 V19.2.0:6.3.4.3.5;6.3.4.4.1/.4.2;Figure6.3.4.1-1，印刷页 140、55、58、59。

## 证据边界

- 本主题只覆盖所列普通预安排组呼离开或释放条件；原文错引、计时器名称差异与未核事务恢复不由本页修复。

## 按需继续

- [group-participant-leave](group-participant-leave.md)
- [private-call-server-release](private-call-server-release.md)
- [server-idle-timers](server-idle-timers.md)
- [server-queued-grant-retry](server-queued-grant-retry.md)
- [prearranged-call-setup-result](prearranged-call-setup-result.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[媒体侧 TS24.581 V19.2.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；混合来源按claim的source_references分版追溯，不将媒体页码归给24.281。

- [chat离开与存续的对应条件](chat-release-policy.md)

需要判断紧急状态及TNG2与组时长计时的关系时，见[CF 的紧急状态更新：独立授权、告警分流与 TNG2](emergency-session-control.md)。
