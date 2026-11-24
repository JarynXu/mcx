# 终端进出预设区域，哪些业务须支持触发或取消紧急告警？

在 **MCVideo、MCData** 中，MCX 终端移入预设区域，业务须提供以进区为条件触发**业务紧急告警**的机制。判断的是告警，不是组呼是否建立，也不是某个调度员是否收到了位置报告。见 3GPP TS 22.280 V16.8.0（Release 16，Stage 1） [R-5.1.9-001，印刷页 14](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=15)。

终端离开预设区域，告警有两种可能：随离区取消，或继续有效，直到 MCX 用户取消。对第一种，条文没有指定谁执行取消；对第二种，条文明写 MCX 用户。不能只凭一次离区记录判定告警已取消，也不能反过来认定只能手动取消。本项没有指定默认分支或选择分支的人。见 [R-5.1.9-002，印刷页 14](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=15)。

**两条都是在网和离网共用的 Stage 1 能力要求**，见[第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)。[表 A.1（MCPTT），印刷页 62](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=63)、[表 B.1（MCVideo），印刷页 73](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=74)、[表 C.1（MCData），印刷页 84](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=85) 的 §5.1.9 行中，A.1 明写 NA，B.1、C.1 均列 -001 和 -002。不能据此要求 MCPTT 满足这两条；也不能由 A.1 的这一行断言 MCPTT 没有自己的区域通知程序。

若问**同一 MC 系统内的在网流程**，见[Stage 2 进区或离区的服务器与客户端分工](emergency-alert-area-entry-exit.md)。若手里是 **MCPTT 客户端的区域通知**，应查[Stage 3 区域指示、应答和本机状态](area-alert-notification.md)。另一个问题是按位置把告警路由给哪个调度员，见[在网调度员与地理区域的关联](onnetwork-location-dependent-dispatch-areas.md)。这些程序和路由条件不是 §5.1.9 的触发器实现要求。
