# 同用户多客户端的服务设置：读取、观察与停止观察

## 适用条件

- 固定 TS24.379 V16.14.0 的在网 MCPTT 服务设置观察。范围是客户端与服务用户的 PF，观察本客户端或同一用户其他客户端；服务器身份不匹配的拒绝也在范围内，不预设身份核对成功。
- 初始读取、持续订阅、in-dialog 重新订阅/退订、PF 接收、发送 NOTIFY 和客户端收到 NOTIFY 是分别适用的事件；不要求它们同时发生，不把 200、缓存更新或 PUBLISH 成功设为全页前提。
- 本页只承担设置观察及必要的删除比较，不承担完整 SIP 注册、服务授权、设置发布、跨设备配置修改或呼叫建立。TS24.229、RFC6665/4354/3903 作为被调用接口，完整外部处理不由本页替代。

## 初始读取与持续观察使用不同的请求寿命

适用事件：客户端要查看同一 MCPTT 用户另一客户端的服务设置，或核对本客户端当前设置；本条处理初始 SUBSCRIBE 的构造，不预设服务器身份核对或订阅处理已成功。

客户端须按 §7.2.4 生成 initial SIP SUBSCRIBE。Request-URI 为服务该用户的 originating PF 的公共服务身份，application/vnd.3gpp.mcptt-info+xml 正文的 mcptt-request-uri 为该用户 MCPTT ID；二者不可互换。请求须带 P-Preferred-Service 中的 MCPTT ICSI、Event=poc-settings，以及 Accept=application/poc-settings+xml。只取当前状态时，Expires 须为 0；要当前状态及后续通知时，Expires 须为 4294967295。

规范强度：初始请求生成、所列身份/服务/事件/MIME 字段和依目的选择的 Expires 取值均为 SHALL。

### 边界

- 4294967295 是本条规定的请求取值，也是 NOTE 所述 Expires 的最大值；它不证明服务器授予永续订阅，也不替代寿命协商、刷新或失效恢复程序。
- §7.2.4 的设置发现用途是同一用户的客户端；不能据此提供读取其他用户设置的能力。服务器收到不相同身份时的拒绝仍在下一条范围内。
- F.1.3 说明 mcptt-request-uri 的 Normal/Encrypted 表示；目标 ID 的本业务含义来自 §7.2.4，不能套用 F.1.3 中私呼/组呼 session-type 的例子，给 SUBSCRIBE 添加私呼类型。

### 依据

- 3gpp-ts-24.379-v16.14.0：§7.2.4 initial SUBSCRIBE steps1–7 and NOTE1；§F.1.3 representation and session-type/request-uri comparison；印刷页 151, 152, 547, 548。

## PF 核对被观察用户与请求发起者，拒绝事件不依赖成功

适用事件：服务器收到同时满足 §7.3.6.1 入口的 SUBSCRIBE：Request-URI 为 served 用户的 PF PSI，mcptt-info 正文 mcptt-request-uri 标识该服务器服务的 MCPTT ID，P-Asserted-Service 带 MCPTT ICSI，且 Event 为 poc-settings。身份相同或不同是该入口内部的分支，不作为全条成功前提。

服务器须从正文确定 served MCPTT ID，并按该 PF PSI 条件从 P-Asserted-Identity 的公共用户身份确定 originating MCPTT ID。两者不同时须返回 403 并停止余下步骤；未由该身份差异分支停止时，按所引用 SIP/事件包程序生成 SUBSCRIBE 的 200 响应。订阅存续期间，服务器须按 §7.3.6.2 通知该用户服务设置的变化。

规范强度：身份识别、身份不同的 403 与停止、后续生成 200，以及订阅期间的变化通知为 SHALL。

### 边界

- 该比较不等于全部认证和授权已完成。§7.3.6.1 没有展开公共身份无法映射、绑定缺失/过期的处理或所有失败码；不能从私呼准入规则搬入默认拒绝算法。
- 客户端构造使用 P-Preferred-Service，服务器本入口检查 P-Asserted-Service；不能据客户端字段就宣称服务器入口条件自动满足。完整 SIP 核心处理仍依 TS24.229。
- §6.3.1.4 所列 SUBSCRIBE 分类针对 conference 和会话身份；poc-settings 在 §7.3.6.1 有自己的 PSI/正文/服务/事件条件，不能沿用 conference 的目标，也不能因通用列表未列出而判断不支持设置观察。原入口枚举有两个编号 3，此处按字段区分。
- SUBSCRIBE 的 200 是请求响应，不是含设置的 NOTIFY 已到客户端，更不是其缓存已更新。

### 依据

- 3gpp-ts-24.379-v16.14.0：§7.3.6.1 full；§7.3.6.2；§7.2.4 (request/receipt comparison)；§6.3.1.4 full (conference comparison)；印刷页 82, 83, 151, 152, 158, 159。

## 按客户端标识缓存实际通知，profile 扩展不等于发布新设置

适用事件：服务器需要通知订阅者有关被订阅用户客户端的设置变化，或客户端实际收到符合所引用 SIP/事件包程序且含 application/poc-settings+xml 正文的 NOTIFY；两者是角色不同的替代事件，不能以客户端已收到通知约束服务器发送。

服务器须生成含当前 answer mode 的 am-settings 和标识 active profile 的 selected-user-profile-index 的 poc-settings 正文，再按所引程序发送 NOTIFY。客户端实际收到上述 NOTIFY 后，须对每个由 id 属性标识的客户端，分别缓存 am-settings 为其当前应答模式，以及 selected-user-profile-index 为其 active MCPTT service user profile。§7.4.1.2.2 要求正文按 RFC4354 构造 poc-settings 根、一个或更多 entity，每个 entity 含一个 selected-user-profile-index；本版扩展 schema 内的 user-profile-index 类型为 nonNegativeInteger。

