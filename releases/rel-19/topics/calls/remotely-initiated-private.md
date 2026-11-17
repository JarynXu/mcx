# 远程请求私呼：谁发起、拨给谁、结果回给谁

固定 TS24.379 V19.4.0，主系统在网 MCPTT 远程请求另一用户发起普通按需私呼；A 为请求者、B 为被要求起呼者、C 为该私呼被叫，允许 A=C。

请求与结果 MESSAGE 的 PF/CF 转送按各自接收事件适用，不将权限成功、消息送达或私呼成功作为共同前提。

排除组呼、ambient listening、跨系统/网关、紧急、功能别名、预建立会话与 ric 优先级/接续模式覆盖；不扩展被调用私呼全部实现。

## 请求谁起呼，与起呼后拨给谁

适用条件：请求用户 A 要求远端用户 B 发起私呼给指定用户 C；三种角色不要求是三个不同身份。

§11.1.7.1 区分 requesting（A）、remote（B）和 identified（C）。A 的客户端先检查 allow-request-remote-init-private-call，缺失或 false 时 SHOULD 提示无权，并 SHALL 停止。本页其余请求字段适用于通过该检查的分支：生成 SIP MESSAGE，mcptt-called-party-id=C，request-type=remotely-initiated-private-call-request，resource-lists 内列 B；notify-remote-user 按 A 要求设 true 或 false。Request-URI 是服务 A 的 PF PSI，不是 B 或 C 的 MCPTT ID。P-Preferred-Service 和 Accept-Contact 的 g.3gpp.icsi-ref 携 MCPTT ICSI，后者另带 require、explicit，然后发送。

依据：§11.1.7.1; §11.1.7.2.1 steps1-3。

不把 B 当本次控制 MESSAGE 的最终私呼被叫，也不把 A 自动当作后续私呼主叫。

可选优先级与 ric-commencement-mode 未在本主题请求范围启用；不由许可发控制请求推导 C 已接受通话。完整 XML/SIP 模板及配置文档验证不在本页。

## 发起 PF 核身份与请求许可，结果消息不套请求许可

适用条件：PF 收到远程私呼 request 或 response 类型的 MESSAGE；各拒绝分支按事件和字段条件分别适用。

发起 PF 可因资源不足或拥塞风险返回 500，可附 Retry-After。它从 P-Asserted-Identity 的公共身份取得发送者 MCPTT ID；绑定不存在或过期则返回 404+Warning141 并停止。只有 request-type 为 remotely-initiated-private-call-request 且请求者 allow-request-remote-init-private-call 缺失或 false 时，才返回 403+Warning158。通过后向该服务的 CF PSI 发送 MESSAGE，复制 mcptt-info 与 resource-lists，并将已确定的发送者 ID 写入 mcptt-calling-user-id。结果 MESSAGE 回程发送者为 B，不能强制沿用 A 的身份或把请求许可拒绝条件无差别套给 response-type。

依据：§11.1.7.3.1 steps1-14 and response paragraphs; §11.1.7.2.2 completion steps2-4 (return-sender comparison)。

§11.1.7.3.1 的 2xx 段写响应于 step13 发送的 MESSAGE，但发送实际列在 step14；保留此回指差异，不静默修改。该段要求生成 200 转给客户端，4xx/5xx/6xx 转发错误，均不等于私呼发起成功。

服务 CF PSI 的确定方法在本条 NOTE5 明列超出规范范围。本页只限主系统，不扩展 partner/gateway 路由。

## CF 按控制消息收件人转送，不按私呼被叫转送

适用条件：CF 收到远程私呼请求或结果 MESSAGE；终接 PF 随后按其实际收件身份处理。

CF 可因资源或拥塞风险以 500 拒绝；Accept-Contact 缺 MCPTT ICSI 时以 403 拒绝。缺 resource-lists 正文，或全部 list 中 entry 多于一个时，返回 403+Warning145 并停止。可转送分支复制正文，将资源列表中的用户 ID 写入 mcptt-request-uri，Request-URI 则设为服务该用户的终接 PF PSI。请求方向列表用户是 B，结果方向是 A；mcptt-called-party-id 仍描述 C。终接 PF 从正文 mcptt-request-uri 查公共身份绑定，缺失返回 404；可因资源/拥塞风险返回 500。通过后调用 §6.3.2.2.11 生成 MESSAGE，以该终接用户的公共身份为 Request-URI，按 §6.3.2.2.9 复制正文，并发送。

