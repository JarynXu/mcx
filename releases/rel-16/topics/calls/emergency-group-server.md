# 已有按需预安排组会话：CF紧急升级、取消与分层反馈

## CF 主线适用条件
- 固定TS24.379 V16.14.0，本节的报文处理面向在网已有按需预安排组会话，直接组身份，由其controlling MCPTT function处理re-INVITE。排除初始建立、chat/预建立、临时/重组、广播/system、离网、跨系统及完整媒体/话权算法。 下文另列本组 TNG2 到期；到期的非参会通知不以活动组会话为条件。
- 先说明 emergency-ind 升级或取消，以及组状态和告警的各自条件；终接 PF、CF 的 200 带 149 的另外两种业务回报各在单独一节。本文不展开随呼告警发送或迫近危险的完整生命周期。
- 每条按实际角色、请求/响应/ACK事件及旧组状态分别适用；不以已获授权、组状态false、已取消成功或所有下游已响应为共同前提。CF组状态与客户端MEG/MEGC/MES/MEA不可互换。

## 已有会话先验证字段组合，再按用户与组配置判断升级权限

适用条件：CF收到以MCPTT session identity识别已有按需预安排组会话的re-INVITE；各拒绝检查和相应权限分支分别适用，不预设请求有效或已获授权。

资源不足或有拥塞风险时CF MAY用500拒绝，MAY带Retry-After并跳过后续步骤；紧急请求可被选择接受。含emergency-ind或imminentperil-ind时须调用字段验证：emergency=true要求alert存在且imminent不存在，emergency=false允许alert存在或缺失但imminent须不存在；无效组合须403/150。升级权限要求调用用户allow-emergency-group-call=true，且（DedicatedGroup配置匹配目标组并且目标组allow-MCPTT-emergency-call=true，或UseCurrentlySelectedGroup并且目标组allow-MCPTT-emergency-call=true）。其余升级请求未授权，须403携emergency=false及alert=false并停止。若Resource-Priority为紧急值、请求未含emergency且组当前紧急状态false，也须403并停止。

规范强度：资源/拥塞拒绝及Retry-After为MAY；字段验证、授权判定和所列403分支为SHALL。

- §6.3.3.1.17的无效组合段写发送403，未另写统一skip-rest；不能把其他拒绝分支的停止措辞补到该段。
- 入口为已有会话的re-INVITE，不借初始INVITE的PSI分类、成员准入或客户端已授权证明CF再次授权；组业务形态为预安排不等于其当前紧急状态必须false。
- §6.6收取保护处理先于业务过程，发送保护及多MIME/SDP首体义务仍适用；本页不实现XML验证、配置获取、密钥或完整SIP事务。字段不存在与false按各条款区别处理。

依据：TS24.379 V16.14.0 §10.1.1.4.7 opening, steps1–5；§6.3.3.1.13.2;6.3.3.1.14;6.3.3.1.17；§6.3.1.1 (initial INVITE classification comparison)；§6.5;6.6.1.1–4；§F.1.3 relevant identities/boolean fields，正文页 78,112,113,116,117,118,137,138,139,253,254,547,548,549。

## 已紧急与首次升级使用不同分发及计时分支

适用条件：请求emergency=true且CF按§6.3.3.1.13.2判为授权；本文不发起新告警，alert=false。另一个事件是所发下行re-INVITE收到200，其媒体动作只在该事件发生时适用。

CF缓存发起紧急呼叫的MCPTT ID。组已紧急时，按caller为其他已归属成员生成并发送emergency=true的MESSAGE；若组迫近危险状态true则清为false。组原非紧急时，置紧急状态true，启动TNG2，按§6.3.3.1.6向其他参与者生成并发送re-INVITE；收到对应200才调用媒体接口。该helper采用当前与终接客户端建立的媒体参数、发起者ID及紧急Resource-Priority，携emergency=true；本页无新告警时携alert=false。若TNG3正在运行且发生升级，停止TNG3，TNG2取服务配置group-time-limit；启动TNG2时不启动TNG3。

规范强度：所列缓存、分支状态、构造发送及定时动作为SHALL；媒体调用为收到对应响应后的SHALL。

