# 创建组文档：403 与 409

适用：Release 19，TS 24.481 V19.3.0 的 GMC/GMS 建组流程。

客户端以 HTTP PUT 提交组 XML；Request-URI 为 users tree 中的 XCAP URI，XUI 使用配置的 group creation XUI（§6.3.2.2.1，p15）。

GMS 先确定发送者身份，再校验创建权限；无权限返回 403 并停止。XML 的 group/list-service/@uri 不符合本地策略时，返回含 uniqueness-failure 和至少一个可接受 alt-value 的 409，并停止（§6.3.2.3，p16）。

GMC 收到上述带建议值的 409，可选用建议组 ID 再申请（不是替换寻址 XUI）；不是任意 409 都适用，也不是必须重试或已创建成功（§6.3.2.2.2，p15）。

这里仅覆盖建组的权限及标识冲突分支，不替代 XML schema、认证或 RFC 4825 全流程。[条款来源](../../sources.json)；[结构化条件](creation.json)；[读取权限](document-access.md)。
