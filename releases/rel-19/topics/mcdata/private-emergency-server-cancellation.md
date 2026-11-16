# 私聊 SDS 紧急取消：权限未决说明与部分接受结果

## 适用范围

- 限 TS24.282 V19.7.0，在网、已有 on-demand one-to-one SDS session；直接 MCData ID 目标。不是 standalone SDS、组、pre-established、FD、IPCONN 或初始 INVITE。
- 仅各前序门槛未拒绝时继续。服务器信令与缓存状态不证明媒体/QoS或单条 SDS 送达。只处理本用户附带告警，排除 originated-by、functional alias 与跨域。

## 取消权限与原文未决说明

适用条件：CF收到emergency-ind=false，先完成.9组合校验。

取消允许不带alert-ind或带alert-ind，但不得带imminentperil-ind。正文.2.3以allow-cancel-private-emergency-call=true为获准，false或缺失为未获准；同页编辑说明仍将查此字段还是使用local policy列为FFS，必须一起呈现。

- 不能将这一授权选择写成完全定稿，也不能因此删除已有取消行为。告警取消.2.2仅明确true/false，不自行给字段缺失补默认值。

依据：§9.2.4.4.6;6.3.7.1.20 step1;6.3.7.1.9;6.3.7.2.3 private branch，印刷页 242、112、104、105、119。

## 拒绝条件及告警缓存

适用条件：进入.20，分别观察未授权或授权分支。

私聊取消未授权时回403并写emergency=true；同时请求alert=false且告警取消也未授权，响应还写alert=true，随后停止。携带emergency级Resource-Priority也回403并停止。通过后清除该私聊紧急关系缓存；只有附带告警取消也获准，才清除对应告警缓存。

- 本范围仅无originated-by的自身告警。清缓存先于下游200，不补失败恢复；取消优先条件不是BYE。

依据：§6.3.7.1.20 steps2,4,5;6.3.7.2.2，印刷页 112、113、118、119。

## 下游取消请求与回指差异

适用条件：CF经.20调用.22，私聊取消获准。

CF生成带当前媒体参数的re-INVITE，复制mcdata-info并设emergency=false，使用normal Resource-Priority；告警取消获准时设alert=false。发送后收到200缓存Contact。

- .22 step3c原文把未授权告警取消回指.2.3，且写收到INVITE；同条step3b和.20结果分支使用.2.2。不得静默修为.2.2/re-INVITE，也不将该不一致分支当可直接实现的无歧义下游alert=true规则。

依据：§9.2.4.4.8;6.3.7.1.20 step6;6.3.7.1.22 steps1–5 and response;6.3.7.1.13/.4，印刷页 242、113、114、115、107、101。

## 部分接受与后续告警结果

适用条件：CF收到下游200且尚未回邀请客户端；私聊取消获准、alert=false但告警取消未获准。

CF通过.23生成200并加Warning149。收到对应ACK后调用.10，INFO写alert=true；该分支没有另行要求在INFO写emergency=false，不能补写。成功响应须区分紧急私聊条件取消和仍未取消的告警。

- 延用.23的SDS answer/计时/身份/Warning/媒体接口要求；不声称已解决.22 step3c的下游引用矛盾。

依据：§6.3.7.1.20 response and ACK;6.3.7.1.10 step3b;6.3.7.1.23;9.2.4.4.2，印刷页 105、113、115、116、237。

## 证据边界

- 取消授权的FFS与.22引用差异仍未解决，不能据此构造完整、无歧义的实现。

## 按需继续

- [已有私聊 SDS 紧急变更：PF 身份与转发边界](private-emergency-server-forwarding.md)
- [私聊 SDS 紧急升级：CF 授权、下游请求与告警结果](private-emergency-server-upgrade.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
