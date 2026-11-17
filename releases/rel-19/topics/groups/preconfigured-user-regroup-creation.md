# 预配置用户重组创建：指定用户、局部成功与通知

本页说明 TS24.379 V19.4.0 §16.3 的在网预配置 user regroup 创建：由用户指定 MCPTT ID 名单，分别经过客户端、O-PF、CF、T-PF及接收通知的客户端。各角色的接收事件分别适用，不要求同一节点满足所有入口。

按§16.1，服务器与客户端已配置预配置组；重组继承其完整配置（包括安全密钥），但不继承 preconfigured-group-use-only。配置取得、密钥分发、完整通话建立与移除不在本页展开。

服务器的 user regroup 创建分类（§6.3.1.3）要求对应角色 PSI 为 Request-URI，mcptt-regroup 正文含 preconfigured-group、create及非空 users-for-regroup；客户端创建通知分类（§6.2.0.1）要求对应公共用户身份为目的，regroup正文含preconfigured-group与create。按F.7.3，用户列表含一个或多个MCPTT ID，users与groups两种列表不能同时存在。

## 用户指定的是待归属用户，不是组成组

适用条件：用户要求建立基于预配置组的user regroup。

客户端向服务自己的O-PF发送MESSAGE：以唯一临时URI标识实际重组，以preconfigured-group标识配置来源，以users-for-regroup列出用户MCPTT ID并携create。mcptt-info携客户端ID；使用活动功能别名或用户请求应用优先级时，按各自条件携字段。收到该MESSAGE的2xx后，建议提示创建成功。

规范强度：必需字段、条件字段及发送为SHALL；P-Preferred-Identity为MAY；成功与原文所列失败提示为SHOULD。

依据：§16.1；§16.3.1.1 full；§6.3.1.3 user regroup creation classifications；§F.7.3 identity/list semantics and create user branch。印刷页：98,99,620,621,637,638,777,778。

唯一URI形成由实现决定；Accept-Contact、MCPTT服务标识及可选P-Preferred-Identity仍按原条款。本页不是完整报文模板。

失败提示段写收到SIP INVITE的4xx/5xx/6xx，前文构造为MESSAGE；保留文字差异，不自行改写。2xx成功提示不证明全员通知或通话接通。

## O-PF检查既有重组权限，并按480重选CF

适用条件：O-PF按共同分类收到user regroup创建请求。

O-PF从PAI公共用户身份确定MCPTT ID。用户profile没有allow-regroup=true时，回403/160并停止；通过后选择CF，复制两类正文与收到的接触头，以自身PSI作PAI转发。收到480时选择另一CF并重新生成、转发请求；收到2xx时调用6.3.2.1.5.2生成200，以自身PSI作PAI返回客户端。其它4xx及5xx/6xx按原文复制Warning转回。

规范强度：身份、授权拒绝、转发、480重选及响应为SHALL；资源性500、Retry-After与helper的Resource-Share为MAY。

依据：§16.3.2.1；§16.3.2.2 full；§6.3.1.3 originating user-create classification；§6.3.2.1.5.2 full (actual response helper)；§16.2.2.2 480 branch NOTE7 (comparison only)。印刷页：98,108,109,624,625,638,639,640。

资源不足或拥塞风险时可500、可带Retry-After并停止。缺失allow-regroup与非true都不能通过；不为user regroup创造另一套许可。

本段480正文要求重选，NOTE7说明PSI可在本系统或伙伴系统；不能移植group创建段关于是否重试的部署注。CF选择方式仍是本段NOTE1所说部署决定；次数、终止策略及跨域发现算法未在这里给出。

2xx触发生成200，但Warning复制句限定收到的200。实际helper含timer/Session-Expires、Contact与Supported头、可选Resource-Share及收到200含mcptt-info时的复制；不将这些响应头解释为MESSAGE建立媒体会话。

## CF的成功门槛是任一T-PF返回200

适用条件：CF按共同分类收到user regroup创建请求。

不能处理该user regroup时CF回480；重组ID已使用时回403/165，均停止。通过后，CF将所有指定用户按服务他们的T-PF分组，逐T-PF发送MESSAGE，复制正文和接触头，加入该T-PF对应的users-for-regroup，以CF自身PSI作PAI。任一被发送请求的T-PF返回200时，CF向上游回200，并保存重组URI、预配置组身份及收到的整份用户集合。没有收到200的分支规定回480。

