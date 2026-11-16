# MCData owner 状态回流：独立订阅、匹配确认与缺席条件

限 serving 为一个 served 用户观察一个 handled 组 owner 的 per-group affiliation；本版不支持一个此类 SUBSCRIBE 观察多个 served 用户。

这段观察不同于客户端到 serving 的 per-user/per-client 观察，也不同于 group dynamic 订阅。收到的 PIDF 必须符合相应过程和 §8.4.1，并按用户、客户端、组及本地期限匹配。

## 独立观察事务

适用条件：serving 要确定该用户是否已在组 owner 成功归属。

serving 另向该组关联的 CF 发送 SUBSCRIBE，在 mcdata-info 中分别放组 ID 和 served 用户 ID，使用以该用户 ID 限制的 per-user simple-filter。当前及后续状态用 Expires=4294967295，仅取当前用 0，并接受 PIDF；对话内续订/退订仍有各自 Expires 规则。owner 入口要求过滤器用户与 mcdata-calling-user-id 一致；随后检查期限、组是否存在以及 handled 用户是否为成员，通过后回 SUBSCRIBE200 并在订阅期间通知变化。PUBLISH 准入与这段订阅是不同事务，前者没有替代后者。

- owner 对 Expires 缺失或非零过短返回 423/Min-Expires=4294967295；组不存在或非成员分别 403 并停止。
- §8.3.3.4 是明确的 per-user filter，与 group dynamic 所用 per-group filter 的未闭合编码不混同。
- 原文要求为发现成功状态建立此观察，但所核 §8.3.2.6/.7 没有规定必须先等该 SUBSCRIBE200 才能发送 owner PUBLISH；不补时序锁或自动订阅触发算法。

依据：§8.3.2.7 initial/in-dialog SUBSCRIBE;8.3.3.4;8.4.2.2 per-user syntax，印刷页 170、171、181、182、188、189。

## 正向状态确认

适用条件：owner NOTIFY 的 per-group PIDF 包含 served 用户的 tuple.id、相应 affiliation.client 及 affiliation.expires；serving 本地存在同一用户、客户端和 handled 组的未到期 affiliating 条目。

满足这些条件时，serving 将该本地条目置为 affiliated，并把 next publishing time 设为当前时刻与通知中归属到期时刻之间的中点。owner 的 §8.3.3.5 明确要求在 affiliation 中给出 expires；这一状态通知参与确认，不能把 owner PUBLISH200 直接替换成同样的状态转移。

- 本地未到期与通知里有 expires 是分别列出的条件，不能只看到用户/客户端名字就更新任意条目。
- 正向确认分支没有额外要求 p-id 匹配，也没有在此明确把本地 expiration time 改成收到的 expires；不从其他分支补这些赋值/条件。
- 这一分支只规定原状态 affiliating，不给已经 affiliated 的刷新通知补相同更新算法。next publishing time 记录不等于已完成下一次刷新或保证续期成功。

依据：§8.3.2.7 NOTIFY step1;8.3.3.5 step3a，印刷页 171、182。

## 缺席的状态条件

适用条件：owner 通知没有该 served 用户及 served 客户端的匹配 tuple/affiliation.client 结构；serving 的相应 handled 组本地条目仍未到期。

本地条目为 affiliated 或 deaffiliating 时，§8.3.2.7 step2 要求转为 deaffiliated，并把本地期限设为当前时刻。若条目仍在 affiliating，step3 另要求通知有 p-id，且等于该条目的 affiliating p-id，才对同样的缺席作上述处理。因此“owner 没列出这个客户端”不是一条不分状态的通用拒绝规则；仍等待首次确认的条目尤其不能跳过请求关联条件。

