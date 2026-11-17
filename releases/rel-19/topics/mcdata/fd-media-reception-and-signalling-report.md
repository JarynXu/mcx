# 媒体面 FD：收齐文件、信令面完成指示与业务通知

## 适用范围

- 限普通在网直接 one-to-one 或普通组 standalone FD 的单播媒体链；不含紧急/迫近危险、别名、ad hoc、跨域网关、MBMS/MBS或离网。
- 各角色实际前序准入、身份、资源、安全与会话检查仍须满足；这里只追踪已进入所列步骤的传输/结果，不提供完整准入表。
- TS24.582 V19.0.0 与 TS24.282 V19.7.0 分别固定版本核查。两份文档交叉引用不等于这两个快照已证明完全兼容；源内错引与MIME差异不作静默修正。
- 终止客户端的接收/重组结论以MSRP会话已建立为前提；不通过修正错误ACK引用来证明该入口已无歧义闭合。

## 收齐、重组与交给应用

适用主体：终止客户端。

适用条件：MSRP会话已建立，收到指示chunking的SEND。

须等待剩余分块，并将全部请求重组为文件后再向应用交付；收到文件时解码mcdata-file MIME。全部分块成功收到后，必须向信令面指示下载完成。这个内部指示不等于用户已阅读，也不是已经送到主叫的SIP业务通知。

- 不宣称200响应本身承担全部重组/完整性证据。
- 无分块时具体完成事件的实现、损坏内容及解码失败处置不在此展开。

依据：3GPP TS 24.582 V19.0.0 §7.1.3.1;7.1.3.2，印刷页 30。

## 客户端完成入口的实际范围

适用主体：终止客户端信令面。

适用条件：已发送FD INVITE的200并收到对应ACK，或后来收到媒体成功下载指示。

24.282 §10.2.5.2.4 step6h及7dix的ACK调用都写24.582 §6.1.2.3，属于SDS而非FD §7.1.3。该条成功下载指示段只明确：原请求有Application metadata container时，可按本地策略处理。不能将它改写为直接调用FD完成通知helper；媒体章§4.1.2把disposition交给24.282的一般边界仍应保留。

- 这是已核入口的具体缺口，不是全规范绝无任何FD完成报告的结论。
- 不把错误6.1.2.3静默改成7.1.3，也不从HTTP §10.2.1.2补调用。

依据：3GPP TS24.282 V19.7.0 §10.2.5.2.4 step6h,7dix and successful-download indication，印刷页 293、294。

依据：3GPP TS 24.582 V19.0.0 §4.1.2;7.1.3，印刷页 10、30。

## PF有条件的完成报告

适用主体：T-PF信令面。

适用条件：发生§10.2.5.3.4所列成功下载事件，且该条所说发出的INVITE中FD请求要求完成更新；不从源文or/and省略请求守卫。

§10.2.5.3.4列媒体面成功下载指示，或接收客户端检索延期FD后成功下载，并在完成更新请求条件下调用§12.2.2.3。helper向原请求mcdata-calling-user-id所指用户生成SIP MESSAGE；组场景带calling-group-id，以§6.3.8.1生成FD NOTIFICATION。这是PF自身的信令报告入口，不能当作终止客户端已明确执行同一caller。

- 原句混合or与and，未裁决无完成更新请求时第一分支是否仍发送；本claim主动收窄到请求存在。
- 24.582只明确终端向其信令面指示、T-PF暂存向其信令面指示；普通转发路径中T-PF如何获知终端完整下载，不在这些条款核出，不能捏造接口。
- 该完成入口本身不证明通知已送达主叫；后续条件路由见本页下文，客户端 caller 及 PF 获知终端完成事件的来源缺口仍保留。

依据：3GPP TS24.282 V19.7.0 §10.2.5.3.4 final completion indication;12.2.2.3，印刷页 302、318。


## 完成报告之后的有条件路由

上面的 PF 报告入口只说明通知生成，不承担后续送达证明。以下分别追踪该通知实际进入各角色时的条件，不补齐媒体事件到 PF 的缺口，也不把各段合成无条件成功链。

### 完成报告的目标与关联键

适用主体：发出完成通知的 PF。

适用条件：已满足本页 PF 完成报告条款的事件及完成更新请求守卫，进入 §12.2.2.3 生成 FILE DOWNLOAD COMPLETED；本条不补出 PF 获知终端完成的接口。
适用条件：适用 §6.5 的入站 XML 验证/解密先于业务处理，出站保护仍须执行；本条不替代其密码与配置子程序。

