# MCVideo服务器主动晚进入邀请：触发、接受与媒体许可

TS24.281 V19.3.0，普通在网、带 transmission control、按需预安排组呼的进行中会话进入路径；普通 GMS 组，不含TGI/重组/预配置重组、NCF/gateway、chat、广播、ad hoc、功能别名、远程/ambient、离网或预建立会话。目标会话是否仍存在/active由各入口实际检查，客户端认为会话还在不代表CF一定找到它。

客户端 emergency state 未置位，组不处于MVEG2、MVIG2/MVIG4，客户端响应时不在MVEGC2/3或MVIGC2/3；请求不含emergency-ind、imminentperil-ind、alert-ind、用户请求优先级扩展或优先通信Resource-Priority；CF组的in-progress emergency与imminent-peril均为false。没有待处理的优先升级/取消。

每条claim只继承本主题common_conditions及自身conditions，不继承前条成功。以下三个入口必须分开：客户端用session identity重入、组ID发起链到CF后发现ongoing、CF收到通知后主动邀请晚进入者；不能把一个入口的检查/Warning自动移到另一个入口。

本页保留正文错引及独立版本边界；只把真实正文列出的状态与顺序当结论。IMS/RFC、媒体编码/密钥、配置schema及完整失败恢复依赖未全部闭合。

## 服务器主动邀请的两个触发

适用条件：CF被通知某MCVideo客户端新近affiliated，或者被通知该客户端从覆盖外返回；存在要加入的ongoing普通预安排组呼。

CF SHALL按照§9.2.1.4.1邀请该客户端加入ongoing组呼。本页普通本地组对应逐客户端邀请§9.2.1.4.1.1。这个入口由CF收到通知触发，与用户在客户端发起session-identity重入INVITE不同；仅在组名单中出现不等于这里的触发事件。

- 如何通知CF客户端回到覆盖范围在规范范围外；本段不规定覆盖探测、定时轮询或客户端必须先自动重呼。
- 本段只调用邀请过程，未重新列客户端请求入口的join许可/容量错误链。不能把这些检查悄悄加到此处，也不能据此宣称其豁免全系统共享策略。

依据：§9.2.1.4.6;9.2.1.4.1.1，印刷页 223、236。

## 晚进入仍经过终接接受

适用条件：CF已进入普通晚进入邀请，向某客户端执行§9.2.1.4.1.1；后续T-PF收到的邀请无Answer-Mode/Priv-Answer-Mode，客户端没有可复用预建立会话组合。

CF把SIP Request-URI设为目标T-PF PSI，PAI设为CF PSI，XML mcvideo-request-uri为目标用户ID而mcvideo-calling-group-id为组ID，并据原offer构造SDP。T-PF仍检查isfocus、已收到的Answer-Mode Indication以及目标用户/public-user-identity绑定，分别可产生403/104、480/146或无绑定404；随后根据已存auto-answer/manual-answer选择helper，按绑定身份发往客户端。客户端是否自动/手动接受仍受实际Answer-Mode与本地设置/允许覆盖条件约束。

- 完整逐字段生成、资源不足拒绝、183/PRACK gating及用户拒绝480/110见prearranged-call-terminating；这里保留入口差异，不把已经ongoing当作跳过终接接受的许可。
- GKTP文档存在且含MKFC-GKTPs时，CF逐项重新生成并只装入成功I_MESSAGE；T-PF收到MKFC-GKTPs时执行§6.3.2.3.2。算法和失败处理仍未闭合，信令邀请不证明新终端已取得可用密钥。

依据：§9.2.1.4.6;9.2.1.4.1.1;9.2.1.3.2;9.2.1.2.1.2，印刷页 210、211、212、220、221、223、224、236。

## 响应、会议通知与媒体许可

适用条件：服务器晚进入邀请已发送；CF收到该客户端邀请INVITE的200，或该客户端已发送其INVITE 200。

CF按所调用的邀请过程与媒体平面交互、向conference订阅者发NOTIFY，并将收到的邀请成员200本地计数加1；此晚进入入口没有重置该计数为0或重新调用初建required/TNG1完成链。对24.581 V19.2.0的终接participant而言，信令发送200时建立basic transmission实例但进入no-permission，并建立每call的general reception controller；实际按源接收许可另行处理。ongoing组仍在运行，不等于新加入终端沿用他人的发送/接收授权。

- 本段“未列重新启动”不扩成所有扩展流程绝不启动TNG1。CF计数的完整存续/重置模型、无响应重试和通知丢失恢复未在late-entry段定义。
- 普通组服务器Mode1与客户端Mode0条件分支仍按既有server-reception-permission边界；跨规范独立版本不称互操作完成。

依据：§24.281 V19.3.0:9.2.1.4.6;9.2.1.4.1.1;24.581 V19.2.0:6.2.4.2.3;6.2.5.1;6.2.5.2.2，印刷页 224、236、36、45、46。

## 证据边界



## 按需继续

- [prearranged-call-terminating](prearranged-call-terminating.md)
- [rejoin-session](rejoin-session.md)
- [participant-transmission-control](participant-transmission-control.md)
- [participant-reception-control](participant-reception-control.md)
- [server-reception-permission](server-reception-permission.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。

[媒体许可来源 TS24.581 V19.2.0](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；媒体页码与条款按各claim的source_references分别追溯，不混入24.281版本。