- 这两个缺席分支均受用户、客户端、handled 组及本地未到期约束，不影响其他用户或组的任意记录。
- deaffiliated 是 serving 本地状态，随后客户端可见信息还受 per-user 通知过滤；不要求发出 schema 未列的 deaffiliated wire 状态。
- p-id 不匹配或缺失时不满足 step3；本批不为这类仍在等待的条目补超时拒绝或重试结论。

依据：§8.3.2.7 NOTIFY steps2,3，印刷页 171、172。

## 两跳p-id的关联边界

适用条件：需要把客户端触发的归属请求与 owner 通知中的缺席结果关联起来。

客户端 PUBLISH 接入后，§8.3.2.3 step14a(i)(B) 和 step14a(iii)(D) 的相应分支要求 serving 将其 p-id 写入重新 affiliating 或新建的组条目。向 owner 发 PUBLISH 时，§8.3.2.6 另生成全局唯一 current p-id，并写入发出的 PIDF；只有未到期 affiliating 条目的 affiliating p-id 尚未设置，才把 current p-id 填入该本地字段。owner 在由 PUBLISH 触发且已识别 p-id 的通知中回填这一 owner 跳的值，而 serving 的 affiliating 缺席分支又要求它与本地 affiliating p-id 相等。两跳如何完整映射不能由字段同名推得，不能擅自把已设的客户端 p-id 覆盖掉来消除差异。

- 这是具体关联缺口，不代表每个正向 owner 通知均不能使用；正向确认按前一 claim 的独立条件处理。
- 没有读取或推定实现私有映射，不把“通常应该相同”写成标准已经定义。
- 不把 owner 的 p-id 自动一路复制成客户端收到的 p-id；serving 到客户端的关联填入条件另见 §8.3.2.5。

依据：§8.3.2.3 steps14a(i)(B),14a(iii)(D);8.3.2.6 steps7,9,10;8.3.3.3 step12;8.3.3.5 step3b;8.3.2.7 NOTIFY step3，印刷页 165、166、169、172、181、182。

## 证据边界

- 正向和缺席分支分别可核验，但两跳 p-id 映射以及完整重试/续期调度仍有边界，不能称作已验证的完整状态机。

## 按需继续

- [explicit-affiliation-lifecycle-results](explicit-affiliation-lifecycle-results.md)
- [group-dynamic-observation](group-dynamic-observation.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§8.3.3.3 step10 versus steps2,11：零selected expiration分支删除MCData ID等于served MCData ID的用户记录，前面识别和非零处理使用handled MCData ID。 不把变量静默统一，不将零值分支表述为已验证的精确删除目标。

§8.3.2.3 step14;8.3.2.6 steps7,9,10;8.3.2.7 NOTIFY step3：客户端接入已可能设置affiliating p-id，owner跳新建current p-id时仅在字段未设才写本地值，缺席确认却要求相等。 单独标出跨跳关联缺口，不自造覆盖或映射算法。

§8.3.2.6 steps4,5,10;8.3.3.3 steps10,11：owner请求按该用户所有有效客户端聚合，撤销却使用Expires0；零值owner处理是用户记录级删除，且有served/handled变量差异。 不推断多客户端部分撤销一定只影响单个客户端，也不补按剩余客户端数切换请求类型的策略。

§8.3.2.7 NOTIFY step1：正向确认设置affiliated及next publishing time，未明确用收到的expires覆盖本地expiration time；已affiliated的刷新通知也不满足该分支初态。 保留实际赋值范围，不补完整每轮续期状态机。

§8.2.2 NOTE1;8.3.2.3 opening5,steps9,10,18：客户端零期限可省PIDF与serving入口仍必需PIDF的差异由上一批保留。 本批从已满足相应入口的服务器过程起算，不绕过该限制或宣称端到端零body撤销已闭合。

§8.3.2.3 steps14a(ii),15;8.3.2.7;8.4.1.2 table8.4.1.2-1：部分serving生成分支写de-affiliating，通知处理和schema写deaffiliating。 不新增wire状态，不静默修成经过实现验证的一致状态机。
