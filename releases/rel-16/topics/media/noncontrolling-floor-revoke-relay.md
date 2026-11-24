# 控制侧发来的 Floor Revoke，非控制侧怎样转发？

先分清两次实收。非控制 MCPTT 功能的**话权控制服务器接口**实收控制侧的 Floor Revoke，按 Track Info 找到要转发的**话权参与者接口**。然后看这名参与者对应的接口是否实际接到该消息，以及它当时是否处于 `P: has permission`。这两条都是转发收到的 Floor Revoke，不是本地新发起撤权。[3GPP TS 24.380 V16.9.0，Release 16，Stage 3，§6.5.4.10，印刷页 111](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=112)；[§6.5.5.4.7，印刷页 117](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=118)。

## 转给哪个参与者接口？Track Info 要不要保留？

服务器接口须用 Track Info 末尾的 `Participant Reference` 确定本次对应的话权参与者接口，再按引用值的数量准备发出的 Floor Revoke：

- **只有一个引用值：**去掉发出消息里的整个 Track Info 字段。
- **有多个引用值：**只删 Track Info 里的最后一个引用值，保留该字段。

两种情形都须把 Floor Revoke 转给刚确定的参与者接口。例如，收到的引用值依次为 A、B，按 B 确定接口，发出时删 B、留 A；如果只收到 B，仍按 B 确定接口，发出时移除整个字段。A、B 表示引用值，不是用户姓名。从报文看见 Track Info 已删，不能反推该接口已实收；若找不到可用引用或对应接口，本节没有给出缺失或无效时的处置。[§6.5.4.10 步骤 1–3，印刷页 111](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=112)。

## P 接口转发后，是否记录待收确认？状态会变吗？

话权参与者接口原已处于 `P: has permission`，且实收来自该服务器接口的 Floor Revoke，须把它发给自己对应的话权参与者。**若 Floor Revoke 的 subtype 第一位是 1**，该接口还须记录预期收到针对 Floor Revoke 的 Floor Ack。第一位不是 1 时，本步没有要求新建这项记录，也没有规定如何清理原有记录。

无论是否记录待收确认，这个接口在本条都须**保持 `P: has permission`**。这是非控制侧参与者接口的本地状态，不是终端或全局仲裁状态。看到 P 状态不变，或看到一项待收确认，不能据此认定实际撤权已完成、已收到或发出 Ack、该重传哪一条消息，或参与者实际还能发媒体。[§6.5.5.4.7 步骤 1–3，印刷页 117](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=118)。

若查的是[本地话权抢占与撤权计时](on-network-preemption-revoke.md)，或[非控制侧因 RTP 检查触发本地撤权](on-network-noncontrolling-floor-rtp.md)，按对应入口读。不能拿那些动作解释一次实收的控制侧 Floor Revoke。
