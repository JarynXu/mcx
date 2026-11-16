# Chat 既有会话更新：客户端响应与预建立转接

TS24.379 V19.4.0 在网chat组呼。各claim独立写明入口，不把预安排组呼的被叫自动/手动选择和session-ID重入原样搬来。

## 客户端如何响应既有对话更新

适用条件：chat客户端收到既有按需或预建立会话内re-INVITE；本条仅不含emergency-ind、imminentperil-ind、alert-ind和优先级扩展的普通情形。

10.1.2.2.1.2适用于两种承载。客户端生成200，Contact带g.3gpp.mcptt和MCPTT ICSI；按需分支的SDP answer按6.2.2，预建立分支根据已经协商的参数生成answer；发送200。它是既有对话更新，不是10.1.1预安排初始来呼的自动/手动接听选择。

依据：§10.1.2.2.1.2 introduction and steps6–11。

## 参与功能按承载分流

适用条件：参与功能收到面向chat终接客户端的re-INVITE；本条不含Resource-Priority扩展。

若发给客户端的请求将在预建立对话内发送，进入10.1.2.3.2.2并跳过剩余步骤。否则按6.3.2.2.10生成re-INVITE，SDP offer由收到的offer按6.3.2.2.1生成，并发给客户端。收到该请求的200后按6.3.2.2.4.2生成上游200，以收到的SDP answer按6.3.2.2.2.1构造answer并转送。

依据：§10.1.2.3.1.4。

## 预建立分支等待客户端响应

适用条件：终接参与功能已进入10.1.2.3.2.2的chat预建立分支，所收为相应INVITE或re-INVITE；本条不含Resource-Priority扩展。

在预建立对话内向客户端生成re-INVITE，SDP offer由收到offer按6.3.2.1.1.2构造；收到客户端对该re-INVITE的200后，才按6.3.2.2.4.2生成上游200并按6.3.2.2.2.2附answer。不要把预安排Auto分支不等客户端最终响应的行为移到这里。

依据：§10.1.2.3.2.2。

## 初始请求复用预建立是可选决策

适用条件：参与功能按10.1.2.3.1.3处理chat终接INVITE，前序资源/isfocus检查未拒绝。

当客户端有无关联业务呼叫的预建立会话，且speech和floor-control两媒体段分别匹配时，参与功能MAY按本地策略转10.1.2.3.2.2；不是只匹配speech即可，也不是匹配就必须复用。此服务器入口没有授权把客户端10.1.2.2.1.6的优先范围扩成普通chat被叫接受算法。

依据：§10.1.2.3.1.3 step4。

## 证据边界

- 终接initial INVITE完整客户端链不纳入普通范围；尤其不为缺少普通接听说明自造默认Auto/Manual。
- 6.3.2.2.10、6.3.2.2.4.2等共用生成helper沿原引用，未重新核全部头字段、MIKEY、失败和RFC事务流程；上面不是完整消息模板。
- 未核24.380媒体、实际话权、自动回覆盖检测或自动恢复。
- 优先指示true/false各有状态副作用，本主题明确排除，不能在收到这些指示时只执行普通baseline。

## 按需继续

- [preestablished-session-lifecycle](preestablished-session-lifecycle.md)
- [../groups/conference-state](../groups/conference-state.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页319、320、333、334、339；仅本版本。

- [按需Chat入口](chat-ondemand-entry.md)
- [控制侧准入](../groups/chat-ondemand-control.md)
