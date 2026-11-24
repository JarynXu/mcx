# IWF 定义的组，本地没有组配置：MC 系统找谁取？

MC 系统的组管理服务器（GMS）向 IWF 的组管理功能请求组配置，由 IWF 返回所请求的配置。这是 TS 23.283 V16.8.0 §10.2.3.5 的取配置流程，不是组归属请求。[§10.2.3.5，图 10.2.3.5-1 与正文，印刷页 30](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=31)

**什么时候适用？** 组定义在 IWF，至少有一名 MC 业务用户是组成员，MC 系统的 GMS 没有保存该组配置，且 MC 系统已配置 IWF 组管理功能的寻址信息。正在由该 MC 系统服务的用户在用户档里配置了这个组，是原文举的例子。用户档里有该组，不能据此认定 GMS 已保存组配置，也不能把这个例子当成唯一触发条件。[§10.2.3.5，图 10.2.3.5-1 与正文，印刷页 30](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=31)

**哪一边发请求？** 图 10.2.3.5-1 上，MC 系统的 GMS 先向 IWF 发送 IWF Group Information Provision Request，IWF 再向 GMS 返回 IWF Group Information Provision Response，提供所请求的配置。虽然图题用了“primary MC system”，图中标作组主系统的一边是 IWF；两步正文也明确写的是 MC 系统向 IWF 取配置，而不是两套普通 MC 系统交换配置。[§10.2.3.5，图 10.2.3.5-1 与正文，印刷页 30](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=31)

**谁负责把配置给用户？** 注释把这项责任交给该 MC 系统的 GMS，范围是以这个 MC 系统为服务系统的该组成员。IWF 返回配置不证明本地 GMS 已经保存，更不能证明终端已收到。本节未规定向终端交付的时机、订阅更新、失败处理或具体协议字段。[§10.2.3.5，图 10.2.3.5-1 与正文，印刷页 30](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/16.08.00_60/ts_123283v160800p.pdf#page=31)

要判断用户是否已办理归属，查[LMR 定义组的归属](lmr-hosted-mc-affiliation.md)；若问题是创建临时重组，查[MC 与 LMR 的动态重组](lmr-interworking-dynamic-regroup.md)；只有对端是另一个 MC 系统而非 IWF 时，才对照[两个 MC 系统间的组配置](partner-group-configuration.md)。
