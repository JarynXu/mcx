# 双话权：第二路停止与原主路退出后的接续

## 适用范围

- 固定TS24.380 V19.1.0普通在网组呼，选择不撤销原持有者的overriding pre-emptive分支；排除multi-talker、audio cut-in、广播、ambient listening、紧急/迫近危险及临时组。
- 以下接纳条件是在创建 D 之前已成立的前提，不是退出时仍须重新满足的即时条件：接口请求者协商queueing及mc_priority、非receive only，显式请求带priority；有效优先级为pre-emptive，当前持有者非pre-emptive且没有其他pre-emptive请求排队。本地策略选择允许原持有者与新请求者同时发送，而非撤销。
- 分别观察G基本仲裁、D双话权仲裁及服务端参与者接口；许可、通知、媒体转发请求与终端实际收到/停止是不同证据。本页不核完整终端处理、配置schema、安全密钥或混音。

- 原有三种第二路出口分别只适用于 D: Floor Taken 的 T11 到期、T12 到期、以及已送达 D 的关联 overriding 参与者 Floor Release；各自的计时器、接收集合、通知顺序与确认条件仍以对应声明为准。新增原主路退出只涵盖 Release、T1 到期和断开指示已到 G 三个入口；不据此扩展旧三个出口或推定完整媒体交接。

本文使用 G 表示基本话权仲裁，D 表示双话权仲裁。overriding 指新增的抢占发言者，overridden 指创建 D 时仍获准发言的原持有者；原主路退出后的状态按各节区分。两路许可不等于任意数量的并发发言许可。

## 断流超时停止第二路分发

适用主体：D仲裁逻辑。

状态：D: Floor Taken。

适用条件：T11到期。

T11到期，先停运行中的T12，再请求分发器停止向其他客户端分发overriding客户端的RTP，随后释放D媒体资源、实例及相关运行计时器。step4向相关non-controlling function及受控的接收新路者发Idle，明确G=1、序号加1。若基本状态为原文G: Taken，step5向相关non-controlling function及受控的仅接收新路者发Taken，按privacy条件带当前获准者身份和可选alias、序号加1及Audio SSRC of Granted Participant。若基本状态为G: Idle，step6向所有floor participants发Idle，序号加1。最后进入Start-stop。

- step5恢复Taken和step6全体Idle均未指定G-bit值；不从step4或其他入口补位，也不将未指定解释为默认0。
- 基本状态在本段写G: Taken/G: Idle，对应一般G控制的Taken/Idle语境；不据简称另造状态。
- 仅核停止新路分发的义务，不证明旧路结束或客户端缓存清空。

规范强度：主体shall；alias may。

依据：3GPP TS 24.380 V19.1.0 §6.3.6.3.3，印刷页 107、108。

## 说话时长到期撤销并结束D

适用主体：D仲裁逻辑。

状态：D: Floor Taken。

适用条件：T12到期。

按step1–8顺序：停止T11；请求分发器停止向其他MCPTT客户端分发RTP；向获准参与者发Revoke，cause=2、G=1，若存有dual关联Track Info则携带，随后删除所存dual Track Info。若基本状态为G: Taken，向仅接收新路的参与者发Taken，按privacy条件含当前获准者身份和可选alias、序号加1及Audio SSRC of Granted Participant；本条对non-controlling function接收者附加临时组会话条件，本页排除临时组，故不无条件包含该接收集合。若基本状态为G: Idle，向所有floor participants发Idle，序号加1。通知后才释放D媒体资源及实例，最后Start-stop。

- 本handler未在Revoke之后先发G=1的Idle；Taken及全体Idle也未明列G-bit，不补0或1。
- step3a的cause文字引用6.3.4.5.2；保留交叉引用。此D handler未列等待Release/T3，不能据此拼出普通G撤销全链，也不否认所引条款的存在。
- step1停止T11没有if running限定；step7释放资源/实例未重述any running timers，不从另外两个出口移植文字。
- step2只写停止向其他客户端分发RTP，本页不将其扩成全部组会话媒体停止。
- 终端实际停采音、停播放或接收Revoke仍不是此服务器动作的既成事实。

规范强度：动作及必选字段shall；privacy条件下alias may。

依据：3GPP TS 24.380 V19.1.0 §6.3.6.3.4，印刷页 108、109。

## 收到Release结束第二路，不结束整个组呼

适用主体：D仲裁逻辑。

状态：D: Floor Taken。

适用条件：仲裁者收到关联overriding参与者的Floor Release；本页以该D事件已经送达为输入。