- §10.1.1.4.7 step6(iii)写each other affiliated member，而被调用§6.3.3.1.11描述affiliated but not participating，不能擅自统一收件集合。helper以目标用户的终接PF为Request-URI，体内分别标目标用户和业务组，身份与路由不是同一个字段。
- 已true分支未重列启动TNG2，不能把false→true分支的重启条件加给所有重复升级。B.2.1-1的概括性启动行不能抹掉程序分支。TNG2实例关联单组的紧急状态，不是全系统唯一计时器。
- §6.3.3.1.6按紧急状态选择Resource-Priority，namespace/priority取§6.3.3.1.19服务配置，不硬编码。升级若含mc_implicit_request仅被识别为隐式话权请求，不证明话权获准或RTP送达。
- CF管理组in-progress emergency状态；MEG是客户端对该状态的视图，MEGC为客户端本人请求状态。Annex G为informative，不据其表格造CF状态变量或全设备原子同步。

依据：TS24.379 V16.14.0 §10.1.1.4.7 step6；§6.3.3.1.6;6.3.3.1.11；§6.3.3.1.13.1 (excluded new-alert comparison)；§6.3.3.1.19;6.3.3.5.2；§B.2.1 Table B.2.1-1 TNG2/TNG3；§6.4 re-INVITE implicit-request branch；§G.3–4 (informative perspective text)，正文页 107,108,110,111,112,118,119,125,137,254,533,585,586。

## 取消失败与取消组状态、告警缓存是不同分支

适用条件：收到emergency=false的re-INVITE；未授权拒绝分支与条文所写授权且组当前紧急的正向分支为替代分支。正向授权回指存在下述缺口，不能假定其已得到修复；收到下行200是另一个独立事件。

§6.3.3.1.13.4将allow-cancel-group-emergency=true/false分别判为授权/未授权。未授权时CF须403携emergency=true；仅请求alert=false且该用户有未结告警时另携alert=true，发送后停止。正向step8在其所写授权判断且组状态true时要求清组紧急状态、清该用户未结紧急组呼缓存。仅请求alert=false、告警取消权限成立且该用户有未结告警时，按originated-by存在则指定目标、缺失则请求发送者清告警缓存。向其他参与者发送§6.3.3.1.6 re-INVITE，收到对应200才调用媒体；停止TNG2；向已归属但未参与成员发送emergency=false的MESSAGE，仅已满足上述告警取消条件才另携alert=false。TNG2运行中取消时，§6.3.3.5.2还要求停止TNG2并按组on-network-maximum-duration启动TNG3。

规范强度：授权true/false判定、拒绝、满足各自条件的缓存/状态/分发/计时动作为SHALL；正向分支保留原文授权回指，不把缺口改写成实现保证。

- §10.1.1.4.7 step8正向授权回指§6.3.3.1.16，但.16实际是TNG2到期处理；负向step7才引用.13.4。不能静默更正、据此宣称取消授权到成功的完整可执行链已闭合。
- 组取消和告警取消helper分别只列true/false，没有定义缺配置元素的结果；同页private分支写false or not present，不可移植到组。告警取消权限与组取消权限不合并。
- §6.3.3.1.6 step4(b)(ii)的告警取消权限回指.15，实际.15为imminent-peril re-INVITE生成，不是.13.3。helper仍写满足其条件才携alert=false，存在originated-by时复制；不能删掉该差异以保证所有接收端清告警。
- TNG2到期的.16是另一个事件：降低组状态并通知；不证明等同用户取消的缓存清理。TNG3到期才调用会话释放，本页不展开其BYE链。取消紧急状态不等于结束会话、清所有用户MES或清所有告警。

依据：TS24.379 V16.14.0 §10.1.1.4.7 steps7–8；§6.3.3.1.13.3–4；§6.3.3.1.6;6.3.3.1.11；§6.3.3.1.15–16 (cross-reference/expiry comparison)；§6.3.3.5.1–2;B.2.1 Table B.2.1-1；§F.1.3 originated-by，正文页 107,108,110,113,116,117,124,125,254,255,533,549。

## 200、149和ACK后的INFO不能合并为业务全部完成

适用条件：分别观察：p256明确的收到下行re-INVITE之200事件；发往邀请客户端的200携149后收到其ACK事件；或发出的MESSAGE收到2xx事件。三者互不作为全局AND前提。

