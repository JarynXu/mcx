# MCPTT 经 MBMS 转发话权消息：同一序号还能收到 Floor Ack 吗？

能。**不再下发一条话权消息**和**回复上游请求的确认**是两个判断。这里限在网 MCPTT 参与功能（PF）处于 `M: A conversation is active`，收到目的端正在监听 MBMS 子信道的 Floor Idle、Floor Taken 或 RTP。不能拿这些规则判断其他单播分支。〔TS 24.380 V16.9.0，Rel-16，Stage 3，§10.2.3.1–.3、.5，印刷页 205–208〕

## Floor Idle 和 Floor Taken：按会话的消息序号决定下发

PF 先查该会话有没有存过话权消息序号。首条、尚无记录时保存收到的序号；已有记录时，只在收到的序号**更高**时更新。两种情形都要把发向 MBMS 的这条消息的确认位设为 **0**，再发到 MBMS 子信道。序号等于或低于记录时，丢弃这条下行消息，不再向 MBMS 发送它。比如已存 42，再收到序号 42 的 Floor Taken，就不会把这条消息再下发。〔§10.2.3.2、.3，印刷页 206–207，步骤 1–3〕

## 回复 Floor Ack：看入向确认位，不看有没有再次下发

若**收到的** Floor Idle 或 Floor Taken 的确认位为 **1**，PF 必须向控制 MCPTT 功能回复 Floor Ack。Floor Idle 的 Ack 填 **Message Type 5**；Floor Taken 的 Ack 填 **Message Type 2**；两者均填 **Source 1**，表示确认来自 PF。即使收到的序号 42 因重复未再下发，入向请求确认时本步骤仍适用。PF 回复 Ack 不能证明这条消息已下发到 MBMS，也不能证明任何监听终端已经收到。〔§10.2.3.2、.3，步骤 4〕

## RTP：查这一包是否已经在 MBMS 上发送过

PF 收到发往监听该子信道客户端的 RTP，查的是**该包是否已通过 MBMS 子信道发过**。已发过就丢弃；未发过就指示媒体分发功能在该子信道发送。不要给 RTP 套用 Floor Idle 或 Floor Taken 的消息序号比较；本段没有规定怎样识别同一 RTP 包。若该包的目的端不是正在监听 MBMS 子信道的客户端，§10.2.3.5 的注说经单播承载转发。以上三种处理均有重启 **T15**、保持 **M** 状态的步骤；这也不能证明终端已经收到或播放。〔§10.2.3.2、.3 步骤 5–6，§10.2.3.5，页 208〕

要看[MBMS 应用控制消息和终端监听报告](../bearers/mbms-application-control-signalling.md)，或[非控制功能的其他 RTP 权限分支](on-network-noncontrolling-floor-rtp.md)，请按实际角色和消息类型分开查。

依据：[3GPP TS 24.380 V16.9.0，Release 16，Stage 3（ETSI，印刷页 205–208）](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=206)。

若还没确定该消息为什么应进入 MBMS 子信道处理，先查[参与功能怎样选择下行话权和 RTP 路径](mbms-pf-floor-routing.md)。本页只处理已经进入活动 MBMS 会话分支的去重与确认。若在终端侧已抓到包，要判断话权消息或 RTP 是否转给本地组件，读[终端按通话关联和 SSRC 处理实收包](../bearers/mcptt-mbms-map-unmap-timers.md#client-receives-floor-or-rtp)。
