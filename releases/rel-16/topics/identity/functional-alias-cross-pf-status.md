# MCPTT 跨参与功能查别名状态：乙侧从哪里认出查询者甲，何时回 403？

甲要知道**乙已经启用了哪些功能别名**。甲、乙由不同的参与 MCPTT 功能（PF）服务。甲的客户端先找服务于甲的起始参与功能（O-PF）；转发时，目标变成服务于乙的终接参与功能（T-PF）。**乙侧 T-PF 从正文的 `mcptt-calling-user-id` 识别甲，不把服务器间的 P-Asserted-Identity 当成甲的用户身份。** 这是按用户查状态，不是把某个别名解析成一份用户名单。[TS 24.379 V16.14.0 §§9A.2.1.3、9A.2.2.2.4、9A.2.2.2.9，印 200–201、205、210–211](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=211)

## 先对两段 SUBSCRIBE，别把目标用户和下一跳混在一起

| 抓到的位置 | 去哪、怎样认人 |
| --- | --- |
| 甲的客户端发起查询 | SIP Request-URI 填甲侧 O-PF 的公共服务身份（PSI）；业务正文的 `mcptt-request-uri` 填**乙的 MCPTT ID**，`request-type` 为 `functional-alias-status-determination`。 |
| O-PF 收到发给自己的、符合 §9A.2.2.2.9 入口的请求，发现不服务乙 | 从正文取乙的 MCPTT ID，从入站 `P-Asserted-Identity` 中的公共用户身份识别甲。新请求的 SIP Request-URI 写乙侧 T-PF 的 **PSI**；新 `P-Asserted-Identity` 写**甲侧 O-PF 的 PSI**。新正文的 `mcptt-request-uri` 继续写乙，`mcptt-calling-user-id` 写甲的 **MCPTT ID**。 |
| T-PF 收到满足 §9A.2.2.2.4 的本地服务入口的请求 | 正文 `mcptt-request-uri` 仍是被查询的乙；因为请求发给的是 T-PF，查询者从正文的 `mcptt-calling-user-id` 取。如果另一个案例是 O-PF 自己服务被查用户，进入的是该条的 O-PF 入口，从 `P-Asserted-Identity` 的公共用户身份识别查询者。 |

[§9A.2.1.3 初始客户端请求，印 201](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=202)；[§9A.2.2.2.9 入口与身份，印 210](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=211)、[出站字段，印 211](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=212)；[§9A.2.2.2.4 接收身份，印 205](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=206)

准备判断终接是否应处理时，查**终接实际收到的请求**。§9A.2.2.2.4 的入口还核实目标由本服务器服务、MCPTT 的 `P-Asserted-Service`、`Event: presence` 及正文内的 `functional-alias-status-determination`。转发条款 §9A.2.2.2.9 列了它自己的入口，生成步骤逐项列出两个用户字段并要求包含其他接收信令元素；它没有把终接的 `request-type` 检查列为转发入口条件。该转发入口对 MIME 名的文字也与生成步骤略不同（未写 `+xml`）；本页不据此制定 MIME 容错或追加规则。[§§9A.2.2.2.4、9A.2.2.2.9，印 205、210–211](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=211)

## 查别名状态，为什么拒绝条件却提到“修改”？

按 §9A.2.2.2.4，**查询者 MCPTT ID 与被查用户不同，且查询者无权修改对方的功能别名状态**，须回 SIP `403 (Forbidden)` 并停止该程序。这是这次状态订阅所用的权限条件，不是说 SUBSCRIBE 本身会改状态。查询者就是被查用户时，不触发这条「不同且无权」的拒绝；不能仅凭这一点跳过其他入口条件。本版此处不定义授权策略的完整实现。[§9A.2.2.2.4 步骤 1–4，印 205](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=206)

该程序的 **200 回的是这次 SUBSCRIBE**，不是乙的任何一个别名已启用。O-PF 转发相关订阅响应；在订阅有效期间，O-PF 也转发相应通知。到实际收到的 SIP NOTIFY 里查**按用户组织的 `application/pidf+xml` 正文**。服务乙的服务器构造此正文时，不纳入已过期、或状态为 `deactivated` 的条目信息。先对上乙与本次订阅，再读通知里的别名状态；没有抓到通知不能记成乙没启用别名。[§§9A.2.2.2.4–.5，印 206](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=207)；[§9A.2.2.2.9 末段，印 211](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=212)；[§9A.2.1.3，印 201](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=202)

如果问的是[客户端怎样提交启停别名、观察发布结果](mcptt-functional-alias-client.md)，读客户端程序。若从**一个功能别名 ID**出发，要查有哪些用户已启用它，读[别名属主侧解析订阅](alias-owner-resolution-subscription.md)，不按本页找被查询用户的 T-PF。
