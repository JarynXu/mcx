# 话权仲裁：组归属与私呼主控

ETSI正式发布的TS23.283 V19.5.0，Release19，Stage2。

## 互通组话权控制

组归属MCPTT系统时由其服务器主控；组归属LMR系统时由IWF代表主控。MCPTT组的主系统由配置定义并通过组ID识别，不能按当前发言者所在地更换主控。 [§10.5.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 互通私呼采用话权控制

IWF或MCPTT服务器中的一方负责双方请求仲裁，非主控方必须不加过滤地转交其用户的全部话权请求。主控可按发起侧或其他方式分配；手动建立示例中的发起侧责任不能扩张为所有场景的唯一分配规则。 [§10.5.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 已建立的私呼里谁裁决话权

**先看这通私呼实际由谁主控，再看谁发了请求和谁得到结果。** TS 23.283 V19.5.0 的两个 Stage 2 示例都从 MCPTT client 1 与 LMR 用户**已建立、启用话权控制**的同一通互通私呼开始。§10.5.3 允许按发起侧或其他方式分配主控，非主控方须转交自己用户的全部话权请求，不做本地过滤。不能从谁起呼、谁正在讲话、图里谁有一条箭头，推断谁仲裁。这里不借组呼过滤或自动／手动建呼来判主控，不适用于未启用话权控制的私呼。查规范不需要抓包。

### LMR 系统经 IWF 控制：本例拒绝 MCPTT 用户打断

1. **MCPTT 客户端起初持有话权。** 说完后发 Floor release（1），MCPTT server 向 IWF 转交（2）；IWF 向 server 指示 Idle（3），server 通知客户端（4）。这是交还话权，不是通话结束。
2. **后来换成 LMR 用户占用。** IWF → server 发 Taken（5），server → MCPTT 客户端转告（6）。这是告知话权由别的用户持有，不是本端获准发送；实际语音要另核。
3. **MCPTT 用户尝试打断。** 客户端带相应优先级向 server 发 Request（9），server 转 IWF（10）；IWF → server 返回拒绝（11），server → 客户端通知拒绝（12）。引言说由 IWF 拒绝，步骤 11 则具体写 **LMR 系统拒绝，IWF 通知 server**。别因 IWF 或 server 发出拒绝就把它认作那个裁决方；本例不规定拒绝原因，也不是 MCPTT 用户一定打断失败。

语音步骤 7 的编号有图文差异：**图**把 7a 画成 IWF → MCPTT server、7b 画成 server → 客户端；**正文**把 7a 写成 LMR 用户 → IWF，继而通向客户端的部分记作 7b。保留这两种写法，不把它们拼成同一组逐跳编号或报文证明。[§10.5.9、图 10.5.9-1，印刷页 115–116](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=116)。

### MCPTT server 控制：本例允许 LMR 用户打断

1. **起初话权空闲。** 客户端向 server 发 Request（1）。server 给客户端 Granted（2），另向 IWF 发 Taken（3），告知话权给了 MCPTT 客户端。**NOTE 1：3 可在 2 之前或之后。** 图示语音由客户端 → server（4a）→ IWF（4b）；向 IWF 发占用通知不证明客户端已收授予或已发语音。
2. **LMR 用户要打断正在讲话的 MCPTT 用户。** IWF 得知（5），带本例足以打断的优先级向 server 转请求（6）。是 **MCPTT server** 按优先级和配置准许（7），不是 IWF 自行授予，也不从一个高优先级值推所有同类请求都成功。
3. **撤销旧许可和授予新许可是两条腿。** server → MCPTT 客户端发 Revoked（8），向 IWF 发 Granted，让 LMR 用户获得话权（9）。**NOTE 2：9 可在 8 之前或之后。** 不能把收到原持有者对 8 的确认设为发 9 的必经条件，也不能从“有一条先发”推对端已收。图文的 10a/10b 是另一条证据：LMR 语音经 IWF → server → MCPTT 客户端。这两个注各限自己的一对通知，不放开其他步骤的因果，也未规定双方实收的先后。

[§10.5.10、图 10.5.10-1 和 NOTE 1/2，印刷页 116–117](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=117)。

**查现场先对上这一次私呼、请求、对象和方向。** Grant 是对请求的许可，Taken 通知接收方话权给了别人；仅见请求被转交、通知被发出或一个同名回包，不等于另一端收到、话权已生效在另一端、旧媒体已停或新媒体到达。核信令实收不要求有媒体证据；核实际传输或收音再看媒体。话权 Release、Revoked 与[整通私呼释放](private-release.md)是不同操作。问[话权消息含义](floor-signals.md)、[自动私呼建立](private-automatic.md)、[手动私呼建立](private-manual.md)或[组呼过滤](floor-filtering.md)，按各自场景读。本段没有给优先级门槛、超时、重试或 SIP/RTCP 映射。[§§10.5.2.2–.4、.8–.11、10.5.3，印刷页 103–108](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf#page=109)。

## 边界

§10.5.3 只到主控及转交职责；§10.5.9/.10 只核两条私呼示例。不规定主控选举、故障迁移、部署拓扑、完整话权状态机或媒体实现。

[private-manual](private-manual.md) · [floor-filtering](floor-filtering.md) · [floor-signals](floor-signals.md) · [结构化条件](floor-control-owner.json)
