# SDS会话逐消息发送：媒体就绪、许可与构造入口

## 适用范围

- 固定TS24.582 V19.0.0，普通在网单播one-to-one或组SDS session客户端发送；24.282 V19.7.0仅按所列caller和对象条款对照，不宣称两个快照完整互通。
- 各claim按实际角色、事件和待检查条件使用；不将许可已通过、全体连接已成功或消息已交付作为全页共同前提。
- 不含standalone发送生命周期、离网、FD、IPCONN、MBMS/MBS、ad hoc与预建立复用的额外条件，也不提供完整RFC传输、安全或重传实现。

## 原会话发起者不是唯一发送者，首个MSRP事件仍须分别判断

**条件：** 普通在网单播one-to-one或组SDS session；客户端已按自身信令分支进入建立媒体连接的事件。主叫、终接客户端及active/passive端点按实际角色分别判断，不要求所有角色同时完成。

会话中具有适当权限的用户可以发送SDS，不限于会话原发起用户。主叫按收到SDP answer的setup选择端点角色并建立连接，作为active时先发空MSRP SEND绑定连接；§6.1.2.2.1在收到首个SEND的MSRP200后允许生成、发送SDS或所请求的通知。终接客户端按收到的SDP offer建立连接：作为active时收到首个SEND的200，或作为passive时对收到的首个SEND发出200，才到该段明确的发送入口。这些是进入逐消息发送过程的媒体事件，仍须执行下一条的许可与大小门槛。

**规范强度：** 连接处理明确动作是SHALL；首个事件后原文为can；无发送权限不应使用过程为SHOULD NOT，不能统一改成全部SHALL。

- 信令调用只表示进入媒体过程：24.282 §9.2.4.2.3的INVITE2xx分支发送ACK、启动session timer并调用24.582 §6.1.2.2；终接§9.2.4.2.4以前序未停止、已发送INVITE200且收到其ACK为媒体调用事件。SIP200或ACK不能替代首个MSRP事件。
- 主叫段没有像终接段那样明列passive端发送首个200的替代入口。本页不补对称规则，也不据此断言主叫passive永远不能发。RFC连接细节与此分支完整性不在本页解决。
- §6.1.2.1对无发送权限客户端采用should not使用这些过程；不能将有媒体连接误当获得发送许可。普通会话范围不自动推广为ad hoc、预建立复用、紧急扩展或MBMS。

