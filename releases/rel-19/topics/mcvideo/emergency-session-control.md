# CF 的紧急状态更新：独立授权、告警分流与 TNG2

## 适用范围

- TS24.281 V19.3.0（2026-01）的在网、本地预安排 MCVideo 组；排除广播、chat、重组/NCF、跨系统、功能别名、应用请求优先级、地理触发、临时组和 imminent peril 操作。每条 claim 独立继承本主题 common_conditions，并叠加自身 conditions，不继承前条成功。
- 发起用户已经取得服务授权，调用身份可由现有绑定识别，且已归属于目标组；不在本页展开隐式归属或 N2 超限处理。目标接收用户的绑定是否存在，仍按对应 claim 检查。预安排只限定组类型，不代表已处于 emergency 状态；具体状态由每条条件指定。
- 用户 MCVideo emergency state、告警状态 MVEA、客户端所见组 emergency 状态 MVEG、客户端紧急组呼状态 MVEGC 和 CF 的 in-progress emergency state 是不同对象。不能用一项已置位替代其它项。
- 本文 info MIME 指 application/vnd.3gpp.mcvideo-info+xml；MCVideo ICSI 为 urn:urn-7:3gpp-service.ims.icsi.mcvideo；PSI 指 public service identity。保留本版错引，不把正文流程意图等同于已无歧义闭合的互操作实现。
- CF 收到以现有 on-demand 预安排 MCVideo session identity 为目标的 re-INVITE；请求含 emergency-ind，不带 imminentperil-ind，组当前无 imminent-peril 状态。只处理本用户发起及本人取消，不带 originated-by。
- 所列正文描述 CF 的操作和条件；授权、校验、re-INVITE、通知、INFO 的调用编号存在多处错引，实际 helper 仅按其自身正文独立注明，不把勘误猜测视为规范结论。媒体仅记录向 TS24.581 的交接，不新推 emergency TC 算法。

## CF 的独立权限检查

适用条件：CF 在 9.2.1.4.7 接收含 emergency-ind 的会话更新；执行该条前置校验与授权。

CF 可因资源不足/拥塞风险用500拒绝，可带 Retry-After，emergency=true 可选择接受。实际 6.3.3.1.16 校验中，emergency=true 要求不含 imminentperil-ind 且包含 alert-ind；emergency=false 要求不含 imminentperil-ind、alert-ind可有可无，无效组合403/Warning150。实际 .12.2 的紧急组呼授权要求用户 allow-emergency-group-call=true，且 DedicatedGroup 包含目标组或 UseCurrentlySelectedGroup，并均要求组 allow-MCVideo-emergency-call=true。未授权紧急呼叫按主条403；实际拒绝 helper .13 填 emergency-ind=false 和 alert-ind=false。若收到紧急值的 Resource-Priority、却无 emergency indication 且组 in-progress emergency=false，主条另要求403。

- 主条分别把校验/授权/拒绝引到 .17/.13.2/.14；实际正文为 .16/.12.2/.13。此处并列核验，不静默替换主条引用。
- 本主题正常入口本已含 emergency-ind；最后一项是主条另列的异常报文限制，不能把“没有 indication”泛化成“indication=false”。
- emergency=true 的 alert-ind 必须存在，但可为false；通话权限与告警权限独立。本页不把此 INVITE/re-INVITE 验证规则自动施加于所有独立 MESSAGE。

依据：§9.2.1.4.7 steps1–5;6.3.3.1.12.2;6.3.3.1.13;6.3.3.1.16，印刷页 110、111、114、115、116、236、237。

## 状态更新与其他参与者通知

适用条件：CF 已通过前置条件，收到 emergency-ind=true 且获准的紧急组呼请求；组当前无 imminent-peril 状态。

CF 缓存发起紧急呼叫的 MCVideo ID；若同时收到 alert-ind=true 且告警获准，再独立缓存告警发起者。若组已处于 in-progress emergency=true，则为每个其他 affiliated member 发送 emergency-ind=true 的 MESSAGE；若组原为false，则先设为true、启动TNG2，再向其他通话 participants 生成并发送紧急 re-INVITE。收到下游 re-INVITE 的200后与 TS24.581 媒体面交互。

- 已是true的分支在所列步骤没有要求重启 TNG2，不能自行刷新计时器。false→true分支也没有在同一主步骤再列对所有非参与 affiliated 用户的 MESSAGE，不从取消分支反向补齐。
- 主条 TNG2 到期引 .16，实际到期为 .15；紧急 re-INVITE 引 .6，但 .6 标题/正文是发送初始 INVITE，实际 .5 才是紧急 re-INVITE helper。保留该关键报文类型错引。
- 主条仍保留“timers need to be defined”的编辑注；本页另按已存在的6.3.3.5.2记录配置时长与交互，而非宣称编辑注已消失。

依据：§9.2.1.4.7 step6;6.3.3.1.5–6;6.3.3.1.15，印刷页 104、105、115、237、238。

## 取消通话状态与清理告警分开处理

适用条件：CF 收到 emergency-ind=false 的 re-INVITE；本用户取消自己的紧急呼叫，未带 originated-by。实际取消授权按 .12.4 的用户 allow-cancel-group-emergency 真/假判断。

