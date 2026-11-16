# 服务器授予后的媒体计时：T20 重传、T1 静默与 T2 超时撤销

限 TS24.380 V19.1.0 普通在网、已协商话权控制的呼叫；非广播、system、emergency、imminent-peril、ambient listening 或 temporary group session。

不采用 dual floor、multi-talker、audio cut-in 或抢占；本页不处理并发话者、跨组重组和优先级切换。

G 状态属于服务器 general floor control arbitration；服务器每客户端 U 状态及客户端自身 U 状态不是同一个状态机。各条保留明确事件和状态。

只核已经授予后的媒体与计时器行为。进入 Floor Idle 后是否立即选取下一请求，须转查仲裁主题；不得把 Floor Idle 等同整场通话结束。

## 授予时启动哪些计时器

适用条件：服务器按 §6.3.4.4.2 进入 G:Floor Taken，并已确定本次获授权的 participant；另判断其请求此前是否排队。

发送 Floor Granted，Duration 携 T2 的值，并启动该 participant 的 T1；只有此前排队的请求才启动 T20、初始化 C20=1。此处没有启动 T2 的步骤，不能把 Duration 当作从 Granted 发出时开始的说话倒计时。服务器还向其他 participant 发送 Floor Taken，并将 general state 设为 G:Floor Taken。

依据：§6.3.4.4.1–.2;6.3.4.4.5，印刷页 63、64、65。

边界：本条提取计时职责，不是完整 Granted/Taken 字段模板。表11.1.3-1 的 T20 启动描述还明确该 queued participant 已协商 queueing。

## 获授用户开始发送 RTP

适用条件：服务器处于 G:Floor Taken；media distributor 报告收到 permitted MCPTT client 的 RTP。

本普通非 ambient 范围内，若该 participant 的 T2 尚未运行则启动；重启其 T1，停止仍运行的 T20，按 local policy 指示分发 RTP，仍处于 G:Floor Taken。T2 已运行时不因每个 RTP 包重新开始，T1 则按收包重启。

依据：§6.3.4.4.5，印刷页 65。

边界：输入必须来自 permitted 客户端，不能把任意收到的 RTP 当作授予或延长占用的依据；本条不证明媒体解密、真实性或所有接收端实际播放成功。

## T20 到期不单独撤权

适用条件：服务器处于 G:Floor Taken，已为此前排队且获授予的 participant 启动 T20；发生 T20 到期事件。

C20 尚未达上限时重发 Floor Granted、重新启动 T20 并把 C20 加1；到期且 C20 已达上限时仍保持 G:Floor Taken，不由该事件单独撤权或结束通话。表11.2.3-1 明确达到上限后不再重发；整个 Granted 重传时间另受 T1 限制。

依据：§6.3.4.4.9–.10;11.1.3 Table11.1.3-1 Note3;11.2.3 Table11.2.3-1，印刷页 68、245、250。

边界：不把计数加1本身当作新的到期事件，也不据默认值虚构固定收回时刻；不将 C20 上限当成客户端已确认的证据。

## T1 到期与缓冲例外

适用条件：服务器处于 G:Floor Taken，获授权 participant 的 T1 到期；未采用 multi-talker。

停止该 participant 仍运行的 T2、T20，要求停止向其他客户端分发从该 participant 收到的 RTP；若正在进行 RTP 缓冲，已经在缓冲中的包是明示例外。随后按 §6.3.4.3.2 进入 G:Floor Idle 的处理，不能写成无条件丢弃所有缓冲音频或直接拆除整场呼叫。

依据：§6.3.4.4.3，印刷页 64。

边界：本条只写进入 Idle 处理的调用边界，不重复下一请求选择。该缓冲例外不能移植到客户端收到 Revoke 后丢弃剩余缓冲 RTP 的不同分支。

## T2 到期进入撤销宽限

适用条件：服务器处于 G:Floor Taken；该 participant 的 T2 到期。

停止其 T1；以原因 #2（Media burst too long）进入 pending Floor Revoke 处理，向该 participant 发 Floor Revoke，若原 Floor Request 有 Track Info 则携存储值，启动 T3 并设为 G:pending Floor Revoke。不是仅刷新 Duration，也不是此刻直接完成整场呼叫释放。

依据：§6.3.4.4.4;6.3.4.5.2，印刷页 64、65、71。

边界：本普通范围排除需另带特殊 Floor Indicator 的呼叫类型。本条只证明进入撤销宽限状态，不给出 T3 到期后的完整路由算法。

## 服务器宽限不授权客户端续发

适用条件：服务器已处于 G:pending Floor Revoke，T3 正运行；media distributor 报告收到该 permitted participant 的 RTP。

服务器重启 T1，按 local policy 继续分发这些 RTP，仍留在 pending Floor Revoke。服务器的宽限期处理不授权已经收到 Revoke 的客户端继续发送；客户端停止发送及缓冲清理按其自身状态机另行判断。

