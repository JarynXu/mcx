# 普通预安排组重入与晚入：会话身份、准入和恢复证据

## 适用条件

- 固定TS24.379 V16.14.0及TS24.380 V16.9.0；普通在网按需预安排组、无implicit floor request。排除预建立、chat、临时/重组、广播、紧急/危急、ambient和完整NCF链；用户及组不处于会触发优先级程序的状态。
- 主动重入与CF收到新归属/回覆盖通知后的晚入邀请是替代入口。各请求、响应和媒体事件按其角色分别适用，不把服务器仍有会话、已授权、已归属、容量充足或收到200设为全页共同前提。
- 本页说明实际输入下的有界职责与接口。客户端需要目标session identity才能构造定向重入，但不保证身份缓存/路由/映射已恢复；拒绝路径仍在范围内。不是完整断线自动恢复、媒体重建或全组交付实现。

## 主动重入使用会话URI，组身份仍留在请求正文

条件：用户要求重入，或客户端被触发为返回覆盖；请求针对普通预安排组的既有会话身份，不要求服务器仍能找到该会话。此条不将后续准入成功设为前提。

客户端须生成initial SIP INVITE，而不是用re-INVITE代替。§10.1.1.2.4.1继承初建§10.1.1.2.1.1，仅将step10的Request-URI改为待重入MCPTT session identity。初建step10原为服务该用户的PF PSI，group ID原在正文mcptt-request-uri；重入没有把正文group ID也改成session URI。session-type仍为prearranged，并包含发起client-id、所需服务标记和按§6.2.1生成的SDP；本页不请求implicit floor。§4.5定义session identity为服务器分配的GRUU形式SIP URI，PF向客户端的Contact给本地分配身份并维持与CF身份的映射；客户端可以缓存至不再需要。

强度：initial INVITE、继承构造和目标替换为SHALL；初建Supported timer及Session-Expires为SHOULD、P-Preferred-Identity为MAY，不能把这些改成全部必填；客户端缓存是can表述。

- 客户端如何得知已经回到覆盖范围明确不在§10.1.1.2.4.1范围。可缓存不是断线后身份必然仍存在的保证，本页不提供丢失session URI后的发现/恢复算法。
- §6.3.1.1通过iFC/PSI等分类服务器入口，§4.5说明会话身份可供IM CN路由initial请求。不能把session URI直接替换成配置中的PF PSI，也不能仅因URI文字不同就断言该重入入口不可路由。完整SIP路由仍依TS24.229。
- 预建立重入另发REFER，NCF重入另有本地Contact身份规则；本页不把它们并入普通按需流程。

依据：3gpp-ts-24.379-v16.14.0 §4.5；§10.1.1.2.4.1–2 (pre-established comparison)；§10.1.1.2.1.1；§6.2.1;6.4；§6.3.1.1；§F.1.3 field representation/items2–3；§10.1.1.5.3.1 (NCF comparison)，印刷页 38,39,56,57,77,78,136,137,220,221,229,262,547,548。

## PF仍核主叫与准入，映射的是会话身份

条件：O-PF实际收到§10.1.1.3.5.1的originating-PF INVITE且session-type=prearranged；或收到其转发请求的2xx/4xx/5xx/6xx响应。请求与响应为替代事件。

重入PF须继承§10.1.1.3.1.1的处理，step10改为与入站Request-URI会话身份对应的映射身份。PAI公共身份没有有效MCPTT ID绑定时须拒绝404/141并停止；本地策略不许发起预安排组呼时须拒绝403/109；不支持所需语音编解码拒绝488；超过用户N6并发限制拒绝486/103；无法确定组控制方拒绝404/142并停止。通过相应前序处理后按共同INVITE helper转发，移除入站Answer-Mode/Priv-Answer-Mode，设置calling-user-id并处理SDP。收到下游2xx时生成200、处理SDP、Warning与PAI、包含映射会话身份并送客户端；§4.5共同规则要求向客户端的Contact携带PF身份并维持映射。收到4xx/5xx/6xx时生成响应、携带收到的Warning并转送客户端。

