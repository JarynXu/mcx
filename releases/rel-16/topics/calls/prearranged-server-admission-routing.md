# 普通按需预安排组呼：服务器准入与邀请路由

- 固定 TS24.379 V16.14.0 的在网、直接组身份、GMS 管理的普通预安排组；组文档不含 temporary/regrouped，不是 constituent 组或预配置重组；不含 chat、广播、功能别名或离网业务。
- 普通请求不带 emergency-ind/imminentperil-ind/alert-ind，组也不处于紧急或迫近危险状态。各角色按实际收到的初始请求处理；不以主叫已归属、文档已取得、目标已接受或全链成功作为公共前提。
- 范围是 O-PF/CF/T-PF 的准入、组资格、受邀集合及身份路由。新建与加入既有普通会话分别适用，不提供完整响应聚合、会议事件、媒体/安全实现或组呼释放生命周期。

## O-PF 的主叫身份、起呼许可和组路由

- 条件：O-PF 收到按 §6.3.1.1 分类的 originating INVITE，session-type=prearranged；每项拒绝与后续构造按实际到达的步骤分别适用。

O-PF 从 P-Asserted-Identity 的公共用户身份查主叫 MCPTT ID；绑定缺失或已过期时返回 404+Warning141 并停止。按本地策略不允许发起预安排组呼时返回 403+Warning109；未提供 MCPTT speech codec 时返回488；超过用户 MaxSimultaneousCallsN6 时返回486+Warning103。继续处理时按正文中的目标组身份确定组 CF PSI，无法确定则404+Warning142并停止。出站 Request-URI 写 CF PSI，mcptt-calling-user-id 写已确定的主叫 MCPTT ID；通用 INVITE helper 复制入站 P-Asserted-Identity 和相关 mcptt-info，但组呼程序明确不复制 Answer-Mode、Priv-Answer-Mode。因此客户端不能用这些模式头直接指定组成员的最终应答方式。

规范强度：身份识别、指定拒绝、目的地址和正文身份构造、模式头不复制为 SHALL；资源拒绝及 Retry-After 为 MAY。
- 边界：资源不足或拥塞时返回500及附 Retry-After 都是 MAY。Warning109 的 step3 未另写停止，不把相邻拒绝的 stop 措辞移入本步。
- 边界：O-PF 隐式归属 step6 要求未归属且请求是获准的优先呼叫；普通请求不能据此自动补齐归属。CF 的组侧检查另行适用。
- 边界：CF PSI 如何发现是本版明确未规定的实现接口；本页不补发现算法、完整 SDP/安全实现、位置上报或功能别名处理。

依据：3gpp-ts-24.379-v16.14.0 §6.3.1.1 originating/controlling group/terminating INVITE classifications，印刷页 77,78；3gpp-ts-24.379-v16.14.0 §10.1.1.3.1.1 opening and steps1–17; priority implicit-affiliation steps6–7 comparison only，印刷页 229,230,231,232；3gpp-ts-24.379-v16.14.0 §6.3.2.1.3 full;6.3.2.1.1.1 full，印刷页 83,84,85。

## CF 先核媒体、服务标记与组文档

- 条件：CF 收到按 §6.3.1.1 分类的组 CF 初始 INVITE；组文档查询失败、组资格拒绝与继续处理分别适用，不要求已经取到文档或已通过成员检查。

CF 的目标组来自 mcptt-request-uri，发起用户来自 mcptt-calling-user-id。媒体参数不可接受或没有 MCPTT speech codec 时488并停止；Accept-Contact 缺所要求的 MCPTT 或 ICSI feature tag 时403并停止。GMS 管理的组调用 §6.3.5.2：未订阅时订阅组文档的 xcap-diff；订阅得到404时返回404+Warning113，其他4xx/5xx/6xx时返回相应最终响应及Warning114。收到组文档通知或已有缓存后，普通组的 list-service 含 on-network-disabled 时403+Warning115，发起用户不在组 list 时403+Warning116；invite-members=true而请求不是prearranged时404+Warning117，invite-members=false而请求不是chat时404+Warning118，均停止相应后续。CF 初始处理已发送3xx/4xx/5xx/6xx时不再继续建立；通过后才缓存收到且支持的 Contact feature tags，并把受邀成员200计数初始化为0。

