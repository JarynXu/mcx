# 离网MCPTT普通组呼合并：选择另一呼叫与本地切换

固定ETSI发布的TS124379 V19.4.0，对应3GPP TS24.379 V19.4.0 Release19 Stage3；仅普通离网MCPTT BASIC GROUP CALL到BASIC GROUP CALL的有限合并，不是MCVideo。

已具备该组合法使用条件、承载及配置；不处理广播、紧急/迫近危险升级、网关、安全或发现。各端按本地基本控制S3和类型控制T2的对应事件判断，不把两种状态机当成同一个状态。

探测、用户应答、本地退出与参与中合并是不同入口，按各自状态、事件及条件读取。所有媒体/话权调用只到接口，不引入在网服务器仲裁。

满足各自守卫时，下面列出的过程动作是规范要求。

## 同组之外还要比较呼叫身份和起始时间

MCPTT客户端基本控制处于S3，收到普通BASIC GROUP CALL公告；本地当前类型也是BASIC GROUP CALL。

普通合并的完整选择条件是：组ID相同 AND（发起用户ID不同 OR call identifier不同）AND（公告start time较早 OR（start time相等 AND公告call identifier较小））。发起用户ID只参与是否另一呼叫的判断，不是最后的大小排序项。条件不成立只能说未命中此合并分支，不能据此裁定其他公告处理也不存在。

不能只凭同组或更小call ID合并；类型升级分支不在此范围。不同组即使时间更早也不满足本条。

依据：TS24.379 V19.4.0 §10.2.2.4.6.1，印刷页393。

## 按所选公告切换本地呼叫记录和话权入口

MCPTT客户端基本控制处于S3；收到GROUP CALL ANNOUNCEMENT，其MCPTT group ID等于所存组ID，且Originating MCPTT user ID或Call identifier至少一项不同于所存值；本地当前类型与公告类型均为BASIC GROUP CALL。以上条件同时成立，且还满足以下二者之一：公告Call start time较早；公告Call start time等于所存值且公告Call identifier较小。

客户端依次保存公告的SDP、Call identifier、Originating MCPTT user ID、Refresh interval及Call start time，按所存SDP调整媒体，并以terminating floor participant重启floor control，调用TS24.380 §7.2。随后停止TFG6并按§10.2.2.4.1.2重启，停止TFG2并按§10.2.2.4.1.1.1重启，最后保持S3。TFG6为MaxDuration−(当前UTC秒−公告Call start time)，UTC以1970-01-01起算且不计闰秒；这里使用触发合并计算的公告时间。周期TFG2为所存refresh interval×(2/3+2X/3)秒，每次计算X均匀抽自0至1。

两个stop没有if running限定，不自行加上。最大时长不是合并后重新取得完整配置时长；配置缺省值、负值和时钟异常未核。 TS24.380 §7.2仅为24.379中的依赖引用，内部话权流程及许可未核，不证明旧话权延续、新话权取得或声音送达。

依据：TS24.379 V19.4.0 §10.2.2.4.6.1;10.2.2.4.1.2;10.2.2.4.1.1.1，印刷页393,384,385。

## 类型控制独立保存公告中的类型信息

MCPTT客户端类型控制处于T2；收到GROUP CALL ANNOUNCEMENT，其MCPTT group ID等于所存组ID，且Originating MCPTT user ID或Call identifier至少一项不同于所存值；本地当前类型与公告类型均为BASIC GROUP CALL。以上条件同时成立，且还满足以下二者之一：公告Call start time较早；公告Call start time等于所存值且公告Call identifier较小。

类型控制依次保存公告的Last call type change time、Last user to change call type和Call type。此处普通BASIC分支没有另列ProSe优先级重设或重新进入T2的动作；该条后续重设优先级、计时及状态转换分别受EMERGENCY或IMMINENT PERIL类型条件约束，不能搬给BASIC。

本条不能省略自己的身份和排序守卫，也不能把前一过程已处理过公告当成本条必然成立。

依据：TS24.379 V19.4.0 §10.2.3.4.9，印刷页406,407。

## 本地合并不是同一呼叫任意改SDP，也不保证全网收敛

MCPTT客户端在上述普通合并范围中比较基本控制与并行类型控制的处理；或判断合并对原有固定SDP规则的适用范围。

§10.2.2.1规定本版同一离网组呼期间SDP保持不变、媒体流不能修改；§10.2.2.4.6.1则在另一呼叫公告满足合并守卫时，要求保存所选公告SDP并调整本地媒体。这里区分持续参与同一呼叫与采用被选中另一呼叫的描述，不据此允许任意会话内重协商。§10.2.3.1说明类型控制与基本控制并行存在。两处合并过程各自检查守卫；基本过程更新所存call ID、发起者等比较值后，另一过程如何取得其判定所需值，这些条款没有给出跨状态机调度顺序。不能补成强制旧值快照、原子事务或先基本后类型的实现规则。

此为局部条件过程，未证明所有UE均收到相同公告、最终选中唯一呼叫、完成同步切换或无媒体间断。 start time和call ID均相等但发起者不同时，身份差异守卫虽成立，普通排序守卫仍不成立；不能创造发起者ID排序来保证收敛。

依据：TS24.379 V19.4.0 §10.2.2.1;10.2.2.4.6.1;10.2.3.1;10.2.3.4.9，印刷页382,393,394,406,407。

## 关联范围

[探测与建立](offnetwork-group-probe-and-start.md)、[用户应答与周期公告](offnetwork-group-acceptance-and-announcement.md)、[本地离开](offnetwork-group-local-leave.md)各自保留原适用条件，不自动成为合并的前后步骤。

来源：[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。仅局部过程，话权内部及全网收敛未核。
