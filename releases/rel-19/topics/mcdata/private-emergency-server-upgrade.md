# 私聊 SDS 紧急升级：CF 授权、下游请求与告警结果

## 适用范围

- 限 TS24.282 V19.7.0，在网、已有 on-demand one-to-one SDS session；直接 MCData ID 目标。不是 standalone SDS、组、pre-established、FD、IPCONN 或初始 INVITE。
- 仅各前序门槛未拒绝时继续。服务器信令与缓存状态不证明媒体/QoS或单条 SDS 送达。只处理本用户附带告警，排除 originated-by、functional alias 与跨域。

## CF 参数验证与升级许可

适用条件：CF收到emergency-ind=true的re-INVITE。

先检查SDP，不可接受回488并停止；再核优先指示组合。升级要求无imminentperil-ind且有alert-ind，非法组合回403/Warning150。私聊授权要求allow-emergency-private-call=true，且目标满足UsePreConfigured名单或LocallyDetermined；否则403，emergency-ind与alert-ind均false。

- 告警权限独立；不能以allow-activate-emergency-alert替代私聊紧急权限。

依据：§9.2.4.4.5;6.3.7.1.19 steps1–3;6.3.7.1.9;6.3.7.2.6 private branch;6.3.7.2.7;6.3.7.2.1，印刷页 104、105、111、118、121、242。

## 告警缓存先于目标应答

适用条件：已通过前序检查，主叫与目标尚无进行中的紧急私聊状态。

CF先缓存这对用户的紧急私聊关系；仅请求alert=true且告警也获授权时缓存对应告警。随后向resource-lists目标调用.21。此缓存动作发生在收到目标200之前。

- step4的Resource-Priority校验把授权回指step2，但实际授权在step3；保留差异，不静默改号。没有已核失败回滚规则，不能把提前缓存等同对端成功。

依据：§6.3.7.1.19 steps4–6;6.3.7.2.1，印刷页 111、112、118。

## 下游请求与另行告警

适用条件：CF经.19/.21发送获授权升级。

CF用.13生成带当前终端媒体参数的re-INVITE，并按SDS offer规则处理；复制mcdata-info，设emergency=true，使用服务配置的emergency Resource-Priority。告警获授权则调用.3填告警、组织及位置资料；缺少告警指示或请求告警但未获授权时出站alert=false。收到目标200后缓存Contact。

- .19前置校验已要求升级带alert-ind；.21的缺失分支不能反过来豁免该校验。Resource-Priority取配置值，不能硬编码为某个数值或宣称承载已提优先级。

依据：§9.2.4.4.7;6.3.7.1.21;6.3.7.1.13/.3/.4;9.2.4.4.1;6.3.7.2.1，印刷页 100、101、107、114、118、237、242。

## 200、Warning 149 与 ACK 后的 INFO

适用条件：CF收到发出的re-INVITE的200，且尚未向邀请客户端回响应。

CF用.23按SDS session生成200。若请求alert=true但告警未授权，200带Warning149；收到该200对应ACK后才调用.10发送INFO，INFO使用g.3gpp.mcdata-info，emergency=true、alert=false。私聊升级接受与附带告警拒绝可以同时成立。

- .23要求timer、Session-Expires/uac、CF身份及session Contact、SDS标记和SDS answer，并保留收到的Warning/mcdata-info，调用媒体接口。不能用200代替告警全部获准或数据已送达。

依据：§6.3.7.1.19 response and ACK;6.3.7.1.10;6.3.7.1.23;6.3.7.2.1;9.2.4.4.2，印刷页 105、112、115、116、118、237。

## 证据边界

- 不解释客户端MED/MDEA状态机，不向组IPEG推广。

## 按需继续

- [已有私聊 SDS 紧急变更：PF 身份与转发边界](private-emergency-server-forwarding.md)
- [私聊 SDS 紧急取消：权限未决说明与部分接受结果](private-emergency-server-cancellation.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
