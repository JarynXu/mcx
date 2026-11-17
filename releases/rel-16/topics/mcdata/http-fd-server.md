# 私聊HTTP文件分发服务端：准入、目标转送与受理证据

- 固定 TS24.282 V16.13.0（2026-02），普通在网、直接 MCData ID 私聊 HTTP FD 的服务器信令责任；主请求为 one-to-one-fd 的 FD SIGNALLING PAYLOAD，不覆盖组、功能别名、媒体面 FD、终止/延期列表或完整存储服务器 HTTP 实现。格式错误拒绝不以输入已经合格为前提。
- O-PF、CF、T-PF 的接收、继续处理和响应是各自事件；网络通知仅适用条目明确列出的 T-PF 接收分支。不得把有效绑定、通过发送许可、目标已接收或已下载作为全页共同前提。
- 服务器仍须满足5.3的适用密钥材料复制义务；MIME封装和适用XML保护按6.4、6.5.1.1–4，接收验证/解密在其他处理之前。本页不验收外部SIP、配置schema或完整安全实现。

## O-PF先核主叫身份并选CF，再按实际守卫映射发送拒绝

适用：O-PF实际收到6.3.1.1所分类的HTTP FD请求；或实际收到自己向CF所发MESSAGE的响应。后续步骤仅在前序未停止时执行。

O-PF可因资源不足或拥塞风险用500拒绝，可带Retry-After，并停止。它从PAI中的公共用户身份确定主叫MCData ID并授权；缺绑定或绑定过期返回404/Warning141并停止。若有mcdata-controller-psi就采用该值，否则本页one-to-one-fd按主叫选择承载私聊HTTP FD的CF；无法确定CF返回404/142并停止。随后调用11.1。在controller-psi缺失的守卫下，发送许可缺失或false映射403/Warning200，超过MaxData1To1映射403/202，出站名单存在且含一个或多个entry且目标不匹配映射403/229，各拒绝均停止。继续时新建MESSAGE，Request-URI设为所选CF PSI，复制全部入站MIME，填主叫MCData ID，使用FD的P-Asserted-Service并保留入站PAI。对实际收到的202或200分别生成同码回客户端；实际收到4xx/5xx/6xx则保留收到的Warning并转送。

规范强度：条件检查、拒绝/停止、构造及响应为SHALL；资源拒绝及Retry-After为MAY。

- controller-psi存在不等于11.1无需执行，也不能将step7的具体拒绝映射无条件扩大。11.1另列私聊FD文件大小检查，但这里step7未给该项独立映射；不借SDS错误码补齐。
- 本页不覆盖主叫功能别名的step10A；不能把该分支当被叫目标解析。这里Warning202不是SIP202。

依据：TS24.282 V16.13.0 §6.3.1.1 HTTP FD O-PF/CF/T-PF classification，印刷页46,47（规范依据）；TS24.282 V16.13.0 §10.2.4.3.1 full; step10A comparison only，印刷页166,167,168（规范依据）；TS24.282 V16.13.0 §11.1 steps1,1A,4,7,12，印刷页187,188,189（规范依据）；TS24.282 V16.13.0 §5.3, 6.4, 6.5.1.1–4，印刷页37,55,56,57（适用的公共服务器/MIME/安全义务）。

## CF先处理排队和文件URL校验，再选唯一直接目标

适用：CF收到HTTP FD请求，或决定处理此前排队的同类请求；检查失败、排队与继续处理分开适用。

CF资源不足或有拥塞风险时可用500拒绝（可带Retry-After）或排队。已排队时回202/Warning215并停止本节，不继续当作已转给目标。未排队继续检查所需mcdata-info和mcdata-signalling正文；缺所需正文拒绝403/199。需只有一个FD SIGNALLING PAYLOAD或FD HTTP TERMINATION消息，否则403/209；需只有一个Payload IE，否则403/210；载荷类型非FILEURL则403/211，URL所指文件不存在则403/212，均停止。本页PAYLOAD有FD disposition request type时保存Conversation ID和Message ID用于关联；有Metadata时按其中可用性与max-file-availability的较小值确定TDC2值，无Metadata则用default-file-availability。私聊缺resource-lists或含多个entry返回403/205并停止；PAYLOAD且恰好一个entry时，实际调用10.2.4.4.1向该用户转送。继续到step13–16时，为PAYLOAD启动并关联TDC2，再向O-PF返回202；它不是目标已下载的证据。

规范强度：上述条件检查、拒绝/停止、保存、转送、计时和202为SHALL；资源拒绝/排队及Retry-After为MAY。

- step10未给存在resource-lists但零entry的同一拒绝分支，不能将零entry静默改写为缺失或多entry；也不能据此认为零entry可以转送。
- 此版本step7b要求文件存在但未在该步指定HTTP HEAD算法，本页不从其他Release补取证方法。Metadata的file-availability是日期时间，而step9把其用于timer value比较；本页保留这一表达，不另定换算公式。
- 只记录TDC2启动/关联，未展开到期生成通知、文件删除、重试或完整释放；不将这里202与排队202/215混为同一事件。

依据：TS24.282 V16.13.0 §10.2.4.4.2 opening,steps1–10,13–16; steps11–12,17–18 comparison only，印刷页170,171,172,173（规范依据）；TS24.282 V16.13.0 §15.2.17 Metadata，印刷页243,244（规范依据）；TS24.282 V16.13.0 §5.3, 6.4, 6.5.1.1–4，印刷页37,55,56,57（适用的公共服务器/MIME/安全义务）。

