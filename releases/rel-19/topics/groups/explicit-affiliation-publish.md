# 显式归属请求与刷新：PUBLISH表达客户端的组兴趣

在网 MCPTT；执行 TS24.379 V19.4.0 §9.2.1.2 的客户端显式 affiliation 建立或刷新。

目标用户在目标客户端仍对至少一个组感兴趣；不覆盖撤销/去归属。

状态确定过程应先启动，见配套状态观察主题；这里不把 PUBLISH 的事务成功当作已归属。

## 新兴趣与接近到期的刷新

适用条件：用户表达对一个或多个组的兴趣；或客户端从 §9.2.1.3 的 NOTIFY 得知某组为 affiliated 且其到期时间临近，用户仍对该组感兴趣。

客户端以 §9.2.1.2 的 SIP PUBLISH 过程表达新兴趣或续期兴趣。刷新依据该组通知的状态与到期时间，不是仅见 PUBLISH Expires 为最大值便不再刷新。

依据：§9.2.1.2 opening bullets 1 and 3。

## SIP目的地与业务目标不是同一个ID

适用条件：生成本范围内的 SIP PUBLISH。

Request-URI 为服务该用户的发起参与功能 PSI；application/vnd.3gpp.mcptt-info+xml 中 mcptt-request-uri 是目标 MCPTT 用户 ID，不是组 ID。P-Preferred-Service 携 MCPTT ICSI urn:urn-7:3gpp-service.ims.icsi.mcptt；至少仍对一组感兴趣时 Expires=4294967295。

依据：§9.2.1.2 steps 1–4。

## 发布完整兴趣组列表

适用条件：依 §9.2.1.2 构造 PUBLISH 的 per-user PIDF 正文。

正文包含目标用户在目标客户端感兴趣的全部组，而非只列新增/续期组；包含目标客户端 ID。每个 affiliation 元素不得带 status 或 expires 属性；presence/p-id 设置全局唯一值。

依据：§9.2.1.2 step 6(a–d)。

## 用户、客户端、组的编码层次

适用条件：解释上述 per-user affiliation PIDF；不是 per-group 通知。

presence/entity 标识 MCPTT 用户；每个客户端一个 tuple，tuple/id 标识客户端；其 status 子元素下每个感兴趣组一个 affiliation，group 属性为组 ID。需要同时保留用户、客户端和组的层次，不能仅按用户 ID 合并多个客户端归属。

依据：§9.3.1.2 per-user construction items 1–8。

## 归属刷新不强制照搬空正文

适用条件：刷新一个或多个组的 affiliation 到期时间，使用 §9.2.1.2。

该条注释明确说明刷新可能携带 application/pidf+xml 正文，借此一次刷新多个组，区别于直接照搬 RFC3903 的通用刷新做法；不能自行把所有此类刷新强制改成空正文。

依据：§9.2.1.2 final NOTE and send paragraph。

## 证据边界

- 本条未定义临近到期的固定提前秒数或周期，不自行设置统一刷新比例。
- 这是本条列明的业务字段，不是完整可发送请求模板；SIP 核心及 presence publication 仍依所引 TS24.229、RFC3903/3856。
- 用户表达兴趣不等于客户端自行宣告已 affiliated。全局唯一 p-id 用于相关通知关联，不在此定义 SIP ETag/If-Match 等发布事务机制。
- 外层 status 是 PIDF 元素；EP3 禁止的是 affiliation 的 status 属性，不是删除 PIDF 的 status 元素。这里给编码所表达的层次，不要求某种本地数据库表或持久化方案。
- 保留原文 possibly 的表述，不把注释独立升级成所有 SIP PUBLISH 刷新均必须带正文。此流程的请求字段仍按 EP2/EP3 和原条文构造。
- 已读 §§9.2.1.1–3 没有定义客户端针对 PUBLISH/SUBSCRIBE 各 4xx/5xx/6xx 的专属重试、回滚或统一业务失败码；不把服务器拒绝码编造成客户端新增动作。
- 客户端以 NOTIFY 的 per-user 信息确定成功/拒绝相关状态；具体服务器拒绝后如何筛选/更新/省略条目由服务器研究补齐，本稿没有把未出现的组一概定义为被拒。
- 不要求创建某种本地持久表，不把发出请求时的兴趣名单写成已获准 affiliation。消息所表达的用户/client/group及可用状态、到期、p-id各有不同含义；本稿只保留这些关联，不规定具体存储实现。
- 服务器存储中的 deaffiliated 状态不应直接扩充客户端 XML schema 的 statusType；本稿不研究撤销流程。
- TS24.229、RFC3903、RFC3856、RFC3863、RFC6665、RFC4661 的完整事务、认证、事件头、ETag/If-Match、订阅终止和重传实现。
- 显式归属服务器授权、并发N2限制、持久记录更新、跨服务器PUBLISH/NOTIFY以及拒绝通知构造。
- 撤销/去归属、取消订阅、强制和协商修改他人归属、基于位置/functional alias规则的触发。

## 按需继续

- [explicit-affiliation-observation](explicit-affiliation-observation.md)
- [prearranged-admission](prearranged-admission.md)
- [active-call-entry](active-call-entry.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页206、207、235；仅本版本。

- [减少兴趣组或全部退组](explicit-deaffiliation-request.md)
