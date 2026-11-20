# 原组已重组：302 里的宿主 PSI 和临时组 TGI 分别用在哪？

Rel-16、Stage 3。本文从一笔仍以原组 ID 请求建呼的 INVITE 看三份证据：收到原 INVITE 的控制功能如何处理，发起侧参与功能怎样使用 302，临时组宿主根据本机是否已有呼叫做什么。以同系统在网为例，不讨论跨系统路由和重组本身怎样创建。

## 控制功能不是临时组宿主，才走这里的 302

先核 §6.3.5.2(6) 的入口。实际收到的是按 §6.3.1.1 归为给组控制功能的 INVITE，经过 PSI 路由交给控制功能，Request-URI 是组服务 PSI、Contact 不含 `isfocus`。其 MCPTT-info 正文的 `mcptt-request-uri` 仍指向原组，且与其匹配的文档显示原组已经重组。控制功能从原组文档取关联的临时组标识（TGI）。第 (4)(b)(iii) 项识别文档类别时写的是 `on-network-regrouped`；第 (6)(a) 项取值时写的是 `regrouped` 的 `temporary-MCPTT-group-ID` 属性。两处字面各自保留，不据此补组文档格式。

本机不托管这个 TGI 时，停止处理**本笔 INVITE**，在这笔事务上回 302（Moved Temporarily）。两个标识用途不同：

- SIP `Contact` 是托管这个 TGI 的 MCPTT 服务器的公共业务身份（PSI），给出下一请求的 SIP 目标。
- MCPTT-info 正文的 `mcptt-request-uri` 是临时组的 TGI，给出下一请求的业务组目标。

**发起侧参与功能（O-PF）实收匹配的 302 后，才核下一笔。** 以客户端发 INVITE 的按需聊天组为例：O-PF 实际收到客户端 INVITE，向控制功能发出 INVITE，随后实际收到该事务的 302；若 `Contact` 含 SIP URI，且有含 `mcptt-request-uri` 的 MCPTT-info XML，按 §6.3.2.1.10 生成新 INVITE。新请求的 SIP Request-URI 取自 302 的 `Contact`，新正文的 `mcptt-request-uri` 取自 302 正文，`mcptt-calling-user-id` 仍是先前确定的主叫 MCPTT ID。只有 302 正文实际带 `session-type` 时才以该值设置新请求的此字段；不能从 302 状态推得它必有。按需聊天组发起条文另规定基于原客户端 offer 构造 SDP offer，再转送这一请求。

CF 发出 302、O-PF 实收 302 并发送新 INVITE、真正宿主收到新 INVITE 是三次取证。仅有 302 不证明后两项、原腿成功、宿主的呼叫已建立或媒体已通。别把任意 302 都归到这里：例如 §6.3.3.1.13.7 的 OPTIONS 授权另有产生 302 的路径。预安排终止侧 §10.1.1.4.2(5b) 另写到重组的 403/Warning text 148；同处 (5c)(ii) 又写组文档处理已发送最终错误或重定向就不再继续。不要按本页推断优先级，也不要对同一笔生成两个最终响应。

依据：[§6.3.1.1，印 78](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=79)；[§6.3.5.2(4)、(6)(a/b)，印 131–132](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=132)；[§6.3.2.1.10，印 92–93](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=93)；[§10.1.2.3.1.1，印 278](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=279)。相邻不同路径：[§6.3.3.1.13.7，印 115](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=116)；[§10.1.1.4.2(5)，印 243–244](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=244)。

## 本机就是临时组宿主，按 TGI 对齐实际呼叫状态

以下仍是第 (6) 项的原组 INVITE 分支。**不要把 O-PF 重送后已直接携带 TGI 的 INVITE 当作再次进入第 (6) 项。** 若新请求同样属于送控制功能的 INVITE，且取到的文档对应 TGI，另查第 (8) 项的守卫。

- **这个临时组的呼叫已在进行：** 宿主把主叫 MCPTT ID 关联到该临时组呼叫，执行所引用的媒体面交互，并退出这一条组文档程序。查本机该 TGI 的进行中呼叫和主叫关联记录。此处没有指定一个成功应答，关联和媒体面交互也不等于终端实际入会、获准发话或收到了 RTP。
- **这个临时组没有正在进行的呼叫：** 宿主尚未订阅其文档时，才订阅该 TGI 的 `xcap-diff` 事件包。实际收到含该 TGI 文档的通知，或本机已经缓存该文档时，从文档的 `constituent-MCPTT-group-ID` 读取组成组 ID。订阅送出、收到订阅成功及具备匹配文档分别取证，均不证明新呼叫建立。紧邻的 (6e/f) 错误分支字面指 TGI 关联的 MCPTT 组 ID 文档，不能自动套成任意一次 TGI 订阅失败。
- **收到组成组提示时再看下一层守卫：** 原 INVITE 正文实际有 `associated-group-id`，该 ID 出现在 TGI 文档的组成组列表，且该组不归本机托管时，第 (6h) 项规定退出此程序、由非控制功能处进行用户授权。退出不是已获授权，更不是加入呼叫。

依据：[§6.3.5.2(6)(c)–(h)、(8)，印 132–133](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/16.14.00_60/ts_124379v161400p.pdf#page=133)。如果目前只能核到文档订阅或缓存，先查[组文档是否实际可用](../groups/mcptt-server-group-document-cache.md)；重组建立和客户端通知分别参见[同系统临时重组](../groups/single-system-temporary-regroup.md)与[预配置组重组通知](../groups/preconfigured-regroup-notification.md)。
