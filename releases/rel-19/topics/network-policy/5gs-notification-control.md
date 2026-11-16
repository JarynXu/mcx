# GBR 无法保障时：通知不等于立即释放

适用：TS23.501 V19.8.0; GBR QoS Flow; Notification control without Alternative QoS Profiles。

此页仅讨论 GBR、启用 Notification control、没有 Alternative QoS Profiles，且应用流量能适应 QoS 变化的分支。

SMF 只有在绑定该流的 PCF 下发 PCC 规则设置对应参数时，才启用通知控制（§5.7.2.4.1）。失保判断需考虑 Averaging Window，Delay-critical GBR 还需考虑 MDBV，不是看到一个瞬时值就判定失保。RAN 无法满足 GFBR、PDB 或 PER 时，通知 SMF 并保留流；但无线链路故障或 RAN 内部拥塞等具体条件仍可能要求释放资源。RAN 应尝试重新满足 profile（§5.7.2.4.1a）。

若 NG-RAN 已收到相应方向的 PSDB 和 PSER，且该方向应用 PDU Set QoS handling，判断中的 PDB/PER 按 §5.7.2.4.1 替换为 PSDB/PSER；未满足这些条件的另一方向仍使用 PDB/PER。不能把这条保留规则推广到未启用通知控制或有替代 profile 的其他分支。

## 来源与边界

If PDU Set QoS handling applies, §5.7.2.4.1 substitutes PSDB/PSER for PDB/PER in applicable directions; detailed PDU Set behavior is not covered.

Alternative QoS Profiles and complete restoration/PCF/AF signaling are not covered.

[精确条款与结构化条件](5gs-notification-control.json)，[来源目录](../../sources.json)。

- [5GS QoS 基础](5gs-qos-model.md)
