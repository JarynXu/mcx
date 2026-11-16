# SDS服务器准入：主叫身份、控制功能与私聊目标

限在网、非紧急的standalone SDS控制面SIP MESSAGE；one-to-one目标直接使用MCData ID。预安排组只覆盖O-PF普通路由分支；排除ad hoc、TGI、重组、functional-alias解析、跨域网关和媒体面。

请求已经按§6.3.1.1识别为对应角色的standalone SDS输入：其Accept-Contact的g.3gpp.icsi-ref及P-Asserted-Service使用SDS ICSI。每条准入结论仅在前序检查未拒绝时适用。

O-PF、T-PF和CF均有资源不足或拥塞风险时可回500的入口；Retry-After为可选。本主题不把通过客户端发送选择或任一单项检查当成全链获准。

## PAI绑定确定主叫身份

适用条件：O-PF收到客户端的standalone SDS请求。

O-PF从P-Asserted-Identity中的public user identity确定主叫MCData ID并授权用户；绑定在服务授权时建立。绑定不存在或有效期已过，回404加Warning141并停止。随后向CF发送时，O-PF把所确定的主叫MCData ID写入mcdata-calling-user-id，而出站P-Asserted-Identity改为O-PF自己的PSI；不能把下游PAI中的服务器身份误当主叫用户ID。



依据：§9.2.2.3.1 steps2,3,12,14 and NOTE1，印刷页 195、196、197、198。

## 控制功能按业务和组选择

适用条件：O-PF已确定主叫身份，处理one-to-one-sds或普通非重组group-sds。

one-to-one-sds选承载主叫用户one-to-one standalone SDS服务的CF，不是直接跳到目标用户的T-PF。普通group-sds按mcdata-request-uri中的组ID确定CF。无法确定CF时回404加Warning142并停止；成功后的出站Request-URI是所选CF的PSI。CF发现算法本身未在这些条款给出。

- 明确排除associated-group-id/重组分支，不将其异常拼写和路由扩入本普通组主题。

依据：§9.2.2.3.1 steps4a(ii),4b,5,10 and NOTE8，印刷页 196、197。

## 授权成功仍须检查发送策略

适用条件：O-PF处理one-to-one-sds并执行§11.1授权检查。

服务授权绑定成立仍不等于允许本次发送。allow-transmit-data缺失或false映射为403/Warning200；MaxData1To1超限映射为403/Warning202；配置了One-to-One-Communication条目而目标不匹配映射为403/Warning229，均停止后续步骤。控制面payload阈值另有403/Warning203，见发送选择主题，不能把这几类拒绝混成一个最大报文限制。

- Warning200、202是Warning编号，不是SIP200、202状态码。

依据：§9.2.2.3.1 steps6–8;11.1 steps1,1A,7，印刷页 196、197、310、311。

## 私聊目标列表与MIME检查

适用条件：CF收到one-to-one-sds；前置资源检查未拒绝，且不是functional-alias目标。

CF先要求mcdata-info+xml、mcdata-signalling和mcdata-payload三类MIME齐备，否则403/Warning199并停止；再执行私聊SDS服务尺寸检查，超max-data-size-sds-bytes时403/Warning218。目标列表缺失或entry超过1个时403/Warning204；恰好1个entry时按其uri中的MCData ID调用§9.2.2.4.1.1发送。不能把零entry情况补写成原文已规定的统一403分支。

- 已存在但含零entry的resource-lists未落入上述明确分支；本稿不裁决其完整处理。
- MIME齐备只说明这项结构条件满足，不证明全部编码、权限或安全校验通过。

依据：§9.2.2.4.2 steps1–3,5a,5b(i),5b(iii);11.1 step3，印刷页 201、202、310、311。

## 终接绑定与入站名单

适用条件：T-PF收到面向其服务目标用户的one-to-one standalone SDS请求。

T-PF使用mcdata-request-uri中的目标MCData ID查找其public user identity绑定；不存在就回404并停止。本条没有复述O-PF的绑定过期条件。若目标profile存在非空IncomingOne-to-OneCommunicationList、主叫mcdata-calling-user-id不匹配任一条目，且没有允许任意用户来信的配置，回403/Warning230并停止；任一条件不成立不能据这条组合条件拒绝。

- 不把本私聊入站列表推广为全部group-sds的许可算法；不从允许任意主叫推导绕过其他检查。

依据：§9.2.2.3.2 steps1–3a，印刷页 198、199。

## 证据边界

- 服务授权绑定创建/续期过程及TS24.484 profile完整schema未纳入。
- 身份绑定和发送权限检查不替代适用的XML/TLV保护、密钥处理或端到端payload验证；本页不证明密码学认证完成。
- 仅记录指定角色的拒绝和转发规则，不构造缺失的统一SIP事务状态机。
- 不覆盖客户端的最终渲染和READ；参见sds-disposition-timing。

## 按需继续

- [sds-transmission-selection](sds-transmission-selection.md)
- [sds-disposition-timing](sds-disposition-timing.md)

[ETSI TS124282 V19.7.0 / 3GPP TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

### 相关服务器路径

- [SDS普通组控制：组文档、发送资格与当前归属](sds-group-controller-admission.md)
- [SDS服务器链：地址转换与202、200的证据范围](sds-server-responses-and-routing.md)
