# MCPTT 远程发起私呼：甲请乙呼叫丙，谁收请求，谁收结果？

这个流程中，**甲提出请求，乙实际发起私呼，丙是被叫**。也可以让乙呼叫甲，此时甲既是请求人，也是被叫。这里限在网按需私呼；请求乙拨号的 SIP MESSAGE 不是乙拨打这通私呼的 INVITE。〔TS 24.379 V16.14.0，Rel-16，Stage 3，§11.1.7.1、§11.1.7.2.1–.2，印刷页 415–417〕

## 请求中的两个目的：交给乙处理，请乙呼叫丙

甲客户端发送远程发起请求时，Request-URI 填服务甲的参与 MCPTT 功能（PF）的公共服务标识（PSI）；`resource-lists` 里的 MCPTT ID 指向**接令并拨号的乙**；`mcptt-called-party-id` 填**被叫丙**的 MCPTT ID。甲侧 PF 在向控制功能发出的请求中，把由收到的 P-Asserted-Identity 对应查得的甲的 MCPTT ID 写入 `mcptt-calling-user-id`。乙客户端处理到达自己的请求时，从 `mcptt-called-party-id` 取被叫，并按在网按需私呼流程发起呼叫。不能把传送指令的 Request-URI 或 `resource-lists` 当成被叫 ID。〔§11.1.7.2.1 步骤 2d–f、§11.1.7.2.2 收请求步骤 2–3、§11.1.7.3.1 步骤 2、6–9，印刷页 415–416、418〕

## 什么时候没有单独的结果 MESSAGE？

乙完成发起流程后，必须同时核对两件事：**乙收到的请求中，被叫 ID 与 `mcptt-calling-user-id` 相同；乙成功发起了这通私呼**。两项都成立，乙应跳过后续的结果发送步骤。比如，甲请乙呼叫甲，乙成功发起，则不另发业务结果。甲请乙呼叫甲但乙发起失败，仍要发失败结果；甲请乙呼叫另一个用户丙，不论发起成功或失败，也要另发结果。仅看未收到一条 MESSAGE，不能反推乙成功，也不能断言乙没发送。〔§11.1.7.2.2 发起流程完成后的步骤 1 及注，印刷页 417〕

其余情形，乙发出一条**新的 SIP MESSAGE**：Request-URI 指向服务乙的 PF；`resource-lists` 使用乙收到的请求中 `mcptt-calling-user-id` 的值，指定结果发给甲；`mcptt-called-party-id` 仍是乙所呼叫的目标。正文 `response-type` 是 `remotely-initiated-private-call-response`，用 `remotely-initiated-call-outcome` 的 `success` 或 `fail` 报告发起结果。甲若实际收到此业务结果，从该字段判断成功或失败。原请求的 SIP 事务响应不是这条业务结果；即使业务结果是 `success`，也不能据此证明双方实际收听或通话。〔§11.1.7.2.2 发起流程完成后的步骤 2–4、§11.1.7.2.1 收结果步骤 1，印刷页 416–417〕

若是在被叫忙时留下请求，由被叫用户后来决定拨回，查[私呼回电](private-callback.md)；若要判断实际接通，还要查[按需私呼的应答与媒体证据](private-client-answer-evidence.md)。

依据：[3GPP TS 24.379 V16.14.0，Release 16，Stage 3，印刷页 415–418（ETSI）](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=416)。
