# 排队后的授予与释放：用户确认、查询超时和通话结束

限 TS24.380 V19.1.0 §6.2 的在网基本 floor participant；已协商使用话权控制。

普通非广播、非 system、非 emergency/imminent-peril、非 ambient listening；不采用 pre-emptive、dual floor、multi-talker 或 audio cut-in。

每条保留触发状态与计时器条件。队列中的 grant、普通 pending Request 的 grant、pending Release 的迟到 grant 不能互换。

接收消息要求 Ack 的前提为 subtype 首位=1；相应 Floor Ack 的 Source=0。发出的 Floor Release 请求 Ack 是 MAY，Ack 收到/未收到后的处理是原文明示的实现选项。

## 排队接收媒体和位置通知

适用条件：状态为 U: queued，分别收到 RTP 或 Floor Queue Position Info。

收到 RTP 时请求 mixer 呈现，SHOULD 重启 T103，仍 queued，不因此获发送许可。收到 Queue Position Info 时，需要确认则回 Ack(type=9)；消息表示已排队或本端曾查询位置时，可向用户提供位置及可用优先级。停止正在运行的 T104，仍 queued。

依据：§6.2.4.9.1–.2;6.2.4.9.7，印刷页 51、53。

边界：位置与优先级展示是 MAY；未给出等待时长估算或位置变化即应重发请求的算法。

## 查询位置与 T104 超时

适用条件：状态为 U: queued；客户端请求查询位置且 T132 未运行，随后分别判断 T104 未达或达到 C104 上限的到期。

发送 Floor Queue Position Request，启动 T104、C104=1，留在 queued。未达上限时重发查询、重启 T104、C104 加 1，仍 queued。达到上限时给客户端 floor queued timeout，发送 Floor Release，可请求 Ack，启动 T100、C100=1，进入 pending Release。查询超时不是保留队列无限查询，也不直接跳到 has no permission。

依据：§6.2.4.9.9–.11，印刷页 53、54。

边界：T132 未运行是查询入口的明示条件。未核各计时器配置数值；不把 T104 上限误作整个队列最长等待时间。

## 排队获授后仍等待用户

适用条件：状态为 U: queued；收到 Floor Granted，尚未取得用户发送意愿确认。

需要确认时回 Ack(type=1)，通知用户已获 grant；停止运行中的 T104，启动 T132。若可选 T103 正在运行，且对应 participant 的此前 Floor Taken 没带 G-bit=1，停止该 T103。保存 Granted Participant 的 Audio SSRC 供后续 RTP 使用直到释放，但状态仍是 queued，不立即转发缓冲语音。

依据：§6.2.4.9.4;6.2.4.5.1 Note，印刷页 52、44。

边界：T103 停止条件保留 participant 关联和此前 Taken 的 G-bit 条件。收到 grant 与用户接受是两个事件；Floor Ack 也不是用户确认。

## 用户确认与 T132 超时

适用条件：状态仍为 U: queued，已收到 grant 且 T132 正运行；分别收到用户想发送的指示或 T132 到期。

用户在 T132 运行时确认要发送，停止 T132 并进入 has permission，后续按 §6.2.4.5.2 发送语音。若 T132 到期，则发送 Floor Release，可通知用户话权已不可用，可请求 Ack，然后直接进入 has no permission。此超时分支没有启动 T100 或进入 pending Release，不套普通释放重传链。

依据：§6.2.4.9.12–.13;6.2.4.5.2，印刷页 54、44、45。

边界：不把任意按键或 T132 未运行时的动作当作本分支确认；没有用户响应并不允许自动发送已缓冲语音。

## 排队请求被拒或取消

适用条件：状态为 U: queued；分别收到 Floor Deny、Floor Idle，或 Queued Floor Requests 的 Purpose=2（Cancel Notification）。

Deny 需要时 Ack(type=3)，必须通知拒绝、可显示 Reject Cause；Idle 需要时 Ack(type=5)，可通知 idle；Cancel Notification 需要时 Ack(type=14)，必须通知队列请求被取消，可展示 Requested Party's Identity 中的请求者。三分支都停止运行中的 T104 并进入 has no permission。

依据：§6.2.4.9.5;6.2.4.9.8;6.2.4.9.15，印刷页 52、53、54、55。

边界：这些条文未在此重复停止 T132；不自行补写该操作或推断竞态优先级。主动请求清空他人队列的授权和服务器处理不在本主题。

## 主动释放须区分原状态

适用条件：用户在 pending Request、has permission 或 queued 中要求释放当前请求/发送许可；分别按原状态处理。

三种状态都发 Floor Release，可请求 Ack，启动 T100、C100=1，并进入 pending Release。pending Request 另外停止 T101；queued 另外停止运行中的 T104 并停止 T132；has permission 可在尚未发送任何媒体前主动释放。不要把取消正在请求、取消排队和释放已取得许可写成同一个原状态。

