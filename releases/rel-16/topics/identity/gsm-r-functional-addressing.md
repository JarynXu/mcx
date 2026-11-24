# MCPTT、MCVideo 要与哪类 GSM-R 系统互通？用功能别名能找到哪一侧的用户？

对 MCPTT、MCVideo，MCX 业务系统须能与**同时符合 UIC GSM-R（EIRENE）标准 [9] 和 EN 301 515 [10]** 的 GSM-R 系统互通。条文后的注指出，要尽量减少对 GSM-R 的影响；没有要求对端零改造或指定网关。[§6.17.3.1，R-6.17.3.1-002 及注，印刷页 49](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=50)

MCX 系统还须让**功能别名**与 GSM-R 使用的**替代寻址方式**互通。条款没有规定两侧的地址须写成相同字符串，也没有规定转换方法。[R-6.17.3.1-003，印刷页 49](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=50)

| 想联系谁 | 别名可达性的要求 |
| --- | --- |
| GSM-R 用户 | 须能通过**由 MCX 业务系统激活的对应功能别名**联系到该用户。查到别名已经配置，不能当作它已被激活。[R-6.17.3.1-004，印刷页 49](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=50) |
| MCX 用户 | MCX 业务须允许通过功能别名，在 **MCX 业务系统或 GSM-R 系统**上联系到该用户。本项没有要求同一个别名同时在两侧注册。[R-6.17.3.1-005，印刷页 49](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=50) |

这是[3GPP TS 22.280 V16.8.0（Release 16，Stage 1）第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)的在网要求。[表 A.1（MCPTT），印刷页 69](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=70)和[表 B.1（MCVideo），印刷页 80](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=81)都列出 -002 至 -005。[附录 C 表 C.1 的说明，印刷页 84](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=85)将其定义为 MCData 适用项的穷举表；其[GSM-R 行，印刷页 91](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=92)只列位置互通 -001，**不列 -002 至 -005**。因此不能把这四项当作 MCData 必须满足的要求；未列也不是禁止实现。

要辨认 MCX 系统本身的用户 ID 和别名配置要求，见[在网身份与别名管理](onnetwork-id-and-alias-management.md)；若要分清给终端配置别名与该别名已激活，见[终端的功能别名配置](functional-alias-configuration.md)。
