# MCData HTTP FD：被叫功能别名解析与单目标重建

固定 TS24.282 V19.7.0，普通在网、本地 one-to-one FD using HTTP 的被叫功能别名信令；不含组 FD、媒体面 FD、HTTP TERMINATION 或别名激活管理。

客户端发起、PF 转发、CF 处理及客户端收到 300 是不同角色和事件入口，分别依本条条件适用；前序要求停止时不得继续，不预设全链已成功。

本页只核目标解析与重建责任。文件上传、接收决定、下载、安全上下文和完整 SIP 事务仍有各自条件，不由一个已选 ID 代替。

## 初始请求把被叫别名与路由、主叫别名分开

适用条件：客户端按 §10.2.4.1 完成适用文件大小检查与上传步骤，进入 §10.2.4.2.1，目标为一个被叫功能别名。

客户端生成 SIP MESSAGE，在 resource-lists 的 entry.uri 放被叫别名，mcdata-info+xml 的 request-type 为 one-to-one-fd，anyExt/call-to-functional-alias-ind 为 true。§6.2.4.1 的 Request-URI 指向服务本用户的 PF PSI，使用 FD 服务标签和 FD ICSI；被叫别名不替换这一路由地址。客户端按 §6.2.2.2 生成 FD SIGNALLING PAYLOAD，Payload IE 的类型为 FILEURL，数据为文件 URL，再发送。

- functional-alias-URI 是客户端知道并要携带的活跃主叫别名，与被叫 entry.uri、call-to-functional-alias-ind 不同。PF §10.2.4.3.1 step10A 核的是主叫别名激活状态，句内字面写 outgoing SIP INVITE；本页不把它当被叫解析，也不静默修正请求方法。
- 这里记录构造 helper 的实际调用，不是完整二进制编码模板。§6.2.2.2 另有新/已有 conversation、Message ID、应用标识、下载要求及可选 metadata 等条件，不能把整包原样复用当通则。
- 上传前置和目标选择分属不同步骤。§10.2.2.1 对需要端到端安全的 one-to-one 文件规定上传前保护二进制；本页不由后续 300 反推已解决所选用户的密钥绑定或重加密。

规范强度：所述地址、被叫标志、FD payload 构造及发送为 SHALL；本条不将 helper 的可选字段变为必填。

依据：TS24.282 V19.7.0 §10.2.4.1;10.2.4.2.1 steps1,2,4,5，印刷页275,276,277（规范依据）。
依据：TS24.282 V19.7.0 §6.2.4.1 steps2–4，印刷页61（请求构造依赖）。
依据：TS24.282 V19.7.0 §6.2.2.2，印刷页57,58（FD payload 构造依赖）。
依据：TS24.282 V19.7.0 §10.2.4.3.1 step10A，印刷页279（主叫别名对照及源文方法边界）。
依据：TS24.282 V19.7.0 §10.2.2.1 UE-stored file step7，印刷页272（上传安全前置边界）。

## CF先过HTTP请求门槛，再选一个已激活用户

适用条件：CF实际收到 §10.2.4.4.2 的 HTTP FD 请求，或决定处理此前排队请求；本页解析分支为 one-to-one-fd、FD SIGNALLING PAYLOAD，call-to-functional-alias-ind=true。以下按步骤顺序处理，拒绝或排队停止不预先排除在条件外。

CF 可因资源不足或拥塞回 500 或排队；已排队时回 202/Warning215并停止本次余下步骤。继续时先核必需 MIME、单个 FD 消息、单个 Payload IE、FILEURL 和文件存在性，所列不符合分别触发403/199、209、210、211、212并停止；按条件记录 disposition 关联 ID、处理 metadata/可用期后才到 step10。one-to-one 请求缺 resource-lists 或名单总计超过一个 entry 时，回403/205并停止。标志为 true 时调用 §22.2.2.2.8 查已激活该别名的 MCData ID；没有可确定 ID 时回403/145并停止。否则从结果选择一个 ID，以300的 mcdata-info 中 mcdata-request-uri 返回，并停止本节余下步骤，不能继续给所有激活者发送文件请求。

- 205 的明确条件是名单缺失或超过一个 entry；不补“存在名单但零 entry”的错误码或成功行为。选择哪一个 ID 由实现决定，不补排序、轮询或群发策略。
- §6.7.3 的文件存在性检查是带有效访问令牌的 HTTP HEAD；200/404分别进入可用/不可用处理。它不是 GET 下载，不把其他 HTTP 错误自行全部映射成403/212。
- §22.2.2.2.8 的查询使用初始 SUBSCRIBE，Request-URI 为关联别名的 CF PSI，mcdata-request-uri 为别名，presence/per-functional-alias filter 与 PIDF 用于取得激活状态。step4要求 Expires=0，NOTE6允许为当前及后续通知请求4294967295；不是调用时必然长期订阅。
- 解析 helper 的 PSI 发现算法不在其范围内；其头字段字面写 Events，接收 NOTIFY 段又以 MCData client 为主语。这里保留调用和结果边界，不给出可直接执行的过滤 XML、完整查询权限或服务器接收状态机。
- 300 分支明确停止，不能再顺着后文202或投递步骤认定文件已获接受。可用期和 disposition 的记录也不证明下载完成。

