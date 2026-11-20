# 离网 MCPTT 组紧急告警：谁确认，谁取消，TFE1 到期清什么？

一台终端可以在本端不处于紧急状态的 E1 下，记录别人的告警、发出接收确认。也可以在本端已发警的 E2 状态下，取消跟踪别人的告警而仍留在 E2。**E1/E2 是本终端按 MCPTT 组保存的告警状态；接收方还在紧急用户列表中按原发警者 ID 跟踪告警，每个用户 ID 有各自的 TFE1。** 以下限 3GPP TS 24.379 V16.14.0（Release 16，Stage 3）的离网 MCPTT 组告警；告警收发和组呼参与、类型变化是不同程序。[§12.2.2.2、图 12.2.2.2-1，印刷页 457](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=458)；[§12.2.3.3，印刷页 458–459](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=459)。

## 本机发起离网组紧急告警，为什么收到 ACK 还会再发？

本机在 E1，收到用户对指定组发警的指示。用户配置档的 `/<x>/<x>/Common/MCPTTGroupCall/EmergencyAlert/Authorised` 与组配置的 `/<x>/<x>/Common/AllowedEmergencyAlert` **都为 true**，才满足这条发警入口。终端将本机已存紧急状态置 true，再保存指示的组 ID；生成并发送 `GROUP EMERGENCY ALERT`，填写该组 ID、本机用户 ID 作为原发警者、自己的组织名。若有请求，可以加入终端当前位置。发送后启动 TFE2，进入 E2。[§12.2.3.1，印刷页 458](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=459)；[§15.1.16.1、表 15.1.16.1-1，印刷页 484–485](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=485)。

终端在 E2 遇到**本机 TFE2 实际到期**，按当时的组、自己的 ID 和组织名重新生成并发送 ALERT；若有请求，仍可带当前位置。不要求逐字节重发上一条。发送后重启 TFE2，留在 E2。这条重传程序未规定收到 ACK 即停，也未列重传次数上限。权限不满足时，只能说不满足此发警入口，不能凭这两节推定某种失败响应或错误处理。[§12.2.3.1–2，印刷页 458](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=459)。

## 另一台终端第一次记入甲，再收到甲的告警要不要回 ACK？

终端在 E1 或 E2 实际收到 `GROUP EMERGENCY ALERT`，查看**本机列表中是否已有来件的 Originating MCPTT user ID**。这里判断的是本机记录，不是这条告警在全组首次发送，也不是判断两个报文的字节是否相同。[§12.2.3.3–4，印刷页 458–459](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=459)。

| 本机列表 | 收警端怎么做 |
| --- | --- |
| 原发警者不在列表 | 登记原发警者；有位置字段时登记来件位置（ALERT 的位置在消息表中为可选）。生成并发送 `GROUP EMERGENCY ALERT ACK`：组 ID、Originating ID 取自来件；Sending ID 填本机用户 ID。发送后启动该原发警者对应的 TFE1。 |
| 原发警者已在列表 | 可用收到的位置更新旧位置，重启该人的 TFE1。这条分支没有另列发送 ACK 的动作。 |

两条分支都保留本机当时的 E1 或 E2。比如甲发告警，乙回 ACK：ACK 的 Originating ID 指甲，Sending ID 指乙。若乙的列表后来移除了甲，再收到一份时仍按当时是否在列表判断；不是对甲的消息永久去重。[§12.2.3.3–4，印刷页 458–459](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=459)；[表 15.1.16.1-1、表 15.1.17.1-1，印刷页 485](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=486)。

## 甲主动取消自己的告警，要等别人回包才回 E1 吗？

甲端在 E2，实际收到本地用户取消告警的指示，且用户配置档的 `/<x>/<x>/Common/MCPTTGroupCall/EmergencyAlert/Cancel` 为 true。该节列的是取消告警的权限，不是发警的双条件，也不是降低紧急组呼优先级的 `CancelMCPTTGroup`。甲端将已存紧急状态置 false，生成 `GROUP EMERGENCY ALERT CANCEL`：组 ID 取本机已存值，Originating ID 和 Sending ID 都填甲自己的用户 ID。甲端发送以后停止 TFE2，回 E1，不等取消 ACK。只有 E1 状态、用户操作或等待结束的记录，不能代替甲端实际发出 CANCEL 的证据。[§12.2.3.5，印刷页 459](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=460)；[表 15.1.18.1-1，印刷页 485](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=486)。

## 乙不再跟踪甲：要区分实收 CANCEL 和本地 TFE1 到期

- **实收 CANCEL，且来件的原发警者还在乙端列表。** 乙端在 E1 或 E2，删除该用户及其位置记录，生成并发送 `GROUP EMERGENCY ALERT CANCEL ACK`，随后停止对应的 TFE1，保留自己的 E1 或 E2。ACK 的组 ID 取收到的 CANCEL，Sending ID 是乙自己的 ID。**第 2(c) 项对 Originating ID 的来源却写的是收到的 `GROUP EMERGENCY ALERT`，没有 CANCEL 字样。** 门槛和第 2(a) 项用的是收到的 CANCEL；字段表只说明 ACK 中有 Originating ID，不能抹平这处报文名差异。所引条款没有规定应从哪个历史报文取值、如何补救差异，也不把原文静默改成从当前 CANCEL 复制。[§12.2.3.6 第 2(a)–(c) 项，印刷页 459–460](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=460)；[表 15.1.19.1-1，印刷页 486](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=487)。
- **该用户仍在乙端列表，其关联的 TFE1 实际在本机到期。** 乙端删除该用户和位置，留在本端原有的 E1 或 E2。这条路径没有规定发送 CANCEL 或 ACK。删除记录不证明甲已发 CANCEL；只见某包缺失也不足以确证本地 TFE1 到期。[§12.2.3.7，印刷页 460](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=461)。

TFE1 是收警端跟踪单个原发警者的计时器，默认 30 秒、最大 60 秒；TFE2 是发警端的 ALERT 重传计时器，默认 5 秒、最大 10 秒。两者均可配置。要判断某端清除记录的时间，用该端实收、重启与到期的记录，不拿默认值代替实际配置。[表 B.3.4-1，印刷页 540](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=541)。

**一份 ACK 的证据只到相应终端。** 在实际记录足以把它和本次已知告警或取消关联时，ACK 表示所识别的终端确认收到相应消息。四种报文的字段表没有逐次告警的唯一标识、令牌或序号；仅靠组 ID 和用户 ID，不能为反复发警的每个报文找到唯一对应。看到回包发出不证明原发警端已实际收到；一份回包也不证明用户已阅读、全组已收到或每台终端都清除了记录。[§§15.1.16–19，印刷页 484–486](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=485)。

若场景是在网，读[在网 MCPTT 独立组告警](standalone-group-alert-client.md)；若业务是其他服务，读[离网 MCVideo、MCData 组告警的 Stage 2 流程](offnetwork-group-emergency-alert.md)，不把它当成本文的可替换信令。若另有组呼发起指示，见[离网紧急组呼的建立](offnetwork-group-emergency-establishment.md)；若已在通话中且要恢复普通类型，见[离网组呼降级](offnetwork-group-emergency-downgrade.md)。
