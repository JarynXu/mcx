# SDS服务器链：地址转换与202、200的证据范围

限上述普通one-to-one或非重组预安排组的在网控制面standalone SDS；各发送动作都以相应前置检查成功为前提。

Request-URI中的服务路由、消息体中的MCData用户/组ID、SIP事务响应和SDS disposition notification分开解释；这里不处理第12章通知聚合。

## 用户标识与服务器路由的转换

适用条件：CF已按§9.2.2.4.2选出一个接收用户并调用§9.2.2.4.1.1，之后T-PF向终端转送。

CF出站Request-URI是目标T-PF的PSI，mcdata-request-uri则改为目标MCData ID；组发送另保留mcdata-calling-group-id。T-PF经§6.3.2.1再将Request-URI改为绑定到目标MCData ID的public user identity。CF和T-PF各自把出站PAI设为自己的PSI，不把这个PAI解释成最初发送用户；SDS服务标识随相应过程设置。

- 不规定网络如何从目标ID发现T-PF PSI；跨域网关不在本主题。
- §5.3还要求相关keying material从入站复制至出站，本页不是完整MIME/安全字段模板。

依据：§9.2.2.4.1.1 steps5a,5b,6–9;9.2.2.3.2 steps4–6;6.3.2.1，印刷页 95、199、200。

## 控制功能202不证明已送达

适用条件：CF在§9.2.2.4.2正常one-to-one恰好一个直接目标分支，或普通组目标分发分支，执行到steps7–8。

CF生成202( Accepted )回复原入站MESSAGE并发向O-PF；O-PF收到该202再向客户端生成202。CF这些步骤没有把收齐下游客户端200列为返回202的前提。202表示本控制处理分支的接受响应，不是某个接收用户的DELIVERED或READ，也不是全组接收完成。其与第12章通知的关联/聚合另行处理。

- 结论是对已核步骤事件前提的限定，不扩展为RFC3428全部202语义。
- 不裁决零entry、后续失败竞态或实现内部异步调度。

依据：§9.2.2.4.2 steps5b(iii),6k,7–8;9.2.2.3.1 response to step15，印刷页 198、202、204、205。

## 终接200属于另一段请求

适用条件：T-PF已向目标MCData客户端发送MESSAGE，随后收到目标端200。

T-PF生成200向CF返回。这是CF至接收侧一段请求的响应，不等同CF向O-PF生成的202，也不能据此假定原发送客户端必然收到一个代表接收成功的第二个最终响应。目标客户端自身是在适用资源/MIKEY检查后发送200，再处理SDS内容；用户/应用送达与已读仍用独立通知证据。 O-PF的§9.2.2.3.1也规定收到200时向客户端返回200；该按收到响应执行的分支仍不表示202之后必须再回第二个最终响应。

- 客户端处理细节复用sds-disposition-timing，本页不再定义显示/应用处理状态。

依据：§9.2.2.3.2 response handling;9.2.2.4.2 steps7–8;9.2.2.2.2 steps1–6;9.2.2.3.1 response handling，印刷页 195、199、205、198。

## 失败转发不能拼成同步全链保证

适用条件：T-PF收到其出站MESSAGE的4xx/5xx/6xx，或O-PF收到发往CF的MESSAGE的此类失败。

T-PF对其收到的失败生成相应SIP响应、带上收到的Warning字段并转给CF；O-PF对其收到的此类失败同样带上Warning并转给发送客户端。两段规定不能拼成“任何目标失败必在原事务同步返回给主叫”：本次读取的CF发送子过程未给出把202之后的接收侧失败转换成原请求第二个最终响应的规则。

- 仅说明已核条款没有闭合该推论，不宣称所有其他规范或实现禁止独立失败通知。
- 不新建重试、回执聚合或最终业务结果算法。

依据：§9.2.2.3.2 failure response handling;9.2.2.3.1 failure response handling;9.2.2.4.1.1;9.2.2.4.2 steps7–8，印刷页 198、199、200、205。

## 证据边界

- 未核完整TS24.229/RFC3428事务规则；这里只使用24.282显式描述的消息跳及响应事件。
- 不覆盖通知聚合、重交付和待投递状态；该部分由后续主题负责。
- 不把功能角色推成部署拓扑或独立进程。

## 按需继续

- [sds-disposition-timing](sds-disposition-timing.md)
- [delivery-evidence](delivery-evidence.md)

[ETSI TS124282 V19.7.0 / 3GPP TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

### 相关服务器路径

- [SDS服务器准入：主叫身份、控制功能与私聊目标](sds-server-identities-and-private-admission.md)
- [SDS普通组控制：组文档、发送资格与当前归属](sds-group-controller-admission.md)
- [SDS通知控制功能：原消息关联、组成员检查与聚合窗口](sds-disposition-aggregation.md)

## 媒体面SDS的对应路径

- [SDS 媒体面结果：建链 200、媒体接口与交付证据](sds-media-setup-and-transfer-evidence.md)
- [SDS 媒体面收尾：结果 BYE 与逐段释放](sds-media-result-and-release.md)
