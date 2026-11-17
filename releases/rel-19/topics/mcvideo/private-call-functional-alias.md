# 在网私呼拨功能别名：权限、目标选择与 300 重试

TS 24.281 V19.3.0 的普通在网按需、传输控制型（TC）私呼；初次目标为一个 functional alias，后续 300 重试以返回的单个 MCVideo ID 为目标。

不涉及紧急、紧急警报、FTA、跨域、remote、ambient listening、push/pull、预建立会话、Replaces 或 Resource-Priority；不含强制自动接续。

客户端、O-PF 和 CF 的声明分别按自己的接收事件与字段条件适用；没有把成功解析、权限通过或终接接受设为所有分支的共同前提。

以下条件成立时，各过程执行所列 SHALL 动作。实现自选策略只限原文明确留给实现的部分。

## 先区分被叫别名与主叫别名

发起 MCVideo 客户端收到用户建立普通私呼的请求，邀请对象为一个 functional alias。

客户端按私呼条款生成初始 INVITE：Request-URI 为服务自身的 O-PF PSI，resource-lists 的唯一 entry uri 为被叫 functional alias，mcvideo-info+xml 中 session-type=private，并在 anyExt 放入 call-to-functional-alias-ind=true。客户端需要携带自身 active functional alias 时，另用 functional-alias-URI；该字段不是被叫目标。非强制自动接续时，按用户请求的自动或手动模式分别携带 Answer-Mode=Auto 或 Manual。

这些是识别别名私呼的字段，不替代其余 SIP/SDP 构造要求；不覆盖 Priv-Answer-Mode 强制自动分支。

来源：TS 24.281 V19.3.0 §10.2.2.2.1 steps 1,7,11(b,c),13，印刷页 325, 326。

## 目标是别名仍需通过发起权限检查

O-PF 收到 session-type=private 的初始 INVITE；到达相应检查前未被前序检查拒绝。以下各项分别以自己的字段和配置条件判断，不要求所有拒绝条件同时成立。

allow-private-call 缺失或为 false 时，返回 403 + Warning 107 并停止。请求 Auto 时若 allow-automatic-commencement 缺失或为 false，返回 403 + 125；请求 Manual 时若相应 allow-manual-commencement 缺失或为 false，返回 403 + 126，均停止。PrivateCall 列表存在且至少一个条目、目标 resource-lists URI 不匹配且无列表外呼叫许可时，返回 403 + 144 并停止。另一个独立检查是：call-to-functional-alias-ind=true、请求携带主叫 functional-alias-URI，且该主叫别名的 FunctionalAliasList 内 ListOfAllowedFAsToCall 存在并至少一个条目；若目标 URI 未匹配，返回 403 + 171 并停止。

没有主叫 functional-alias-URI 不能据此触发 11A 的 171 分支，但仍须通过其他检查；别名标记不豁免身份绑定、单目标和 codec 等检查。

当请求通过检查而进入转发步骤 17a 时，O-PF 只在所带主叫别名确实对该 MCVideo ID 激活时复制 functional-alias-URI，否则省略；这里不展开激活状态取得过程。

来源：TS 24.281 V19.3.0 §10.2.2.3.1.1 steps 10,11(a-c),11A，印刷页 333, 334；TS 24.281 V19.3.0 §10.2.2.3.1.1 step 17a，印刷页 334, 335。

## CF 查询激活用户，但请求与接收契约存在缺口

CF 处理普通 private INVITE，call-to-functional-alias-ind=true，前序准入、单目标和媒体检查未拒绝，进入 §10.2.2.4.2 step 7a(a)。

CF 按 §20.2.2.2.8 识别已激活被叫别名的用户。该 helper 构造初始 SUBSCRIBE：Request-URI 指向处理该别名的控制功能 PSI，mcvideo-request-uri 为该 functional alias ID，P-Asserted-Service 为 MCVideo ICSI，Expires=0，Accept=application/pidf+xml；正文为指向该别名的 per-functional-alias simple-filter。该条将 presence 头名称写为 Events。

PSI 发现不在该 helper 范围。该条到构造请求结束，没有列出接收 NOTIFY 并提取用户 ID 的完整处理。

接收侧 §20.2.2.3.4 要求 mcvideo-calling-user-id，以及与该 ID 匹配的 per-user filter，头名写 Event；发送 helper 未列该 calling-user-id，且使用 per-functional-alias filter。两侧条件不能静默拼接成已闭合查询交换，也不能把 Expires=0 改成长订阅。

来源：TS 24.281 V19.3.0 §10.2.2.4.2 step 7a(a)，印刷页 345；TS 24.281 V19.3.0 §20.2.2.2.8，印刷页 490, 491；TS 24.281 V19.3.0 §20.2.2.3.4 receiver conditions 1-5，印刷页 494, 495。

## 一个或多个已识别用户都返回单目标 300

CF 的普通 private 请求满足 call-to-functional-alias-ind=true，前序检查未拒绝；进入 §10.2.2.4.2 step 7a 后，分别处理无法识别任何用户 ID，或已识别至少一个用户 ID 的结果。

无法识别任何 MCVideo ID 时，CF 返回 403 + Warning 145 并停止。识别出至少一个时，CF 选择其中一个 ID，返回 300 并停止本条其余过程；选择方式由实现决定。300 的 Contact 是 MCVideo session identity 的 SIP URI；application/vnd.3gpp.mcvideo-info 正文中 mcvideo-request-uri 才是所选 MCVideo ID。300 不以存在多个候选为必要条件，也不是向所有激活用户同时邀请。

查询契约缺口意味着这里是对已取得识别结果的条件式处理，不承诺任意 helper 请求一定取得有效结果。

7a 返回 300 并停止，而后面的 step 10 才列分配 session identity；该 300 所用 session identity 的取得时机未闭合，不补造提前分配或复用已有会话的步骤。

来源：TS 24.281 V19.3.0 §10.2.2.4.2 step 7a(a-c), NOTE 1, step 10，印刷页 345, 346。

## 客户端用正文 ID 重发，并保留被叫别名上下文

发起客户端收到针对该别名初始 INVITE 的 SIP 300 响应，其中正文包含 mcvideo-request-uri。

客户端把该 mcvideo-request-uri 中的 MCVideo ID 作为邀请对象，依同一私呼条款生成新的初始 INVITE。resource-lists entry uri 改成所选 ID；anyExt 不得包含 call-to-functional-alias-ind，且须包含 called-functional-alias-URI，值为初次请求使用的被叫别名 URI。这里使用正文 ID，不把 Contact 的 session identity 当作被叫 ID。

O-PF 对不含 SDP 的其他 SIP 响应要求连同 MIME 正文沿信令路径转发；这只支持满足该条件的 300 转发，不推断含 SDP 响应走同一分支。

新 INVITE 仍受相应准入和终接模式检查。300 只提供重试目标，不证明终接接受、会话已建立或视频已送达；省略标记不等于发送标记 false。

来源：TS 24.281 V19.3.0 §10.2.2.2.1 receipt of SIP 300 steps 1-3，印刷页 326, 327；TS 24.281 V19.3.0 §10.2.2.3.1.1 other SIP responses without SDP，印刷页 335。

## 范围边界

仅覆盖别名目标如何进入私呼、受到权限约束、获得条件式选择结果并重试；不覆盖别名激活/停用生命周期、完整发现、安全或所有 SIP 错误处理。

不展开 TS 24.581 媒体/传输控制内部过程；不能由目标选择推断视频传输许可或送达。

直接 MCVideo ID 私呼页仅作其他入口的比较，不继承其排除别名的共同条件。

来源发布方：[ETSI](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)。
