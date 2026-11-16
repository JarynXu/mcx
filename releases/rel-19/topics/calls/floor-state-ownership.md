# 话权状态归谁：客户端、服务器接口与呼叫仲裁分开读取

限本版第6章在网话权控制；以下是基本状态机职责和选定接口行为，不是完整实现或所有扩展状态机。

需要先确定状态机所有者、关联呼叫/参与者和当前事件，再读取动作；状态字母 U 本身不能识别所有者。

## 三个状态所有者

适用条件：分析一场按协商使用话权控制的 MCPTT 呼叫；需要确定客户端与服务器状态的归属。

客户端 floor participant 使用 §6.2.4 基本状态机（例如 U:has permission、U:queued）。服务器另外有 §6.3.4 的呼叫仲裁 G 状态机，以及 §6.3.5 面向关联参与者的服务器接口 U 状态机（例如 U:permitted、U:not permitted and Floor Taken）。两个 U 不是同一个实例；服务器接口已 permitted 不能单独证明客户端已收到 grant 或完成排队后用户确认。

依据：§6.2.1;6.2.4.9.4;6.2.4.9.12;6.3.1;6.3.5.1。

## 每场呼叫与每个参与者

适用条件：服务器为 MCPTT 呼叫维护话权仲裁及面向参与者的基本接口。

仲裁逻辑每场 MCPTT 呼叫维护一个 general floor control operation 实例；服务器为其服务的每个 floor participant 建立一个 basic floor control operation towards the participant 实例。接口的输入包括仲裁指令、参与者发送的话权消息、媒体，以及某些呼叫处理 SIP 消息。预安排主叫接口在服务器向主叫发送 SIP200 时建立，预安排被叫接口在服务器收到 SIP200 时建立；chat 接口在服务器响应所收初始 INVITE 发出 SIP200 时建立。这些建立事件不是通用的话权授予判据。

依据：§6.3.2.2;6.3.4.1;6.3.5.1。

## 接口不只是转发

适用条件：服务器接口处于 U:not permitted and Floor Idle；分别收到关联参与者的 Floor Request 或 Floor Release。

接口不是透明转发器。Request 在非广播或广播发起者场景转交仲裁；广播非发起者的 Request 由接口发送 Deny，Reject Cause=5（Receive only）。Release 若要求确认则接口回 Ack（Message Type=4，Source=2；有 Track Info 则回带），发送 Floor Idle，并用 Track Info 顶层 Participant Reference 加 SSRC，或无 Track Info 时仅 SSRC，查找并移除该参与者已排队请求，仍留在原接口状态。这一状态的本地处理不能推成所有状态的统一处理。

依据：§6.3.5.3.4;6.3.5.3.7。

## Ack不是统一仲裁事件

适用条件：服务器接口处于 U:not permitted and Floor Idle，收到仲裁给出的 Floor Granted 并按 §6.3.5.3.5 向关联参与者发送。

接口转发 Granted，可设置要求 Ack 的标志，然后进入服务器侧 U:permitted；原文将收到 Ack 的处理及未收到时的动作列为实现选项，不把等待 Ack 列为该转态前提。该条没有规定 Ack 必须交给 G，也没有规定收到 Ack 必停止 G 的 T20。不能把消息确认、服务器许可状态和客户端实际发送/用户确认合为一个完成事件。

依据：§6.3.5.3.5;6.3.5.1。

## 单人退出与整场释放

适用条件：服务器收到呼叫释放相关过程；分别判断仅某客户端离开且其他客户端仍在通话，或整场 MCPTT 呼叫释放。

单人离开时先停止向该客户端发送话权消息/RTP，并丢弃其输入；信令层确定与该参与者的呼叫已释放后，释放其服务器接口实例。整场呼叫释放时先停止向所有参与者发送，信令层确认整场释放后再终止 G 及该呼叫的各服务器接口实例。单参与者退出不能直接等同销毁整场 G；仲裁发起整场释放还依赖 TS24.379 的释放策略。

依据：§6.3.3。

## 证据边界

- 未覆盖 dual floor、multi-talker、audio cut-in、临时组及非控制功能的完整模型。
- 接口分支仅示例性核对选定状态，不把未列出的消息路径视为不存在。
- 状态机职责不规定进程、线程、节点部署、物理黏性或分布式状态同步方案。
- 本主题不证明媒体加密、呼叫准入、媒体到达或用户接听完成。

## 按需继续

- [floor-participant-entry-request](floor-participant-entry-request.md)
- [floor-participant-queue-release](floor-participant-queue-release.md)
- [mcpc-connect-evidence](mcpc-connect-evidence.md)

[ETSI 官方 TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)，印刷页36、52、54、55、56、57、58、76、78、82、83、84；仅本版本。

[仲裁计时器及Ack边界](floor-server-media-timers.md)：仅按该页版本和适用条件衔接。
