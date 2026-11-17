# 独立紧急告警取消：本人、他人及不同成功证据

TS24.281 V19.3.0，在网、本系统预安排MCVideo组的独立紧急告警取消；无ongoing组会话，且本次只请求取消告警，不携emergency-ind。排除地理告警、临时组、跨系统、网关、别名与通话内re-INVITE。

请求用户已获服务授权且已归属目标组；未归属/N2处理不在本页。每条声明按自身客户端、PF、CF或接收者事件适用，不预设后续授权成功、目标绑定存在或通知已送达。

MVEA告警状态、用户emergency state、组MVEG/MVEGC及CF告警缓存分别判断。本页保留授权错引、通知生成错引和client-id匹配缺口，不宣称可直接拼成无歧义互操作实现。

## 本人或他人的告警，分别填写取消对象

用户请求取消指定组的告警；客户端执行§11.2.1.2与§6.2.8.1.6。

客户端按调用用户profile中ruleset/rule/actions的allow-cancel-emergency-alert=true判断获准，其它情况未获准。获准才构造独立MESSAGE：P-Preferred-Service与Accept-Contact使用MCVideo ICSI，后者带require/explicit；P-Preferred-Identity可选。info中的mcvideo-request-uri为组ID、alert-ind=false；取消另一用户发起的告警时另带originated-by，值为原告警发起者MCVideo ID。SIP Request-URI使用原文所称服务group identity的PF PSI。仅在本次请求不含originated-by时把本端MVEA置4 cancel-pending，然后发送。

- 本页不附带取消组紧急状态，故不进入step5的emergency-ind=false构造。本人和他人分支不额外引入其它服务的any-user许可字段；本版所列客户端条款没有该条件。
- §11.2.1.2未单列未授权时的提示或响应，不从其它服务补造。取消构造也没有明确列mcvideo-client-id，但后续回执要求匹配原请求client-id；不能静默添加完整模板或声称关联已闭合。
- 本条不在发送时清用户emergency state；他人取消请求不因这个发送步骤改变请求者自己的MVEA。

依据：§11.2.1.2 opening,steps1-8; 6.2.8.1.6 cancellation paragraph，印刷页 68,370。

## PF转发之后，CF按alert=false进入取消处理

O-PF收到服务用户的emergency-notification MESSAGE，或CF收到其对应分类的MESSAGE；各自前置检查未拒绝才继续。

O-PF从PAI的公共用户身份确定并授权调用用户，确定目标组CF PSI，将info复制到新MESSAGE并将calling-user-id置为绑定识别出的调用用户ID，PAI改为本PF PSI后发送。CF分类允许info中出现emergency-ind或alert-ind；§11.2.3.1先检查资源、MCVideo ICSI及组preconfigured-group-use-only限制，随后step3遇alert-ind=false即调用§11.2.3.2并停止该主条余下步骤。该分派没有要求ongoing会话或同时携emergency-ind。

- O-PF/CF资源不足或拥塞可500并可带Retry-After；针对alert=true的接受例外不自动用于本次false请求。CF缺ICSI须403，组preconfigured-group-use-only=true须403/Warning168。
- 已归属条件避开O-PF隐式归属错引；CF PSI发现、完整身份失败处理及SIP错误转发仍依赖外部/未闭合条款。O-PF成功响应段称step10发送，但实际发送在step12，不能以改号掩盖。
- 这是实际caller到取消handler的证据，不表示下一步权限检查或端到端处理已经成功。

依据：§6.3.1.2 emergency notification classification; 11.2.2.1 steps1-12,response paragraphs; 11.2.3.1 steps1-3，印刷页 84,374,375,376,377。

## CF分别拒绝取消或清除指定发起者的告警缓存

CF进入§11.2.3.2且alert-ind=false，不含emergency-ind；分别按该handler判定告警取消未授权或已授权。

未授权分支返回403并携alert-ind=true，然后停止。已授权时，有originated-by就清该ID的outstanding alert缓存；没有则清发送者ID的缓存。因本次不含emergency-ind，CF对每个已归属但未加入会话的成员生成取消通知，保留calling-user-id，有originated-by则复制，并设alert-ind=false。之后发送本请求的200，再发送独立成功接收指示，带alert-ind=false、alert-ind-rcvd=true，并回带原请求client-id。没有等待全部下游2xx才发200或回执的明确屏障。

