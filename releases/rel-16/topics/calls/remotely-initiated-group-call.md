# 远程发起 MCPTT 组呼：请求和结果各填谁的 PF？

甲请求乙发起对组 G 的呼叫。**甲是请求者，乙是实际发起组呼的远端用户，G 是目标组。** 委托请求和乙之后送回结果的两份 SIP MESSAGE，各有自己的目标。在 TS 24.379 V16.14.0，不能把[远程发起私呼](remotely-initiated-private-call.md)首跳的规则照搬给组呼。〔§§10.1.5.1、10.1.5.2.1–.2，印 313–316〕

## 甲发委托：外层找乙的 PF，名单写乙，业务正文写组 G

在甲的客户端发出 `remotely-initiated-group-call-request` 时，外层 SIP `Request-URI` 填**服务乙的参与 MCPTT 功能（PF）的公共服务标识（PSI）**。资源列表写乙的 MCPTT ID；`mcptt-info` 正文中的 `mcptt-request-uri` 写 G 的组身份，不写甲或乙的用户 ID。这里说的是客户端构造的消息；不是说所有后续转发腿沿用同一个 Request-URI。〔§10.1.5.2.1 第 3d–f 项，印 314–315〕

甲的客户端先查自己的业务档。没有 `allow-request-remote-init-group-call`，或值为 `false`，须停止该过程。甲若要求先查乙是否归属 G，另走第 2 项的权限、查询及关联结果检查；不能把没做前置查询当作其他角色免查。〔§10.1.5.2.1 第 1–2 项，印 313–314〕

## 到 CF 时再看归属；它发出的正文里，组和用户换了位置

控制 MCPTT 功能（CF）收到业务类型为 `remotely-initiated-group-call-request` 的 MESSAGE 时，若按 §6.3.6 判定资源列表所指的乙**未归属**入站 `mcptt-request-uri` 指明的 G，须回 **SIP 403**，Warning 文本中的 MCPTT 业务编号为 **120**，并停止本程序的剩余步骤。这是 CF 对委托请求的条件；不能因甲没要求前置检查而略过，也不能对乙后发的业务结果套用这个请求专用的拒绝分支。〔§10.1.5.4 第 3 项，印 318〕

如果流程走到 CF 发出 MESSAGE，出站正文用 `mcptt-calling-group-id` 保留入站写在 `mcptt-request-uri` 的组身份 G，再把出站 `mcptt-request-uri` 改填入站资源列表所指的用户。外层 Request-URI 用与这个**接收用户**对应的终接 PF 的 PSI。对委托请求，接收用户是乙；对乙返回的结果，则是名单里的甲。条款把怎样找到终接 PF 地址留在本版本范围外。〔§10.1.5.4 程序入口、第 7–8 项及注，印 318–319〕

## 收到请求的 200，不是收到乙的组呼结果

发起侧 PF 收到对它发出的 MESSAGE 的 2xx 后，须向其客户端生成并返回对应的 SIP 200；CF 也有对下游 2xx 生成上游 200 的步骤。这是**所对应的 MESSAGE 事务**的响应。只看到甲侧针对委托的 200，不能登记乙的组呼已发起成功，也不能把没看到后续结果记成业务失败。〔§§10.1.5.3.1、10.1.5.4 末段，印 317、319〕

乙的客户端收到委托后调用组呼发起程序。该程序结束时，乙按组呼的规定**另发一条 SIP MESSAGE**。外层 Request-URI 填**服务甲的 PF 的 PSI**；资源列表用乙收到的委托里 `mcptt-calling-user-id` 的值；正文 `mcptt-request-uri` 写被呼叫的组 G。正文 `response-type` 是 `remotely-initiated-group-call-response`，`remotely-initiated-call-outcome` 为 `success` 或 `fail`，说明乙发起这次组呼的结果。甲按这个字段判业务成功或失败，不拿委托 MESSAGE 的 200 代用。成功也不是所有组员已经加入或收到媒体的证据。〔§10.1.5.2.1 结果接收段，印 315；§10.1.5.2.2，印 315–316〕

来源：[TS 24.379 V16.14.0，Release 16，Stage 3（ETSI），客户端两向 MESSAGE，印 313–316](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=314)；[PF 和 CF 响应及转发，印 317–319](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=318)。
