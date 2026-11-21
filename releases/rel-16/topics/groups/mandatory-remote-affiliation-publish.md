# 强制变更他人的 MCPTT 组归属：跨 PF 的 PUBLISH 和结果取证

甲要求修改乙在客户端 C 上的组归属，两人由不同的参与 MCPTT 功能（PF）服务。抓包时，先认出这是一笔强制模式的 `presence` PUBLISH：请求修改的是乙在 C 上的归属，发起人是甲。不要沿用[协商模式的 SIP MESSAGE](negotiated-affiliation-client.md)，也不要把[查询他人归属的 SUBSCRIBE](other-user-affiliation-status.md)当成变更。

## 两段请求用相同的方法，身份字段的角色不同

| 抓包位置 | Request-URI | P-Asserted-Identity | MCPTT 业务正文 |
| --- | --- | --- | --- |
| 甲的起始 PF 收到的 PUBLISH | 服务甲的起始 PF 的公共业务标识（PSI） | 起始 PF 据其中的公共用户身份识别甲 | `mcptt-request-uri` 指向本 PF 不服务的乙的 MCPTT ID |
| 起始 PF 生成、发给乙侧的 PUBLISH | 服务乙的终接 PF PSI | 服务甲的起始 PF PSI | `mcptt-request-uri` 是乙的 MCPTT ID，`mcptt-calling-user-id` 是甲的 MCPTT ID |

起始 PF 的转发分支还检查 MCPTT 的 P-Asserted-Service、`presence` Event 和按用户组织的 `application/pidf+xml` 正文。它在生成请求时保留其他信令元素，并把收到的 SIP 响应转回。到乙侧，P-Asserted-Identity 标识甲侧 PF；终接 PF 从 `mcptt-calling-user-id` 认出甲，从 `mcptt-request-uri` 认出乙，然后核对甲能否修改乙。不要把乙的 MCPTT ID 放到 SIP Request-URI 当服务器地址，也不要因为两段的 P-Asserted-Identity 不同就认定发起用户变了。

固定版的 MIME 类型写法不一致：§9.2.2.2.9 的入站检查写 `application/vnd.3gpp.mcptt-info`；§9.2.1.2 的客户端构造、§9.2.2.2.9 的出站构造和 §9.2.2.2.3 的终接入口都写带 `+xml` 的类型。这两种写法怎样匹配，本版没有在这两条里说明。还有一处身份用语：§9.2.1.2 客户端构造第 2 项把 `mcptt-request-uri` 写作“该 MCPTT 用户”的 ID，没有像期限和 PIDF 项那样写明是目标用户。§9.2.2.2.9 的接收入口则明确要求这里标识起始 PF 不服务的目标。表格从**起始 PF 实际进入转发分支**讲起，不把接收条件反写成一套无歧义的客户端构造，也不规定怎样发现终接 PF。第 9 章适用 §6.6 的保护规则；表格不是信任自报身份的规则。

依据：[TS 24.379 V16.14.0，Rel-16 Stage 3，§6.6.1.1，印刷页 138](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=139)；[§9.2.1.2，印刷页 168–169](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=169)；[§9.2.2.2.9，印刷页 181–182](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=182)；[§9.2.2.2.3 入口及第 1–4 项，印刷页 173](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=174)。

## 终接 PF 已回 200，为什么乙的归属还没变？

在上述终接分支中，若甲无权修改乙的归属，终接 PF 须回 **403** 并停止。通过权限检查后，若 `Expires` 缺失，或为小于 4294967295 的非零值，须回 **423**，带 `Min-Expires: 4294967295`，并停止。零值走撤销兴趣分支，不是这项 423 的条件。

**终接 PF 先回 200，再检查 PIDF 的 `presence entity` 是否等于正文指向的乙。** 例如，业务正文指向乙，但 PIDF 的 `entity` 仍填甲，终接 PF 须停止后续步骤，即使已经回了 200。通过这项检查后，才从 PIDF 的 `tuple id` 识别乙的客户端 C，接着处理该客户端的组条目。不该把甲的客户端 ID 当成 C，也不该用一次 200 证明乙已经归属或解除归属。各组的兴趣列表、零期限和组宿主处理见[显式归属状态处理](explicit-affiliation-client.md)。

若要用归属状态确定程序获知这次变更的成功或拒绝，客户端须在发起变更前先启动对乙的状态确定。排查乙在 C 上对 G 的状态时，从订阅端看实际收到的、携有效按用户 PIDF 的 NOTIFY，按乙、C、G 逐项核对。若变更程序调用了通知生成程序且已识别本次 PUBLISH 的 `p-id`，生成的通知须带该值；有 `p-id` 可关联请求，仍要读 G 的状态。缺少通知不能证明成功或失败；通知没列 G 也不等于查到了本次解除成功，已到期、已解除或被过滤的条目可能不在报告里。归属状态不证明乙接听了某一场组呼。

依据：[§9.2.2.2.3 第 4–19 项，印刷页 173–176](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=174)；[§9.2.1.1、§9.2.1.3，印刷页 167–170](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=168)；[§§9.2.2.2.4–.5，印刷页 176–177](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=177)；[§9.3.1.2，印刷页 194–196](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=195)。
