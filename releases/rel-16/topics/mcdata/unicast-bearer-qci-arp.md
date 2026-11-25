# MCData 单播承载：看见 QCI 70，能判断新建或抢占了吗？

不能。QCI 70 是 MCData **媒体专用承载**使用的 QoS 类别。要判断这次是改了已有承载、另建了承载，还是抢占了一条旧承载，得分别查运营商策略、ARP（分配与保留优先级）和实际的资源处理。这里说的是 Rel-16 在网 MCData 的 EPS 单播。[3GPP TS 23.282 V16.8.0，Stage 2，§5.8.3，印刷页 19–20](https://www.etsi.org/deliver/etsi_ts/123200_123299/123282/16.08.00_60/ts_123282v160800p.pdf#page=20)。

**申请时，谁向谁要资源？** 对于 MCData 会话请求，须经动态策略与计费控制（PCC）申请资源。MCData 系统经 Rx 向 PCRF 请求，并带上 MCData 应用标识，供 PCRF 判断应使用的 QCI。条款规定 MCData 的媒体专用承载使用 QCI 70；不能据此给 SIP 信令、默认承载或 MBMS 指定 QCI。只见一次 Rx 申请，不说明网络已分配资源。终端至少须支持一条供 MCData 使用的承载；这个下限不规定本次建几条。[§5.8.3 首段，印刷页 19](https://www.etsi.org/deliver/etsi_ts/123200_123299/123282/16.08.00_60/ts_123282v160800p.pdf#page=20)；[续文首段，印刷页 20](https://www.etsi.org/deliver/etsi_ts/123200_123299/123282/16.08.00_60/ts_123282v160800p.pdf#page=21)。

**哪些情况下可以改旧承载，哪些情况下会抢占？** 条款在媒体面列了两种受运营商策略约束的做法：

| 情形 | 本节能判断什么 |
| --- | --- |
| 策略允许修改已有承载 | MCData 系统可以请求修改已有承载的 ARP，不必为此发起新的专用 GBR（保证比特率）承载。看到请求还不能记为“已改”。 |
| 策略支持抢占，且其他应用承载的数量已达上限 | 新发起的 MCData EPS 承载还须比所比较的其他应用承载优先，且相应非 MCData 承载允许被抢占。在这条分支下，MCData EPS 承载抢占一条原有的 EPS 承载。 |

这两种做法不组成固定流程。只见承载数已满，或只见新承载优先级高，不能判这次一定抢占。若待让位的承载不可抢占，或新承载的优先级没有更高，本分支不支持把它判成已让位。即便条件齐备，要确认现场已经发生，还要看承载处理结果。这里提到专用 GBR 承载是为了说明什么时候可不另起一条，不能用来给所有 QCI 70 承载定性。[§5.8.3 两项策略条件及注，印刷页 20](https://www.etsi.org/deliver/etsi_ts/123200_123299/123282/16.08.00_60/ts_123282v160800p.pdf#page=21)。

**QCI 70 能识别紧急通信吗？** 不能。条款另给出 MCData 通信类型之间的 EPS 承载优先级：紧急最高，迫近危险（imminent peril）次之，普通最低。这是 MCData 内部的相对顺序，本节没有按这三类另定 QCI，也没有指定 ARP 数值。这个次序也不能用来给 MCData、MCPTT、MCVideo 排先后，或确认某次会话已拿到资源。[§5.8.3 末段，印刷页 20](https://www.etsi.org/deliver/etsi_ts/123200_123299/123282/16.08.00_60/ts_123282v160800p.pdf#page=21)。

- 若手头只有会话进展请求或客户端的 OK，查[公共单播资源建立和修改](../bearers/unicast-resource-establishment-modification.md)。若实际是并行会话要共用承载，查[公共 EPS 优先级共享](../bearers/unicast-bearer-priority-sharing.md)。这两项程序各有前提。
- 若问资源不足时，有抢占权限的组能要求 MC 业务做什么，查[在网 MCX 业务抢占要求](../bearers/onnetwork-service-preemption.md)；它不是本页对非 MCData EPS 承载的判断。若问已经进行的一对一 SDS 升级后何时调整双方承载，查[一对一 SDS 紧急升级](one-to-one-sds-emergency-upgrade.md)。