PF 从原 FD 请求的 mcdata-calling-user-id 确定通知目标，放入 resource-lists 的 entry URI；组场景另带原 mcdata-calling-group-id。实际 SIP Request-URI 经 §6.3.2.2 指向 CF 的 PSI，并带 FD P-Asserted-Service 和 PF 自身 PSI 的 P-Asserted-Identity。§6.3.8.1 的完成分支保留原 Conversation ID、原 Message ID，填写当前时间和 FILE DOWNLOAD COMPLETED；面向用户时不带应用标识，面向应用时回带原 Application ID 或 Extended application ID。

规范强度：所列协议动作按原文 SHALL/MAY 保留；结果证据边界不新增协议动作。

- 通知目标用户、CF 的 PSI、原消息关联键各有用途，不能把目标用户 ID 直接当这一跳的 Request-URI。
- §12.2.2.3 step5 的 mcdata-calling-user-id 指通知所关联用户，不是把原文件发送方再次填成通知发出者的依据。
- §12.2.2.3 与 §6.3.2.2 没有在所读生成步骤中逐项列完 CF 入口需要的 Accept-Contact；仅凭这些 helper 不证明完整请求已满足下一跳入口。
- §6.3.8.1 step6di 将 Application ID 交叉引用写为 §15.2.3；保留此差异，不据此修订编码表。

依据：3GPP TS24.282 V19.7.0 §10.2.5.3.4 final completion indication，印刷页 302。
依据：3GPP TS24.282 V19.7.0 §12.2.2.3，印刷页 318。
依据：3GPP TS24.282 V19.7.0 §6.3.2.2，印刷页 95、96。
依据：3GPP TS24.282 V19.7.0 §6.3.8.1，印刷页 122、123。
依据：3GPP TS24.282 V19.7.0 §6.5.1，印刷页 123、124。

### 控制功能仍要核对原 FD

适用主体：CF。

适用条件：CF 已实际收到符合 FD disposition notification 命名入口的 SIP MESSAGE，signalling body 为 FILE DOWNLOAD COMPLETED；不以 PF 发出动作代替收到。
适用条件：适用 §6.5 的入站 XML 验证/解密先于业务处理，出站保护仍须执行；本条不替代其密码与配置子程序。

CF 资源不足或有拥塞风险时可回 500，可带 Retry-After。继续时检查 Accept-Contact 的服务值；不含条款列出的 SDS 或 FD ICSI-ref 值则 403 停止。缺 resource-lists MIME 或其 list 集合超过一个 entry，回 403/Warning145 并停止。CF 用通知的 Conversation ID 与 Message ID 关联原 FD，无法关联则 403/Warning216 并停止。若 mcdata-info 带组 ID，CF 取得组文档并检查 mcdata-calling-user-id 是否匹配组成员，不匹配则 403/Warning116 并停止。

规范强度：所列协议动作按原文 SHALL/MAY 保留；结果证据边界不新增协议动作。

- 本条限定 FD 入口；共用检查列 SDS/FD 备选值不授权混用服务分类。
- 条款只明列缺 MIME 和超过一个 entry 的拒绝，不把零 entry 自动认定合法或补成完整校验算法。
- 完成类型不适用 §12.2.3 step6 的 FILE DOWNLOAD REQUEST REJECTED 文件删除分支；不能从完成通知推出删除存储文件。
- 组文档取得失败恢复、全部成员变化和重试不在本条展开。

依据：3GPP TS24.282 V19.7.0 §6.3.1.1 FD disposition notification classification，印刷页 89。
依据：3GPP TS24.282 V19.7.0 §12.2.3 steps1–6,15a–b，印刷页 318、319、320。
依据：3GPP TS24.282 V19.7.0 §6.5.1，印刷页 123、124。

### 直转与 202 的证明范围

适用主体：CF。

适用条件：完成通知已通过前述资源、服务、目标列表、原 FD 关联及适用组成员检查；能从 resource-lists 确定目标用户。
适用条件：选择 mcdata-info 存在但不含组 ID 的私聊，或带组 ID 且通知不需要聚合的普通组分支；不覆盖需要聚合、已聚合后的晚到通知。
适用条件：适用 §6.5 的入站 XML 验证/解密先于业务处理，出站保护仍须执行；本条不替代其密码与配置子程序。

