# SDS 媒体面结果：建链 200、媒体接口与交付证据

限在网、正常非紧急的 on-demand standalone SDS，目标为直接 MCData ID 的 one-to-one 或普通预安排组；排除 SDS session、预建立会话、ad hoc、TGI、重组、functional alias、跨域网关、MBMS/MBS 和 FD。

这里区分 SIP INVITE 的建链响应、媒体面的传输结果和 SDS disposition；不把三个层次合成同一个成功状态。

本页依据 TS24.282 V19.7.0 核验信令与媒体接口，不以信令程序替代媒体内部成功判据。TS24.582 V19.0.0 的有限媒体结论另见相关主题，各页条件独立适用。

## 匹配的下游200触发控制功能应答

适用条件：CF 已按 §9.2.3.4.3 发出目标邀请，收到对此 INVITE 的 SIP 200，且该响应中的 MCData ID 与对应 INVITE 的 MCData ID 匹配。

CF 按 §9.2.3.4.4 调用 §6.3.7.1.23，以 SDS using media 指示生成并向邀请端发送 200。helper 写入 CF 自身的 MCData session identity、SDS/isfocus Contact 标签、Require:timer 和 Session-Expires，并以 §9.2.3.4.2 生成 SDP answer，还要与媒体面交互。该触发条件不是等齐全组所有 200，也没有声明所有目标的数据都已送达。这里的 session URI 用于会话，不能当作 SDS Message ID。

- 本段没有 first-only 或此前未发最终响应的明确守卫；不据此推出多次发送最终响应、重复建链或完整竞态算法。
- 响应中缺少或不匹配 MCData ID 时的后续处理未在本段明示，本页不补成统一失败分支。
- 没有重新核实每个 SIP dialog 的 session identity 映射算法。

依据：§9.2.3.4.3 response to step13;9.2.3.4.4 final response procedure;6.3.7.1.23 steps1–10，印刷页 115、116、222、224。

## 客户端ACK触发媒体面交互

适用条件：以下角色事件独立适用，不是必须同时满足的条件：发送客户端收到原始 INVITE 的 2xx，进入 §9.2.3.2.3 的响应处理；或者接收客户端通过自身前序检查，按 §9.2.3.2.4 生成并发送带 SDP answer 的 200，再收到对此 200 的 ACK，进入接收端媒体接口。

发送客户端收到 2xx 后必须发送 ACK、启动 SIP Session timer，然后按 TS 24.582 §6.1.1.2 与媒体面交互。接收客户端的 200 表示接受邀请并给出 recvonly SDP；它收到 ACK 后才进入本条规定的媒体面交互，即 TS 24.582 §6.1.1.3。因此，收到 INVITE 的 200 或发出 ACK 不能独立证明 SDS payload 已完整传输、已显示或已读。

- 发送端条件是 2xx，接收端生成的具体响应是 200；不将二者随意改为同一个枚举。
- 这里陈述规范的触发事件，不编造跨各 SIP dialog 的全局时钟顺序。

依据：§9.2.3.2.3 2xx response steps1,3,4;9.2.3.2.4 steps4–10 and ACK procedure，印刷页 213、214、215。

## 实际数据传输仍需媒体规范

适用条件：需要判断本页范围内真正的数据发送、接收或成功判据时，按所考察角色的实际事件定位：发送客户端收到 INVITE 2xx、接收客户端收到对已发 200 的 ACK、O-PF/T-PF 收到对应 INVITE 200，或 CF 到达 §9.2.3.4.4 的私聊 step6c/组 step7k 及相关响应调用点。各入口独立，不要求所有角色同时通过准入或已经完成媒体传输。

本版把发送客户端、接收客户端、O-PF、T-PF 和 CF 的媒体处理分别交给 TS 24.582 §6.1.1.2、§6.1.1.3、§6.2.1.4、§6.2.1.5 和 §6.3.1。24.282 可以核到协商的 mcdata-signalling/mcdata-payload 类型、这些接口触发点及之后的成功/失败指示，但这些条款本身没有展开 MSRP 数据消息、分块确认、重传或成功必须覆盖哪些接收者。本页接口调用不能证明全组 DELIVERED、READ 或应用处理完成；独立的 TS24.582 V19.0.0 媒体响应主题也不将来源侧 MSRP 200 解释为全组交付。

- 这是来源明确给出的接口边界与本页核验范围，不宣称 TS 24.582 本身没有定义这些内容。
- §9.2.1.2 的已核入口是含两种 MIME 的 SIP request；不能仅因 MSRP 协商了同名类型，就无来源地把该 SIP 入口直接套成 MSRP 接收算法。
- 相关媒体主题独立依据 TS24.582 V19.0.0；不把 24.282 V19.7.0 的版本号套到 24.582，也未证明这两个精确版本的完整互通、完整 RFC/重传行为或媒体结果接口映射。

依据：§5.3.0;9.2.3.2.1 step1f;9.2.3.2.3 2xx and media-result procedures;9.2.3.2.4 ACK procedure;9.2.3.3.3 200 response step10;9.2.3.3.4 200 response step9;9.2.3.4.3 200 response;9.2.3.4.4 steps6c,7k;6.3.7.1.23 step10，印刷页 50、116、210、213、214、215、218、220、222、223、224。

## 建链拒绝与传输失败分开处理

适用条件：发送客户端分别处理两个独立事件：对已发 INVITE 收到 4xx、5xx 或 6xx 最终响应时进入建链错误分支，不要求建链准入成功；或者已进入媒体传输后收到媒体面关于 standalone SDS 未成功发送的指示，进入媒体失败分支。不将这两种事件合取。

客户端对 INVITE 的 4xx/5xx/6xx 要告知用户 SDS 无法发送，并发送 ACK。媒体面另有未成功指示入口，触发的是面向已建立会话的 BYE，并带 transmission failed 的 Reason；两个入口不能合并成收到任意失败都发送 BYE。对应地，发送端收到建链 2xx 后仍可能随后收到媒体失败。

- 不覆盖 CANCEL、超时、300 别名重定向或 TS 24.229 的事务重试与 ACK 细节。

依据：§9.2.3.2.3 2xx response, 4xx/5xx/6xx response and unsuccessful media transfer procedures，印刷页 213。

## 证据边界

- 未将一般 SIP 成功、媒体传输成功与第 12 章 disposition 通知混成单一端到端成功证据。
- 通知聚合和通知接收另见对应通知主题，不以此处媒体结果替代。

## 按需继续

### 媒体来源：TS24.582 V19.0.0

以下媒体页面限各自所列条件，不证明与本页 TS24.282 V19.7.0 的完整版本组合。

- [SDS媒体确认：CF受理与终端交付分开判断](sds-msrp-response-boundary.md)

### 信令与通知来源：TS24.282 V19.7.0

- [sds-media-session-setup](sds-media-session-setup.md)
- [sds-media-result-and-release](sds-media-result-and-release.md)
- [sds-disposition-timing](sds-disposition-timing.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 来源中的未解细节

- §9.2.3.4.4 final response paragraph，印刷页 224：CF 上游 200 的条件写下游 200 且 MCData ID 匹配，未写 all-targets、first-response-only 或尚未发最终响应守卫。只能保留所述触发，不自行补全组响应竞态。
