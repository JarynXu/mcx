# 远程发起组呼：请求权限、远端归属与起呼结果

固定 TS24.379 V19.4.0 §10.1.5 的在网远程发起组呼：A为请求者，B为被要求实际起呼的远端用户，G为目标组。请求与结果MESSAGE、B发出的组呼INVITE/REFER以及最终媒体交付是不同层次。

各claim按实际接收事件分别适用。服务器按6.3.1.3的PF/CF角色、PSI目的与mcptt-info中的request-type或response-type分类；客户端按6.2.0.1识别对应group-call-request或group-call-response。不得将请求许可或远端归属守卫套给所有结果消息。

本页展开控制请求及结果责任，并核对被调用组起呼入口；不展开紧急/迫近危险、广播、临时组/重组、功能别名、跨系统发现算法及完整媒体实现。预建立分支仅说明实际caller与可用会话前提，不承诺FFS情形有可执行回退。

## A请求B向G起呼，许可与三个身份各自明确

适用条件：A要求向B发送针对G的远程组呼请求。

A的profile缺allow-request-remote-init-group-call或值为false时，客户端建议提示未授权并停止。G配置含preconfigured-group-use-only=true时也建议提示并停止。通过后生成MESSAGE：mcptt-request-uri为G，resource-lists列B的MCPTT ID；request-type为remotely-initiated-group-call-request，按A是否要求提示B设置notify-remote-user。原文目的Request-URI为服务B的PF公共服务身份。

规范强度：缺许可/配置专用组时停止、必需字段与发送为SHALL，用户提示为SHOULD；P-Preferred-Identity及ric应用优先级为MAY。

依据：§10.1.5.1；§10.1.5.2.1 full；§6.3.1.3 remote group MESSAGE classifications；§F.1.3 request/response-type and notify semantics。印刷页：97,98,370,371,729,730。

P-Preferred-Identity与ric-app-level-priority为可选；服务标识和接触头按该程序。未指定notify意愿时不自造默认值。

此去程目的写服务B的PF，而O-PF后续核的是发送者PAI绑定；两者不得静默改成服务A的PF或认定绑定自动存在。本页不是已补齐所有部署路由的报文模板。

F.1.3的notify=false定义也写远端用户将被通知；10.1.5.2.1按不通知意愿设false，10.1.5.2.2又明确false不提示。保留定义与程序文字差异，实际程序动作见远端claim。

## PF核发送者绑定，请求许可只在request分支检查

适用条件：O-PF按6.3.1.3收到远程组呼request或response MESSAGE。

O-PF从PAI公共身份取得发送者MCPTT ID；绑定不存在或过期时回404/141并停止。仅request-type为远程组呼请求时，检查请求者allow-request-remote-init-group-call，缺失或false回403/157并停止。随后按mcptt-request-uri中的G找CF，复制mcptt-info与resource-lists，将calling-user-id设为绑定得到的ID，以自身PSI作PAI转发。收到下游2xx生成200回客户端，4xx/5xx/6xx转回。

规范强度：身份/绑定拒绝、条件授权拒绝、转发与响应为SHALL；资源性500和Retry-After为MAY。

依据：§10.1.5.3.1 full；§6.3.1.3 originating PF request/response classification；§10.1.5.2.1 step3(f)；§10.1.5.2.2 outcome step2。印刷页：97,371,373,374。

资源不足或拥塞风险时可500、可带Retry-After并跳过其余步骤。结果消息仍核发送者绑定，但不因请求者许可缺失而套用request-only拒绝。

回程结果客户端的目的又写服务A的PF，而结果发送者是B，O-PF仍按入站PAI核发送者。去回程均保留这个目的/绑定边界，不把请求者ID当发送者ID补齐。

O-PF的200只是转送MESSAGE的响应，不能当B起呼成功。CF的PSI发现及跨域出口选择未在此给出完整算法。

