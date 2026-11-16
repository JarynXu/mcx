# MCPC Connect：本地占用、终接接受与下游结果

TS24.380 V19.1.0（ETSI 2026-01），独立于关联主题使用的 TS24.379 V19.4.0。

在网MCPTT预建立会话的第9章状态机；每个预建立会话一个实例，以下conditions须同时满足；不是所有MCPTT调用的统一状态机。

## REFER 响应只证明本地占用

适用条件：客户端处于U: Pre-established session not in use，收到为发起预安排/adhoc/private呼叫或加入chat而发送的REFER的2xx。

创建6.2.4话权参与者状态机，进入U: Pre-established session in use。这是本地媒体控制状态迁移，不等于控制功能已接受下游业务INVITE或被叫已接听；不能把既有REFER200边界误写为客户端此时完全不改变状态。

依据：§9.2.2.3.5，印刷页 220、221。

## 向发起端传达控制侧结果

适用条件：参与功能处于G: Pre-established session in use，收到控制功能的业务SIP200。

向发起客户端发Connect：会话身份取200 Contact；有session-type则映射类型，无则no session type；有Warning warn-code=399则携其warn-text；有P-Answer-State则携对应Answer State；有mcptt-called-party-id则携Invited MCPTT User Identity。SHOULD要求确认，启动T55并将C55加1，仍在in use。Connect将下游结果传给客户端，但没有Answer State不能自造Confirmed，Connect也不能等同话权授予。

依据：§9.3.2.4.10，印刷页 227、228。

## 已占用客户端收到 Connect

适用条件：客户端已在U: Pre-established session in use，收到Connect。

若确认标志置1则回Acknowledge Reason Code=Accepted，保持in use。本条不是重新执行空闲状态的用户接受/拒绝分支，因此此Ack不能一律解释为用户刚完成接听动作。

依据：§9.2.2.4.2，印刷页 221。

## 空闲终接的自动应答分支

适用条件：参与功能处于G:not in use，收到控制功能INVITE且处于automatic answer mode。

向受邀客户端发Connect，要求确认，启动T55并将C55初始化1，按需预留媒体资源。其会话身份取INVITE Contact；组呼类型及组ID按正文映射，邀请者身份不可得或需隐私时用anonymous@anonymous.invalid；Media Streams在预建立协商流多于本呼叫需要时加入。此分支前提不能省略为任何终接都用Connect。 进入 G: Pre-established session in use。若 session-type=private 且 INVITE 带 MIKEY-SAKKE I_MESSAGE，还须将其原样放入 PCK I_MESSAGE 字段；本页不据此省略私呼密钥处理。

依据：§9.3.2.3.3，印刷页 223、224。

## 空闲客户端接受或拒绝

适用条件：客户端在U:not in use收到Connect。

若接受呼叫，必须回Accepted Ack；Connect含Media Streams时只使用其中指明的流，创建话权状态机并进入in use。否则回带合适原因的Ack并保持not in use。这里Ack是该客户端接受/拒绝分支证据，仍不是全组所有用户已接听或已取得话权。

依据：§9.2.2.3.2，印刷页 220。

## Connect 确认与 T55 超时

适用条件：参与功能在G:in use收到Connect相关Ack，或T55到期。

收到Ack先停止T55；非Accepted则发Disconnect并带对应Reason Cause，启动T56/C56=1、向控制功能发释放指示，进入Call releasing；Accepted则在此前尚未发送时发业务INVITE200并保持in use。T55到期且C55未达上限时重发Connect、重启并C55加1；T55到期且C55已达上限时向控制功能发释放指示，可释放非预建立所需资源并返回not in use。超时返回不是客户端确认成功。

依据：§9.3.2.4.7–9，印刷页 226、227。

## 证据边界

- 24.380第9章与24.379不同精确版本仅作有条件关联，不宣称完整互操作验收。
- 未核8.3字段二进制编码、T55/T56默认值和C55/C56配置值、全部话权机以及认证/密钥链，不能交付完整实现。
- 9.3.2.4.10只写C55加1，本研究未补造发起侧初始化位置。
- 9.3.2.4.11失败分支引用先前Connect会话身份存在证据缺口，保留为未核依赖。
- 客户端UI何时显示接通/失败与所有媒体实际可用并非本批证明范围；主叫收到Connect、终接Ack、话权获得分别判断。

## 按需继续

- [mcpc-disconnect-evidence](mcpc-disconnect-evidence.md)
- [preestablished-group-association](preestablished-group-association.md)
- [group-terminating-responses](group-terminating-responses.md)
- [floor-participant-entry-request](floor-participant-entry-request.md)

[ETSI 官方 TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅所列版本和条款。
