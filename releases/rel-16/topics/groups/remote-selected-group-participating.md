# 远程换组的 MESSAGE 在哪一跳被拒？发起与终接参与功能怎样转送？

在网 MCPTT。甲要求乙选中组 G，变更请求从甲发给乙；乙另发一条 MESSAGE 报告结果，方向是乙到甲。**发起参与功能（O-PF）服务这条 MESSAGE 的发送者，终接参与功能（T-PF）服务这条 MESSAGE 的收件人。** 查结果时，乙侧是 O-PF，甲侧才是 T-PF。以下依据 3GPP TS 24.379 V16.14.0（Release 16，Stage 3）。

## 甲的名单里有乙，为什么 O-PF 仍可能回 403/155？

先查 O-PF 实收的那条 MESSAGE。对于变更请求和业务结果，O-PF 都用 SIP `P-Asserted-Identity`（PAI）中的**发送者公共用户标识**查其 MCPTT ID；这项绑定在业务授权时建立。找不到绑定或现有绑定已过期，O-PF 须回 **404 / Warning 文本 141** 并停止。只有 `request-type=group-selection-change-request` 才继续检查用户配置中的 `RemoteGroupSelectionURIList`。缺少含至少一个条目的名单，或按第 3 项比对不匹配，O-PF 须回 **403 / Warning 文本 155** 并停止。带 `response-type=group-selection-change-response` 的结果 MESSAGE 仍查发送者绑定，但不重做第 3 项的名单检查。[§10.1.4.3.1 第 1–4 项，印 310](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=311)。

这里有一处不能用“甲的名单里有乙”解释过去：

| 在哪里检查 | 固定版本怎样写 |
| --- | --- |
| 甲的客户端 | 用目标用户乙的 MCPTT ID 匹配甲配置的名单。发请求时，MCPTT 信息正文的 `mcptt-request-uri` 填**组 G**，乙的 MCPTT ID 放在**资源列表正文**中。 |
| O-PF 第 3(a)(ii) 项 | 指定用入站 MCPTT 信息正文 **`mcptt-request-uri` 中的 MCPTT ID** 匹配名单，并未指向资源列表中的乙。紧接着第 4 项又把同一元素中的值称为**组标识**，按它确定控制功能（CF）。 |

[客户端 §10.1.4.2.1，印 308](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=309)；[O-PF §10.1.4.3.1，印 310](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=311)。这是两个检查点，也是本版文字之间的差别。诊断 155 时，要核对 O-PF 实收的两份正文、本次采用的名单和实际比对值。不能凭客户端已放行认定网络也应放行，也不能据此要求部署把组 G 加入名单，或擅自改为读取资源列表。若只有返回给甲的 403，还要确认**哪一跳生成了它**：[CF 自己的服务标签检查和归属资格检查](remote-selected-group-controlling.md)也可能回 403，其中资格拒绝用的是 Warning 文本 120。

## 从组 G 路由到用户乙，两个 404 分别查谁？

| 本条 MESSAGE 去向 | 成功转送时如何寻址 | 若在本地查不到绑定 |
| --- | --- | --- |
| O-PF → CF | 按入站正文的组 G 选择 CF，SIP Request-URI 写 **CF 的公共服务标识**。O-PF 复制 MCPTT 信息正文和资源列表，把按入站 PAI 查得的发送者 MCPTT ID 写入 `mcptt-calling-user-id`；出站 PAI 沿用入站的公共用户标识。 | 查的是**发送者**，无绑定或过期是 404/141。 |
| CF → T-PF → 收件人 | CF 从入站资源列表取**本条消息的收件人**，把其 MCPTT ID 写入出站正文的 `mcptt-request-uri`，把组 G 写入 `mcptt-calling-group-id`，SIP 目标是该收件人的 T-PF。T-PF 用实收的 XML `mcptt-request-uri` 查绑定；向客户端发 MESSAGE 时，SIP Request-URI 写绑定的**收件人公共用户标识**。 | T-PF 查的是**收件人**，绑定不存在则回 404。该步骤没有规定附上 141，也没有另列发起侧的过期条件。 |

变更请求的收件人是乙；业务结果的收件人是甲。O-PF 和 T-PF 遇到资源不足或拥塞风险都**可以**回 500，也**可以**带 Retry-After。要定位一次 404，先按业务类型和方向认出本条 MESSAGE 的发送者、收件人，再核各跳实际收到的响应与本机生成的响应。仅凭发送端看到的 404，不能断定是本端绑定还是对端绑定有问题。[§10.1.4.3.1–2，印 310–311](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=311)；[CF §10.1.4.4，印 312](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=313)；[终接 MESSAGE 构造 §6.3.2.2.11，印 103](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=104)。

## 若乙回 202，甲会看到 202 还是 200？

若变更请求送到乙，乙对这条 MESSAGE 回 SIP 202，T-PF **转送收到的 202** 给 CF。CF 收到该 2xx 后，**生成 200** 给 O-PF；O-PF 收到 2xx 后也**生成 200** 给甲。202 只是用来区分“转送 2xx”和“生成 200”的例子，并不要求乙使用 202。下游回 4xx、5xx 或 6xx 时，T-PF、CF、O-PF 各把收到的错误转给自己在本条 MESSAGE 上的上游。[§10.1.4.3.1–2 的响应处理，印 311](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=312)；[§10.1.4.4 末两段，印 313](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=314)。

甲收到的 200 不是乙的换组结果。要判断甲获知了什么，找**乙发给甲的另一条结果 MESSAGE**，读 `selected-group-change-outcome`。如果返回途中乙的 O-PF 因没有有效的乙方绑定而回 404/141，能定位的是**结果没能从这条腿送出**，不能倒推乙先前未换组。成功或失败怎样由乙判定，见[远程选组的两个客户端](remote-selected-group-client.md)。[§10.1.4.2.1–2，印 308–310](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=309)。
