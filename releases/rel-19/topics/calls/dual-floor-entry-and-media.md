# 双话权：保留原发言者的第二路许可与媒体

## 适用范围

- 固定TS24.380 V19.1.0普通在网组呼，选择不撤销原持有者的overriding pre-emptive分支；排除multi-talker、audio cut-in、广播、ambient listening、紧急/迫近危险及临时组。
- 接口请求者协商queueing及mc_priority、非receive only，显式请求带priority；有效优先级为pre-emptive，当前持有者非pre-emptive且没有其他pre-emptive请求排队。本地策略选择允许原持有者与新请求者同时发送，而非撤销。
- 分别观察G基本仲裁、D双话权仲裁及服务端参与者接口；许可、通知、媒体转发请求与终端实际收到/停止是不同证据。本页不核完整终端处理、配置schema、安全密钥或混音。

本文使用 G 表示基本话权仲裁，D 表示双话权仲裁。overriding 指新增的抢占发言者，overridden 指仍获准发言的原持有者。两路许可不等于任意数量的并发发言许可。

## 先选同时发言，再进入D仲裁

适用主体：请求者服务端接口及仲裁逻辑。

状态：接口U: not permitted and Floor Taken；G: Floor Taken；D初始Start-stop。

适用条件：共同范围；接口收到显式Floor Request，继而仲裁者收到转交的pre-emptive请求。

接口按请求值与协商最大priority较低者等参数计算有效优先级；在共同条件下转交抢占请求并保持接口状态。G: Floor Taken按本地策略选择同时允许当前speaker与请求者时，§6.3.4.4.7 step3明确调用§6.3.6.2.2，后者创建D状态机、保存请求者SSRC及请求中存在的Track Info，进入D: Floor Taken。不是因为数字更高就自动撤销旧talker。

- 本页两项均协商，避免not queueing OR not priority拒绝外层与后续OR条件重叠；不据此改写原文。
- 6.3.6.2.2以请求被授予为入口措辞，实际发送Granted在随后6.3.6.3.2；保留调用关系，不插入额外预先Granted。

规范强度：取值/转交/创建shall；有效优先级与并发策略依规定/本地政策。

依据：3GPP TS 24.380 V19.1.0 §6.3.5.4.4 steps1,5;6.3.4.4.7 step3;6.3.6.2.2，印刷页 86、87、88、65、66、106。

## D不是任意多talker容量列表

适用主体：仲裁逻辑。

状态：D状态机生命周期。

适用条件：已有当前speaker，另一个具overriding pre-emptive优先级者获准不撤销原speaker。

为允许不撤销较低priority当前speaker的参与者保留一个D实例；该参与者称overriding MCPTT client。NOTE限定一个呼叫仅一个此类pre-emptive用户；基本G控制继续，不能把D解释成multi-talker任意许可列表。未定义事件到达当前D状态时丢弃控制消息、请求分发器丢弃所收RTP并保持状态。

- 原文写lower flow priority，保留该用词而不造另一种priority字段。
- D初始及media burst释放回Start-stop；完整释放/重建竞态不在此推导。

规范强度：实例/未定义事件处理shall；单用户限制为NOTE。

依据：3GPP TS 24.380 V19.1.0 §6.3.6.1;6.3.6.2.1，印刷页 104、105。

## G-bit授予与分组通知

适用主体：仲裁逻辑。

状态：进入D: Floor Taken。

适用条件：已由6.3.6.2.2进入D授予流程。

向请求者发Granted：Duration=T12，含granted priority、已有Track Info、G-bit=1及生成保存的全局唯一audio SSRC。先向相关non-controlling function及按本地策略仅听overriding媒体的受控参与者发Idle，序号加1；再向相关non-controlling function及会听overriding媒体的受控参与者发Taken，序号加1、G-bit=1、该audio SSRC，未请求privacy时含granted MCPTT ID且可含alias。启动T11并进入D: Floor Taken。原speaker继续发声，听原路、新路或两路由配置决定。

- 入口Idle未明列G-bit=1，不能因随后Taken是1而给Idle补位。
- NOTE1描述non-controlling端在收到Taken G=1时向仅听新路者发Idle，与上层先发Idle的语境并列保留；不扩成完整非主控流程。
- 不沿用multi I-bit或Granted Users列表；alias为may。

规范强度：主体shall；alias may；原speaker继续与接收分组为NOTE。

依据：3GPP TS 24.380 V19.1.0 §6.3.6.3.2，印刷页 106、107。

## 第二路RTP有独立计时与接收策略

适用主体：D仲裁逻辑。

状态：D: Floor Taken。

适用条件：媒体分发器指示收到overriding MCPTT client的RTP。

