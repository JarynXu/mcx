# 5GS QoS：QFI、5QI 与 ARP 分别决定什么

适用：TS23.501 V19.8.0; 5GS QoS model。

QFI 标识 PDU Session 内最细粒度的 QoS Flow，并在该 Session 内唯一；同 QFI 流量获得相同转发处理。不能一概令 QFI 等于 5QI；本页不提供§5.7.1.3的分配及对应ARP/N2配置规则（§5.7.1.1）。

5QI 引用转发特性；每条流的 QoS profile 包含 5QI 和 ARP，GBR 流另需上下行 GFBR、MFBR（§5.7.1.2、§5.7.2.1）。ARP 包含优先级、抢占能力和可被抢占属性，用于资源不足时的接纳、拒绝及可能的抢占释放（§5.7.2.2）。

这能帮助定位配置职责，但不能据一个 5QI 数值断言接纳成功、带宽已保证或完成 MCX 业务映射；也不能把 EPS 的 QCI 配置直接复制成整个 5GS 配置。

## 来源与边界

Not an MCX traffic-class mapping, PCC rule implementation, 5QI table or EPS/5GS interworking verification.

Referenced TS23.502/23.503/24.501 mechanisms remain unchecked; V19.9.0 equivalence not asserted.

[精确条款与结构化条件](5gs-qos-model.json)，[来源目录](../../sources.json)。

- [EPS 信令承载](eps-signalling.md)
- [GBR 通知控制](5gs-notification-control.md)

普通 MCPTT 的有限业务用途另见[语音 QoS 与 SIP 信令的边界](mcptt-5gs-voice-qos-scope.md)。该页独立依据 TS23.289 V19.7.0（Stage2），不扩大本页 TS23.501 V19.8.0 的已核条款，也不证明两者精确版本组合的完整互通、Stage3 流绑定或实际语音交付。