**依据：**
- [TS24.582 V19.0.0 §6.1.2.1;6.1.2.2.1;6.1.2.3.1](https://www.etsi.org/deliver/etsi_ts/124500_124599/124582/19.00.00_60/ts_124582v190000p.pdf)，印刷页 16,17,18；规范依据。
- [TS24.282 V19.7.0 §9.2.4.1;9.2.4.2.3 2xx response;9.2.4.2.4 ACK event](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 224,228,231；实际信令caller比较；不替代媒体就绪。

## 每条SDS按私聊或组分别检查许可和两个大小上限

**条件：** 客户端准备在SDS session中按§6.1.2.4发送一条SDS；媒体连接就绪按上一条实际角色事件成立。许可与大小是否满足是本条待判断内容，不先假定全部通过。

one-to-one发送只在三项同时满足时被允许：用户profile的actions内allow-transmit-data存在且为true，消息大小不超过服务配置max-data-size-sds-bytes，且不超过用户profile的MaxData1To1。组发送则要求该组文档action内mcdata-allow-transmit-data-in-this-group存在且为true，消息大小不超过mcdata-on-network-max-data-size-for-SDS，且不超过相应entry的mcdata-max-data-in-single-request。某项恰好等于上限只满足该大小比较，不能代替另外的比较或许可。会话已建立、用户是原发起者、上一条成功均不能免除这次发送条件。

**规范强度：** 原文only if限定发送许可；条件全部满足后才执行后续SHALL构造及发送，不把每个不满足分支改写为规范未列的协议拒绝响应。

- 本条来自媒体规范自己的session caller，不把24.282 standalone控制面分流阈值搬过来，也不新增缺省上限、配置缺失时的允许值或“换媒体即可绕过大小限制”。
- 字段名称按24.582保留，组action与私聊actions不自行统一。24.481/24.484文档获取、schema与默认值未在此展开；本条没有为不满足条件补SIP/MSRP错误码或会话自动释放。

**依据：**
- [TS24.582 V19.0.0 §6.1.2.4 permission and size conditions](https://www.etsi.org/deliver/etsi_ts/124500_124599/124582/19.00.00_60/ts_124582v190000p.pdf)，印刷页 18；规范依据。

## 条件满足后构造本条消息，不借standalone的成功收尾

**条件：** §6.1.2.4中适用的私聊或组发送条件均满足，并在已建立的MSRP连接上生成该条SDS。仅按本条调用的构造helper解释，不把通用helper的其他输入分支自动选为session发送方案。

客户端分别调用§6.1.1.2.2和§6.1.1.2.3生成SDS SIGNALLING PAYLOAD与SDS DATA PAYLOAD，再按§6.1.1.2.4将两者放入MSRP SEND。信令正文的MIME为application/vnd.3gpp.mcdata-signalling，数据正文为application/vnd.3gpp.mcdata-payload；多正文按§6.4.1使用multipart/mixed及边界。session caller特别要求To-Path取收到SDP中的MSRP URI，再在已建立连接发送。数据helper的Number of payloads记录本条发送的payload数量，不是会话里发过多少条SDS；消息的生成、发送与收件人交付或已读仍是不同证据。

**规范强度：** 条件满足后的生成、封装、To-Path及发送为SHALL；不从发送动作推导对方交付或读取成功。

- §6.1.1.2.4还列仅信令或仅数据正文的输入分支，但§6.1.2.4本身明确生成两种payload。本页不因helper有单正文分支，就省掉此caller要求的一种payload。
- 24.282 §15.1.2和§15.1.4另定义信令/数据对象，后者含保护payload相关条件。本文不是完整二进制或安全封装配方，也不保证两个固定快照的全部接口兼容；应用标识、回复关联、UUID及保护编码仍按各自helper和外部依赖处理。
- 本条调用的是构造helper，不是standalone §6.1.1.2.1整套生命周期，不能搬入其成功200后终止SIP的动作。24.282 session媒体失败指示的BYE是另一事件；通知或释放只在相关页的事件与范围成立时使用，不作为本次SEND后的必走成功步骤。

**依据：**
- [TS24.582 V19.0.0 §6.1.2.4 steps1–4;6.1.1.2.2–6.1.1.2.4;6.4.1](https://www.etsi.org/deliver/etsi_ts/124500_124599/124582/19.00.00_60/ts_124582v190000p.pdf)，印刷页 14,15,18,26；规范依据。
- [TS24.282 V19.7.0 §15.1.2.1;15.1.4.1 and NOTES](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 352,353,354；对象及payload数量/保护依赖边界。
- [TS24.582 V19.0.0 §6.1.1.2.1 successful MSRP response](https://www.etsi.org/deliver/etsi_ts/124500_124599/124582/19.00.00_60/ts_124582v190000p.pdf)，印刷页 13；comparison-only：standalone成功释放不可移植。
- [TS24.282 V19.7.0 §9.2.4.2.3 unsuccessful media indication](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)，印刷页 228,229；comparison-only：session失败释放为另一事件。

## 使用边界与关联

- 本页负责客户端何时进入逐消息发送以及应检查什么，不负责服务器整链准入、对端交付证明或完整会话释放。
- [SDS session后续证据](sds-session-message-evidence.md)：按其普通私聊/配置组、实际媒体失败或媒体释放后通知事件解释，不把SEND当整链成功。
- [SDS session带内通知](sds-session-inband-notification.md)：只有已建立且满足其发送许可/大小等共同条件，并到达实际收到内容或通知事件时适用；不是本条发送动作的无条件成功后续。