若T12未运行则启动；重启T11；请求分发器将新路RTP转给相关non-controlling function、overridden MCPTT client，以及按本地策略接收该overriding客户端的受控参与者，保持D: Floor Taken。NOTE引用23.379的override同时接收上限N7；本页不提供数值或协商算法。

- T12从媒体指示事件而非Granted即开始运行；不把Duration字段当已运行证据。
- 安全页的33.180多发言者媒体保护/混音条件不直接作为本双话权分发实现，未作跨版本互通验证。
- overridden客户端是step3单列的接收者，不以它同时属于一般策略选择集合为附加条件。

规范强度：shall；推论明确限于本条事件。

依据：3GPP TS 24.380 V19.1.0 §6.3.6.3.5，印刷页 109。

## 已获准接口转交请求，但未明确选择 G 或 D

共同接纳条件已建立 D；本条只观察同一 overriding 参与者的服务端接口；另排除 system call。 状态为先 U: not permitted and Floor Taken，后 U: permitted。

初次 Granted 的 G-bit=1 时，接口保存 overriding without revoke 指示并进入 U: permitted；该状态收到关联参与者的 Floor Request 后，将请求转交仲裁逻辑并保持状态。§6.3.5.5.7未明确写选择 G 或 D，不能仅凭保存的角色指示宣称请求路由已闭合。

- §6.3.5.5.7在请求事件下还列媒体动作：step1后b指向§6.3.4.4.5；存有overriding指示时step2要求转发RTP并指向§6.3.6.3.5。保留该事件/动作组合，不把它搬到相邻RTP条款或称为已视觉确认的排版错误。
- 所引G媒体过程会按条件启动T2、重启T1、停止T20；D媒体过程会按条件启动T12、重启T11。因此不能将D请求handler未列计时动作扩大为整个接口链绝不影响计时器。
- 初次Granted的接口Ack请求位是MAY；本条不把其处理复制成U: permitted下重发Granted的完整回程。

依据：TS24.380 V19.1.0 §6.3.5.4.9;6.3.5.5.7;6.3.5.5.6，印刷页91、92、95。 媒体调用对照§6.3.4.4.5、§6.3.6.3.5，印刷页65、109。

## D对同一获准者再次请求的回应

共同接纳条件已建立 D，D仍服务该overriding参与者；另排除system call；来自已获准发送overriding媒体者的Floor Request已经到达D。 状态为D: Floor Taken。

D须向此前获准的参与者再发Granted：Duration带T12值，Floor priority带已授予优先级；本次Request有Track Info时带回本次收到的值，随后保持D: Floor Taken。这个入口按已有许可身份判断，不要求先证明报文逐字重复，也不据本次priority重新授予。

- §6.3.6.3.7未列启动/重启T11或T12、重建D、重新分配audio SSRC或重发Idle/Taken；不等于完整接口调用链无任何媒体计时动作。T12 value不解释为未核的剩余时长或重新给满额时长。
- 本handler未明列G-bit或Audio SSRC字段，不能照搬初次进入D的字段清单，也不能由未列反推字段禁止存在或默认值。
- 本次无Track Info时不能从本handler推定回填旧保存值；也未列替换所存dual Track Info。
- 其他用户、原overridden用户及尚未获准请求不满足本入口；本页不推定它们全部丢弃、全部拒绝或进入第二个D。初次授予、G自身重请求及排队各有独立入口。

依据：TS24.380 V19.1.0 §6.3.6.3.7;6.3.6.3.2;6.3.6.3.1，印刷页110、106、107。

## 条款差异与解释边界

§6.3.6.3.2 step2 NOTE1，印刷页 106：non-controlling说明收到Taken G=1时发Idle，与主控step2发Idle并列，不把note当已核非主控完整caller。

## 未覆盖的行为

- 有限server D状态用途；不代表完整双话权、配置、安全或终端状态机已闭合。
- 原主路的三个有限退出入口与 Terminate 接续见配套退出主题；完整媒体交接与主副路状态迁移仍未闭合。
- 同一overriding参与者再次请求的D回应已列；接口到G/D的选择与重发Granted完整回程仍未闭合。call release的D两阶段区别见配套退出主题，完整信令层释放未覆盖。
- 端到端G-bit/Ack路由与终端停发确认（不排除配套退出主题已核的条件Ack生成）
- 23.379 N7及接收分组配置字段
- 端到端加解密、混音、首包/首音验收

## 按需继续

- [双话权：第二路停止与原主路退出后的接续](dual-floor-stop-evidence.md)
- [优先请求：何时触发撤销，为什么队首仍不等于获权](floor-preemption-decision.md)
- [撤销传递：服务端宽限、终端停止请求与交接证据](floor-revoke-observation.md)
- [多发言者与预配置重组：服务器混音和组密钥前提](../security/group-call-media-boundaries.md)

[3GPP TS 24.380 V19.1.0，ETSI 官方发布版](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅适用于所列版本和条款。
