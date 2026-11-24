# 在网终端能要求验证 MCX 业务本身的身份吗？

能。**提出要求的是 MCX 终端，被认证的是 MCX 业务。** 业务必须为终端提供这种方式；[TS 22.280 V16.8.0 §6.13.3，R-6.13.3-001，印刷页 44](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=45) 没有要求终端每次接入都使用它。

例如，一名用户已通过身份认证，终端已在 IMS 注册，用户也获准使用 MCPTT。这些结果仍不能证明终端要求过验证 MCPTT 业务的身份，更不能证明业务已通过验证。验证客户端的身份也不能代替验证业务。本条没有指定认证协议、交互端点、凭据、时机或失败处理，也没有要求双向认证。

这是 Release 16 的 Stage 1 要求。[第 6 章，印刷页 29](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=30)限定在网使用；规范性表 [A.1（MCPTT），印刷页 68](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=69)、[B.1（MCVideo），印刷页 79](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=80)、[C.1（MCData），印刷页 90](https://www.etsi.org/deliver/etsi_ts/122200_122299/122280/16.08.00_60/ts_122280v160800p.pdf#page=91) 都列出了这一项。

要区分“用户是谁”和“用户获准使用哪项业务”，看 [Stage 2 主系统登录](../identity/home-system-authentication.md)；要判断一份 REGISTER 是否也在申请 MCPTT 授权，看 [Stage 3 共享 SIP 注册](../identity/shared-sip-registration.md)。
