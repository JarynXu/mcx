# 普通预安排组呼准入：成员、归属与发起权限分别检查

在网 MCPTT；普通、GMS 管理且未重组的组；收到指向该组控制功能的初始 INVITE。

该组没有已分配且 active 的组会话；本主题研究新建，不是加入进行中会话。

非 TGI、非任何基于预配置组的重组；非远程发起；不含 emergency-ind 或 imminentperil-ind，不触发优先呼叫例外。

本链终点是准入检查与受邀成员选择，不宣称已经接通、已获话权或所有成员已答复。

## 控制功能的媒体及服务标识检查

适用条件：控制功能开始处理该 INVITE。

资源不足/拥塞时 MAY 500（MAY Retry-After）；媒体参数不可接受或未提供 MCPTT speech codec 时 488 并停止；Accept-Contact 缺 g.3gpp.mcptt 或缺正确 MCPTT ICSI 的 g.3gpp.icsi-ref 时 403 并停止。

依据：§10.1.1.4.2 steps 1–3。

## 组文档初处理与普通组成员检查

适用条件：组 ID 对应 GMS 组文档。

先按 6.3.5.2 获取/处理组文档：未订阅则订阅 xcap-diff；订阅返回 404 对应 404 + 113，其他 4xx/5xx/6xx 对应原最终响应 + 114。普通未重组组若含 on-network-disabled 则 403 + 115；成员列表无主叫 MCPTT ID 则 403 + 116；on-network-invite-members=false 而请求为 prearranged 则 404 + 118。preconfigured-group-use-only=true 另由父过程拒绝为 403 + 167。

依据：§6.3.5.2 steps 1–5; 10.1.1.4.2 step 5(a–a1,c)。

## 本次客户端的归属与用户记录期限

适用条件：控制功能执行 6.3.6；在本普通新呼叫分支检查主叫归属。

按组 ID 找 group entry，再按主叫 MCPTT ID 找 user entry，再确认该 user entry 的客户端列表含本次 mcptt-client-id，且该 user entry 的 expiration time 尚未到达；任一不满足均判定本客户端未归属。普通新呼叫未归属时 403 + 120 并停止。

依据：§6.3.6 steps 1–5; 9.2.2.3.2; 10.1.1.4.2 step 14(a)。

## 发起权限不能由成员身份替代

适用条件：同一普通组新建呼叫；前序归属等检查未拒绝。

成员身份不足以授权发起：组文档需有主叫 entry，且存在适用于 is-list-member 或匹配主叫 identity 的 rule，其 actions/allow-initiate-conference=true；supported-services 必须存在，含 MCPTT ICSI service 及 MCPTT speech group-media。未满足这些发起条件时 403 + 119 并停止。

依据：§6.3.5.4 controlling-function branch steps 2–4; 10.1.1.4.2 step 14(b)。

## 准入后的邀请选择与归属门槛

适用条件：新建组会话的前序检查通过，进入 10.1.1.4.2 step 14(g)。

6.3.5.5 仅选择已归属成员；归属人数低于 on-network-minimum-number-of-affiliated-members，或任何标记 on-network-affiliation-to-group-required 的成员未归属，均以 480 + 112 停止，不继续发出邀请。只有归属门槛等前序检查通过后才继续邀请；成员数超过 on-network-max-participant-count 时，只邀请该上限数量，并优先含 on-network-required 的成员；其余选择策略未规定。

依据：§6.3.5.5; 10.1.1.4.2 step 14(g)(i,v)。

## 证据边界

- §6.3.5.5 的人数上限未给缺字段默认值，不推断为无限人数。规范假设 GMS 已验证上限不低于 required 用户数；其余邀请选择策略在范围外，未给违反此假设的服务器补救算法。

- on-network-disabled 的条件是元素存在，不自行增补 =true。组文档订阅本身链接已有 server-subscription/subscription-proxy，不在此复述。
- 任何已发送的组文档初处理 4xx/5xx/6xx 使父过程停止；已有缓存可以进入初处理，并非每次都重新下载。
- 到期时间属于组下的 user information entry，不把它改为客户端单独的有效期，也不与 O-PF 身份绑定有效期混淆。
- 主控与 O-PF 的归属判定不是同一算法：9.2.2.2.11 按 user→client→group 查找，affiliating/affiliated 视为已归属，deaffiliating/deaffiliated 视为未归属；该条正文没有重复 expiration 检查。本主题不以此覆盖主控 6.3.6。
- 14(a) 特殊优先/远程/重组条件含复合 and/or；这里只采用全部特殊分支排除后的普通情形，不能按简化式生成所有场景代码。
- 不得替换成 join-handling；加入已有组会话使用 6.3.5.3 和 10.1.1.4.2 step 15(b)，不在本新建主题展开。
- 普通组规则不得套用到 TGI 或重组的主控/非主控职责分配。
- on-network-affiliation-to-group-required 是归属前提；on-network-required 是需确认的成员。不能合并两标志。
- 6.3.5.5 的 max 比较原文写 number of members，不能擅自改成全部在线终端或所有已接听成员。
- TNG1、所需答复数量、P-Answer-State/缓冲媒体、最终 200/失败释放另成后续主题；这里通过准入不保证最终成功。
- 未完成整套组呼建立；仅有界发起、准入与邀请选择入口，后续答复/接听、TNG1/TNG3、媒体/话权/安全协商不是本稿覆盖。
- 未展开 9.2.1/9.2.2 全套显式或隐式 affiliation 注册、刷新、撤销；只验证消费其记录的判定入口和存储层次。
- TS24.484 配置的生成/合法性、TS24.229 与 RFC SIP 实现依赖未独立展开。
- 未由普通组流程推导跨系统重组、广播、远程发起或紧急呼叫的完整成功/失败状态机。

## 按需继续

- [加入已有会话的授权](join-authorization.md)

- [prearranged-origination](prearranged-origination.md)
- [../calls/group-acknowledged-start](../calls/group-acknowledged-start.md)
- [../calls/group-release-timers](../calls/group-release-timers.md)
- [../security/group-key-membership](../security/group-key-membership.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页159、160、161、162、163、164、228、293、294、295、296、297；仅本版本。

- [受邀侧服务设置、寻址与身份绑定](../calls/group-terminating-addressing.md)

- [本客户端如何请求及刷新归属](explicit-affiliation-publish.md)

- [implicit-affiliation-eligibility](implicit-affiliation-eligibility.md)
