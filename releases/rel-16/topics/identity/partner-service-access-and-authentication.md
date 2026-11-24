# 用户到伙伴 MCX 系统开展业务：谁授权，认证参数从哪来？

**两侧都要授权。** 例如，甲是林的主 MCX 系统，乙是伙伴。业务须能让林在乙开展业务，但甲和乙都要准许。在移动网已能漫游，或者在乙通过了用户身份认证，都不能代替甲、乙的业务授权。[§6.17.2，R-6.17.2-001，印刷页 48](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=49)

**用谁的参数认证谁？** 林在乙向某项 MCX 业务认证，认证须基于从林的主系统甲取得的安全参数。被认证的是林，不是乙的业务；这是应用层的认证，不是 3GPP 网络认证。条款规定参数来源，没有要求乙在每次认证时都实时查询甲，也没有指定凭据格式。[R-6.17.2-002 及注 1，印刷页 48](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=49)

**如果还需要受访移动网提供功能，**这些功能受漫游能力和运营方协议约束。这里的受访 PLMN 是移动网；甲、乙则是 MCX 业务系统。运营方有漫游协议不能代替甲乙授权，两侧的业务授权也不能保证受访网能提供所需功能。[R-6.17.2-003，印刷页 48](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=49)

这是 [3GPP TS 22.280 V16.8.0（Release 16，Stage 1）第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30) 的在网要求。[表 A.1（MCPTT），印刷页 69](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=70)、[表 B.1（MCVideo），印刷页 80](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=81)、[表 C.1（MCData），印刷页 91](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=92)均列出R-6.17.2-001 至 -003。

迁移时要按所选用户配置档检查哪两侧的许可，见[Stage 2 迁移业务授权](partner-migration-authorization.md)；要查移动网、APN 和 SIP 核心的选择，见[迁移网络接入](../bearers/partner-migration-network-access.md)。若终端要验证的是业务本身的身份，见[终端要求认证业务](../security/service-authentication-requirements.md)。
