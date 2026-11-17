# 预建立会话内发起组SDS session：身份、接入与业务结果

组SDS有自己的§9.2.5.3流程。预建立会话标识承载侧对话，REFER中的组ID标识业务目标；REFER200与业务建立结果也分开判断。

## 共同范围

- TS24.282 V19.7.0，普通在网预安排组SDS session使用已存在的预建立会话。排除私聊、standalone、ad hoc、紧急/迫近危险、功能别名、应用优先级扩展、FD及跨域。
- 每个角色仅在其实际收到的消息或用户指示以及该入口前序条件满足时执行。已有预建立承载不等于已关联目标组业务或获准发送。
- 媒体面只保留24.582接口引用；完整安全、配置schema、SIP/RFC、资源共享和端到端交付实现未核。

## 组身份、承载身份与请求类型分开

用户请求在已有预建立会话内发起普通group SDS session；不是standalone或新建预建立承载。

客户端先查组文档list-service中的preconfigured-group-use-only；该元素存在且true时，SHOULD提示组上不允许SDS session，并SHALL停止余下步骤。继续时生成dialog外REFER：Request-URI为预建立session identity，Target-Dialog标识该预建立会话；Refer-To的cid指向resource-lists，客户端只放一个entry，其uri是组ID。该URI的body参数携带§9.2.4.2.1的SDP offer和mcdata-info，request-type为group-sds-session，mcdata-request-uri为同一组ID，mcdata-client-id为发起客户端ID。加SDS P-Preferred-Service、Contact的SDS标签及Supported:norefersub、Refer-Sub:false后发送。组ID不是预建立session ID，也不把单entry理解为单个成员。

- 本页选择普通组SDS session。general虽同时列group standalone，不能因此省略两个request-type/SDP分支的区别。
- 原文body部分MIME写mcdata-info而其他位置写mcdata-info+xml；step5又称SIP INVITE的可选P-Preferred-Identity。保留文字差异，本页不是可直接执行的完整报文模板。
- 不提供客户端何时改选on-demand、多个预建立会话如何择一、资源共享的承载分配或端到端密钥实现。

依据：§9.2.5.3.0;9.2.5.3.1.1 opening,steps1–9 (step5 comparison only)，印刷页252,253,254。所列正文动作SHALL；用户提示、Session-Expires等按原文SHOULD或MAY分别保留。接口调用不升级为媒体交付证明。

## REFER200先于业务INVITE，PF准入没有消失

PF实际收到符合§9.2.5.3.2.1的REFER：Request-URI指本PF预建立session，Refer-To cid/Content-ID关联资源列表及body参数；本页选择客户端生成的单组entry、group-sds-session。各拒绝入口独立判断，拒绝后不得继续。

PF资源不足或有拥塞风险时可回500并可带Retry-After。继续时从PAI绑定确定主叫MCData ID，无绑定或过期回404/141；§11.1不允许发起则403/200并停止；缺被cid引用的resource-lists回403/145；不能确定服务主叫的CF则404/142。满足norefersub和Refer-Sub:false时不建隐式订阅。PF先生成并发送REFER最终200，再用§9.2.5.1.1生成业务INVITE发往确定的CF。共同helper依据已协商的预建立SDP及REFER body中的offer构成出站SDP；从body复制mcdata-info，并复制移除body参数后的resource-lists，使用PF身份和SDS服务字段。Session-Expires是SHOULD，不把helper概括成全部字段一律SHALL。

- 403/200中的200是Warning文本编号，不是SIP成功状态。
- PF step6对多个entry且group-sds写判为group SDS session；客户端却生成单entry并区分group-sds-session。本页不修正这一数量/类型规则，也不扩多组请求。
- 共同SDP helper仍回指9.2.3.3.1，未由本页验证所有session SDP兼容关系。CF选择及跨域路由内部算法未展开。
- REFER200发生在业务INVITE之前，不能证明CF已邀到组员、媒体已接通或SDS已送达。

依据：§9.2.5.3.2.1 opening,steps1–6,7–13;9.2.5.1.1，印刷页243,255,256,257。所列正文动作SHALL；用户提示、Session-Expires等按原文SHOULD或MAY分别保留。接口调用不升级为媒体交付证明。

## 业务结果回到原对话，终接侧仍需关联条件

分别判断独立事件，不要求同时成立：O-PF收到其业务INVITE的200；原发起客户端在REFER所指预建立dialog内收到状态re-INVITE；T-PF实际进入组业务INVITE终接过程；终接客户端在无已关联MCData业务的预建立session内收到establish-request。只执行各自事件动作。

O-PF收到业务INVITE200后与媒体面交互，用§9.2.5.1.2向预建立session发re-INVITE，并在其2xx后再次交互媒体面；helper将业务INVITE2xx对应为establish-success，错误对应为establish-fail。原发起客户端收到对应状态时分别提示业务建立成功或失败，并调用媒体接口。终接侧PF可因资源/拥塞回500，按入站mcdata-request-uri的MCData ID查用户绑定，无绑定回404并停止；继续时按§9.2.5.1.3向预建立session生成re-INVITE，存在入站mcdata-info时复制并加establish-request，Contact带映射到入站Contact业务session identity的标识和SDS/isfocus标签。发往终接客户端，实际收到2xx后调用媒体面。终接客户端仅在预建立session尚无关联MCData业务且state=establish-request、request-type=group-sds-session时调用§9.2.4.2.4。

- 起呼客户端收到REFER2xx也会调用媒体面，不能与后续业务establish-success合并为同一成功。预建立资源共享200更不能替代业务状态或单条SDS送达/已读。
- 原发起客户端re-INVITE段step0的接受、SDP answer和200动作置于紧急/迫近危险条件内；本页普通组不能把它搬成无条件明示步骤。
- helper定义错误→establish-fail，但组O-PF caller这里只显式展开业务INVITE200入口；完整错误响应调度、关联表写入/解绑和并发复用未闭合。
- 终接侧mcdata-request-uri是该入站终接请求中的用户绑定输入，不把起呼REFER中的组ID直接当用户ID查表。入站Contact业务ID、映射后的业务ID和预建立session ID分开。
- 9.2.5.3没有像私聊9.2.5.2.3那样列CF过程；本页只核PF向CF的业务请求及响应接口，不从私聊或on-demand页的common_conditions拼造组CF完整调用链。终接选择预建立还是按需、CF目标集合及全员完成判据仍未闭合。

依据：§9.2.5.3.2.1 SIP200 procedure;9.2.5.1.2;9.2.5.3.1.1 final2xx and re-INVITE procedures;9.2.5.3.2.2;9.2.5.1.3;9.2.5.3.1.2，印刷页243,244,254,255,257,258。所列正文动作SHALL；用户提示、Session-Expires等按原文SHOULD或MAY分别保留。接口调用不升级为媒体交付证明。

## 边界与相邻问题

这是普通组预建立使用的有界信令主链，不是全部组准入、CF分发、按需/预建立选择或业务交付闭环。已有[私聊使用](pre-established-private-sds-use.md)和[预建立准入](pre-established-session-admission.md)的条件不自动扩成组；离开业务与销毁承载另见[分别释放](pre-established-leave-and-release.md)。

[官方固定版本](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)。
