# MCPTT 服务设置观察：同用户多客户端的查询与通知

固定 TS24.379 V19.4.0，主系统在网 MCPTT 客户端观察同一用户的本端或其他客户端当前服务设置。这里负责 SUBSCRIBE/NOTIFY 观察，不负责 PUBLISH 设置修改、服务授权或撤销。

客户端请求、服务器拒绝/接受、变化通知及接收缓存按各自事件适用，不以订阅已被接受或已收到设置为全页前提。

RFC4354（2006，Informational）作为实际调用的外部事件包/格式依赖，不是 Rel19 规范；不展开完整外部 SIP 事件状态机或通话/媒体许可。

## 先区分一次读取、持续观察与退订

适用事件：客户端要核实自身当前设置，或发现同一 MCPTT 用户另一客户端的设置；首次请求与既有订阅内操作分别适用。

客户端 SHALL 生成 initial SUBSCRIBE：Request-URI 为服务该用户的 originating PF PSI，mcptt-info 正文的 mcptt-request-uri 为该用户的 MCPTT ID；P-Preferred-Service 携 MCPTT ICSI，Event=poc-settings，Accept 包含 application/poc-settings+xml。只取当前状态时 Expires=0；需要当前状态及以后通知时 Expires=4294967295。重订和退订 SHALL 使用 in-dialog SUBSCRIBE，仍携上述 Event 与 Accept；继续观察设 4294967295，退订设 0。

规范强度：上述 MCPTT 请求构造、时长选择及对话内操作 SHALL；RFC 默认仅比较，不另造 MCPTT 可选字段。

- RFC4354 的通用默认时长为 3600 秒，SUBSCRIBE 通常无正文且 Request-URI 标用户；MCPTT 本入口明确正文目标、PF 地址、Accept 和上述 Expires 值，不用 RFC 通用默认替换这些要求。请求值不证明服务器实际承诺永久订阅。
- SUBSCRIBE 的 Expires=0 在 initial 请求表示只取当前状态，在既有订阅表示退订；不得当作 PUBLISH Expires=0 删除服务设置、归属和绑定。
- 本主题不展开 SIP 事件对话全部重试、协商有效期、错误恢复及退订完成响应细节。

依据：TS24.379 V19.4.0 §7.2.4 initial and in-dialog SUBSCRIBE paragraphs、§7.3.5 (PUBLISH removal comparison)，印刷页 181,182,189；RFC4354（外部依赖） §5.3、§5.4、§5.5 (generic defaults comparison)，印刷页 7。

## 服务器核对发起用户与被查询用户

适用事件：服务器收到符合 §7.3.6.1 所列 PF Request-URI、已服务 MCPTT ID 正文、MCPTT P-Asserted-Service 与 poc-settings Event 的 SUBSCRIBE。

服务器 SHALL 从 mcptt-request-uri 识别被服务 MCPTT ID，并在所述 PF Request-URI 条件下从 P-Asserted-Identity 的公共身份识别 originating MCPTT ID。两者不同，SHALL 返回 403 并停止；进入可继续分支后 SHALL 生成 SUBSCRIBE 的 200。在订阅持续期间，服务器 SHALL 按 §7.3.6.2 通知被订阅用户的设置变化。该入口允许同用户的多客户端观察，不是任意用户的设置查询授权。

规范强度：身份提取、不同用户的 403/停止、可继续分支的 200 及订阅期内变化通知均为 SHALL；RFC 认证及授权要求为 MUST/MUST NOT。

- RFC4354 还要求认证订阅及仅向有授权的订阅者发送内容；本页不把两个 ID 相等说成无需认证，也不把其通用授权机制扩为 MCPTT 任意第三方可查。
- 本条没有为 PAI 无法映射、目标未被服务或其他入口字段缺失指定统一错误响应，不从 PUBLISH 的 404/Warning141 分支移植。
- SUBSCRIBE 200 是订阅请求的响应，不包含本页要缓存的实际设置值，也不证明某客户端已接受通话或媒体可达。

依据：TS24.379 V19.4.0 §7.2.4 opening、§7.3.6.1 full，印刷页 181,189,190；RFC4354（外部依赖） §5.6、§5.6.1、§5.6.2，印刷页 8。

## NOTIFY 携每客户端设置，不重新授权或修改 profile

