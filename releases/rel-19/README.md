# Release 19

## 按问题查找

- [位置报告与组目标](topics/location/reporting.md)：订阅取消、当前组归属、测量时间与 UE label 方向。
- [位置触发覆盖与恢复](topics/location/trigger-override.md)：哪些触发可被覆盖，覆盖期间的新请求及取消后的恢复。
- [Rx 临时拒绝与重试间隔](topics/network-policy/rx-retry.md)：Retry-Interval 的等待义务和永久失败边界。

Agent 可使用[轻量主题索引](topics.json)定位问题，需要结构化条件时再读取该主题旁的 JSON，不必加载其他主题。

## 证据与覆盖

[来源清单](sources.json)固定所用标准版本和条款。[覆盖与核验状态](status.json)列明当前范围。

以上内容是限定范围的规范解释，尚未独立复核指定版本原文，也不代表整个 Release 或可直接运行的协议实现。位置配置取消条件的字段集合尚待核清，本目录不提供该行为的确定规则。