CF 复制收到的 signalling MIME，出站 MESSAGE 的 Request-URI 指向通知目标用户所对应 PF 的 PSI，把 resource-lists 中目标 MCData ID 放入 mcdata-request-uri，设置 FD Accept-Contact、FD P-Asserted-Service 以及 CF 自身 PSI 的 P-Asserted-Identity 后发送。随后 CF 生成 202 回通知发出侧 PF；这段动作没有以目标客户端返回 200 为前提，不能据 202 宣称原文件主叫已看到结果或全组文件接收完成。

规范强度：所列协议动作按原文 SHALL/MAY 保留；结果证据边界不新增协议动作。

- 这里的目标 PF 是通知接收方向的终接 PF，不能按原文件传输方向误认成文件接收方 PF。
- 需要聚合的组通知另有 §12.2.3 step15c，本条不据 SDS 主题补其 FD 计时、全员完成或晚到策略。
- CF/PF PSI 发现算法、完整事务超时和失败恢复未由本条闭合。

依据：3GPP TS24.282 V19.7.0 §12.2.3 steps7–19, selected non-aggregation branches，印刷页 319、320、321。
依据：3GPP TS24.282 V19.7.0 §6.5.1，印刷页 123、124。

### 原主叫端收到通知还需哪些步骤

适用主体：通知目标 PF / 通知接收客户端。

适用条件：PF 实际收到来自 CF、面向终接客户端的 FD disposition notification；随后客户端结论仅在该客户端实际收到相应请求时适用。
适用条件：适用 §6.5 的入站 XML 验证/解密先于业务处理，出站保护仍须执行；本条不替代其密码与配置子程序。

目标 PF 资源不足或有拥塞风险时可回 500、可带 Retry-After 并停止。继续时用 mcdata-request-uri 查找 MCData ID 与 public user identity 的绑定；不存在则 404 并停止。通过后调用 §6.3.2.1，将 Request-URI 设为目标用户的 public user identity，保留收到的 Accept-Contact/Reject-Contact 及参数，按 MIME 规则组织内容，以 PF 自身 PSI 为 P-Asserted-Identity，加入 FD 服务值并发送。该请求的 2xx/4xx/5xx/6xx 转回 CF。客户端实际收到 FD disposition notification 后，§12.2.1.2 要求解码 signalling MIME 并将通知交给用户或应用。

规范强度：所列协议动作按原文 SHALL/MAY 保留；结果证据边界不新增协议动作。

- §12.2.2.2 没有复述来自用户路径的绑定过期条件或 Warning141，不移植为本条明文响应。
- §12.2.1.2 的这两步未列出专门的 SIP200 生成步骤或完整客户端原消息关联算法；不从其他 FD/HTTP 入口补出。
- 协议要求交给用户或应用，不证明人已阅读理解、应用业务完成，更不证明所有原文件接收者均已完成；通知接收端在此通常是原文件主叫。

依据：3GPP TS24.282 V19.7.0 §12.2.2.2，印刷页 317、318。
依据：3GPP TS24.282 V19.7.0 §6.3.2.1，印刷页 95。
依据：3GPP TS24.282 V19.7.0 §12.2.1.2，印刷页 315。
依据：3GPP TS24.282 V19.7.0 §6.2.1.1 FD disposition notification classification，印刷页 54、55。
依据：3GPP TS24.282 V19.7.0 §6.4;6.5.1，印刷页 123、124。

## 原文差异

step6未接受/拒绝403；step7另给非mandatory等待、480/110拒绝、480/231延期。

依据：3GPP TS24.282 V19.7.0 §10.2.5.2.4 steps6,7，印刷页 292、293、294。

本页不将两段拼成确定性用户决定状态机，不用HTTP TDU2修复。

## 证据边界

- 不覆盖应用读取/执行、文件内容完整性算法或全文件系统。
- HTTP下载完成的请求条件及源文冲突仍留在HTTP旧页，不移植为媒体面规则。

## 按需继续

- [媒体面 FD：服务器 200、转发与暂存分别证明什么](fd-msrp-hop-ack-and-storage.md)
- [FD 接收决定：自动下载、接受、延期与完成通知](fd-download-decision-and-completion.md)
- [HTTP 文件分发：文件已存、URL 已通知与下载成功](fd-http-file-and-signalling-evidence.md)

[3GPP TS 24.582 V19.0.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124582/19.00.00_60/ts_124582v190000p.pdf)；仅所列版本和条款。

[3GPP TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅所列版本和条款。
