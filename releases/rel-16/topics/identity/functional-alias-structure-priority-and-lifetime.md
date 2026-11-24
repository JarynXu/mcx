# 功能别名如何组成，谁能设优先级和期限，何时自动启停？

**别名可由在组织内有含义的元素组合（-014）。** 例如，别名可包含组织、岗位、任务或设备等信息。条文用示例说明组成方式，没把分隔符或字段写成强制语法。[R-5.9a-014，印刷页 23](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=24)。

| 要处理什么 | 标准要求 |
| --- | --- |
| 用外部信息创建或删除（-015） | 系统须允许管理员利用外部来源的信息创建或删除别名，例如运行排班、位置、速度或方向。信息变化不等于外部系统已经改动别名。[R-5.9a-015，印刷页 23](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=24)。 |
| 设置通信优先级（-016） | 系统须允许管理员为别名指定**通信优先级**。这不规定承载等级，也不表示一次通信已取得资源或发生抢占。[R-5.9a-016，印刷页 23](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=24)。 |
| 设置期限（-017） | 系统须允许管理员为别名设定期限。期满后别名**停用**，不是删除别名定义。条文未规定起算点。[R-5.9a-017，印刷页 23](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=24)。 |
| 按业务运行条件自动启停（-018） | 业务须支持按运行条件自动启用和停用别名。MCX 用户 ID、登录或退出业务系统、外部系统提供的特定信息，都是条件的例子。不能据此认定任何一次登录、退出或外部更新一定触发启停。[R-5.9a-018，印刷页 23](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=24)。 |

这是 3GPP TS 22.280 V16.8.0（Release 16，Stage 1）[第 5 章的在网和离网共用要求，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)。规范性[表 A.1（MCPTT），印刷页 64](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=65)、[表 B.1（MCVideo），印刷页 75](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=76)、[表 C.1（MCData），印刷页 86](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=87)。三表在 5.9A 功能别名行组均列 -014 至 -018。

若问题是占用时还能否启用，查[逐别名的占用策略和接管](functional-alias-activation-conflict-and-takeover.md)。若要对照在网 Stage 2 的[终端收到别名配置](functional-alias-configuration.md)或[按规则自动启停](functional-alias-automatic-activation.md)，读相关程序。一次在网通信的应用优先级怎样分配或映射，另见[应用优先级要求](../bearers/onnetwork-application-priority-assignment.md)。
