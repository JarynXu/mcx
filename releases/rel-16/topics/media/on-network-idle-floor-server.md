# 普通在网话权服务器：Idle 请求处理与条件授予

## 适用范围

- 固定 TS24.380 V16.9.0；普通在网、按需、单话权客户端与 controlling floor control server 的显式请求。排除 implicit、广播/system/emergency/imminent-peril、ambient、临时组、dual/multi-talker、抢占和 MBMS。
- 本页只处理已有 Idle U/G 上的非排队请求及其结果接口，不证明全部初始化、授权政策或队列调度已经闭合。适用的会话协商与媒体保护仍须满足，不能把请求、拒绝或尚未授予排除在共同条件外。
- PF、逐参与者 U、整通话 G 的动作按各自实际事件适用；拒绝、授予和对其他参与者的通知不是全局同时前提。

## PF 转发、逐参与者 U 与整通话 G 是不同责任

条件：会话已建立，本次是普通显式请求；请求方的服务器接口处于 U: not permitted and Floor Idle，仲裁 G 处于 Floor Idle。PF 的转发规则仅在其实际接收消息时适用。

PF 收到客户端话权控制消息须立即转交 floor control server；本页无 MBMS 子信道，收到 server 消息须立即转交客户端。服务器每通话有一个 G 仲裁实例，每参与者有一个 U 接口实例。普通非广播 U 收到关联参与者的 Floor Request 须转交 G，仍保持 not permitted and Floor Idle。允许提出请求，不等于已获发送许可。

强度：上述实例划分、转发与状态保持为 SHALL。

- 本页从已成立的 Idle U/G 开始，不把 SIP 200、客户端请求、组归属或 PF 转发当作这些状态已经正确建立的证明。§6.3.5.2.1 分别以服务端向主叫发 200、从被叫收 200 描述关联创建，不是话权授予。
- 初始化接口存在两个不能静默修复的边界：§6.3.5.2.2 step2a(ii)/2b(i) 命名 not permitted and Floor Idle，却回指实际设置 permitted 的 §6.3.5.5.2；step4b(ii) 则指向 §6.3.5.3.2。§6.3.4.2.2 无隐式授予分支调用 Idle helper，但 §6.3.4.3.2 两段入口都排除 Start-stop。本页不能据此补出统一初始化、首次 Idle 发送或 T4/T7 启动。

依据：3gpp-ts-24.380-v16.9.0 §6.3.1;6.3.2.2;6.3.4.1；§6.3.5.3.1–4；§6.4.1–2 non-MBMS branch；§6.3.5.2.1–2 steps2/4 (initialization comparison)；§6.3.5.5.2 (cited helper comparison)；§6.3.4.2.2;6.3.4.3.2 (initialization boundary)，印刷页 51,52,54,55,56,71,72,73,74,75,76,85,101,102。

## Idle 仲裁区分拒绝和条件授予，不设默认必授予

条件：G 在 Floor Idle 收到来自允许提出话权请求的参与者的 Floor Request；下述拒绝与授予是替代事件，不要求同时成立。

§6.3.4.3.3 的拒绝列表涉及通话只有一个客户端和关联参与者的 on-network-recvonly。若请求被拒，G 须发送 Floor Deny，按对应原因携 #3 Only one participant 或 #5 Receive only，可附解释文本；请求含 Track Info 时须复制，随后留在 Idle。仅当请求确已获授予时，G 须停止 T4/T7，保存获准参与者 SSRC 至该请求对应话权释放，条件保存收到的 Track Info，并调用 Taken 入口。

强度：拒绝后的发送、原因与条件 Track Info、状态保持以及 if granted 后续动作均为 SHALL；解释文本为 MAY。

- 拒绝入口原文引导语是 one of the following conditions，a/b 列表又以 and 连接。本页保留这处逻辑差异，不将其改成确定的 OR 或 AND 判定器；实现者不能凭本文解决只有其中一项为真的准入判断。
- if granted 是条件而不是未命中所列拒绝就必授予。优先级字段和策略输入不提供本页完整授权政策；不移植客户端、其他 Release 或离网仲裁规则。
- 表11.1.3-1 对 T4 normal stop 概括为参与者请求许可，而本条正文将停止 T4/T7 放在 if granted 中；不把表述概括反向改成每个到达请求均先停止。

依据：3gpp-ts-24.380-v16.9.0 §6.3.4.3.3；§8.2.3.4;8.2.3.13；§8.2.6.1–2；§11.1.3 table11.1.3-1 T4 comparison，印刷页 57,150,154,155,163,164,165,216,219。

