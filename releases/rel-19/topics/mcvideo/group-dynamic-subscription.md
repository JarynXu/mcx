# 组动态数据订阅：client路由、两层权限与字段冲突

TS24.281 V19.3.0第8章MCVideo在网per-group dynamic data的presence订阅：client经serving/O-PF访问拥有目标组的owner/CF。以普通本地组和所列转发入口为范围，不展开跨系统/gateway、NCF、重组/别名操作、优先业务状态转换、离网或完整IMS/RFC实现。可选数据字段的出现不代表这些扩展业务已核实。

每条claim独立继承本主题common_conditions并叠加自己的conditions，不继承前条成功。本版owner入口存在组ID/用户ID匹配冲突，编码和filter也有拼写/namespace异常，均保留；不把条件条款等同已验证可直接互操作的报文实现。

这里的组动态数据订阅、显式归属结果观察及conference会话状态订阅是不同入口。获取信息不自动建立归属、加入通话或取得媒体许可；不复制显式归属/会议订阅的完整流程。

本页MCVideo ICSI指urn:urn-7:3gpp-service.ims.icsi.mcvideo；public service identity简称PSI。

## 客户端寻址与观察期限

适用条件：MCVideo client要订阅某group ID的动态数据变化，或获取该组当前动态信息，使用8.2.1.6。

client生成初始SUBSCRIBE，Request-URI设serving O-PF的PSI；mcvideo-info中的mcvideo-request-uri设目标group ID，P-Preferred-Service带MCVideo ICSI，Accept含application/pidf+xml，并携带8.3.2的per-group simple-filter且指明该组。当前和后续通知用Expires=4294967295，仅取当前用初始Expires=0。对话内续订仍用4294967295，取消订阅用0，并带PIDF Accept。

- client的SIP目标是PF，不是把group ID或已知conference session identity直接当Request-URI。0在这里表示取当前或取消订阅，不是归属PUBLISH清空请求。
- client主条要求filter指明group ID，而8.3.2.2列出的per-group filter路径没有显式group-ID entity谓词；不自行发明补充字段或可执行filter样例。完整RFC Event/对话/超时处理未展开。

依据：§8.2.1.6，印刷页 177、178。

## PF授权、转发和响应回流

适用条件：O-PF收到发往自身PSI的SUBSCRIBE，mcvideo-request-uri识别不由该server服务的group ID，P-Asserted-Service为MCVideo ICSI且Event=presence；使用8.2.2.2.16转发分支。

PF从mcvideo-request-uri取目标group ID，从PAI的public user identity识别originating MCVideo ID。originator无权进行此订阅时403并停止。通过后基于收到请求生成新SUBSCRIBE，Request-URI设目标组CF PSI，PAI设本PF PSI；mcvideo-info的request-uri仍是group ID，calling-user-id设originating用户ID，并带入其它收到的信令元素后发送。PF转发收到的SUBSCRIBE响应、NOTIFY及NOTIFY响应。

- 此入口限目标组不由该serving server服务的分支；同一节点同时拥有组的处理不由本条推导。PF PSI与真实calling用户ID的两层身份不能互换。
- 入口和部分取字段句的MIME写application/vnd.3gpp.mcvideo-info（缺+xml），生成段则写mcvideo-info+xml；另有SUBCRIBE拼写及重复step4。保留，不静默修正文。
- 生成目标写controlling function，但相邻路由NOTE称terminating function/target user；PSI发现方法未闭合。本页不套conference订阅的session映射、Record-Route或Contact改写步骤。

依据：§8.2.2.2.16，印刷页 195、196。

## owner入口身份冲突

适用条件：对照8.2.2.2.16生成的group动态数据订阅与8.2.2.3.9接收入口，检查group ID、用户ID和filter的一致性。

owner入口除CF PSI、两个mcvideo-info身份字段、MCVideo P-Asserted-Service和presence Event外，还写filter需指明与mcvideo-calling-user-id相同的MCVideo group ID。但PF明确把calling-user-id设为originating用户ID，owner随后的step2也把该字段解释为handled用户MCVideo ID。此版组ID/用户ID要求相互有张力，不能把入口5静默改成与mcvideo-request-uri比较后宣称链路已闭合。

- 这里报告原文冲突，不断言所有实际系统必失败，也不推定group ID和user ID必相同。未查实现/勘误或其它版本，不裁决应采用哪种修正。
- 后续owner响应规则按其原文入口条件分别记录；条件规则可用不等于已完成可互操作报文验证。

依据：§8.2.2.2.16 step4c;8.2.2.3.9 entry5 and steps1–2，印刷页 196、201、202。

## owner期限、组存在和读取授权

适用条件：请求已到达8.2.2.3.9处理范围：CF PSI、group request-uri与user calling-user-id、MCVideo服务标识、presence Event和该段所写per-group filter入口条件均按原文考虑；组/用户字段冲突不在本条修复。

owner从request-uri识别served group ID，从calling-user-id识别handled用户。Expires缺失或非零且小于4294967295时423，Min-Expires=4294967295，并停止。GMS中组不存在或该用户无权订阅该组动态数据，任一成立时403并停止；通过后生成SUBSCRIBE 200，并在订阅期间对信息变化发送8.2.2.3.10通知。

- 这里检查的是dynamic-data订阅权限，本段没有把显式归属owner过程的“必须是组成员”检查直接重写进来；也不据此推断任何非成员天然获准。
- 本段未为403列Warning码，不搬用呼叫或conference的错误码。0不会触发“nonzero且太小”条件，但当前取值/取消的完整RFC行为另依赖引用规范。
- 订阅期间段写served MCVideo ID，通知专段则指served group ID；保留措辞差别。200只说明本订阅处理结果，不是已经送达动态数据或会话接通证据。

依据：§8.2.2.3.9，印刷页 201、202。

## 证据边界

- 组ID/用户ID入口冲突未裁决；本页给出原文可核条件，不保证所有标准字段可无歧义拼成可运行报文。

## 按需继续

- [group-dynamic-notification](group-dynamic-notification.md)
- [conference-subscription](conference-subscription.md)
- [service-authorization](service-authorization.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

## 原文差异与未闭合依赖

- 8.2.2.3.9入口5要求filter的MCVideo group ID等于calling-user-id；PF该字段装originating用户ID，owner step2也将其解释为handled用户。未改成request-uri。
- 8.2.2.2.16入口MIME缺+xml、SUBCRIBE拼写和重复step4；路由主步骤是CF，注释却称terminating function/target user。
- 8.2.2.3.9订阅期间通知对象写served MCVideo ID，下一通知专段是served group ID；RFC编号也有3903[37]等差别，未移用作新处理算法。
- 8.3.1.2叙述groupCallOnoing与schema/filter groupCallOngoing不同；groupStatus schema string与ABNF两值分开记录。
- 8.3.2.2 per-group filter把MCVideo扩展节点/属性写pidf前缀；groupStatus路径取ModifiedBy，affiliated Contact address选项取client属性及status谓词；不静默修XPath或联系人类型。
- per-group filter所列路径不显式嵌入group-ID entity选择，与client和owner入口所称group ID匹配关系未闭合。
