# 私呼自动或手动应答由哪些条件选择

仅 TS24.379 V19.4.0 带话权控制的在网按需私呼被叫的 §11.1.1.2.1.2 步骤9–10。客户端已走过前面的拒绝和安全检查；本页不授予主叫强制接听权限。

## 进入自动过程的三种条件

适用条件：按本节选择应答模式。

Answer-Mode=Auto且被叫设置为自动；或Answer-Mode=Auto、被叫设置手动但愿意自动应答；或收到Priv-Answer-Mode=Auto。满足任一时执行自动过程。不能将普通Auto请求直接等同Priv-Answer-Mode。

依据：§11.1.1.2.1.2 步骤9。

## 手动选择同样有配置与意愿条件

适用条件：按本节选择应答模式。

Answer-Mode=Manual且被叫设置为手动；或Answer-Mode=Manual、被叫设置自动但允许手动应答；或收到Priv-Answer-Mode=Manual。满足任一时执行手动过程。

依据：§11.1.1.2.1.2 步骤10。

## 选模式后仍要执行响应和媒体步骤

适用条件：进入选定应答过程。

自动过程生成200，包含Require:timer、Session-Expires且refresher=uas、MCPTT能力标记和适用SDP；再与媒体层交互。手动过程另有拒绝/转发和180振铃，最终200依同一构造规则。模式选择不是媒体连通证明。

依据：§6.2.3.1.1; 6.2.3.2.1。

## 证据边界

- 本节假定模式头与session-type已正确对应；没有完整定义头缺失、相互冲突或未列组合的通用回退，不能自造默认值。
- RFC5373及服务器强制模式授权尚未完整核查；不得把被叫的模式执行规则当作任意主叫的权限。
- Replaces、转接及媒体层完整处理仍依其规范，本页不列全。

## 按需继续

- [private-client-acceptance](private-client-acceptance.md)
- [../security/private-key-distribution](../security/private-key-distribution.md)

[ETSI 官方 TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页71、72、424；仅本版本。