适用事件：服务器要通知已订阅用户的某客户端设置变化；或客户端实际收到带 poc-settings 正文的 NOTIFY。两角色按各自事件处理。

服务器 SHALL 构造 application/poc-settings+xml：am-settings 表示该客户端当前 Answer-Mode，selected-user-profile-index 标识其 active user profile，然后发送 NOTIFY。接收客户端 SHALL 按 entity 的 id 逐客户端缓存 am-settings 和 selected-user-profile-index，作为该客户端的当前应答模式及 active profile。§7.4.1.2.2 的 MCPTT 扩展正文含一个或多个 entity，各含一个 selected-user-profile-index，其 user-profile-index 为非负整数；multiplex-support 为零或一个可选元素。RFC4354 的 entity id 区分同一用户地址记录下的发布实体；am-settings/answer-mode 的 XML 值为 automatic 或 manual。

规范强度：MCPTT 正文构造、发送和实际收到正文后的逐客户端缓存 SHALL；字段数量和类型按本版语法，RFC 术语用于被调用格式定义。

- RFC4354 通用文档允许零 entity；MCPTT 扩展语法列一个或多个。不能用通用空文档直接推断该 MCPTT 客户端所有设置已删除。
- TS 发布步骤以 auto-answer/manual-answer 描述当前模式，而 RFC XML 定义及 TS 示例使用 automatic/manual。本页区分程序术语与 XML 字面值，不把它们无说明地替换成完整报文模板。
- §7.2.4 的接收缓存动作明确列两项，不据 multiplex-support 的可选语法自动增加第三项强制缓存，也不把缺失当作订阅失败。
- 观察到 active profile 的索引不是下载 profile 正文、改变配置、重新授权或证明全部设备当前在线。RFC4354 §5.11 的通用跨终端设置描述不替代 MCPTT 按客户端 id 分别缓存的明确要求。

依据：TS24.379 V19.4.0 §7.2.4 NOTIFY receipt paragraph、§7.3.6.2 full、§7.4.1.2.1、§7.4.1.2.2 syntax and schema (example comparison)、§7.2.2 step6(a) (value wording comparison)，印刷页 180,182,190,191,192；RFC4354（外部依赖） §5.16、§6 entity/id and am-settings definitions，印刷页 11,12,13；RFC4354（外部依赖） §5.11 (generic cross-terminal state comparison)，印刷页 10。

## 无正文通知不抹掉已知文档

适用事件：订阅者在同一对话内处理 NOTIFY 文档顺序；各客户端缓存仍遵守 MCPTT 的实际带正文接收条件。

RFC4354 §5.8 将同一对话中最高 CSeq 的 NOTIFY 所带文档作为当前文档；若该 NOTIFY 没有文档，使用次高 CSeq 中存在的文档。这个事件包规则解释了为何“收到通知”不等于收到新设置，不能把无正文通知当空设置覆盖。MCPTT §7.2.4 的具体缓存入口仍要求收到 application/poc-settings+xml 正文，再按客户端 id 读取其两项设置。

规范强度：RFC §5.8 给出当前文档选择规则；MCPTT 实际带正文的缓存 SHALL。本文不新增清空、超时或全局排序的强制动作。

- 没有正文与有正文但零 entity 是不同情况；不自创两者的同一清空算法。RFC 的组合策略范围外说明也不授权本页定义跨客户端冲突胜出或增量合并规则。
- 此规则限定同一对话，不按全局 CSeq 给不同订阅排序。本文不推断通知丢失后的自动恢复、缓存 TTL 或无响应即设备离线。
- MCPTT 的变化通知构造要求与 RFC 通用可无正文通知分别按其实际入口读；不得用 RFC 的 MAY 消去 §7.3.6.2 的正文要求。

依据：TS24.379 V19.4.0 §7.2.4 NOTIFY receipt paragraph、§7.3.6.2，印刷页 182,190；RFC4354（外部依赖） §5.7、§5.8、§5.16 (composition boundary)、§6 zero-entity distinction，印刷页 8,9,11,12。

## 相关入口

- [mcptt-publish-service-authorization](mcptt-publish-service-authorization.md)
- [profile-selection](profile-selection.md)
- [../calls/commencement-selection](../calls/commencement-selection.md)

外部事件包与格式：[RFC4354](https://www.rfc-editor.org/rfc/rfc4354.html)。
