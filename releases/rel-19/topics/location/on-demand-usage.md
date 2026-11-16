# 按需使用位置：先取得位置，再回报

适用：单个 MC 系统，TS23.280 V19.9.0 §10.9.3.6.2；目标 LMC 已有位置报告配置。

请求来自 LMC 时，LMS 检查请求权和目标向该请求者分享位置的权限。MC 服务服务器在本流程中隐式可信，无需对该服务器作这一授权检查，不能推广到其他主体。

LMS 根据请求信息触发按需报告，或从 PLMN 获取最新位置，然后立即回报已获取的信息。“立即”不证明定位测量零延迟或特定精度。可选 UE label 不发给 MC 服务服务器。

[条款与条件](on-demand-usage.json)、[来源目录](../../sources.json)。底层§10.9.3.2的已核采集行为见[配置与上报](report-acquisition.md)；PLMN LCS及完整协议编码仍未核；不把此版本结论冒充旧 V19.10.1 摘要已核。

按问题续读：[位置权限要求](privacy.md)、[MC/LMR 互通查询](../interworking/location-query.md)。

令牌与逐条消息校验另见[服务授权](../identity/service-authorization.md)中的位置分支，来源TS33.180 V19.4.0。
