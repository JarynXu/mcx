# 在网 MCPTT：持有者松开 PTT 后，谁确认放权，谁停止转发 RTP？

Floor Ack 要看它确认哪条消息。服务器给放权者的 Ack（Message Type=4、Source=2）确认收到了 **Floor Release**；终端给服务器的 Ack（5、0）确认收到了 **Floor Idle**。哪一个都不是“全组已停收语音”的回执。

本页限 3GPP TS 24.380 V16.9.0（Release 16，Stage 3）：同系统内已建立的普通按需组呼，显式申请获准的唯一持有者主动放权，服务器接口直接关联该终端。不含广播、系统呼叫、临时组、紧急或迫近危险组呼、环境监听、音频切入、双话权或多人同时发言。下文用 **U** 指控制服务器上面向一个参与者的接口，用 **G** 指同一服务器为本次通话仲裁话权的逻辑。终端也有自己的状态，不与 U 或 G 共用。

## 松开 PTT 后，哪个动作才要求停止分发？

1. **终端发 Release。** 已有发送许可的用户可以在第一包语音发出前松开 PTT。终端须发送 Floor Release，启动 T100，将 C100 置 1，进入 pending Release。它可以在 Release 的 subtype 首位置 1，要求确认；收到或没收到这个 Ack 后怎样处理，由实现决定。[§6.2.4.5.1、§6.2.4.5.3，印刷页 42–43](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=43)。
2. **U 确认并转交。** 原持有者的 U 在 permitted 实际收到关联终端的 Release。若 subtype 首位是 1，U 须回 Floor Ack（Message Type=4，Source=2，控制功能）。在没有保存 overriding / overridden without revoke 标记的分支，U 须将交给 G 的 Release 的 subtype 首位置 0（已是 0 则不变）。它转交后仍在 permitted。[§6.3.5.5.3 第 1、4 项，印刷页 85](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=86)。
3. **G 请求停止转发。** G 在 Floor Taken 实际收到这份 Release，才按此事件要求媒体分发器停止转发来自该发送者的 RTP，停止该端正在运行的 T2、T20。不支持多人同时发言时，G 执行进入 Floor Idle 的程序。释放是计时器表给 T1 列出的正常停止条件；该收件条款只逐项列出 T2、T20，未给 T1 的停止排定先后。[§6.3.4.4.6 第 1–4 项，印刷页 61](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=62)；[表 11.1.3-1 的 T1 行，印刷页 218](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=219)。

只有第 2 步的 Ack，不能断定第 3 步已经发生。即使已有 G 发出的停转请求，也不知道最后一包何时到达听众；U 暂留 permitted 同样不能证明媒体还在传。

## G 发给全员的 Floor Idle，到哪一步才能算终端收到了？

这里从 G 的 Taken 进入 Idle 程序，还须满足：**没有客户端协商排队、不存在 §6.3.6 的双话权状态机，且活动请求队列为空**。G 删除此前为一般话权仲裁保存的 Track Info（如有），向全体话权参与者发送 Floor Idle，消息序号加 1；启动 T7 并将 C7 置 1，启动 T4，将一般仲裁状态置为 Floor Idle。[§6.3.4.3.2 首种入口第 1、2 项，印刷页 56](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=57)。

同一个消息名，收件人当时的状态决定动作：

| 实际收到 Floor Idle 的一方 | 处理 |
| --- | --- |
| 原持有者的 U，仍为 permitted，未存上述标记 | 收到 G 的 Idle，转为 not permitted and Floor Idle，清除本接口已存的 Track Info（如有）。该分支没有明写把**这同一份** Idle 转给原终端；不能据此断言已转发，也不能断言禁止转发。[§6.3.5.5.4(2)，印刷页 85](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=86)；[§6.3.5.3.2，印刷页 75](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=76)。 |
| 另一参与者的 U，原为 not permitted and Floor Taken，未存双话权标记 | 收到 G 的 Idle，须转给自己的关联端，可以要求 Ack；进入 not permitted and Floor Idle。[§6.3.5.4.3，印刷页 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=79)。 |
| 已在 not permitted and Floor Idle 的 U | 若在此状态实际收到 G 的 Idle，须转给关联端，可以要求 Ack，仍在本状态。这不能倒推进入此状态的那份通知已转发，也不保证还有下一份。[§6.3.5.3.10，印刷页 77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)。 |
| 原持有者的终端，仍在 pending Release | 实收普通 Floor Idle，若消息要求确认须回 Floor Ack（Message Type=5，Source=0，参与者）；可提示用户话权空闲，须停止 T100，转为 has no permission。[§6.2.4.6.4，印刷页 45–46](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=46)。 |
| 旁听终端，已在 has no permission | 实收 Floor Idle，若消息要求确认，同样回 Ack（5、0）；此前未提示过则可提示空闲，若可选的 T103 正在运行则须停止。该端仍无发送许可。[§6.2.4.3.2，印刷页 37–38](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=38)。 |

原终端还有另一条退出等待的路：T100 到期次数达到 C100 上限时，本端进入无许可。这不证明 U 或 G 收到了 Release。空闲是话权状态，不是呼叫已结束；判断某个听众是否收到了这一份 Idle，还要看该听众的收件证据。[§6.2.4.6.3，印刷页 45](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=46)。

## 释放后还有带载荷的 RTP，服务器能把它交给分发器吗？

要看**同一个 U 的前后两个状态**。先前它在 permitted 收到过本关联终端的 Floor Release；现在它已在 not permitted and Floor Idle，网络媒体接口又报告收到了该终端**带载荷**的 RTP。两个条件都满足时，U 须要求网络媒体接口不要把收到的这些包转给分发器，并向该终端发 Floor Revoke，拒绝原因 **#3（无发送媒体突发的许可）**。U 进入 not permitted but sends media，启动 T8；在此状态不得要求网络媒体接口把该终端的 RTP 转给分发器。[§6.3.5.3.8，印刷页 77](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=78)；[§6.3.5.7.2，印刷页 89](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=90)。

单点看到迟到的 RTP，只能说明包到了该点；不能据此推断终端仍有话权、分发器已转发或听众已播放。这里的 Revoke 针对无许可发送，不表示有人抢占。§6.3.5.3.8 的注另行说明：若关联的一方是非控制功能的服务器接口，未授权 RTP 由该非控制功能处理，不套用本页的直接客户端入口。

要核对终端重传或其他等待结果，读[普通在网话权客户端](on-network-floor-client.md)。如果实际起点是空闲时收到新申请，读[空闲服务器如何授予话权](on-network-idle-floor-server.md)；没有 Release 而是收包超时或到达发言时限，读[媒体与发言超时](on-network-floor-media-timeouts.md)。若控制方此前已选择撤销，或发送者只是撤回排队，读[抢占撤销与退队](on-network-preemption-revoke.md)。
