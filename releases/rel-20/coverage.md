# Release 20 覆盖范围

已收录 TS 22.179 V20.0.0 的两处 MCPTT 通话需求（Stage 1），以及 TS 24.484 V20.1.0 的伙伴系统迁移配置流程与相关条款（Stage 3）。两者按各自范围阅读；未覆盖完整规范、其他规范或整个 Release，未据此验证实现。

## MCPTT 环境监听与 ad hoc 组呼转发

可区分另一呼叫打断环境监听时的结束、暂停后恢复与有条件并行；可查 ad hoc 组呼转发的配置权限、四类触发和发起者成功通知。

TS 22.179 V20.0.0 的 Stage 1 通话需求。环境监听看被监听用户实际发送或接收；转发超时或拒绝仅列手动开始模式。

未收录这些功能的 Stage 2、Stage 3 或实际设备表现，不确定 SIP 映射、媒体状态机或目标已入会；不代表完整 Rel-20 覆盖。

[环境监听遇到其他呼叫：结束、暂停后恢复或并行](topics/calls/ambient-listening-interruption.md) · [Ad hoc 组呼转发：授权、四种触发条件和成功通知](topics/calls/ad-hoc-group-call-forwarding.md)

## 伙伴系统迁移时的身份与用户配置

区分主系统给的接入配置档、伙伴侧订阅的配置档、IdMS 的 HTTPS 地址和 CMS 订阅代理的 SIP 标识；判断变更通知能证明哪一步。

TS 24.484 V20.1.0 的伙伴迁移在线配置；代理初始订阅、MCPTT 伙伴条目结构和 schema 只用于辨认对应分支。

不覆盖各业务迁移授权、伙伴认证的完整消息，未验证 TS 24.481 组文档取回、业务采用新配置或实际互通；没有裁定 MCPTT XML 层级差异在网络上的编码。

[迁入伙伴 MC 系统：接入时用哪份用户配置档，接入后又订阅哪份？](topics/identity/partner-migration-profile.md)
