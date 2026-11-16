# MCData 隐式归属边界：普通发送、请求型提交与退出不能混用

限TS24.282 V19.7.0。普通业务对比只覆盖非紧急、非重组的组standalone SDS控制面、HTTP FD组文件分发及已核两客户端IPCONN，不泛化到全部业务分支。

§8.3.2.12–.14和§8.3.3.6/.7是被其他过程调用的helper，只有相应请求确实要求并触发隐式归属时才适用；其存在本身不构成普通请求的自动入组许可。

## 普通业务不自动入组

适用条件：普通组请求的其他前置检查未阻断，CF执行组归属门槛；或评估是否能把同一组入场模型套到IPCONN。

普通组standalone SDS控制面在 §9.2.2.4.2 step6j 检查主叫归属；HTTP FD 的 group-fd、FD SIGNALLING PAYLOAD 分支在 §10.2.4.4.2 step12g 做同类检查。主叫未按§6.3.5归属时，两处均规定403/Warning120并停止，不是在这里自动调用隐式归属再继续发送。§8.1及本次核到的§16.2.2.1请求型调用另有紧急告警范围，不能移植为普通发送规则。IPCONN第20章描述两客户端在网通信，也不能借“MCData服务”名称补成组隐式入场。

- 只取普通组适用的SDS条件，不修订step6j的重组混列条件或重复编号。HTTP FD这里也不是FD HTTP TERMINATION分支。
- 未完整审查紧急告警业务；引用其调用只为证明入口范围不同，不给普通请求增加486或紧急例外。
- IPCONN的版本兼容、身份及媒体证据复用既有页，不把这里的范围结论扩为所有将来版本或所有IP承载。

依据：§8.1;9.2.2.4.2 step6j;10.2.4.4.2 steps12,12g;16.2.2.1 steps3,4;20.1，印刷页 157、158、204、283、284、383、443。

## 请求型helper的条件接口

适用条件：某已确认调用入口收到的SIP请求确实要求对发送客户端做隐式归属，因而调用§8.3.2.12；只有相关owner入口要求资格检查/状态建立时才调用§8.3.3.6/.7。

请求型PF helper从mcdata-client-id识别客户端，从mcdata-request-uri识别组，从P-Asserted-Identity公共身份经绑定确定用户。它复制该客户端旧列表，为缺失或已过期的目标组新增affiliating条目，执行跨客户端不同有效组的N2计数/策略缩减；若目标组因N2不能加入，须丢弃整个候选并停止，否则才替换该客户端列表。owner资格helper另外检查GMS中组存在、handled用户为成员、且owner本地已有该组信息项；通过只是eligible。真正调用owner状态建立helper后，才按组→用户记录加入尚未存在的客户端ID，按本地策略设期限并调用owner通知。

- owner从mcdata-request-uri取组、mcdata-calling-user-id取handled用户；不要将PF收到的PAI用户绑定与owner看到的calling-user字段混同。
- 本条只是条件接口，不说明所有普通请求都会调用它，也不为helper未列的资格失败自造SIP响应。
- §8.3.2.12同样使用未在本条赋值的candidate expiration interval，并存在复制已过期旧条目再新增的唯一性问题；不凭显式流程补值或去重。
- owner本地组条目存在与GMS中组存在是两项条件；eligible不等于本地状态已创建，更不等于业务已成功。

依据：§8.3.2.12;8.3.3.6;8.3.3.7，印刷页 175、176、177、182、183。

## 提交和取消不可混用

适用条件：SIP请求实际触发过§8.3.2.12，并收到该请求的CF结果，或PF决定拒绝这一个请求。

§8.3.2.13只在PF收到CF对该触发请求的2xx时，将由§8.3.2.12新增的组条目置为affiliated，并调用§8.3.2.5通知。§8.3.2.14在PF决定拒绝该触发请求，或收到CF的4xx/5xx/6xx时，只删除由§8.3.2.12新增、且匹配请求用户/客户端/目标组的条目。这与配置链走§8.3.2.6时，owner PUBLISH的3xx–6xx或timer F到期会清理同一用户各客户端下handled组记录不同；不能因为都叫隐式归属就统一成一种“回滚”。

