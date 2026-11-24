# 业务组的层级决定某次组通信的优先级吗？

不能只按一个组处于上级还是下级，就断定哪次通信更优先。3GPP TS 22.280 V16.8.0（Release 16，Stage 1） 把两项能力分开写在 §5.1.7；[第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13) 的范围包括在网和离网。

- **组织的是业务组。** 业务须提供机制，能把 MCX 业务组组织成一个或多个层级结构。条文没有指定层数，也没有写上级组是否继承或支配下级组的优先级。见 [R-5.1.7-001，印刷页 13](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=14)。
- **排序的是组通信。** 业务须提供机制，按通信要素各自关联的优先级，确定 MCX 业务组通信的优先顺序。业务类型、请求方身份、目标方身份均为例子。条文没有要求只用这三项，也没有给它们规定固定权重或冲突时的胜出顺序。见 [R-5.1.7-002，印刷页 13](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=14)。

[表 A.1（MCPTT），印刷页 62](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=63)、[表 B.1（MCVideo），印刷页 73](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=74)、[表 C.1（MCData），印刷页 84](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=85) 的 §5.1.7 行均逐号列出这两项，适用于 MCPTT、MCVideo 和 MCData。

若问在网管理员如何设置**组传输**的优先级层级，见[管理员配置组传输、业务组及子集的优先级](onnetwork-group-priority-administration.md)。若问不同通信在**传输、呈现**上的动态相对优先级，见[在网组通信间的比较](onnetwork-group-communications-priority.md)。离网业务使用哪些属性来确定通信优先级，见[离网通信优先级](../bearers/offnetwork-communication-priority.md)。这些条款各有自己的对象，不能从业务组的组织层级推断一次抢占结果。
