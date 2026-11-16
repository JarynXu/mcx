# Release 19

## 按问题查找

- [位置报告与组目标](topics/location/reporting.md)：订阅取消、当前组归属、测量时间与 UE label 方向。
- [位置触发覆盖与恢复](topics/location/trigger-override.md)：哪些触发可被覆盖，覆盖期间的新请求及取消后的恢复。
- [Rx 临时拒绝与重试间隔](topics/network-policy/rx-retry.md)：Retry-Interval 的等待义务和永久失败边界。

- [组文档寻址与成员表权限](topics/groups/document-access.md)：寻址与授权的区别，成员读取全表的条件。

- [创建组文档：403 与 409](topics/groups/creation.md)：创建地址、拒绝原因和建议组 ID 的重试条件。

- [跨服务商组文档转发](topics/groups/forwarding.md)：路由映射、身份头和 Authorization 处理。

- [LMR 互通：IWF 的规范边界](topics/interworking/scope.md)：业务范围、接口模型和用户身份。

Agent 可使用[轻量主题索引](topics.json)定位问题，需要结构化条件时再读取该主题旁的 JSON，不必加载其他主题。

## 证据与覆盖

[来源清单](sources.json)固定所用标准版本和条款。[覆盖与核验状态](status.json)列明当前范围。

以上内容是限定范围的规范解释。组文档主题及 LMR 互通范围页已对照所列原文条款核对；其他主题仍为整理说明。任何单页核对均不代表整个 Release 或可直接运行的协议实现。位置配置取消条件的字段集合尚待核清，本目录不提供该行为的确定规则。
