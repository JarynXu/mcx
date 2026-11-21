# 独立组紧急告警：本人发起、取消与反馈证据

## 适用范围

- 固定TS24.379 V16.14.0，在网直接组身份的独立告警客户端责任，主线为本人发起、本人取消及实际反馈。不是紧急组呼建立/升级流程，不扩离网、私呼目标、功能别名或区域触发。
- 用户请求、原请求响应、取消回执和接收通知分别适用；不把已授权、已起呼、已归属、所有人收到或成功取消设为共同前提。原文要求的授权与匹配条件只限制对应动作。
- 第三方取消、额外组紧急状态取消和服务器处理仅作必要接口/状态比较，不承诺完整端到端分发、归属或取消闭环。

## 本人告警发起：许可、位置和告警状态分别处理

条件：客户端收到用户向指定MCPTT组发送独立紧急告警的请求；先判断许可，只有获授权的发送分支执行构造与状态动作。不是已建立组呼或已获话权才可处理的事件。

客户端发起许可要求 allow-activate-emergency-alert=true，并且满足以下一种配置：DedicatedGroup且目标匹配uri-entry；或UseCurrentlySelectedGroup且目标组allow-MCPTT-emergency-alert=true。其他情况为未授权。获授权时，按§12.1.1.1构造预计out-of-dialog的SIP MESSAGE：P-Preferred-Service及带require/explicit的Accept-Contact携MCPTT ICSI，mcptt-request-uri为组身份、alert-ind=true、mcptt-client-id为发起客户端ID，可带P-Preferred-Identity。请求须携§6.2.9.1紧急位置报告：ReportType为Emergency；已配置EmergencyLocationInformation则按其内容填CurrentLocation，无该配置则包含按F.3.3填的CurrentCoordinate。客户端设置MES（若尚未set），置MEA2 confirm-pending，Request-URI指向服务该组身份的PF PSI并发送。

强度：授权分类、获准构造、位置、MES/MEA及发送为SHALL；P-Preferred-Identity为MAY，无位置配置时额外位置字段是NOTE中的本地策略选择。

- 这里的许可不是紧急组呼许可，也不保证CF授权。CF §6.3.3.1.13.1的DedicatedGroup分支还要求组allow-MCPTT-emergency-alert=true；不能因客户端通过便跳过服务端检查。
- F.3.3通用CurrentCoordinate为optional，不抵消本次无位置配置时caller要求包含坐标。§6.2.9.1称ReportType element，F.3.3称attribute；保留这个表示差异，不把本文当可直接发送的完整XML模板。坐标编码另依TS23.032，本文不说明如何取得定位。
- 独立告警本身不改变CF组in-progress紧急状态或EPS bearer优先级。MES、MEA、组状态与媒体许可不同；本页不展开功能别名、区域自动触发、离网或私呼目标告警。

依据：3gpp-ts-24.379-v16.14.0 §6.2.8.1.6；§12.0;12.1.1.1；§6.2.9.1;F.3.3 (EmergencyLocationInformation and Report)；§6.3.3.1.13.1 (group authorization comparison)；§4.6.3，印刷页 41,42,65,76,77,111,112,444,445,564,568,569。

## 发起响应改变MEA，不证明全组收到或显示

条件：原发起MESSAGE分别收到2xx或4xx/5xx/6xx；这是替代响应事件，不要求成功先发生。

收到发起MESSAGE的SIP2xx，客户端须置MEA3 emergency-alert-initiated；收到4xx、5xx或6xx须置MEA1 no-alert。失败时MES仍保持set，原文NOTE允许用户需要时手动清除；不能随失败自动清MES。仅在CF发起程序已进入§12.1.3.1 step4b的获授权分支、且未在前序处理或step4b(i)的归属资格处理中拒绝请求时，CF才在向其他归属成员发送通知、缓存告警后回200，并另行构造alert-ind-rcvd=true、alert-ind=true及入站client-id的MESSAGE，用于告知成功收到告警。它不是每个成员已收到、显示或读取的证明。

