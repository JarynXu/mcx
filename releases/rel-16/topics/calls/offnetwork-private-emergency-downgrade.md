# 离网紧急私呼取消：本端已回 Q1，对端确认了吗？TFP6 和 TFP8 各管什么？

**不能据此判断。** 终端发出紧急取消后就把本端呼叫类型设为普通私呼、进入 Q1，不等对端确认。等到同一呼叫的取消 ACK，才有对端收到这次取消的证据；这仍不是实际媒体送达的证据。这里讲的是一通**已进行的离网 MCPTT 紧急私呼**怎样降回普通私呼，不是取消整个通话。[TS 24.379 V16.14.0 §11.2.3.4.6.1、.3，印 441–442](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=442)；[§15.1.12–13，印 483](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=484)

## 谁能主动取消紧急？本端发出后等什么？

在呼叫类型状态 **Q2**，紧急私呼主叫可以发起取消；被叫的用户配置档须存在 `Common/PrivateCall/EmergencyCall/CancelPriority` 叶节点且值为 `true`，才符合本段对被叫的条件。终端发送 `PRIVATE CALL EMERGENCY CANCEL`，使用本场已存的 Call identifier、主叫 ID 和被叫 ID；不是 SIP CANCEL，也不是 `PRIVATE CALL RELEASE`。接着停仍在运行的 TFP1、停 TFP8，将取消重传计数 CFP6 设为 1、启动 TFP6，并把本端呼叫类型设为普通私呼、进入 Q1。[§11.2.3.4.6.1，印 441](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=442)；[§15.1.12，印 483](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=484)

| 本端在 Q1 实际遇到的事件 | 本端接着做什么 |
| --- | --- |
| 收到与这次取消对应、Call identifier 相同的 `PRIVATE CALL EMERGENCY CANCEL ACK` | 停仍在运行的 TFP6；用已存的 SDP 应答建立媒体会话，把 ProSe 分组优先级设为离网普通私呼对应的值，留在 Q1。ACK 表示对端收到取消，不证明两端已收到语音。 |
| TFP6 到期，CFP6 还没到上限 | 再发取消，CFP6 加一，重启 TFP6，留在 Q1。步骤 3 把 CFP6 写成 timer；同一段的条件及附录 C.2.2 将 CFP6 定义为计数器，TFP6 才是计时器。 |
| TFP6 到期，CFP6 已等于上限 | 呼叫类型控制释放已存呼叫类型及 ProSe 分组优先级，进 Q0。基本呼叫控制若在 **P4**，同一达限事件要求启动 TFP7、停 TFP5、释放呼叫类型状态机并进 **P1**（暂忽略同一 Call identifier）。不要把这两段当成一个状态或推断它们的执行先后。 |

[§11.2.3.4.6.2–.4，印 441–442](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=443)；[§11.2.2.4.5.9，印 435](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=436)；[§11.2.3.1，印 436](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=437)；[表 C.2.2-1，CFP6 表项，印 542](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=543)

仅有本端进入 Q1 的记录，不能确认对端状态、媒体已经按普通私呼重建或分组优先级已经复原。仅有「未看到 ACK」也不能直接判达限；先核对本场 TFP6 和 CFP6。达限步骤没有写额外发一条 RELEASE，不能仅凭本端进 P1 就认定另一端已结束。[§11.2.3.4.6.1–.4，印 441–442](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=442)；[§11.2.2.4.5.9，印 435](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=436)

## 对端已经是 Q1，或本端 TFP8 到期，分别怎样判？

- **收到同一 Call identifier 的紧急取消：**接收端在 Q1、Q2 都要发送取消 ACK，再用已存 SDP 应答建立媒体、恢复普通私呼的 ProSe 分组优先级。如果原先在 Q2，还要停 TFP8、把类型设为普通私呼并进 Q1。在 Q1 并不是丢掉同一呼叫后续取消的理由。[§11.2.3.4.6.5，印 442–443](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=443)
- **在 Q2 的 TFP8 到期：**这条是本端隐式降级。按已存 SDP 应答建立媒体，恢复普通私呼优先级，把类型改回普通并进 Q1。这段没有列发送取消、等 ACK 或结束会话的动作，不能把一次本端 TFP8 到期写成对端也已降级。[§11.2.3.4.6A，印 443](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=444)

若原问题是怎样[把普通私呼升级为紧急私呼](offnetwork-private-emergency-upgrade.md)，查升级请求与接受分支。若已经实收的是 [PRIVATE CALL RELEASE](offnetwork-private-release-evidence.md)，查释放整个通话的 P、Q 与媒体证据，不能套用紧急取消的 ACK。
