# MCPTT 和 MCVideo 在同一台终端共享 SIP 注册，怎样判断哪项业务已获授权？

一台终端上，MCVideo 已在运行，用户又启动 MCPTT。即使只看到一份 REGISTER，且 Contact 带有 MCPTT 标记，也不能据此把两项业务都记为“已授权”。**SIP 注册由同一终端上同时运行的 MC 业务客户端共享；业务授权要看请求针对哪项业务、该业务服务器怎样处理。** 以下以 Rel-16 的在网 MCPTT 为例。[TS 24.379 V16.14.0，Stage 3，§7.1，印刷页 147–148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=149)

## 增减一项业务，共享注册怎样变？

同一台 MC 终端上的 MCPTT 和其他 MC 业务客户端同时运行时，各自的注册程序合成一份 REGISTER。若 MCVideo 本来就在运行，MCPTT 注册时要**再注册，带上 MCVideo 等原有运行中业务的参数**。反过来，若用户退出 MCPTT，MCVideo 仍须保持注册，终端也要再注册：从 Contact 去掉 `g.3gpp.mcptt` 以及值指向 MCPTT 的 `g.3gpp.icsi-ref`，保留其他运行中业务的参数。不能把这次 MCPTT 退出记成整机注销。[§7.1，印刷页 148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=149)

一份 REGISTER **可以**列多个 Contact，每个业务客户端一个，前提是这些地址的 **IP 和端口都相同**。这是地址出现的条件，不是授权计数。若确实用这份 REGISTER 同时办理多项业务的授权，即使这些业务可以使用同一个访问令牌，也要按业务分别提供 MIME 正文。只有注册请求时，不能反过来假定其中有每项业务的授权材料。[§7.1，印刷页 148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=149)

## Contact 一样，授权请求看哪里？

**注册 MCPTT 客户端**时，无论只做 SIP 注册，还是用 REGISTER 一并申请 MCPTT 授权，都要求 Contact 携带那两项标记；后一项 ICSI 的值是 `urn:urn-7:3gpp-service.ims.icsi.mcptt`。只看到标记，连“本次请求了 MCPTT 授权”都还不能确定。[§7.2.1，印刷页 148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=149)；[§7.2.1AA，印刷页 149](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=150)

用户认证成功、访问令牌可用时，看实现选择哪种请求来办授权：

- **REGISTER：** MCPTT 的业务信息正文携带认证所得的访问令牌和发起端的 MCPTT 客户端 ID。
- **PUBLISH：** 除上述授权资料，还要带业务设置正文，其中有当前应答方式和所选用户配置档的索引。若只是设置、更新、刷新或移除已有设置，另见[只发布 MCPTT 设置](../calls/settings-publication.md)；一个 PUBLISH 或一份设置正文本身不能区分两条分支。

以下保护规则针对上述两种**办理 MCPTT 授权的请求**。若机密性、完整性保护都关闭，令牌和客户端 ID 按原值携带。任一保护启用便另带密钥材料；启用机密性时加密令牌和客户端 ID，启用完整性时保护 MCPTT 业务信息正文，授权用 PUBLISH 还保护设置正文。因此未看见明文令牌不等于没有提交授权，提交了也不等于获准。[§7.2.1，印刷页 148–149](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=149)；[§7.2.2，印刷页 150–151](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=151)

<a id="continuity-registration"></a>
### 业务授权另用 PUBLISH，注册时还要管连续性吗？

要看**客户端是否支持 MCPTT 业务连续性**。支持时，用 REGISTER 一并申请业务授权（§7.2.1），或只注册、不用这份 REGISTER 申请业务授权（§7.2.1AA），两条各自都要求客户端遵循 TS 24.237 §6.2.2 的 PS–PS 连续性 IMS 注册程序。改用 PUBLISH 办授权不会免除这项要求，也不意味着要做两次注册。§5.2 在说明符合连续性程序的客户端须实现什么时，点名 §7.2.1 的注册要求和 §14A 的会话转移程序；仅注册分支的依据则是 §7.2.1AA 自己的明文。[TS 24.379 V16.14.0 §5.2，印 51](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=52)；[§7.2.1，印 148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=149)；[§7.2.1AA，印 149](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=150)。