收到该D入口的Release后，按step1–9顺序：请求分发器停止向其他客户端分发overriding客户端的RTP；停运行中的T12；停止T11；释放D媒体资源、实例及相关运行计时器。若所收Release subtype第一位为1（请求确认），须发Floor Ack，Source=2、Message Type=4。随后向相关non-controlling function、overridden floor participant以及受控的接收新路者发Idle，明确G=1、序号加1。若基本状态为G: Taken，向相关non-controlling function及仅接收新路者发Taken，按privacy条件含当前获准者身份和可选alias、序号加1及Audio SSRC of Granted Participant；若基本状态为G: Idle，向所有floor participants发Idle，序号加1。最后Start-stop。

- 本节开头仅写收到Floor Release；本页关联对象是D所服务overriding用户，不外推任意他人的Release结束D。
- 终端经接口到D的完整路由仍未核，但本handler请求确认位成立后的Ack是明确义务；不把Ack当终端清缓存或全组释放证据。
- step7恢复Taken和step8全体Idle没有明列G-bit；只有step6明确G=1，不按其他入口补位。
- 停止T12带if running，停止T11没有该限定；不把两者写成同一个条件。

规范强度：动作与条件Ack shall；privacy条件下alias may。

依据：3GPP TS 24.380 V19.1.0 §6.3.6.3.6，印刷页 109、110。

## 原持有者的 Release 送往 G，而非 D

适用主体：原持有者服务端接口及 G 仲裁。

状态：接口 U: permitted；G: Floor Taken；D: Floor Taken。

适用条件：承接此前已按本页共同接纳条件建立的 D；普通在网组呼，另排除 system call。本节状态与事件分别适用，不把此前创建 D 时原持有者获准发言的条件要求延续至退出之后。；接口已保存该参与者 overridden without revoke 指示；收到其 Floor Release。

接口先按请求确认位回 Ack（Message Type=4、Source=2，原消息有 Track Info 时带回），将确认位清为 0 后送至 general 状态机，删除 overridden 指示并转 U: not permitted and Floor Taken。G 收到 Release 后要求停止转发该发送者 RTP，停止其运行中的 T2/T20；非 multi 分支调用 §6.3.4.3.2。该条并未列停止 T1。

- 接口已经存有 overridden 指示是本 claim 的输入，不从参与者姓名推断。
- 另一 overriding 指示分支把 Release 送至 D；两种角色不可交换。
- 停止转发不证明终端缓存清空或全组停止。

规范强度：动作 SHALL；NOTE 与本文证据边界单独说明。

依据：3GPP TS 24.380 V19.1.0 §6.3.5.5.3 steps1,3;6.3.4.4.6 steps1–4，印刷页 94、65。

## 原主路 T1 到期也可进入同一转换入口

适用主体：G 仲裁。

状态：G: Floor Taken；D: Floor Taken。

适用条件：承接此前已按本页共同接纳条件建立的 D；普通在网组呼，另排除 system call。本节状态与事件分别适用，不把此前创建 D 时原持有者获准发言的条件要求延续至退出之后。；原主路 T1 到期，非 multi-talker；D 实例仍存在。

先停止原持有者运行中的 T2/T20，请求停止向其他客户端分发其 RTP，但已在服务器缓冲中的 RTP 在持续缓冲情形下例外；随后调用 §6.3.4.3.2。此入口与主动 Release 的媒体缓冲条件不同。

- 不把该原路 T1 与 D 的 T11 混同。
- 不加入原文未写的清空缓冲或全组结束。

规范强度：动作 SHALL；NOTE 与本文证据边界单独说明。

依据：3GPP TS 24.380 V19.1.0 §6.3.4.4.3 steps1–4，印刷页 64。

## 客户端离开须先区分服务端接口事件

适用主体：原持有者服务端接口及 G 仲裁。

状态：接口非 Start-stop/Releasing；G: Floor Taken；D: Floor Taken。

适用条件：承接此前已按本页共同接纳条件建立的 D；普通在网组呼，另排除 system call。本节状态与事件分别适用，不把此前创建 D 时原持有者获准发言的条件要求延续至退出之后。；原持有者的应用/信令层发 call release step1；接口断开指示到达 G；不研究整组 call release。

接口停止向关联端发送控制消息、请求停向该端发 RTP、忽略来自该端的控制消息、请求停将其 RTP 交分发器，再通知仲裁该客户端开始断开，接口进入 Releasing。G 的 permitted-client-release 非 multi 分支调用 §6.3.4.3.2。该 G 分支没有另列停止 T1/T2/T20，不能从其他退出条款移植。