- handler两处告警取消授权均引6.3.3.1.13.1；实际取消授权标题及内容在6.3.3.1.12.3。后者按调用用户ruleset的allow-cancel-emergency-alert true/false判定，未给缺失默认值；不把此定位当修好caller，也不把客户端actions层级自动等同服务器。
- 通知生成引.11，实际.11是发起告警内容填充且置alert=true；通知生成器在.10。回执生成引.20，实际.20是地域进出通知；成功接收生成器在.19。保留主条明确的false及发送职责，不编造调用覆盖顺序或已修好的报文。
- 本分支清的是选定发起者的告警缓存，不清所有用户告警或组in-progress emergency，也不是BYE。无ongoing是本页业务范围，handler的此无emergency-ind分支自身不以会话存在为前提。

依据：§11.2.3.2 opening,1a,2a-c,2e-k,response paragraph，印刷页 378,379,380,381。本handler明列的条件、缓存、通知和回执；包括原文所写.13.1/.11/.20调用字符串。

依据：§6.3.3.1.12.3，印刷页 111,112。comparison-only：实际取消权限helper，不作为自动修复handler错引。

依据：§6.3.3.1.13，印刷页 114。comparison-only：实际.13为priority拒绝响应段，并非主条所引.13.1权限条款；不用于本页执行算法。

依据：§6.3.3.1.10; 6.3.3.1.11 opening,step1，印刷页 108,109。comparison-only：区分通知生成与发起告警内容填充，保留后者alert=true与主条取消false的差别。

依据：§6.3.3.1.19; 6.3.3.1.20，印刷页 117,118。comparison-only：区分成功接收与地域进出通知生成，不代换调用者。

## 本人取消依匹配回执改变状态，200不能替代回执

客户端已发送§11.2.1.2请求；本条分别处理满足client-id匹配条件的接收指示，或该请求的4xx/5xx/6xx。

接收指示须alert-ind-rcvd=true且client-id匹配原请求。原请求无originated-by时，收到alert=false将MVEA置1 no-alert并清用户emergency state；收到alert=true且当前MVEA4则恢复MVEA3。对于本人的4xx/5xx/6xx，若含alert=true且当前MVEA4，或响应不含带alert元素的info MIME且当前MVEA4，同样恢复MVEA3。对他人告警取消，这些以原请求无originated-by为条件的本端状态动作不适用。

- 本条没有用普通200响应直接清MVEA，也没有把无响应、超时、3xx或错误响应中alert=false并入恢复分支。“不含带alert元素的info MIME”包括缺该元素，不仅是整个MIME缺失。
- client-id构造与匹配缺口见请求条目；只对实际满足匹配条件的回执解释状态，不补造对端生成行为。
- 所列本人失败恢复不自动清用户emergency state；缺emergency-ind不等于emergency=false，不因此清MVEG/MVEGC。

依据：§11.2.1.2 receipt-indication and error-response paragraphs，印刷页 370,371。

## 第三方取消通知只清匹配接收者的告警状态

接收客户端实际收到§11.2.1.3的通知，info含alert-ind=false；本页通知不含emergency-ind。

客户端SHOULD展示告警取消及组ID，原告警发起者优先取originated-by，缺失才取calling-user-id。仅当originated-by等于接收用户自己的MCVideo ID时，SHALL将其MVEA置1。客户端最后生成并发送该MESSAGE的200。这里的显示、接收者MVEA、请求者匹配回执和CF缓存是不同证据。

- 接收者step2b没有像本人匹配回执那样明写清用户emergency state；不能增加该动作，也不能替其它未收到通知的人清状态。缺emergency-ind不触发组MVEG/MVEGC清除。
- 目标PF仍检查用户绑定，不存在则404；不复制其它业务的expiry/Warning规则。PF先从XML request-uri取目标，但其生成helper/回执转发又称从incoming SIP Request-URI取用户，入口可为PF PSI，保留该身份层次冲突，不提供已闭合路由模板。

依据：§11.2.1.3 steps2,7-8; 11.2.2.2-3; 6.3.2.2.11，印刷页 102,371,372,373,376,377。

## 按需继续

- [emergency-alert-message](emergency-alert-message.md)
- [emergency-session-client-path](emergency-session-client-path.md)
- [emergency-session-control](emergency-session-control.md)
- [service-authorization](service-authorization.md)

[ETSI TS124281 V19.3.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)。仅本版本；外部配置、SIP与密码算法仍是独立依赖。
