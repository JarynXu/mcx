# 没有任何固定基础设施时，谁能使用离网 MCX 业务？

**没有任何固定基础设施，离网 MCX 业务也必须能运行；只有获授权的用户才能使用。** 这是业务必须具备的能力和使用业务的必要条件，不是说只要两台终端能互通，两名用户就都已获准。见 [TS 22.280 V16.8.0 §7.10，R-7.10-001、-002，印刷页 55](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=56)。

谁来给用户授权？MCX 业务必须提供一种机制，让 **MCX 业务管理员**能授权用户使用离网 MCX 业务（[R-7.10-003，印刷页 55](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=56)）。这项要求说的是业务要给管理员什么能力，没规定授权必须在离网前还是在现场办理，也没指定凭据或检查方法。反过来，规定了授权机制，不等于某个用户已经获准。

这是 Release 16 的 Stage 1 离网要求（[第 7 章，印刷页 50](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=51)）。规范性[表 A.1（MCPTT，印刷页 70）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=71)、[表 B.1（MCVideo，印刷页 81）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=82)、[表 C.1（MCData，印刷页 92）](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=93)均列出 §7.10 的三项要求。

如果这次通信仍通过回传已中断的 LTE 站点接入，查[孤立网的本地 MCPTT 能力](../bearers/iops-local-mcptt-service.md)。终端虽然仍在站点覆盖内，这次通信若走离网直连，仍按离网要求判断。

若要判断谁给离网终端配置参数或组资料，见 [Stage 2 的离网配置角色](../groups/offnetwork-configuration-roles.md)；若要核对离网 MCPTT 客户端怎样探测或加入普通组呼，见 [Stage 3 的离网普通组呼](../calls/offnetwork-group-client.md)。配置下发记录或一次组呼公告，本身都不能证明管理员已经授权这名用户使用离网业务。
