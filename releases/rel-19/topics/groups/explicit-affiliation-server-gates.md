# 显式归属服务器公共入口：身份、权限、期限与200的限度

TS24.379 V19.4.0；Stage3。

在网显式affiliation状态发布与状态订阅，区分服务用户和拥有组两种服务器角色。

覆盖建立、刷新与撤销共享门槛；不据输入不符推导未写明的错误码。每条只继承本主题共同条件和自身条件，不继承前条结果。

user_publish：§9.2.2.2.3入口：PUBLISH指向服务该用户的O-PF或T-PF PSI；mcptt-info+xml的mcptt-request-uri标识本服务器服务的用户；P-Asserted-Service为MCPTT ICSI；Event=presence；PIDF为per-user affiliation。

group_publish：§9.2.2.3.3入口：PUBLISH指向组CF PSI；mcptt-info+xml有mcptt-request-uri及mcptt-calling-user-id；P-Asserted-Service为MCPTT ICSI；Event=presence；PIDF为per-group affiliation。

user_subscription：§9.2.2.2.4入口：SUBSCRIBE指向服务该用户的O-PF或T-PF PSI；mcptt-info+xml的mcptt-request-uri标识本服务器服务的用户；P-Asserted-Service为MCPTT ICSI；Event=presence。

group_subscription：§9.2.2.3.4入口：SUBSCRIBE指向组CF PSI；mcptt-info+xml有mcptt-request-uri及mcptt-calling-user-id；P-Asserted-Service为MCPTT ICSI；Event=presence；simple-filter+xml按用户过滤且指定ID与mcptt-calling-user-id一致。

## 身份、修改授权与期限

适用条件：收到符合user_publish入口的请求。

served用户取mcptt-request-uri；O-PF入口的originator由PAI中的PUI识别，T-PF入口由mcptt-calling-user-id识别。两者不同且originator无修改权限时403并停止。Expires缺失或非零且小于4294967295时423，Min-Expires=4294967295并停止。

依据：§9.2.2.2.3 steps 1–5。

## 200之后仍有身份检查

适用条件：收到符合user_publish入口的请求；修改权限及Expires检查未停止处理。

非零Expires按RFC3903确定candidate间隔；零值令candidate间隔为零。返回200/Expires后，才检查PIDF entity是否等于served用户；不等则停止后续记录处理。因此PUBLISH 200本身不证明归属记录已更新，更不证明组主控已确认。

依据：§9.2.2.2.3 steps 6–9。

## 组存在与成员门槛

适用条件：收到符合group_publish入口的请求。

目标组取mcptt-request-uri，handled用户取mcptt-calling-user-id。Expires缺失或非零且小于4294967295时423/Min-Expires=4294967295并停止；GMS中无该组或用户不是该组成员时403并停止。这里不移植发起呼叫的allow-initiate-conference等规则。

依据：§9.2.2.3.3 steps 1–5。

## 控制侧200的证据边界

适用条件：收到符合group_publish入口的请求；Expires、GMS组存在及组成员检查均未停止处理。

先返回200及RFC3903选定的Expires，再核PIDF entity等于served组、tuple id等于handled用户；任一不符均停止后续记录处理。因此控制侧PUBLISH 200同样不能单独证明client列表已生效。

依据：§9.2.2.3.3 steps 6–8。

## 用户状态订阅授权

适用条件：收到符合user_subscription入口的请求。

served用户取mcptt-request-uri；O-PF入口originator由PAI的PUI识别，T-PF入口由mcptt-calling-user-id识别。originator不同且无修改该用户归属状态权限时403并停止；否则200并在订阅有效期间通知状态变化。不要把modify门槛擅自改为更宽的只读授权，也不要给本入口移植组侧SUBSCRIBE的423分支。

依据：§9.2.2.2.4。

## 组状态订阅授权

适用条件：收到符合group_subscription入口的请求；过滤用户与calling用户一致是入口条件，不是可省略的装饰。

Expires缺失或非零且低于4294967295时423并带相同Min-Expires；组不存在或handled用户非成员时403；通过后200并在订阅期间通知该用户状态。该入口不授权读取全组所有用户的归属。

依据：§9.2.2.3.4。

## 证据边界

- 本页只到输入门槛及早期200/后续身份检查，不宣称给出撤销的无冲突完整事务顺序。组侧零期限禁退FA的200/403顺序问题由撤销主题保留。
- 订阅接受、状态发布接受、具体client记录生效、呼叫授权是不同结果。
- 不代替完整RFC3903、SIP事务及业务入呼实现；归属结果不代表呼叫已接受。

## 按需继续

- [explicit-affiliation-publish](explicit-affiliation-publish.md)
- [explicit-affiliation-observation](explicit-affiliation-observation.md)
- [explicit-deaffiliation-state](explicit-deaffiliation-state.md)
- [active-call-entry](active-call-entry.md)
- [explicit-affiliation-server-state](explicit-affiliation-server-state.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页211、212、214、215、228、229、230、231；仅本版本。
