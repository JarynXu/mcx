# 私呼路由表 H.3-1：被叫放在哪个字段，200 必须回被叫 ID 吗？

**实现私呼时，不要把资料性附录 H 的路由表当报文模板。** 以同一 MC 系统归属网内、带话权控制的普通按需 MCPTT 私呼为例，甲呼叫乙。路由表和主程序在两处用了不同的字段名：一处是控制功能（CF）邀请终接参与功能（T-PF）的 INVITE，另一处是 T-PF 回给 CF 的应答。先对上报文方向，再看主程序和 XML 定义。[TS 24.379 V16.14.0，Rel-16 Stage 3，表 H.3-1，印 597](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=598)。

## CF 发出的 INVITE：要绑定的是乙，不是头部断言的甲

| CF → T-PF 的位置 | 按主程序放什么 |
| --- | --- |
| SIP 请求行 `Request-URI` | 服务乙的 T-PF 的公共服务身份（PSI），不是乙的 MCPTT ID。 |
| `P-Asserted-Identity` | 从入向 INVITE 复制甲的公共用户身份（IMPU）。这个头不是被叫选择键。 |
| `application/vnd.3gpp.mcptt-info+xml` 的 `mcptt-request-uri` | 从入向资源列表复制**乙的 MCPTT ID**。同一正文的 `mcptt-calling-user-id` 是甲的业务 ID。 |

附录 H.3 这一行把乙的 ID 列在 `mcptt-called-party-id`。**主程序 §11.1.1.4.1 第 4 项却写 `mcptt-request-uri`，T-PF 在 §11.1.1.3.2 第 4 项也读这个元素**，用它取乙的 MCPTT ID 与公共用户身份的绑定。抓包只看见 `mcptt-called-party-id`，不能认为 T-PF 已拿到了该步骤规定的查找键。`mcptt-called-party-id` 本身是规范所定义的另一元素，不是拼错的 `mcptt-request-uri`。[§11.1.1.4.1 第 1、4–6 项，印 378–379](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=380)；[§11.1.1.3.2 第 3–5 项，印 377](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=378)。

若已走到按乙的业务 ID 查绑定的步骤，且绑定不存在，T-PF 须回 404。若记录没保留完整 XML、缺该元素或请求更早就被拒，不能拿这条“绑定不存在”的规则替缺字段指定统一响应。也不能拿 PSI、甲的 PAI 或相邻响应里的乙 ID 来补这笔请求的证据。[§11.1.1.3.2，印 376–377](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=378)。

## T-PF 回 CF 的 200：先查它有没有要复制的正文

表 H.3-1 的 T-PF→CF 响应行写的是 `mcptt-called-user`。F.1.2 的业务 XML 定义列的是 `mcptt-called-party-id`，并标为可选；F.1.3 说明该元素可以表示终接用户的 MCPTT ID。本版没有把表里的 `mcptt-called-user` 定义为该元素的别名。另有语法扩展入口，不等于这两个名字可以互换，也不据此规定未知元素的一般 SIP 拒绝码。[F.1.2，印 545–546](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=546)；[F.1.2 扩展类型，印 546](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=547)；[F.1.3，第 5 项，印 548](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=549)。

以乙**按需自动接听**为例，§6.3.2.2.5.2 要求 T-PF 按最终响应通则为 **CF 的 INVITE** 生成 200。通则只在乙的**入向 SIP 应答**已经带有 `application/vnd.3gpp.mcptt-info+xml` 时要求复制这份正文。该规则不要求 T-PF 在没有这份正文时另造一个被叫字段。不要把 PRACK 的 200 配给 INVITE，也不要把终端回给 T-PF 的一笔应答直接当成 T-PF 已转出的应答。**验收先分别对上两条腿各自的 INVITE 和 200，再比较 T-PF 实际收到和发出的正文。不应要求每份这种私呼 200 都带 `mcptt-called-user`，也不能据缺此字段判断没接听。**[§6.2.3.1.1，印 58–59](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=59)；[§6.3.2.2.5.2，印 97](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=98)；[§6.3.2.2.4.2 第 5 项，印 95](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=96)。

要查普通私呼还有哪一步准入或拒绝，读[私呼服务器准入与路由](private-server-admission-routing.md)。要判断终端是自动应答、人工应答，还是只有临时响应，查[私呼客户端接听证据](private-client-answer-evidence.md)。要分清公共用户身份、业务用户身份和终端标识，查[同一用户跨业务和终端的身份映射](../identity/cross-service-user-mapping.md)。这些区分也不回答 T-PF 地址怎么发现或通话媒体是否已经到达。