p256先以收到re-INVITE之200为事件要求调用媒体，随后列生成并向MCPTT客户端发送200、按§6.3.3.2.1生成SDP应答、Supported包含norefersub和tdialog等步骤。SDP对被接受媒体及控制通道使用CF的IP/端口，控制通道fmtp交给媒体规范接口。若请求alert=false但告警取消未授权，200须带149 SIP INFO request pending。只有该200携149且收到客户端ACK，才调用§6.3.3.1.18，在原dialog发送Info-Package=g.3gpp.mcptt-info的INFO；未授权告警取消分支携alert=true。对发出MESSAGE的2xx则按SIP规范处理。

规范强度：满足各自事件与字段条件时，200构造/发送、149、ACK后INFO及相关媒体调用均为SHALL；不把这些事件写成必然发生。

- p256的Upon receiving a SIP200是独立正文行，不能改成收到原请求即无条件生成200，也不能推导等待全部下游200的算法。组已紧急而仅发MESSAGE等路径与该200段怎样衔接，所读段未完整说明，本页不补时序。
- 这里只取未获准撤警的 149。未获准发起告警、组已紧急时的获授权迫近危险请求也可能收到 149，见下文。§6.3.3.1.18 的三种 INFO 正文不能互相套用。
- 媒体规范与完整SIP/RFC接口未展开；200/ACK/INFO、通知2xx均不等于全部成员状态同步、告警已取消、获话权或媒体交付。客户端状态按其自身接收事件处理，不能用客户端common为CF成功背书。

依据：TS24.379 V16.14.0 §10.1.1.4.7 p256 response/ACK/MESSAGE branches；§6.3.3.2.1；§6.3.3.1.18;6.3.3.1.13.1/.13.3 (149 branches)；§F.1.3;6.5;6.6.1.1–4，正文页 111,112,113,118,119,120,137,138,139,256,547,548,549。

## 已有预安排组呼更新优先状态：终接 PF 如何转送 re-INVITE？

这段看的是**终接参与功能（PF）收到发往本场终端的 re-INVITE**，不是控制功能（CF）判断能否升级。只取本页已有按需预安排组会话的范围。§10.1.1.3.6 的入口是 MCPTT 信息正文有 `emergency-ind` 或 `imminentperil-ind`。**明确写 false 仍有这个元素；两个元素都没带，不能仅凭 SIP 的 Resource-Priority 头或正文里的 `alert-ind` 就套这段。** 这个入口也不替 CF 完成字段组合校验或授权。[TS 24.379 V16.14.0，Release 16，Stage 3，§10.1.1.3.6，印刷页 239–240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)。

### 入向有优先级头就照值带出，缺头时本条不要求补值

PF 须检查入向请求有没有 `Resource-Priority`。若有，出向 re-INVITE 须按入向内容填该头；对实收的头可按 TS 24.229 进一步处理；这些动作超出本 TS 24.379 的范围，不能凭头值判断媒体优先级已经生效。若入向没有该头，这两条没有要求 PF 用 `emergency-ind` 或 `imminentperil-ind` 另算补值，也没有把缺头列为拒绝或停止转送的条件。PF 不是这里为初始 INVITE 纠正头字段的 CF。后者在适用分支走可靠 183、收到对应 PRACK 后回复 200，并构造 UPDATE；不能用这条流程替终接 PF 的 re-INVITE。[§10.1.1.3.6 第 1–4 项，印刷页 239–240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=240)；[§6.3.2.2.10，印刷页 103](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=104)；[§6.3.3.1.8，对照，印刷页 109](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=110)。

终接 PF 向终端构造出向 re-INVITE，`Supported` 须含 `tdialog`，可以带 `Resource-Share`。正文按 §6.3.2.2.9 处理。以此次 MCPTT 信息正文为例，尚未复制时复制内容，不把实收正文里的 `MKFC-GKTP` 元素复制出去。不能要求两个腿的正文逐字节相同。给终端的 SDP offer 以同一份入向 re-INVITE 的 offer 为基础，按需会话的辅助程序只保留一个 MCPTT 语音媒体段，入向有媒体面控制段时也包含该段；按条文条件替换地址和端口，不把这次 offer 当成照搬另一条腿的 SDP 或旧会话模板。[§§6.3.2.2.9–10，印刷页 102–103](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=103)；[§10.1.1.3.6 第 2–4 项，印刷页 240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=241)；[§6.3.2.2.1、§6.3.2.1.1.1，印刷页 83、93](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=84)。

