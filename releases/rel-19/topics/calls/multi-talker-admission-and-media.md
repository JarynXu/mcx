# 多talker：容量、授予列表与媒体分发

## 适用范围

- 固定TS24.380 V19.1.0，在网已配置multi-talker的普通组呼；不含dual floor、audio cut-in、广播、ambient listening、紧急/迫近危险或离网。
- 核服务端接口中明确的未满额转交入口及仲裁G状态有限行为；不声称覆盖全部准入、排队后继或配置互通。最大同时talker数及允许名单按已配置值判断，不补schema、默认值或更新生效。
- 按各claim区分当前talker、新请求者、被撤销者和其他talker；授予列表表示许可集合，不是所有成员均收到媒体的证明。

## 配置与入口不是双话权状态机

适用主体：服务端面向参与者接口与floor control arbitration logic（分别说明）。

适用状态：接口U: not permitted and Floor Taken；仲裁者G: Floor Taken。

适用条件：组配置为multi-talker；接口收到Floor Request；未达到最大同时talker数且请求者MCPTT ID位于配置的allowed multi-talkers list时适用转交分支。仲裁者部分以实际收到请求为条件。

multi-talker允许在既有talker不被撤销时增加可发言成员，但同时talker数受配置上限限制。§6.3.5.4.4开头明确：组已配置multi-talker、尚未达到最大同时talker数且请求者MCPTT ID位于允许名单时，接口把请求转交仲裁逻辑并保持U: not permitted and Floor Taken。仲裁者的§6.3.4.4.7a是G状态内专门入口，不引用dual的D状态。一般组配置引用24.481组文档，ad hoc配置引用24.484服务文档；本页不核其字段。

- NOTE 3只限制其后达到上限时的处理，不否定p85未满额允许名单分支。其他准入/不在名单或非该分支的全部结果未在本页展开；不得把条件转交扩成无条件接纳。
- 一般说明允许按配置排队/相对优先级拒绝；本页不把该概述替代具体队列状态机。

依据：3GPP TS24.380 V19.1.0 §4.1.1.2;6.3.5.4.4 opening and NOTE 3;6.3.4.4.7a，印刷页 21、22、66、67、85、86。

## 未满允许并发；满额抢占选最低者

适用主体：controlling MCPTT function中的floor control arbitration logic。

适用状态：G: Floor Taken。

适用条件：收到请求且组已配置multi-talker；分别考虑上限未达到，或已达到且请求有效优先级为pre-emptive。

未达到上限时，允许当前speaker(s)和新请求者同时发送媒体；达到上限且有效优先级为pre-emptive时，从所有有发送许可者中选择优先级最低者撤销。不是固定撤销最早speaker，也不是所有旧talker同时失去许可。

- 上限已满且非pre-emptive的具体结果不由该step补出；不填同优先级择人规则。
- 有效优先级不直接等于请求数字；本页以已判定结果为输入。

依据：3GPP TS24.380 V19.1.0 §6.3.4.4.7a step1，印刷页 66。

## 并发授予更新列表与音频标识

适用主体：controlling MCPTT function中的floor control arbitration logic。

适用状态：G: Floor Taken。

适用条件：7a选择允许当前speaker(s)及请求者同时发送媒体。

给新请求者Floor Granted，Duration装入T2值，包含granted priority、已存关联Track Info（如有）、I-bit=1及服务端生成并保存的全局唯一audio SSRC供该参与者RTP使用；将其MCPTT ID加入当前获准talker列表。向相关non-controlling function及按本地策略监听其RTP的受控参与者发送Floor Taken，带递增1的序号、I-bit=1、获准用户及audio SSRC列表；未请求privacy时带granted identity并可带functional alias，另可带alias列表。为新获准者启动T1；若该Floor Request曾排队，须为该获准参与者启动T20并将C20初始化为1；随后留G: Floor Taken。

- Floor Taken接收集合受本地策略限定，不等于全体成员；SSRC列表不是媒体已收到证明。
- T20/C20动作以该请求曾排队为条件，不推广至未排队请求；此处不证明此前排队到该授予的完整调用链。

依据：3GPP TS24.380 V19.1.0 §6.3.4.4.7a step3，印刷页 66、67。

## 取得许可与媒体分发是不同事件

适用主体：controlling MCPTT function中的floor control arbitration logic。

适用状态：G: Floor Taken。

适用条件：媒体分发器指示已收到permitted MCPTT client的RTP。

非ambient listening时为该参与者启动T2（若尚未运行）；为其重启T1，停止运行中的T20，并请求分发器按本地策略把RTP转给参与者，仍留G: Floor Taken。不能仅凭新增Granted就断言所有监听端已听到该talker。

- 这里只核一般G状态对已获准媒体的处理；不扩为混音、解码、各接收者最大解码路数或dual接收配置。

依据：3GPP TS24.380 V19.1.0 §6.3.4.4.5，印刷页 65。

## 原文差异与适用限制

§6.3.4.4.7a step3a(iii)，印刷页 67：Track Info称关联multi-talker floor control operation状态图；该名称本身不足以建立独立状态机。

## 证据边界

- 有限G状态用途；不是完整multi-talker端到端状态机或配置互通验证。

## 按需继续

- [优先请求：何时触发撤销，为什么队首仍不等于获权](floor-preemption-decision.md)
- [撤销传递：服务端宽限、终端停止请求与交接证据](floor-revoke-observation.md)
- [多talker：逐人退出与满额撤销](multi-talker-release-and-revoke.md)

[3GPP TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅所列版本和条款。
