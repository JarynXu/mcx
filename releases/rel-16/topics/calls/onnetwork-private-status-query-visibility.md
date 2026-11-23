# 在网私通信：谁能查用户在网和参与能力，管理员能配什么？

**用户在网，不等于能参加私通信。** 对这两项信息，分别看谁可以查询、管理员能否配置是否提供、又能否配置哪些用户可以获知。依据是 3GPP TS 22.280 V16.8.0（Release 16）的在网私通信 Stage 1 要求。以下六条都用 **should（宜）**，未以有无话权控制限定适用范围。[第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)；[§6.7.2，印刷页 37（PDF 第 38 页）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=38)；[§6.7.3，印刷页 38（PDF 第 39 页）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=39)。

| 要查的信息 | 业务宜向获授权 MCX 用户提供的查询机制 | 业务宜向 MCX 业务管理员提供的配置机制 |
| --- | --- | --- |
| 某位 MCX 用户是否在网（present on the network） | 查询该用户是否在网。[R-6.7.2-001，印刷页 37](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=38)。 | 配置该用户的在网信息**是否可供获知**。[R-6.7.3-001，印刷页 38](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=39)。另宜提供机制，让管理员配置**哪些 MCX 用户**能确定该用户是否在网。[R-6.7.3-002，印刷页 38](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=39)。 |
| 某位 MCX 用户是否能参加私通信 | 查询该用户是否具备参加私通信的能力。[R-6.7.2-003，印刷页 37](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=38)。 | 配置该用户的私通信参与能力信息**是否可供获知**。[R-6.7.3-003，印刷页 38](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=39)。另宜提供机制，让管理员配置**哪些 MCX 用户**能确定该用户是否具备这一能力。[R-6.7.3-004，印刷页 38](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=39)。 |

例如，甲获准查询乙是否在网，并查到乙在网。甲不能据此认定乙能参加私通信，也不能把这一查询权限当成获准查看乙的参与能力。管理员配置某项信息可供获知，并没有改变乙的实际在网状态或能力，也不表示可以向未获授权者披露。条款没有规定默认可见性、这几项设置的先后或怎样合并、怎样处理一次无权查询，也不保证一次查询返回结果。

这些推荐机制不以已经建立私通信为前提；查询参与能力也不以先证实目标用户在网为前提。本节不规定怎样计算参与能力，不指定 SIP Presence、身份绑定或报文，也不能用查询结果证明本次通信获准、已接听或已建立。

**适用业务：** 表 A.1（MCPTT）、B.1（MCVideo）、C.1（MCData）均在相应要求行明确列出上述六项。[表 A.1，印刷页 67](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=68)；[表 B.1，印刷页 78](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=79)；[表 C.1，印刷页 89](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=90)。

另查[谁可发起无话权控制私通信及可联系谁](onnetwork-no-floor-private-authorization.md)、[组归属与选定状态](../groups/onnetwork-group-status-information.md)或[多终端登录](../identity/multiple-device-login.md)时，分别看各自的 Stage 1 要求。若问[在网 MCVideo 自动私呼](../mcvideo/onnetwork-automatic-private-call.md)或[普通在网 MCPTT 私呼服务器准入](private-server-admission-routing.md)，按 Stage 2 或 Stage 3 的具体条件核对；那些过程不是这里的两种查询或四种可见性配置。
