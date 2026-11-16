# FD 发送准入：文件上限、单次额度与拒绝来源

限在网、普通 one-to-one 或已配置组的 FD。HTTP 错误映射只适用于 claim 指定的 HTTP FD SIP MESSAGE 分支。

逐项检查按 §11.1 的顺序及各步骤适用条件执行；前序若已要求停止，则不继续后面的检查。角色名 client、PF、CF 分别指 MCData 客户端、参与功能、控制功能。

不包含别名解析、重组、ad hoc、跨域网关、紧急或迫近危险扩展；不声称覆盖全部 FD 准入。

## 客户端与CF的文件上限

适用条件：用户拟发送 FD；已执行前序适用的传输控制，尚未被拒绝。

one-to-one FD 拟发送的数据大小超过服务配置的 max-data-size-fd-bytes，或组 FD 超过该组的 mcdata-on-network-max-data-size-for-FD 时，客户端与 CF 都须判定因文件大小而不允许发送，并停止 §11.1 后续步骤。比较符为严格大于；刚好等于上限不触发本项拒绝，但不代表其他检查通过。§10.2.1.1 在选择 HTTP 或媒体面之前调用 §11.1。

- 这是 FD 文件大小限制，不是 SDS 控制面阈值，也不是 §11.2 自动接收阈值。
- 配置值来自相应配置/组文档；本页未读取 TS 24.484 或 TS 24.481 来核 schema、默认值或缺失数值的处置。

依据：§11.1 steps4,6;10.2.1.1 steps1,2，印刷页 264、265、311。

## 共享单次请求额度

适用条件：FD 继续进入 §11.1 的 one-to-one 或组 MCData 单次请求额度检查。

文件上限没有替代单次请求额度。one-to-one 的 payload 大于用户配置 MaxData1To1，由客户端与 PF 判定不允许并停止；组 payload 大于组文档相应 entry 的 mcdata-max-data-in-single-request，由客户端与 CF 判定不允许并停止。两项也是严格大于才触发。这使私聊 FD 的文件上限与单次额度由不同服务器角色承担。

- 源文 steps4/6 写拟发送的数据/文件大小，steps7/8 写 payload。不能未经依据把 HTTP FD 的 URL 字符串长度、信令体长度和实际文件字节数视为同一个计量值。
- 本页没有核出 HTTP FD 在服务器侧计算该 payload 大小的统一算法，不把两种上限合并成一个 min 值公式。

依据：§11.1 steps4,6,7,8，印刷页 311。

## 私聊HTTP的条件化拒绝映射

适用条件：O-PF 收到 HTTP FD 请求并已到达 §10.2.4.3.1 steps6,7；application/vnd.3gpp.mcdata-info+xml 中不含 mcdata-controller-psi。；§11.1 step7 判定因 one-to-one 单次请求额度超限而不允许发送。

此分支由 O-PF 返回 SIP 403、Warning202，并停止该调用过程。Warning202 在这里对应单次请求额度超限，不能据此改写为 FD 文件大小服务上限超限；该错误映射还受 mcdata-controller-psi 缺失的外层条件约束。

- mcdata-controller-psi 存在时不能照抄这个 step7 映射；也不能据此声称 §11.1 的传输控制义务被取消。
- §11.1 step4 的私聊 FD 文件上限责任仍在客户端与 CF；本页已核 HTTP 调用分支未为该项核出专用 Warning 映射，不编造对应码。

依据：§10.2.4.3.1 steps6,7b;11.1 step7，印刷页 278、311。

## 组HTTP的相同Warning不能唯一定位原因

适用条件：CF 正在处理 HTTP FD 的 FD SIGNALLING PAYLOAD，request-type 为 group-fd，前序检查通过并到达 §10.2.4.4.2 step12f。

若 §11.1 step8 判定组单次额度超限，CF 返回 SIP 403、Warning208 并停止；若 step6 判定该组 FD 文件大小上限超限，源文也要求 SIP 403、Warning208 并停止。两个分支使用同一代码，后者的 Warning 说明仍描述单次额度。排障时只有 403/208 不足以唯一定位超的是哪一种上限，须结合命中分支和配置值。

- 保留 V19.7.0 的代码和说明，不把文件上限分支自动修成另一个 Warning。
- 本条只说明两个大小拒绝分支，不复述组文档取得、组禁用、成员、服务许可和归属的全部前置检查。

依据：§10.2.4.4.2 steps12f(ii),12f(iii);11.1 steps6,8，印刷页 284、311。

## 证据边界

- 没有覆盖媒体面 FD 的具体 SIP 错误映射、上传协议内部限制或错误重试。

## 按需继续

- [fd-msrp-start-and-originator-result](fd-msrp-start-and-originator-result.md)

- [fd-http-file-and-signalling-evidence](fd-http-file-and-signalling-evidence.md)
- [fd-download-decision-and-completion](fd-download-decision-and-completion.md)
- [sds-transmission-selection](sds-transmission-selection.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 条款衔接边界

- §10.2.4.4.2 steps12f(ii),12f(iii)：组单次额度和组 FD 文件大小拒绝都使用 403/Warning208，第二分支仍带单次额度说明。按原文保留；不宣称一条 Warning 唯一对应一个根因。
- §11.1 step4;10.2.4.3.1 step7;10.2.4.4.2：私聊 FD 文件上限在 helper 约束客户端与 CF；已核 HTTP O-PF step7 为其他拒绝定义响应，CF 的私聊分支未给出该上限的专用响应映射。不虚构码，也不把 O-PF 单次额度检查当成该 CF 文件上限检查。
