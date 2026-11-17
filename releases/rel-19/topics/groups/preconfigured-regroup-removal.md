# 预配置重组移除：用户请求、服务器决定与退归属

固定TS24.379 V19.4.0原生预配置重组移除：既有group regroup或user regroup，按实际类型分发。不是新建重组，也不以group创建专用条件限制user regroup的移除。

用户提出移除与CF自主决定是替代入口；客户端、O-PF和CF的条件各自适用，不能把用户授权或客户端可知紧急状态套给所有服务器入口。

本页覆盖请求、响应、移除通知与终端退归属。不能将一个200解释为所有节点清理完成、全部媒体释放或所有终端已确认；创建失败补偿另由创建页说明。

命名接收入口还受§6.2.0.1/§6.3.1.3分类约束：相应用户公共身份或服务器PSI为Request-URI，并有preconfigured-group与remove。O-PF、CF、NCF及客户端分类写mcptt-regroup正文，T-PF分类却写mcptt-info正文。下文按各入口已识别后的责任叙述，不把只列重组URI/remove的构造段视为分类字段已闭合，也不替规范补字段或改正文类型。

## 用户入口：可判定紧急时先停止

适用条件：用户要求移除基于预配置组的group或user regroup。

若客户端能确定重组in-progress emergency=true，建议提示用户并停止后续步骤。否则构造发往服务用户O-PF的SIP MESSAGE，regroup正文携实际临时重组URI及remove动作，mcptt-info携客户端ID；实际使用活动功能别名时按条件携带。收到该MESSAGE的2xx时建议告知用户移除成功。

规范强度：客户端能判定紧急时停止及正常请求必需构造/发送为SHALL；用户提示为SHOULD；P-Preferred-Identity为MAY，保留其原文请求方法。

依据：§16.2.1.2 full；§16.1 (identity definitions)。印刷页：620,621,622。

依据：§6.3.1.3 removal MESSAGE classifications (dependency/comparison)。印刷页：98,99。

未能确定紧急状态不是确认非紧急；服务器仍执行自己的检查。NOTE只说用户若获授权可先取消紧急状态再重试，不授予本流程自动取消的权限。

本段P-Preferred-Identity可选字段与失败提示句写SIP INVITE，而前序构造/发送为MESSAGE；保留文字差异。失败提示原文覆盖4xx/5xx/6xx，不静默改其请求方法。

本页不逐字段替代完整报文构造，Accept-Contact与服务标识仍按本条款。2xx提示不是全网退归属或媒体释放证明。

16.2.1.2明列的regroup构造仅有重组URI/remove；6.3.1.3的O-PF入口另需preconfigured-group。此处未给出该字段的补入步骤，不以缓存中URI关联替代所要求的报文字段。

## O-PF核授权，响应helper不是通话建立证据

适用条件：O-PF收到针对临时重组身份的移除MESSAGE。；接收请求须按本页共同条件中的相应角色分类识别；分类与构造差异不由本页补齐。

O-PF从PAI确定用户MCPTT ID；profile不含allow-regroup=true时回403/161并停止。通过后找到实际重组关联CF的PSI，复制指定接触头及两种正文，PAI设为自身PSI并转发。收到2xx时按6.3.2.1.5.2生成200，按移除条款携收到的Warning、以自身PSI作PAI并发给客户端；收到4xx/5xx/6xx时携收到的Warning转回响应。

规范强度：身份/授权拒绝、转发及所列响应动作、helper必需头和条件正文复制为SHALL；资源性500、Retry-After及Resource-Share为MAY。

依据：§16.2.2.3 full；§6.3.2.1.5.2 full (actual response dependency)。印刷页：108,109,625,626。

依据：§6.3.1.3 removal MESSAGE classifications (dependency/comparison)。印刷页：98,99。

资源不足或拥塞风险时可500、可带Retry-After并停止。allow-regroup缺失或非true均不能通过。所核移除响应没有创建流程的480重选CF分支，不移植该策略。

