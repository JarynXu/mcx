# 被叫参与功能：用户绑定、来电权限与服务模式

TS24.379 V19.4.0 §11.1.1.3.2；本页沿在网按需、带话权控制的私呼路径使用。本节原文也覆盖预建立会话，不能把后续按需客户端规则套到所有分支。

## 控制侧来电先检查角色标记

适用条件：收到terminating participating的INVITE。

资源不足或拥塞风险时可返回500，可附Retry-After；拒绝后停止。缺Contact中的isfocus标记须403+Warning104。紧急指示下可选择接受，不等于取消全部后续授权。

依据：§11.1.1.3.2 步骤1–2。

## 先识别转发分支，再判断用户与模式

适用条件：处理目标MCPTT ID。

即时转发、迁移转发以及无绑定时已启用的no-answer转发，是本节先处理的特殊分支。未被这些分支处理且找不到MCPTT ID与公共用户身份绑定，才按步骤7返回404。普通private缺已收到的Answer-Mode Indication，返回480+Warning146；不要从缺绑定直接推断所有情况都404。

依据：§11.1.1.3.2 步骤4–7a。

## 被叫是否可被此人呼叫另有检查

适用条件：用户发起的普通私呼，call-transfer-ind及call-forwarding-ind均缺失或false。

被叫配置不允许参与私呼时403+Warning127。对session-type=private，非空IncomingPrivateCallList不含主叫且没有名单外接听许可时，403+159并停止。主叫有拨打许可不替代被叫侧许可。

依据：§11.1.1.3.2 步骤8–9。

## 服务器模式选择与客户端选择不是同一条件表

适用条件：先前检查和可能的转发未终止本流程。

服务器按收到的Answer-Mode Auto/Manual，或缺该头时客户端上报的auto-answer/manual-answer，或相应Priv-Answer-Mode，进入对应自动/手动过程。该选择还要走后续客户端流程；不能用它覆盖客户端配置与意愿条件。

依据：§11.1.1.3.2 步骤12–13。

## 证据边界

- 转发只指出分支顺序，未展开最大次数、目标绑定、MESSAGE触发和失败处理全流程。
- 本页不包括功能别名来电名单及TNP1完整条件；不能声称所有授权已覆盖。
- 步骤10的拒绝对象写originating，与本节terminating标题不一致，未据此改写实现。

## 按需继续

- [originating-authorization](originating-authorization.md)
- [private-client-acceptance](private-client-acceptance.md)
- [commencement-selection](commencement-selection.md)
- [../identity/migration-authorization](../identity/migration-authorization.md)

[ETSI 官方 TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页448、449、450、451；仅本版本。
