# 私呼紧急升级：目标许可、待确认状态与告警结果

## 适用范围

- TS24.281 V19.3.0（2026-01）；已建立的在网、本地、带 transmission control、直接面向单一 MCVideo ID 的按需私呼，现有 SIP 对话和媒体参数已经存在。排除预建立会话、FTA、功能别名、组呼、远程发起、ambient、离网及无TC私呼。
- 每条声明独立继承共同条件并叠加自身条件，不继承前条成功。请求仅由紧急条件发起者对自身条件操作，不含 originated-by；对端声明观察该请求的接收客户端，不要求接收者等于发起者。本页不建立新私呼，也不执行 BYE。
- 用户 emergency state、私呼优先级 MVEPP、发起私呼状态 MVEPC、私呼告警 MVPEA、CF 的 originating→target 缓存是不同对象。它们不等于组呼 MVEG/MVEGC/MVEA，也不等于媒体发送许可。
- info MIME 指 application/vnd.3gpp.mcvideo-info+xml。规范中的调用编号、组/私呼用词、状态编号及外部媒体规范不一致均保留；本页不提供已闭合的可运行互操作实现。
- 本次升级发起前为 MVEPC1、MVEPP1、MVPEA1；这是发起条件，不要求后续响应或 INFO 处理时仍处于初始状态。后续事件按各声明所列当时状态判断。请求不附带告警，或所附告警已在客户端获准；其它告警组合不在本页请求主线内。

## 客户端针对目标检查权限

适用条件：客户端按6.2.8.3.1.1及.1.3判断该目标。

紧急私呼许可要求 allow-emergency-private-call=true，且 PrivateCall/EmergencyCall/MCVideoPrivateRecipient 的 entry-info 为 UsePreConfigured 并列出目标用户，或为 LocallyDetermined；其它情况未授权。附带私呼告警另要求 allow-activate-emergency-alert=true，且 OnNetwork/PrivateEmergencyAlert 使用同样的目标选择规则。两种权限不能互代。

- 10.2.2.2.5 不像组呼主条先列明确的未授权 SHOULD告知/停止步骤；本页仅描述获准入口，不借组呼补失败动作。
- 只读取24.281使用的profile字段，不展开24.484规则求值。

依据：§6.2.8.3.1.1;6.2.8.3.1.3，印刷页 77、78。

## 升级请求与待确认状态

适用条件：用户请求升级，已获紧急私呼许可；满足本主题初始状态和告警选择。

10.2.2.2.5生成re-INVITE，调用6.2.8.3.2设置用户emergency state、emergency-ind=true、MVEPC2；请求且获准告警时带alert-ind=true、MVPEA2并执行紧急告警位置trigger，未请求告警时带false。原文将非MVEPP2的优先级状态置为“MVEPP3: confirm-pending”。请求另带按6.2.8.3.3选择的Resource-Priority和当前媒体参数SDP，若需implicit transmission request按6.4指示，再发送。

- G.10表把confirm-pending列为MVEPP4，把3列为cancel-pending；正文.2和.5却写3。保留冲突，不把3静默修成4。
- 6.2.8.3.3的紧急优先级条件与normal条件可能重叠：已获准MVEPC2/3或MVEPP2要求紧急值，而授权取消或MVEPP1/3要求normal；不裁决重叠优先级。
- 请求告警但本地未获准时.2没有完整alert填值分支；不据此造false默认值或可运行报文。

依据：§10.2.2.2.5;6.2.8.3.2–3;G.10，印刷页 78、331、635。

## 响应和独立告警结果

适用条件：收到本次升级最终响应；INFO仅按6.2.8.3.7自身入口判断。

升级2xx先调用原文所列TS24.380用户面，再调用.4：MVEPC2/3时将MVEPP置2、MVEPC置3；MVPEA2且无Warning149才由此将MVPEA置3。4xx/5xx/6xx按.5，在MVEPC2/3条件下置MVEPC1，若为原文“MVEPP3: confirm-pending”则置1；原请求alert=true时置MVPEA1。以下 INFO 行为只陈述 §6.2.8.3.7 的独立入口，不证明主条的 group-session 入口已分派到此。该私呼对话内 INFO 须含g.3gpp.mcvideo-info包、关联info MIME及至少一个alert/emergency/imminentperil指示；MVPEA2时alert=false/true分别置1/3。

- 主条INFO入口写识别ongoing group session，与实际helper的private-call dialog不同；只并列两处，不宣称入口无歧义。
- 该私呼INFO helper未列组呼helper的“先回200”步骤，也没有MVEPC3门槛；不移植组呼处理顺序。
- 24.380引用按原文保留，未验证或替换成24.581；2xx不证明RTP开始或媒体许可。错误段未规定恢复用户emergency state。

依据：§10.2.2.2.5 response paragraphs;6.2.8.3.4–5;6.2.8.3.7，印刷页 79、80、81、331。

## 证据边界

- 状态编号、INFO入口与媒体引用存在规范缺口。

## 按需继续

- [MCVideo 按需私呼：客户端邀请、应答与接通证据](private-call-client-signalling.md)
- [私呼本人取消：通话、告警与用户状态分开处理](private-emergency-client-cancellation.md)
- [私呼紧急更新的服务器路径：两侧PF、CF权限与部分成功](private-emergency-server-path.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。
