# 显式归属结果：先订阅状态，再用NOTIFY关联请求

TS24.379 V19.4.0 客户端 §9.2.1.1/§9.2.1.3；为自身用户观察当前客户端显式 affiliation 的结果及变化。

这里只覆盖建立/续订状态观察、接收通知和请求关联，不覆盖取消订阅、去归属或对他人的控制授权。

## 先启动状态观察

适用条件：客户端需要得知 affiliation status change 的成功或拒绝结果。

必须在启动状态变更之前先启动 affiliation status determination 过程。不能只依 PUBLISH 已发送或事务答复就断言各组已归属。

依据：§9.2.1.1 final paragraph; 9.2.1.3 NOTE 1。

## 订阅当前状态及后续变化

适用条件：客户端初始请求获取归属状态。

生成初始 SUBSCRIBE，Request-URI 指向服务该用户的发起参与功能 PSI；mcptt-info+xml/mcptt-request-uri 为目标 MCPTT 用户 ID；P-Preferred-Service 为 MCPTT ICSI，并声明 Accept:application/pidf+xml。需要当前状态和后续通知时 Expires=4294967295；仅抓取当前状态时 Expires=0。

依据：§9.2.1.3 initial request steps 1–6。

## 按客户端筛选

适用条件：只请求该 MCPTT 用户在指定 MCPTT 客户端所归属的组。

SUBSCRIBE 必须带 application/simple-filter+xml 的 per-client 过滤，指明该客户端 ID。§9.3.2.2 将筛选目标定位为 presence 下 tuple 的 id，而不是 affiliation/group。

依据：§9.2.1.3 initial request step 7; 9.3.2.2 per-client restrictions。

## 订阅续期不等于归属续期

适用条件：已有该状态订阅，客户端要继续获取当前状态及后续通知。

使用同一 dialog 内的 SUBSCRIBE 续订，Expires=4294967295，并带 Accept:application/pidf+xml。这刷新的是状态观察订阅；组兴趣持续到期时仍调用 PUBLISH 的归属刷新过程。

依据：§9.2.1.3 re-subscribe paragraph and items 1,3; 9.2.1.2 opening refresh bullet。

## 从NOTIFY与p-id判断结果

适用条件：收到符合所引 SIP/presence 过程的 NOTIFY，且其 application/pidf+xml 是按 §9.3.1 构造的 per-user affiliation 信息。

客户端据正文判定用户在各客户端、各组的 affiliation 状态。NOTIFY 若含 presence/p-id，其值标识触发该通知的 PUBLISH；无 p-id 时，本条未给出替代的请求相关算法。

依据：§9.2.1.3 NOTIFY paragraph。

## 状态字段与到期时间的边界

适用条件：解析上述 per-user 状态通知或保留其业务上下文。

per-user PIDF 以用户→客户端→组组织；affiliation 的 status、expires 在通用语法中可选，expires 类型为 xs:dateTime。statusType 列出 affiliating、affiliated、deaffiliating，未列 failed/rejected。不能发明逐组失败枚举、把缺字段默认成 affiliated，或把绝对到期信息当作 SUBSCRIBE 的秒数。

依据：§9.3.1.2 per-user items 2–10; Table 9.3.1.2-1 affiliationType/statusType。

## 证据边界

- 原文要求先 initiate，没有要求等待 SUBSCRIBE 的200或首个NOTIFY之后才发送PUBLISH；不增加这个先后门槛。
- 初始 SUBSCRIBE 的 Expires=0 在此是一次状态获取，不是 PUBLISH 撤销，也不是本页未覆盖的取消既有订阅。
- 完整过滤 XML 与命名空间见原条款；不要误用 per-user 过滤中的 MCPTT 用户 ID 代替此处 client ID。
- 不把 SUBSCRIBE 续订或它的 Expires 与各个 affiliation/expires 合并成同一个计时器。
- 此条件不能简化为收到任意 NOTIFY 即接受其状态；也不能要求每个 NOTIFY 都必须含 p-id。
- §9.2.1 没有提供缺失 status/expires、通知中未列组、失败重试或本地持久记录的完整处理算法；须与服务器通知构造和所引 RFC 合并核对，不能自行定义。
- 已读 §§9.2.1.1–3 没有定义客户端针对 PUBLISH/SUBSCRIBE 各 4xx/5xx/6xx 的专属重试、回滚或统一业务失败码；不把服务器拒绝码编造成客户端新增动作。
- 客户端以 NOTIFY 的 per-user 信息确定成功/拒绝相关状态；服务器记录清理与通知构造的已核分支见[服务器记录与通知](explicit-affiliation-server-state.md)；这些分支不提供所有拒绝或条目省略的唯一原因映射，不能把未出现的组一概定义为被拒。
- 不要求创建某种本地持久表，不把发出请求时的兴趣名单写成已获准 affiliation。消息所表达的用户/client/group及可用状态、到期、p-id各有不同含义；本页只保留这些关联，不规定具体存储实现。
- 服务器存储中的 deaffiliated 状态不应直接扩充客户端 XML schema 的 statusType；本页不展开撤销流程。
- TS24.229、RFC3903、RFC3856、RFC3863、RFC6665、RFC4661 的完整事务、认证、事件头、ETag/If-Match、订阅终止和重传实现。
- 显式归属服务器授权、并发N2限制、持久记录更新、跨服务器PUBLISH/NOTIFY以及拒绝通知构造。
- 撤销/去归属、取消订阅、强制和协商修改他人归属、基于位置/functional alias规则的触发。

## 按需继续

- [explicit-affiliation-publish](explicit-affiliation-publish.md)
- [prearranged-admission](prearranged-admission.md)
- [active-call-entry](active-call-entry.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页206、207、208、235、236、237、238；仅本版本。

- [退组状态及通知省略的边界](explicit-deaffiliation-state.md)
