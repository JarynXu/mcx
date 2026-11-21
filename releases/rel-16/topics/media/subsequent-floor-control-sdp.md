# 重新协商话权通道：后续 SDP offer 能带 mc_granted 吗？

同一个 MCPTT 会话可以在建立之后才第一次协商媒体面控制通道。**判断某份 SDP 是这个通道的初次还是后续 offer，要查这条通道先前有没有协商过，不能只看 SIP 方法或对话是否已存在。** 比如通道已经谈妥，后来用新 offer 改同一通道的媒体地址，这才是本页讨论的后续协商。反过来，称它为通道的初次 offer，也不能把它自动视为初始 SIP INVITE。[TS 24.380 V16.9.0，Rel-16 Stage 3，§14.2.1 及注，印 238](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=239)。

## 改地址时，不要把上次的授予字段复制进 offer

后续 offer 沿用初次协商的生成规则，但**不得包含 `mc_granted`**。§14.5 没有为它在后续 offer 中定义语义。若终端接受在初始 SIP INVITE 的 200 内收到 SDP 授予指示，§14.2.4 要求它在该初始 INVITE 的 offer 带上这个字段。那是能力声明，不是申请话权或授予。不要把这个初始 INVITE 的用法套到只因通道首次协商而称为初次的 SDP。[§14.2.4，印 238](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=239)；[§14.5，印 240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=241)。

例如，正常的后续 offer 没带 `mc_granted`，而对应 answer 在该控制通道的 `fmtp` 里加了它。发 offer 的一方须**丢弃这个新增参数，不是按这条规则丢弃整份 answer**。如果双方的 SDP 都带了它，§14.4 的“answer 新增参数”条件不成立；但 offer 的生成仍违背 §14.5，两边都写了也不是有效授予。先配对同一次 offer/answer 和对应的媒体段，再判增量。单见 SIP 200 不足以认定话权已授予。即便是适用的初始应答，没带 mc_granted 也只说明本份 answer 没用该字段指示授予，不能判请求被拒或不会另行获授。[§14.3.4，印 239–240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=240)；[§§14.4–5，印 240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=241)。

## 紧急升级可以请求话权，但请求入仲裁时仍没有许可

TS 24.380 只对**普通呼叫经 SIP re-INVITE 升级为紧急呼叫**定义后续 offer 中 `mc_implicit_request` 的语义。不能拿普通媒体修改里出现的同名字段当隐式请求，也不能把条文没定义语义说成它已经规定了失败响应。answer 中的接纳参数表示受理隐式请求，不是 Floor Granted。[§14.5，印 240](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=241)；[§12.1.2.2 及注 4，印 226](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=227)。

以在网普通组呼为例。原先是别人有发言许可，服务器面向这台申请终端的接口处于 `U: not permitted and Floor Taken`。当通话已升级为紧急组呼，而且应用与信令面已告知该后续 offer 含隐式请求参数时，这个接口须通知话权仲裁逻辑，然后**留在原状态**。查到这笔通知，只能说请求交给了仲裁。在同一状态下，接口若实际收到仲裁发来的 Floor Granted，才按授予程序转发给该终端并进入 `U: permitted`；仅见网络发出通知也不能证明终端收到或有语音实际送出。[§6.3.5.4.1，印 77–78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)；[§6.3.5.4.8，印 83](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=84)；[§6.3.5.4.9，印 84](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=85)。

如果查的是[初始 SDP 给 offerer 的 SSRC 和授予证据](implicit-floor-sdp-ssrc.md)，用同一媒体段的初始 offer/answer 核对。若要对照[在网单话权的显式抢占与撤销](on-network-preemption-revoke.md)，该页以显式 Floor Request 为主，隐式升级仅作比较，不能用显式流程替代。若查[在网按需预安排直接组的紧急发起或升级 SIP 信令](../calls/emergency-group-client.md)，按该组呼的客户端程序走，不用媒体面的 U 状态代替业务状态。
