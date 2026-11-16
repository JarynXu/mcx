# FD 文件可用期：逐消息计时、过期通知与删除条件

限 CF 已处理的正常 HTTP FD 请求，相关前序准入已通过；未扩媒体面 FD 的可用期处理。

文件可用计时器 TDC2 与接收客户端等待决定的 TDU2 不同。文件 URL、Conversation ID 和 Message ID 保持各自含义。

到期通知、列表移除和内容服务器文件删除分别按明确条款判断，不能互相替代。

## 逐消息的可用期

适用条件：CF 处理 FD SIGNALLING PAYLOAD，metadata 是否存在及所需配置值已确定。

按 §10.2.4.4.2，有 Metadata IE 时，CF 以其中的 file availability 信息与 max-file-availability 的较小值形成可用期计时值；没有 Metadata IE 时使用 default-file-availability。之后启动 TDC2，并关联 Conversation ID、Message ID 和可选应用标识。同一物理文件可有多个计时器，各按 Conversation ID/Message ID 唯一关联；延期或接受动作本身没有被本条规定为延长文件可用期。

- 不造统一 TDC2 数值。metadata 的 file-availability 编码为截止日期时间；本页未核配置 schema、单位转换和时钟异常规则。
- §12.4.1.1/F.2.2 概述为 metadata 或本地策略，HTTP 专用 step9 给出了 max/default 配置算法；不只引用概述来略掉该限制。

依据：§10.2.4.4.2 steps9,13,14 and NOTE4;12.4.1.1;15.2.17;F.2.2 Table F.2.2-1 NOTES2,3，印刷页 282、283、285、323、370、639。

## 到期通知的接收范围

适用条件：与特定 Conversation ID 和 Message ID 关联的 TDC2 到期。

CF 的到期目标是已收到该 HTTP FD、但尚未下载文件的客户端：私聊对应目标，或组通信中满足这一条件的各客户端。CF 给这些目标发送 FD NETWORK NOTIFICATION，类型为 FILE EXPIRED UNAVAILABLE TO DOWNLOAD，携带原关联 Conversation ID、Message ID、当前时间及已关联的应用标识。不能改写为给全组所有成员、所有静态成员或已经下载者统一发送。

- CF 如何取得所有下载状态的实现接口未在这些段落展开；不声称任意通知缺失就能准确证明没有下载。
- §12.4.2.2 对 notification type 的交叉引用写 15.2.6，但实际 FILE EXPIRED 编码在 §15.2.18，保留该来源差异。

依据：§12.4.1.1;12.4.2.1;12.4.2.2;15.1.9.1;15.2.18，印刷页 323、324、357、370。

## 通知与物理删除

适用条件：到期 FD NETWORK NOTIFICATION 沿 PF 送到接收客户端，各角色资源及身份检查未拒绝。

PF 按 HTTP FD 终止侧过程处理；收到 FILE EXPIRED 时，§10.2.4.3.2 要求从 stored file list 移除相应文件条目。客户端先回 SIP 200，再解码网络通知，有应用标识则交给应用，没有则交给用户。这些动作表达文件已不能再下载及本地通知/记录处理；§12.4.2.2 本身没有规定内容服务器此时必须执行物理删除，接收端的 200 也不证明用户已经看到通知。

- PF 移除条目在原文仅写用 Conversation ID 识别；CF 的计时器却以 Conversation ID 与 Message ID 关联。不静默替换其键，也不据此设计会误删同一会话其他文件的实现。
- 不宣称文件过期后永远不能由其他授权过程恢复；只描述本次 FD 的可下载状态通知。
- 未知应用标识的专门处理未在 §12.4.4 列出，不从初始 FD 下载过程移植同一异常动作。

依据：§12.4.2.2;12.4.3;12.4.4;10.2.4.3.2 steps1–5，印刷页 279、280、324、325。

## 全部拒绝时的删除条件

适用条件：CF 收到 FD REQUEST REJECTED disposition；已通过 §12.2.3 的资源、服务标签、目标和 Conversation ID/Message ID 关联检查。

没有组标识的 FD 拒绝，或带组标识且其他被邀请组员的通知已全数收到并全部拒绝时，CF 执行两项义务：若该文件没有其他仍运行的可用期计时器，删除 media storage function 内与该 Conversation ID/Message ID 关联的文件；停止该通知关联的 TDC2。原文列删除条件在前、停止关联计时器在后，不可改写为先停计时器再据此决定删除。因此一个组员拒绝、一个用户接受、一个计时器停止，都不能单独推出存储文件应删除。

- 没有从本条推导所有下载完成后也自动删除；原文这里的触发是拒绝及所列集合条件。
- 关联失败须回 403/Warning216 并停止，不能使用无法关联的通知删除文件。
- 删除操作的具体存储 API 和并发实现未核。

依据：§12.2.3 steps1–6;F.2.2 Table F.2.2-1 TDC2 normal stop，印刷页 318、319、639。

## 证据边界

- 未扩主动终止、服务器提前删除、授权用户删除或媒体面 FD 释放过程。

## 按需继续

- [fd-download-decision-and-completion](fd-download-decision-and-completion.md)
- [fd-http-file-and-signalling-evidence](fd-http-file-and-signalling-evidence.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文疑义

- §12.4.2.2 step2a;10.2.4.3.2 first step5;15.2.18：FILE EXPIRED 的交叉引用指向 15.2.6，实际网络通知编码表在 15.2.18；不把 FD disposition 枚举与网络通知枚举合并。
- §10.2.4.3.2 first step5;12.4.1.1;12.4.2.2：PF 清理列表只写 Conversation ID，CF 计时器与到期通知按 Conversation ID/Message ID 关联。保留差异，不声称已经核出安全的存储键实现。
- §F.2.2 Table F.2.2-1;12.4.1.1;12.4.2.2：定时器表列 HTTP 或媒体面，12.4 明示 HTTP 文件分发目标；本页刻意只取 HTTP 子集，不从该差异扩展媒体面到期全链。