规范强度：媒体、服务标记、文档错误及组资格拒绝、条件停止和缓存/计数初始化为 SHALL；CF 资源不足或拥塞时的500与 Retry-After 为 MAY。
- 边界：普通无紧急/迫近危险字段且组不处于这些状态时，携带对应紧急/迫近危险 Resource-Priority 值仍触发 step12 的403；本页不把普通范围解释为跳过这个不一致检查。
- 边界：§6.3.5.2 step4(b)(ii) 字面以不含 temporary 或 regrouped 分类，随后(iii)又列非temporary但regrouped；本页只处理两者均不含的普通组，不替原文改 OR 或实现通用分类器。
- 边界：GMS 文档获取使用 TS24.481 接口；本页核的是24.379的调用、返回及成员检查，不提供外部订阅/缓存更新的完整实现。重组转向与 NCF 授权不在本页。

依据：3gpp-ts-24.379-v16.14.0 §10.1.1.4.2 definitions and steps1–9,12，印刷页 242,243,244；3gpp-ts-24.379-v16.14.0 §6.3.5.1;6.3.5.2 steps1–5 (ordinary group);step4 classification comparison，印刷页 130,131,132；3gpp-ts-24.379-v16.14.0 §6.3.3.2.2 full，印刷页 120；3gpp-ts-24.379-v16.14.0 §6.3.1.1 group CF classification，印刷页 78。

## 新建许可、加入许可与归属分别判断

- 条件：CF 已到达普通组的准入分支；未进行中的新建和已进行中的加入为替代分支，任一资格或人数拒绝仍可发生。

是否 ongoing 由已分配组呼会话身份且会话 active 两项共同判断。本页非 constituent、无 emergency-ind/imminentperil-ind 的普通请求中，未通过 §6.3.6 归属检查时返回403+Warning120并停止。该检查要求组条目、用户条目、对应客户端 ID 均存在且用户条目未到期；不能只查组成员名单。新建另按 §6.3.5.4 检查发起资格，不符为403+Warning119；加入既有会话按 §6.3.5.3 检查加入资格，不符为403+Warning121。两者都需用户 list entry，并有匹配 is-list-member 或用户 identity 的 rule，但动作分别是 allow-initiate-conference=true 与 join-handling=true；supported-services 若存在须支持 MCPTT，且其中 group-media 若存在须含 MCPTT speech。已有会话达到人数上限时，按本地策略认为请求者优先级更高，可移除一名参与者并跳过随后拒绝；否则返回486+Warning122并停止。

规范强度：ongoing 判断、归属及许可检查、指定拒绝与停止为 SHALL；满员时本地策略允许的参与者移除为 MAY。
- 边界：§6.3.6 NOTE 指出发起客户端 ID 来自 mcptt-info 的 mcptt-client-id；它不是用户 ID 或公共身份的替代值。归属的建立/解除及状态同步见显式归属主题。
- 边界：本页不将上述普通分支简化条件用于临时组或优先呼叫；原文14(a)/15(a)的 constituent 与隐式归属分支仍有独立条件。
- 边界：满员时移除是 MAY 和本地策略，不是所有高优先用户都自动挤出他人；此处不实现移除的媒体及通知全链。

依据：3gpp-ts-24.379-v16.14.0 §10.1.1.4.2 steps9,14(a–b),15(a–d)，印刷页 244,245,246,247；3gpp-ts-24.379-v16.14.0 §6.3.5.3–6.3.5.4 full，印刷页 134,135；3gpp-ts-24.379-v16.14.0 §6.3.6 full，印刷页 135,136。

## 受邀集合、归属门槛和应答门槛不同

- 条件：CF 的普通组新建请求通过相应前序准入后进入 step14(e,g)；集合选择失败仍在本条范围内，不要求组成员已经应答。