规范强度：资源500、排队及 Retry-After 为 MAY；所列检查、拒绝、解析调用、300响应及停止为 SHALL；选人算法由实现决定。

依据：TS24.282 V19.7.0 §10.2.4.4.2 opening,steps1–10b and NOTE3，印刷页281,282,283（规范依据）。
依据：TS24.282 V19.7.0 §6.7.3.1;6.7.3.2，印刷页135（文件存在性实际依赖）。
依据：TS24.282 V19.7.0 §22.2.2.2.8，印刷页488（被叫别名解析实际依赖及字面边界）。

## 收到300后另建直接ID请求，不能据此宣告交付

适用条件：客户端实际收到初始 HTTP FD SIP MESSAGE 的300响应，内含该段指定的 mcdata-request-uri；PF/CF处理新请求时按各自入口重新适用要求，不假定初次解析已替其授权。

客户端以响应中的 MCData ID 作为被邀请用户，按 §10.2.4.2.1 另建 SIP MESSAGE：resource-lists entry.uri 改为该 ID，anyExt 不再包含 call-to-functional-alias-ind，并用 called-functional-alias-URI 保留初始被叫别名。新请求仍按同节调用 FD payload 构造，不是把原事务当作已投递。实际进入 CF 时仍需走 HTTP 请求门槛；未被前序停止、符合 step10c 的 FD SIGNALLING PAYLOAD 与恰好一个目标 entry 条件时，才调用 §10.2.4.4.1 发往该用户。

- PF §10.2.4.3.1 重新适用资源、绑定、CF确定及按条件执行的发送许可检查。无绑定或过期回404/141，无可确定CF回404/142；不能由别名查到ID推导发送许可已通过。这里不展开 §11.1 的配置算法。
- PF响应段明确列200、202、4xx/5xx/6xx，未单列300转发。本页分别确认CF生成300和客户端收到300后的动作，不宣称中间传递已由这些条款完整闭合，也不补回退、重试或事务调度。
- 300段的响应 MIME 字面为 application/vnd.3gpp.mcdata-info，而请求构造写 +xml；保留这一接口文字差异，不据此规定兼容转换。CF step10c 的语句还把 FD SIGNALLING PAYLOAD 与 resource-lists MIME 连写，不能据此把 XML 名单嵌进二进制 FD 消息。
- §10.2.4.4.1 的目标用户 mcdata-request-uri 与终端 PF 的 SIP Request-URI 不同；Mandatory download 缺失时另调用 §11.2。此处只确认实际下一步责任，不借私聊媒体 FD 或 SDS 页补 HTTP 接收算法。
- 300、SIP接受与文件下载完成是不同证据。本页不覆盖完整终端下载、完成通知或安全实现；不能把接收者选择当作成功交付。

规范强度：收到300后的新请求构造为 SHALL；后续PF/CF动作仍依各自守卫，资源拒绝的 MAY 不提升为必然拒绝。

依据：TS24.282 V19.7.0 §10.2.4.2.1 SIP300 paragraph and steps1–3，印刷页277（规范依据）。
依据：TS24.282 V19.7.0 §10.2.4.3.1 steps1–14 and response paragraphs，印刷页277,278,279（新请求PF入口及300中间传递边界）。
依据：TS24.282 V19.7.0 §10.2.4.4.2 steps1–10c，印刷页281,282,283（新请求实际CF caller及源文语句边界）。
依据：TS24.282 V19.7.0 §10.2.4.4.1 steps1–10，印刷页280,281（下一步目标与下载决定调用边界）。
依据：TS24.282 V19.7.0 §6.2.2.2，印刷页57,58（新请求FD构造依赖）。
依据：TS24.282 V19.7.0 §10.2.3.1 HTTP200 paragraph，印刷页275（下载成功证据对照）。

## 使用边界与相关主题

- 限HTTP FD目标解析与重建，不以SDS主题的 common_conditions 扩张为FD依据，也不覆盖媒体FD、跨域路由或别名激活管理。
- 安全、配置 schema、HTTP/RFC完整实现和查询 XML 模板不在本页核验范围；应按各自规范及业务事件继续处理。

- [fd-http-file-and-signalling-evidence](fd-http-file-and-signalling-evidence.md)：文件URL、HEAD与接受证据：仅在其HTTP角色和事件条件成立时阅读，不把300分支当202后续。
- [fd-file-availability-and-expiry](fd-file-availability-and-expiry.md)：文件可用期：仅按其metadata和计时事件使用，不能由别名选人证明文件仍可下载。
- [fd-download-decision-and-completion](fd-download-decision-and-completion.md)：HTTP下载决定与完成：只有实际进入其CF/终端/完成事件才适用，不能由300直接跳到下载成功。
