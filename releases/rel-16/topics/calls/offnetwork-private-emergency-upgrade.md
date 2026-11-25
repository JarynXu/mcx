# 离网私呼紧急升级：同一通话何时升为紧急，拒绝和无响应各回到什么状态？

这是一通已经在进行的离网普通 MCPTT 一对一私呼。升级仍使用这通呼叫的 **Call identifier**，不是重新建立一通私呼。每台终端有两套并行的本地状态：基本呼叫控制看 **P**，呼叫类型控制看 **Q**。发起升级的一端可以先进入 Q2，不能因此判定对端也已进入紧急。以下限 TS 24.379 V16.14.0 的这条升级程序。[§11.2.3.1–3，印刷页 436–437](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=437)

## 发起升级时，同一通呼叫怎么识别？

在 **Q1（进行中的普通私呼）**，用户要求升级，且本机用户配置的 `PrivateCall/EmergencyCall/Authorised` 为 true，才命中这条发起程序。终端生成并保存紧急 SDP offer，把自己的 MCPTT 用户 ID 存为 caller ID、对端存为 callee ID，并把本地呼叫类型置为 `EMERGENCY PRIVATE CALL`。这两个身份按**本次升级**填，不按普通呼叫当初由谁发起来判断。

`PRIVATE CALL SETUP REQUEST` 携带已存的 Call identifier、两个用户 ID、`AUTOMATIC COMMENCEMENT MODE`、紧急呼叫类型和紧急 SDP offer，用户位置字段可选。发起端选用紧急私呼对应的 ProSe 包优先级，向对端发送请求；将 CFP1 置为 1、启动 TFP1，若 TFP6 在运行则停止，进入 **Q2（进行中的紧急私呼）**。原文不等对端 ACCEPT 才进入 Q2。这里只记录所选优先级类别，不指定数值，也不证明底层已按该类别传包。[§11.2.3.4.5.1，印刷页 438](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=439)

发起端在 Q2，**TFP1 到期且 CFP1 仍低于上限**时，计数加 1，沿用该 Call identifier、已存两端 ID、呼叫类型和紧急 offer。每次重传的 Commencement mode 仍须明确写 `AUTOMATIC COMMENCEMENT MODE`，不沿用原普通私呼的模式。终端可更新并可携带用户位置。再次发出请求后重启 TFP1，仍在 Q2。不能按 SETUP REQUEST 的条数计新呼叫。只有一条离线抓包、没有本机当前 Call identifier 或分支记录时，也不能只凭消息名断定它一定是一次升级。[§11.2.3.4.5.2，印刷页 439](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=440)

## 对端实收同一 Call identifier 的紧急请求，怎样接受或拒绝？

对端必须在 Q1 或 Q2，实收的 SETUP REQUEST 的 Call identifier 等于它已存的呼叫标识，Call type 为 `EMERGENCY PRIVATE CALL`。接下来判断请求的 SDP 所描述的媒体会话能否建立。

- **能建立：**接收端按来件 offer 生成并保存紧急 answer，从来件取 caller ID，用自己的 MCPTT 用户 ID 作 callee ID；生成带同一 Call identifier、两端身份和 answer 的 `PRIVATE CALL ACCEPT`。原在 Q1 时，先切换紧急私呼包优先级、停止仍在运行的 TFP6、启动隐式降级计时器 TFP8，再发 ACCEPT，然后更新呼叫类型并进入 Q2。原已在 Q2 时，仍发适用的 ACCEPT 并留在 Q2；本条不要求它再启动或刷新 TFP8。
- **不能建立：**接收端回 `PRIVATE CALL REJECT`，沿用来件的呼叫标识和两端 ID，并留在接收前所在的 Q1 或 Q2。只有本次要求限制失败通知**且**用户配置 `PrivateCall/FailRestrict` 为 true，才用 `FAILED`，否则用 `MEDIA FAILURE`。`FAILED` 在这条分支不表示用户拒接。

这里的 SDP 判断与发 ACCEPT 不等于媒体已通。该段不把接收端进入 Q2 写成等 ACCEPT ACK 或接到 RTP；不要把普通私呼初建的 P5 证据搬到此处。[§11.2.3.4.5.6，印刷页 440–441](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=441)

## 发起端收到回复，或最终等不到回复，会怎样？

| 发起端实际发生的事件 | 本地结果 |
| --- | --- |
| 在 Q2 实收本次 SETUP REQUEST 对应、Call identifier 相同的 **ACCEPT** | 保存收到的紧急 SDP answer，生成并发出带已存标识和身份的 **PRIVATE CALL ACCEPT ACK**；停止仍在运行的 TFP1；TFP8 未运行才启动。若尚未按这份 answer 建立媒体会话，应建立，仍在 Q2。原文注释说每次收到适用的 ACCEPT 都按本条重发 ACK。 |
| 在 Q2 实收本次 SETUP REQUEST 对应、Call identifier 相同的 **REJECT** | 停止仍在运行的 TFP1，改回普通私呼对应的包优先级和 `PRIVATE CALL` 类型，进入 **Q1**。本条没有列出恢复旧 SDP、改动 TFP8 或发送 RELEASE 的步骤。 |
| 在 Q2 **TFP1 到期且 CFP1 等于上限** | 呼叫类型控制清除存储的当前呼叫类型和包优先级，进入 **Q0**。不是显式 REJECT 后的 Q1，也不能据此判断对端是否收到、同意或拒绝。 |

同一个达限事件还要查基本呼叫控制。在本端 **P4（参加进行中的呼叫）**，TFP1 到期且 CFP1 等于上限时，§11.2.2.4.5.8 规定启动 TFP7、停止 TFP5、释放呼叫类型控制状态机，进入 **P1（忽略相同呼叫标识）**。Q2 分支描述 Q0，P4 分支描述 P1 与释放类型状态机；条款没指定两套处理的调度顺序。不要把 Q0 记成恢复普通通话，也不要把 P1 记成已经与对端交换了 RELEASE。P4 达限条款没有列出发送 RELEASE 或终止媒体会话；同页明确终止媒体的是 TFP5 到期的另一条规定。核实本地媒体是否结束、对端收到什么，另查各自证据。[§11.2.3.4.5.3–.5，印刷页 439–440](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=440)；[§11.2.2.4.5.6、.8，印刷页 435](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=436)

抓到对端发 ACCEPT，不等于发起端实收；发起端真实收到对应 ACCEPT 才能套用接受分支；要看本地动作是否完成，还须核对本端处理记录。发出 ACK 仍不证明对端实收。两端的 Q 状态、媒体会话处理、实际语音是否到达分别查证。

若确认是[新建离网紧急私呼](offnetwork-private-emergency-establishment.md)，查首条请求、接听模式和 TFP8 的启动。普通私呼初建按模式查[自动应答](offnetwork-private-auto-client.md)或[手动应答](offnetwork-private-manual-client.md)。若是组公告里的同组类型变化，查[离网组呼紧急升级](offnetwork-group-emergency-upgrade.md)。本页不展开新建紧急私呼、不定义实际降级步骤、媒体参数计算、话权或一端同时收到对向升级时的处理顺序。

已在进行中的离网紧急私呼要恢复普通私呼时，查[取消紧急、TFP6 达限与 TFP8 隐式降级](offnetwork-private-emergency-downgrade.md)；这不是再次升级或释放整通话。