CF 创建组会话并分配会话身份，按 §6.3.3.5.1 处理 TNG3：组文档存在 on-network-maximum-duration 才用其值启动，缺失则不启动。选择受邀者时，§6.3.5.5 只允许邀请已归属成员，普通组从组文档 list 逐一按 §6.3.6 判断；人数超出 on-network-max-participant-count 时仅邀请上限人数，并优先 on-network-required 成员。随后若已归属人数低于 minimum-number-of-affiliated-members，或任一 affiliation-to-group-required 成员未归属，返回480+Warning112并停止。通过后，存在已归属且 on-network-required 的成员时，须在发邀请前启动 TNG1。归属门槛不是应答完成。按 §6.3.3.3 的正常分支，收到全部已归属且标记 required 的成员对邀请的 200 时，CF 停止 TNG1；这条分支还检查受邀 INVITE 的 200 计数大于或等于 minimum-number-to-start，才向发起侧发 200。CF 按 §10.1.1.4.1.1 向选定的个别用户发邀请；收到某一受邀者的200后才增加该200计数，会议通知可以早于向发起者的响应，不能证明整个组会话最终建立成功。

规范强度：会话分配、条件启停计时器、仅邀已归属成员、上限及优先选择、门槛拒绝、计数为 SHALL；配置必需性及通知不等于建立成功按 NOTE 层次解释。
- 边界：step14(g)(v) 字面回指13(g)(i)，而实际选人步骤在14(g)(i)；保留该号次差异，不把两个步骤静默改写成同一引用。
- 边界：on-network-required 与 on-network-affiliation-to-group-required 是不同字段，minimum-number-to-start 与 minimum-number-of-affiliated-members 也是不同门槛。其他超额名单选择策略不由本版限定；规范假设 GMS 校验最大人数不少于 required 人数。
- 边界：TNG3 配置对预安排组为必需是 §6.3.3.5.1 NOTE1 的说明；正文仍明确写出字段缺失则不启动的行为。这里不补配置缺失时的默认时长。
- 边界：本条只给正常邀请与必要应答门槛，不展开 TNG1 到期政策、全部响应聚合/失败补偿、会议订阅实现或完整释放生命周期。

依据：3gpp-ts-24.379-v16.14.0 §10.1.1.4.2 steps14(e,g)，印刷页 245,246；3gpp-ts-24.379-v16.14.0 §6.3.5.5 full;6.3.6 full，印刷页 135,136；3gpp-ts-24.379-v16.14.0 §6.3.3.5.1 full (ordinary initial timer);6.3.3.3 initial TNG1 start/stop and minimum-response gate，印刷页 121,124,125；3gpp-ts-24.379-v16.14.0 §10.1.1.4.1.1 response200 and NOTEs4–5，印刷页 241。

## 最后一名必需成员回 200：CF 怎样匹配并完成正常应答？

这里限同一 MC 系统内新建普通非优先在网按需 MCPTT 预安排组呼：使用 GMS 管理的未重组直接组身份，不是临时组或 TGI；请求和组状态均非紧急、非迫近危险。

**先对上同一条受邀 INVITE 与被叫身份。** 控制功能（CF）实际收到对已归属且标记 `on-network-required` 成员的邀请 200 后，核对其 MCPTT ID 是否等于对应出向 INVITE 正文 `mcptt-request-uri` 的被叫 MCPTT ID，并确认没有其他发给已归属必需成员的 INVITE 200 待收。SIP 的外层 Request-URI 是终接参与功能（T-PF）的 PSI，不是被叫用户 ID。这里没有指定从响应的哪个字段取 MCPTT ID，不能猜测是 `P-Asserted-Identity`、`Contact` 或其他头，也不能只凭一个 200 判定这是最后一名必需成员。原文还检查一类跨系统 NCF 邀请：若此前的 183 指有必需成员，就不能还有该腿 200 待收。本节是同系统直接组，没有这类邀请腿。[TS24.379 §10.1.1.4.1.1，第 2、4(a) 项，印刷页 240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=241)；[§10.1.1.4.2，字段定义，印刷页 243](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=244)；[§10.1.1.4.2，匹配受邀 200 的条件，印刷页 249–250](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=250)。

