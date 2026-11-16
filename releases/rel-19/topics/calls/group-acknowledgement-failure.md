# TNG1到期与required提前拒绝怎么处理

在网预安排组呼，选定控制功能成立门槛；不是完整组呼状态机。

按各claim区分归属人数与应答计数；不因SIP200便推断所有成员可收听。

## 到期但人数不足还要等待

适用条件：TNG1已到期。

计数不足minimum-number-to-start仍等待更多200，达门槛后才执行超时策略；不能称到期必立即失败或必立即接通。

依据：§6.3.3.3。

## 达到门槛后的proceed与abandon

适用条件：TNG1到期且200计数达到启动门槛。

on-network-action-upon-expiration-of-timeout-for-acknowledgement-of-required-members=proceed：媒体处理后发200+111；abandon：480+112，对confirmed dialog发BYE并媒体处理，对non-confirmed发CANCEL。

依据：§6.3.3.3。

## required提前失败的另一分支

适用条件：TNG1正在运行，已归属required成员对受邀INVITE回4xx/5xx/6xx。

TNG1到期前收到已归属required成员的4xx/5xx/6xx时，策略不继续则停表并转发原final附112。策略继续且200计数已达门槛时，其余全部受邀客户端尚未全响应则继续TNG1；其余全部受邀客户端都回200则停表并完成媒体处理后回200+111。这里的其余不限required集合，且不是超时abandon的480分支。

依据：§6.3.3.3。

## 证据边界

- 10.1.1.4.2 p300 required全部响应分支没有重述minimum-number-to-start，6.3.3.3 p149明确有门槛；应保留引用关系，不隐藏差别或生成一套覆盖全部分支的自创状态机。
- 10.1.1.4.2 p300–301另有TNG1未运行、计数等于门槛、支持buffering、未发final的200分支，不能从该段外推无buffering完整策略。
- 临时组/预配置重组涉及non-controlling function required指示与未完成200，未完整整理；不能直接套普通组逐用户计数。
- 配置缺省值/非法组合、重复响应去重、永远凑不够minimum的其他事务退出、媒体/话权实际许可与BYE/CANCEL竞态未核。
- 原文若干引用编号疑义：6.3.3.3生成200指6.3.3.2.2；10.1.1.4.2 step14g(v)写13g(i)。保留不据此生成实现。

## 按需继续

- [group-release-timers](group-release-timers.md)
- [group-acknowledged-start](group-acknowledged-start.md)
- [../security/group-call-media-boundaries](../security/group-call-media-boundaries.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页149、150、151；仅本版本。
