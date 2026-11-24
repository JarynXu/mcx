# 在网 MCPTT 呼叫升级时话权空闲，谁处理隐式话权请求？

升级的 SIP 200 不是话权授予。对已经进行的在网 MCPTT 呼叫，话权服务器面向单个参与者的 **U 接口**和负责整场话权的 **G 仲裁**各有自己的入口。先查是哪一层实际收到事件，再查这一层的前态。不用一层的状态或一条 SIP 响应代替另一层的处理证据。

## U 把请求报给仲裁，仍没有许可

前态是 `U: not permitted and Floor Idle`。已有会话升级为紧急组呼，且应用与信令面实际指示这次后续 SDP offer 含 `mc_implicit_request` fmtp 属性时，U 须向话权服务器的仲裁逻辑报告这笔因升级产生的隐式请求，自己仍留在原状态。只在报文里看到属性，不能证明 U 收到了这项指示。这一条只写紧急组呼升级，没有给迫近危险升级写同样的 U 入口。[TS 24.380 V16.9.0，Release 16，Stage 3，§6.3.5.3.9，印刷页 77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)。

## G 收到请求后，拒绝和授予分开判断

G 在 `G: Floor Idle` 时，实际收到因升级为紧急组呼或迫近危险呼叫产生的隐式话权请求，才适用下面的规则。G 的入口列出两种升级，不说明前一段的 U 也处理这两种升级。

- **拒绝：** 通话只有一个 MCPTT 客户端时，G 须拒绝。请求被拒后，须发 `Floor Deny`，`Reject Cause` 写 #3（Only one participant），可附 `Reject Phrase` 说明，并留在 `G: Floor Idle`。不能把同一数字当成 `Floor Revoke` 的原因码。
- **请求实际获准：** G 须停 `T4`（Inactivity）和 `T7`（Floor Idle），保存获准参与者的 SSRC，并按 §6.3.4.4.2 进入 `G: Floor Taken`。保存的 SSRC 保留到这笔请求对应的话权释放。停止计时器和保存 SSRC 属于授予分支，不是收到请求就做。通话有两台或更多客户端，不等于本条要求授予。

这里能判断的是话权服务器按该事件应走的分支。它不证明终端收到授予、已经开始发 RTP 或别人听到了语音。[TS 24.380 V16.9.0，§6.3.4.3.6，印刷页 58](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=59)。

[空闲时收到显式 Floor Request](on-network-idle-floor-server.md)；[话权已被占用时的再协商](subsequent-floor-control-sdp.md)；[初始 SIP 会话中的隐式请求](implicit-floor-early-media.md)；[Floor Deny 与 Floor Revoke 的原因码](floor-deny-revoke-cause.md)。