依据：§6.2.4.4.8;6.2.4.5.1;6.2.4.5.3;6.2.4.9.6，印刷页 43、44、45、52、53。

边界：本普通范围不含 dual floor 的 G-bit 回带和 overriding/overridden 状态清理。Floor Release 不等于发 SIP BYE 或终止整场组呼。

## 话权被撤销

适用条件：状态为 U: has permission，收到 Floor Revoke，Floor Indicator 的 G-bit=0（非 dual floor）。

必须通知正在撤销许可，可告知原因；要求 mixer 丢弃剩余缓冲 RTP 并停止向服务器转发编码语音。发送含 G-bit=0 的 Floor Release，可请求 Ack，启动 T100、C100=1，进入 pending Release。不能把 Revoke 当作仅显示提示而继续发音。

依据：§6.2.4.5.4，印刷页 45。

边界：本条限定原文 G-bit=0 分支，不为缺失 Floor Indicator 的消息补默认解析；优先请求触发撤销及服务器接口的有限处理见关联主题；消息安全校验仍未在本页展开。

## T100 重试与释放完成

适用条件：状态为 U: pending Release；分别遇到 T100 到期、Floor Idle 或 Floor Taken。

T100 未达 C100 配置上限时重发 Release，可请求 Ack，重启 T100、C100 加 1并维持 pending Release；达到上限则进入 has no permission。普通非广播情况下收到 Idle，需要时 Ack(type=5)，可通知 idle，停止 T100并进入 has no permission。收到 Taken，需要时 Ack(type=2)，保存被授予者 Audio SSRC，应为新 talker 启动可选 T103；仅当自身不在 List of Granted Users 才按该条停止 T100，然后进入 has no permission。

依据：§6.2.4.6.1–.5，印刷页 47、48。

边界：T100 达上限后的本地转态不是服务器确认收到 Release 的证据。Taken 分支不能省略 List of Granted Users 条件而宣称总会停 T100；普通范围排除广播结束时另进 Releasing 的分支。

## 迟到授予不撤销释放

适用条件：状态为 U: pending Release；收到迟到的 Floor Granted，或收到 RTP 媒体。

Granted 需要确认时仍回 Ack(type=1)，但继续 pending Release，不恢复 has permission。收到 RTP 则请求客户端呈现，并 SHOULD 为该发送者启动可选 T103，仍 pending Release。Grant 的作用取决于当前状态，听见 RTP 也不能取消本端释放流程。

依据：§6.2.4.6.6;6.2.4.6.8，印刷页 48、49。

边界：不把接收 Ack 解释成重新接受话权。媒体来源校验与乱序窗口未在本主题建立。

## 结束通话的两阶段处理

适用条件：MCPTT call 即将释放或本 participant 离开，应用/信令层发出 call release step1；随后应用/信令层确定通话已释放并发出 step2。

step1 在除 Start-stop、Releasing 外的活动状态停止发送 floor control、停止运行中的计时器，请求客户端停止 RTP，并进入 Releasing。此时等待信令层完成断开。step2 释放全部资源及仍有关联的计时器，回到 Start-stop并终止状态机实例。用户面可发起第一阶段，但第二阶段总由应用/信令层发起。

依据：§6.2.2;6.2.4.7.1–.2;6.2.4.8.1–.2，印刷页 36、49、50、51。

边界：不从一个 Floor Release 或 T100 到期推导整个通话释放完成。SIP 释放条件、预建立会话是否保留由相应 TS24.379/MCPC 主题处理。

## 证据边界

- 仅按各页的状态与条件衔接；撤销发出不证明终端已停，排到队首不证明新 Granted，下一持有人首包成功也须独立观察。
- 只解释接收者的状态与动作，不提供服务器队列公平性、抢占、dual floor、multi-talker 或 audio cut-in 的完整流程。
- T100/T101/T104/T132 数值与可配置范围未核，不给默认秒数；§8 消息编码、§13 安全处理未完整展开。
- 队列 Deny/Idle/Cancel 与 grant 后 T132 的竞态未补充；条文明写的不同转态保持原样。
- SIP 呼叫准入、GMK/PCK 媒体加密和已取得 floor permission 是不同层次，不由本页任何单一状态推定另两层已成功。

## 按需继续

- [优先请求与撤销的有限分支](floor-preemption-decision.md)
- [撤销传递、宽限与停止证据](floor-revoke-observation.md)
- [floor-participant-entry-request](floor-participant-entry-request.md)
- [group-participant-leave](group-participant-leave.md)
- [server-release-chain](server-release-chain.md)
- [implicit-floor-request](implicit-floor-request.md)

[ETSI 官方 TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅所列版本和条款。

[服务器排队的协商条件](floor-server-queue-admission.md)：仅按该页版本和适用条件衔接。

[服务器授予后计时与客户端等待不同](floor-server-media-timers.md)：仅按该页版本和适用条件衔接。