依据：§11.1.7.4 steps1-12 and response paragraphs; §11.1.7.3.2 steps1-6 and response paragraphs; §6.3.2.2.11; §6.3.2.2.9; §11.1.7.2.1 step2(d-f); §11.1.7.2.2 completion steps2(d-e),3-4。

CF 的拒绝条件写缺正文或多于一个 entry，不据此自行增加空列表的相同拒绝分支；本文可转送路径按有效单个收件 ID 讨论。

终接 PF §11.1.7.3.2 step5 将 P-Asserted-Service 写在 outgoing SIP INVITE，但 step4/6 是 MESSAGE。此方法名差异未修复，不能将本页当完整无歧义报文模板。

终接 PF 转发 2xx 或 4xx/5xx/6xx 给 CF；CF 对下游 2xx 生成 200 给发起 PF、错误则转发。这些是 MESSAGE 事务结果，不是 C 已接听或媒体已到达。

## 远端实际收到请求后，调用按需私呼发起过程

适用条件：B 实际收到远程私呼请求 MESSAGE，且本地策略选择 on-demand；本主题不启用 ric 优先级或 commencement 覆盖字段。

B 从 mcptt-called-party-id 提取 C，按 §11.1.7.2.2 step3 调用 §11.1.1.2.1.1 发起对 C 的私呼。notify-remote-user=true 时 MAY 提示 B 收到请求；false 时 SHALL 不提示收到该请求，且收到该 INVITE 的 180 或 183 时不提示起呼进度。是否完成发起须等待所调用私呼过程的结果，不能在收到控制 MESSAGE 时宣布成功。

依据：§11.1.7.2.2 steps1-3; §11.1.7.2.2 step4 (comparison only: excluded pre-established branch); §11.1.7.2.2 completion paragraph and steps1-2。

此页核的是 §11.1.7 对普通私呼的实际调用契约，不声称重新核完 §11.1.1.2.1.1 所有 SIP、SDP、鉴权及媒体步骤。通知开关不是用户已读、接受或拒绝的证据。

本地策略选预建立且已有预建立会话才走 step4；本页不把按需分支当预建立不可用时的自动回退，也不将两条件共同施加给所有角色。

step3 对 ric-app-level-priority 及 ric-commencement-mode 的响应是 MAY 携带相应请求头，不将可选覆盖变成保证优先权或强制接通。本页不展开这些覆盖。

## 结果回到请求者，但“请求者就是成功被叫”无需另发

适用条件：B 已完成所调用的私呼发起过程；或 A 实际收到控制 MESSAGE 错误响应或结果 MESSAGE。各分支分别适用。

若 C 的 MCPTT ID 等于收到请求正文的 mcptt-calling-user-id，且私呼发起成功，B SHALL 跳过结果发送的剩余步骤：此时 A 就是成功私呼的被叫，原文 NOTE 说明其已知结果。否则 B 生成新的 MESSAGE，resource-lists 列原请求的 mcptt-calling-user-id（A），mcptt-called-party-id 仍为 C，response-type=remotely-initiated-private-call-response，remotely-initiated-call-outcome 依发起成功与否设 success 或 fail；Request-URI 为服务 B 的 PF PSI，再走上述转送。A 收到结果 MESSAGE 后按 outcome 判断成功/失败，SHOULD 提示用户。A 收到原控制请求的 4xx/5xx/6xx 时 SHOULD 提示请求失败且不继续余下步骤。

依据：§11.1.7.2.2 completion paragraph,steps1-4,NOTE; §11.1.7.2.1 response paragraphs; §11.1.7.3.1 step3 (comparison only: request-only permission guard); §11.1.7.4 steps7-9 (return-routing dependency)。

C=A 但发起失败仍不满足跳过条件；C≠A 即使发起成功仍发结果 MESSAGE。不得把“未见结果 MESSAGE”一律判为失败。

success 表示被调用私呼发起过程成功，不额外证明媒体可听、话权获得、用户已读或持续在线。原 MESSAGE 的 200 与这份新 MESSAGE 的 outcome 分开判断。

本页不补超时、重试、关联标识、去重和未列出错误分支的算法。

## 阅读边界与导航

此页是远程控制请求、调用及结果的读者路径，不是从控制 MESSAGE 到媒体接通的完整实现证明。原文 PF 步骤回指和 outgoing INVITE 方法名差异保留。

[普通私呼控制与结果](control-routing-results.md)与[被叫接续](private-client-acceptance.md)解释被调用链的其他责任，不据此省略远程请求分支的条件。

来源：[TS24.379 V19.4.0 官方原文](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
