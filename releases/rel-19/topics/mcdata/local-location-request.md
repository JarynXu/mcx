# MCData按需位置请求：本地目标许可、刷新与报告证据

## 适用范围

- 固定TS24.282 V19.7.0，在网MCData直接用户ID列表的按需位置查询；所查询目标的位置由同一PF管理。排除功能别名目标、跨PF转送、完整持续报告配置、历史恢复及位置触发的组/告警动作。
- 各角色按自身接收事件和claim条件判断；请求许可、逐目标分享许可、报告发送许可分开，不将后续成功设为拒绝或静默停止的共同前提。
- 本页核有限Stage3业务责任，不从Stage1/2位置要求补报文、授权算法或成功闭环。配置、测量和安全依赖不因收到200而完成。

## 直接ID请求先过身份与请求许可检查

**条件：** 请求客户端需要查询一个或多个MCData用户的位置，选择直接MCData ID列表而不是功能别名。PF准入分支以实际收到该客户端位置请求MESSAGE为事件；拒绝分支不要求请求许可或目标分享许可已经通过。

客户端将MESSAGE送往服务自己的PF公共服务身份，以resource-lists entry.uri列出所请求用户的MCData ID，携MCData ICSI的P-Preferred-Service及带require/explicit的Accept-Contact；位置MIME正文含带RequestId的Request。可以携P-Preferred-Identity、refresh=true及Request.anyExt中的LocationFilter，后者以区域TriggerId和AreaIn表达区域内或区域外筛选。PF可因资源不足或拥塞风险以500拒绝，可附Retry-After并停止该拒绝路径；随后按PAI公共用户身份识别请求用户。无有效绑定时404/Warning141并停止，无resource-lists正文时403/244并停止，无位置请求许可时403/245并停止。通过这些前置后，PF先发送200，再识别和处理各目标。

**规范强度：** 客户端必需构造及PF明确拒绝/后续步骤为 SHALL；P-Preferred-Identity、refresh和LocationFilter为 MAY；资源拒绝及Retry-After为 MAY。

- 200发生在逐目标分享许可、刷新和区域过滤之前，不代表所有目标已同意、位置已取得或Report已到达。请求许可的判断算法不在该段范围内。
- 列表中的MCData ID、PF路由身份、请求用户PAI及关联标识分别使用，不能把客户端自报身份当成PAI绑定。目标是用户ID；不据此补一个用户多个终端的选择算法。
- 本页不处理alias-only请求或跨PF：客户端另有别名入口，但PF前序要求resource-lists且别名分支回指状态确定§22.2.2.2.7，不能拿解析过程替换回指。
- 正文与schema存在RequestId/RequestID、ReportId/ReportID大小写差异。这里说明请求与报告的关联责任，不提供静默统一后的可发送XML。

