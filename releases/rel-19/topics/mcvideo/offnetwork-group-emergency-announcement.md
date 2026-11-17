# 离网组呼：BASIC参与者收到紧急类型公告

## 共同条件

- 固定TS24.281 V19.3.0 Rel19 Stage3；只取已参与离网组呼、类型控制处于T2且保存类型为BASIC的客户端收到紧急类型公告。
- 基本呼叫机与类型控制机分别判断；不纳入初建T0、不同call合并、广播、在网、降级或紧急告警。T1或T3的其他接收入口不在本页。
- 身份、安全、配置及承载前提仍须满足；24.483配置schema、优先级数值及24.581媒体细节未核，不把本地类型更新视为全组同步或媒体许可。

## 改变者身份决定时间守卫

适用主体：已参与离网组呼的MCVideo客户端类型控制器。

适用条件：本地T2且stored call type=BASIC GROUP CALL，实际收到GROUP CALL ANNOUNCEMENT；公告MCVideo group ID与当前组一致，Call Identifier与已存call identifier相同，Call type为EMERGENCY GROUP CALL。
适用条件：最后改变者相同时，还须已存last call type change time严格小于公告对应时间；最后改变者不同时，按step2b独立判断，不继承step1或step2a的时间比较。

改变者相同且时间更新的分支，先保存公告的最后类型变化时间，再把当前类型改为紧急类型、设置相应离网紧急ProSe逐包优先级，停止运行中的TFG14，按§9.3.3.4.1.1启动TFG13并进入T1。改变者不同的紧急公告分支先保存公告的时间及最后改变者，然后执行同样的类型、优先级、计时和T1动作；step2b没有要求公告时间比本地新。因此不能给所有紧急公告统一添加“时间更新才接受”的规则。

规范强度：适用守卫成立后的列明动作SHALL；不同改变者分支不添加原文未列的时间守卫。

- 同改变者且时间相同或更旧不满足本条step1；不据此补造整套丢弃、错误响应或其它状态行为。
- Last user to change call type是类型变化者字段，不是UDP发送者或Originating MCVideo user ID的同义替换。
- step2a的同类型且时间更新是另一分支；本页BASIC收到EMERGENCY不满足同类型，不能把2a的时间条件借给2b。
- TFG13只保留精确helper调用，计时计算、配置取值和过期处理不在本页新增验证；不能声称从收到公告开始重新获得完整配置时长。
- 本条没有新增公告转发、确认、修改基本机SDP/call ID或告警状态的动作；仅证明本地类型控制按条件更新，不证明所有组员已更新。

依据：[TS24.281 V19.3.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf) §9.3.3.4.7.2 opening,step1a–b,step2 opening and2b;step2a contrast，印刷页313–314。

## 证据边界

仅BASIC在会接收紧急公告的两种改变者分支，不是全部类型协调协议。