强度：响应对应MEA动作为SHALL；CF所述缓存/响应/回执动作仅在上述成功处理分支为SHALL；用户手动清MES和随后自动起紧急组呼是NOTE中的说明/实现选择，不升级为强制动作。

- §12.1.1.1 NOTE4允许实现随后自动起紧急组呼，但告警成功不等于呼叫已经建立或话权已授予。
- §12.1.3.1向其他归属成员循环调用通知helper；§6.3.3.1.11的描述却是已归属但未参与成员。保留caller与helper收件范围文字差异，不据此承诺所有成员分发闭合。
- Annex G是informative：G.5表以MEA1为初始状态，并说明MES可set或clear；不能把MEA1一律解释为非紧急。G.1将授权他人取消列入MES清理事件，但具体接收程序另有自己的状态动作，不能靠概览表补正文。

依据：3gpp-ts-24.379-v16.14.0 §12.1.1.1 responses/NOTEs3–4；§12.1.3.1 steps1–4b(vi) (success-branch guards and comparison)；§6.3.3.1.11–12;6.3.3.1.20；§F.1.3 items17–18；§G.1;G.5 (informative comparison)，印刷页 110,111,119,445,452,453,454,549,584,587。

## 原 MESSAGE 已回 200，发起者的告警回执从哪条链回来？

原请求的 SIP 200、给组内其他成员的告警通知、给原请求者的回执是三类记录。对本页的独立组告警，控制 MCPTT 功能（CF）在发起或取消程序各自的成功分支中，回复原请求，然后另发一份 SIP MESSAGE，告知这次告警或取消请求已被接收。这不是组成员已经收到、显示或阅读告警的回执。[TS 24.379 V16.14.0，Release 16，Stage 3，§12.1.3.1 第 4(b)(iii)–(vi) 项，印刷页 453–454](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=454)；[§12.1.3.2 第 2(e)–(k) 项，印刷页 456](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=457)；[§F.1.3 第 18 项，印刷页 549](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=550)。

**在 CF 发出的回执中，目的地和目标用户写在两处。** SIP Request-URI 指向与原请求者的 MCPTT ID 对应的终接参与功能（PF）地址，P-Asserted-Identity 填 CF 的 PSI。目标用户的 MCPTT ID 则写在 `application/vnd.3gpp.mcptt-info+xml` 正文的 `mcptt-request-uri` 中。CF 分别放入 MCPTT 和 MCPTT ICSI 的 Accept-Contact 条件；上述成功分支还写入 `alert-ind-rcvd=true`、发起为 `alert-ind=true` 或成功取消为 `alert-ind=false`，并按条文取相应入向请求的客户端 ID。要查回执，找这份独立请求，不拿原请求的 200 或某个成员收到的告警通知代替。[§6.3.3.1.20，印刷页 119](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=120)；[§12.1.3.1 第 4(b)(v)–(vi) 项，印刷页 453–454](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=454)；[§12.1.3.2 第 2(g)–(k) 项，印刷页 456](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=457)。

### 终接 PF 实收回执：查正文的用户 ID，不用自己的 PSI 查绑定

