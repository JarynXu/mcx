# 独立组紧急告警：MESSAGE 发起、分发与确认边界

TS24.379 V19.4.0，主系统在网 MCPTT 独立组紧急告警；目标为非 ad hoc 的既有组，当前没有正在进行的组通话，发起用户在 PF 和 CF 各自检查时均已归属目标组。

客户端用户 profile 的 EmergencyAlert 使用 DedicatedGroup。限定普通客户端/PF/CF，不含跨系统、网关、离网、地理围栏触发、隐式归属、告警取消或会话内紧急升级。各角色按自己的事件适用，不共同继承授权成功。

## 先查告警许可，再发送独立 MESSAGE

用户请求向指定组发送紧急告警。用户 profile 的 EmergencyAlert 采用 DedicatedGroup；客户端针对该组判断许可。未获准和获准是替代分支。

组文档 list-service/preconfigured-group-use-only=true 时，客户端 SHOULD 提示该组不允许告警，SHALL 停止。否则，DedicatedGroup 分支要求用户 allow-activate-emergency-alert=true 且 uri-entry 包含目标组；未满足视为未授权。获准后形成独立 SIP MESSAGE：P-Preferred-Service 和带 require、explicit 的 Accept-Contact 使用 MCPTT ICSI；mcptt-info+xml 中 mcptt-request-uri 取该 DedicatedGroup 的 uri-entry，alert-ind=true，mcptt-client-id 为本端 ID；加入 §6.2.9.1 要求的位置。客户端设置尚未设置的自身 emergency state，把 MEA 置 2（等待告警确认），Request-URI 则指向服务自身的 PF PSI，然后发送。正文目标组与 SIP Request-URI 不是同一个地址。

本页不构造完整 SIP/XML/位置编码，也不展开可选功能别名和用户请求的 application priority；它们不是本主题额外的成功前提。

§12.1.1.1 的 UseCurrentlySelectedGroup 构造只明确列没有当前组的回退，未在该分支列已有当前组的赋值；另有 EmergencyAlert 缺失构造分支，但授权 helper 又要求相应配置。本页不以常识修补两处范围，故只整理 DedicatedGroup 路径。

客户端 DedicatedGroup 授权条件未另列组 allow-MCPTT-emergency-alert；CF 仍独立检查该组权限。

来源：§12.1.1.1 opening,steps1-2,4(a)(i)(A),4(b,c),5-9；§6.2.8.1.6 initiation paragraph，印刷页 78, 537, 538；对照范围：§12.1.1.1 steps4(a)(i)(B),4(a)(ii)（仅比较已排除的选组分支）。

## PF 绑定检查不能由告警标记跳过

发起 PF 收到该客户端的告警 MESSAGE；发起者在本次 PF 检查时已归属目标组。响应段分别适用于 PF 收到本次转发请求的 2xx。

PF 可因资源不足或拥塞风险以 500 拒绝，并可携 Retry-After。继续时从 P-Asserted-Identity 的 public user identity 查询 MCPTT ID；没有绑定或绑定已过期，返回 404+Warning141 并停止。已归属路径取得目标组的 CF PSI，向该 PSI 发送新 MESSAGE，复制收到的 mcptt-info+xml，以查得的身份填写 mcptt-calling-user-id，并复制存在的位置正文；P-Asserted-Identity 改为自身 PF PSI。收到下游 2xx 时，生成带本 PF PSI 的上游 200 并发给客户端。

未归属路径的隐式归属、N2 上限和成功/失败收尾不属于本页；不能从本页推导未归属者必然可发告警。

PF PSI/CF PSI 的发现和完整事务转发保留规范外部依赖；可选功能别名转送还须核活动状态，不把简单复制理解为保留任意别名。

原文 2xx 响应段回指 step10，而发送列在 step12；保留该编号差异，不将其改写成规范修订。

来源：§12.1.2.1 steps1-3,5-12,2xx response paragraph，印刷页 544, 545, 546。

## CF 再授权，通知已归属成员并缓存告警

CF 收到 alert-ind=true 的独立告警 MESSAGE；目标组当前没有正在进行的通话，发起者在 CF 检查时已归属。前置拒绝、授权失败和成功各按自己的条件适用。

CF 可因资源或拥塞风险以 500 拒绝。Accept-Contact 缺 MCPTT ICSI 的 g.3gpp.icsi-ref 时返回 403；组 preconfigured-group-use-only=true 时返回 403+Warning168，均停止。DedicatedGroup 告警须同时满足用户 allow-activate-emergency-alert=true、uri-entry 包含目标组、组 allow-MCPTT-emergency-alert=true；未授权返回带 alert-ind=false 的 403。通过后，CF 向每个其他已归属成员生成并发送告警 MESSAGE：目的地为该成员的终接 PF PSI，正文标目标成员、告警所属组、发起用户、alert-ind=true 和发起用户的 mission critical organization，并复制存在的位置。随后生成 200、缓存该用户已发起告警的信息，再向请求方发送 200。