- 接口通知写到 arbitration logic，未明确列在 G/D 并存时依哪条角色指示选择子状态机。本 claim 把指示已到达 G 作为额外条件，不宣称完整路由闭合。
- §6.3.6.3.8 是 overriding 客户端断开的 D 处理，不能套给原主路。

规范强度：动作 SHALL；NOTE 与本文证据边界单独说明。

依据：3GPP TS 24.380 V19.1.0 §6.3.5.8.1–6.3.5.8.2;6.3.4.4.11，印刷页 101、68。

## 调用 Idle 入口不保证落在 Idle

适用主体：G 仲裁。

状态：从非 Start-stop 调用 §6.3.4.3.2，D 实例存在。

适用条件：承接此前已按本页共同接纳条件建立的 D；普通在网组呼，另排除 system call。本节状态与事件分别适用，不把此前创建 D 时原持有者获准发言的条件要求延续至退出之后。；从上述有限 G 退出入口到达 §6.3.4.3.2 的 D-exists 分支。

依顺序删除已存的 G 关联 Track Info；向配置为接收 overridden 媒体的所有参与者发送 Idle，序号加 1；向配置为仅接收 overridden 媒体者发送 Taken，序号再加 1。该 Taken 在未请求 privacy 时带 overriding 用户的 MCPTT ID，但 Audio SSRC 字段按本版字面取为给 overridden 参与者生成的 SSRC；位置按 §6.2.4.3.5。然后将 general 状态设为 G: Floor Taken，向 D 发送 termination instruction。该分支未列取队首或启动 T4/T7，也未调用 §6.3.4.4.2 重新授予。

- D-exists 分支没有前一 D-absent 分支的“无人协商 queueing”前提，不把前一段 guard 移过来。
- 普通范围中这两条通知未明列 G-bit=0 或 1；不能补默认值。
- 位置回指保留 profile/可用性条件：不可用或不允许报告时用 Not provided，不能由隐私身份分支推成任意披露。
- Taken 身份与 SSRC 指向不同角色；保持原文差异，不纠正为 overriding SSRC，也不声称媒体关联正确。
- 原文先设 G Taken 再发 Terminate；不能把段落标题当最终空闲状态。

规范强度：动作 SHALL；NOTE 与本文证据边界单独说明。

依据：3GPP TS 24.380 V19.1.0 §6.3.4.3.2 second branch;6.2.4.3.5，印刷页 60、61、40。

## Terminate 转移计时职责，不结束第二路 talk burst

适用主体：D 仲裁与 G 计时职责。

状态：D: Floor Taken；caller 已将 general 状态设为 G: Floor Taken。

适用条件：承接此前已按本页共同接纳条件建立的 D；普通在网组呼，另排除 system call。本节状态与事件分别适用，不把此前创建 D 时原持有者获准发言的条件要求延续至退出之后。；D 实际收到 termination instruction。

若 T11 运行，将 T1 值设为 T11 值并启动 T1；若 T12 运行，将 T2 值设为 T12 值并启动 T2。随后释放 D 相关媒体资源及实例、停止该状态机相关运行计时器，D 进入 Start-stop。NOTE 明确 overriding 参与者保持话权直到当前 talk burst 结束。本 handler 未列发送新的 Granted、Revoke、Idle 或 Taken。

- value 未在本 handler 明写为剩余时长或重新取默认值；不擅自选择时间语义。
- T11/T12 各自是否运行分别决定转移，不能无条件同时启动 T1/T2。
- 不能把 D 资源释放扩成停止仍有话权者的整个媒体会话；资源迁移实现细节没有在本条列全。
- 未明列把 D 保存的 SSRC/Track Info 转存为 G 关联状态；不补迁移算法。

规范强度：动作 SHALL；NOTE 与本文证据边界单独说明。

依据：3GPP TS 24.380 V19.1.0 §6.3.6.3.9;6.3.4.3.2 second branch steps4–5，印刷页 111、61。

## 状态与计时转换不等于接口媒体交接已闭合

适用主体：原 overriding 参与者的服务端接口。

状态：U: permitted。

适用条件：承接此前已按本页共同接纳条件建立的 D；普通在网组呼，另排除 system call。本节状态与事件分别适用，不把此前创建 D 时原持有者获准发言的条件要求延续至退出之后。；接口仍保存 overriding without revoke 指示；若实际收到来自仲裁的 Floor Idle。

§6.3.5.5.4 的 overriding 分支在实际收到 Floor Idle 时会转发 Idle、删除 overriding 指示且保持 U: permitted。G 的转换通知接收集合却按是否配置接收旧 overridden 媒体决定，不能由 D 已终止推定该接口必已收到 Idle 或清除指示。§6.3.5.5.6–.7 的文本提取可见未保存 overriding 指示时请求将 RTP 转交分发器，以及与 RTP 转发、§6.3.4.4.5、§6.3.6.3.5 有关的动作；文本提取中的标题、编号与事件归属关系不清，未完成版面核对；不能据此重排动作或宣称已证实原版排版错误。