1. **先确认入口。** §12.1.2.3 从终接 PF 经初始过滤准则实收 MESSAGE 开始：入向 SIP Request-URI 是该 PF 自己的 PSI，MCPTT 信息正文含 `alert-ind-rcvd`。入口写的是元素**存在**，没有额外要求值为 true 或比对客户端 ID。回执声明成功、请求者匹配后更新本机状态，各有自己的条件。例如本人取消的客户端分支还要求 `alert-ind-rcvd=true` 和匹配已发请求的客户端 ID。组成员通知的程序是 §12.1.2.2；§6.3.1.3 的对应描述查 `alert-ind` 或 `emergency-ind`，没有说必须缺少 `alert-ind-rcvd`。因而不能仅凭 `alert-ind` 区分两种用途，也不据这几条补互斥分类或处理优先级。[§§12.1.2.2–3，印刷页 451–452](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=452)；[§6.3.1.3，印刷页 79](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=80)；[§12.1.1.2，印刷页 446](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=447)。
2. **区分两种失败。** 若资源不足而无法处理，或有拥塞风险，PF **可以**拒绝并回 500，亦可附 Retry-After；走拒绝分支就不继续做后续步骤。继续处理时，步骤 2 要求用正文 `mcptt-request-uri` 内的 MCPTT ID 查询它与公有用户身份的绑定。步骤 3 要求在找不到这项绑定时回 404。这不是“只要没看到正文或字段就必回 404”的规则。[§12.1.2.3 第 1–3 项，印刷页 452](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=453)。
3. **查实际出向 MESSAGE。** 找到绑定时继续构造并发送出向请求。复制入向 MCPTT 信息正文、P-Asserted-Identity，以及实际收到的全部 Accept-Contact 和 Reject-Contact（含特性标签、值、参数）。出向 Request-URI 要用公有用户身份。步骤 4(b) 却把相应 MCPTT ID 的位置写成**入向 SIP Request-URI**；入口说该 URI 是 PF 的 PSI，步骤 2 又从 **XML** 取 ID。排障时分开保留两份 SIP Request-URI、XML ID 和绑定结果。不能把入向 PSI 当用户 ID 去查，也不能用常见转发规则替本版文字选定步骤 4(b) 有歧义的输入。[§12.1.2.3 第 2–5 项及末段，印刷页 452](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=453)。

若只有一份 200，先把它对到实际请求和接收点。原请求的 200 不证明 CF 的回执已到 PF；PF 构造或发送回执不证明终端已实收。终接 PF 收到它自己发出的 MESSAGE 的 2xx，只证明实际有这份事务响应；本条没有规定可凭它断言原请求者已显示、读取或完成客户端状态更新，也没有规定必须把这一份 2xx 原样转回 CF。[§§12.1.2.3、12.1.3.1，印刷页 452–454](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=453)。

## 本人取消依实际回执处理，不能用2xx替代取消结果

条件：用户请求本人取消指定组告警时先检查allow-cancel-emergency-alert；只有其值true的请求获授权。构造发送、收到匹配取消回执、收到4xx/5xx/6xx是各自事件；未授权不执行发送分支。反馈不以已取消成功为前提。

本人获授权取消构造SIP MESSAGE，沿§12.1.1.2的MCPTT ICSI/Accept-Contact/P-Preferred-Identity规则，mcptt-request-uri为组身份、alert-ind=false，不含originated-by，Request-URI指向服务组的PF PSI；置MEA4 cancel-pending并发送。若另外请求且获准取消组in-progress状态，才另带emergency-ind=false。对实际已发请求，收到alert-ind-rcvd=true且mcptt-client-id匹配该已发请求ID的MESSAGE后：alert-ind=false且已发请求无originated-by时，须置MEA1并清MES；alert-ind=true、当前MEA4且已发请求无originated-by时，须回MEA3。该匹配反馈中emergency-ind存在且为false时另置MEGC1/MEG1，true不触发该清理。收到原取消请求的4xx/5xx/6xx时，只有本人请求且当前MEA4，并满足（响应alert-ind=true，或响应不含带alert-ind的mcptt-info正文），才按所列分支回MEA3。

强度：获授权后的构造、条件字段、发送及上述匹配/失败状态动作为SHALL；P-Preferred-Identity为MAY。