- 请求型取消helper没有列3xx或timer F，也没有要求恢复所有被N2策略影响的旧记录；不补完整快照恢复。
- §8.3.2.14只规定PF本地新增条目的删除，本条未证明owner已同步撤销。
- 2xx条件属于触发§8.3.2.12的请求，不能套到任意设置200、显式PUBLISH200或每条SDS成功响应；归属确认也不证明数据已读或文件取得。

依据：§8.3.2.13;8.3.2.14;8.3.2.6 failure paragraph;8.3.2.15 step11，印刷页 169、170、177、179。

## profile漏项与服务退出

适用条件：配置组列表变化，或客户端准备通过poc-settings Expires0退出MCData服务。

§8.3.2.15对旧组列表先复制，再按条件增补配置组；没有配置组或没有新增时会提前停止。因此从profile删除一个组ID，不能仅凭这个过程判定对应归属已经撤销。真正的poc-settings Expires0退出另按§7.3.5：RFC3903处理成功后移除service settings，原文说明包含全部group affiliations，再移除MCData ID与公共用户身份的绑定并回200。它不是归属presence PUBLISH的同一个零值入口，也不是取消状态订阅。

- 退出的all group affiliations与多客户端绑定之间缺少完整清理选择算法，沿用service-settings-validity已列限制；不扩成全设备全部绑定删除，也不削成只影响某一组。
- 不把profile漏项、token到期或settings自然到期自动替换为§7.3.5全部清理动作。
- 本条不证明既有SDS/FD/IPCONN通信已完成释放；归属/授权清理和通信终止的消息及证据需分别核验。

依据：§8.3.2.15 steps4,8;7.3.5;8.2.2 step4;8.2.3 in-dialog SUBSCRIBE，印刷页 148、149、159、160、177、178。

## 证据边界

- 请求型helper仅作明确条件下的对比，不构成普通业务调用证明；完整紧急业务及owner取消过程未展开。

## 按需继续

- [sds-group-controller-admission](sds-group-controller-admission.md)
- [fd-size-admission](fd-size-admission.md)
- [service-settings-validity](service-settings-validity.md)
- [ipconn-target-and-admission](ipconn-target-and-admission.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文边界

§8.3.2.15 step8b(iii);8.3.2.12 step7b(iii)：两段均用candidate expiration interval设置新增条目期限，但各自未在本条赋值。 记录算式与未定义输入，不从显式发布、settingsExpires或owner本地策略移植默认期限。

§8.3.2.2;8.3.2.15 step8a/b;8.3.2.12 step7a/b：记录要求同一列表组ID唯一；候选过程却先复制所有旧条目，再为已过期同组新增，未明确清除过期副本。 不自行去重、覆盖或删除，不能称候选表算法已通过实现验证。

§8.1 versus7.3.2;8.3.2.15 opening：概述把REGISTER列为配置隐式归属触发，但7.3.2实际步骤未列与PUBLISH相同的显式调用。 本批以7.3.3/.4明确调用为主，不给每个REGISTER成功补一段自动执行序列。

§7.3.4 step12;8.3.2.15 opening,steps1,2：settings-only调用该过程，过程身份提取却仍按服务授权请求描述。 保留既有授权有效前提，不编造上下文切换或重新授权行为。

§8.3.2.15 steps8b,11;8.3.2.6 steps7,9,10;8.3.2.7 NOTIFY step3：配置新增分支只列状态/期限赋值，未写客户端p-id；owner发送过程对未过期affiliating且affiliating p-id未设的条目赋current p-id，已设则不覆盖。 未设条件满足者可获得owner跳关联值；既有条目已设时仍按实际值检查缺席关联。不将显式两跳冲突无条件推广到新配置条目，也不补所有新增的初始化默认值或完整续期闭环。

- [请求型 helper 在紧急告警中有明确调用，业务结果才决定本地完成或取消。](emergency-alert-admission-and-results.md)
