# 显式退组的服务器状态、失败清理与多客户端疑点

在网显式撤销；区分服务用户的server与拥有组的server，两个角色的记录维度和PUBLISH正文不同。

不覆盖隐式取消§9.2.2.2.14/§9.2.2.3.11。

服务用户侧以user→client→group存储；拥有组侧以group→user→client存储且到期时间属于user记录。

处理已接受PUBLISH的记录更新以相应输入匹配、前置授权/Expires检查及PIDF identity一致性检查通过为前提；PUBLISH200本身不足以证明更新已执行。失败响应或Timer F超时的本地清理不继承对端成功检查条件，对端因授权、Expires等拒绝仍触发该清理。

服务用户侧输入：PUBLISH目的为服务目标用户的O-PF或T-PF PSI，mcptt-request-uri为该server服务的目标MCPTT ID，P-Asserted-Service为MCPTT ICSI、Event=presence、PIDF为per-user。发起者非目标用户时须有修改权限；Expires及presence.entity检查通过后才处理记录。

组所属端输入：PUBLISH目的为本组控制功能PSI，mcptt-request-uri为组ID、mcptt-calling-user-id为handled user，P-Asserted-Service为MCPTT ICSI、Event=presence、PIDF为per-group；组存在且用户为成员，Expires检查及PIDF entity/tuple.id一致性检查通过。

以下PUBLISH记录处理按各自角色继承相应输入条件；NOTIFY处理则按所在条目的订阅和通知条件。

## 删除兴趣组先进入撤销中

适用条件：服务用户侧已按目标user/client取得原served list并建立candidate list，candidate interval非零，且某原组记录未过期，却未出现在新PIDF group属性集合内。

拷贝此记录到candidate；若原状态affiliated或affiliating，将新状态改为de-affiliating，expiry=当前时间+2×Timer F。不是立即删除记录。非零列表仍受跨该用户client的N2去重计数与provider policy裁减过程约束。

依据：§9.2.2.2.3 step14a(ii),14b–c。

## 全部退出的候选记录

适用条件：服务用户侧已按目标user/client取得原served list并建立candidate list，candidate interval=0。

对该client原served list中每一个组记录拷贝至candidate，并置de-affiliating、expiry=当前时间+2×Timer F。此step15未加原状态或未过期筛选，不能套用step14的筛选。

依据：§9.2.2.2.3 step15。

## 不是所有撤销中记录都触发同一上行发布

适用条件：完成candidate替换，且某组旧记录为affiliated且未过期，新candidate为de-affiliating。

为served user与该组执行§9.2.2.2.6；不能扩写为任何de-affiliating记录都无条件发送。另识别来件p-id并调用§9.2.2.2.5通知用户状态订阅者。

依据：§9.2.2.2.3 steps17d–19。

## 失败清理跨该用户的所有客户端

适用条件：§9.2.2.2.6发出的该用户/该组(de)affiliation PUBLISH Timer F到期，或收到3xx/4xx/5xx/6xx。

删除served user所有client之下该handled group的组记录；条文没有只删发起client、只删de-affiliating或回滚旧状态的限制。此为本地失败清理，不能作为组所属端成功撤销证据。

依据：§9.2.2.2.6 final paragraph。

## 组端功能别名可禁止撤销

适用条件：组端PUBLISH以组ID及handled user ID为目标，选定expiry=0，且组配置forbidden-deaffiliation-FAs匹配handled user已激活FA；或forbidden-deaffiliation-if-last-FAs匹配已激活FA且该user是将此FA绑定到本组的最后用户。

step10a0规定403并停止。注意同节step6已规定先发200，形成响应顺序冲突；不可在知识库偷偷改为确定单一事务流程。

依据：§9.2.2.3.3 steps6,10a0。

## 零到期分支删除用户记录的范围

适用条件：owner前置检查通过；PIDF entity匹配组ID，tuple.id匹配handled user；选定expiry=0且未命中禁止撤销FA条件。

step10a删除组内相应用户信息项（其下包含client列表），不是只删除一个client。原文删除匹配使用served MCPTT ID，但前文定义handled MCPTT ID；保留术语疑点，需核勘误，不能装作变量完全闭合。后续step12识别p-id、step13通知组状态订阅者。

依据：§9.2.2.3.3 steps7–10,12–13。

## 从组端通知确认不再归属

适用条件：§9.2.2.2.7收到组所属服务器NOTIFY，已处理其确定的handled group，且本地该user/client/group记录为affiliated或deaffiliating，尚未过期；NOTIFY PIDF中没有同时匹配该user tuple.id和该client affiliation.client的条目。

置deaffiliated，expiry=当前时间。该分支不要求p-id匹配；另一个affiliating失败分支才有p-id条件，不能混合。

依据：§9.2.2.2.7 step2。

## 通知省略的记录不等于失败枚举

适用条件：§9.2.2.2.5向已存在的用户状态订阅发送NOTIFY。

不输出已过期或deaffiliated组记录；按请求中的per-client filter裁剪。若由§9.2.2.2.3调用且已识别handled p-id，NOTIFY携该p-id。该规则与仍可能输出deaffiliating状态不同。

依据：§9.2.2.2.5。

## 证据边界

- §9.2.2.3.3先200后禁止FA时403的顺序冲突。
- §9.2.2.3.3 step10a使用served MCPTT ID而该处理路径此前识别handled MCPTT ID。
- 一个client撤销但其他client仍保留同组时，§9.2.2.2.6撤销Expires0与正文仍包含其他client，组端零expiry删除用户整体记录之间有张力；不可声称跨client撤销安全已闭合。
- 本次未核RFC3903完整ETag/条件发布/重试、24.229传输认证、GMS与FA配置取得过程。
- 本次未从第9章得出进行中呼叫退出时序；不要把未见BYE当作必须保持通话的肯定命题。
- 同一用户多个客户端的退组组合未由本版这些段落闭合；不能据此给出保证不影响其他客户端的确定算法。
- 删除本地记录不是对端撤销成功或已退出进行中呼叫的证据。

## 按需继续

- [explicit-deaffiliation-request](explicit-deaffiliation-request.md)
- [explicit-affiliation-observation](explicit-affiliation-observation.md)
- [prearranged-admission](prearranged-admission.md)
- [../calls/group-release-timers](../calls/group-release-timers.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页211、212、213、214、215、217、219、228、229、230；仅本版本。
