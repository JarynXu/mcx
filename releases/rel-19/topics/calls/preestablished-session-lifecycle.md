# 预建立会话：建立门槛、空闲修改与拆除顺序

TS24.379 V19.4.0 第 8 章的在网 MCPTT 客户端与 participating MCPTT function 之间的预建立会话。

预建立会话本身与随后承载的 MCPTT 业务呼叫分别判断；本主题不替代具体呼叫的权限、组归属、接听和话权程序。

## 注册与资源共享前提

适用条件：客户端考虑建立一个或多个预建立会话。

客户端完成 SIP 注册并按 §7.2.2 或 §7.2.3 设置服务后，可建立一个或多个预建立会话。参与功能必须使用资源共享，既可经 SIP core，也可直接经 Rx 对接 PCC；不能把支持预建立等同于只支持其中一种路径。建立后客户端可用它发起业务呼叫，参与功能可用它承接终接呼叫。

依据：§8.1;8.1A。

## 客户端建立请求

适用条件：客户端已完成 SIP 注册并按 §7.2.2 或 §7.2.3 设置服务，发起预建立会话。

先收集提供 MCPTT 服务接口上的 ICE candidates，再生成 initial INVITE。Request-URI 为服务用户且标识预建立建立用途的 participating PSI；Contact 含 g.3gpp.mcptt，Accept-Contact 含 MCPTT 与 ICSI 标签及 require/explicit，P-Preferred-Service 为 MCPTT ICSI，Supported 含 timer。应带 Session-Expires，建议不指定 refresher，若指定则为 uac；附按 §6.2.1 构造且带 ICE candidates 的 SDP offer，再发送。P-Preferred-Identity 是可选。

依据：§8.2.1;6.3.1.1 first request type。

## 服务器的顺序检查

适用条件：参与功能收到 §6.3.1.1 定义的建立预建立会话 initial INVITE，即 Request-URI 指向该参与功能用于预建立建立的 PSI。

按 §8.2.2 顺序检查：未分配 PSI 按 §6.3.7.1 返回 404；识别、验证 MCPTT ID 并做本地授权，拒绝时 403/Warning100；判断资源共享支持。若由 SIP core 支持，检查用户与 third-party REGISTER Contact 的 registration-token 所标识 UE 的绑定，并核其与 INVITE Feature-Caps token 一致。step5 明文在不支持资源共享或不存在用户与 Feature-Caps 所指 UE 的绑定时返回 403/Warning100 并停止。随后媒体验证缺 MCPTT speech codec 则 488，支持所需媒体参数的资源不可用则 500 并停止。通过后才分配会话 URI。

依据：§8.2.2 steps1–8;8.1A;6.3.7.1。

## 200 前的媒体处理与之后的 ICE

适用条件：§8.2.2 steps1–8 未拒绝请求，参与功能已分配预建立会话 URI。

按 §6.3.2.1.5.2 构造 INVITE 200：Contact 使用该预建立 URI，PAI 为参与功能 PSI，Supported 含 norefersub，并附带 ICE candidates 的 SDP answer。SIP core 支持资源共享时，还带 Resource-Share answer，其 media-sharing、session-initiator、timestamp 和逐 m-line sharing rules 依该条设置。先完成 §24.380 媒体处理，再发 200，随后执行 ICE candidate evaluation；选到非默认 candidate pair 时须再按 §8.3 进行 offer/answer。客户端收到 INVITE 2xx 后另执行媒体交互。

依据：§8.2.2 steps9–12 and Notes1–2;8.2.1 final paragraph;6.3.2.1.5.2。

## 空闲时由客户端修改

适用条件：既有预建立会话当前没有关联的 MCPTT 呼叫，客户端需修改其参数。

客户端发送 UPDATE 或 re-INVITE，附 SDP offer，必要时带 ICE candidates。参与功能要求 offer 至少有一个媒体流，其媒体参数和至少一个 codec 可接受，否则 488；通过则生成带 SDP answer 的 200，Contact 带预建立会话 URI。客户端保留先前协商资源直到收到 200；收到后，若参数/codec 改变或原用媒体流被 answer 拒绝，按 §24.380 处理媒体。

依据：§8.3.1.1;8.3.2.1。

## 空闲时由服务器修改

适用条件：既有预建立会话当前没有关联的 MCPTT 呼叫，参与功能需修改其参数。

