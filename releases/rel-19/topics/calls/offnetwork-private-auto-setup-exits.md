# 普通自动离网MCPTT私呼：建立等待中的重传、失败与取消

ETSI TS124379 V19.4.0，对应3GPP TS24.379 V19.4.0 Release19 Stage3；仅普通PRIVATE CALL、自动应答、已确定双用户的离网私呼发起端。已满足授权和模式配置并发送建立请求，所存身份、offer及类型值可用。

只解释基本控制P2的重传、无响应上限、收到拒绝和用户取消入口。不覆盖手动应答、紧急升级、终接P5失败、取消的对端处理及P3重传算法。消息传输仍依赖§11.2.1.1.1，完整安全、媒体和话权实现未核。

基本控制与类型控制并行，按各自实际状态和事件处理；本页的释放call-type状态机动作不等于另行声称某个Q状态转换，不设定跨机调度或原子性。

条件成立后，以下列明动作是规范要求；本地位置更新另为可选。

## 未到上限重传，达到上限退出等待

发起MCPTT客户端基本控制处于P2，TFP1到期；所存模式为AUTOMATIC COMMENCEMENT MODE。分别处理CFP1小于上限或等于上限。

CFP1小于上限时，可更新所存本地用户位置，然后将CFP1加1；生成PRIVATE CALL SETUP REQUEST，以所存call identifier、caller ID、callee ID、模式、类型机当前类型及offer SDP填写相应字段，按§11.2.1.1.1发往另一客户端，启动TFP1并保持P2。CFP1等于上限时，启动TFP7、释放call-type控制状态机，然后进入P1。

本地位置可更新不等于普通私呼可发送User location IE；该发送许可限定EMERGENCY PRIVATE CALL，不用于本页普通类型。上限数值、计时参数及CFP1大于上限的行为未在此补齐。 自动模式达上限出口不启动手动模式的TFP9，也未列发送RELEASE。

依据：TS24.379 V19.4.0 §11.2.2.4.2.2;11.2.2.4.2.4，印刷页516,517。

## 拒绝响应必须对应所存呼叫

发起MCPTT客户端基本控制处于P2，收到回应PRIVATE CALL SETUP REQUEST的PRIVATE CALL REJECT，且其Call identifier IE等于所存call identifier。

依次停止运行中的TFP1、停止运行中的TFP9、启动TFP7、释放call-type控制状态机，进入P1。

本条未以Reason值区分这些退出动作；不同call identifier的REJECT不满足本入口，不能套用本条清理。完整分派和鉴权不在此证明。

依据：TS24.379 V19.4.0 §11.2.2.4.2.7，印刷页517。

## 用户取消发送RELEASE后等待响应

发起MCPTT客户端基本控制处于P2，收到MCPTT用户取消该私呼请求的指示。

生成PRIVATE CALL RELEASE，以所存call identifier、caller ID和callee ID填相应字段，按§11.2.1.1.1发送；停止TFP1、停止TFP9，启动TFP3，然后将CFP3初始化为1，进入P3。

本条停止TFP1/TFP9未附if running，不能替换成拒绝响应的条件式停止。原文先启动TFP3再初始化CFP3，不套用已建呼叫释放的步骤次序。 这只是取消发起端的请求与等待入口，不证明自动终接端已处理RELEASE；不将手动模式§11.2.2.4.4.8扩为自动P5规则。本条未列终止媒体或释放类型机，不能补成取消即全部清理。

依据：TS24.379 V19.4.0 §11.2.2.4.2.9，印刷页518。

## 后续边界

进入P1不等于立即清除call identifier；后续TFP7清标识规则是另一个状态入口。取消到P3也不等于已经收到释放确认。

TFP1/CFP1重传与自动上限出口有明确的小于/等于划分，不将这一守卫移植到其他计时器。终接P5的一般重传与上限失败入口另有重叠，此处不裁定其执行优先级。

[自动建立](offnetwork-private-auto-control.md)说明成功入口；[已建呼叫释放](offnetwork-private-release.md)以已建呼叫为场景，不能把该页共同条件直接套到建立取消。P/Q并行依据§11.2.3.1（p528）。

来源：[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