**依据：**
- [TS24.282 V19.7.0 §17.3.3.2 full procedure](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 417；规范依据。
- [TS24.282 V19.7.0 §17.2.3.2 steps1–7 and NOTES1–2](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 411,412；规范依据。
- [TS24.282 V19.7.0 §D.4.2 tRequestType;D.4.3 Request/Report semantics](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 596,597,612；关联、filter位置与大小写对照。
- [TS24.282 V19.7.0 §17.2.3.2 step7b and step7A(a);22.2.2.2.7](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 412,485,486,487；comparison-only：排除别名与跨PF，不以它闭合当前直接ID路径。

## 每个本地目标另查分享许可，再决定刷新与筛选

**条件：** PF已通过本次请求的前置检查并返回200，按直接ID列表确定目标；对当前目标的位置由本PF管理。以下每个目标分别处理。

PF先核目标用户是否允许把位置提供给请求用户；不允许时静默忽略该目标请求，停止该目标余下步骤。允许后，无缓存或Request.refresh=true时请求目标即时更新，等待实现定义的时长，收到后存储或更新；已有位置但超过实现定义的陈旧阈值时也要求更新。收到LocationFilter时，AreaIn=true而目标在区域外，或AreaIn=false而目标在区域内，跳过余下步骤。继续到报告生成分支时，PF向与请求用户MCData ID绑定的公共用户身份发送新的MESSAGE；Report的关联属性取原请求标识，CurrentLocation承载目标位置，mcdata-reporting-uri标识所查询的MCData ID。

**规范强度：** 逐目标许可判断、条件更新及报告构造按本段强制步骤；分享不允许和筛选不满足时停止相应处理，不另补错误响应。

- 分享许可不等同请求许可；静默忽略发生在200之后，不能编造第二个403、每目标失败清单或全员完成回执。授权取得机制未定义。
- 无缓存/refresh分支与陈旧缓存分支是原文分别列出的条件，不擅自合并为互斥分支或承诺只请求一次更新。等待时长和陈旧阈值未给固定秒数。
- 若等待更新超时或仍无可用位置，该段没有完整规定回退、重试或空报告算法，不保证仍能报告最新位置。筛选不满足也不意味着目标离线或拒绝分享。
- 报告类型可为小区等信息，依配置与实现，不保证经纬度或新的GNSS测量。Request/Report相关字段大小写以及LocationFilter在客户端anyExt与PF正文描述之间的表达差异必须保留；不把本页当完整schema验证。

**依据：**
- [TS24.282 V19.7.0 §17.2.3.2 step7a,step7A(b)(i–v) and NOTES4–5](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 412,413；规范依据。
- [TS24.282 V19.7.0 §17.2.3.1](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 411；即时更新实际helper。
- [TS24.282 V19.7.0 §17.3.3.2 steps6–8;D.4.2 tRequestType/tReportType;D.4.3 Request/Report semantics](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 417,596,597,612；关联、过滤位置及报告含义。

## 目标报告另有配置、内容与异常处理边界

**条件：** 目标端收到§17.3.3.1所列带MCData ICSI Accept-Contact、location-info MIME及Request的MESSAGE；随后按§17.3.4报告。独立MESSAGE发送使用既有位置报告配置的路由输入。PF异常剥离分支则仅在§17.2.5完整条件匹配时另行判断，不以目标已成功报告为前提。

显式位置请求使目标端调用报告过程并重置minimumReportInterval；它不以周期trigger仍为true为前提。若本来就需发送其他SIP请求，可把报告放入该请求；否则生成独立MESSAGE，其Request-URI取先前位置报告配置请求的PAI SIP URI。请求触发的Report携带从Request取出的关联值，报告过程重启minimumReportInterval并清除triggers。PF接收目标Report时另按收到的MCData ID授权，允许后使用位置。D.4中Report有必需CurrentLocation和ReportType，具体坐标及测量时间可选，关联标识用于对应请求而非证明新鲜度。

**规范强度：** 显式请求后的报告、计时器处理、PF授权及异常条件匹配后的剥离为 SHALL；不把可选坐标/时间提升为必需结果。

- 周期trigger路径受minimumReportInterval及到期时trigger仍真约束；显式请求另有直接报告入口，不将两者AND合并。独立报告目的地来自配置，不擅自改为刚收到的查询请求PAI；配置缺失的路由恢复未在本页闭合。
- §17.3.4.2把位置报告元素的加入与已触发trigger相连，D.4又要求CurrentLocation。本页不补无trigger时全部字段的生成算法；收到Report也不证明坐标完整、所有目标都响应或请求端已处理。
- §17.2.5异常条件为：PAI识别的公共用户身份不关联本PF服务的用户，或mcdata-info中的mcdata-request-URI识别本PF服务的MCData用户；再同时要求Accept-Contact含g.3gpp.mcdata和MCData ICSI两项，以及location-info含Request或Configuration。符合时PF发送SIP请求需移除location-info正文。第二个OR项原文没有not，不擅改为“不服务”；也不省略后面的header/body条件来断言所有本地请求都会剥离。
- §17.2.4.1还对进入/离开组地理区域或紧急告警区域列出额外调用。本页限按需位置获取，不展开这些事件的告警或组状态动作。坐标编码、内容保护和完整XML实现仍是依赖。

**依据：**
- [TS24.282 V19.7.0 §17.3.3.1;17.3.4.1;17.3.4.2](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 416,417,418；规范依据。
- [TS24.282 V19.7.0 §17.3.1;17.2.4.1](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 414,415；配置内容输入及PF收到Report的授权。
- [TS24.282 V19.7.0 §17.2.5 full procedure](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 415；完整OR及header/body异常守卫。
- [TS24.282 V19.7.0 §D.4.2 tReportType;D.4.3 Request/Report and CurrentLocation semantics](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 597,612,613；内容必需/可选、关联大小写和测量时间范围。

## 使用边界

- 同一次请求的200、各目标许可、后续Report以及Report中的位置新鲜度是不同证据。没有报告也不能唯一归因为权限失败。
- 源文的字段大小写、条件关系和不完整构造边界均保留；不提供端到端可执行报文或全目标最新位置保证。
