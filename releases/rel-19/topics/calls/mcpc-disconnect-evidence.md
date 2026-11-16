# MCPC Disconnect：失败通知、释放确认与预建立保留

TS24.380 V19.1.0（ETSI 2026-01），独立于关联主题使用的 TS24.379 V19.4.0。

在网MCPTT预建立会话的第9章状态机；每个预建立会话一个实例，以下conditions须同时满足；不是所有MCPTT调用的统一状态机。

## 失败建呼后的 Disconnect

适用条件：参与功能在G:in use收到控制功能的失败建呼指示。

向客户端发Disconnect，SHOULD要求确认，启动T56/C56=1，终止呼叫并进入G:Call releasing。原文要求会话身份与建呼Connect中相同，但失败可能尚无先前Connect；此先前值来源未闭合，不能自造字段。本条未规定Reason Cause或SIP失败码映射，不能移植非Accepted Ack分支的原因映射，也不能反推禁止携带该字段。

依据：§9.3.2.4.11，印刷页 228。

## 控制侧释放并保留预建立承载

适用条件：参与功能在G:in use收到控制功能释放呼叫指示。

停止仍运行的T55，发Disconnect，其会话身份与建呼Connect相同，SHOULD要求确认；启动T56、初始化C56=1并进入Call releasing。状态含义是释放业务同时保留预建立会话。

依据：§9.3.2.4.5;9.3.2.5.1，印刷页 226、228。

## 客户端断开与真正停止承载

适用条件：分别判断客户端在U:in use收到Disconnect、U:not in use收到Disconnect，或U:not in use收到预建立会话停止指示。

U:in use收到Disconnect，确认标志为1时回Accepted Ack，进入U:not in use并执行6.2.4相关动作。若本来就在U:not in use收到Disconnect，则条件性确认后保持该状态。另一个不同事件是U:not in use收到预建立会话停止指示，此时释放资源/计时器并进入Start-stop；不将该条推广到任意客户端状态。

依据：§9.2.2.4.5;9.2.2.3.3–4，印刷页 220、221。

## Ack 与 T56 耗尽的证据不同

适用条件：参与功能处于G:Call releasing。

收到Ack停止T55（若运行）和T56，可释放不为预建立所需的呼叫资源，返回not in use；T56到期且C56未达上限时重传Disconnect、重启并计数加1；T56到期且C56已达上限时也可释放上述资源并返回not in use。两条路径同到空闲，但计数耗尽没有证明客户端收到/确认断开。

依据：§9.3.2.5.2–4，印刷页 228、229。

## 客户端主动释放的反方向路径

适用条件：参与功能在G:in use收到客户端释放业务但保留预建立的指示。

向控制功能发送业务释放，可释放不为预建立所需的呼叫资源，停止T55并返回not in use。此路径不能套成控制侧发来的释放一律先Disconnect并等待Ack。

依据：§9.3.2.4.4，印刷页 226。

## 证据边界

- 24.380第9章与24.379不同精确版本仅作有条件关联，不宣称完整互操作验收。
- 未核8.3字段二进制编码、T55/T56默认值和C55/C56配置值、全部话权机以及认证/密钥链，不能交付完整实现。
- 9.3.2.4.10只写C55加1，本页未补造发起侧初始化位置。
- 9.3.2.4.11失败分支引用先前Connect会话身份存在证据缺口，保留为未核依赖。
- 客户端UI何时显示接通/失败与所有媒体实际可用并非本页证明范围；主叫收到Connect、终接Ack、话权获得分别判断。

## 按需继续

- [mcpc-connect-evidence](mcpc-connect-evidence.md)
- [preestablished-session-lifecycle](preestablished-session-lifecycle.md)
- [chat-participant-release](chat-participant-release.md)
- [floor-participant-queue-release](floor-participant-queue-release.md)

[ETSI 官方 TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅所列版本和条款。