## CF检查B对G的归属，再重写消息的用户目的

适用条件：CF收到远程组呼request或response MESSAGE；request-only归属检查另按本claim条件适用。

CF拒绝缺指定MCPTT ICSI接触标签的请求（403），配置专用组标记true时回403/167并停止。仅远程组呼request分支，若资源列表中的B按6.3.6不归属G，回403/120并停止。通过后复制mcptt-info，把原mcptt-request-uri中的G写入calling-group-id，再将mcptt-request-uri改为资源列表中的收件人MCPTT ID，向服务该用户的T-PF发送，以CF自身PSI作PAI。下游2xx转换为200回O-PF，错误响应转回。

规范强度：所列拒绝、请求分支归属检查、字段重写与转发响应为SHALL；资源性500和Retry-After为MAY。

依据：§10.1.5.4 full；§6.3.6 full (actual affiliation dependency)；§6.3.1.3 controlling request/response classification；§F.1.3 calling-group-id semantics。印刷页：97,98,163,164,375,376,727。

资源不足或拥塞风险时可500、可带Retry-After并停止。response分支不套B归属守卫；其资源列表收件人为A，不能继续按去程B发送。

6.3.6逐项核匹配的组条目、用户条目、该用户下的客户端ID以及用户条目未过期。不能把组成员名单中有B等同于已归属。10.1.5此处给B的MCPTT ID及G，却未在所列步骤交代用于该helper的远端客户端ID取得方式；不以A客户端ID或资源列表补出。

request-uri经过CF后是控制消息收件用户，目标组保存在calling-group-id。F.1.3说明calling-group-id可向终接用户指示组身份，但本页不由该定义重写实际字段。

## T-PF按重写后的用户身份投递，不无条件复制正文

适用条件：T-PF收到按6.3.1.3分类的远程组呼request或response MESSAGE。

T-PF用mcptt-request-uri中的MCPTT ID查公共用户身份绑定；不存在时回404并停止。实际调用6.3.2.2.11生成MESSAGE，复制收到的接触头、以对应公共用户身份为目的并以T-PF自身PSI作PAI；正文按6.3.2.2.9条件填充。发送后将2xx或4xx/5xx/6xx响应转回CF。

规范强度：绑定拒绝、调用helper、条件正文复制/排除、发送和响应转发为SHALL；资源性500和Retry-After为MAY。

依据：§10.1.5.3.2 full；§6.3.2.2.11 full；§6.3.2.2.9 full；§6.3.1.3 terminating PF request/response classification；§6.2.0.1 remote-group request/response classifications。印刷页：66,67,97,125,126,374,375。

资源不足或拥塞风险时可500、可带Retry-After并停止。helper只在相关正文存在且尚未复制时复制；mcptt-info中的MKFC-GKTP明确不复制，不能写成所有正文原样透传。

6.3.2.2.9的location正文入口与复制文字存在mcptt前缀差异；不在此静默统一名称。

10.1.5.3.2 step5写在outgoing INVITE中放P-Asserted-Service，而实际helper与发送步骤都是MESSAGE。保留这一文字差异，不添加改方法或另发INVITE步骤。

## B实际调用组呼程序，预建立不可用没有已定义回退

适用条件：B客户端实际收到远程组呼request MESSAGE。按需政策与预建立政策是替代分支。

notify-remote-user=true时B可显示请求；按需政策下调用10.1.1.2.1.1向G起呼，预建立政策且有可用预建立会话时调用10.1.1.2.2.1。两个实际起呼分支中notify=false均禁止显示收到请求和起呼进行中提示。收到ric-app-level-priority时，可将其值放入按需初始INVITE或预建立初始REFER的Resource-Priority。按需入口实际携prearranged、G、B客户端ID，并因远程触发携remotely-initiated-call-request-ind=true。

