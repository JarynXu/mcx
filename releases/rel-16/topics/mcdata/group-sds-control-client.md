# 预安排组 standalone SDS 控制面：客户端发送、接收与处置

## 适用范围

- 固定 TS24.282 V16.13.0（2026-02）Rel16；普通在网预安排组 standalone SDS 控制面客户端责任，不含组会话、ad hoc创建、MBMS或完整服务器分发。
- 按发送、接收、内容处理和通知的实际角色/事件分别适用；许可通过或200不是全页共同前提，后续处理只在相应前序未停止时适用。
- MIME封装与适用XML保护按6.4及6.5.1.1–4；接收完整性验证/解密先于其他处理，失败停止。6.6.3.1–2依实际协商保护数据，组DPPK使用GMK/GMK-ID，不能套私聊PCK。签名数据还须验证签名；完整密码、密钥管理和配置schema仍是外部依赖。

共同依据：TS24.282 V16.13.0 §6.4、6.5.1.1–4、6.6.3.1–2，印刷页55–57、65。

## 先核组发送资格，再选择控制面

条件：用户要向预安排组发送普通 standalone SDS；尚未假定许可通过。

11.1 按组身份检查：组内发送许可 mcdata-allow-transmit-data-in-this-group 缺失或 false 时停止；数据超过组 mcdata-on-network-max-data-size-for-SDS，或 payload 超过该组 entry 的 mcdata-max-data-in-single-request 时也停止。只有发送控制成功且 payload 不超过服务配置 max-payload-size-sds-cplane-bytes，才调用控制面发送；超过该阈值转媒体面入口，并非自动拒绝。

强度：11.1停止及阈值分派为 SHALL；9.1组服务关闭为 SHOULD NOT。

- 9.1 对组 mcdata-allow-short-data-service=false 的客户端要求为 SHOULD NOT 发送；不能把此强度或字段与下一构造步骤的 AllowedSDS=false SHALL 拒绝合并。
- 本入口明确 pre-arranged group，不据此支持临时成员列表或任意 ad hoc 组创建。SDS session 是9.2.1.1另一个调用分支；其许可不能当 standalone 的共同条件。
- 私聊 allow-transmit-data、目标名单、MaxData1To1 及私聊服务级 SDS 上限有各自 one-to-one 守卫，不移植为组规则。

依据：3gpp-ts-24.282-v16.13.0 §9.1;9.2.1.1；11.1 steps2,5,8,12;other branches comparison-only，印刷页105,106,187,188,189。

## 组身份不等于 SIP 请求目的地址

条件：实际通过发送控制并进入9.2.2.2.1组控制面构造；AllowedSDS检查仍待执行。

若请求组文档中的 /<x>/<x>/Common/MCData/AllowedSDS 存在且为 false，拒绝发送并停止。继续时，mcdata-info携 group-sds、目标 MCData group identity 和发起 client ID；SIP Request-URI 则是服务本用户的 PF 公共服务身份。6.2.4.1 设置 SDS 服务标签及 P-Preferred-Service，P-Preferred-Identity可选。6.2.2.1生成独立 signalling 与 data payload MIME，设置当前时间、会话标识和新 Message ID；回复另带原消息的 InReplyTo。用户内容不带应用ID；应用内容带对应 Application ID 或 Extended application ID。

强度：构造及false拒绝为SHALL；P-Preferred-Identity为MAY，功能别名以两项条件为守卫。

- AllowedSDS 仅明确 false 拒绝，不把缺失擅改为 false；配置 schema 和默认值仍是外部依赖。
- 活跃功能别名只有客户端知晓且决定携带时才加入，不是目标组身份的替代。文本编码仍按6.2.2.1的客户端/组字符集条件选择 TEXT 或 CODED TEXT，不在本页重建二进制编码器。
- 私聊分支的 resource-lists 与 PCK/MIKEY构造不能改名作为组加密算法；组数据保护另按共同保护条件。

依据：3gpp-ts-24.282-v16.13.0 §9.2.2.2.1 steps1,3–5;step2 comparison-only；6.2.4.1；6.2.2.1，印刷页40,41,44,45,108,109。

## 先应答事务，再处理内容；应用过滤另有结果

条件：终端实际收到按6.2.1.1分类的standalone SDS MESSAGE，或随后进入其内容处理；不要求资源和保护预先成功。

分类要求 Accept-Contact 的 g.3gpp.icsi-ref 与 P-Asserted-Service 均为 SDS ICSI。资源不足时可拒绝，若拒绝则返回480并停止。若实际携MIKEY，须按接收步骤验证，认证失败返回606/136并停止。前序未停止才发送200，然后调用9.2.1.2。解码后按Conversation ID和InReplyTo建立关联；无两类应用ID时面向用户呈现，用户通知为可选；有应用ID时不通知用户，未知应用丢弃，已知应用交付。因此200不证明呈现、阅读或应用接受。

强度：资源不足拒绝及用户提醒为MAY；一旦拒绝的480停止、条件MIKEY验证、200与内容分派按SHALL。

- 这里只核客户端实际接收入口，不将发送者的组许可作为接收前提，也不把用户内容与应用内容分支强行同时执行。
- 该接收程序没有在这些步骤另列按本机组名单过滤的算法；不能据此推定服务器成员筛选已成功，或将私聊入站名单当组客户端过滤。
- 条件存在MIKEY的接收步骤保留；不能反推普通组发起必须按私聊分支生成MIKEY。

依据：3gpp-ts-24.282-v16.13.0 §6.2.1.1；9.2.2.2.2；9.2.1.2，印刷页38,39,106,107,109,110。

## 组处置通知保留组关联，不等于全组完成

条件：实际处理本组消息的处置请求、不能交付事件、显示事件或计时器事件，或实际收到SDS NOTIFICATION；各事件独立适用。

DELIVERY请求生成送达通知；READ等待显示指示。DELIVERY AND READ启动TDU1：先显示则停止计时器并合发，先到期则先发送达，后显示再发已读。通知的目标用户取原mcdata-calling-user-id，组关联取原mcdata-calling-group-id；新MESSAGE经PF发送，resource-lists携目标用户并保留组关联。SDS NOTIFICATION复用原Conversation ID与Message ID；不能交付用户或应用时类型为UNDELIVERED。收到相应通知时解码并交付用户或应用，不能由单个通知推定全组完成。

强度：规定动作 SHALL；条件不满足不能推定已执行。

- 通知分类除SDS服务标识外还要求signalling body含SDS NOTIFICATION，不能把所有SDS MESSAGE都当回执。全组目标选择、聚合、重投和服务器回程未在本页验收。
- 本页没有从这些客户端程序取得已发送standalone组SDS的撤回算法；媒体BYE以已建立媒体通信为入口，FD HTTP TERMINATION属于FD，不移植为本页取消。SIP事务错误/取消的外部规则也未据此补全。

依据：3gpp-ts-24.282-v16.13.0 §9.2.1.3；12.1;12.2.1.1–2；6.2.3.1;6.2.4.1；6.2.1.1 notification classifier；13.2.2.2.2.1–2 (media release comparison-only)；6.2.2.4 (HTTP FD termination comparison-only)，印刷页39,42,43,44,45,107,108,191,192,202,203。

## 使用边界

- 6.6.3.2对数据signalling保护写CPK/CPK-ID，本页保留字面依赖，不把它改成其他密钥名或补完整安全算法。
- 旧私聊主题有自身one-to-one条件，不能通过链接继承为组客户端规则。