实际调用的helper规定Require:timer、Session-Expires及请求未带refresher时设uac；Contact含MCPTT、ICSI和isfocus标签，Supported含tdialog/norefersub，可带Resource-Share，收到200含mcptt-info时条件复制。helper虽位于INVITE响应标题下，正文明确供其他程序引用并适用于发送200；不能仅凭标题判错引，也不能由这些头推断MESSAGE建立媒体会话。

移除caller以收到2xx为入口，但Warning复制文字写收到200；helper的正文复制也以收到200含正文为条件。保持各自条件，不扩成所有2xx必带相同正文。PSI发现与跨域路由算法不在本页展开。

6.3.1.3的O-PF移除分类要求Request-URI为O-PF PSI，regroup正文含preconfigured-group及remove；转发复制正文不能自动填补前序构造未列字段。

## CF接受用户请求后先回200，再通知下游

适用条件：CF收到请求移除预配置重组的MESSAGE。；接收请求须按本页共同条件中的相应角色分类识别；分类与构造差异不由本页补齐。

CF检查重组in-progress emergency=true时回403/169停止；目标重组不存在时回403/163停止。通过后先回200。group regroup按每个组成组找到其NCF并通知；user regroup按属于且已归属该重组的用户，按服务他们的T-PF组织列表并通知。下行复制所收指定接触头及两种正文，PAI设为CF自身PSI；user分支另携相应users-for-regroup。

规范强度：命中紧急/不存在守卫的拒绝、通过后的200及按类型通知为SHALL；资源性500和Retry-After为MAY。

依据：§16.2.3.2 full；§16.2.1.2 step1/NOTE (comparison: client knowledge)。印刷页：622,630,631,632。

依据：§6.3.1.3 removal MESSAGE classifications (dependency/comparison)。印刷页：98,99。

资源不足或拥塞风险时可500并可带Retry-After，拒绝后停止。紧急状态拒绝并非一般非紧急授权已通过的反证，各层条件不同。

200在下游分发之前，条款未将收到全部下游响应设为此200的前提。后续失败、超时或部分通知未达时，本段没有完整聚合结果/原子回滚规则，不自行补成功保证。

group与user是替代路由。不能让user regroup绕到组成组NCF，也不能把所有配置用户替代已归属列表。此处没有给出以BYE结束全部通话或清除全部CF缓存的完整算法。

6.3.1.3的CF移除分类要求CF PSI及preconfigured-group/remove；原文MIME名在regroup与+xml间带空格。保留文字异常，不把实际重组URI视为该字段的替代。

## CF自主决定有独立入口，不等于全局越权许可

适用条件：CF自身决定移除基于预配置组的重组；不是收到用户移除请求的入口。

group regroup中，CF逐组成组找到NCF并发MESSAGE，regroup正文携实际重组URI及remove动作。user regroup中，CF按属于且已归属重组的用户建立T-PF及用户列表，逐T-PF发送包含重组URI、remove和相应users-for-regroup的MESSAGE。

规范强度：决定入口成立后，按重组类型生成列表和通知为SHALL；本条款未给出可扩展成全局授权的MAY许可。

依据：§16.2.3.3 full；§16.2.3.2 steps1-4 (comparison: request guards)；§16.2.2.3 steps2-3 (comparison: user authorization)。印刷页：625,630,632,633。

依据：§6.3.1.3 removal MESSAGE classifications (dependency/comparison)。印刷页：98,99。

16.2.3.3没有重复用户请求入口的allow-regroup或紧急403/169守卫；这只是两个程序入口的文字区别，不证明服务器在所有策略下可无条件移除紧急重组。作出决定的完整策略未在本段展开。

本入口无上游用户请求可按前一claim回200；不复制用户请求分支的接触头、正文或PAI构造要求为此入口新增步骤。只陈述实际明列的发送字段。