规范强度：满足会话分支时调用、false时禁止两类提示、按需remote指示为SHALL；true时显示及传入ric优先级到Resource-Priority为MAY；被调用入口的配置拒绝提示为SHOULD。

依据：§10.1.5.2.2 request handling steps1-3 and Editors note；§10.1.1.2.1.1 opening,steps1-3/12-17 and response branches；§10.1.1.2.2.1 opening and invocation；§6.2.0.1 request classification；§F.1.3 notify-remote-user semantics。印刷页：67,268,269,270,277,278,371,372,730。

两个组呼入口仍检查配置专用组true并停止；按需的紧急/迫近危险/广播分支不由远程请求豁免。本页不展开这些特殊呼叫、完整SDP或后续服务器准入。

预建立入口调用10.1.2.2.2.1并将目标/类型改为prearranged；这里不重新展开完整关联过程。若政策选预建立但没有可用会话，10.1.5.2.2保留FFS，不自动改用按需或宣称必返回fail。

F.1.3对notify=false的文字与此程序禁止提示不同；不把true的MAY提升为必须提示，也不由附录文字反转程序。

按需INVITE收到403/120且请求携remote指示true时，10.1.1.2.1.1另有调用归属、确认归属后重新起呼分支；这不是控制MESSAGE403的自动重试。本页只保留调用边界，不补归属或媒体依赖完整实现。

## 结果来自B的起呼程序完成，不来自控制MESSAGE的200

适用条件：以下为三个替代的角色事件，各自仅触发对应动作：B完成10.1.1.2.1.1或10.1.1.2.2.1后构造并发送结果；或A收到结果MESSAGE后判断并提示结果；或A发出的控制请求收到4xx/5xx/6xx后处理请求失败。A的两个接收事件均不以另行证明B已完成起呼为前提。

B构造response-type为remotely-initiated-group-call-response的MESSAGE：resource-lists列收到请求中calling-user-id标识的A，mcptt-request-uri重新设为所呼G，并按所调用组呼起呼过程是否成功设置outcome为success或fail。原文目的为服务A的PF，随后经PF/CF按各自response责任送达。A从outcome判断成功或失败，建议提示用户；A发出请求收到4xx/5xx/6xx时也建议提示失败并停止该请求过程。

规范强度：完成后构造并发送结果、收到结果后判断为SHALL；向A提示结果或请求失败为SHOULD。

依据：§10.1.5.2.2 upon completion result construction；§10.1.5.2.1 error/outcome reception；§10.1.5.3.1/.3.2/.4 response forwarding；§6.2.0.1 response classification；§F.1.3 remotely-initiated-call-outcome semantics；§10.1.1.2.1.1 2xx handling (comparison: actual call response)。印刷页：67,269,270,371,372,373,374,375,376,730。

结果是B报告起呼程序的结果，不证明全体组成员已接听或音频已交付；按需起呼2xx后还有用户平面交互，P-Answer-State显示也只是可选。控制MESSAGE的200不能替代此结果。

F.1.3的fail语义写由group selection change request触发失败，而10.1.5.2.2明列远程组呼起呼失败；接收段outcome名字还出现call与-outcome间空格。保留文字差异，不按附录错误措辞换成另一业务结果。

没有把既有远程私呼的特定结果省略规则套到本流程，也不把未完成起呼的FFS情况强行归入完成后的success/fail。

## 阅读边界与导航

请求许可、PF身份绑定、远端用户在具体客户端的组归属、控制消息响应、实际起呼结果分别成立；本页保留PF路由/绑定、remote客户端身份以及预建立FFS边界，不宣称端到端接口已补齐。

[普通按需组呼](../groups/prearranged-origination.md)和[预建立组会话关联](preestablished-group-association.md)有各自适用条件，不能解除其限制后直接当作本页的完整实现。[远程私呼](remotely-initiated-private.md)另述用户目标，不代替本页组归属与组CF责任。

来源：[TS24.379 V19.4.0 官方原文](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
