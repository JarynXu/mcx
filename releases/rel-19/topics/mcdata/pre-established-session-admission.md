# MCData 预建立会话：SDS 范围、共享资源与准入

## 适用范围

- TS24.282 V19.7.0 §18，普通在网客户端向服务自己的PF建立预建立SIP session；它先于后续的具体私聊SDS通信。
- 客户端已SIP注册并按§7.2.2或§7.2.3设置服务设置。这里不把服务设置200、SIP注册或预建立INVITE200当成某个对端已经接通。
- resource sharing和UE绑定按本节及被引用外部接口处理；只核24.282明确的义务、错误和标识，不声称PCC/SIP core或媒体实现已验收。

## 预建立会话的用途与共享资源

适用条件：客户端满足注册与服务设置前提，并决定是否提前建立与PF的会话。

客户端MAY建立一个或多个预建立会话；建立后客户端MAY用它发起media standalone SDS或SDS session，PF也MAY用它终接这两类SDS。使用预建立会话要求resource sharing：PF可经SIP core，或直接经Rx接口与PCC交互；支持共享后仍是MAY允许客户端使用。这个先行会话不等于后续已经选定目标并建立业务，也不是HTTP FD的文件上传/分发状态。

- SIP core支持共享可从第三方REGISTER的message/sip中Resource-Share=supported识别；registration-token用于识别注册UE。这里的UE身份、MCData用户ID和后续业务session标识不可混为一个字符串。
- 直接Rx路径的内部控制不在本页核验范围；不能因为规范允许两条共享路径就自行省略§18.3.2.2列出的绑定或拒绝条件。

依据：§18.1;18.2;18.3.1;9.2.5.2.0，印刷页 244、418、419。

## 初始 INVITE 与准入检查

适用条件：客户端发送§18.3.2.1初始INVITE，PF收到满足§6.3.1.2命名条件的预建立请求。

客户端把Request-URI指向服务PF，在mcdata-info XML的anyExt内设pre-established-session-ind=true，并使用SDS服务标记、SDP offer及ICE候选。PF先检查PSI是否已分配，无则404；依据本地策略验证用户并授权，失败403/225。若SIP core支持共享，还要核MCData用户与第三方REGISTER中registration-token所识别UE的绑定，并与INVITE Feature-Caps中的UE身份相匹配。共享不支持、所列绑定不存在或PF不支持预建立时回403/226；媒体参数不可接受，或 SDP offer 未提供 MSRP URI时回488，资源不足回500，各失败均停止后续步骤。

- 403/225是用户/本地策略准入；403/226列多个条件，不可仅凭226唯一定位成SIP core不支持。
- 客户端收集ICE仅针对取得MCData服务的接口；本页不补具体候选对选择或网络配置。
- Session-Expires为SHOULD；refresher应不带，若带须为uac，不能把它改成每个请求必有固定期限。

依据：§6.3.1.2 pre-established request;18.3.2.1;18.3.2.2 steps1–7;18.2，印刷页 93、419、420、421。

## 预建立 200 证明什么

适用条件：PF通过预建立准入并生成INVITE200；客户端收到对应2xx。

PF分配标识预建立会话的URI并放入Contact，200还带PF身份、norefersub、SDP answer；SIP core支持共享时才加入Resource-Share answer及逐媒体流共享规则。PF先调用24.582媒体过程，再发送200，然后评估ICE候选；若选中非默认候选对，还需要§18.3.4的后续offer/answer。客户端收到2xx后也调用媒体过程。这个200证明的是该预建立事务进入成功分支，不能代替后续REFER触发的业务建立结果或逐消息送达。

- 预建立SDP offer明列m=message、sendrecv、本端MSRP路径、signalling与payload两种accept-types及actpass；这些是协商属性，不证明数据已经发送。
- §18.3.1.2 SDP answer helper写修改received SDP answer中的地址/端口，同时又指received SDP offer接受的流；保留此输入措辞，不重构为已验证的SDP算法。
- 本小节客户端2xx段没有完整列出ACK与媒体就绪时序，外部SIP/媒体规范未核；不额外宣布此时可无条件传任意数据。

依据：§18.3.2.2 steps8–12 andNOTE;18.3.2.1 2xx procedure;18.3.1.1/.2，印刷页 419、420、421、422。

## 证据边界

- §18.1/.3.1明列standalone SDS using media plane和SDS session；不能据sendrecv/MSRP共性扩大到FD或IPCONN。
- 多个预建立会话是MAY，不等于任意数量业务同时占用一个会话或无限保留资源。

## 按需继续

- 需区分 SIP-core 支持、直接 Rx 路径、IP-CAN 绑定或共享资源执行证据，查[MCData 预建立共享资源：SIP 支持、Rx 绑定与完成证据](../network-policy/mcdata-preestablished-resource-sharing-boundary.md)。
- [预建立会话上的私聊 SDS：REFER、业务 INVITE 与结果反馈](pre-established-private-sds-use.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
