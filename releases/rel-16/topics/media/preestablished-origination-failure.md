# 主叫收到 REFER 200，后面为什么还会收到 Disconnect？

看 200 和后面的失败分别属于哪一笔。甲使用已有预建立会话发起普通在网私呼：**甲的 REFER 由发起侧参与功能（O-PF）答复；O-PF 另发给控制功能（CF）的业务 INVITE，才有 CF 对业务建立的结果。** 主叫先收 REFER 200、业务 INVITE 后被 CF 拒绝，这两件事并不冲突。下文只查同一普通私呼发起尝试，且这通私呼使用话权控制。[TS 24.380 V16.9.0，Release 16，Stage 3，§9.1，印刷页 193](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=194)；[附录 A.5.2.2 的主叫失败例，图 A.5.2.2-1，印刷页 255](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=256)。

## 哪个失败才会触发这条 Disconnect？

两个现场记录都能出现 404，但不能合并。**O-PF 对主叫的 REFER 回 404**，先按[私呼发起的 SIP 事务](../calls/private-preestablished-origination.md)查是哪个本地检查；这不是 CF 对独立业务 INVITE 的回复。**O-PF 对 REFER 已回 200，后来在自己的业务 INVITE 上实收 CF 的失败答复**，则查同一次失败是否已经以呼叫建立失败指示送到本地媒体面。只有看到两条 SIP 记录，不能填成媒体面已处理。

O-PF 对这条预建立会话处于 `G: Pre-established session in use`，并实际收到 CF 的本次呼叫建立失败指示时，须向甲发送 MCPC Disconnect，启动 T56，将 C56 初始化为 1，终止这次呼叫尝试，并进入 `G: Call releasing`。它**宜**将 subtype 首位置 1 请求确认；启动 T56 并未以确认位已置 1 为前提。这不是主叫的 REFER 被拒，也不是因终端用 Busy 或 Not Accepted 回了某份 Connect。只抓到 O-PF 发 Disconnect，仍分不出它究竟走了哪种入口。[§9.3.2.4.11，印刷页 202–203](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=203)；[终端负确认的对照，§9.3.2.4.7，印刷页 201](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=202)。

## 失败时没有本次 Connect 的记录，Disconnect 的身份怎么核？

第 1(a) 项仍要求沿用这通呼叫建立时 Connect 的**整个 MCPTT Session Identity 字段内容**，既含 `Session Type`，也含会话身份值。资料性附录的失败图在 CF 对业务 INVITE 回 4xx 后画了 Disconnect，没有画本次 Connect，也没有给这项字段的取值。若可靠记录找不到本次 Connect，字段便缺少比对依据；不能拿 REFER 的 200、失败答复的 Contact、预建立会话的身份或上一通呼叫的 Connect 补值。也不由图上没画 Connect 推出可以不发 Disconnect、可以省略字段或必须怎样兼容。[§9.3.2.4.11 第 1(a) 项，印刷页 202](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=203)；[§8.3.3.3、表 8.3.3.3-1，印刷页 176](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=177)；[图 A.5.2.2-1，印刷页 255](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=256)。

## 发出 Disconnect，就算两边都退出了吗？

不是。`G: Call releasing` 是 **PF 保留预建立会话、正在处理本次呼叫释放**的过渡状态，不是销毁预建立会话。先查 PF 的发送，再查甲是否实际收到、甲当时的本地状态与确认位；要说 PF 已收到确认，另看 PF 的配对收件。资料性图的第 7 步有这份确认，不代表所有线上实例都收到它。要进一步区分实收确认和重试到限，读[在网预建立私呼的释放与确认](preestablished-release-outcome.md)的相应条款，不把其正常 CF 释放入口当成本次建立失败的原因。[§9.3.2.5.1–.4，印刷页 203](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=204)；[终端实际收件，§9.2.2.4.5，印刷页 196](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/16.09.00_60/ts_124380v160900p.pdf#page=197)。

如果 CF 实际回的是业务 INVITE 的 **200 OK**，读[发起侧主叫 Connect 的赋值](preestablished-connect-outcome.md)，不要选失败出口。若实际收到的是甲对本次 Connect 的负确认，也按同一旧页的负确认入口另判。只有 REFER 200、尚未配到下一笔事务时，当前证据只够回答 REFER 这一腿。

[结构化条件与声明](preestablished-origination-failure.json)。