**停 TNG1 和向发起侧发 200 的条件要分开。** §6.3.3.3 的正常总则在收齐已归属必需成员的邀请 200 时要求停 TNG1；向发起侧发 200 另要求收到的受邀 INVITE 200 计数**大于或等于** `on-network-minimum-number-to-start`。第 249–250 页的具体段写了身份匹配、无待收和停表，但没有重述该计数门槛，也未明列 TNG1 正运行、支持缓冲或尚未发送原最终响应等条件。不要把相邻非运行分支的**等值**门槛或实际到期政策套过来，也不要据此裁定分支优先级、认定门槛可省或会重复发最终响应。[TS24.379 §6.3.3.3，正常停表、计数与到期对照，印刷页 121–122](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=122)；[§10.1.1.4.2，正常应答与相邻分支，印刷页 249–250](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=250)。

**CF 的正常应答与通知。** CF 按 §6.3.3.2.3.2 为原发起 INVITE 生成 200。只有组成员数超过 `on-network-max-participant-count`，并且正是这个上限导致未邀全时，才按本项添加 Warning 文本 `122 too many participants`；Warning 外层码是 399。这是正常新建的 200，不是已有会话满员拒绝的 486/122，也不是 TNG1 到期按配置继续的 200/111。CF 附上对自己收到的原 INVITE SDP offer 的 answer；此次媒体面交互触发的处理完成后，CF 才发送 200。然后 CF 生成并向 conference event package 的订阅者发送 NOTIFY，告知发起用户已加入。[TS24.379 §10.1.1.4.2，正常应答第 1–8 项及注 11，印刷页 249–250](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=250)；[§6.3.3.2.1、§6.3.3.2.3.2，SDP 与最终响应，印刷页 119–120](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=120)；[§4.4.1，Warning 格式，印刷页 33](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[§10.1.1.4.2，第 15(d) 项的 486/122 对照，印刷页 247](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=248)；[§6.3.3.3，到期继续的 200/111 对照，印刷页 122](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=123)。

**不要把两种 NOTIFY 或两条 SIP 腿混在一起。** 个别邀请程序在 CF 收到对应 INVITE 的 200 时另做媒体交互、向订阅者发 NOTIFY 并增加本地计数；该通知可以先于发起侧的 200，不是上一段的发起用户加入通知。发起侧参与功能（O-PF）实际收到对自己发出 INVITE 的匹配 2xx 时，另为终端生成 200 和 SDP answer；若收到的是 200，将该响应里实际收到的 Warning 字段纳入自己发送的 200。CF 或 O-PF 发出 200 不证明终端收到，单见 200、Warning 或 NOTIFY 也不证明全组已加入、主叫已获话权或 RTP 已通。定位时核对同一 CF 组会话的原发起腿、对应受邀 INVITE 与实际响应、身份和归属、必需标记与未邀全的原因。[TS24.379 §10.1.1.4.1.1，收到受邀 200 的动作和注 4–5，印刷页 241](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=242)；[§10.1.1.3.1.1，收到 2xx 后第 2–4、8 项，印刷页 232](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=233)。

## TNG1 到期或必需成员提前拒绝，CF 如何处理？

这里限同一 MC 系统内新建普通在网按需预安排组呼。组须由 GMS 管理，使用未重组的直接组身份，不是临时组；请求和组状态均非紧急、非迫近危险。先分清 **CF 还没发成员邀请、TNG1 正在运行，还是 TNG1 已到期**。

**还没发成员邀请。** 在第 14(g) 项，若组内已归属人数低于 `on-network-minimum-number-of-affiliated-members`，或者有标记 `on-network-affiliation-to-group-required` 的成员未归属，CF 就对发起侧原 INVITE 回 480，Warning 文本带 112，并跳过后续步骤。这发生在启动 TNG1 和发出成员 INVITE 之前。通过检查后，只有组文档里有已归属且标记 `on-network-required` 的成员，才在发邀请前启动 TNG1。必须归属和必须应答是两个标记；已归属人数也不是收到邀请 200 的人数。[§10.1.1.4.2，第 14(g)(i)–(ii)、(v) 项，印刷页 245–246](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=246)；[§6.3.3.3，开头，印刷页 121](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=122)。

**TNG1 已到期，仍有必需成员的 200 待收。** 这里指已归属且标记 `on-network-required` 的成员，对 CF 发出的相应 INVITE 尚有 200 未收到。若 CF 已收到的受邀成员 INVITE 200 计数低于 `on-network-minimum-number-to-start`，须等受邀客户端后续的实际应答，直到 CF 的该计数等于该值；不能仅因到期就立即回 480 或 200。计数达到或超过门槛，才看组文档的 `on-network-action-upon-expiration-of-timeout-for-acknowledgement-of-required-members`。[§10.1.1.4.2，末尾 TNG1 分派，印刷页 250](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=251)；[§6.3.3.3，到期计数条件，印刷页 121–122](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=122)。

- **`proceed`：** CF 对原 INVITE 生成 200，Warning 文本带 111，附对原 offer 的 SDP answer。CF 按条文与媒体面交互；由此触发的媒体面处理完成后，CF 才向发起侧发送这份 200。
- **`abandon`：** CF 对原 INVITE 发 480，Warning 文本带 112。按 CF 侧每条受邀对话的状态处理：已确认的发 BYE 并与媒体面交互，未确认的发 CANCEL。[§6.3.3.3，到期第 1(a)、2 项及注 2，印刷页 122](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=123)。

**TNG1 运行时，CF 提前收到必需成员的最终失败。** 要有 CF 收到的实际响应：该受邀成员已归属、标记 `on-network-required`，且本次对应 INVITE 回的是最终 4xx、5xx 或 6xx。若策略决定不继续，CF 停止 TNG1，把收到的最终失败响应转发给原发起侧，Warning 文本带 112。状态码不固定为 480；这段也没有列出到期放弃时的同一清理动作。若策略决定继续，而且受邀成员 INVITE 的 200 计数已达到或超过门槛，该条列明：在 “all other invited clients have not yet responded” 的条件下，让 TNG1 继续运行；若其余受邀客户端都已对相应 INVITE 回 200，则停止 TNG1，对原 INVITE 生成带 Warning 文本 111 的 200，附对原 offer 的 SDP answer，并按条文与媒体面交互。由此触发的媒体面处理完成后，CF 才向发起侧发送这份 200。不要把前一句改成“只要有一个人没答”，也不要从这两句推定有的 200、有人未答或失败等混合结果。[§6.3.3.3，到期前收到最终失败的两段及注 3–5，印刷页 122–123](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=123)；[§10.1.1.4.2，末尾 TNG1 分派，印刷页 250](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=251)。

**看响应之外的证据。** 111 和 112 在 Warning 的引号文本里，外层码是 399。光看 480/112，分不出邀请前拒绝、到期放弃，或提前收到的失败本身就是 480；光看 200/111，也分不出到期继续和提前继续。用同一 CF 的组会话记录对应原 INVITE、实际的受邀腿及响应，核对归属和标记、计入的匹配 INVITE 200、TNG1 的运行/到期事件及对应配置和策略。临时响应和 ACK 不算作受邀 INVITE 的 200；抓包没看到请求或回包，不能证明没发、没收或计时器已到期。CF 发了最终响应、BYE 或 CANCEL，不等于终端已收到、对话清理已完成或语音已通。[§4.4.1，印刷页 33](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[§10.1.1.4.1.1，收到受邀 INVITE 200 的段落，印刷页 241](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=242)。

## TNG1 未运行：受邀侧的 183 或 200，何时让 CF 给主叫 200？

这里限同一 MC 系统内新建普通在网按需 MCPTT 预安排组呼：直接组身份未重组，不是临时组或 TGI，也不是加入既有会话；请求和组状态均非紧急、非迫近危险。以下两条都要求控制功能（CF）**实际收到对应受邀 INVITE 的响应、本次 TNG1 未运行、CF 支持媒体缓冲，且还没对原发起 INVITE 发最终响应**。

| CF 在受邀腿收到什么 | CF 怎样应答原发起 INVITE |
| --- | --- |
| **183，含 `P-Answer-State: Unconfirmed`** | CF 生成 200，写入 `P-Answer-State: Unconfirmed`，并给出原 SDP offer 的 answer。此分支未把应答计数或 `100rel` 列为条件。 |
| **200** | CF 收到的受邀 INVITE 200 计数必须**等于**组文档的 `on-network-minimum-number-to-start`，不是“大于或等于”。在这些条件下 CF 按本地策略生成 200，并给出原 SDP offer 的 answer。这段未要求带 Unconfirmed，也没禁止带。 |

两条分支都是 CF 先按条文与媒体面交互，待由此触发的媒体处理完成后，再发送原发起 INVITE 的 200。第 248 页生成 200 处回指 §6.3.3.2.3.2；第 250 页印的是 §6.3.3.2.2，后者讲收到初始 INVITE 时缓存 Contact 的特征标记。本段不把这个回指改成前者，也不据此补第 250 页的响应字段。TNG1 未运行只描述当时状态，不等于从未启动，也不能单独证明已经到期；实际到期且仍待必需成员 200 时，走本页上一节的到期程序。[TS24.379 §10.1.1.4.2，183 路径与注 9，印刷页 248–249](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=249)；[§10.1.1.4.2，受邀 200 路径、注 13 与到期分派，印刷页 250](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=251)；[§6.3.3.2.2、§6.3.3.2.3.2，回指对照，印刷页 120](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=121)。

**PRACK、受邀者的 200 和主叫收到的 200 是不同证据。** 个别邀请程序另规定：CF 收到同时含 `Require: 100rel` 和 `P-Answer-State: Unconfirmed` 的 183，须向受邀侧发 PRACK；收到对应受邀 INVITE 的实际 200，才把本地计数加一。发起侧参与功能（O-PF）实际收到对自己发出的 INVITE 的 2xx 后，为终端另生成 200 和相应 SDP answer；若收到的 200 带 `P-Answer-State`，第 6A 项要求把该应答状态写入自己发往终端的 200。终端侧单见 200 或 Unconfirmed，不能确定 CF 走的是哪条路径。把同一 CF、同一组会话的原发起 INVITE 和受邀腿对应起来，核对实际收到的响应、当时的 TNG1 与原 INVITE 最终响应状态，以及适用的计数、缓冲能力和策略。[TS24.379 §10.1.1.4.1.1，个别邀请的 183 和 200，印刷页 241](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=242)；[§10.1.1.3.1.1，收到 2xx 后第 2–3、6A、8 项，印刷页 232](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=233)。

**主叫能否提前发 RTP，要看话权侧。** 新 SIP 会话带话权、已识别主叫的隐式话权请求，且服务器支持并允许媒体缓存时，话权控制服务器收到受邀侧参与功能的第一个未确认指示，可以另给主叫提前发 RTP 的指示。确实给了该指示，主叫才从这项动作获得许可；MCPTT 服务器缓存实际收到的 RTP，至少到首位受邀客户端接受邀请或缓冲超过上限。不要把 SIP 200/Unconfirmed 当成这项早期许可，也不要据此断定收到过 RTP、何时停止缓冲或被邀者已能听到语音。其他缓存条件见[隐式话权与提前发送 RTP](../media/implicit-floor-early-media.md)。[TS24.380 §6.3.2.1，新会话初始化，印刷页 51](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=52)；[§6.3.2.2，早期指示和缓存，印刷页 52](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=53)。

## TNG1 未运行：受邀侧最终失败，何时回最终响应、移除或补邀？

这里限同一 MC 系统内新建普通在网按需 MCPTT 预安排组呼：使用 GMS 管理的未重组直接组身份，不是临时组或 TGI；请求和组状态均非紧急、非迫近危险。控制功能（CF）实际收到本次受邀腿 INVITE 的最终 4xx、5xx 或 6xx，才有这项入口。同时，**TNG1 当时未运行，且 CF 实际收到的受邀 INVITE 200 计数恰好等于组文档的 `on-network-minimum-number-to-start`**。用的是受邀腿的 INVITE 200，不是已归属人数、临时响应或发给主叫的 200。这里没有把“支持媒体缓冲”或“该成员是必需成员”列为条件。[TS24.379 §10.1.1.4.2，未运行时收到最终失败的入口与两项处理，印刷页 251](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=252)；[§10.1.1.4.1.1，收到受邀 INVITE 200 时计数，印刷页 241](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=242)。

CF 按策略与各项条件处理：

| 原发起 INVITE 的 200 发送状态 | 还要实际收到哪些响应 | CF 的动作 |
| --- | --- | --- |
| 尚未发送 200 | **其余每位**已受邀客户端都已回 SIP 最终响应。这一项不要求这些响应全是失败。 | 向原发起侧发 SIP 最终响应。本段没有规定固定的状态码、Warning 或状态码映射。 |
| 已发送 200 | **所有**已受邀客户端都已回非 2xx、非 3xx 的 SIP 最终响应，包括触发这次处理的客户端。 | 按移除程序移除这位受邀客户端，不等于拆除整组。若组成员数超过 `on-network-max-participant-count`，且全组尚未都被邀请，可补邀一位此前未被邀请的组成员；不是重试这位失败者，也不是必做。 |

第一项原文查的是 CF **尚未发 200**，不是尚未发任何最终响应。第二项也仍受前面的等值计数条件约束。若日志里同一受邀集合在同一时点每人只有一个最终结果，正数的受邀 200 计数会与“所有人都回非 2xx、非 3xx 最终响应”产生张力。规范没给处理这类冲突的算法。不要把“所有”缩成“其余”或“还没响应的人”，也不要假设计数被清零，或据此断言第二项永远不可能发生。[TS24.379 §10.1.1.4.2，两项处理，印刷页 251](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=252)。

**移除看对应的会话和目标。** 移除程序要求 CF 为该参与者的会话释放与媒体面交互，再生成并发送针对该参与者的 BYE。若 CF 实际收到匹配此 BYE 的 200，还要为相关 SIP 会话的媒体资源释放与媒体面交互。不能仅凭一条失败 INVITE，就断定有可用对话或发生了这个 BYE；也不能从 BYE 或其 200 推出整组已释放。[TS24.379 §6.3.3.1.5，单个参与者移除及收到 BYE 200，印刷页 106–107](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=107)。

定位时，核对同一 CF、同一组会话里原发起 INVITE 的 200 发送记录、各次实际邀请和对应最终响应、当时的 TNG1、计数与组配置。未运行不说明从未启动或本次刚到期，漏抓一条 SIP 消息也不说明没发或没收。CF 发了 200 不等于终端收到；补邀发出或某一腿出现 INVITE 200 不证明其他人加入或媒体已通。[TS24.379 §10.1.1.4.2，未运行时收到最终失败，印刷页 251](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=252)。

## 下行路由到用户，组身份和会话身份仍保留

- 条件：CF 对已选个别用户调用 §10.1.1.4.1.1；或 T-PF 收到该组呼 INVITE。两角色的接收失败与继续下发分别适用；终接仅展开未命中空闲匹配预建立承载的按需分支。

CF 发出的 Request-URI 为服务目标用户的 T-PF PSI，P-Asserted-Identity 为 CF PSI；mcptt-request-uri 改为被邀用户 MCPTT ID，组 ID 放在 mcptt-calling-group-id，mcptt-calling-user-id 随通用 helper 复制保留。Contact 则携带组会话身份和 isfocus 等标记，Referred-By 携邀请者的公共用户身份。T-PF 先检查 isfocus，缺失403+Warning104并停止；再检查所需应答设置，缺失480+Warning146并停止，只有继续到 step4–5 才按被邀 MCPTT ID 查公共身份绑定，缺失404。按需下发时，T-PF 的 Request-URI 写该被邀用户公共身份，PAI 复制收到的 CF 身份；Contact 使用与收到的会话身份相映射的会话身份。自动和手动通用入口先按空闲预建立会话及语音/话权媒体段匹配选择承载，不能仅由主叫按需便推断被叫一定按需。客户端应答模式及200证据见组呼客户端主题，本页不重复其用户接受流程。

规范强度：所述请求身份构造、绑定检查及相应拒绝、承载条件分派为 SHALL；通用 INVITE helper 的 Session-Expires 为 SHOULD，Resource-Share 为 MAY，不将可选头当准入前提。
- 边界：T-PF PSI 的发现是 §10.1.1.4.1.1 NOTE1 明示的未规定接口；不要用目标用户 ID 直接替代路由 PSI。
- 边界：T-PF 的普通组入口不包含私呼的 IncomingPrivateCallList/Warning159 检查；不能从私呼主题移植该拒绝。其已存设置与客户端模式选择不替代 CF 的组资格。
- 边界：MIME 复制仍受 §6.3.2.2.9 的已复制判断和 MKFC-GKTP 排除约束；该 helper 的位置 MIME 条件与后续复制目标字面名称不同，§10.1.1.3.2 NOTE2 又使用 MKFC-GKTPs，不把这些字样静默统一。
- 边界：这里只说明身份及承载交接责任，不把邀请发送、Contact 映射、SIP200或会议通知当作所有用户接听、实际话权获准或媒体可用的同一证据。

依据：3gpp-ts-24.379-v16.14.0 §10.1.1.4.1.1 opening and steps1–9，印刷页 240,241；3gpp-ts-24.379-v16.14.0 §6.3.3.1.1–6.3.3.1.2 full，印刷页 105,106；3gpp-ts-24.379-v16.14.0 §10.1.1.3.2 full，印刷页 238；3gpp-ts-24.379-v16.14.0 §6.3.2.2.3 full;6.3.2.2.5.1;6.3.2.2.5.2 steps3–11;6.3.2.2.6.1;6.3.2.2.6.2 steps1–10，印刷页 94,95,96,97,98,99；3gpp-ts-24.379-v16.14.0 §6.3.2.2.9 full;6.3.2.2.1;6.3.2.1.1.1，印刷页 83,93,94,102,103；3gpp-ts-24.379-v16.14.0 §11.1.1.3.2 steps2–8 (private-call incoming-list comparison only)，印刷页 376,377。

## 组呼继续后，主叫能否收到未回 200 的受邀名单？

这里看本页「TNG1 到期或必需成员提前拒绝，CF 如何处理？」中的**提前继续**分支：TNG1 到期前，CF 实际收到已归属且标为必需的成员对本次邀请的最终失败；受邀 INVITE 的 200 计数达到门槛，策略允许继续，而且其余受邀客户端均回了 200。CF 据此向发起侧发送原 INVITE 的 200，Warning 文本带 111。以下按 §6.3.3.3 紧接其后的程序说明。仅抓到 200/111，不能据此定位到这条分支或认定名单已经发送。

**发名单还要看两件事：**CF 实际收到针对上述 200 的 SIP ACK；发起方的用户配置档明确将 `allow-to-receive-non-acknowledged-users-information` 设为 `true`。两项都成立，CF **可以**向发起客户端发送 SIP INFO，不是必须发送。INFO 走原发起请求建立的对话，`Info-Package` 为 `g.3gpp.mcptt-info`，带 `application/vnd.3gpp.mcptt-info+xml` 正文。发起终端本地发了 ACK，不等于 CF 收到了；配置允许也不等于终端最终收到了 INFO。

**名单只回答“哪些已被邀请的成员没有发送本次邀请的 SIP 200”。** 正文按 `non-acknowledged-user` 条目携带这些成员的 MCPTT ID，不只列有必需标记的成员。未被邀请的组成员不在集合内；有最终失败响应但没发本次邀请的 200，仍符合这个筛选条件。这里的 200 是**受邀 INVITE 的应答**，不是发起方给建呼 200 回的 ACK。名单不是组成员名册、实时缺席名单或语音收听记录。附录 F.1.3 允许相应元素使用加密内容，不能要求抓包必见明文 ID。

**另看 MESSAGE 与会议 NOTIFY。** 在 §6.3.3.3 的到期继续段，随后收到受邀 INVITE 的 200 或收到受邀客户端 BYE，CF 可以另向发起方在原对话内发 SIP MESSAGE，文字说明未齐必需成员时仍继续了组呼。该 MESSAGE 不是上述按人列 ID 的 INFO。到期继续段另有发会议 NOTIFY 的规定，收件人是会议事件订阅者。不能由收到 MESSAGE 或 NOTIFY 推定 CF 已发送这份 INFO。本文不把以 “above SIP 200” 限定的 ACK 分支推广成所有携 111 的成功响应都必须或都会发 INFO。

依据：[TS 24.379 V16.14.0（Rel-16，Stage 3）§6.3.3.3，到期继续、到期前继续及对应 ACK，印刷页 122–123](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=123)；[附录 F.1.3，元素保护，印刷页 547](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=548)、[n) 项，印刷页 551](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=552)。

