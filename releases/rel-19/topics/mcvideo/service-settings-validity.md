# MCVideo设置有效性：刷新、观察、退出与通话准入

TS24.281 V19.3.0 第7章的普通在网 MCVideo 客户端与服务该用户的 PF/server；第10章仅作普通 on-demand、带 transmission control、直接单用户私呼的准入衔接。排除 partner migration、MCVideo gateway UE 接入、跨系统 gateway、别名/FTA、远程/ambient、优先通信及其例外。

每条 claim 只继承本主题 common_conditions 和自身 conditions。SIP 注册、用户认证、MCVideo 服务授权、CSK 可用、service settings 成功传达、某次呼叫获准及媒体发送/接收许可是不同结果。

外部 TS24.229、TS24.482、TS24.484、TS29.283、TS33.180 及 RFC/XML 算法只按明确调用定位依赖；不以别的服务、版本或既有高层概要补造本版报文、错误码、回滚和寿命。

## 设置报文及有效期

适用条件：客户端按 §7.2.3 设置、更新或刷新服务设置，或按 §7.2.2 同时授权和发布；移除动作另按 Expires=0 claim。

PUBLISH 的 Request-URI 是 serving PF 的 PSI，P-Preferred-Service 为 MCVideo ICSI，Event=poc-settings。非移除操作的 Expires 设4294967295。poc-settings 提交当前 auto-answer/manual-answer、selected-user-profile-index 以及 multiplex-support；settings-only 的 mcvideo-info 则含目标 mcvideo-request-uri 和 client-id，按配置成对加密，并按完整性配置保护两种XML body。设置计时器针对匹配 Instance Identifier URN 的 client settings，更新时也更新 user settings 计时器；这不证明 token 或身份绑定同样有效到该 Expires。

- 7.4.1.2.2 把 multiplex-support 的语法基数列为0或1，而发送过程要求包含该元素；不能用 schema 可选性抹去调用者要求。此处只列配置值含义，不重写全部 RFC4354 XML。
- settings-only 请求没有在该段以新 access token 重新授权；不是 token refresh grant。token、SIP注册、设置、绑定及CSK的寿命分别判断。
- 客户端收到 settings-only PUBLISH200 时 MAY 告知用户设置已成功传达，不是 SHALL 报所有业务已可用。

依据：§7.2.1A;7.2.2 steps6–7;7.2.3;7.4.1.2.2，印刷页 153、154、155、165、166。

## settings-only 的既有绑定要求

适用条件：服务器收到 settings-only PUBLISH：Event=poc-settings、poc-settings body、mcvideo-info 内含 mcvideo-request-uri/client-id；进入 §7.3.4。

服务器先从 P-Asserted-Identity 识别 IMS identity，再执行7.3.1A；该处理不成功则403/Warning140并停止。随后验证目标 MCVideo ID 与 IMS public user identity 的绑定：不存在或已过期则404并停止；存在且未过期时，profile 尚未缓存才下载。继续的 RFC3903 处理不成功也不再执行后续步骤；成功才缓存设置到期、发送200。settings-only 不能使已经失效的服务授权绑定自行复活。

- 原文 step1 用 PAI，step4 却写 Request-URI 中的 IMS public user identity；客户端7.2.1A又把 Request-URI 设为PF PSI。保留字段冲突，不提供替规范选字段的实现结论。
- settings-only 的成对机密字段为 request-uri/client-id：两者均加密须都解密成功，只一个加密判失败，均明文则直接识别。不是授权PUBLISH的token/client-id pair。
- 本段没有给绑定有效期计算方法或把它等同 access token exp；也未将404加上发起私呼所用Warning141。

依据：§7.3.4 steps1–9;7.3.1A settings-only branch;7.2.1A，印刷页 153、154、159、162、163。

## 200之后的能力与profile处理

适用条件：服务器的授权 PUBLISH 或 settings-only PUBLISH 已完成此前所有步骤，进入 §7.3.3 或 §7.3.4 的200后设置/profile处理。

服务器使用 am-settings 作为该 client 的当前 Answer-Mode。multiplex-support 存在且true表示支持媒体控制通道与媒体流复用，缺失或false表示不支持；这是支持指示，服务器据其决定何时何处使用，不等于每次呼叫必复用。selected-user-profile-index 存在时识别该active profile，未缓存则下载所需profile；缺index且有多个profile时选含Pre-selected-indication者，仅一个则默认该项。若 profile 的 OnNetwork/ImplicitAffiliations 含至少一个组ID entry，则须调用8.2.2.2.15。

