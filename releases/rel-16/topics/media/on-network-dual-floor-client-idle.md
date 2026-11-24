# 双话权：有发送许可的 MCPTT 终端收到 Floor Idle，要放权吗？

不一定。终端的话权参与者原在 `U: has permission`，并实际收到话权控制服务器发来的 `Floor Idle` 时，TS 24.380 V16.9.0 §6.2.4.5.7 有两项清标记的规定。命中任一项，终端仍有发送许可。[§6.2.4.5.7，印刷页 44](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=45)

| 收件前已存的标记 | 还要核对什么 | 终端做什么 |
| --- | --- | --- |
| 本端覆盖对方且未撤销对方话权（`overriding without revoke`） | 第 1 项没另要求消息中 `Floor Indicator` 的 G 位为 1。 | 清除**本端覆盖对方**的标记，留在 `U: has permission`。 |
| 本端被覆盖但未被撤权（`overridden without revoke`） | 第 2 项还要求这份 `Floor Idle` 的 `Floor Indicator` 中 G 位为 1（Dual Floor）。 | 清除**本端被覆盖**的标记，留在 `U: has permission`。 |

在各自条件成立后，来向 `Floor Idle` 的 subtype 首位为 1 才按该项回 `Floor Ack`。清标记和保持许可不以要求确认或实际发出 ACK 为条件。这里的 **G 位是消息字段**，不是服务器仲裁状态名。只看到 Idle，不能认定本端清了哪项标记、失去许可或整场组呼已经空闲；没有命中这两项条件时，本条不规定下一步。

**核对 ACK 时要区分流程的字面写法和通用编码。** 两项都把 ACK 的 `Message Type` 写成 `1 (Floor Idle)`，`Source=0`（话权参与者）。同版通用 §8.2.3.14 把 `Message Type` 定义为前置 `000` 加上被确认消息的五位 subtype（包括首位）；表 8.2.2.1-1 把 `Floor Idle` 列为 `x0101`、`Floor Granted` 列为 `x0001`。两处写法不一致。本页保留差异，不据此选择实际 ACK 的编码值，也不使用其中一个数值单独判报文是否合法。[表 8.2.2.1-1，印刷页 148](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=149)；[§8.2.3.14，印刷页 155](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=156)。

若要查[双话权交接时服务器为什么发 Idle 或 Taken](on-network-dual-floor-handover.md)，看服务器侧的另一个程序。若终端收件前已经在等待自己放权的结果，查[等待释放时收到 Idle](on-network-holder-release.md)，不沿用本页的许可状态。
