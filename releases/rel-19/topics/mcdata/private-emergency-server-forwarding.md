# 已有私聊 SDS 紧急变更：PF 身份与转发边界

## 适用范围

- 限 TS24.282 V19.7.0，在网、已有 on-demand one-to-one SDS session；直接 MCData ID 目标。不是 standalone SDS、组、pre-established、FD、IPCONN 或初始 INVITE。
- 仅各前序门槛未拒绝时继续。服务器信令与缓存状态不证明媒体/QoS或单条 SDS 送达。只处理本用户附带告警，排除 originated-by、functional alias 与跨域。

## 只适用于已有一对一 SDS 会话

适用条件：收到现有私聊 SDS 会话的升级或取消请求。

§9.2.4.3.5 将服务用户请求交给 .18；§9.2.4.3.6 将 CF 请求交给 .17。CF 的接收升级/取消入口分别调用 .19/.20，发送入口分别调用 .21/.22，并在接收入口明确 SDS session 子服务。

- 不可把这些 one-to-one wrappers 改写成组调用链。

依据：§9.2.4.3.5/.6;9.2.4.4.5–.8，印刷页 236、242。

## 发起侧 PF 的绑定与请求

适用条件：O-PF执行§6.3.7.1.18。

资源不足或拥塞风险时可回500，Retry-After可选。O-PF从请求PAI的public user identity确定主叫MCData ID；无有效绑定回404/Warning141并停止。出站mcdata-calling-user-id使用确定的身份；有相应输入时复制目标resource-lists、mcdata-info及location-info，使用已有session的当前SDP，并保留已收到的Resource-Priority值。

- 有紧急指示时可以选择接受，不是资源拒绝必然豁免。身份绑定成立不等于CF紧急授权通过。排除别名，但原文step6对已带别名另有激活检查，不能删除为通用规则。

依据：§6.3.7.1.18 steps1–9，印刷页 110、111。

## 终接侧 wrapper 的实际调用

适用条件：T-PF经§9.2.4.3.6进入§6.3.7.1.17。

T-PF按存在条件复制SDP、resource-lists、Resource-Priority、mcdata-info和location-info并发送给客户端。

- 本wrapper调用.17而非.15；不得把.15的绑定404、资源500与200处理拼入本条，冒充明确caller链。

依据：§9.2.4.3.6;6.3.7.1.17;6.3.7.1.15 (comparison only)，印刷页 108、110、236。

## 发起侧的成功响应与 Warning

适用条件：O-PF收到200。

O-PF生成返回客户端的200，按存在条件复制mcdata-info及Warning，PAI使用自身PSI，发送后按TS24.582与媒体面交互。

- Warning149不会因PF转发自动消失；本条未核TS24.582实现结果，也未补T-PF的专用200入口。

依据：§6.3.7.1.18 response steps1–6，印刷页 111。

## 证据边界

- 这是明确wrapper下的信令责任，不声明全网实现闭环。

## 按需继续

- [SDS session 建立：协商通路不等于发送一条消息](sds-session-establishment.md)
- [私聊 SDS 紧急升级：CF 授权、下游请求与告警结果](private-emergency-server-upgrade.md)
- [私聊 SDS 紧急取消：权限未决说明与部分接受结果](private-emergency-server-cancellation.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
