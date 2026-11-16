# PF 存储控制准入：身份、分层许可与目标检查

限参与MCData功能PF收到§21.3的通信存储控制SIP MESSAGE；授权和目标检查均以本版本明确的条件为界。

步骤4的各子检查以mcdata-info body含request-type=store-comms-in-msgstore-ctrl-req为外层条件；不得丢弃各子项对all、specific或body是否存在的限制。

## 绑定与拥塞分别处理

适用条件：PF开始处理该存储控制MESSAGE。

资源不足或有拥塞风险时，PF可用SIP500拒绝，可附Retry-After，并跳过后续处理。继续处理时，PF从P-Asserted-Identity中的公共用户身份确定呼叫用户MCData ID；该绑定在服务授权时建立。绑定找不到或已过有效期时，PF须返回SIP404及Warning141，并停止剩余步骤。客户端自报的client ID或名单中的用户ID不能替代这个发起用户绑定。

- 500及Retry-After均为may，不写成所有拥塞必然500或必带重试时间。
- 没有为缺失/畸形P-Asserted-Identity额外推导本节未明列的解析错误码；只陈述无法建立/过期绑定的404条件。

依据：§21.3.3.2 steps1–3 and NOTE，印刷页 474。

## 总体和全体私人许可

适用条件：PF已通过身份绑定检查，进入步骤4。

ruleset中的allow-store-comms-in-msgstore缺失或false时，PF以SIP403和Warning234拒绝并停止。若请求包含store-all-private-comms-in-msgstore，ruleset中的allow-store-private-comms-in-msgstore缺失或false也触发同一拒绝；该检查由all字段存在触发，不只针对值true。因此全体私人通信的停用请求同样受该许可约束。

- 步骤4b的明确guard是all-private字段存在；不把这一子项改写成所有specific-private请求都会执行同样的字段检查，也不由此宣称指定私人名单可绕过授权。步骤5仍把实际控制范围限定为获准存储的通信。
- Warning234说明存储控制未获准，不与传输许可、对象访问令牌失效或目标不存在混为一种原因。

依据：§21.3.3.2 steps4a,4b，印刷页 474、475。

## 组范围逐项保留许可条件

适用条件：PF进入步骤4的组控制许可检查，区分all-group存在与缺失。

请求含store-all-group-comms-in-msgstore时，步骤4c检查用户profile中各MCDataGroupInfo的allow-store-group-comm-in-msgstore；原文将缺失或false列为SIP403/Warning234拒绝并停止的条件。all-group缺失而控制body含enable或disable的group名单时，步骤4e按指定Group ID匹配对应MCDataGroupInfo，检查相同许可元素，缺失或false同样拒绝并停止。不能把全体组开关写成忽略组授权，或把被拒请求默认为只跳过未授权组再部分成功。

- 保留原文each及匹配条件的范围，不补未知Group ID的独立错误码，也不制定空组列表、混合许可列表的过滤/部分成功算法。
- 步骤4e以all-group缺失为前提；在all-group存在时不再把它当作指定名单执行分支，但步骤4c和其他必要检查仍适用。

依据：§21.3.3.2 steps4c,4e，印刷页 475。

## 目标拒绝与body冲突

适用条件：PF进入步骤4的目标结构检查。

步骤4d把控制body、all-private字段和all-group字段均未出现列为无法确定目标，须以SIP403/Warning235拒绝并停止。步骤4f则写明：specific-private或specific-group存在，且请求缺少application/resource-lists+xml body时，同样403/235并停止。4f的MIME名称与客户端步骤6和D.7要求的mcdata-msgstore-ctrl-request body不同，不能悄悄改成同一个类型，也不能认定仅带后者就必然通过PF。

- 4d是三个目标载体都缺失的联合条件，不能写成缺少任意一个就拒绝。
- 4f没有同类all字段缺失这一guard；不能用执行阶段的all优先条件跳过此处检查。
- 本页不决定应删除、替换或补加哪一种body，也不提交修正报文。该原文差异必须在实现/互通设计前另行澄清。

依据：§21.3.2.2 step6;21.3.2.3 step6;21.3.3.2 steps4d,4f;D.7.1–D.7.3，印刷页 473、474、475、624、625。

## 证据边界

- 未核24.484完整授权配置、24.229通用SIP错误处理或服务授权建绑定过程；本页不引入SDS传输/归属准入条件。

## 按需继续

- [message-store-control-request](message-store-control-request.md)
- [message-store-control-result](message-store-control-result.md)
- [message-store-access-and-objects](message-store-access-and-objects.md)
- [service-authorization-binding](service-authorization-binding.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§21.3.2.2 step6;21.3.2.3 step6;21.3.3.2 step4f;D.7：客户端指定名单用application/vnd.3gpp.mcdata-msgstore-ctrl-request+xml；PF step4f检查的缺失body却为application/resource-lists+xml。 保留两处MIME字面与适用条件。不擅自按常见协议、旧版本或其他服务替换其中一处，不提供所谓已修正的互通报文。
