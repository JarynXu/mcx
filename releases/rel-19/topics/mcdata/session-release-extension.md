# MCData 会话释放预告：剩余量、TDC3 与延期决定

TS24.282 V19.7.0 §13.2.4.1–.4，已有普通在网 on-demand SDS session，由服务器按配置选择通知通信发起者。不是 HTTP FD 的 MESSAGE 分支，也不覆盖授权第三人释放或紧急状态。

在对应 MCData communication 的 SIP dialog 内处理 INFO。各入口所需 Info-Package、与包关联的 MIME 类型及 COMMUNICATION RELEASE 类型均须满足；同对话本身不能替代这些条件。

SIP200只按其对应事务判断。剩余量是辅助决策资料，延期请求是用户选择，延期决定由CF按本地策略和已有资料给出；不得合并为一个“延长成功”。

## 释放预告不是最终释放

适用条件：服务器已选择 §13.2.4 的有预告释放，并向通信发起者发送 intent。

CF 在会话对话内发送 INFO，Info-Package 为 g.3gpp.mcdata-com-release，以关联的 mcdata-signalling MIME 携带 COMMUNICATION RELEASE，Comm Release Information type 为 INTENT TO RELEASE，Content-Disposition 为 Info-Package。需要更多资料时才加入 REMAINING AMOUNT OF DATA 查询；Reason 可加入而非必带。客户端满足同对话、包及关联 MIME 条件后解码，遇到此类型先回200，再按查询条件处理补充信息；这一 INFO/200 本身不是最终 BYE 或媒体已释放。

- §13.2.4.2.1 step3 的通知/展示原因带有 Reason 存在条件；不把本页所有无 Reason 请求一概补成相同 UI 行为。
- 无预告释放的CF要求Reason与这里CF MAY加Reason不同；不从一个分支覆盖另一个。
- 预告适用范围在 §13.2.4.1 列 SDS 和 FD using media plane；不能只凭 §13.2.3 还包括 IPCONN，就把本分支扩大到 IPCONN。

依据：§13.2.4.1;13.2.4.4.1;13.2.4.2.1 opening,steps1,2;15.1.10.1;15.2.19/.20，印刷页 332、333、334、335、357、358、371。

## INFO与200的逐段转发

适用条件：PF 在对应会话对话内，从 CF 或客户端收到 Info-Package=g.3gpp.mcdata-com-release 的 INFO。

PF 为另一侧生成 INFO，复制 Info-Package 和 MIME bodies，并在相应通信对话内发送。收到另一侧对出站 INFO 的200后，PF才为入站 INFO生成并返回200。CF发起预告/结果与客户端发起延期请求使用不同方向，但均有这一分段处理；PF返回200不能单独证明CF已接受延期或已执行最终释放。

- 复制仍须遵守已有的 MIME 处理/保护规则；本页不把这一句当成密文可任意透传的许可。
- 本 helper 明列复制包和 MIME bodies，却未明列复制 Reason；相较无预告 BYE 的显式 Reason 复制要求，本页不保证 CF 的可选原因在所有段都已保真到达，也不据缺此步骤断言必须丢弃。
- 本小节给出200处理，未在这里补齐4xx/5xx/6xx或超时的转发/回收算法。

依据：§13.2.4.3.1/.2，印刷页 334。

## 剩余字节资料不是延期请求

适用条件：客户端收到符合 §13.2.4.2.1 入口的 INTENT TO RELEASE，且 Data query type 存在并为 REMAINING AMOUNT OF DATA。

客户端 SHALL 回传 DATA PAYLOAD：Number of payloads=1，Payload content type=TEXT，内容为尚待发送的数据字节数；它用 mcdata-payload MIME 和 Content-Disposition=Info-Package，在同一通信对话内以 INFO 发往 PF。CF 在同对话、对应包和关联 mcdata-payload MIME 的入口解码，按 Number of payloads 遍历并保存各 Payload，关联到正在进行的通信。它不是发送剩余业务数据本身，也不是 EXTENSION REQUEST；仅保存资料的 §13.2.4.4.2 未列停止 TDC3 或批准延期。

- 客户端生成补充资料 INFO 的步骤未明列设置 Info-Package，而 PF 的 §13.2.4.3.2 和 CF 的 §13.2.4.4.2 均要求该包。保留此接口条件缺项，不声称按已列生成步骤即可完整通过后续入口。
- §13.2.4.4.2 未明列对补充资料 INFO 回200；PF的相应200又以收到下游200为触发。不从邻近延期请求的应答步骤替它补出响应。
- 字节数的文本语法、采样时刻与媒体进度一致性未在这些条款细化；不把这个TEXT当成已核的媒体余额真值。

依据：§13.2.4.2.1 step2c and DATA PAYLOAD generation;13.2.4.4.2;15.1.4.1，印刷页 333、335、353。

## TDC3的起止及到期

适用条件：CF 已发预告 INFO，并收到对应200；或相应 TDC3 到期。

