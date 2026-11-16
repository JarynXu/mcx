# MCData 配置触发隐式归属：候选组、N2 与 owner 结果

限 TS24.282 V19.7.0 普通在网、服务授权已成功的 MCData 用户；§7.3.3 或 §7.3.4 的适用前置门槛未阻断，执行 active profile 后续处理。settings-only 不等于重新授权，现有绑定须满足其自身有效性条件。

serving 为服务该用户的 PF，owner 为目标组的控制功能。过程针对本次 served 用户和客户端，但 N2 计数与 owner 发送可能涉及该用户其他客户端。

配置元素及调用关系依据 TS24.282；profile schema、缺省值、下载失败处理和并发一致性算法尚未核验。

## 配置与授权入口

适用条件：相应 PUBLISH 授权/设置处理成功，active profile 中的 OnNetwork/ImplicitAffiliations 含一个或多个携组 ID 的 entry。

§7.3.3 和 §7.3.4 在设置200之后处理 active profile，再按这个配置条件调用 §8.3.2.15。该过程以已成功服务授权为前提，从服务授权请求识别 served 用户 ID，并从 mcdata-client-id 识别 served 客户端；profile 尚未缓存时按指定数据库过程取得。缺少 ImplicitAffiliations，或没有包含组 ID 的 entry，就停止余下归属步骤。因此设置200与配置入口成立都不是这些组已成功归属的证据。

- active profile 的索引/预选规则和绑定检查复用 service-settings-validity，不将调用视为绕过安全或授权检查。
- §8.1概述包括REGISTER触发，但§7.3.2正文没有逐步写出同样的§8.3.2.15调用；不补每个REGISTER成功必跑该过程的执行序列。
- §8.3.2.15身份来源写服务授权请求，而§7.3.4是settings-only调用；本页不发明重绑定或上下文选择算法来消除措辞差异。

依据：§7.3.3 steps7–12;7.3.4 steps7–12;8.3.2.15 opening,steps1–4，印刷页 147、148、177。

## 候选列表与无新增短路

适用条件：§8.3.2.15已定位served用户、served客户端及其原组列表。

serving 先把目标客户端的旧组条目复制到候选列表，再为配置表中原来没有记录、或记录已过期的组新增条目；新条目置为 affiliating，期限按当前时间加 candidate expiration interval 设置。若 step8b 未新增组条目，step8c 要求丢弃候选列表并停止，发生在 N2 检查和写回之前。这个过程不是把所有配置组无条件刷新或重置，也没有像显式完整兴趣 PUBLISH 那样，因某旧组未列在新配置表里就自动撤销它。

- 旧组先复制并不保证永远保留：随后若走到N2策略缩减，候选还可能改变。这里只说明配置漏项本身不是删除指令。
- 本条使用candidate expiration interval，却没有在§8.3.2.15内定义其取值；不擅自从设置Expires、token有效期或owner期限赋值。
- 先复制旧条目、再为已过期的同组新增，可能与§8.3.2.2组ID唯一记录要求冲突。原文未在这里明确删除旧副本或去重，不能自行修成已验证的更新算法。

依据：§8.3.2.15 steps5–8;8.3.2.2，印刷页 163、177、178。

## 跨客户端N2与本地提交

适用条件：有新增组条目，未在step8c停止，进入§8.3.2.15 step9。

N2候选数不是新配置entry数，也不是简单客户端条目数。serving 按候选列表及同一用户其他客户端列表，统计状态为 affiliating/affiliated且尚未到期的不同组 ID。超过该用户 N2 时，按服务提供者策略把候选组缩减到 N2；然后才用候选列表替换目标客户端保存的组列表。不能把profile列出的每个组都当成已获准保留，也不能把这一写回称为owner已经提交成功。

- 不决定哪些组被保留，不把N2解释成某个客户端的独立配额；未核策略如何处理并发或跨客户端约束。
- 本配置过程没有§8.3.2.12 step10那种“当前请求目标组因N2不能加入便丢整个候选”的分支，不从另一个helper补它。
- 写回对象是served客户端的列表；不能因计数读到其他客户端，就推导本步骤也批量重写了它们。