### 终端这一腿的 200 到了，PF 才构造返回控制侧的 200

PF **实际收到终端对上述出向 re-INVITE 的 SIP 200** 后，先按 §6.3.2.2.4.2 生成返回控制侧的 200，按按需会话规则以终端这份 200 的 SDP answer 为基础生成自己的 answer，与媒体面交互，然后转送该 200。比如返回的 Contact 采用映射到 CF 入向请求 Contact 所给标识的 MCPTT 会话身份，不是原封搬运终端的 Contact。这里的入口是实际收到**对应出向事务的 200**，没有把 ACK 列为调用媒体面的前置事件；也不因此替代 SIP 本身的 ACK 处理。[§10.1.1.3.6 收到 200 后第 1–4 项，印刷页 240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=241)；[§6.3.2.2.4.2，印刷页 95](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)；[§6.3.2.2.2.1、§6.3.2.1.2.1，印刷页 84、94](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=85)。

要验的是同一 PF 的入向和出向两个 re-INVITE、终端这份 200、媒体接口调用及返回控制侧的 200。只有终端腿 200 时，仍缺媒体接口调用和返回控制侧的记录。PF 返回了 200，只说明这条响应，不单独证明 CF 已实收、终端已经更改优先状态、承载优先级已经生效或媒体已经送到听众。

## 范围与相关主题
- 这是CF局部职责与真实接口边界，不是完整全组紧急生命周期；配置、身份建立、SIP事务、告警服务及媒体实现各有外部依赖。
- 正向取消授权错回指、通知收件范围和响应事件衔接差异均保留，不据有效输入假定这些缺口已经解决。

- [客户端紧急请求与状态](emergency-group-client.md)：按客户端事件读取，不证明CF授权。
- [普通预安排组初始服务器准入](prearranged-server-admission-routing.md)：仅比较初始入口，不能解除其普通组共同条件。

## 200 带 149：随呼告警或迫近危险请求结果怎么看？

这里看在网已有按需预安排组呼的 **CF 对邀请客户端所发 re-INVITE 回 200** 的情形。Warning 文本中的 149 表示还要看后续 INFO，不能直接把 SIP 事务成功记成请求的每项业务都成功。以下两项与上文“请求撤警未获准”共用 149，但业务结果和 INFO 正文不同。〔[TS 24.379 V16.14.0，§4.4.2 表 4.4.2-2，印刷页 37](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=38)；[§10.1.1.4.7，印刷页 256](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=257)〕

| 原来实际收到的请求和 CF 判定 | 发送 149 后的 INFO 应写什么 | 怎么读 |
| --- | --- | --- |
| 带 `emergency-ind=true` 和 `alert-ind=true` 的合法组合；紧急组呼获准，但独立的随呼告警未获授权 | `emergency-ind=true`、`alert-ind=false` | 这次告警未获准，不把获准的紧急组呼当作整笔拒绝，也不推定以前的告警因此清除。 |
| `imminentperil-ind=true` 的迫近危险请求获授权，但该组已经处于进行中的紧急状态 | `imminentperil-ind=false`、`emergency-ind=true` | 迫近危险这一项未获准；本次请求按紧急级别获准。不是发起人取消了迫近危险，也不是它申请的迫近危险级别生效。 |

依据：[§6.3.3.1.17–18，印刷页 117–118](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=119)；[§10.1.1.4.7 响应第 5、7 项及注 5，印刷页 256](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=257)。对合法的迫近危险入口，原请求不含 `emergency-ind` 或 `alert-ind`；不要用 INFO 回报的组合反推原请求就写了这两个字段。两条都是到了本节的 200 构造步骤才加 149。未获准发起紧急组呼本身走前面的 403 分支；尚未处于紧急状态时的迫近危险请求转走 §10.1.1.4.8，不能套表里的第二行。这里以该请求实际获授权为前提。固定版的请求第 4 项字面回指 §6.3.3.1.13.6（取消授权），发起授权另列于 §6.3.3.1.13.5。两处不能当成同一个检查，不用响应码反推授权，也不替第 4 项改引用。〔[§6.3.3.1.13.5–.13.6，印刷页 113–114](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=114)；[§10.1.1.4.7 请求第 4 项，印刷页 254](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=255)〕〔[§10.1.1.4.7 请求第 2–4、9 项，印刷页 253–255](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=254)〕

