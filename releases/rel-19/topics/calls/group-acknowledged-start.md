# 组呼建立门槛：归属、required应答与最少人数

在网预安排组呼，选定控制功能成立门槛；不是完整组呼状态机。

按各claim区分归属人数与应答计数；不因SIP200便推断所有成员可收听。

## 邀请前先检查归属条件

适用条件：新建组呼，前置授权已通过，普通MCPTT group ID分支。

已归属人数低于on-network-minimum-number-of-affiliated-members，或任一on-network-affiliation-to-group-required成员未归属，回480+112并停止后续。不同于应答人数门槛。

依据：§10.1.1.4.2 step14g(i)。

## 有已归属required成员才启动TNG1

适用条件：控制功能收到建组INVITE，取回组文档中存在已归属且on-network-required成员。

邀请前启动TNG1；值取on-network-timeout-for-acknowledgement-of-required-members。不是TNG3或T4；未给固定秒数。

依据：§6.3.3.3; B.2.1。

## required全部成功仍要达到最少200计数

适用条件：所有已归属required成员已回INVITE200。

停TNG1；受邀成员200计数达到on-network-minimum-number-to-start才回主叫200。无需所有非required成员应答，后者稍后200按加入进行中会话处理。

依据：§6.3.3.3。

## 没有运行TNG1的媒体缓冲分支

适用条件：收到针对§10.1.1.4.1邀请的下游183且P-Answer-State=Unconfirmed，TNG1未运行，控制功能支持media buffering，尚未回主叫final。

构造上游200且仍带Unconfirmed；不能将200统一当全员已接听。本段未列最少200计数前提，保留与一般门槛的分支差异。

依据：§10.1.1.4.2。

## 被邀请者响应计数

适用条件：所选新会话建立/收到被邀者INVITE200。

计数从0开始，收到被邀者200加1；conference NOTIFY可能早于主叫200，不保证整个组会话建立成功。

依据：§10.1.1.4.2 step8;10.1.1.4.1.1。

## 证据边界

- 10.1.1.4.2 p300 required全部响应分支没有重述minimum-number-to-start，6.3.3.3 p149明确有门槛；应保留引用关系，不隐藏差别或生成一套覆盖全部分支的自创状态机。
- 10.1.1.4.2 p300–301另有TNG1未运行、计数等于门槛、支持buffering、未发final的200分支，不能从该段外推无buffering完整策略。
- 临时组/预配置重组涉及non-controlling function required指示与未完成200，未完整整理；不能直接套普通组逐用户计数。
- 配置缺省值/非法组合、重复响应去重、永远凑不够minimum的其他事务退出、媒体/话权实际许可与BYE/CANCEL竞态未核。
- 原文若干引用编号疑义：6.3.3.3生成200指6.3.3.2.2；10.1.1.4.2 step14g(v)写13g(i)。保留不据此生成实现。

## 按需继续

- [group-release-timers](group-release-timers.md)
- [group-acknowledgement-failure](group-acknowledgement-failure.md)
- [../security/group-call-media-boundaries](../security/group-call-media-boundaries.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页149、291、295、296、299、300、709；仅本版本。

- [确认等待前的准入检查](../groups/prearranged-admission.md)