未获准取消时返回403且 info 带 emergency-ind=true；若所收请求还带 alert-ind=false 且该用户有 outstanding alert，再带 alert-ind=true，发送后停止。获准取消且组当前 in-progress emergency=true 时，CF 先清组 emergency 状态及该用户 outstanding emergency group call 缓存。仅当请求还带 alert-ind=false、告警取消也获准且该用户存在 outstanding alert 时，才清本人 alert 缓存。随后向其他通话 participants 发送取消 re-INVITE，下游200触发媒体交互；停止TNG2。对 affiliated 但未参与通话的成员另发 emergency-ind=false 的 MESSAGE；只有前述告警也确实取消时在该通知增加 alert-ind=false。

- 本条只限制所列清除缓存分支，不排除其它程序处理告警。取消通话授权与 allow-cancel-emergency-alert 各自独立；原文组取消权限对缺失字段没有本页可用的默认值。
- step7 引 .13.4，step8 却引 .16 来判取消许可；实际为 .12.4。告警许可引 .13.3，实际 .12.3；向参与者生成 re-INVITE 又引 .6，NOTE3则写 .5。所有差别保留。
- 如果组本已false，主条step8的状态/通知/stop分支不成立；本页不推导重复取消的全部幂等结果。取消不是 BYE 或全组释放。

依据：§9.2.1.4.7 steps7–8;6.3.3.1.12.3–.12.4，印刷页 111、112、238、239。

## 通话成功响应与告警拒绝结果

适用条件：CF 执行 9.2.1.4.7 的成功响应段，紧急呼叫升级或取消本身没有被前置规则拒绝；所请求的告警发起或取消可能另被拒绝。

该段生成200并加入 SDP answer、Supported 的 norefersub/tdialog。若收到 alert-ind=true 但告警未获准，或 alert-ind=false 但告警取消未获准，须在200带 Warning149（SIP INFO request pending）。在成功响应步骤中，CF 先与媒体面交互，再发200；收到针对这个带149的200之 ACK 后，主条调用后续 INFO 过程。实际 INFO helper .17 指定 Info-Package=g.3gpp.mcvideo-info：告警发起被拒时发 emergency-ind=true/alert-ind=false，告警取消被拒时发 alert-ind=true，并在相应对话发给请求客户端。

- 成功段前还有“收到 re-INVITE200 后与媒体面交互”的独立句，后续编号成功段的整体触发关系及是否等待所有参与者并未清楚界定；不补全员成功门槛，也不把这句删掉后声称200可无条件立即发送。
- 主条 ACK 后调用 .18，实际 .18 是读取 Resource-Priority 值、.17 才是 INFO；保留错引。因此本条说明主条的149/ACK意图与实际INFO字段，不宣称引用链无歧义。
- 200 可以伴随告警部分拒绝，不证明两个请求都成功；同样没有证明视频发送/接收许可已经改变。

依据：§9.2.1.4.7 success/ACK paragraphs;6.3.3.1.17，印刷页 116、239、240。

## TNG2 到期后的状态与计时

适用条件：控制功能启动/取消/到期处理预安排紧急组呼的 TNG2；相应条件逐一成立时执行 6.3.3.5.2 和实际到期 helper .15。

启动 TNG2 时不得启动 TNG3。若 TNG3 正运行而通话升级，须停止TNG3，以服务配置 on-network/emergency-call/group-time-limit 启动TNG2。TNG2正运行而紧急组呼取消时，停止TNG2，并以组文档 on-network-maximum-duration 启动TNG3；TNG2到期时也用该值启动TNG3，这些条件同样适用于重启。TNG2到期 helper先把组 in-progress emergency=false；若会话仍 ongoing，向各 participant 发送 .9 定义的取消 re-INVITE（normal Resource-Priority、emergency=false）。对 affiliated 非 participant 另发 emergency=false 的 MESSAGE；下游 re-INVITE200 后与媒体面交互。

- TNG2到期不是本条定义的 BYE，也没有明确清除所有用户 emergency state 或 outstanding alert 缓存。TNG3按配置值重新启动，不是续跑升级前剩余值。
- 主条 9.2.1.4.7 将到期处理错引到 .16；实际 .15 与6.3.3.5.2分别核过。TNG2具体时长、默认/配置缺失处理及完整24.484/24.481配置约束未核，不填固定秒数。
- 当组会话已经不存在时，.15仍先清组状态，并保留通知非参与 affiliated成员的步骤；不从“ongoing时发re-INVITE”的条件删除其它步骤。本页也未补全媒体优先级转换。

依据：§6.3.3.5.2;6.3.3.1.15;6.3.3.1.9，印刷页 108、115、128。

## 证据边界

- 源文可以支撑各角色请求、权限、状态改变和成功/告警拒绝分流，但 helper 错引和成功段触发歧义使可运行完整实现尚未闭合。
- 只记录本用户 re-INVITE 路径；独立 MESSAGE 同时取消告警和通话的复杂权限交集、第三方取消、紧急初建/迟入、广播/chat优先级、媒体抢占和密钥处理未核。

## 按需继续

- [紧急告警 MESSAGE：权限、组内通知与接收确认](emergency-alert-message.md)
- [已有预安排会话升级或取消：客户端与两侧 PF 的处理](emergency-session-client-path.md)
- [MCVideo全组释放：五项策略、TNG3和公共BYE边界](group-release-policy.md)
- [MCVideo设置有效性：刷新、观察、退出与通话准入](service-settings-validity.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。
