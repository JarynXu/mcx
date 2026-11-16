# 媒体面 FD：何时能发文件，响应如何触发收尾

## 适用范围

- 限普通在网直接 one-to-one 或普通组 standalone FD 的单播媒体链；不含紧急/迫近危险、别名、ad hoc、跨域网关、MBMS/MBS或离网。
- 各角色实际前序准入、身份、资源、安全与会话检查仍须满足；这里只追踪已进入所列步骤的传输/结果，不提供完整准入表。
- TS24.582 V19.0.0 与 TS24.282 V19.7.0 分别固定版本核查。两份文档交叉引用不等于这两个快照已证明完全兼容；源内错引与MIME差异不作静默修正。

## 最终信令响应与媒体入口

适用主体：主叫客户端。

适用条件：收到普通媒体面FD INVITE的最终响应。

SIP 2xx触发ACK、启动会话计时器并调用24.582 §7.1.2。4xx/5xx/6xx触发文件未能发送的用户提示及ACK。前者只进入媒体流程，不证明文件已传出或已接收。

- 不把SIP 2xx改称MSRP 200；没有把全部SIP异常都归入这三个错误类别。

依据：3GPP TS24.282 V19.7.0 §10.2.5.2.3 response handling，印刷页 290。

## 连接、空SEND与文件发送

适用主体：主叫客户端。

适用条件：已收到建立FD MSRP连接的指示；协商参数可用。

按收到的SDP answer建立连接；answer为passive时本端active，为active时本端passive。本端active时必须先发空SEND绑定连接。原文规定收到首个SEND的MSRP 200后可以发文件：To-Path来自answer，Content-Type为application/vnd.3gpp.mcdata-file，body承载文件或部分文件。

- 7.1.1对未获发送许可写should not，不升级为本文另造的shall not授权门槛。
- 首个200可对应绑定空SEND，不能当文件完成。passive端首个SEND的具体引导不据常识补出。
- 24.282的SDP accept-types写mcdata-signalling，见跨源差异，不宣称MIME完全一致。

依据：3GPP TS 24.582 V19.0.0 §7.1.1;7.1.2.1，印刷页 29、30。

## 分块收尾和错误响应

适用主体：主叫客户端。

适用条件：已经进入文件SEND；分别观察启用chunking或收到non-200的路径。

启用chunking时继续发送所需分块、等待每个SEND的200，并在最后一个200后按24.282终止SIP会话。收到non-200时按引用RFC处理错误；终止MSRP会话的步骤要求中止尚未发送的分块、提示文件无法分发，并终止SIP会话。

- 最后200收尾规则在If MSRP chunking is used下，不能扩成不分块成功路径的同一句显式义务。
- 不推导具体重传次数、RFC错误分类、自动改用HTTP或对所有接收者交付成功。

依据：3GPP TS 24.582 V19.0.0 §7.1.2.1，印刷页 30。

## 媒体失败指示后的BYE

适用主体：主叫客户端信令面。

适用条件：收到媒体面指示文件发送不成功。

生成并发送BYE，Request-URI使用待释放的MCData session identity；Reason协议值SIP、cause 480、text为transmission failed。这个BYE是失败释放信令，不是收件方的拒绝通知，也不是成功收尾证明。

- 24.582描述终止SIP的义务，24.282这里明确的是收到失败指示时的动作；不臆造跨层API、每个错误的映射或完成时也用此Reason。

依据：3GPP TS24.282 V19.7.0 §10.2.5.2.3 final indication handling，印刷页 290、291。

## 原文差异

SDP accept-types为mcdata-signalling。

依据：3GPP TS24.282 V19.7.0 §10.2.5.2.1/.2;10.2.5.4.1/.2，印刷页 286、287、302、303。

MSRP文件MIME为mcdata-file。

依据：3GPP TS 24.582 V19.0.0 §7.1.2.1;7.1.3.2，印刷页 29、30。

两个固定快照字段不一致。并列呈现，不替换任一原文字段，不宣称协商兼容已闭合。

## 证据边界

- 不展开RFC传输实现、文件系统、重传、断点续传或完整安全配置。
- 不新增HTTP下载流程；HTTP 201/GET 200与FD通知已由旧页覆盖。

## 按需继续

- [FD 发送准入：文件上限、单次额度与拒绝来源](fd-size-admission.md)
- [媒体面 FD：服务器 200、转发与暂存分别证明什么](fd-msrp-hop-ack-and-storage.md)
- [媒体面 FD：收齐文件、信令面完成指示与业务通知](fd-media-reception-and-signalling-report.md)
- [HTTP 文件分发：文件已存、URL 已通知与下载成功](fd-http-file-and-signalling-evidence.md)

[3GPP TS 24.582 V19.0.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124582/19.00.00_60/ts_124582v190000p.pdf)；仅所列版本和条款。

[3GPP TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅所列版本和条款。
