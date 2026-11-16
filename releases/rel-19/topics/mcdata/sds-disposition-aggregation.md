# SDS通知控制功能：原消息关联、组成员检查与聚合窗口

TS24.282 V19.7.0普通在网one-to-one或非重组组SDS带外通知；进入12.2.3的CF处理，排除FD的专用删除文件分支。

适用的6.5入站XML安全处理先于本页步骤；出站也受6.5约束。通知发出者与回执目标按原SDS方向区分。

后续成功分支仅在其conditions列明的前置门槛未终止处理时成立；通过某一检查不等于全链成功。

## 控制功能检查目标与原消息关联

适用条件：CF执行12.2.3通知处理；本文选取SDS范围，保留该共用过程的原文服务标识检查。

资源不足或拥塞风险可拒绝500并可带Retry-After。Accept-Contact不含原文列出的SDS或FD ICSI-ref服务值时403停止；resource-lists MIME缺失或其list集合中entry多于一个时403加Warning145停止。CF还用通知的Conversation ID及Message ID关联原SDS请求，关联失败则403加Warning216停止。

- entry为零不是step3明列的拒绝条件；本页不把它静默改成entry数必须恰为1的完整校验算法，也不宣称空列表可成功转发。
- 服务检查的SDS/FD备选文字不表示SDS通知可任意冒用FD服务分类；入口分类另见6.3.1.1。

依据：§12.2.3 steps1–5，印刷页 318、319。

## 组通知发出者必须匹配组成员

适用条件：CF处理SDS通知，资源、服务、resource-lists及原请求关联检查均未终止；收到的mcdata-info MIME含mcdata-calling-group-id。

CF按该组ID取得组文档，未缓存时从GMS检索，并识别组成员。mcdata-calling-user-id中的通知发出者MCData ID必须匹配组成员，否则403加Warning116并停止。此处成员检查不能替换成原数据呼叫准入中的归属检查，也不等于已经收齐组回执。

- 本步未规定GMS取文档失败的完整恢复策略；不自动引入9.2.2或其他helper的错误响应。
- 本步没有把已声明的XML用户ID与PF绑定重新比较的独立步骤，不额外声称该比较已经执行。

依据：§12.2.3 step15a–b，印刷页 320。

## 无需聚合的通知直接转发

适用条件：CF处理SDS通知，资源、服务、resource-lists、原请求关联及适用组成员检查均未终止；目标用户可由resource-lists确定。；收到的mcdata-info MIME不含mcdata-calling-group-id；或者包含该组标识且通知不需要聚合。

无组标识的分支按step16复制signalling MIME；组但无需聚合的分支按step15d复制并转入step16。出站MESSAGE以目标用户对应终接PF的PSI为Request-URI，把入站resource-lists中用户ID放入mcdata-request-uri，并带SDS服务标识及CF自己的P-Asserted-Identity后发送，不必为这些分支启动TDC1。

- step16明确要求存在mcdata-info MIME但其中没有组标识；不把整个mcdata-info MIME缺失也归成已规范的一对一直转路径。
- 跨域网关及终接PF PSI发现算法未展开。

依据：§12.2.3 steps7–14,15d,16–17，印刷页 319、320。

## 到期或通知齐全结束聚合等待

适用条件：CF处理SDS通知，资源、服务、resource-lists、原请求关联及组成员检查均未终止；收到的mcdata-info含组ID。；需要聚合通知，且尚未发送过该聚合通知。

TDC1未运行时才启动，CF将收到的signalling MIME复制到聚合的出站MESSAGE。TDC1到期或已收到所有组成员的全部MCData disposition通知，均转入step16继续发送。装不进一条MESSAGE时，原文NOTE6要求为剩余通知另建MESSAGE。到期放行不表示全员都已送达或已读。

- 原文使用all group members，不在本页改为已归属者、实际收件者或某个quorum；如何判定各类型回执已齐、去重和成员变化未给出完整算法。
- 没有从“copy MIME”推导合并二进制字段、统一改写为READ或把若干回执压成单一成功结果。

依据：§12.2.3 step15c and NOTE6;steps16–17，印刷页 320。

## 聚合计时与晚到通知的缺口

适用条件：组SDS需要聚合，适用12.2.3 step15c及F.2.2的TDC1。

TDC1默认5秒且可配置，每个特定组SDS可有独立实例；表列在全部其他组成员通知均到齐时正常停止，到期发送聚合通知。正文要求尚未发过聚合通知才进入15c，因此不能从本条推出每条后到通知都重启窗口，也不能推出聚合发出后晚到通知必转发或必丢弃。

- 需要聚合但已经发过聚合通知时，15c不再满足，15d的无需聚合条件也未满足；正文没有明确补出该情况下的body处理策略，保留缺口。
- 5秒不是任意通知的固定延迟，更不是TDU1的120毫秒或重交付计时器。

依据：§12.2.3 step15c;F.2.2 TableF.2.2-1 and NOTE1，印刷页 320、639。

## 控制功能202不证明目标消费

适用条件：CF的SDS通知流程已通过适用拒绝门槛，并已走到直转或满足聚合放行条件后的12.2.3 step17。

CF先发送出站MESSAGE，随后按steps18–19生成202并回给通知发出侧PF；这两个步骤没有以前端目标客户端返回200为前提。该202因此不能证明回执已交到目标用户，更不能额外证明原SDS已显示。目标PF仍有自己的资源和绑定门槛。

- 未从该段补造所有失败、超时及聚合等待期间的SIP事务处理；24.229及RFC依赖保持未核。

依据：§12.2.3 steps17–19;12.2.2.2 steps1–3，印刷页 317、320、321。

## 证据边界

- 仅限本页指定SDS通知分支，安全子程序、完整事务行为与部署配置另行核验。

## 按需继续

- [sds-disposition-timing](sds-disposition-timing.md)
- [sds-notification-routing](sds-notification-routing.md)

[ETSI TS124282 V19.7.0 / 3GPP TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## MCData具体XML程序

- [xml-inbound-validation](xml-inbound-validation.md)
- [xml-server-forwarding](xml-server-forwarding.md)

这些指定程序依据TS24.282 V19.7.0；不从其他安全架构页的可选机制表述推导MCData配置缺项即关闭。
