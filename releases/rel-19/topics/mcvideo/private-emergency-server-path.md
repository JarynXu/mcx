# 私呼紧急更新的服务器路径：两侧PF、CF权限与部分成功

## 适用范围

- TS24.281 V19.3.0（2026-01）；已建立的在网、本地、带 transmission control、直接面向单一 MCVideo ID 的按需私呼，现有 SIP 对话和媒体参数已经存在。排除预建立会话、FTA、功能别名、组呼、远程发起、ambient、离网及无TC私呼。
- 每条声明独立继承共同条件并叠加自身条件，不继承前条成功。请求仅由紧急条件发起者对自身条件操作，不含 originated-by；对端声明观察该请求的接收客户端，不要求接收者等于发起者。本页不建立新私呼，也不执行 BYE。
- 用户 emergency state、私呼优先级 MVEPP、发起私呼状态 MVEPC、私呼告警 MVPEA、CF 的 originating→target 缓存是不同对象。它们不等于组呼 MVEG/MVEGC/MVEA，也不等于媒体发送许可。
- info MIME 指 application/vnd.3gpp.mcvideo-info+xml。规范中的调用编号、组/私呼用词、状态编号及外部媒体规范不一致均保留；本页不提供已闭合的可运行互操作实现。
- 以已有私呼会话为上下文，身份和绑定仍按各 PF 入口重新读取及检查，不预设检查必然成功。CF 升级/取消分别按收到的 emergency-ind 进入；后续动作仅在此前适用检查未拒绝时成立。

## 发起侧 PF 转发与响应顺序

适用条件：O-PF收到服务用户的既有按需私呼re-INVITE。

O-PF可按Resource-Priority拒绝；资源不足/拥塞可500并带Retry-After。继续时从PAI公共用户身份绑定调用用户MCVideo ID并授权，校验媒体，未提供MCVideo视频codec须488。生成下游re-INVITE，写入绑定得到的calling-user-id，带当前媒体SDP并转带收到的Resource-Priority，再转发。下游200触发生成本段200、SDP answer、复制Warning并设置本PF PSI的PAI，先发给客户端，再调用TS24.581媒体面。其它不含SDP的响应连同MIME按主条转发。

- 资源例外只写含emergency indication可选择接受，未限定true，不借组呼缩窄。
- 主条生成helper引6.3.2.1.9，实际对应重INVITE helper为.7；.7仅条件复制resource-lists、info、location MIME。不把缺失目标列表自动补成已知对端。
- 主条未在此列绑定缺失404/141，不从初始INVITE流程搬入。

依据：§10.2.2.3.1.3;6.3.2.1.7，印刷页 94、339、340。

## 终接侧 PF 绑定与响应顺序

适用条件：T-PF收到既有按需私呼re-INVITE。

T-PF资源不足/拥塞可500并带Retry-After，含emergency indication时可选择接受。从info的mcvideo-request-uri取用户ID查绑定；绑定不存在则404停止。按6.3.2.2.10生成re-INVITE，保留相关MIME和收到的Resource-Priority，带当前媒体SDP并发送；不改变answer-mode。收到客户端200后生成本段200和基于收到SDP的answer，PAI置本PF PSI，先调用TS24.581，再向上游转发。其它不含SDP的响应按信令路径转发。

- 不要把XML mcvideo-request-uri等同SIP Request-URI；本条只说绑定不存在404，未重复expiry或Warning。
- O-PF先发200后媒体、T-PF先媒体后发200，不能合并为统一顺序。

依据：§10.2.2.3.3;6.3.2.2.9–10，印刷页 101、102、342、343。

## CF 的参数和权限检查

适用条件：CF分别收到emergency=true升级或emergency=false取消请求。

两主条先要求SDP至少一个媒体流的参数及至少一个codec/format可接受，否则488停止。实际校验helper6.3.3.1.16要求emergency=true时无imminentperil且有alert；false时无imminentperil，alert可有可无；无效403/150。实际.12.2私呼授权要求allow-emergency-private-call=true及UsePreConfigured含目标或LocallyDetermined。实际.12.4取消私呼许可要求allow-cancel-private-emergency-call=true；false或缺失均未授权。告警及告警取消另按.12.1私呼目标规则、.12.3判断。

- 主条校验引.17、授权引.13.x，实际标题为.16和.12.x；分开记录，不声称引用链已修好。
- CF告警发起须allow-activate-emergency-alert=true及PrivateEmergencyAlert的UsePreConfigured含目标或LocallyDetermined；告警取消.12.3只列true/false，未给缺失默认值。与私呼取消的明确缺失拒绝不同。

依据：§10.2.2.4.3–4;6.3.3.1.12.1–4;6.3.3.1.16，印刷页 110、111、112、115、116、347、348、349。

## 升级状态、告警缓存及下游输入

适用条件：CF 已进入升级主条，emergency=true；后续缓存和发送仅在此前适用检查通过后执行。

