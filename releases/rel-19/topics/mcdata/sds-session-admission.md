# SDS session 准入：后续使用、双方发送许可与组服务开关

限 §9.2.4 的在网 SDS session；不把 §9.2.3 单次 standalone SDS 经媒体面传送等同于本主题的 SDS session。

普通直接用户目标或已配置组，不含别名、重组、ad hoc、跨域网关及紧急/迫近危险扩展。

结论只覆盖 §11.1 的 session 特有准入和所列调用点，不覆盖完整 session 建立、媒体传送或释放。

## 后续使用不是跳过前序门槛

适用条件：用户拟建立供后续 one-to-one MCData 通信用的 SDS session；执行 §11.1 已到达 step9。

step9 对客户端不再增加检查，并令其从 step11 继续。这是到达该步骤后的控制流，不是跳过前面的发送权限、目标许可或其他适用检查。§9.2.1.1 仍要求 SDS session 发起先完成 §11.1，成功后才进入 §9.2.4.2.3。

- step11 只在 IP Connectivity 条件成立时适用；本条没有把 SDS session 转成 IP Connectivity。
- 不据“后续使用”推导所有 payload 相关检查都一定被执行或一定被豁免；保留各步骤自己的适用条件。

依据：§11.1 steps1,1A,9,11,12;9.2.1.1 SDS session branch，印刷页 190、310、311。

## PF检查双方发送许可

适用条件：§11.1 step9 的 one-to-one SDS session for later use；对 PF 判断。

发起端或终止端任意一方的用户配置 actions 中 allow-transmit-data 缺失或为 false，PF 都须判定不允许建立该 SDS session，并停止后续步骤。这里检查双方发送许可，不能只用发起者许可通过来替代，也不能把终止者的这一字段改写成一般接收许可。

- 该段没有分配两个用户配置的取得方法，也没有单独给出此 step9 拒绝的 SIP Warning；不得补出配置同步算法或专用错误码。

依据：§11.1 step9，印刷页 311。

## 组服务元素缺失即拒绝

适用条件：用户拟在某 MCData group identity 上建立 SDS session，执行到 §11.1 step10。

组文档 list-service 中 mcdata-allow-short-data-service 缺失或为 false，客户端和 CF 均须判定不允许建立该组 SDS session，并停止后续步骤。缺失也属于拒绝条件，不能只检查显式 false；它是 session 的强制检查，不能被一般 SDS 服务概述中的 SHOULD 表述替代。

- 本条不把字段缺失的行为推广到所有 standalone SDS 分支；各调用过程仍须按自己的条件解释。
- 该服务开关不是 actions 中针对本用户的 mcdata-allow-transmit-data-in-this-group，两个检查不可合并。

依据：§11.1 step10;9.1 general service restriction，印刷页 189、311。

## 调用点分别定义错误响应

适用条件：分别观察普通 SDS session 的 O-PF §9.2.4.3.3 step7，或 CF §9.2.4.4.4 step8 的指定拒绝分支；各自前序检查通过。

O-PF 将 §11.1 step1 的发送权限拒绝映射为 SIP 403/Warning221，将 step1A 的目标许可拒绝映射为 403/Warning229。组 CF 在服务开关显式 false 时返回 403/Warning206；在 §11.1 step2 的本用户组发送许可拒绝时返回 403/Warning222。各分支均停止后续过程。这些代码有自己的条件，不能据相近的 Warning 含义，把 step9 的双端许可或 step10 的元素缺失自动补成同一个映射。

- 只给已明确列出的对应关系；§11.1 的拒绝义务不因本批未核出一一对应的响应码而消失。
- 完整 session 准入还涉及媒体参数、身份、服务标识、组文档与归属，本条不是可直接替代全流程的检查清单。

依据：§9.2.4.3.3 steps6,7a,7b;9.2.4.4.4 steps8d,8f;11.1 steps1,1A,2,9,10，印刷页 233、241、310、311。

## 证据边界

- 未扩展完整 SDS session 媒体协议；TS 24.582 仍为未核依赖。

## 按需继续

- [sds-transmission-selection](sds-transmission-selection.md)
- [sds-media-session-setup](sds-media-session-setup.md)
- [service-authorization-binding](service-authorization-binding.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 条款衔接边界

- §11.1 step9 versus 9.2.4.3.3 step7;11.1 step10 versus 9.2.4.4.4 steps8d,8f：通用 helper 给出 session 特有拒绝义务，但已核调用分支的明示响应对应到 step1、step1A、step2 或显式 false，未给出 step9 和 step10 元素缺失的一一映射。分别保留规范义务和已核响应；不静默把调用分支引用改为 step9/10。