强度：所列绑定、拒绝、构造、映射和响应处理为SHALL；资源/拥塞时拒绝500及Retry-After为MAY。

- 资源/拥塞检查仍可先发生。原文step3的403/109没有另写停止，不补成与step2a相同的stop语句；各拒绝/继续语句按其本身处理，不能因本页有转发说明推所有拒绝仍须转发。
- §10.1.1.3.1.1响应step6未重复说明映射身份安放在哪个header，但§4.5已明确Contact共同规则；这不是缺少任何header依据。映射义务不证明现网缓存一定有效。
- 该继承保留组控制方发现步骤，其发现方法在原文NOTE7中不展开。本页不把组文档/配置和服务授权数据库的取得算法补全；priority触发的implicit affiliation不属于普通主线。

依据：3gpp-ts-24.379-v16.14.0 §10.1.1.3.5.1；§10.1.1.3.1.1 full；§4.5；§6.3.2.1.1.1;6.3.2.1.2.1;6.3.2.1.3;6.3.2.1.5.2，印刷页 38,39,83,84,85,87,230,231,232,233,239。

## CF重入拒绝区分会话、权限、归属与容量

条件：CF收到§10.1.1.4.5.1所述Request-URI包含待重入会话身份的INVITE；后续检查也覆盖会话已不存在或资格不满足，不能预设所有守卫已通过。

CF可因资源/拥塞拒绝500并可带Retry-After；若Request-URI所指组呼不存在须拒绝404。媒体/语音编解码不可接受拒绝488；缺所需mcptt或ICSI Accept-Contact标记拒绝403并停止。确定calling MCPTT ID后，加入许可不满足须403/121，归属不满足须403/120。加入许可按§6.3.5.3核组成员entry、适用join-handling规则及条件supported-services；归属按§6.3.6另核组entry、user entry、client ID及未到期，不能只查成员名单。容量上限已到时，本地策略认为新用户优先级更高可移除一个既有参与者并跳过下一拒绝步；否则该容量分支返回486/122。成功路径生成200及SDP，完成所调用媒体处理后才发送200，再生成并发送已订阅客户端的conference通知。

强度：所列检查/拒绝与成功路径200、SDP、媒体接口、通知为SHALL；资源拒绝/Retry-After、Resource-Priority优待和容量满时按本地策略移除为MAY。

- 403/121加入许可与403/120归属是两个不同门槛；原文特定拒绝步骤未统一写skip rest，不擅自增补通用停止算法。成功路径只适用于未被前序处理拒绝的请求，不能给所有入站请求承诺200。
- 容量例外通过§10.1.1.4.4.3调用共同BYE移除helper；它说明移除所选参与者，不是整个组呼必然结束。媒体和SIP释放完整实现不在此展开。
- group ID初始请求另在§10.1.1.4.2判断组呼是否ongoing；它不能替代本条定向session URI的重入入口。本页不把重入当再次创建新会话或重置整个组的初始化。

依据：3gpp-ts-24.379-v16.14.0 §10.1.1.4.5.1 full；§6.3.5.3;6.3.6；§6.3.3.2.1–2;6.3.3.2.3.2；§6.3.3.4；§10.1.1.4.4.3;6.3.3.1.5；§10.1.1.4.2 steps9/14e (initial group-target comparison)，印刷页 106,119,120,121,124,134,135,136,244,245,251,252,253。

<a id="rejoin-invite-ack-routing"></a>
## 重入 INVITE 的 ACK：收到这条腿的 200 或 486 后，怎么写？

**终端收到重入 INVITE 的 200，要先认它收到的那份响应。** 在本节的普通在网按需预安排组呼中，终端主动重入，发的是新的 initial INVITE。这里看同一个 MC 系统内的终端腿，不含分叉，也没有与 200 匹配的早期对话。组呼可以还是原来那场；本次 SIP INVITE 和它的 ACK 不能从旧对话复制。[TS 24.379 V16.14.0 §10.1.1.2.4.1，印 229](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=230)。

