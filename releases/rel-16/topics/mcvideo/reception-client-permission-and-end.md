# 在网 MCVideo 接收客户端：通知、接收许可与结束

## 适用条件

- 固定 TS24.581 V16.9.0，信令入口限 TS24.281 V16.12.0。范围为普通在网、带传输控制、按需一对一私呼的客户端接收控制职责；不含组呼、广播、系统/紧急/危急、ambient、远程推拉、离网、MBMS 或接收覆盖仲裁。
- 本次会话使用协商的媒体控制通道，适用的信令准入和媒体保护义务仍须执行。各条分别按实际角色、状态与事件适用，不把已经获准接收、收到 RTP、结束成功或所有事件均发生作为共同前提。
- 本页从已证明的呼叫建立、接收通知、用户请求及结束事件说明客户端职责。Reception Mode 只按实际收到的字段处理；不推导普通私呼服务器怎样从配置选择该字段，也不把 SIP Auto/Manual 应答模式等同于接收模式。

## 呼叫建立、对方传输通知与本方接收许可分开

**适用事件：** 替代事件：普通主叫实际收到 INVITE 的 SIP 200；普通终接客户端经适用应答过程发送该 200；或已处于 U: reception controller 收到服务器 Media Transmission Notification。通知事件不要求此前已获本方接收许可。

主叫和终接方分别在上述建立事件创建 general reception control 实例并进入 U: reception controller。每个呼叫保持一个 general 实例。收到传输通知时，若 subtype 首位为 1 则须 Ack（过程列 Message Type=6、Source=0），通知用户并保存发送者 User ID 和 SSRC；可显示媒体详情。若实际 Reception Mode=0，则创建 basic reception control 实例，映射已存发送者身份并令该 basic 实例进入 U: has permission to receive。general 实例仍保持 reception controller；Mode=1 不自动授予接收许可。

**强度：** 实例、状态、通知、保存与条件性 Ack 为 SHALL；媒体详情展示为 MAY；建立时点来自 NOTE。

- 普通主叫的媒体调用来自 §10.2.2.2.1 的 INVITE 200 处理；终接方由 §10.2.2.2.2 的实际模式入口进入 Auto helper，Manual 在发送最终 200 时调用同一 helper。安全、资源及模式选择仍由信令入口负责。
- 通知说明另一用户的媒体传输，Mode=0 的接收许可来自该字段分支，不来自对方 Transmission Granted 或本方 SIP 200。Mode=1 不表示永久拒绝，仍可进入用户请求。
- 服务器组呼模式选择 §6.3.6.3.3 不能用于补普通私呼的 AutoReceive 配置或 Reception Mode 生成算法；本页未闭合该配置到字段的链。
- 接收许可不证明 RTP 已到达或画面已呈现。basic 实例按请求/对应发送者映射，不能将单个源许可扩成所有媒体许可。

依据：3gpp-ts-24.581-v16.9.0 §6.2.5.1–2.3, 6.2.5.3.1–2, 9.2.3.21, 9.2.13, 6.3.6.3.3 (group-mode comparison only), 6.3.7.3.3 (server notification comparison only)，印刷页 44, 45, 46, 86, 87, 95, 96, 156, 157, 167, 168；3gpp-ts-24.281-v16.12.0 §10.2.2.1, 10.2.2.2.1 INVITE200 paragraph, 10.2.2.2.2 steps1–8, 6.2.3.1.1 steps8–10, 6.2.3.2.1 final200 paragraph，印刷页 44, 45, 267, 269, 270, 271。

## 请求获准之后还要区分媒体到达

**适用事件：** 替代事件：general reception controller 中用户请求接收已保存 User ID/SSRC 对应的媒体；该 basic 实例在 U: pending request to receive 收到响应或 T103 到期；或该 basic 实例已在 U: has permission to receive 收到服务器关于源编码视频到达的指示。只取普通接收优先级。

用户请求时发送 Receive Media Request，创建 basic 实例并映射发送者，general 实例保持原状态；basic 进入 pending request to receive 时启动 T103、C103 置 1。拒绝响应须按 subtype 首位为 1 的守卫 Ack（过程列 Type=7、Source=0），通知拒绝，可显示 Reject Cause，停 T103 后进入 terminated。T103 未达 C103 上限时重发请求、重启计时器、计数加 1；到上限则通知超时并 terminated。获准响应按同一守卫 Ack，通知接收成功，停 T103 并进入 has permission to receive。在该状态，另收到服务器关于源编码视频到达的指示时才按该事件接收视频并保持状态。

**强度：** 所述请求、响应处理、通知、计时及接收动作为 SHALL；拒绝原因展示为 MAY；重传总时段限制为 NOTE 中 SHOULD。

- §9.2.3.17 的 Result=0/1 分别表示接收未获准/获准。§9.2.14 开头却用 permission to send 描述 Receive Media Request，和接收过程、消息字段用途不一致；不据此把该请求改成传输授权。
- §6.2.5.4.3–4 用 C103 判断 T103 重试及上限；§11.1.1 的 T103 表在到限句写 C105。保留该差异，不合成新的计数算法。T103 取配置，NOTE3 建议总重传时段小于 6 秒，并非单次固定 6 秒；C103 表默认值为 3。
- 请求的头 SSRC 标识请求者，所请求媒体的发送者 SSRC 是另一个字段；响应头 SSRC 标识服务器。不能用响应者身份替换媒体源映射。
- 非普通 Reception Priority 的协商算法不在本页；过程回指 §14.3.3，而该节标题及内容为 mc_priority。§6.2.5.5.2 未定义呈现完成或媒体混合实现，不能以接收成功提示作为画面已显示的证据。

