# SDS session 的分段 200 与参与者范围

同版 §9.2.4 普通在网 session；直接私聊或配置组，不含别名、重组、ad hoc、跨域和优先通信扩展。

各角色的前序检查成功；本主题只跟踪 INVITE 和成功响应，不用一个局部 200 代替全体参与者状态。

PF 指参与功能，CF 指控制功能；观察哪个 SIP 事务段、哪个被邀请目标是结论的组成部分。

## PF重新生成本段响应

适用条件：O-PF 收到上游 CF 返回的 session INVITE 200，或 T-PF 收到终接客户端的对应 200。

两个 PF 分支都生成本段的 200，而不是把下游响应无改动地视为端到端结果。它们按 §9.2.4.3.2 生成 SDP answer；如需要，替换媒体 IP/端口并在 IP 被替换时把自己的 MSRP URI 前置到 path。O-PF 的会话标识映射自收到的 200 Contact；T-PF 返回的标识映射自 CF 原 INVITE Contact。双方分别调用自己的媒体接口，再向上游发送 200。

- 地址替换是 if required；PF/CF 同服务器且 PF 无独立媒体地址/端口时省略替换，不把媒体必经独立 PF 当作普遍要求。
- 本条不补齐 TS24.229/RFC 的所有头域和事务规则；其200不是MSRP逐消息确认。

依据：§9.2.4.3.2;9.2.4.3.3 200 response steps1–12;9.2.4.3.4 200 response steps1–10;4.2.2，印刷页 34、232、234、236。

## 目标匹配200不等于全组完成

适用条件：CF 收到按 §9.2.4.4.3 发出的目标 INVITE 的 SIP200，且该响应中的 MCData ID 与对应 INVITE 中的 MCData ID 匹配。

满足这一关联条件后，§9.2.4.4.4 令 CF 以 SDS using session 为子服务调用 §6.3.7.1.23，生成并发送给邀请者的 200。该响应带 CF 会话 Contact、计时要求，以及按 §9.2.4.4.2 生成的 session SDP answer。原文这个触发段没有把“所有被邀请者均返回200”列为条件，因此不能把邀请者看到200解读为全组均已建立，更不能读成全组某条消息已送达。

- 保留源文的目标 ID 匹配条件，不自行发明缺失ID的接受规则。
- 这里也没有规定只处理“第一条200”的守卫或全部成员完成的计数算法；本条不补出这些算法。

依据：§9.2.4.4.3 200 response;9.2.4.4.4 final200 procedure;6.3.7.1.23 steps1–10;9.2.4.4.2，印刷页 115、116、237、239、242。

## 后来归属仍需邀请

适用条件：组 session 的组文档、成员、服务与发送许可、发起者 affiliation 等前置检查通过。；初始目标由 §6.3.4 决定；或 session 已建立后又有客户端成功 affiliation 到该组。

初始组建立调用 §6.3.4 决定目标；未找到 affiliated 成员时返回403/Warning198并停止，其他正常目标经 §9.2.4.4.3 邀请。该邀请过程还明确用于 session 建立之后成功 affiliation 的客户端。因此既有组 session 的存在、某个客户端后来 affiliation 成功、对该客户端发出邀请、该邀请得到响应，是不同事件；不能用较早的200替代后来加入端的建立结果。

- 迟加入邀请不等于自动补发历史数据，也不证明该客户端已收到加入前的消息。
- §9.2.4.4.4 step8j 回指 stepg，但决定目标实际列在 steph；本页保留条款差异，不扩出新的成员选择算法。

依据：§9.2.4.4.4 steps8h–8k;9.2.4.4.3 opening and steps7–13，印刷页 237、238、239、242。

## 证据边界

- 未建立全组最终加入完成判据、失败成员恢复或完整成员状态机。

## 按需继续

- [sds-session-establishment](sds-session-establishment.md)
- [sds-session-message-evidence](sds-session-message-evidence.md)
- [sds-session-admission](sds-session-admission.md)
- [sds-media-session-setup](sds-media-session-setup.md)
- [sds-disposition-timing](sds-disposition-timing.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§9.2.4.4.4 step8j：邀请组成员时回指stepg，目标决定步骤为steph。 引用整个8h–8k连接关系，并记录回指差异，不依据笔误发明目标算法。

§9.2.4.3.3 200 response opening：响应段写为回应step16的INVITE，实际发送列在step17。 按对应INVITE响应理解，不把编号文本改成协议新步骤。

已有一对一 SDS 会话的紧急条件取消及部分接受结果另见[私聊 SDS 紧急取消：权限未决说明与部分接受结果](private-emergency-server-cancellation.md)。