CF收到预告的200后才启动 TDC3（request for extension），不是发出预告即开始，也不是收到剩余量资料才开始。F.2.2 给出的默认值为15秒且可配置；若在CF收到延期请求前到期，§13.2.4.4.1 要求按 §13.2.2.2.4.4 释放，计时表称立即释放。这里的“立即”是进入释放动作的时点，不是全部参与者在同一瞬间完成BYE/200。

- 15秒是默认可配置值，不是用户读完预告后保证得到的完整人工反应窗口。
- TDC3与每条消息回执TDC1、文件可用期TDC2不同；不能复用后两者的停止条件或默认值。
- 尚未收到预告200、延期请求与到期竞态、延期结果INFO丢失等情况的额外恢复未在本链细化，不自行补新的默认接受/拒绝。

依据：§13.2.4.4.1 final paragraphs;13.2.2.2.4.4;F.2.2 TableF.2.2-1 TDC3，印刷页 329、335、639。

## 延期请求200不等于批准

适用条件：用户因服务器预告而请求延长通信，客户端进入 §13.2.4.2.2；CF收到符合关联对话/包/MIME条件且类型为 EXTENSION REQUEST 的 INFO。

客户端在同一通信对话内发送 INFO，明确带 g.3gpp.mcdata-com-release、关联 mcdata-signalling MIME、Content-Disposition=Info-Package，并将 COMMUNICATION RELEASE 类型设为 EXTENSION REQUEST。CF识别后停止 TDC3，回200，然后另按 §13.2.4.4.4 发送延期决定。因此这个200证明的是请求处理分支已响应，不能替代后续 ACCEPTED/REJECTED 业务决定。

- 用户可请求延期不等于必须请求；补报剩余字节数与用户请求延期是不同动作。
- 本步骤未规定扩展时长、额外可发字节数或TDC3重新启动；不把停止等待计时器解释成无限期续用许可。

依据：§13.2.4.2.2;13.2.4.4.3;15.2.20，印刷页 333、335、371。

## 延期决定及拒绝后的释放

适用条件：CF 已收到延期请求，进入 §13.2.4.4.4 生成并发送决定。

CF结合本地策略与已保存的剩余量资料作出接受或拒绝决定，用新的会话内 INFO 发送 COMMUNICATION RELEASE，类型为 EXTENSION RESPONSE，包、mcdata-signalling MIME及Content-Disposition保持本过程要求。该过程写接受时填 ACCEPTED、拒绝时填 REJECTED；客户端在符合入口并识别 EXTENSION RESPONSE 后，先回200，再按 Extension Response Type 通知用户。若CF决定拒绝，它在收到这个结果INFO的200后才调用释放 helper；不是一收到延期请求、回该请求200或发出REJECTED就已完成最终释放。

- §13.2.4.4.4 生成段把决定字段称为 extension request type，但客户端、消息表及 §15.2.21 标题称 Extension response type；后者用途段也沿用request字样。保留命名不一致，不能宣称完整编码互通已验证。
- 消息表把 Extension response type 列为可选，§15.2.21 又限定只在 EXTENSION RESPONSE 时使用，其他类型可忽略。此处依据过程分支判断结果，不为缺项、保留值或错误类型补出接受默认值。
- ACCEPTED表示本次延期决定获准；本段未规定具体延长量、再次预告或新计时周期，也不构成剩余全部SDS送达保证。
- 本段未给出结果INFO无200时的另一释放时限；不将TDC3已停之后的行为从到期分支推补。

依据：§13.2.4.4.4;13.2.4.2.3;15.1.10.1;15.2.21，印刷页 333、335、336、357、358、371、372。

## 证据边界

- 只核正常有效消息下的主干及明确计时条件；保留补充资料INFO的包/应答缺项，不声称该可选分支已完成互通闭环。
- 没有全员回执门槛、全组同步结束时刻或所有SDS消息回滚算法。最终BYE与具体媒体释放仍接已有主题和未核24.582接口。

## 按需继续

- [session-server-release](session-server-release.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§13.2.4.2.1 step2c;13.2.4.3.2;13.2.4.4.2：补充剩余量INFO的生成未明列Info-Package设置，而后续PF/CF入口要求g.3gpp.mcdata-com-release；CF资料接收段未明列200应答，PF应答段却以收到200为条件。 记录可选资料回传分支的具体接口缺项，不从延期请求或RFC常识无声补足。

§13.2.4.4.4;13.2.4.2.3;15.1.10.1;15.2.21：CF生成过程使用extension request type一词，消息表/客户端/IE标题使用Extension response type；IE用途文字也夹有request。 保留同一接受/拒绝决定的可核语义与字面名称差异，不自行创造新IE，也不声称编码问题已被修复。

§13.2.4.4.1;13.2.4.3.1;13.2.4.2.1 step3 versus13.2.3.2.3：预告CF可带Reason、客户端有原因展示步骤，但中间PF INFO转发明列复制项仅包和MIME；无预告BYE反而明确要求复制Reason。 不保证可选原因跨所有INFO段已由这些条款保证，也不反推PF必须删除Reason。
