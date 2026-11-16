# 私呼本人取消：通话、告警与用户状态分开处理

## 适用范围

- TS24.281 V19.3.0（2026-01）；已建立的在网、本地、带 transmission control、直接面向单一 MCVideo ID 的按需私呼，现有 SIP 对话和媒体参数已经存在。排除预建立会话、FTA、功能别名、组呼、远程发起、ambient、离网及无TC私呼。
- 每条声明独立继承共同条件并叠加自身条件，不继承前条成功。请求仅由紧急条件发起者对自身条件操作，不含 originated-by；对端声明观察该请求的接收客户端，不要求接收者等于发起者。本页不建立新私呼，也不执行 BYE。
- 用户 emergency state、私呼优先级 MVEPP、发起私呼状态 MVEPC、私呼告警 MVPEA、CF 的 originating→target 缓存是不同对象。它们不等于组呼 MVEG/MVEGC/MVEA，也不等于媒体发送许可。
- info MIME 指 application/vnd.3gpp.mcvideo-info+xml。规范中的调用编号、组/私呼用词、状态编号及外部媒体规范不一致均保留；本页不提供已闭合的可运行互操作实现。

## 本人取消的权限与选择

适用条件：本用户请求取消自己发起的紧急私呼，MVEPC3；按各分支读取MVPEA。

allow-cancel-private-emergency-call=true才获准，其它情况未授权；主条未授权时SHOULD告知并停止。获准后调用6.2.8.3.6：MVPEA1时带emergency=false、清用户emergency state、MVEPP3 cancel-pending；MVPEA非1且仅取消通话时带emergency=false、MVEPP3，保留用户emergency state。若请求同时取消本人告警，则始终带emergency=false、置MVEPP3并清用户emergency state；仅告警取消获准才另带alert=false和置MVPEA4，否则SHOULD告知无告警取消权限。

- 告警取消许可要求allow-cancel-emergency-alert=true，其它情况未授权。此私呼helper在同时请求取消两者时，清用户emergency state不被告警许可条件包住；不可改成组呼规则。
- 仅取消通话分支将MVEPC误拼MVEPPC；保留拼写异常，不引入新状态机。

依据：§10.2.2.2.4;6.2.8.3.1.2–3;6.2.8.3.6，印刷页 77、78、79、80、330。

## 请求字段及最终响应

适用条件：客户端已获本人取消许可；不带originated-by。

请求带按6.2.8.3.3选择的Resource-Priority和当前媒体参数SDP；需要隐式发送请求时按6.4指示，再发送re-INVITE。2xx先与原文所指TS24.380用户面交互，再置MVEPP1/MVEPC1；MVPEA4且无Warning149时置MVPEA1。错误响应含emergency=true才由该分支置MVEPP2；含alert=true时置MVPEA3。错误响应完全不含info MIME时，置MVEPP2，并恢复进入取消前的告警状态。

- 完全无info MIME不等于有MIME但无alert元素；不扩大恢复条件，也不自动恢复用户emergency state。
- 本条取消紧急条件，不是结束会话；错误响应下的优先级和告警状态分别按所列字段及缺失条件处理。Resource-Priority重叠未裁决；CF还会拒绝带紧急优先级值的取消请求。
- 主条声称on-demand，但NOTE提预建立group session，2xx告警段称priority group call；本页严格限定按需私呼并保留异常。

依据：§10.2.2.2.4;6.2.8.3.3，印刷页 78、330、331。

## 后续 INFO 中的告警结果

适用条件：符合6.2.8.3.7的私呼对话内INFO入口，MVPEA4。

Info-Package须为g.3gpp.mcvideo-info，带关联info MIME，且至少设置alert/emergency/imminentperil之一；MVPEA4时，alert=true将其置3，alert=false将其置1。没有alert时不据这两个分支推导结果。

- 取消主条仍写ongoing group session入口，与private helper不一致。149表示告警部分等待，不把它当整个通话取消失败。
- 不增添helper未写的MVEPC门槛、originated-by检查或显式先回200步骤；本主题本已排除第三方。

依据：§6.2.8.3.7;10.2.2.2.4 INFO paragraph，印刷页 80、81、331。

## 对端重邀请的状态与接受

适用条件：对端收到既有按需私呼的re-INVITE，不含originated-by。

emergency=true时SHOULD显示升级、发起者及存在的告警，并设置本私呼MVEPP2；emergency=false时SHOULD显示降级及请求者，若alert=false另SHOULD显示告警取消；置MVEPP1，原MVEPC3时再置MVEPC1。已有对话不尝试改变answer-mode；客户端接受re-INVITE，生成带SDP answer的200，发送后才调用TS24.581媒体面。

- 本次不含originated-by，不利用该条第三方告警取消分支清掉接收者自己的MVPEA或用户emergency state。
- 对端的MVEPP2不能当发起者MVEPC3，也不能把200或显示告警当已授予发送许可。

依据：§10.2.2.2.3，印刷页 329、330。

## 证据边界

- 本人取消边界之外的第三方操作、释放及故障恢复未展开。

## 按需继续

- [MCVideo 私呼释放：客户端 BYE 与媒体停止、资源回收](private-call-client-release.md)
- [私呼紧急升级：目标许可、待确认状态与告警结果](private-emergency-client-upgrade.md)
- [私呼紧急更新的服务器路径：两侧PF、CF权限与部分成功](private-emergency-server-path.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。
