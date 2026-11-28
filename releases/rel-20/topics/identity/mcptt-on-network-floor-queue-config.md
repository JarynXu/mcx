# MCPTT 在网话权队列：容量、等待时长和校验

**队列能放多少，和一笔请求最多能等多久，是两个配置。**两项都在 MCPTT 在网业务配置的 `<on-network>/<floor-control-queue>` 下。

依据：3GPP TS 24.484 V20.1.0（Release 20，Stage 3）§8.4.2.1/.3/.6/.7。

| 字段 | §8.4.2.7 在网定义 | Schema 类型 |
| --- | --- | --- |
| `depth` | 话权队列容量上限（项 10），不是当前队列位置或实际有多少请求。 | `xs:unsignedShort` |
| `max-user-request-time` | 一笔用户话权请求在队列里的最长时间（项 11），不是拿到话权后可发话的时长。 | `xs:duration` |

### 先辨认报错对应哪个字段

- **`depth` 的值语义无效。**§8.4.2.6 要求配置管理服务器返回 HTTP 409（Conflict），包含 XCAP `<constraint-failure>`；若带 `phrase`，建议用 `semantic error`。这段还列了其他字段，所以只见这句诊断不能确认出错的是 `depth`。它没给队列深度的业务合法区间；相邻的“大于 255”规则说的是 `min-length-alias`，不能移给队列深度。符合 XML 类型也不证明语义有效。
- **`max-user-request-time` 的时长格式或秒值有问题。**它是 §8.4.2.6 具名时长清单第 7 项；`depth` 不在这份清单。格式不符和秒值无效要分开，按[具名时长的两个校验分支](ad-hoc-broadcast-hang-time.md#缺项和校验怎么判)核，在这一项不套深度的 `semantic error`。

### 缺字段和示例值别混读

§8.4.2.1 在网项 6 说可以包含该队列块，并列出这两个子字段。§8.4.2.3 的 Schema 对队列块、`depth` 与 `max-user-request-time` 分别声明 `minOccurs="0"`，均无声明默认值。这个声明不证明某份缺项或空块配置会被服务接收，也不证明排队已关闭。附录 A 表 A.2.3-12 的 HTTP 响应示例填了 `4` 和 `PT30S`，不是缺项时的默认值。

要查一笔请求是获准、拒绝还是排队、由谁移出，或所选组模式是否支持排队，走 [Stage 1 普通在网话权申请](../calls/ordinary-floor-request-outcomes.md)。同属 Release 20 的 TS 22.179 V20.0.0 §6.2.3.2 分别规定队列深度可配置、移除机制和管理员配置组队列定时器；不要从本页两个 XML 字段推一次申请的实际结果、计时起点或退出动作。也不把本页在网字段照搬到离网。

[3GPP 原文归档](https://www.3gpp.org/ftp/Specs/archive/24_series/24.484/24484-k10.zip) · [来源与版本](../../sources.json) · [结构化记录](mcptt-on-network-floor-queue-config.json)