- §12.1.1.2取消构造未要求mcptt-client-id；F.1.2允许其缺省，F.1.3允许MESSAGE包含发起客户端ID，但并未强制所有取消自动添加。CF §12.1.3.2 step2i又从入站请求复制它，客户端反馈父守卫要求匹配。因此只能说明实际具有可匹配ID时的处理，不能自动沿用首次告警ID、从dialog推导，或保证构造步骤天然满足回执关联。
- 取消的SIP2xx不是本条清MEA/MES的事件；所列取消错误分支也不把MES自动设回set或清除。未列的alert=false错误响应等情况不补统一恢复。Annex G.5表把MEA4的MES描述为clear，而§12.1.1.2发送步骤只设置MEA4、在匹配成功反馈才明确清MES；保留差异，不用表格补发送时清MES。
- 第三方取消在构造中带originated-by=原告警者ID，因此不会套用本人无originated-by的MEA4及成功清MES分支。其完整权限、分发和完成责任不在本页。
- CF §12.1.3.2用§6.3.3.1.13.1判断取消授权，但被引用段只描述alert=true的发起授权。此处不能把客户端取消许可当CF许可或静默改编号。该CF入口仅alert=false，未附ongoing-call守卫。
- 额外组状态取消使用§6.2.8.1.7，只有true/false授权分支，未给缺失值默认。CF未获告警取消许可但获组状态取消许可的step1b(vi)写发送200并skip rest，后面仍列成功回执vii–ix；这是特定组合的顺序边界，不用它否定普通本人取消，也不补完组状态取消全链。

依据：3gpp-ts-24.379-v16.14.0 §6.2.8.1.6–7；§12.1.1.2 full；§12.1.3.1 step3;12.1.3.2 full (server boundary comparison)；§6.3.3.1.13.1;6.3.3.1.20；§F.1.2 client-id;F.1.3 items15/17/18；§6.3.2.2.9–11;12.1.2.3 (copy/receipt comparison)；§G.5 (informative comparison)，印刷页 65,102,103,111,112,119,445,446,447,452,453,454,455,456,545,547,548,549,587。

## 收到他人通知的显示、状态和200各有含义

条件：客户端实际收到§12.1.1.3的emergency notification MESSAGE。alert=true、alert=false及emergency字段分别按收到的内容适用；第三方取消只作接收状态比较，不假定本人取消请求存在。

alert-ind=true时，应显示告警及组身份、发起用户和mission-critical organization；提供functional alias时可显示它。alert-ind=false时，应显示取消及组身份，告警者取originated-by（若有），否则取mcptt-calling-user-id。若originated-by的MCPTT ID为接收用户自身，须置MEA1；本分支没有同样写清MES。收到emergency-ind=false时按对应程序另置MEG1/MEGC1；这不是单凭alert=false推导出的组状态取消。程序最终须生成并发送SIP200响应。

强度：告警/取消显示为SHOULD，functional alias显示为MAY；条件MEA/MEG/MEGC动作及200为SHALL。

- 本人匹配取消回执清MEA和MES，与第三方取消通知只明确清MEA并不对称。不能把前者的MES清理搬到后者，也不能把第三方通知当本人请求回执。
- §6.2.0.1 pp55–56完整客户端MESSAGE分类列表未列§12.1.1.3所用的精确emergency notification名称。本文按后者实际事件处理，不据这两页未列而断言全规范无支持，也不自行发明分类字段规则。
- 显示建议与发送200不能证明用户已经阅读。§12.1.1.3还有emergency=true及imminent状态通知分支，本页只保留必要取消比较，不承担完整紧急/迫近危险状态生命周期。

依据：3gpp-ts-24.379-v16.14.0 §12.1.1.3 full；§6.2.0.1 (classification comparison)；§6.3.3.1.11–12 (notification fields)；§F.1.3 items4/6/12/15；§12.1.1.2 (self-receipt comparison)，印刷页 55,56,110,111,446,447,448,548,549。

## 共同依赖与边界

- §6.5多MIME处理及§6.6的适用保护仍需执行；F.1普通字段类型与加密字段形式不可互换。本文止于这些实际接口，不提供完整SIP、XML编码、外部密码学或定位实现。
- MEA、MES、MEG/MEGC和CF组状态不是同一变量；informative状态表不能代替正文逐事件守卫。

依据：3gpp-ts-24.379-v16.14.0 §6.5;6.6.1 (protection interface only)；§F.1.2–3 relevant field representation；§4.6.3;G.1;G.5，印刷页 41,42,137,138,139,545,547,548,549,584,587。

## 相关主题

- [紧急组呼客户端](emergency-group-client.md)：组呼发起、升级与本人紧急状态取消。
- [紧急组呼服务器](emergency-group-server.md)：已有会话CF re-INVITE职责，不能替代独立告警MESSAGE。
