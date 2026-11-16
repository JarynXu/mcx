# MCData 归属失败与结果回到客户端：清理范围及期限边界

限同版普通显式归属的 serving 与组 owner 路径；失败指 §8.3.2.6 明列的 owner PUBLISH 事务结果，不替代其他业务的错误处理。

serving→owner 的 per-group 通知与 serving→client 的 per-user 通知是两段；客户端已按既有 §8.2.3 建立相关订阅时，才按该订阅判断后续可见结果。

## 失败清理的跨客户端范围

适用条件：为 served 用户向 handled 组发送的归属或撤销 PUBLISH，其 timer F 到期，或收到 3xx、4xx、5xx、6xx 响应。

§8.3.2.6 要求删除该 served 用户各客户端记录下、组 ID 等于 handled 组的每个组条目。原文没有把清理限制为本次发起变更的单一客户端，也没有只删 affiliating 或本次新建条目的条件。这是该段明确的本地清理，不是恢复请求前列表快照；也不能据此声称 owner 已撤销关联或实际业务会话已经释放。

- 3xx 在该失败处理集合内，不为这一过程补自动重定向/重试。
- timer F 数值依赖 SIP 规范，未核；本条不把临时网络失败改写成永久禁止归属。
- 删除范围限同一 served 用户和 handled 组，不扩展到其他用户、其他组或 owner 的全部记录。
- 原文该失败段只列删除动作，没有直接规定向客户端补发第二个 PUBLISH 响应或恢复旧列表。

依据：§8.3.2.6 failure paragraph，印刷页 169、170。

## 重建客户端可见结果

适用条件：serving 的 owner 通知处理或失败清理改变了其本地记录，客户端对相关用户的状态观察订阅有效。

§8.3.2.4 要求 serving 在订阅期间通知用户信息变化，§8.3.2.5 则按本地用户→客户端记录重建 per-user PIDF，省略过期和 deaffiliated 条目并应用客户端过滤。owner 的 per-group NOTIFY 不是原样转交客户端的成功回执。只有 §8.3.2.5 明列的“由客户端 PUBLISH 接收过程调用且已识别 handled p-id”条件才要求回填该关联值；不能把任意 owner 状态更新都说成会携原客户端 p-id。期限在各层也有不同作用：owner 保存用户级期限，serving 保存客户端下的组期限；收到 owner 正向通知时明确更新的是状态及 next publishing time，而不是自动同步全部期限字段。

- §8.3.2.7 的状态分支和 §8.3.2.6 的失败段没有逐段再写一次调用 §8.3.2.5；本条依据订阅期间通知变化的总义务说明回流，不补精确调度、重发或到达保证。
- 已过期数据不进入该 per-user 通知，不等于本批已经核到两端所有期限到期时的主动删除/撤销定时器。
- 设置 next publishing time 和 §8.3.2.6 的近到期刷新入口不构成完整定时实现；本批未核每轮刷新如何更新时间及失败后的自动恢复。
- 客户端的列表缺席依然要结合过滤、期限及请求关联判断；不能把这种结果表示当成完整拒绝原因字典。实际 SDS session 邀请、媒体和 BYE 仍需分别核验。

依据：§8.3.2.2;8.3.2.4 final paragraph;8.3.2.5;8.3.2.7 NOTIFY step1;8.3.3.2，印刷页 163、167、168、171、179。

## 证据边界

- 本批核实清理和通知职责，不补运行实现的重试、定时调度或跨层补偿；源文变量和关联差异仍需保留。

## 按需继续

- [explicit-affiliation-observation](explicit-affiliation-observation.md)
- [sds-session-responses-and-participants](sds-session-responses-and-participants.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§8.3.3.3 step10 versus steps2,11：零selected expiration分支删除MCData ID等于served MCData ID的用户记录，前面识别和非零处理使用handled MCData ID。 不把变量静默统一，不将零值分支表述为已验证的精确删除目标。

§8.3.2.3 step14;8.3.2.6 steps7,9,10;8.3.2.7 NOTIFY step3：客户端接入已可能设置affiliating p-id，owner跳新建current p-id时仅在字段未设才写本地值，缺席确认却要求相等。 单独标出跨跳关联缺口，不自造覆盖或映射算法。

§8.3.2.6 steps4,5,10;8.3.3.3 steps10,11：owner请求按该用户所有有效客户端聚合，撤销却使用Expires0；零值owner处理是用户记录级删除，且有served/handled变量差异。 不推断多客户端部分撤销一定只影响单个客户端，也不补按剩余客户端数切换请求类型的策略。

§8.3.2.7 NOTIFY step1：正向确认设置affiliated及next publishing time，未明确用收到的expires覆盖本地expiration time；已affiliated的刷新通知也不满足该分支初态。 保留实际赋值范围，不补完整每轮续期状态机。

§8.2.2 NOTE1;8.3.2.3 opening5,steps9,10,18：客户端零期限可省PIDF与serving入口仍必需PIDF的差异由上一批保留。 本批从已满足相应入口的服务器过程起算，不绕过该限制或宣称端到端零body撤销已闭合。

§8.3.2.3 steps14a(ii),15;8.3.2.7;8.4.1.2 table8.4.1.2-1：部分serving生成分支写de-affiliating，通知处理和schema写deaffiliating。 不新增wire状态，不静默修成经过实现验证的一致状态机。