依据：§6.3.4.5.1;6.3.4.5.3;6.2.4.5.4，印刷页 45、70、71。

边界：§6.3.4.5.3 Note1 给出 T3 上限小于 T1 上限时 T1 不会到期的限定说明；不能省略配置关系写成任何部署都由 T3 先到期。

## Ack 与服务器重传

适用条件：服务器每客户端接口处于 U:not permitted and Floor Idle 或 U:not permitted and Floor Taken，收到 general arbitration 发来的 Floor Granted。

转发 Granted，可请求 Floor Ack，随后进入服务器接口的 U:permitted。相关 Note 将收到或未收到 Floor Ack 后怎样处理留给实现选择，不能据此写出普遍的“收到 Ack 就停止 T20”。客户端 queued 收到 Granted 仍可能等待自己的 T132 内用户确认，与这些服务器状态分开判断。

依据：§6.3.5.3.5;6.3.5.4.9;6.2.4.9.4;6.2.4.9.12，印刷页 83、91、92、52、54。

边界：也不能反向声称实现绝不允许用 Ack 管理重传；本条仅否定本版本给所有部署规定同一种 Ack 后动作。

## 默认值不是部署值

适用条件：查阅服务器 T1/T2/T20 和 C20 配置依据；未取得实际部署的配置文档。

表11.1.3-1 列 T1 默认4秒、最大6秒；T2 的原标签是 Default maximum value，值为30秒；T20 默认1秒。表11.2.3-1 列 C20 默认上限3。它们均可配置并引用 TS24.484 的指定元素，不能把这些数值断言为当前部署值，或把 T2 的30秒改写成所有配置不可超过的硬上限。 表11.2.3-1的注另规定：计数器未配置时使用默认值；这条明确规则不等于已知某部署未配置。

依据：§11.1.3 Table11.1.3-1;11.2.3 Table11.2.3-1，印刷页 241、243、245、249、250。

边界：本页已核 C20 未配置时使用默认值的注；TS24.484 的配置获取、其他缺省继承、取值校验和版本衔接未核，不生成可直接部署的配置。

## T1 选值与重传窗口

适用条件：为普通在网服务器选择 T1/T20 配置，尤其为已排队后获授予的 participant 预留发送准备时间。

T1 的最小取值 SHOULD 大于服务器至远端 participant 的预期往返时延，低带宽空口需考虑额外延迟；queued participant 获授予时可将 T1 设得比通常更高。T20 的总重传窗口受 T1 限制。不得从这些文字补造 T20×C20+T132 的在网固定公式，也不能把“比通常更高”无条件解释为可超过表列最大值。

依据：§11.1.3 Table11.1.3-1 Notes1–3，印刷页 245。

边界：本条没有确定哪一个计时器在具体运行时先到期；T132 属客户端用户确认计时，不是服务器 T20 的别名。

## 证据边界

- 不包含请求准入、优先级比较、排队排序、下一请求选择或从非控制服务器切换的队列迁移。
- 不把 G:Floor Taken、服务器接口 U:permitted 和客户端 U:has permission 视为同一时点。
- T2 到期后的研究边界到进入撤销宽限及其 RTP 行为；T3 结束、T8 重复 Revoke 与违规媒体发送的完整接口状态链未在本页闭合。
- 未核消息字段二进制编码、完整媒体安全、部署值或计时器同时到期的调度顺序。
- TS24.380 V19.1.0 与既有 TS24.379 V19.4.0 主题只作条件关联，不宣称完整版本互操作。
- §6.3.4.4.9 versus 6.3.4.4.2（印刷页63、64、68）：T20 重发段仅重列部分 Granted 字段，不据此删掉初次发送字段，也不自行补完整重发报文模板。
- §6.3.4.5.5 steps2–6（印刷页72）：T3到期段 step2 明限 multi-talker，step3 发送 Floor Release Multi Talker 却未重复该条件，后面又依赖当前 talker list；本页不将它无声改成普通单话权的完整退出算法。
- §11.1.3 Table11.1.3-1 T1 and Note2（印刷页243、245）：同时保留 T1 表列最大6秒及 queued 情况可高于通常值的说明；原文没有在 Note2 明写豁免最大值，不能自行选择一种覆盖另一种。

## 按需继续

- [floor-participant-entry-request](floor-participant-entry-request.md)
- [floor-participant-queue-release](floor-participant-queue-release.md)
- [group-release-timers](group-release-timers.md)
- [floor-state-ownership](floor-state-ownership.md)
- [floor-server-release-selection](floor-server-release-selection.md)

[ETSI 官方 TS24.380 V19.1.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124380/19.01.00_60/ts_124380v190100p.pdf)；仅上述版本和条款。