依据：3gpp-ts-24.581-v16.9.0 §6.2.5.1 Figure6.2.5.1-2, 6.2.5.3.3, 6.2.5.4.1–5, 6.2.5.5.1–2, 9.2.3.16–19, 9.2.14–15, 11.1.1 T103 and NOTE3, 11.2.1 C103, 14.3.3 (priority-reference comparison only)，印刷页 45, 47, 48, 49, 154, 155, 156, 169, 170, 171, 201, 202, 211, 225。

## 用户取消或结束接收有独立待响应状态

**适用事件：** 替代事件：pending request to receive 中用户取消；has permission to receive 中用户结束接收，即使尚未收到媒体；或 pending reception release 中 T104 到期或收到 Media Reception End Response。

取消或结束时发送带媒体发送者 SSRC 的 Media Reception End Request；若存有 overriding/overridden without revoke 指示则分别移除。取消待请求还须停止 T103。两入口均启动 T104、C104 置 1 并进入 pending reception release。此状态下 T104 未达 C104 上限则重发、重启、计数加 1；到上限则进入 terminated。收到 MRE Response 时，若 subtype 首位为 1 则 Ack（过程列 Type=3、Source=0），可通知用户接收结束，停 T104 并 terminated。进入 terminated 删除该 basic 实例。

**强度：** 发送、清理、计时、状态、条件性 Ack 为 SHALL；结束通知为 MAY；重传总时段限制为 NOTE 中 SHOULD。

- 单个 basic 实例结束不等于普通私呼 general 实例或 SIP 会话已释放。T104 本地到限也不是服务器确认成功。
- 用户结束步骤未另列立即丢弃 RTP 缓存/停止显示；不可移植服务器 MRE 命令的显式停止步骤，也不能反推必须继续显示。
- T104 取配置，NOTE4 建议总重传时段小于 6 秒，C104 默认值为 3。仅继承实际存储指示的条件性清理，不在本页扩写 override 仲裁或广播专用分支。

依据：3gpp-ts-24.581-v16.9.0 §6.2.5.4.6, 6.2.5.5.1;6.2.5.5.3, 6.2.5.6.1–4, 6.2.5.8.1, 9.2.26–27, 11.1.1 T104 and NOTE4, 11.2.1 C104，印刷页 48, 49, 50, 51, 176, 177, 178, 202, 211。

## 服务器接收结束命令、传输结束通知与通话释放不同

**适用事件：** 替代事件：basic has permission to receive 收到服务器 MRE Request；general reception controller 收到 Transmission End Notify；general reception controller 收到应用与信令面的 call release step1；或 general Call releasing 收到应用与信令面的 step2。

收到服务器 MRE Request 时，按首位为 1 的守卫发送 Reception control Ack（过程列 Type=2、Source=0、Message Name=MCV2），通知接收正在结束，可说明原因，要求丢弃剩余 RTP 缓存并停止显示，发送 MRE Response，可通知用户结束并 terminated。与此不同，general 收到 Transmission End Notify 只通知另一用户结束传输并保持状态。call release step1 则停止接收控制消息、要求停止接收 RTP 并进入 Call releasing；step2 释放含运行计时器的全部呼叫资源、终止全部 basic 实例，并回到 Start-stop 终止 general 实例。

**强度：** 正文所列发送、状态、通知及计时动作按 SHALL；明确写可显示原因或可通知的动作为 MAY。

- §6.2.5.5.5 的 Ack 守卫回指 §8.3.2；本版第8章只有 Communication release media plane procedures 标题，随后即第9章。公开保留回指，不暗改成消息编码条款。
- §9.2.3.10 对 Message Type 给出含 subtype 首位的通用编码说明，过程列固定 Type 值；§9.2.31 规定 Ack 字段。本页保留过程数值，不提供解决差异的完整编码器。
- 格式错误消息不改变状态；当前状态没有相应处理程序的接收控制消息/RTP 要丢弃并保持状态，不能以晚到 Granted 跨越 pending release 或恢复已终止实例。
- 本页登记媒体接收控制的释放接口，不证明完整 SIP BYE 生命周期、网络交付、解码或呈现质量。

依据：3gpp-ts-24.581-v16.9.0 §6.2.5.1 unmatched/malformed rule, 6.2.5.3.4–5, 6.2.5.5.5, 6.2.5.8.1;6.2.5.9.1–2, 8 heading and following9 (reference comparison), 9.2.2.1, 9.2.3.10;9.2.3.18, 9.2.26–27;9.2.31，印刷页 45, 47, 50, 51, 52, 142, 145, 146, 151, 155, 176, 177, 178, 180, 181。

## 边界与关联

- 不实现普通私呼 AutoReceive 配置到 Reception Mode 的选择，也不借组模式补齐；不覆盖服务端接收仲裁、非普通优先级或覆盖策略。
- 保护/密钥、完整报文编码、SIP 生命周期、媒体混合与呈现实现仍是独立依赖。
- 实际私呼准入与应答先看[私呼客户端](private-client-answer-evidence.md)，但本页不把所有接收事件改成重新应答邀请。
- [传输请求与获准](transmission-client-request-grant-end.md)只解释发送侧职责，不能替代本页接收许可。

背景依据：3gpp-ts-24.581-v16.9.0 §4.3 (negotiated channel background),5.2.1–2 (client role),13.3.3 (private media/control protection background) pp30,31,32,220; 3gpp-ts-24.281-v16.12.0 §6.2.1–2 (SDP control channel background) pp42,43,44