前述两项 Contact 标记在两种注册方式里都要带，不能拿它们或一个注册 200 当作终端支持接入转移的证明。这里不从所引程序推算额外必带的 REGISTER 字段。若是在验收网络部署，另查[注册时 SCC AS 是否在路径上，主叫和被叫时它分别排第几](../bearers/anchored-session-transfer.md#scc-as-path)。

如果是在验收终端的授权 REGISTER，查[客户端 ID 应生成什么值，明文和密文各用哪个 XML 子元素](mcptt-client-id-lifecycle.md#client-id-on-wire)。

## 到 MCPTT 服务器，查哪项结果？

| 服务器收到什么 | 它怎样识别用户、检查授权 |
|---|---|
| **第三方 REGISTER**，其 `message/sip` 正文内嵌客户端发出的 REGISTER，内层 MCPTT 业务信息含令牌及客户端 ID | 从**第三方请求**识别 IMS 公共用户身份，从**内嵌的客户端请求**依 §7.3.1A 识别 MCPTT ID。检查这个 MCPTT 用户在业务配置中的并行授权上限。达到上限就停止本节后续步骤；这一步**没有指定响应码**。未达上限，才对该 MCPTT ID 执行业务授权。[§7.3.1，印刷页 153](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=154)；[§7.3.2 步骤 1–3，印刷页 155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=156) |
| **办理授权的设置 PUBLISH**：§7.3.1 列 MCPTT 特征标记及 require、explicit 参数；§7.3.3 入口要求 Event 为 poc-settings、有设置正文，且 MCPTT 业务信息含令牌及客户端 ID | 从 **P-Asserted-Identity** 识别 IMS 公共用户身份。先做 §7.3.1A 的保护处理，失败返回 **403，警告文本以 140 开头**，不再查额度。通过后才检查该用户的并行授权上限；达到上限，返回 **486 Busy Here，警告文本以 164 开头**，并停止。未达上限才做业务授权，授权失败返回 **403，警告文本以 101 开头**，并停止。[§7.3.1，印刷页 153](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=154)；[§7.3.3 步骤 1–6，印刷页 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=157) |

读一条失败记录时，先看 SIP 响应状态，再分清 Warning 的外层警告码和引号内的 MCPTT 文本。MCPTT 的三位业务码在**引号内**，后跟空格和说明文字。如果两条 PUBLISH 失败记录都显示 SIP 403、外层警告码 399，一条的文本以 140 开头，另一条以 101 开头，前者停在保护处理，后者停在业务授权。399 本身区分不出原因。§4.4.1 的 399 示例在 INVITE 的语境里；这里的两个 399 是观察值，不据此要求所有 PUBLISH 都用 399。[§§4.4.1–2、表 4.4.2-1，印刷页 33–34](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[§7.3.3 步骤 3、3a、6，印刷页 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=157)

**同一用户的第二个 MCPTT 客户端，是另一个问题。** 服务器用收到的客户端 ID 与已有绑定比较。若该用户已在另一客户端获 MCPTT 授权，而且这次授权也成功，须保留旧绑定，并为新客户端增加「MCPTT ID、MCPTT 客户端 ID、IMS 公共用户身份」的绑定。REGISTER 分支的依据是 §7.3.2 步骤 **4a**；紧邻的步骤 4 把 MCPTT ID 写了两次，不能把第二处自行改成客户端 ID 当作通则。步骤 4a 规定何时保旧增新；注 2 补充数据库保存的内容：除上述三项，还保存一个用于寻址 MCPTT 服务器的标识。PUBLISH 分支见 §7.3.3 步骤 5a–b。[§7.3.2 步骤 4、4a 及注 2，印刷页 155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=156)；[§7.3.3，印刷页 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=157)

当该 MCPTT ID 的绑定**多于一个**时，服务器在这条分支的 200 OK 中将 `multiple-devices-ind` 置为 true。对 PUBLISH，还须业务授权成功且发布处理成功，才走到缓存设置、回 200 的步骤。这里数的是**一个用户在 MCPTT 的绑定**，不是一台终端上运行的业务、REGISTER 或 Contact 数。只见普通 SIP 注册的 200，不能替 MCPTT 或 MCVideo 签认业务授权。[§7.3.2 步骤 6，印刷页 155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=156)；[§7.3.3 步骤 6–9，印刷页 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=157)

## 一次 PUBLISH 同时办理授权、发布设置：绑定以后失败怎么办？200 又能证明什么？

这里看服务端实际收到的授权用 PUBLISH：`Event: poc-settings`，有 `application/poc-settings+xml` 设置正文，另有含 `mcptt-access-token` 和 `mcptt-client-id` 的 MCPTT 业务信息正文。服务器从 `P-Asserted-Identity` 识别 IMS 公共用户身份。只发布设置走另一个程序；不能把那一支的有效绑定检查或 404 搬到这里。[TS 24.379 V16.14.0 §7.3.3，入口及步骤 1，印刷页 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=157)。

**授权通过，设置仍可能发布失败。** 第 5a 项要求服务器把 MCPTT ID 和客户端 ID 绑定到 IMS 公共用户身份；符合同一用户先前已在另一客户端获准的条件时，第 5b 项要求保留旧绑定、增加新绑定。随后，第 7 项才按所引 RFC 3903 处理这次发布。若处理失败，到此停止：不执行第 8 项的本次设置缓存，也不发第 9 项的成功 200。第 7 项没有指定失败响应码。它也没说先前的绑定会回滚或一定持久保留，更没说要清空旧设置。要判断故障后的状态，须核对绑定和缓存的实际记录；不能把一次失败当成授权未通过，也不能拿前面的 403 或 486 给这一步定性。第 5c 项的 Resource-Share 另有条件，这里不展开。[§7.3.3，步骤 5–9，印刷页 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=157)。

**发布处理成功，先缓存，再发 200。** 服务器把本次收到的设置缓存到设置定时器到期，再发 SIP 200 OK；该 MCPTT ID 有多于一条绑定时，响应的 MCPTT 业务信息正文带 `multiple-devices-ind=true`。这个指示说的是绑定数，不是其他客户端已经收到新设置。[§7.3.3，步骤 7–9a，印刷页 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=157)。

**发出 200 后，条文还列了这些服务端步骤：**

1. 用 `am-settings` 中的 Answer-Mode Indication 作为**这个客户端**当前的应答方式（第 10 项）。
2. 服务器还没存有所需用户配置档时，才从 MCPTT 用户数据库下载。请求带 `selected-user-profile-index`，就用索引确定这个客户端的活动配置档；若需下载，只需取所选的那一档。无索引且已存或下载了多档，找含 `Pre-selected-indication` 的那一档作为活动档；只有一档时，注 3 说明该档默认为预选档（第 11–12 项、注 2–3）。这是接收端对缺索引的处理，不改变前述客户端构造授权请求的要求。[§7.3.3，步骤 10–12、注 2–3，印刷页 157](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=158)。
3. 对所服务的 MCPTT ID，若其用户配置档的 `OnNetwork/ImplicitAffiliations` 内至少有一个含 MCPTT 组 ID 的 `entry`，就须调用 §9.2.2.2.15 的隐式归属程序。调用程序不等于已成功归属到某个组。[§7.3.3，步骤 13，印刷页 157](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=158)。

排查时先把 200 与**这笔授权用 PUBLISH** 对上。服务端发出响应，不等于请求端已经收到；即使请求端收到了，也不能凭这份响应判定应答方式或配置档在那一刻是否已生效。查本客户端状态要看服务端实际采用的应答方式和活动档，查某个组要看归属程序的结果。另一客户端是否收到了 [NOTIFY](../calls/settings-observation.md)，要看另一笔通信。

## 资源共享：服务器怎样认出办理注册的是哪台设备？

参与 MCPTT 功能（PF）收到第三方 REGISTER，要分两层读。外层的 `message/sip` 正文里是一整份客户端 REGISTER。**内层请求头**里的 `Resource-Share: supported` 回答“SIP 核心网支持资源共享吗？”；**同一份外层请求的 Contact 头参数** `+g.3gpp.registration-token` 携带办理注册的 MCPTT 终端（UE）身份，回答“是哪台设备？” 不能从内层 Contact 取这个 UE 身份，也不能把业务正文里的访问令牌当作设备标识。[§7.3.1(a)，印刷页 153](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=154)；[§8.1A，印刷页 161](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=162)。

| MCPTT 服务器用哪条请求办授权？ | 用哪份注册记录，绑定哪些身份？ |
|---|---|
| **REGISTER**：服务器实际收到第三方 REGISTER；内嵌客户端 REGISTER 的 MCPTT 业务信息正文含 `mcptt-access-token` 和 `mcptt-client-id`。普通 IMS 注册本身不够。 | 查**眼前这份**第三方 REGISTER。第 2a 项查出并行授权已满就停止，不到第 5 项。走到第 5 项，内层头为 `Resource-Share: supported` 时，须把 **MCPTT ID 和 MCPTT 客户端 ID** 绑定到外层 Contact 参数所标识的 UE。第 4、4a 项写有“授权成功”，第 5 项没有另列这个条件；也不能据此认定授权失败后已经绑定。[§7.3.2，入口及第 1–5 项，印刷页 155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=156)。 |
| **授权兼设置的 PUBLISH**：服务器实际收到 `Event: poc-settings`、设置正文和含上述两个授权字段的 MCPTT 业务信息正文，且本次业务授权成功。 | 从**这次 PUBLISH 的 P-Asserted-Identity** 取得 IMS 公共用户身份，找出**含该 IMS 公共用户身份的第三方 REGISTER**。第 5c 项查这份 REGISTER 内层的 `Resource-Share: supported`，用它外层 Contact 的 `+g.3gpp.registration-token` 取 UE 身份；条件满足，须把 **MCPTT ID** 绑定到该 UE。第 5a 项另把 MCPTT ID 和客户端 ID 绑定到 IMS 公共用户身份；第 5c 项没有把客户端 ID 列为与 UE 绑定的对象。不能拿 PUBLISH 自身的头或正文代替这份 REGISTER。[§7.3.3，入口及第 1–6 项，印刷页 156](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=157)。 |

同一用户在另一台设备也获授权，不能把这份 UE 绑定移作那台设备的许可。要确认服务器实际建立了哪一条绑定，需核对上述请求和相应的服务端绑定记录；单凭 `supported`、授权三元组或 200，不能认定已经共用承载。有了绑定也不等于预建立会话已经成功：若后来 PF 实际收到[建立预建立会话的 INVITE](../calls/preestablished-session-lifecycle.md)，且 SIP 核心网支持资源共享，还要把该 INVITE 的 `Feature-Caps` 参数所标识的 UE 与用户绑定的 UE 对上。[§8.2.2，第 4–5 项，印刷页 163](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=164)。这些条款没有规定多份同一 IMS 公共身份的注册记录如何择一，也没有给出令牌生成、异常值处理、绑定有效期或撤销规则。

## CSK 密钥更新：为什么服务器另发 MESSAGE，客户端何时替换？

**先看参与功能实际收到了什么。** 参与 MCPTT 功能（PF）在办理业务授权的 REGISTER 或 PUBLISH 中收到客户端与服务器密钥（CSK），而且机密性保护已启用，才由 PF 决定是否更新。服务配置的 `confidentiality-protection` 为 `true` 或缺失时启用，为 `false` 时关闭；只有完整性保护不满足这一条件。这不是每次请求都要轮换，也不把“已获业务授权”或 REGISTER/PUBLISH 的 200 当成本段的触发条件。[TS 24.379 V16.14.0，§6.6.2.3.1，印刷页 140](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=141)；[§7.3.7，下载入口，印刷页 159](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=160)。

**如果决定更新，PF 须另发 SIP MESSAGE。** Request-URI 用**第三方 REGISTER 的 To** 中收到的 URI，不能改用授权 PUBLISH 的目的 PF PSI 或普通 Contact。MESSAGE 的 `Accept-Contact` 和 `P-Asserted-Service` 带 MCPTT ICSI（`urn:urn-7:3gpp-service.ims.icsi.mcptt`）；前者按条文使用 `g.3gpp.icsi-ref` 并带 `require`、`explicit`。 `application/mikey` 正文带 CSK-ID 和封装在 MIKEY 中的加密 CSK。这份 MESSAGE 不是原授权请求或它的响应。[TS 24.379 §7.3.7，第 1–6 项，印刷页 159](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=160)。

**终端须实际收到并核验。** 收到带 MCPTT ICSI 的 `P-Asserted-Service` 和 `application/mikey` 的 MESSAGE，且 MIKEY 的 `CSB-ID` 内密钥标识最高 4 位的值为 2，才按本条处理 CSK 下载。发起者标识 `IDRi` 是 URI，就与当前服务 PF 的 PSI 比对；匹配后把 URI 转成 UID。若 `IDRi` 是 UID，就将当前服务 PF 的 PSI 转成 UID，再与收到的 UID 比对。终端用相应 UID 验签。条文所列身份不匹配或 `I_MESSAGE` 认证失败时，回 SIP **488**，Warning 文本是 `136 authentication of the MIKEY-SAKKE I_MESSAGE failed`，并停止。136 在 Warning 文本内；不要把 INVITE 的外层 399 套给这个 MESSAGE，也不要为不符合下载入口的消息补写拒绝码。只有成功提取 CSK 和 CSK-ID，才替换终端为**这个 PF**保存的原一对值。[TS 24.379 §7.2.5，印刷页 152–153](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=153)；[§4.4.1，INVITE 的 Warning 语境，印刷页 33](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=34)；[表 4.4.2-2，第 136 项，印刷页 37](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=38)。

**只发布设置时，用适用的现有 CSK，不是再下载一次。** 受保护的[只发布 MCPTT 设置](../calls/settings-publication.md)使用双方已可用的相应 CSK/CSK-ID 处理 XML；不能由这笔 PUBLISH 判定服务器发过下载、终端换过密钥或业务重新获准。排查更新时，应把 PF 实际收到授权请求的记录、发出的独立 MESSAGE、客户端的核验和替换记录分开看。这里没有规定成功回 200、重试、服务端切换时序或其他终端同步。[TS 24.379 §6.6.2.2，适用密钥，印刷页 139](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=140)；[§7.2.3，只发布设置，印刷页 151](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=152)；[§7.3.1A，设置 PUBLISH 接收侧，印刷页 154–155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=155)。

如果要辨认同值 URI 在不同业务中代表谁，见[跨业务用户身份映射](cross-service-user-mapping.md)。若甲已在平板上获得 **MCVideo 业务授权**，又从手机申请该业务，见[MCVideo 多终端业务授权](../mcvideo/multiple-device-authorization.md)：服务器收到手机的新申请后要处理它，并在给该用户的响应中说明另一台终端已获准（该页依据 TS 23.281 V16.4.0 §7.13，印刷页 161）。若平板上只有 SIP 注册成功的记录，或手机是甲第一次申请该业务，这条“另一台终端已经获准”的提示都不能仅凭现有记录要求；平板已获准也不能替手机确认本次结果。若问如何读取或订阅同一 MCPTT 用户其他客户端的应答设置，见[服务设置观察](../calls/settings-observation.md)。本页不判断 LMS 是否需要独立注册，也不以 MCPTT 的注册或授权推定位置配置的下发时机。

若这次排查是同一客户端掉注册、重启或恢复出厂，查[客户端 ID 何时保留及怎样核对归属](mcptt-client-id-lifecycle.md)。