- 这是条件接口动作与未闭合前提的界定，不证明终端媒体中断或实现一定失败。
- 文本提取中的标题、编号与事件归属关系不清，未完成版面核对；不能据此重排动作或宣称已证实原版排版错误。不把这些动作无疑义地归入某个 handler，也不静默移动动作以补齐接口交接调用链。
- G 的 §6.3.4.4.5 在实际收到 permitted RTP 指示时按条件启动 T2、重启 T1、停止运行中的 T20 并按本地策略转发；它不是已完成接口交接的证据。

规范强度：动作 SHALL；NOTE 与本文证据边界单独说明。

依据：3GPP TS 24.380 V19.1.0 §6.3.5.5.4 step3;6.3.5.5.6–.7;6.3.4.3.2 second branch;6.3.4.4.5，印刷页 94、95、60、61、65。

## 内部 Terminate 与终止通话是不同入口

适用主体：D 仲裁。

状态：D: Floor Taken；或 call-release 状态路径。

适用条件：承接此前已按本页共同接纳条件建立的 D；普通在网组呼，另排除 system call。本节状态与事件分别适用，不把此前创建 D 时原持有者获准发言的条件要求延续至退出之后。；分别比较收到内部 Terminate 与应用/信令层 call release step1/step2。

内部 Terminate 执行计时转移并保留 overriding 当前发言。call release step1 则请求停止向 MCPTT 客户端发送 RTP 并进入 Releasing；step2 释放 D 资源、实例和运行计时器后回 Start-stop。这两段不能因最终都出现 Start-stop 而合并。

- 只用于区分事件与职责，不扩展成完整信令层呼叫释放流程。

规范强度：动作 SHALL；NOTE 与本文证据边界单独说明。

依据：3GPP TS 24.380 V19.1.0 §6.3.6.3.9;6.3.6.4.1–6.3.6.5.2，印刷页 111。

## 条款差异与解释边界

§6.3.6.3.3 steps3–7;6.3.6.3.6 steps4–9，印刷页 107、108、109、110：原文在释放D资源/实例后继续通知并回Start-stop；按列明顺序保留，不另造对象销毁算法。

§6.3.6.3.4 step3a，印刷页 108：cause2说明交叉引用6.3.4.5.2；本页不将该引用静默删除，也不由它擅自引入T3等待完整链。

§6.3.4.3.2 second branch step3 a,d，印刷页 60、61：身份字段明确 overriding participant，Audio SSRC 明确 overridden participant。保留两者，不自行修正。

§6.3.5.5.6–6.3.5.5.7，印刷页 95：文本提取中的标题、编号与事件归属关系不清，未完成版面核对；不能据此重排动作或宣称已证实原版排版错误。

§6.3.6.3.9，印刷页 111：value 及 D 资源释放与 NOTE 的继续发言同时存在；不能自行解释成剩余时长转移、全资源销毁或显式 SSRC 重绑定。

## 未覆盖的行为

- 有限server D状态用途；不代表完整双话权、配置、安全或终端状态机已闭合。
- 原主路 Release、T1 到期及断开指示已到 G 后的有限 Terminate 链见本页；完整媒体交接、SSRC/Track Info 迁移、并发竞态与配置仍未闭合。
- 本页不展开D中再次收到Floor Request；同一已获准overriding参与者的有限回应见配套入口主题，接口G/D选择与Granted回程仍未闭合。call release仅区分D的两阶段动作，不覆盖完整信令层释放。
- 端到端G-bit/Ack路由与终端停发确认（不排除本页已核的条件Ack生成）
- 23.379 N7及接收分组配置字段
- 端到端加解密、混音、首包/首音验收

- 文本提取中的标题、编号与事件归属关系不清，未完成版面核对；不能据此重排动作或宣称已证实原版排版错误。

## 按需继续

- [双话权：保留原发言者的第二路许可与媒体](dual-floor-entry-and-media.md)
- [优先请求：何时触发撤销，为什么队首仍不等于获权](floor-preemption-decision.md)
- [撤销传递：服务端宽限、终端停止请求与交接证据](floor-revoke-observation.md)
- [多发言者与预配置重组：服务器混音和组密钥前提](../security/group-call-media-boundaries.md)

[3GPP TS 24.380 V19.1.0，ETSI 官方发布版](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅适用于所列版本和条款。
