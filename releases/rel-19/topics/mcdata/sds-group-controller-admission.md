# SDS普通组控制：组文档、发送资格与当前归属

限在网、非紧急、非重组的预安排组standalone SDS控制面；request-type=group-sds，组ID对应GMS维护的普通组文档，不是TGI、ad hoc或preconfigured regroup。

CF前置资源和三类MIME检查已通过；本页门槛须按原过程顺序理解，任一规定停止的失败分支都阻断后续分发。

## 组文档是持续的准入依据

适用条件：CF对普通组调用§6.3.3，尚未订阅该组文档。

CF须订阅该组文档的xcap-diff事件，而不是把客户端携来的组ID当成足够授权。订阅取得404时向请求方回404/Warning113；其他4xx、5xx或6xx用相应最终响应加Warning114并停止。调用处只在§6.3.3成功后继续。已存在订阅时不能从这条推出每次发送都重新建立订阅或重新GET全文。

- §6.3.3 step3在通用helper中写SIP INVITE，本调用实际为SIP MESSAGE，保留交叉表述差异。
- 订阅更新时序、缓存一致性和TS24.481完整协议不在本主题。

依据：§9.2.2.4.2 step6a;6.3.3 steps1–3，印刷页 97、202。

## 组形态、成员和服务门槛

适用条件：CF已取得普通组文档，执行§9.2.2.4.2 step6c–6g。

preconfigured-group-use-only=true时403/Warning167；on-network-disabled元素存在时403/Warning115；组文档没有匹配主叫MCData ID的成员条目时403/Warning116；mcdata-allow-short-data-service存在且false时403/Warning206。supported-services缺失，或存在且包含enabler非SDS ICSI的service条目，按本版字面回488/Warning207。上述分支均停止，不把元素缺失、元素存在和false混为同一条件。

- supported-services的字面测试不是“找不到任何SDS项”；多个service条目如何与该测试协同未在本稿修正或推断。

依据：§9.2.2.4.2 steps6c–6g，印刷页 203。

## 发送权限与两种额度分开检查

适用条件：普通组前置文档/服务检查成功，CF执行§11.1的组SDS条件。

组文档actions中适用于本用户的mcdata-allow-transmit-data-in-this-group缺失或false导致403/Warning201；超过mcdata-max-data-in-single-request导致403/Warning208；超过mcdata-on-network-max-data-size-for-SDS导致403/Warning217。三个条件均停止后续步骤。成员资格、允许发送、单次发送额度及组SDS尺寸上限是不同检查，不能因是组成员就跳过后面门槛。



依据：§9.2.2.4.2 step6i;11.1 steps2,5,8，印刷页 203、204、310、311。

## 归属绑定到用户、客户端和有效期

适用条件：CF为普通组检查主叫的当前归属，或按§6.3.4筛选目标成员。

§6.3.5要求同时存在匹配组ID、用户MCData ID、客户端ID的三级记录，且该用户信息项的expiration time未到期。静态成员表中的一行不替代此检查；同一用户另一客户端的记录也不能自动替代所检查客户端。普通组主叫不归属时，§9.2.2.4.2 step6j给403/Warning120并停止。

- step6j还混列重组条件且重复ii编号；本稿仅取本普通组适用的主叫归属检查，不补跨重组布尔表达式。
- 本页不规定归属记录的创建、刷新、撤销和并发同步算法。

依据：§6.3.5;8.3.3.2;9.2.2.4.2 step6j，印刷页 98、179、204。

## 目标是归属成员而非静态全员

适用条件：普通组主叫及前序门槛通过，CF执行step6k，不是TGI或preconfigured regroup。

CF按§6.3.4从普通组文档list中的成员条目出发，逐一以§6.3.5判断归属，只向归属成员发送；定义包括控制功能隐式归属的成员，但不表示本步骤会自动替未归属者建立归属。未找到归属成员时403/Warning198并停止；否则该分支调用§9.2.2.4.1.1向目标成员发送。

- step6k(iii)把目标成员交叉引用为step h所得，而本段求目标在k(i)；原文引用异常保留，不另造目标算法。
- 不把“没有归属成员”改写成“没有其他归属成员”；本条未给出新的主叫排除、去重或并发快照规则。
- 目标筛选不是收到数据、成功解码或READ的证明。

依据：§9.2.2.4.2 step6k;6.3.4;6.3.5，印刷页 97、98、204。

## 证据边界

- 不含组重组、TGI、ad hoc、跨域及隐式归属建立的完整流程。
- 非组成员、服务禁用、发送无权、额度超限与未归属分别保留；不合并为一个泛化的403。
- §9.1关于组SDS禁用的should不替代这里明确分支的shall。

## 按需继续

- [sds-transmission-selection](sds-transmission-selection.md)
- [receiving-data](receiving-data.md)

[ETSI TS124282 V19.7.0 / 3GPP TS24.282 V19.7.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

### 相关服务器路径

- [SDS服务器准入：主叫身份、控制功能与私聊目标](sds-server-identities-and-private-admission.md)
- [SDS服务器链：地址转换与202、200的证据范围](sds-server-responses-and-routing.md)