**哪份 Contact 是终端的输入？** 若链上有发起侧参与功能（O-PF）与控制功能（CF）之间的 SIP 腿，CF 在自己返回的 200 的 Contact 写 CF 托管的会话身份。O-PF 收到下游 2xx 后，为终端生成这一侧的 200，按映射在发往终端的 Contact 写 PF 托管的会话身份。终端用**实际收到的本腿 200**，不抄 CF 那条腿的 Contact。这个 URI 可以与历史值相同；只有历史值不能还原本次响应。区分实际分腿与逻辑角色，不根据 URI 字符串或节点名称判定中间设备是代理还是独立对话端点。[TS 24.379 §10.1.1.4.5.1 第 11 项，印 253](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=254)回指[§6.3.3.2.3.2 第 5 项，印 120](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=121)；[§10.1.1.3.5.1，印 239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)、[§10.1.1.3.1.1 收到 2xx 后第 2、6、8 项，印 232–233](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=233)与[§4.5，印 38–39](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=39)说明终端一侧。

### 200：按新对话构造 ACK

远端目标取终端实收 200 的 Contact **URI**。从这份 200 的 Record-Route 取 URI 值，**按相反顺序**建立路由集，保留 URI 参数。不把临时响应的 Via 列表、组 ID 或初次建呼的 Contact 当作路由集。ACK 用同一对话的 Call-ID、From 与 To 标识和标签；CSeq 数字沿用这份 INVITE，方法写 `ACK`。[RFC 3261 §12.1.2，印 71–72](https://www.rfc-editor.org/rfc/rfc3261.html#section-12.1.2)；[§12.2.1.1，印 73–75](https://www.rfc-editor.org/rfc/rfc3261.html#section-12.2.1.1)；[§13.2.2.4，印 82](https://www.rfc-editor.org/rfc/rfc3261.html#section-13.2.2.4)。

以下只示意 Request-URI 和 Route。假设本腿 200 的 Contact URI 是 `sip:s1@pf.example.invalid;gr`。这些模拟值不是网络地址或完整 IMS 报文；认证和 SDP 按实际呼叫另判。

| 这份 200 给出的 Record-Route | ACK 的 Request-URI | ACK 的 Route |
| --- | --- | --- |
| 无 | `sip:s1@pf.example.invalid;gr` | 不生成 Route。 |
| 依次为 `<sip:edge-b.example.invalid;lr>, <sip:edge-a.example.invalid;lr>` | `sip:s1@pf.example.invalid;gr` | `<sip:edge-a.example.invalid;lr>, <sip:edge-b.example.invalid;lr>` |
| 依次为 `<sip:edge-b.example.invalid;lr>, <sip:strict.example.invalid>` | `sip:strict.example.invalid` | `<sip:edge-b.example.invalid;lr>, <sip:s1@pf.example.invalid;gr>` |

第三行的路由集首项没有 `lr`；按旧式严格路由兼容规则把首项放进 Request-URI，允许留在 Request-URI 的参数才保留，把远端目标放在 Route 末尾。**Request-URI 不是必然的第一物理跳。** URI 和路由集说明 SIP 请求如何组装，不能据此认定现场发送的 IP、端口、协议或 NAT 可达性。已有同标识早期对话时，§13.2.2.4 要求从 2xx 重算路由集，不是重建所有对话状态。其回指由 [RFC Editor 已验证勘误 4084](https://www.rfc-editor.org/errata/eid4084) 从 §12.2.1.2 更为 §12.2.1.1；不要把这里“新对话从 200 Contact 取远端目标”的示例机械套用到该早期对话。

### 486：按原 INVITE 事务确认

若同一笔 INVITE 改为收到最终 486，客户端事务生成 ACK。Request-URI、Call-ID、From 和已有的 Route 都取该事务实际送出那份 INVITE；Via **只放原 INVITE 最顶部的一项**，保留其中的 branch。To 按收到的 486，包括响应给出的标签。CSeq 仍用 INVITE 的数字，方法写 `ACK`；ACK 送到原 INVITE 所用的同一传输地址、端口与协议，不从失败响应另建 200 式目标和路由集。486 是这里选的对照，不凭状态码独断是哪条 MC 准入规则触发。[RFC 3261 §17.1.1.3，印 129–130](https://www.rfc-editor.org/rfc/rfc3261.html#section-17.1.1.3)；[RFC 6026 §8.4，印 12–13](https://www.rfc-editor.org/rfc/rfc6026.html#section-8.4)更新了 INVITE 客户端事务处理，2xx ACK 仍由 UAC 核心处理，不由该 INVITE 客户端事务生成。

排查时先配对本腿 INVITE 和它的最终响应：**CSeq 方法为 REFER 或 PRACK 的 200 都不是这笔 INVITE 的 200**。只保存了旧 Contact、别腿响应或本次 REFER 200，不能填出本腿 INVITE 的 ACK。本节是特定条件下的通用 SIP 字段对照，不替代 TS 24.229 的 IMS 细则，也不判断已实际发送或媒体已建立。

<a id="rejoin-sip-timer-vs-tng3"></a>
## 重入的 200 带了 Session-Expires，整场组呼会续时吗？

甲回到覆盖区，向原会话 URI 发起新的 INVITE。甲收到 200，几秒后却又收到 BYE。这两条消息并不矛盾：**`Session-Expires` 管一条 SIP 对话，TNG3 管控制功能上的一场组呼。** 这里只看普通、同一 MC 系统、无隐式话权请求的按需预安排组呼。若甲不知道原会话 URI，改用组身份加入当前活动的组呼，成功分支带 [Warning 文本 123](prearranged-server-admission-routing.md#join-active-group-123)；它不保证当前组呼就是断线前那一场。

| 把每份 200 配回本段的初始 INVITE | 谁刷新这条 SIP 对话 |
| --- | --- |
| 终端 → 发起侧参与功能（O-PF） | O-PF 收到下游成功响应后，另为终端生成 200，带 `Require: timer` 和 `Session-Expires`。若**终端这份请求没有写** `refresher`，O-PF 须在 200 里写 `refresher=uac`，即由终端刷新。若请求已写该参数，按所引 RFC 4028 的 UAS 规则处理，不能再套“缺省为 uac”，也不能假定照抄下游。 |
| O-PF → 控制功能（CF），若实际有这条 SIP 腿 | 定向重入和按组加入已有会话的 CF 成功分支都调用同一最终响应程序。CF 的 200 须带 `Require: timer`、`Session-Expires`，并明确写 `refresher=uac`；CF 开始监督这条 SIP 会话。这里的 UAC 是发出这份 INVITE 的 O-PF。 |

所以两份 200 即使同写 `uac`，指的也不是同一节点。用各自的 Call-ID、标签和 INVITE CSeq 配对应答，再看实际参数。CF 侧的间隔不代替终端侧的间隔；声明刷新责任也不等于后来真的刷新过。O-PF 与 CF 合设时，须区分逻辑角色，不假定 IMS 上一定有第二段报文。

依据：TS 24.379 V16.14.0，[§10.1.1.3.5.1，印 239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)；[§10.1.1.3.1.1 收到 2xx 后第 2、8、10 项，印 232–233](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=233)；[§6.3.2.1.5.2 第 1–2 项，印 87](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=88)；[§10.1.1.4.5.1 第 11 项，印 253](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=254)；[§10.1.1.4.2 第 15(h,j) 项，印 248](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=249)；[§6.3.3.2.3.2 第 1–3 项，印 120](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=121)。

**怎样认出整场组呼的时钟？** CF 新建组呼、分配会话身份后，按组文档中的 `on-network-maximum-duration` 启动 TNG3。规范说明预安排组应配置该字段，也明确写了字段缺失就不启动。定向重入和按组加入已活动会话的普通成功分支，都没有要求重启 TNG3。要判断是否换了一场，核对 CF 的活动会话记录和新身份分配；新 SIP 对话、Contact 或一次实际的 SIP 刷新都不能代替这项证据。见[§10.1.1.4.2 第 9、14(e) 项，印 244–245](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=245)、[第 15 项，印 246–248](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=247)、[§10.1.1.4.5.1，印 252–253](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=253)和[§6.3.3.5.1，印 124–125](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=125)。

**怎样判断那条 BYE 是不是因为 TNG3 到期？** 查 CF 上同一组呼实例的启动、停止和到期记录。最后一名客户端离开时，CF 须停止 TNG3；若由 CF 移除成员，须在计时器尚未到期且最后一名已被移除时停表。仅发出 BYE 或只剩一人，不等于最后一名已经离开。若确认该场 TNG3 到期，CF 须释放组呼，向所有参与者发 BYE。反过来，一条 BYE 或其 200 既不证明所有人已释放，也不能确定触发原因：媒体面向 CF 指示 T4 到期、仅剩一人或无人、在场的已归属成员不足，以及本地策略要求发起人离开时结束，都可能触发释放。见[§6.3.3.5.1，印 125](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=126)、[§6.3.3.1.5，印 106–107](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=107)、[§6.3.8.1，印 136](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=137)及[§10.1.1.4.4.2–3，印 251–252](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=252)。

## 服务器晚入是另一入口，不是主动重入的必经步骤

条件：CF实际被通知某客户端新归属或返回覆盖，且存在ongoing组呼；或收到本条邀请产生的指定183/200响应。它与客户端主动重入是替代入口。

§10.1.1.4.6要求CF邀请该客户端加入ongoing组呼，调用§10.1.1.4.1。目标客户端邀请按§10.1.1.4.1.1以其T-PF PSI为Request-URI，以目标用户MCPTT ID为正文mcptt-request-uri，并给calling-group-id；共同INVITE helper在Contact带会话身份。§6.3.3.1.1明确给既有会话添加用户时offer包含当前使用的媒体流。收到同时含100rel和P-Answer-State=Unconfirmed的183时须发PRACK；收到该INVITE的200时另与媒体交互、向已订阅参与者发conference通知并增加收到200的本地计数。邀请、183、200及通知分别是不同证据。

强度：实际晚入触发后的邀请及所列183/200处理为SHALL；不因SHALL邀请而宣称目标必接受或媒体必达。

- 如何得知客户端回覆盖、如何发现其T-PF地址，分别在§10.1.1.4.6和§10.1.1.4.1.1的NOTE中不展开。新归属与已进呼不能等同。
- §10.1.1.4.1.1 opening列4.2或403触发，但4.6另有显式调用，不删除这个晚入caller。4.1.1 step5及共同helper仍使用received/incoming INVITE的SDP/正文；6.3.3.1.1给当前媒体流原则，却未在晚入触发段规定完整原始INVITE上下文保存/选择方法。不能假定回覆盖通知本身就是新收到的INVITE。
- 终接客户端的拒绝、Auto/Manual应答须按普通组呼客户端页的实际条件处理，不从服务器发出邀请推定终端已接受。conference通知不能证明所有成员已读或已听；§4.1.1 NOTE4也提醒通知不证明初建必成功。

依据：3gpp-ts-24.379-v16.14.0 §10.1.1.4.6；§10.1.1.4.1.1 full；§6.3.3.1.1–2；§6.3.3.4;10.1.3.1–3 (notification interface)；§10.1.1.2.1.2 (terminating boundary)，印刷页 105,106,124,222,223,224,240,241,253,301,302。

## 重入200与本地无话权状态分开，保留服务器回指差异

条件：主动重入客户端收到INVITE的2xx或相应媒体重入事件；或服务端为重入/邀请参与者建立实际SIP关联并进入对应媒体入口。客户端与服务器、重入与受邀是分别适用的角色事件。

客户端按§10.1.1.2.1.1收到2xx后与用户面交互，可显示收到的P-Answer-State，也可订阅conference；不是收到200就能发话。TS24.380 §6.2.4.2.2明确重入ongoing呼叫时客户端进入U: has no permission；该段也允许在200前先保存收到的控制消息。服务端逐参与者association在originating侧发送200、terminating侧收到200时建立。对不带implicit的主动重入：若已有其他持有人，服务器SHOULD发送Floor Taken并进入not-permitted/Floor-Taken；若无人持有，SHOULD发送Floor Idle，但其目标状态名称与所指helper存在下述差异。主动邀请分支另在有/无持有人时分别进入not-permitted/Floor-Taken或not-permitted/Floor-Idle，不能用邀请分支修补主动重入分支。

强度：客户端重入进入has-no-permission、关联创建及各指定状态动作为SHALL；所述初始化Floor Idle/Taken发送为SHOULD；答案状态显示和conference订阅为MAY。

- TS24.380 §6.3.5.2.2 step2a(ii)写U: not permitted and Floor Idle，却回指§6.3.5.5.2，后者实际设置U: permitted。该文字差异保留，不把它解释为重入已获话权，也不静默改为§6.3.5.3.2。邀请分支step4b(ii)的§6.3.5.3.2回指不同且正确。
- 本页不请求implicit；§6.3.5.2.2 step3使用attempts to initiate an already existing call with implicit的表述，不把它改写成所有主动重入的默认授权路径。完整G初始化、排队调度及后续请求/授予各按对应媒体owner，不以ordinary Idle页补本回指。
  只有在普通在网单话权组呼中，控制侧已识别这名客户端本次 SIP 会话建立时带隐式请求发起既有呼叫，才转查[既有组呼的隐式话权请求](../media/existing-call-implicit-floor-request.md)，看谁已有发送许可、请求端是否协商排队。无隐式话权请求的重入仍按本页。
- conference订阅按client参与中的会话以及非广播条件进行；NOTIFY到达后处理和MAY显示依RFC接口，不能用通知代替语音呈现、全员接收或floor permission。

依据：3gpp-ts-24.379-v16.14.0 §10.1.1.2.1.1 responses;10.1.1.2.4.1；§10.1.3.1–3，印刷页 221,229,301,302。
依据：3gpp-ts-24.380-v16.9.0 §6.2.4.2.1–3；§6.3.5.1–2.2；§6.3.5.3.2;6.3.5.4.2;6.3.5.5.2，印刷页 37,71,72,73,74,75,78,85。

## 共同边界与关联

- §6.5多MIME封装和§6.6适用保护须按实际请求/响应执行；F.1普通URI/String包装与加密字段不同。本页不提供可直接发送的完整 XML/SDP 报文、TS 24.229 的 IMS 配置或密码实现。所列 RFC 只用于 ACK 小节的条件与字段。
- 组身份、各段session identity、公共用户身份及client-id不能互换。归属不等于参加会话，参加会话不等于获话权，返回覆盖不等于服务器已获知。

依据：3gpp-ts-24.379-v16.14.0 §6.2.1;6.4;6.5;6.6.1；§F.1.3 representation/items2–6；§4.5，印刷页 38,39,56,57,136,137,138,139,547,548。

- [prearranged-client-establishment](prearranged-client-establishment.md)
- [prearranged-server-admission-routing](prearranged-server-admission-routing.md)
- [explicit-affiliation-client](../groups/explicit-affiliation-client.md)
- [on-network-floor-client](../media/on-network-floor-client.md)
- [on-network-idle-floor-server](../media/on-network-idle-floor-server.md)

若收到重入请求的是非控制 MCPTT 功能，或由它在新归属、回覆盖后主动邀请，查 [NCF 重入时的 Contact 与晚入响应](noncontrolling-prearranged-rejoin.md)。

若排查的是会话 GRUU 是否能携带组号、正文已加密时该怎样判断，查[会话 GRUU 与敏感业务身份的边界](session-gruu-sensitive-identity.md)。

已成功重入，随后由终端主动离会，查[PF 怎样取出站 BYE 的会话标识，以及哪份 200 才能回给终端](prearranged-participant-refer-leave.md#on-demand-member-bye)。

如果终端已没有旧会话 URI，用户按组身份重新发起普通按需呼叫，见[已有活动组呼时的 200 / 123](prearranged-server-admission-routing.md#join-active-group-123)。这是按组加入的独立入口，不是把组 ID 填入定向重入请求。