## 实际授予后向获准者发 Granted，向其他参与者发 Taken

条件：本次普通非排队请求已获 G 授予，进入 §6.3.4.4.2；单话者，无 dual/multi-talker。不是由未拒绝推定此事件发生。

G 须向获准者发送 Floor Granted，Duration 取 T2 值、Floor Priority 为获授优先级，已存 Track Info 时携带。Duration 的单位是秒。G 须向其他参与者发送 Floor Taken：无 privacy 请求时携获准用户 ID，并可携 functional alias；位置不可得或 profile 不允许报告时 Location type=0，否则按位置表携值；Message Sequence Number 加一。普通非广播分支可携 Permission to Request the Floor=1，这只允许接收者提出请求。G 随后为获准者启动 T1，并置 Floor Taken。

强度：上述发送、条件字段、序号和 T1/状态动作为 SHALL；无 privacy 时 functional alias、非广播的请求许可字段为 MAY。

- Taken 是别人获准的通知，不能当接收者获准；Granted 说明授予发送许可，不证明 RTP 已到达或已向其他客户端播放。Request/Granted/Deny 的 User ID 等字段含离网专用项，不能照报文示意图全部搬入在网。
- §6.3.4.4.2 仅在请求此前已排队时启动 T20 并置 C20=1；本页非排队请求不继承此动作。计时表还要求已协商 queueing。T1 在授予发送时启动，T2 表中是检测 RTP 才启动；Duration 携 T2 的值不等于发送 Granted 时同时启动 T2。
- 消息与字段定义仍是编码依赖；本页不重建完整 RTCP、身份到 SSRC 配置、位置编码、密钥或授权政策。

依据：3gpp-ts-24.380-v16.9.0 §6.3.4.4.2；§8.2.2.1；§8.2.3.2–3;8.2.3.6–7;8.2.3.10;8.2.3.13;8.2.3.21；§8.2.4–6;8.2.9；§11.1.3 table11.1.3-1 T1/T2/T20;11.2.3 table11.2.3-1 C20 (comparison)，印刷页 59,60,148,149,150,151,152,153,154,155,159,160,161,162,163,164,165,167,168,169,218,219,220,224。

## U 下发结果不等于媒体送达，也不补排队调度

条件：对应 U 原在 not permitted and Floor Idle；分别收到 G 发来的 Granted、Deny 或给其他参与者的 Taken。三种结果为替代入口。

U 收到 Granted 须转发给关联参与者，并进入 permitted；收到 Deny 须转发并仍留在 not permitted and Floor Idle；收到 Taken 须转发并进入 not permitted and Floor Taken。三类消息均可请求 Floor Ack；是否处理 ACK 以及收不到 ACK 后如何处理是原文保留的实现选项。

强度：转发及对应状态动作为 SHALL；请求 ACK 为 MAY。

- 服务器 U permitted 是本接口的许可状态，不证明 ACK、RTP 或端到端交付已发生；请求 ACK 的 subtype 位只说明要求确认，不补原文未给的统一失败回退。
- 回到 Idle 的 §6.3.4.3.2 第一段限定非 Start-stop、没有客户端协商 queueing、且不存在 dual 状态机，却在该段内部同时列空队列与非空队列动作。不能删除 no queueing 守卫，或凭其非空队列动作声称已闭合普通协商排队后的推进。本页不提供释放→自动选队首→授予的完整算法。
- 服务器计时表 §11.1.3 和计数表 §11.2.3 不能代替具体状态入口。C7/C20 的表给上限、关联 timer 及达到上限后的行为；不由表头推断状态程序不存在 increment，也不展开本页外重传/撤销/释放。

依据：3gpp-ts-24.380-v16.9.0 §6.3.5.3.3;6.3.5.3.5–6;6.3.5.5.2；§8.2.2.1；§6.3.4.3.2 (queue boundary comparison)；§11.1.3;11.2.3 (timer/counter scope comparison)，印刷页 56,75,76,85,148,216,218,219,220,223,224。

## 边界

- §6.1 要求在媒体安全需要时执行 clause13；完整保护、配置、SIP建立与RFC编码不在本页。
- 本页保留初始化回指、Start-stop 排除、拒绝列表连接词及排队推进边界，不以其他版本补齐；不是完整服务器仲裁实现。

若要核对话权消息里的位置字段，区分 Type 0 与缺字段，或检查多话者的用户与位置列表如何配对，读[MCPTT 话权位置和多话者顺序](floor-talker-location.md)。