- settings-only 的7.3.4 step5已在200之前要求对未缓存的profile下载；step11又列下载与选择。这里保持两处调用，不把所有profile下载都说成发生在200之后。
- profile下载失败、预选标记缺失/重复、条件归属建立失败的完整处理未在本条定义。200先发不证明上述后续动作已经成功。
- 本页只确认隐式归属调用入口，不把service-authorized直接等同affiliated，更不等同有权建立任意组呼或发送媒体。

依据：§7.3.3 steps10–13;7.3.4 steps10–13，印刷页 161、162、163。

## 显式退出与清理边界

适用条件：客户端要求移除服务设置并按7.2.1A把PUBLISH Expires设0；服务器收到 Event=poc-settings、Expires=0，并成功按RFC3903处理。

该操作使MCVideo client退出服务。服务器从PAI识别IMS public user identity，成功处理后移除MCVideo service settings；原文NOTE说明包含移除 all group affiliations；随后移除MCVideo ID与public user identity的绑定，再发200。若UE上其他MC服务仍应保持注册，7.1另要求重新注册时去掉MCVideo/对应ICSI标签而保留其他服务参数，不是注销整个共享注册。

- all group affiliations、多client并存、设置按Instance Identifier计时之间未在此给出完整清理选择算法；不删掉原文all，也不扩成用户所有设备/所有服务绑定全部删除。
- 自然设置到期、token到期、SUBSCRIBE Expires=0不是这个显式PUBLISH移除事件，不能一律套全部清理动作。
- 本段不明写CSK清除、已建立呼叫逐段BYE或服务端回滚；密钥使用终点沿security/signalling-key-update的独立33.180来源，不能把材料仍在等同继续有效。

依据：§7.2.1A;7.3.5;7.1，印刷页 151、152、153、154、163。

## 同用户设置观察

适用条件：client要查看同一MCVideo用户另一client的设置，或验证自己当前设置；服务器收取按7.2.4/7.3.6.1构造的poc-settings SUBSCRIBE。

初始SUBSCRIBE寻址serving O-PF PSI，XML目标为该MCVideo ID，P-Preferred-Service为MCVideo ICSI，Accept含poc-settings MIME。仅取当前状态用Expires=0，当前及后续通知用4294967295；对话内取消订阅才是退订的0。服务器从PAI绑定识别originating ID并与served ID比较，不同则403停止；相同按RFC处理回200，并在订阅期间通知设置变化。收到含poc-settings的NOTIFY后，client按entity id分别缓存各client的Answer-Mode和active profile index，而不是将全部设备合成一份设置。

- 服务端入口还要求Request-URI指向该PF、mcvideo-request-uri为served ID、P-Asserted-Service含MCVideo ICSI及Event=poc-settings；不以收到任意NOTIFY推定来源/授权通过。
- 这是设置观察，不重新建立授权绑定、不给发送媒体许可；SUBSCRIBE200也不等于客户端已收到并应用后续NOTIFY。
- 服务器7.3.6.2明确通知Answer-Mode和profile；本条没有把multiplex-support自动补为NOTIFY必带项。未展开RFC订阅到期、失败和全量/增量处理。

依据：§7.2.4;7.3.6.1/.6.2，印刷页 155、156、163、164。

## 设置与实际私呼准入

适用条件：实际进入普通on-demand、带TC、单一直接ID私呼的O-PF或T-PF入口；此前用户可能已注册、服务授权或更新设置。不是用本claim概括所有组呼/重入/priority入口。

发起私呼O-PF仍从PAI的public user identity确定calling MCVideo ID并授权；绑定找不到或已过期即404/Warning141并停止。终接私呼T-PF在还未收到被叫client的Answer-Mode设置时回480/Warning146；随后按XML目标ID查public user identity绑定，缺绑定回404。两侧通过这些检查后还各有本次私呼权限、目标、媒体和客户端应答条件，不能用注册成功、CSK可用或PUBLISH200替代。

- 终接本段仅明写无绑定404，没有复述发起侧expired/Warning141；不把两侧错误码和寿命判断强行统一。
- T-PF尚未收到Answer-Mode不是所有情况下“服务未授权”的同义词；没有规定可凭缺设置自动选Auto。完整自动/手动和force-auto分支仍见既有private-call-server-admission。
- 这里仅建立授权/设置到呼叫入口的使用链；私呼获准和SIP会话建立之后的TC许可另见已有媒体主题，不重复状态机。

依据：§10.2.2.3.1.1 steps3–4,10;10.2.2.3.2 steps3–6，印刷页 332、333、341。

## 证据边界

- 普通本系统路径。外部认证、配置schema完整性、MIKEY算法、partner migration、gateway UE、全SIP事务和当前call强制结束未闭合；settings订阅仅有界观察链。

## 按需继续

- [service-authorization](service-authorization.md)
- [private-call-server-admission](private-call-server-admission.md)
- [csk-key-update](csk-key-update.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。
