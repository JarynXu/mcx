# 管理员怎样给用户配置档命名？暂停配置档和删除配置档是一回事吗？

给甲的一份用户配置档改名，改的是用来识别这份档的信息。暂停这份档，操作对象是档本身。两项都是 MCX 业务须为业务管理员提供的管理能力。

**分配或修改档的标识信息。** 管理员须能指定并修改 MCX 业务用户配置档的标识信息；名称、标识符、别名是条文给的例子，并非三个都要填。给档改别名，不等于更改甲的业务用户 ID 或启用甲的功能别名。如果改的是[业务组的名称或别名](../groups/group-membership-administration.md)，对象已经不同。[R-5.17-005，印刷页 27](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=28)。

**管理档本身。** 管理员须能**创建、修改、删除和暂停** MCX 业务用户配置档。暂停和删除分开列出；仅凭一份档已暂停，不能判断该档已删除、甲的账号已停用、另一份档也被暂停，或正在进行的通信已结束。条文没有规定四项操作的先后顺序，也没给出暂停后恢复的步骤。[R-5.17-007，印刷页 27](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=28)。

“业务支持管理员这样做”不替某个具体管理员授权。有关[管理员权限内的用户配置档、在用档的修改和终端安装时机](user-profile-management-requirements.md)，以及[同系统内不同组织如何指定管理员、隔离管理参数](shared-system-organization-management.md)，各有自己的要求。[在网管理员操作日志和变更何时生效](onnetwork-administrator-activities-and-change-timing.md)也不是 §5.17 的内容。若要判断终端是否取得配置变更、客户端写回是否成功，另查 [Stage 2 的用户配置档数据更新](user-profile-data-update.md)。

3GPP TS 22.280 V16.8.0（Release 16，Stage 1）把 §5.17 放在在网、离网共用的[第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)。规范性表 [A.1（MCPTT），印刷页 64](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=65)、[B.1（MCVideo），印刷页 75](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=76)、[C.1（MCData），印刷页 86](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=87) 的 §5.17 行均列出 -005 和 -007。
