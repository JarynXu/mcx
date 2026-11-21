# 隐式话权请求：SDP answer 的 mc_ssrc 属于谁？它是授权吗？

终端在普通在网 MCPTT 呼叫的初始 INVITE 里用 `mc_implicit_request` 请求话权。收到该 offer 的 SDP answer 后，**先分开看三个问题：服务器是否接纳请求、为哪个发送方确认了什么 SSRC、何时持有话权。** 以下不套用加入 chat 组呼、加入进行中的预安排呼叫或临时组会话的授予分支。〔TS 24.380 V16.9.0，§§12.1.2.2、14.3.4–.6，印 225–226、239–240〕

## mc_ssrc 是 offerer 的值，不是应答方的

在匹配的 SDP answer 中，`mc_ssrc` 表示 **offerer** 的 SSRC。〔§12.1.2.2，印 226；§14.3.6，印 240〕

- offer 在 `ssrc` 媒体属性中给了一个值：对这里的隐式请求，服务器返回该值；检测到冲突时可返回新值。不能把“与 offer 不同”本身读成拒绝或当作服务器的 SSRC。
- offer 没有指明 SSRC：服务器可以确定一个合适的值。这不是缺值即失败，也不是每次缺值都必须分配。

比较时配对**同一次、同一媒体段**的 offer 和 answer。即使看到换值，也不能仅凭这两处数字定位冲突、确定哪条 RTP 实际用了该 SSRC，或判定哪一端有发言权。

## answer 里有 mc_ssrc，但没 mc_granted，能不能发语音？

按 §12.1.2.2，answer 中的 `mc_ssrc` 只在应答方接纳 offer 中的隐式请求时返回。`mc_implicit_request` 在 offer 是请求，在 answer 是接纳；接纳不等于已授予话权。**只有 `mc_ssrc` 或 `mc_implicit_request`，不是发送语音的许可。** 发起方要另看适用的授予信号，例如收到有效的 Floor Granted 或该流程的 SDP 授予指示。〔§12.1.2.2 及注 2、4，印 225–226〕

`mc_granted` 在初始 offer 表示终端接受用 200 内的 SDP 得到授予指示，不是发出请求；在适用的 answer 才表示话权已授予 offerer。普通非临时 MCPTT 呼叫中，控制功能在 offer 带该参数时可以选择用 200 表示授予，决定用它授予时须在 answer 中带该参数。没带 `mc_granted`，不能据此判隐式请求遭拒或话权以后也不会授予。〔§14.2.4，印 238；§14.3.4，印 239–240；[授予和早期媒体的证据](implicit-floor-early-media.md)〕

## 通用 fmtp 检查不能代替这笔比较

§14.3.1 规定 answer 的 `fmtp` 不得增加相应 offer 没有的参数；§14.4 规定 offerer 丢弃这种额外**参数**，不是丢弃整份 answer。§14.3.6 的专门文字使用的是 **offer 中的 `ssrc` 媒体属性**和 **answer 中的 `mc_ssrc` fmtp 参数**，并明确与 `mc_granted` 是否出现无关。两个字段不是同名参数。排查时要把通用匹配规则和专门返回条件列开；这里不替本版制定通用豁免、实现优先级或自动拒绝策略。〔§§14.3.1、14.3.6、14.4，印 239–240〕

来源：[TS 24.380 V16.9.0，Release 16，Stage 3（ETSI），SDP 语义，印 225–226](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=226)；[IE 配置与应答处理，印 238–240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=239)。
