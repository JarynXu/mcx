# 初次 SIP 注册没有访问令牌，要等 MCX 业务授权吗？

不用等。**初次 SIP 注册不能因为没有 MCX 访问令牌而延迟。** 终端先发不带令牌的 REGISTER，注册照常办理。终端仍须按 C-3 向要授权的 MCX 服务器提交访问令牌。只看到注册成功，只能判断 SIP 核心已完成这次注册，不能给 MCPTT、MCVideo 或 MCData 记“已获授权”。[TS 33.180 V16.13.0，§5.1.3.2.1，印刷页 33](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=34)

## 令牌经哪条请求送到业务服务器？

实现可选用 REGISTER 或 PUBLISH，经 SIP-1、SIP-2 送令牌。C-3 指的是向 MCX 服务器提交令牌。该步骤仍引用本节的两种请求，没有另指定缺令牌时必须改用 PUBLISH。[C-3，印刷页 32](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=33)并非每份 REGISTER 或 PUBLISH 都必须带令牌；不能反推业务授权本身可省。[§5.1.3.2.1–.3，印刷页 33–35](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=34)

| 选用的请求 | 令牌在哪一段交给谁 | 哪一端验证和绑定 |
| --- | --- | --- |
| **REGISTER** | 终端在 REGISTER 中提交令牌。SIP 核心完成 SIP 认证后，经第三方 REGISTER 把令牌转给 MCX 服务器。图中第 8 步是 SIP 核心给终端的 2xx 注册成功响应；第 9 步才是发往 MCX 服务器的第三方 REGISTER。 | MCX 服务器验证令牌。令牌有效时，服务器将 **IMS 公共用户身份（IMPU）**与对应的 **MC 业务 ID** 绑定。图中第 11 步是服务器给第三方 REGISTER 的响应，不是第 8 步给终端的响应。[§5.1.3.2.2、图 5.1.3.2.2-1，印刷页 33–34](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=35) |
| **PUBLISH** | 授权用 PUBLISH 经 SIP 核心送到 MCX 服务器。只看到 PUBLISH 这个方法名，不能判断这笔请求是否携带令牌办理授权。 | MCX 服务器验证令牌，有效时绑定 IMPU 与对应业务 ID，并对这笔 PUBLISH 作响应。图画的是 200 OK 的流程，没有规定无效令牌一定回哪个状态码。[§5.1.3.2.3、图 5.1.3.2.3-1，印刷页 34](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=35)；[续页 35](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=36) |

排查时先把响应对到原请求，再找 **MCX 服务器对该次令牌的验证结果**和**为哪项业务建立了什么绑定**。查 MCVideo 就核对 MCVideo ID；MCPTT 的授权结果不能替代它。令牌已送达、SIP 核心已应答，或日志里出现一条未对上事务的 200，都不足以确认本次绑定。这里不需要抄录令牌内容。

## 终端重注册或换人，能沿用原绑定吗？

若 SIP 注册前已有访问令牌，或终端掉注册后须重注册，条文允许在 REGISTER 中带令牌，不要求为了携带令牌而重新认证 MC 用户。SIP 层的认证和业务服务器对令牌的验证仍是两件事。

若 **IMPU 或 MC 业务 ID 其中一项变了**，终端可经 SIP 提交访问令牌，供 MCX 服务器重做绑定。终端掉注册后换了 IMPU，或同一台终端换了登录用户，都是条文所举的例子。条文没有规定只要发生重注册就必须重绑，也没有说旧令牌或旧绑定会自动适用于新用户。[§5.1.3.2.1，印刷页 33](https://www.etsi.org/deliver/etsi_ts/133100_133199/133180/16.13.00_60/ts_133180v161300p.pdf#page=34)

这是 Release 16 的 MC 安全过程。若问题是[主系统登录时何时认证用户、何时报 SIP 注册成功](home-system-authentication.md)，查 Stage 2 流程。若要按抓包核对[MCPTT 共享 REGISTER、授权用 PUBLISH 的正文或失败码](shared-sip-registration.md)，查 Stage 3 的 MCPTT 专用程序；不要把专用字段套给 MCVideo 或 MCData。LMC 向 LMS 发位置消息是[另一项令牌检查](../location/lmc-lms-access-token.md)。