**先把 ACK 对到 CF 发出的那份带 149 的 200。** CF 实际收到这份 ACK 后，才按 §6.3.3.1.18 向邀请客户端在原对话发 INFO。要找的消息带 `Info-Package: g.3gpp.mcptt-info`，以及 `application/vnd.3gpp.mcptt-info+xml` 正文。按同一对话核对原请求、该 200、匹配 ACK 和 INFO 业务字段。有 200、还没有后续消息的证据时，只能记录当前事务的响应，不能断言 INFO 已发送、终端已收到或实际承载已切换。客户端怎样处理实收 INFO，另查[客户端紧急请求与状态](emergency-group-client.md)。〔[§10.1.1.4.7，印刷页 256](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=257)；[§6.3.3.1.18，印刷页 118](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=119)〕

## TNG2 到期：取消组紧急状态，不是结束组呼

控制功能（CF）实际处理本组的 TNG2 到期时，须把组的进行中紧急状态置为 `false`。**看成员是否参加本场，而不是是否正在发言**，再判断应收到哪条消息。这个入口不等同于有人发起取消请求。〔[TS 24.379 V16.14.0 §6.3.3.1.16，印刷页 117](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=118)〕

- **仍有活动组呼或组会话，且该成员参加了本场。** CF 须向各参会成员发 re-INVITE。它按当前与终接客户端已建立的媒体参数生成 SDP offer，写普通组呼的 `Resource-Priority`，在 MCPTT 业务正文写 `emergency-ind=false`。CF 实际收到对这笔 re-INVITE 的 200，才按这一入口与媒体面交互。它没有要求为本次到期先发送 BYE，也没要求收齐所有人的 200 才清组状态。〔[§6.3.3.1.9–10，印刷页 109–110](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=111)；[§6.3.3.1.19 普通级别，印刷页 119](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=120)〕
- **已归属但不参加本场。** CF 对各符合条件的成员另发 SIP MESSAGE，前面“有活动组呼或组会话”的条件没有写在这一项。SIP 的 Request-URI 是与目标用户 MCPTT ID 对应的终接参与功能地址；正文的 `mcptt-request-uri` 才填目标用户的 MCPTT ID，`mcptt-calling-group-id` 填组 ID，`emergency-ind=false` 表示这次组紧急状态取消。CF 的 PSI 放在 `P-Asserted-Identity`，该版写 MCPTT ICSI 放在 `P-Asserted-Service-Id`。这条通知不等参会侧 re-INVITE 的 200。〔[§6.3.3.1.11，印刷页 110](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=111)；[§6.3.3.1.16 第 3 项，印刷页 117](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=118)〕

**仍在进行的组呼，普通计时器从组配置取值。** 对仍继续、组文档含 `on-network-maximum-duration` 的呼叫，运行中的 TNG2 到期后，CF 按该字段启动 TNG3，不是把原 TNG3 剩余秒数接着倒计时。到期段没有给字段缺失时另设默认时长。这两类计时器事件中，TNG3 本身到期才调用会话释放程序。核对普通优先级请求、收到的对应响应、实际承载及 TNG3 的启动记录，不把它们当成同一个事件。〔[§6.3.3.5.1–2，印刷页 124–125](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=126)；[表 B.2.1-1，印刷页 533](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=534)〕

例如，乙已归属但没加入这场组呼，适用的是 MESSAGE，不应拿乙没有 re-INVITE 当故障。若只有乙说没收到，还要查 CF 为乙发出的消息及乙端实际收件。到期条款没有列取消 `alert-ind` 所表示的告警、清告警或发起者缓存的动作，也不保证终端状态、媒体或承载已改变。〔[§6.3.3.1.16，印刷页 117](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=118)〕
