# 远程改变selected group：按人授权、归属确认与选组结果

固定TS24.379 V19.4.0 §10.1.4的在网远程选组控制。A为发出请求的用户，B为需要改变selected group的目标用户，G为要求B选择的组；改变selected group不等于发起组呼或更换配置profile。

各claim按自身角色和实际事件适用，不把请求授权、目标归属成功或选组成功设为所有响应和失败处理的共同前提。客户端分类见6.2.0.1，服务器按6.3.1.3的PF/CF角色及请求、响应类型区分；构造与分类的实际结构差异另列，不能据此当作已闭合的报文模板。

范围限请求授权、身份转送、目标归属依赖、选组动作及结果。完整归属服务器状态维护、回滚、跨域发现算法和通话/媒体建立不在此展开。

## A按目标用户取得许可，组身份与用户身份分别传递

适用条件：A要求把B的selected group改为G。

若A的profile没有含至少一个entry的RemoteGroupSelectionURIList，或B的MCPTT ID不匹配该名单，客户端建议提示未授权并停止。G的preconfigured-group-use-only存在且为true时也建议提示并停止。通过后生成MESSAGE：mcptt-request-uri为G，resource-lists列B的MCPTT ID，request-type为group-selection-change-request；目的Request-URI为服务该发起用户的PF公共服务身份。

规范强度：许可/配置拒绝后的停止、必要字段和发送为SHALL；拒绝提示为SHOULD；P-Preferred-Identity为MAY。

依据：§10.1.4.1；§10.1.4.2.1 request construction steps1-4；§6.2.0.1 group-selection request/response classification (comparison)；§6.3.1.3 group-selection PF/CF classification (comparison)；§10.1.4.4 step3 (comparison: anyExt)。印刷页：66,67,97,364,365,369。

P-Preferred-Service与Accept-Contact按本程序填写，P-Preferred-Identity为可选；这里不代替完整SIP构造规则。

客户端构造step2(d)把request-type直接列在mcptt-Params下；客户端及服务器分类、CF请求分支却写在anyExt中。两者层级差异保留，不自行增补anyExt并声称原文接口已闭合。

服务器终接PF分类中的response字符串写作group-selection-change -response，带额外空格；目标客户端构造写group-selection-change-response。这里不据此发明另一种消息或静默修订字符串。

## O-PF核发送者身份，但请求许可检查的取值与客户端不同

适用条件：O-PF按6.3.1.3收到选组request或response MESSAGE。

O-PF从PAI公共身份取得发送者MCPTT ID；绑定不存在或已过期时回404/141并停止。仅group-selection-change-request分支检查RemoteGroupSelectionURIList：无非空名单，或mcptt-request-uri所含的原文所谓MCPTT ID不在名单时，回403/155并停止。随后按mcptt-request-uri中的组找CF，复制mcptt-info及resource-lists，把calling-user-id设为发送者绑定所得ID，以自身PSI作PAI发送。下游2xx转换为200回客户端，4xx/5xx/6xx转回。

规范强度：绑定/许可拒绝、身份赋值、转发及响应为SHALL；资源性500和Retry-After为MAY。

依据：§10.1.4.3.1 full；§10.1.4.2.1 steps1/2(d-e) (comparison: authorization target)；§6.3.1.3 originating PF group-selection classification。印刷页：97,364,365,366,367,368。

原始客户端按B的用户ID授权，但O-PF step3(a)(ii)使用mcptt-request-uri；前序该字段是G的组身份。不能把O-PF文字偷偷改为resource-lists里的B，或据客户端通过就断定PF也通过。

结果response也核发送者绑定，但不套request-only名单检查。资源不足或拥塞风险时可回500并可带Retry-After，跳过其余步骤。

CF公共服务身份及跨域出口的具体发现方法不由本页补齐。200是控制MESSAGE响应，不证明B已改组选组。

## CF对请求检查目标归属与资格，再改写用户目的

适用条件：CF收到选组request或response MESSAGE；目标归属/资格和affiliation-required仅在所列request分支适用。

缺指定MCPTT ICSI接触标签时CF回403并停止；G的配置专用标记true时回403/167并停止。对request，资源列表目标B若按6.3.6未归属G，则调用9.2.2.3.8判定资格；无资格回403/120并停止。通过后复制mcptt-info，将原mcptt-request-uri中的G放入calling-group-id，再把mcptt-request-uri改为资源列表中的收件用户。仅request且B未归属但被判有资格时加入affiliation-required=true，向服务该收件人的T-PF发送，以CF自身PSI作PAI。下游2xx转换为200回O-PF，错误响应转回。

规范强度：所列拒绝、条件资格调用、身份改写、条件加入标志和响应为SHALL；资源性500和Retry-After为MAY。

依据：§10.1.4.4 full；§6.3.6 full (actual affiliation dependency)；§9.2.2.3.8 full (actual eligibility dependency)；§10.1.4.3.1 steps2/9 (comparison: calling-user-id source)；§6.3.1.3 controlling group-selection classifications。印刷页：97,163,164,232,233,366,367,368,369,370。

归属helper 6.3.6要求匹配的组、用户、用户下客户端ID以及未过期用户条目。成员名单里有B不足以证明归属；本caller未明确交代目标客户端ID取得方式，不能用A客户端ID或资源列表代填。

资格caller针对资源列表B，而9.2.2.3.8从mcptt-request-uri取handled组、从calling-user-id取handled用户，后者由O-PF设为发送者。helper核GMS组存在/成员及本地组条目；这里未见把B显式映射到该输入的步骤。保留调用身份接口边界，不宣称目标资格接口已无歧义，也不以资格等同已建归属。

