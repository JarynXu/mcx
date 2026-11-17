# 5G MBS 组播接收意愿：join/leave触发与PF反馈边界

## 适用范围

- 固定 TS24.282 V19.7.0（ETSI TS124282 V19.7.0，2026-08），Release19 Stage3 §19A的在网5G MBS；本页仅 multicast MBS 的 UE session join/leave通知，不覆盖broadcast MBS。
- 客户端与参与MCData功能（PF）已有所需服务关系；公告、组会话、无线条件和身份绑定分别按每条实际入口判断，不以收到公告代替业务授权或全部前置过程。
- 每项结论继承全部共同条件，再加自身角色与事件；同一项的替代触发分别判断，不要求两个join分支或三个leave分支同时成立。
- §19的MBMS与§19A的MBS不可仅凭相似名词合并。I.3.4只按调用关系提供术语映射；本页不提供完整公告、Map/Unmap、承载创建、RAN/NAS加入、安全或媒体收发实现。
- 报告接收意愿、发送SIP MESSAGE、PF向媒体面指示和实际收到数据是不同证据；所列片段不证明首包、逐消息送达、全组一致状态或精确版本互通。

## 两条加入意愿报告路径不能互加条件

适用主体：MCData客户端。

适用条件：仅multicast MBS；分别判定映射消息触发或公告/区域/无线条件触发。

须报告希望接收特定MBS session ID的组播数据：一是收到通用MBS信道上的Map Group To Session Stream、正参与其所指组会话且尚未报告ue-session-join；二是收到§19A.2.2公告、进入特定MBS session stream可用的服务区且无线条件良好。第二分支没有重述第一分支的已参与组会话或未报告条件。

规范强度：shall；各条件分支分别适用。

- 收到映射本身不是无条件join；不得给第二支静默补上第一支guard。
- 这是向MCData服务器报告接收意愿的触发，不是5GS下层加入成功或收到首包的证明。无线good判定与Map消息内部媒体处理未核。

依据：TS24.282 V19.7.0 §19A.2.5.1 first condition set，印刷页438。

## 停止接收意愿分别由删除与无线变差触发

适用主体：MCData客户端。

适用条件：仅multicast MBS；分别观察相关公告删除与无线条件。

须报告不再希望接收特定MBS session ID的数据：公告删除项匹配进行中conversation内映射消息的MBS session ID，且未报ue-session-leave；或收到删除项、当前无进行中conversation、先前因该公告通用子信道可用而报过join且未报leave；或遭遇差的MBS session无线条件。

规范强度：shall；各条件分支分别适用。

- 第三支不附加前两支的删除、conversation或防重复条件。
- 停止接收意愿不是删除MCData conversation、撤销组归属或确认网络承载已经销毁；不从“bad”自行推导无线阈值或切单播算法。

依据：TS24.282 V19.7.0 §19A.2.5.1 second condition set，印刷页438。

## 报告目标、业务会话与MBS标识分开

适用主体：MCData客户端。

适用条件：进入§19A.2.5.2发送UE session join notification过程，并按f/g各自条件选取状态。

SIP MESSAGE的Request-URI取公告P-Asserted-Identity中的PF MBS服务身份。usage body版本为1；f分支以successfully joining为前提设ue-session-join，g分支以not joining为前提设ue-session-leave；各自所列报告意图成立时携session-id，并携一个或多个适用mbs-session-id。身份body携本用户MCData ID。P-Preferred-Identity为SHOULD，不能写成所有字段一律必带。

规范强度：主体/字段shall；P-Preferred-Identity should；f/g及session-id均保留自身条件。

- session-id是MCData业务会话标识，不等同mbs-session-id或Request-URI中的服务地址。
- §19A.2.5.1表达接收意愿，§19A.2.5.2 f却用successfully joining；本页不添加下层加入完成的观测或两者时序。没有进行中conversation的触发如何取得所需session-id，所列片段未闭合。
- 原文业务ICSI、usage MIME和身份MIME/元素使用mvdata字样，见原文疑义；本页保留字段语义，不给替换成mcdata的可运行模板。

依据：TS24.282 V19.7.0 §19A.2.5.2 steps1a–h,2，印刷页438、439。

## PF核绑定后仍只得到媒体意愿指示

适用主体：参与MCData PF。

适用条件：收到UE session join notification的SIP MESSAGE；带mbs-multicast-joining-status及身份body，且其中MCData ID由本PF服务。

PF须验证PAI中的公共用户身份与body用户标识绑定。绑定成立后，join且含session-id时向媒体面指示所指MCData会话客户端希望接收特定MBS session ID的数据；leave且含session-id时指示不再希望接收。

规范强度：shall；各条件分支分别适用。

- 未含session-id时，本段没有列出同样的媒体指示动作；不据此构造必拒、默认会话或完整无会话反馈路径。
- 本段未给绑定失败的统一响应码，不补403；媒体指示不是SIP成功响应或交付回执。
- 原文绑定对象写MCDataT ID，leave分支写MCVifdeo client；保留该文本疑点，不跨业务导入MCVideo规则。

依据：TS24.282 V19.7.0 §19A.3.4，印刷页442。

## 原文疑义

- §19A.2.5.2；19A.3.4，印刷页439、442：ICSI使用urn:urn-7:3gpp-service.ims.icsi.mvdata；usage MIME为application/vnd.3gpp.mvdata-mbs-usage-info+xml，身份MIME为application/vnd.3gpp.mvdata-info+xml且元素为mvdata-request-uri。PF处另有MCDataT ID和MCVifdeo client字样。不得自行改成mcdata/MCData后宣称编码已验证。
- §19A.2.5.1；19A.2.5.2；19A.3.4，印刷页438、439、442：意愿触发、successfully joining措辞及条件session-id/服务端有session-id才指示媒体之间没有完整无conversation关联链；保留，不伪造下层成功事件或隐含映射表。
- §19A.2.3.1；19A.2.3.2；19A.3.3，印刷页437、442：相邻listening程序把bad无线条件也归入报告listening，并引用19.3.4/19.2.3.2等不同标题的过程；PF又转指客户端19.3.3。本页不据这些差异推导完整监听状态机，也不把join/leave状态与listening/not-listening互换。
- §I.2；I.3.4，印刷页656、657：I.2说MBMS及对应程序不适用5GS，I.3.4及19A则给明确复用映射；映射中的MIME又写mcptt。仅保留指定调用与边界，不把整个§19原样迁入5GS或裁决完整编码。

## 未覆盖的行为

- 公告生成/缓存/保护、MuSiK、MBS de-announcement确认及完整listening状态机未在本页展开。
- Map Group To Session Stream的编码、TS24.582媒体行为、33.180安全、TS24.229/RFC完整事务、下层5GS加入和good/bad无线检测未核；不提供可运行信令模板。
- 仅所列客户端通知与PF接收片段；没有端到端建立、重试恢复、承载资源或媒体交付验收。

## 按需继续

- 若问题实际属于§19的MBMS公告，不套本页MBS结论，查[MBMS公告与终端监听条件](mbms-announcement-and-listening-conditions.md)。
- 若需对照§19 MBMS监听反馈，注意两套状态不能互换，查[MBMS监听反馈：触发、对象与证据边界](mbms-listening-feedback-boundary.md)。
- 若需理解MCData用户与公共用户身份绑定来源，查[MCData 服务授权如何建立绑定：身份来源、并发上限和响应边界](service-authorization-binding.md)。

[TS24.282 V19.7.0 官方固定版](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅所列版本、条款和条件。
