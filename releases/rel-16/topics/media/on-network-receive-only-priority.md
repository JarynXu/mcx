# 在网 MCPTT 只收：SDP 应答少了 mc_priority，能解释后来的 Floor Deny #5 吗？

不能只凭这两个包把原因连起来。先认出谁回答了同一条媒体面控制通道的 SDP offer，再查哪一侧因哪次话权请求发出了拒绝。本文限同系统普通在网单话权组呼；例子是控制侧直接服务该终端，不用非控制侧转发、多人通话或特殊呼叫的规则替代。

## SDP 先看原 offer 和实际应答者

`mc_priority` 在 offer 中表示发出 offer 的一方希望为自己的 Floor Request 使用的优先级上限（整数 1–255）；在 answer 中表示给这一方的上限，不得高于对应 offer 的值。它不是 Floor Granted。MCPTT 客户端要求不同于默认的优先级时须在 offer 中带该参数。若对应 offer 没有该参数，不用此处的省略规则判定配置，answer 也不能借此加一个 offer 没有的 fmtp 参数。[TS 24.380 V16.9.0 §12.1.2.2，印刷页 225](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=226)；[§14.2.3，印刷页 238](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=239)；[§14.3.1，印刷页 239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=240)

**对应 offer 确实有 `mc_priority` 时**，按实际回答这一腿的角色判断：

| 应答者 | 对这份 SDP answer 的要求 |
| --- | --- |
| 控制功能 CF；该组文档中对应 MCPTT 用户的 `entry` 有 `on-network-recvonly` 元素 | 不带 `mc_priority`。这是元素是否存在的判断，不用收到的省略反推元素的值或配置是怎样取得的。 |
| 控制功能 CF；该用户的对应项没有此元素 | 回三个值的最小值：offer 的话权优先级、组文档的 `user-priority`、业务配置的 `num-levels-priority-hierarchy`。 |
| MCPTT 客户端或非控制 MCPTT 功能 | 回对应 offer 里的值。不套用 CF 的配置分支。 |

§12.1.2.2 注 1 对 offer 或 answer 缺少参数写的是假定默认优先级。不能把省略当成 `mc_priority=0`、已协商了 `receive only` 上限、取得话权或 SIP 失败。要核实 CF 为何省略，查这个 offer、对应 answer、实际应答角色与 CF 本次用的目标用户组记录。这里的组成员配置也不是 SDP 媒体方向属性 `a=recvonly`。[§12.1.2.2 注 1，印刷页 225](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=226)；[§14.3.3，印刷页 239](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=240)

## 话权拒绝另查实际 Floor Request 和本腿的决定

**查控制侧的 U。** 例子是它已在 `U: not permitted and Floor Taken`，确实收到这个接口所关联终端的 **Floor Request**，无 audio cut-in、多人话权、广播或环境监听。条款以客户端已协商排队、按第 14 章在 `mc_priority` 中带话权优先级，或两者兼有，加上适用的本地策略，作为有效优先级处理的入口。这里只举后来独立确认两项都具备的例子，不从前述 SDP 缺项认定已协商。再核实本次算出的**有效优先级为 `receive only`**。此时 U 须在这条腿发 Floor Deny，`Reject Cause` 为 **#5**，请求带 Track Info 时回带，解释文字可选；U 仍为原状态。只具备其中一项时，与相邻 #1 段的条件可能重叠；不从这里补写执行优先级。若实际有效优先级不是只收，不能照此发 #5 或推定一定排队、抢占或获准，见[已有占用时的话权判断](on-network-preemption-revoke.md)。[§6.3.5.4.1，状态定义，印刷页 77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)；[§6.3.5.4.4，印刷页 78–80](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=79)；[有效优先级入口及 #5 分支，印刷页 79–80](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=80)

看到本腿发出 #5，只能证明这条拒绝使用了“请求方只有接收权限”这个原因。若要认定是上述 Taken U 分支，须对上请求、U 的状态与实际判定、拒绝发送记录。#5 不是该分支的唯一标记：例如广播/环境监听还有一支，[G 在 Idle 的旧入口](on-network-idle-floor-server.md)也有另一来源。不要用 #5 倒查成某组文档一定有只收元素，更不要用 SDP 缺项代替实际收件和优先级处理。[§8.2.6.2，印刷页 165](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=166)；[§6.3.5.4.4，印刷页 79](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=80)；[§6.3.4.3.3，印刷页 57](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=58)

**终端有没有收到，另看终端侧。** 终端处于 `U: pending Request` 并实际收到 Floor Deny 时，按这个等待请求应答的状态处理；仅当收到的 Deny 请求确认时才发 Floor Ack（Message Type 3、Source 0）。终端应通知用户、停 T101 并进入未获许可状态。终端已经在 `U: queued` 时，不能套用这里的 T101 处理。不同状态见[终端话权状态](on-network-floor-client.md)。若实际抓到的是非控制侧中继的回复，先按[非控制侧话权响应路由](on-network-noncontrolling-floor-grant.md)辨认哪条腿、哪位终端。SDP、Deny 或它的确认都不能代替 RTP 的终端接收、解码或播放证据。[§6.2.4.4.1、§6.2.4.4.4，印刷页 39–40](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=40)。