主条在未授权时403停止；若收到紧急Resource-Priority但既非获准请求、调用用户也不处于与目标用户的in-progress emergency private call状态，同样403。若此前不在该定向状态，先缓存calling→target为in-progress；仅同时alert=true且另获准时缓存已向目标发告警。随后向收到resource-lists中的目标用户发送升级re-INVITE。对应发送主条10.2.2.4.5复制info、按许可置emergency=true；无告警或告警请求被拒时置alert=false，要求紧急Resource-Priority；对下游200缓存Contact。

- 接收主条目标引用11.1.1.4.5；发送主条反引11.1.1.4.3，实际私呼编号在10.2.2.4。目标resource-lists要求在客户端升级主条未明确生成，是必要链路缺口。
- 发送主条先调用.9，而.9是组呼取消helper，含normal组优先级和emergency=false；随后又设true/紧急。不推导覆盖顺序能消除冲突。
- 告警填充引.12而该处为授权章节；优先级取值引.19而实际.18取配置。接收§10.2.2.4.3 step4把授权回指step2，而该step2是校验；发送§10.2.2.4.5 step4也回指step2，而其step2是复制info。两处均未静默修正。
- 缓存动作在下游成功之前，不能当对端已接受；已存在状态时不反推刷新告警缓存。
- 主条未授权403引.14，实际拒绝helper .13要求emergency=false、alert=false；.14是imminent-peril re-INVITE。保留调用与实际内容差别。

依据：§10.2.2.4.3;10.2.2.4.5;6.3.3.1.9;6.3.3.1.13;6.3.3.1.18–19，印刷页 108、114、116、117、118、347、348、350。

## 取消通话条件与告警分别处理

适用条件：CF收到本人取消emergency=false请求；不含originated-by。

未获准取消须403并带emergency=true；若请求alert=false且告警取消未获准，再带alert=true。即使获准，收到紧急Resource-Priority值也须403停止。通过后清发起者对目标的紧急私呼缓存；只有请求alert=false且告警取消获准时才清发送者的outstanding alert缓存。主条另向resource-lists中的目标发送取消re-INVITE。10.2.2.4.6复制info、获准时置emergency=false；请求取消告警但不获准时置alert=true，要求normal私呼Resource-Priority；下游200缓存Contact。

- 本条拒绝时带alert=true的条件是告警取消未获准，不是组呼主条的outstanding-alert条件。
- 接收/发送主条分别错引11.1.1.4.6/.4；发送还调用组呼取消.9及取值.19。不把同名调用视为完整私呼报文生成器。
- 清私呼状态不等于清所有用户emergency或告警状态；不是BYE。

依据：§10.2.2.4.4;10.2.2.4.6;6.3.3.1.12.3–4;6.3.3.1.9;6.3.3.1.18–19，印刷页 108、111、112、116、117、118、348、349、350、351。

## CF 的部分成功与延后结果

适用条件：本次升级/取消的下游200及对应的后续ACK处理，各事件须满足本节所列当时条件；另述INFO helper仅在其自身入口成立时适用。

CF收到下游200且尚未向邀请客户端发送响应时，生成本段200和SDP answer。升级中的alert=true未获准，或取消中的alert=false未获准时，在200带Warning149。原文先调用TS24.380媒体面，再向发起者发200。主条在收到对应带149的200之ACK后调用6.3.3.1.18；该号实际是Resource-Priority取值，不是INFO生成。另行核得6.3.3.1.17描述INFO字段与对话：它带g.3gpp.mcvideo-info及info MIME，告警发起被拒为emergency=true/alert=false，告警取消被拒为alert=true，并在邀请者对应对话发送。本页不把该独立helper补接成已闭合的ACK→INFO链。其它不含SDP的响应连同MIME向发起侧转发。

- 主条ACK后调用.18，实际.18取Resource-Priority配置，INFO在.17；保持双重定位。
- 200可能只是通话升级/取消成功，告警被拒；不能将NOTE笼统的接受确认凌驾于149条件。
- CF成功段写24.380，T-PF/对端成功段写24.581。本页不替换，不核24.380算法，也不宣称媒体链闭合。
- 取消200的SDP answer要求回指6.3.3.2.2，但该条是Receipt of a SIP INVITE request；SDP answer generation标题实际在6.3.3.2.1。保留生成SDP answer的义务，不把.2.1自动代入或声称answer算法已闭合。

依据：§10.2.2.4.3–4 response/ACK paragraphs;6.3.3.1.17–18;6.3.3.2.1–2，印刷页 116、122、123、348、349、350。

## 证据边界

- 本页描述24.281明列的职责和成功证据，不补目标列表生成、SIP缺口、外部媒体或安全算法；本地成功不等于全链互通。

## 按需继续

- [MCVideo 私呼服务器链：身份准入、终接设置与逐段应答](private-call-server-admission.md)
- [MCVideo 私呼逐段释放：PF、CF的BYE处理与引用边界](private-call-server-release.md)
- [私呼紧急升级：目标许可、待确认状态与告警结果](private-emergency-client-upgrade.md)
- [私呼本人取消：通话、告警与用户状态分开处理](private-emergency-client-cancellation.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。
