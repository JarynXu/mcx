# 普通离网MCPTT私呼：已建呼叫的释放与本地清理

固定ETSI TS124379 V19.4.0，对应3GPP TS24.379 V19.4.0 Release19；仅两个已确定用户的普通自动应答离网私呼，在各条指定状态下处理已建呼叫的用户释放及正常确认。不是在网SIP、手动等待、紧急升级、建立取消或丢包重传算法。

所存呼叫身份与传输条件已经具备；消息发送仍依赖§11.2.1.1.1。该条接收文字的port TBD/8809 messages问题见建立主题，不能用MCVideo修补。完整安全、媒体和话权内部行为不在本页覆盖。

各条入口成立时，以下动作是规范要求。

## 请求释放先进入等待，不立即清除呼叫

普通自动离网私呼的MCPTT客户端基本控制处于P4，收到本用户释放该私呼的指示。

生成PRIVATE CALL RELEASE，Call identifier、caller和callee的MCPTT user ID分别使用所存值，按§11.2.1.1.1发送；随后停止TFP5，将CFP3初始化为1，启动TFP3，进入P3。

该入口没有把用户限定为原发起用户，也没有列立即终止媒体；不能将发出RELEASE等同于已完成本地清理。原文发送步骤使用“in response to the request message”措辞，本入口仍是用户指示，不另造收到请求的前提。

依据：TS24.379 V19.4.0 §11.2.2.4.5.1，印刷页525,526。

## 收请求与收确认分别完成本地清理

分别观察基本控制P4收到PRIVATE CALL RELEASE，或由用户释放进入P3后收到对PRIVATE CALL RELEASE的PRIVATE CALL RELEASE ACK；后续P1清标识另以TFP7到期为触发。

P4收RELEASE时，先生成ACK并以所存call identifier、caller ID、callee ID填字段，按§11.2.1.1.1回复；再终止私呼媒体、停止TFP5、启动TFP7、释放call-type控制状态机、进入P1。P3收对应ACK时，停止运行中的TFP3，再终止媒体、启动TFP7、释放call-type控制状态机并进入P1。P1中TFP7到期才清除所存call identifier并进入P0。

收到RELEASE的本条入口未另列发送者角色或call identifier相等校验，不能据此推定任意消息有效；完整分派、鉴权和报文编码不在此核验。ACK先于接收方媒体终止，不能把ACK的发送时刻当作全部资源已经回收。

依据：TS24.379 V19.4.0 §11.2.2.4.5.4;11.2.2.4.5.5;11.2.2.4.5.7，印刷页526,527。

## Q1清理类型字段不等于基本控制已结束

类型控制处于Q1，收到MCPTT用户释放呼叫的指示，或收到PRIVATE CALL RELEASE。基本控制的P状态不替代这一Q1前提。

释放所存current call type，停止运行中的TFP6，释放所存ProSe per-packet priority，然后进入Q0。该类型状态机与基本控制并行；Q1自己的转换与基本控制释放call-type状态机是不同动作。

不推断两个状态机的调度顺序、原子清理或强制共享快照；Q0不是媒体已终止的证明。该Q1入口没有把RELEASE ACK列为触发。基本控制P4也不能单独证明类型控制必在Q1。

依据：TS24.379 V19.4.0 §11.2.3.1;11.2.3.4.7，印刷页528,536。

## 边界与关联

TFP3到期重传及达上限失败、TFP5最大时长出口另有条款，不属于本页正常确认分支；不承诺释放请求一定送达或最终双方一致结束。

本页列媒体终止的控制要求，不展开TS24.380内部话权清理；也不以旧版本普通组话权说明补全私呼。

TFP3重传与达上限出口的入口有重叠，本页不补执行优先级。建立时的P/Q条件见[自动私呼控制](offnetwork-private-auto-control.md)；[在网释放](release-signalling.md)使用不同信令，不能替代这里的MONP流程。

来源：[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
