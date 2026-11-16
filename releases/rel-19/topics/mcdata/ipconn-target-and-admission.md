# IP Connectivity 建立：业务范围、目标和准入

只适用TS24.282V19.7.0 §20的两个MCData客户端之间在网IP Connectivity；不是组IP连接或离网流程。

普通直接MCData ID目标；可先按本条所列条件从IP信息匹配得出该ID，但不处理功能别名或跨域网关。

过程按各自前置条件执行；先前拒绝要求停止时不能继续。这里只整理选定准入主干，不替代完整SIP/安全规则。

## 先确定版本和目标身份

适用条件：用户或应用请求与另一客户端建立IP Connectivity；请求可包含明确目标MCData ID。；若请求没有目标MCData ID或功能别名，但有目标IP信息，适用可选的配置匹配分支。

§20只描述两个客户端之间的在网IP Connectivity，并明确本版所述过程不兼容Release16。缺少明确目标标识时，客户端可以把请求中的目标IP信息与用户配置的One-to-One communication list中的IPInformation匹配，取得对应用户条目的MCData ID。这个可选匹配把IP信息转换成MCData业务目标，并未取消后续基于身份、服务和权限的建立。

- 不把与Rel16不兼容扩大成与所有早期版本均不兼容，也不据此定义互通迁移方案。
- 源文未给出匹配失败或多重匹配的完整处理；不能编造DNS查找、任选一项或失败后的默认目标。配置schema和匹配算法依赖24.484，本页未读取。

依据：§20.1;20.2.1 opening，印刷页 443、444。

## SIP业务目标与媒体地址分离

适用条件：直接目标MCData ID已确定，客户端生成初始IPCONN INVITE。

INVITE的resource-lists记录受邀用户MCData ID，mcdata-info中的request-type为one-to-one-ipconn，并使用IPCONN服务标识及g.3gpp.mcdata.ipconn能力标签。SIP Request-URI指向服务发起用户的PF公共服务身份，而不是把目标IP直接写成最终用户路由。客户端另加入§20.2.0a的SDP，把业务目标与媒体地址分别传递。

- 不把SDS的request-type、服务标签或m=message默认移植到IPCONN。
- 这里仅说明直接目标主线；别名指示、重定向和应用优先级不在本页展开。

依据：§20.2.1 steps1–4,7–12;20.2.0a，印刷页 443、444、445。

## 发送权限按角色判断

适用条件：按§11.1判断是否允许发起one-to-one IP Connectivity；用户profile的actions/allow-transmit-data缺失或为false。；O-PF已通过本入口前序检查并执行§20.3.1 steps6,7。

§11.1 step1的一般私聊发送许可检查约束客户端和PF；step11另明确IP Connectivity的客户端和CF在该许可缺失或false时须拒绝建立并停止。§20.3.1要求O-PF执行§11.1；若结果为不允许发起MCData通信，返回SIP403/Warning200并停止。不能把SDS session step9的双方allow-transmit-data检查直接当作IPCONN的同一规则。

- 没有把CF在helper中的义务改成PF独占，也没有替§20.4.2编造对应step11的独立Warning。
- §11.1其他适用步骤仍保留自己的条件；本条只展开上述发送许可差异，不声称profile为true就必然建立成功。

依据：§11.1 steps1,9,11;20.3.1 steps6,7，印刷页 310、311、448。

## CF能力标签与唯一目标

适用条件：CF收到IPCONN INVITE，资源分支未拒绝；request-type为one-to-one-ipconn，且目标不是别名。

Accept-Contact缺少g.3gpp.mcdata.ipconn，或缺少携IPCONN ICSI的g.3gpp.icsi-ref时，CF返回403并停止。resource-lists MIME体缺失或其中entry多于一个时，返回403/Warning227并停止；恰好一个entry的直接目标分支才按§20.4.1邀请该MCData用户。业务能力声明与目标唯一性是两个不同检查，不能只凭已有IP地址跳过。

- 明确拒绝条件是MIME体缺失或entry多于一个；该段没有明示零entry对应的同一码，本页不把它补写成“所有非一均227”。
- 不从SDS的媒体参数488分支推导IPCONN在这里也有同一个拒绝过程。

依据：§20.4.2 steps1,2,5a,5b，印刷页 453、454。

## 证据边界

- 未核组IP Connectivity、离网流程、功能别名解析或外部配置默认值。

## 按需继续

- [ipconn-server-path](ipconn-server-path.md)
- [ipconn-media-and-success-evidence](ipconn-media-and-success-evidence.md)
- [service-authorization-binding](service-authorization-binding.md)
- [sds-session-establishment](sds-session-establishment.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§20.1;20.4.0a/.0b NOTES：§20.1范围是两个客户端，CF SDP说明例子却出现组通信媒体分发。 本页严格按明确范围处理双客户端主线，不由注释扩展出组IPCONN。
