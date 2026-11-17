# 多talker：逐人退出与满额撤销

## 适用范围

- 固定TS24.380 V19.1.0，在网已配置multi-talker的普通组呼；不含dual floor、audio cut-in、广播、ambient listening、紧急/迫近危险或离网。
- 核服务端接口中明确的未满额转交入口及仲裁G状态有限行为；不声称覆盖全部准入、排队后继或配置互通。最大同时talker数及允许名单按已配置值判断，不补schema、默认值或更新生效。
- 按各claim区分当前talker、新请求者、被撤销者和其他talker；授予列表表示许可集合，不是所有成员均收到媒体的证明。

## 一个talker退出不必使全组空闲

适用主体：controlling MCPTT function中的floor control arbitration logic。

适用状态：G: Floor Taken。

适用条件：收到Floor Release；multi-talker支持成立。

请求分发器停止转发相关RTP，停止该参与者运行中的T2/T20；发送Floor Release Multi Talker，SSRC及User ID指向退出者，将其从当前获准列表移除。列表仍非空则留G: Floor Taken，空则引用6.3.4.3.2进入G: Floor Idle。

- 进入Idle仅保留调用，不宣称下一位排队者已获授予；6.3.4.3.2的queueing外层未消除。
- 服务器请求停止转发不证明终端停采音或接收端缓冲已清。
- 本handler未列stop T1，不能从其他释放或超时条款补入。

依据：3GPP TS24.380 V19.1.0 §6.3.4.4.6，印刷页 65。

## 一个talker断流只移除该许可项

适用主体：controlling MCPTT function中的floor control arbitration logic。

适用状态：G: Floor Taken。

适用条件：某一talker的T1到期；multi-talker支持成立。

停止该参与者运行中的T2/T20；在multi/non-multi分流之前，共同step3要求分发器停止转发该超时者RTP，但媒体缓存存在时，缓冲中的RTP除外。multi分支向除该超时参与者外的所有参与者发送含其SSRC和MCPTT ID的Floor Release Multi Talker，并将其从当前获准列表移除。列表非空留G: Floor Taken，空则调用6.3.4.3.2进入G: Floor Idle。

- 停止相关RTP转发有服务端媒体缓存例外，不能等同于清空所有接收端缓冲或已交付音频。
- 不把超时等同全体talker退出，也不补下一位队列授予。

依据：3GPP TS24.380 V19.1.0 §6.3.4.4.3，印刷页 64。

## 满额撤销先排队而非立即替换

适用主体：controlling MCPTT function中的floor control arbitration logic。

适用状态：G: Floor Taken → G: pending Floor Revoke。

适用条件：7a上限达到且有效pre-emptive；选择撤销最低优先级talker。

停止被撤销者运行中的T1/T20，以cause 4调用6.3.4.5.2撤销；新请求者插入队首或移到队首。仅其协商queueing时发送队列位置/优先级并按请求有无带回Track Info。进入pending时发Revoke，multi组带相应Floor Indicator，启动该被撤销者的T3。此分支不等于已向新请求者发送Granted。

- 不增加7a未列的stop T2。
- 旧priority主题仅作关联阅读，其单话权共同前提不继承到本页；本页新增从多许可集合选择最低者，其他talker未因此被全撤。
- 不借6.3.4.3.2矛盾queueing外层闭合后续新授予。

依据：3GPP TS24.380 V19.1.0 §6.3.4.4.7a step2;6.3.4.5.2，印刷页 66、67、71。

## 撤销等待中其他talker可独立退出

适用主体：controlling MCPTT function中的floor control arbitration logic。

适用状态：G: pending Floor Revoke。

适用条件：multi-talker已配置；收到没有被发Revoke的参与者Floor Release，或没有被发Revoke者的T1到期。

在G: pending Floor Revoke中，收到未被发送Revoke的其他参与者Floor Release时，要求分发器停止相关RTP，停止其运行中的T2/T20，发送指向该参与者的Floor Release Multi Talker并从获准列表移除；列表空进入G: Floor Idle，非空则原文写stay in G: Floor Taken。另一个独立入口是未被发送Revoke者的T1到期：同样停止相关RTP、停止其运行中的T2/T20、发送指向该参与者的Floor Release Multi Talker并移除；该T1分支明确保持G: pending Floor Revoke。两个入口的状态出口不同，不能因都处理其他talker而合并。

- Release分支位于pending上下文却写stay Taken，保留字面差异，不改成pending。
- 两个分支均未写停止被撤销者T3，Release分支也未列stop T1；不从未列动作推出T3必然持续或状态不变。
- 不套到被撤销者自己的Release/T1或T3出口，不推导新请求者已获授予。

依据：3GPP TS24.380 V19.1.0 §6.3.4.5.4 second branch;6.3.4.5.6 second branch，印刷页 72、73。

## 原文差异与适用限制

§6.3.4.5.4 second branch，印刷页 72：pending上下文的其他人Release分支，列表非空写stay G: Floor Taken；与其他人T1到期保持pending不同，保留不裁决。

## 证据边界

- 有限G状态用途；不是完整multi-talker端到端状态机或配置互通验证。

## 按需继续

- [优先请求：何时触发撤销，为什么队首仍不等于获权](floor-preemption-decision.md)
- [撤销传递：服务端宽限、终端停止请求与交接证据](floor-revoke-observation.md)
- [多talker：容量、授予列表与媒体分发](multi-talker-admission-and-media.md)

[3GPP TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅所列版本和条款。
