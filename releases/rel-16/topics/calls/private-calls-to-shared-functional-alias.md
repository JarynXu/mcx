# 一个功能别名同时有多名使用者时，业务怎样处理私呼？

**同一个别名已经由多人同时启用。** 比如“东区值班”当前由甲、乙都启用。对这个别名，业务须支持普通私呼，也须支持紧急私呼（-023）。这说的是打到**同一个别名**，不是甲自己启用了多个别名，也不要求把电话打给甲乙两人、只打给其中某人或采用先接先得。

**这个别名允许多人同时启用。** 就算此刻只有一人使用，-024 也要求业务让管理员能选择该别名的私呼处理机制。条文没给默认方式，不规定逐个呼叫、同时振铃、优先顺序或计时器。-023 明列紧急私呼；-024 写的是私呼，不能据此认定紧急私呼一定使用同一机制，也不能据此排除其使用同一机制。能选机制不等于已选定某种方式，更不证明某通电话已经接通。

3GPP TS 22.280 V16.8.0（Release 16，Stage 1）第 5 章是在网、离网共用要求，不是信令过程。[第 5 章，印刷页 12](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=13)；[§5.9a.2，印刷页 23](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=24)。

-023 在[表 A.1（MCPTT，印刷页 64）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=65)、[表 B.1（MCVideo，印刷页 75）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=76)、[表 C.1（MCData，印刷页 86）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=87)都按正文编号列出。-024 的 B.1、C.1 逐字列 `R-5.9a-024`；A.1 的同一节对应列印的是 `[R-5.9a-024`，有前导方括号且未闭合。这个对应格可以按节、位置、尾号和正文对照，不能写成三表逐字一致，也不能当作 MCPTT 明确不适用。

相关问题：[按位置路由及别名私呼授权](functional-alias-private-routing-and-authorization.md)；[查当前谁在使用别名](../identity/active-functional-alias-lookup.md)；[组织内判重与别名可达性](../identity/functional-alias-group-use-and-reachability.md)；[在网端的别名配置过程](../identity/functional-alias-configuration.md)。
