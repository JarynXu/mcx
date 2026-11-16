# 转发MESSAGE为什么先回到原主叫

TS24.379 V19.4.0，由相应私呼转发程序调用。区分原主叫、被转发用户和新目标，MESSAGE不是发向新被叫的INVITE。

## 参与功能构造转发请求

适用条件：参与功能生成转发MESSAGE。

forwarding-target-orig-id取配置call-forwarding-target；forward-to-functional-alias决定别名指示true/false。forwarded-by-mcptt-id取原INVITE的mcptt-request-uri，原called-functional-alias-URI存在时复制为forwarded-by-functional-alias。resource-lists指原主叫MCPTT ID，Request-URI指该用户的转发控制功能PSI，PAI为参与功能PSI。

依据：§6.3.2.6。

## 控制功能解析目标并送回原主叫侧

适用条件：控制功能处理转发MESSAGE，且此前检查通过。

forwarding-target-id先取forwarding-target-orig-id；仅转发request且别名指示=true时解析并选择激活用户，无激活者或无法选定则403+145。多激活者按本地策略选择，也可拒绝。成功后目标ID为选中用户，call-to-functional-alias-ind=false，forwarding-target-is-functional-alias=true；非别名时后者false。下游mcptt-request-uri是resource-lists所列用户，Request-URI为该用户终接参与功能PSI。

依据：§11.1.9.4 步骤8–10。

## 接收MESSAGE的绑定规则

适用条件：终接参与功能接收转发MESSAGE。

按mcptt-request-uri查绑定；无绑定直接404并停止。请求分支缓存该用户与mcptt-called-party-id的映射，并发转发需要多份映射。此规则不同于原INVITE无绑定仍可能转发的分支。

依据：§11.1.9.3.2 步骤2–5。

## MESSAGE成功不等于呼叫接通

适用条件：控制功能收到下游转发MESSAGE的响应。

下游2xx对应生成上游200，4xx–6xx转送。这只是转发MESSAGE链的结果，不能据此证明新目标已经接听。

依据：§11.1.9.4 响应处理。

## 证据边界

- 客户端重呼见关联主题；缓存生命周期、24.229与24.484依赖仍未全部核验；本文不是完整报文模板。

## 按需继续

- [forwarding-trigger-limits](forwarding-trigger-limits.md)
- [functional-alias-selection](functional-alias-selection.md)
- [originating-authorization](originating-authorization.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页128、129、510、511、512；仅本版本。

原文边界：§11.1.9.4步骤8a与8b(iv)对forwarding-target-id的anyExt层次写法不一致，不据此宣称完整XML模板已核。

- [forwarding-client-reorigination](forwarding-client-reorigination.md)

- [forwarding-client-results](forwarding-client-results.md)
