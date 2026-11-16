# SIP 对话内请求：标识、目标与路由集

适用：RFC3261 baseline dialog rules; not a complete MCX SIP profile。

对话在 UA 侧由 Call-ID、本地 tag、远端 tag 共同标识（§12）。Call-ID 单独不足以作为完整对话键。

对话内请求使用已保存的 remote target 和 route set（§12.2.1.1）：
- 路由集为空：Request-URI 用远端目标，不加 Route。
- 首项带 `lr`：Request-URI 仍用远端目标，Route 按原顺序放完整路由集。
- 首项不带 `lr`：首项成为 Request-URI，移除那里不允许的参数；Route 放剩余路由，最后附远端目标。

目标刷新能更新远端目标，不能改变路由集；普通非目标刷新请求不改变远端目标，ACK 也不是目标刷新（§12.2）。

因此，分布式实现不能只讨论注册绑定：处理对话内请求还需要正确的对话状态。这是状态职责的推论，不是要求固定某个进程，也没有验证任何复制或故障转移算法。

## 来源与边界

Baseline RFC3261 only; extension updates, MCX profile, transaction matching, transport reuse and failover not fully checked.

RFC has no 3GPP Release; placement under Rel19 is navigational, not a new Rel19 rule.

[精确条款与结构化条件](dialog-routing.json)，[来源目录](../../sources.json)。

- [注册器定位](registrar-routing.md)
- [主系统认证注册](../identity/primary-registration.md)