## CF转送前有条件决定自动下载，并保持目标与主叫身份分工

适用：CF的10.2.4.4.2 step10b已选定本页唯一直接目标并调用10.2.4.4.1；11.2调用仅适用于收到的FD SIGNALLING PAYLOAD没有Mandatory download IE。

CF新建MESSAGE，设置FD的Accept-Contact及ICSI并带require/explicit，按6.4复制mcdata-info和mcdata-signalling。无Mandatory download IE时执行11.2：有Metadata从fileselector取得文件大小，没有则确定URL所指文件大小；私聊文件大小不大于max-data-size-auto-recv-bytes时，须在出站PAYLOAD加入MANDATORY DOWNLOAD。它将mcdata-request-uri改为目标MCData ID，Request-URI设为目标T-PF PSI，复制主叫的PAI，携FD的P-Asserted-Service后发送。主叫身份、目标业务身份和下一跳服务身份不是同一字段。

规范强度：构造、按条件调用11.2、判定及条件满足时加入IE均为SHALL。

- 未通过自动接收阈值不等于拒绝文件分发，也不能把接收端后续用户决定替换成发送许可。原请求已有Mandatory download IE不重复执行这里的缺IE分支。
- 5.3要求在适用分发密钥材料的程序中保证复制；不能因为本地step4列出两个正文就推断密钥必然被丢弃。转送完成不等于终端执行下载成功。

依据：TS24.282 V16.13.0 §10.2.4.4.1 full;10.2.4.4.2 step10b actual caller，印刷页169,170,171（规范依据）；TS24.282 V16.13.0 §11.2 full; group threshold comparison only，印刷页189（规范依据）；TS24.282 V16.13.0 §15.2.16–17，印刷页243,244（规范依据）；TS24.282 V16.13.0 §5.3, 6.4, 6.5.1.1–4，印刷页37,55,56,57（适用的公共服务器/MIME/安全义务）。

## T-PF另核目标绑定与入站名单；返回200只对应实际MESSAGE

适用：T-PF收到HTTP FD请求，或收到HTTP FD网络通知；保存payload仅适用带FD disposition request type的请求，过期删除仅适用条目列出的网络通知。响应分支仅在实际收到自己出站MESSAGE的对应响应时适用。

T-PF可因资源/拥塞用500拒绝，可带Retry-After并停止。它用mcdata-request-uri中的目标MCData ID检索公共用户身份绑定，缺绑定返回404并停止。收到带FD disposition request type的PAYLOAD请求时保存Conversation ID、Message ID和payload；收到FD NETWORK NOTIFICATION且类型为FILE EXPIRED UNAVAILABLE TO DOWNLOAD时，用Conversation ID标识文件并从存储列表删除。之后按6.3.2.1构造给终端的MESSAGE，复制收到的Accept-Contact/Reject-Contact，Request-URI设为目标公共用户身份并保留PAI。入站名单存在且有一个或多个entry、主叫ID不匹配任何entry、并且未配置允许任意来源时，返回403/Warning230并停止；不满足这组共同条件不能据此拒绝。继续时携FD P-Asserted-Service发送。实际收到终端200时生成200回CF；收到4xx/5xx/6xx则保留Warning转回CF。

规范强度：条件绑定检查、拒绝/停止、保存/删除、构造及响应为SHALL；资源拒绝和Retry-After为MAY。

- T-PF这里缺绑定为404，不把O-PF的过期判定或Warning141默默加进来。入站名单为空也不能直接当成230拒绝。
- 10.2.4.3.2将过期通知值指向15.2.6，但该条是下载处置类型；15.1.9表把网络通知指向15.2.18，后者列过期/删除类型。本页保留此回指差异，不构造修正后的编码算法；原文两处step5也不重编号。
- 这里不展开网络通知的产生链或反向FD disposition路由。客户端200先于处理下载决定；也未由本页建立“终端200必然转换成发起端200”的完整CF响应链。

依据：TS24.282 V16.13.0 §6.3.1.1 FD request/network notification classification，印刷页46,47（规范依据）；TS24.282 V16.13.0 §10.2.4.3.2 full，印刷页168,169（规范依据）；TS24.282 V16.13.0 §6.3.2.1 full，印刷页49（规范依据）；TS24.282 V16.13.0 §15.1.9 table15.1.9.1-1，印刷页232（规范依据）；TS24.282 V16.13.0 §15.2.6;15.2.18 tables，印刷页238,239,244（过期回指比较）；TS24.282 V16.13.0 §10.2.4.2.2 steps1–5，印刷页166（客户端200证据边界）；TS24.282 V16.13.0 §5.3, 6.4, 6.5.1.1–4，印刷页37,55,56,57（适用的公共服务器/MIME/安全义务）。

## 使用边界

- 本页是HTTP FD信令服务器职责，不验收文件存储HTTP上传/GET、客户端完整下载、配置默认值、端到端保护或外部队列调度。
- 服务器可以拒绝收到的请求；客户端已通过自己的发送检查不是服务器处理请求的前提。

要区分终端的 SIP 应答、下载决定与 HTTP 下载结果，见[私聊 HTTP 文件分发客户端](http-fd-client.md)。