规范强度：能力/ID拒绝、用户分组、发送、所列200保存及无200时480为SHALL；资源性500和Retry-After为MAY。

依据：§16.3.3.1 full；§6.3.1.3 controlling user-create classification；§16.2.3.1 steps4-7 (comparison only: group response/compensation)。印刷页：99,628,629,630,641,642。

资源不足或拥塞风险时可500、可带Retry-After并停止。成功条件是任一200，不是任一2xx，也不是group创建的全部NCF200；本流程直接面向T-PF。

step5与5(f)把列表回指step3，实际分组列在step4；step6/7把所发送MESSAGE回指step4，实际发送在step5。保留号次差异，不据此补出另一条请求。

无200分支未规定何时完成判断或等待定时器；不能把暂未响应立即等同失败。任一200后保存整份请求名单，不代表其它T-PF或所有用户已成功。本段没有group创建所列的部分失败remove补偿，不补原子回滚。

## T-PF先回200，再通知已知尚未获通知的用户

适用条件：T-PF按共同分类收到user regroup创建MESSAGE；逐用户动作限于收到名单中的MCPTT ID，且从已存信息知道其客户端此前未收到该创建通知。

T-PF先回200。对满足逐用户条件的对象，向关联公共用户身份发MESSAGE，复制接触头及正文，但删除groups-for-regroup而保留users-for-regroup；PAI为T-PF自身PSI。发送后将该MCPTT ID视为已归属实际重组。T-PF保存重组URI、预配置组身份和user regroup成员名单，直至重组移除。

规范强度：200、满足条件时的转发与归属认定、状态保存为SHALL；资源性500与Retry-After为MAY。

依据：§16.3.2.4 full；§16.3.3.1 steps4-6 (actual caller)；§6.3.1.3 terminating user-create classification；§F.7.3 create user branch；§16.2.2.4 step3(e) (comparison only: group forwarding)。印刷页：99,626,627,640,641,642,778。

资源不足或拥塞风险时可500、可带Retry-After并停止。先回200并不以逐用户通知已完成为条件。

已存信息显示未通知才进入该逐用户分支；未知不能直接当未通知，已通知也不能重复套用。本文不补通知历史标记的生成或恢复算法。

本段转发保留的是该T-PF收到的用户列表，不代表CF最初的全体名单。与group创建删除users列表不同；不能借group页改变通知正文。发送后的本地归属认定没有客户端已确认守卫，不证明终端收到或接听。

## 客户端依实际通知认定归属，通话仍需另行建立

适用条件：服务器实际通知客户端创建user regroup；按6.2.0.1识别该创建MESSAGE。16.3.1.3明确调用16.2.1.3。

客户端建议提示用户并回200，保存临时重组身份；收到users-for-regroup时，建议保存其用户列表并将重组识别为user regroup，随后认定自己已归属重组。如果重组为chat group，建议在收到创建通知时加入。

规范强度：200、身份保存、user regroup类型认定及归属为SHALL；用户提示、用户列表保存与条件chat加入为SHOULD；显示列表是NOTE所述选择。

依据：§16.3.1.3 full (actual caller)；§16.2.1.3 full (called procedure)；§6.2.0.1 heading and creation MESSAGE classification；§16.3.2.4 (actual notifying caller)。印刷页：66,67,68,622,623,638,640,641。

身份关联句写把mcptt-regroup-uri与同名mcptt-regroup-uri收到的组身份关联；不静默将后者改成preconfigured-group。

共享程序对组成组列表及避免呼叫组成组的建议有group regroup条件，不套给此user regroup。用户列表可选择显示，但不把T-PF子集视为全网成功名单。

chat加入是SHOULD，不是本页已建立INVITE或媒体交付的证据。客户端通知200、归属状态与呼叫建立分别判断。

## 阅读边界与导航

CF的任一200、T-PF先行200、客户端通知与实际业务通话是不同结果；不将创建响应当成全员接通或一致性提交保证。

[组成组重组创建](preconfigured-regroup-creation.md)有不同的派发对象和成功门槛；[重组移除](preconfigured-regroup-removal.md)另述移除请求与通知。两页条件不能直接替代本页用户创建入口。

来源：[TS24.379 V19.4.0 官方原文](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