response不重新套request-only目标归属/资格检查或新增affiliation-required；结果资源列表收件人为A。资源不足或拥塞风险时可500、可带Retry-After。CF的服务标签及配置检查仍按其入口适用。

## T-PF按收件用户绑定投递请求或结果

适用条件：T-PF收到按6.3.1.3分类的选组request或response MESSAGE。

T-PF按mcptt-request-uri中的收件用户ID查公共身份绑定；不存在则回404。通过后调用6.3.2.2.11生成MESSAGE，依对应公共身份设置目的，复制接触头，以T-PF自身PSI作PAI；调用6.3.2.2.9按条件复制正文，添加本程序的P-Asserted-Service并发送。下游2xx及4xx/5xx/6xx转回CF。

规范强度：绑定不存在拒绝、helper调用、条件复制/排除、发送和响应转发为SHALL；资源性500和Retry-After为MAY。

依据：§10.1.4.3.2 full；§6.3.2.2.11 full；§6.3.2.2.9 full；§6.3.1.3 terminating PF group-selection classification。印刷页：97,125,126,368。

资源不足或拥塞风险时可回500并可带Retry-After，跳过其余步骤。这里绑定不存在的404不自动扩成O-PF的过期/141规则。

helper仅在正文存在且尚未复制时按所列类型复制，mcptt-info里的MKFC-GKTP不复制；location正文入口与复制项存在mcptt前缀文字差异，不在这里静默统一。

## B在明确的归属条件满足后改变selected group

适用条件：B客户端实际收到选组request；归属调用、NOTIFY确认和选组各受其自身条件限制。

affiliation-required=true时，B调用9.2.1.2向calling-group-id所指G发起归属；若尚未调用9.2.1.3则调用状态观察。收到NOTIFY且p-id匹配本次PUBLISH的p-id时，确定该次归属是否成功。仅在“affiliation-required=true且上述归属成功”，或“affiliation-required字段不存在”这两个替代条件下，改变selected group为calling-group-id所指G，并确定选组成功或失败。

规范强度：条件归属调用、观察调用、匹配通知后的判断以及满足入口时的改组和结果确定为SHALL。

依据：§10.1.4.2.2 steps1-2；§9.2.1.1 final paragraph (observation-before-change dependency)；§9.2.1.2 full (actual PUBLISH dependency)；§9.2.1.3 full (actual observation dependency)；§F.1.3 affiliation-required semantics。印刷页：206,207,208,365,730。

字段存在且为false不等于不存在；step2未给该值相同的改组选组入口，不补默认改组、默认成功或默认失败。

PUBLISH带本客户端ID、全部仍感兴趣的组及唯一p-id；归属状态依NOTIFY确定，PUBLISH事务响应不代替匹配p-id的成功确认。未匹配或尚未收到通知不能推成功。

10.1.4.2.2先列归属调用再列尚未启动时的观察调用；9.2.1.1要求改变归属前启动状态确定。保留该依赖顺序要求，不把编号解释成必须等SUBSCRIBE的200才可PUBLISH。完整订阅/归属服务器状态过程见各自主题。

## 选组结果、结果接收和控制失败是三个替代事件

适用条件：三个替代入口分别处理：B执行目标客户端程序的结果构造；或A收到选组response MESSAGE；或A的控制请求收到4xx/5xx/6xx。A的两个接收事件不要求B已完成或选组成功，B的失败结果也不要求成功改组。

B的结果MESSAGE把资源列表收件人设为原请求calling-user-id所指A，将mcptt-request-uri设为要求选择的G，在anyExt中设response-type=group-selection-change-response。选组成功则selected-group-change-outcome=success；被要求归属且归属失败，或选组动作失败，则为fail。B建议提示结果，并向服务自己的PF发送。A收到结果后从outcome判断成功或失败并建议提示；A的控制请求收到4xx/5xx/6xx时，建议提示请求失败并不继续后续步骤。

规范强度：B生成并发送结果、按条件填写outcome及A收到结果后的判断为SHALL；两端结果提示及A请求错误的提示/不继续措辞为SHOULD；B的P-Preferred-Identity为MAY。

依据：§10.1.4.2.2 steps3-6；§10.1.4.2.1 error response and outcome reception；§10.1.4.3.1/.3.2/.4 response forwarding；§6.2.0.1 group-selection response classification；§F.1.3 selected-group-change-outcome semantics。印刷页：67,365,366,367,368,369,370,729,730。

B结果分支明确包括归属失败，无需先完成成功选组。对于前面未列选组动作且没有已判失败的情形，不自造outcome取值、超时或回滚算法。

控制MESSAGE的200只属于转送响应；outcome success描述本次selected group改变，不证明已发起组呼、已有人接听或媒体送达。

请求错误响应原句为should indicate … and not continue；这里不额外把停止升级成独立SHALL。

## 阅读边界与导航

请求许可、目标用户的具体客户端归属、资格、selected group改变及控制消息响应分别判断。字段层级、许可检查身份和资格helper输入存在上述接口边界，本页不提供已经消除差异的端到端报文实现。

[显式归属请求](explicit-affiliation-publish.md)与[状态观察](explicit-affiliation-observation.md)分别说明PUBLISH和NOTIFY责任；[资格判断](implicit-affiliation-eligibility.md)的既有业务入口不替代这里实际核对的远程caller。[配置profile选择](../identity/profile-selection.md)是另一类配置操作，不等于改变selected group。

来源：[TS24.379 V19.4.0 官方原文](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