规范强度：服务器生成正文和客户端收到后缓存为 SHALL；服务器发送步骤按 §7.3.6.2 的程序指令执行；§7.4.1.2.2 给出结构和类型约束。

### 边界

- 缓存是在该客户端实际收到通知后的局部动作，不证明所有设备同步完成、下一次呼叫已经采用该值，也不将观察变成设置发布。§7.2.3 的 PUBLISH 才另列 set/update/remove/refresh 设置程序。
- 本版 §7.2.3 的设置文字使用 auto-answer/manual-answer，表7.4.1.2.2-3 示例使用 automatic/manual；此处不将说明文字当作完整 XML 枚举。answer-mode 事件包的完整定义依 RFC4354。
- 表7.4.1.2.2-1/2 指定 MCS 扩展命名空间及 qualified 元素；表3示例使用 PoC 默认命名空间，未显式展示 selected-user-profile-index 的扩展命名空间切换，client id 也字面写 urn:uuuid。示例不能直接当作已验证的可发送模板，不能静默修正后声称原文如此。
- 本页不规定跨通知文档的合并、缺字段删除、通知新旧排序或完整初次通知/重传/错误恢复。§7.2.4/7.3.6 调用外部事件包程序，不据本 TS 的局部说明断言外部规范也没有这些规则。

### 依据

- 3gpp-ts-24.379-v16.14.0：§7.2.4 NOTIFY receipt；§7.3.6.2 full；§7.4.1.1–7.4.1.2.2 including tables7.4.1.2.2-1/2/3；§7.2.3 full (publication and mode wording comparison)；印刷页 151, 152, 159, 160, 161。

## 三个 Expires=0 必须连同方法和 dialog 判断

适用事件：以下是替代事件：客户端重新订阅或停止既有设置订阅；客户端只取当前状态的初始 SUBSCRIBE（比较）；或服务器收到 Event=poc-settings 且 Expires=0 的 PUBLISH（删除比较）。PUBLISH 处理成功仅约束其删除分支，不约束 SUBSCRIBE 读取或退订。

重新订阅或退订时，客户端须生成 in-dialog SUBSCRIBE，带 Event=poc-settings 和 Accept=application/poc-settings+xml；要当前及后续通知时 Expires=4294967295，要退订时 Expires=0。这个 in-dialog 的 0 与初始 SUBSCRIBE 中“仅取当前”的 0 用途不同。PUBLISH 的 0 则是 §7.3.5 的另一个服务器入口：先从 P-Asserted-Identity 识别公共用户身份，按 RFC3903 处理；只有处理成功后才继续删除 service settings、删除 MCPTT ID 与公共用户身份之间的绑定，并发送 200。

规范强度：所列 in-dialog 构造、Expires 分支及 PUBLISH 的身份识别、处理成功后的删除与 200 为 SHALL；不得去掉成功守卫。

### 边界

- 停止观察不等于删除设置或撤销上述身份绑定；只读初始 SUBSCRIBE 的 0 也不等于取消已有的另一订阅。此处依据方法、dialog 及实际程序区分，不提供跨 dialog 管理算法。
- 本页没有展开完整 PUBLISH 生命周期。RFC3903 处理失败时不能据成功分支推删除或 200；具体失败响应、实体标签和发布恢复依外部程序。
- 按 §7.1，服务授权可使用 REGISTER 或 PUBLISH，并涉及实现选择及认证所得 access-token；设置读取或退订不能替代这些服务授权步骤。

### 依据

- 3gpp-ts-24.379-v16.14.0：§7.2.4 initial and in-dialog SUBSCRIBE；§7.3.5 full (PUBLISH deletion comparison)；§7.1 full (service-authorisation boundary)；§7.2.3 full (publication scope comparison)；印刷页 147, 148, 151, 152, 158。

## 共同接口与边界

- 保护处理须区分父层适用性。§6.6.1.1 将通用适用范围列为 9–12，并说明注册/服务授权的保护在 7；§7.2.3 明确给 PUBLISH 的保密和完整性步骤，不能将该请求构造整套搬成 §7.2.4 的 SUBSCRIBE 构造。§4.8 将 MCPTT ID/client ID 列为敏感数据，§6.6.3.1 列出 mcptt-info 和 poc-settings XML 的完整性保护接口；本页既不据 §7.2.4 未逐步重述而宣布免保护，也不补完整保护应用算法。
- F.1.3 的未加密字段使用 type=Normal 及相应 mcpttURI，已加密字段使用 type=Encrypted 和 EncryptedData 结构。§6.6 的相关配置/密钥接口须按适用程序处理；§6.6.2.2/6.6.3.2 假定所需密钥可用，本页不以同 ID 检查或 XML 格式证明密钥、认证和授权已完成。

- 3gpp-ts-24.379-v16.14.0：§7.1;7.2.3–4;7.3.5–6；§4.8 sensitive-data list and key/configuration interface；§6.6.1.1–4;6.6.2.2–3.2 (protection scope/interface only)；§6.6.3.1 MIME list;6.6.3.2–4 (protection interface only)；§F.1.3 representation；印刷页 45, 46, 138, 139, 140, 143, 145, 146, 147, 148, 151, 152, 158, 159, 547, 548。

## 相关主题

- [private-client-answer-evidence](private-client-answer-evidence.md)
- [private-server-admission-routing](private-server-admission-routing.md)
- [prearranged-client-establishment](prearranged-client-establishment.md)
- [explicit-affiliation-client](../groups/explicit-affiliation-client.md)