已归属不替代告警权限；本页不把客户端允许 DedicatedGroup 视为 CF 也已授权。

通知构造 helper 的概述指已归属但未参与者，而 §12.1.3.1 的调用者写其他已归属成员。本主题限定组无正在进行的通话，不把它延伸成有通话时的唯一分发裁决。

发送通知在缓存/上游 200 之前，但本段没有等待全体通知响应的屏障、失败聚合或事务回滚算法；缓存和 200 不能证明全员收到。

来源：§12.1.3.1 steps1-2A,4(a),4(b)(i-iv)；§6.3.3.1.13.1 group branch；§6.3.3.1.11；§6.3.3.1.12，印刷页 135, 136, 137, 547, 548。

## 接收提示与自身告警状态分开

终接 PF 收到面向成员的告警通知，或客户端实际收到相应告警通知且 alert-ind=true；两者分别按自己的事件处理。

终接 PF 可因资源或拥塞风险以 500 拒绝。它从正文 mcptt-request-uri 中的目标 MCPTT ID 查 public user identity 绑定；无绑定返回 404，有绑定则按 §6.3.2.2.11 生成并发送下行 MESSAGE。收到告警通知的客户端 SHOULD 显示告警及组 ID、发起用户 ID、发起者 mission critical organization，提供了功能别名时 MAY 显示别名；随后 SHALL 生成并发送 200。alert-ind=true 的这一接收分支没有把接收者自身 MEA 设成已发起告警的动作。

只证明实际收到通知的本端行为；界面显示是 SHOULD，不把信令 200 等同于用户已阅读。

§6.3.2.2.11 所调用的完整 MIME 复制/保护以及 SIP 事务机制未在此展开。接收独立告警也不是加入组呼或取得话权。

来源：§12.1.2.2 steps1-5；§6.3.2.2.11；§12.1.1.3 step1,steps7-8，印刷页 125, 126, 540, 542, 546。

## 原请求响应和独立接收指示不是全员回执

发起客户端收到本次告警 MESSAGE 的 2xx 或 4xx/5xx/6xx；或 CF 已完成本次授权告警分支并发送上游 200，继续生成独立接收指示。各事件不要求同时发生。

发起客户端收到原 MESSAGE 的 2xx 时将 MEA 设 3（告警已发起）；收到 4xx、5xx 或 6xx 时设 MEA=1（无告警），自身整体 emergency state 仍保持。CF 在上游 200 后另按 §6.3.3.1.20 向发起者生成接收指示 MESSAGE，带 alert-ind=true、alert-ind-rcvd=true，并回填原请求 mcptt-client-id。它表示 CF 成功接收告警，不是各成员的已读汇总。§12.1.1.1 的 MEA 成功转换明确由原请求 2xx 触发，不改写为必须等待该独立 MESSAGE。

告警成功不等于组呼已建立；后续自动发起紧急组呼只是 §12.1.1.1 NOTE4 的实现相关可能性。未规定的 3xx、超时、重传和响应乱序不补造状态规则。

独立接收指示的终接 PF 条款 §12.1.2.3 step2 从正文 mcptt-request-uri 取 MCPTT ID，step4(b) 却把 MCPTT ID 写为位于传入 Request-URI；入口的 Request-URI 又是 PF PSI。保留身份回指差异，不宣称这条独立指示的完整路由和客户端处理已经闭合。

不套用告警取消的 client-id 匹配和 MEA=4 规则来填发起成功路径；告警取消、组状态取消和通话释放是另外的业务。

来源：§12.1.1.1 response paragraphs,NOTES3-4；§12.1.3.1 steps4(b)(v-vi),2xx response paragraph；§6.3.3.1.20；§12.1.2.3，印刷页 144, 538, 546, 547, 548, 549。

## 范围边界

本页是独立告警的有限业务主链，不是完整 SIP、XML、安全、配置取得、位置编码或失败恢复实现。

自身 emergency state、MEA、组 in-progress emergency state、呼叫建立和各成员提示分别判断；不能由其中一项推断其他项。

动作的 SHALL、界面提示的 SHOULD/MAY、资源拒绝的 MAY 按原文区分；说明性 NOTE 不增加强制流程。

相关主题只是按需查阅入口，不是此流程的必经步骤：

- [alert-state](alert-state.md)
- [group-inprogress-upgrade](group-inprogress-upgrade.md)
- [../identity/mcptt-publish-service-authorization](../identity/mcptt-publish-service-authorization.md)
- [../groups/implicit-affiliation-eligibility](../groups/implicit-affiliation-eligibility.md)

[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，对应 3GPP TS24.379 Rel19。