依据：§8.3.2.15 steps9,10，印刷页 178、179。

## owner请求与成功证据

适用条件：候选列表完成N2处理并已写回目标客户端，进入§8.3.2.15 step11。

serving 遍历配置表中的组，只要它在候选列表中仍有状态为 affiliating 的条目，就为该 served 用户和该组调用 §8.3.2.6；范围不只限本轮新加的条目。随后走既有 serving→owner PUBLISH：用户、客户端、组记录与owner成员检查各自成立，PUBLISH200不能直接把本地状态改成成功。§8.3.2.15 NOTE2 指向客户端 §8.2.3 订阅以获知成功归属的组，具体owner状态匹配沿用 §8.3.2.7，不套请求型helper的2xx完成规则。

- 这里的step11条件就是配置表成员且候选状态为affiliating，不额外加“仅新增”或在调用处补一项原文未列的期限筛选；§8.3.2.6构造body本身另有未到期条件。
- 该owner事务失败/超时按§8.3.2.6清理同一用户各客户端下的handled组条目，不能替换成§8.3.2.14仅删本次新增项的取消。
- owner200早于PIDF一致性检查及多客户端边界仍适用。p-id须另按实际条件判断：§8.3.2.15新增分支未写入客户端p-id；§8.3.2.6对未过期affiliating且affiliating p-id未设的条目填入本轮current p-id，字段已设则不覆盖。不能把显式两跳关联缺口无条件套到所有新配置条目，也不推定所有新增字段一定未设。

依据：§8.3.2.15 steps8b,11 and NOTE2;8.3.2.6;8.3.2.7 NOTIFY step1;8.3.3.3 steps4–8，印刷页 168、169、170、171、178、179、180。

## 证据边界

- 普通配置链已定位，但候选期限来源和过期同组副本处理尚未闭合，不能据本页生成完整实现。

## 按需继续

- [explicit-affiliation-owner-admission](explicit-affiliation-owner-admission.md)
- [explicit-affiliation-owner-state](explicit-affiliation-owner-state.md)
- [implicit-affiliation-entry-and-lifecycle-boundaries](implicit-affiliation-entry-and-lifecycle-boundaries.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文边界

§8.3.2.15 step8b(iii);8.3.2.12 step7b(iii)：两段均用candidate expiration interval设置新增条目期限，但各自未在本条赋值。 记录算式与未定义输入，不从显式发布、settingsExpires或owner本地策略移植默认期限。

§8.3.2.2;8.3.2.15 step8a/b;8.3.2.12 step7a/b：记录要求同一列表组ID唯一；候选过程却先复制所有旧条目，再为已过期同组新增，未明确清除过期副本。 不自行去重、覆盖或删除，不能称候选表算法已通过实现验证。

§8.1 versus7.3.2;8.3.2.15 opening：概述把REGISTER列为配置隐式归属触发，但7.3.2实际步骤未列与PUBLISH相同的显式调用。 本页以7.3.3/.4明确调用为主，不给每个REGISTER成功补一段自动执行序列。

§7.3.4 step12;8.3.2.15 opening,steps1,2：settings-only调用该过程，过程身份提取却仍按服务授权请求描述。 保留既有授权有效前提，不编造上下文切换或重新授权行为。

§8.3.2.15 steps8b,11;8.3.2.6 steps7,9,10;8.3.2.7 NOTIFY step3：配置新增分支只列状态/期限赋值，未写客户端p-id；owner发送过程对未过期affiliating且affiliating p-id未设的条目赋current p-id，已设则不覆盖。 未设条件满足者可获得owner跳关联值；既有条目已设时仍按实际值检查缺席关联。不将显式两跳冲突无条件推广到新配置条目，也不补所有新增的初始化默认值或完整续期闭环。