发出移除通知不证明全网清理完成，也不把原创建失败的补偿remove重算为自主决定。

16.2.3.3自主构造只列重组URI/remove（user另带用户列表），而NCF/T-PF接收分类另列preconfigured-group。此处不补该字段或声称自主发送至下游分类已完全闭合。

## NCF与T-PF先应答，再通知实际已归属用户

适用条件：group路径中NCF收到移除通知；或T-PF收到预配置重组移除通知。两角色分别处理自己的入口。；接收请求须按本页共同条件中的相应角色分类识别；分类与构造差异不由本页补齐。

NCF先回200，再识别该重组中由自身负责的组成组，按所属用户中已归属重组者整理服务T-PF和用户列表；逐T-PF复制指定接触头及两种正文，加入对应users-for-regroup，以自身PSI作PAI发送。T-PF也先回200，再向自身服务且已归属该临时重组身份的每个用户发送MESSAGE到其关联公共身份；复制正文但删除users-for-regroup与groups-for-regroup，并复制入站PAI。发送后将该用户视为已退归属。

规范强度：各角色200、按实际名单/归属条件分发及T-PF退归属认定为SHALL；资源性500和Retry-After为MAY。

依据：§16.2.4.2 full；§16.2.2.5 full；§16.2.3.2 steps5-6 and16.2.3.3 (actual callers)；§16.2.2.4 step3(e-f) (comparison: creation forwarding)。印刷页：626,627,628,630,631,632,633,634,635,636。

依据：§6.3.1.3 removal MESSAGE classifications (dependency/comparison)。印刷页：98,99。

两角色均在资源不足或拥塞风险时可500、可带Retry-After并停止。正常200都先于逐用户下游通知，不等于终端确认汇总。

T-PF实际接收者依据自身服务和已归属该临时组身份判断，不是机械遍历收到的users-for-regroup。移除时去除两类名单并复制入站PAI，与创建时只去users名单且使用自身PSI不同。

本段没有等待所有终端200再认定退归属的条件；也没有列出可据此补造的全部NCF/T-PF缓存擦除、组成组自动恢复或媒体释放步骤。

6.3.1.3的NCF移除分类写regroup正文的preconfigured-group/remove，T-PF移除分类却写mcptt-info正文中的preconfigured-group/remove。保持各自分类文字，不静默统一正文名或推断转发自动完成字段转换。

## 终端收到移除通知才执行本地退归属责任

适用条件：客户端实际收到移除预配置重组的MESSAGE。；接收请求须按本页共同条件中的相应角色分类识别；分类与构造差异不由本页补齐。

客户端建议通知用户重组已移除，向服务器回200，并将自身视为已从该重组退归属。

规范强度：客户端200与退归属认定为SHALL；通知用户为SHOULD。

依据：§16.2.1.4 full；§16.2.1.2 2xx response (comparison: requester result)；§16.2.2.5 (actual notification caller)。印刷页：622,623,627,628。

依据：§6.2.0.1 removal MESSAGE classification (dependency/comparison)。印刷页：66,68。

请求者收到2xx提示、T-PF本地退归属认定与此终端实际收到通知是不同观察点。通知未送达时，不能凭上游200推定客户端已执行本条款。

此处没有完整业务呼叫BYE、媒体释放、密钥销毁或自动重新归属组成组规则；本地退归属不等于已证明所有这些效果。

6.2.0.1的客户端移除分类要求目的为用户公共身份，regroup正文带preconfigured-group/remove。单有临时重组URI不能据此认定已满足此命名入口。

## 阅读边界与导航

范围是移除信令与明确退归属责任，不是完整资源拆除协议。各入口的权限、紧急状态及接收者条件不可互相继承。

[预配置group regroup创建](preconfigured-regroup-creation.md)另述创建失败补偿；[临时组文档拆除](temporary-group-lifecycle.md)属于GMS协议，不能替代本页SIP通知与退归属。

来源：[TS24.379 V19.4.0 官方原文](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