参与功能生成 UPDATE 或 re-INVITE 和 SDP offer，必要时带 ICE candidates；若移除 media-floor control entity，发送前先按 §24.380 交互。客户端若找不到至少一个参数与至少一个 codec 可接受的媒体流则 488，否则生成 SDP answer/200。参与功能收到 200 后按改变的参数/codec、被拒绝的原用流及新接受的未使用流分别交互媒体；该条注释要求在收到 200 前保留先前协商资源。

依据：§8.3.1.2;8.3.2.2。

## 客户端拆除预建立会话

适用条件：客户端要拆除 §8.2.1 建立的预建立会话本身，而非仅离开其承载的一次呼叫。

客户端在预建立 SIP dialog 内发 BYE，Request-URI 使用预建立会话 URI，收到 BYE 200 后进行媒体交互。参与功能收到该 BYE 时：已建立业务会话按 §6.3.2.1.6 移除客户端；业务仍在建立则发 CANCEL，若随后收到该 INVITE 200 则仍按 §6.3.2.1.6 释放；没有业务呼叫则断开客户端侧资源并回 200。收到远端 BYE 200 的分支，先分别释放远端和客户端侧资源，再回客户端 BYE 200。

依据：§8.4.1.1;8.4.2.1。

## 服务器拆除预建立会话

适用条件：参与功能要拆除 §8.2.2 建立的预建立会话本身。

参与功能先按 §8.4.2.2 step1 释放使用该预建立会话的所有 MCPTT 呼叫参与关系，对各业务会话朝控制功能发送 BYE 并处理对应媒体。随后向客户端在预建立 dialog 内发送另一条 BYE，其 Request-URI 是预建立会话 URI；收到该 BYE 200 后处理媒体。业务会话身份与预建立会话身份在这两段 BYE 中用途不同。

依据：§8.4.2.2。

## 证据边界

- TS24.229、TS24.380、TS29.214、RFC4028、ICE 及 PCC 内部过程未独立核验，不能由此交付可运行的完整 SIP/媒体实现。
- 这里只核第 8 章的建立、无关联呼叫时修改和拆除；未给出固定刷新频率、连接保活、故障自动恢复或媒体复用容量算法。
- 注册及服务设置仅为已核条款引用的前提，本次不重做认证、设置发布或 Rx 协议。支持资源共享不豁免 §8.2.2 的身份、本地授权、媒体和资源检查。
- 没有推导固定会话寿命、刷新频率或掉线自动重建算法。§8.2.1 step8 原文先称 refresher header field，后称 header field parameter；保留其所指 Session-Expires 参数边界。
- 不把 step4 的 SIP-core 条件移植成 step5 的额外限制，也不据 step5 推断所有 direct-Rx 实现必被拒；本版两处条件的适用衔接未在本次展开。Warning100 的详细 reason 随失败原因，不用业务权限 Warning109 替代。
- 200 是预建立建立响应，不证明具体组呼已经授权或有人接听。不能把 ICE evaluation 写成发送 200 前已经全部完成。§6.3.2.1.5.2 的 Require=timer、Session-Expires 及默认 refresher=uac 等通用构造仍适用。
- 无关联业务呼叫是入口条件，不是任意进行中组呼改参规则。所读条款没有定义 4xx 后自动重试、修改回滚或事务竞态算法。
- 不能把保留资源的注释扩大成发送请求前绝不进行任何媒体操作；移除 floor-control entity 的前置交互是正文明确分支。
- 这是本版明文给出的 CANCEL/成功交叉情形，不是 SIP 全部竞态实现。业务释放后保留预建立会话的另一条路径不能反过来阻止本条真正拆除。
- 原文 step1(f) 将执行角色称为 terminating MCPTT function，而本节主体为 participating；保留称谓差异，不据此另造第三实体。客户端接收端 §8.4.1.2 对有业务与无业务分别处理，本次不补写其未明列的统一应答/超时状态机。

## 按需继续

- [preestablished-group-association](preestablished-group-association.md)
- [group-participant-leave](group-participant-leave.md)
- [group-participant-removal](group-participant-removal.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页95、108、109、164、199、200、201、202、203、204、205；仅本版本。

按需核对媒体层指定分支：[mcpc-disconnect-evidence](mcpc-disconnect-evidence.md)。来源版本及条件以该页为准。
