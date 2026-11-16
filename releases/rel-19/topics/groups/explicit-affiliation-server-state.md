# 显式归属服务器记录：两侧建立、刷新与通知确认

TS24.379 V19.4.0；Stage3。

在网显式归属服务器记录链，建立与正期限刷新为主。

各条另列触发消息及前置条件；通知与发布失败清理是明确标出的通用过程，也可被撤销主题引用，但不展开撤销特有状态转移。

user_publish：§9.2.2.2.3入口：PUBLISH指向服务该用户的O-PF或T-PF PSI；mcptt-info+xml的mcptt-request-uri标识本服务器服务的用户；P-Asserted-Service为MCPTT ICSI；Event=presence；PIDF为per-user affiliation。

group_publish：§9.2.2.3.3入口：PUBLISH指向组CF PSI；mcptt-info+xml有mcptt-request-uri及mcptt-calling-user-id；P-Asserted-Service为MCPTT ICSI；Event=presence；PIDF为per-group affiliation。

user_subscription：§9.2.2.2.4入口：SUBSCRIBE指向服务该用户的O-PF或T-PF PSI；mcptt-info+xml的mcptt-request-uri标识本服务器服务的用户；P-Asserted-Service为MCPTT ICSI；Event=presence。

group_subscription：§9.2.2.3.4入口：SUBSCRIBE指向组CF PSI；mcptt-info+xml有mcptt-request-uri及mcptt-calling-user-id；P-Asserted-Service为MCPTT ICSI；Event=presence；simple-filter+xml按用户过滤且指定ID与mcptt-calling-user-id一致。

## 参与侧记录层次

适用条件：服务器维护§9.2.2.2.2记录。

层次是user→client→group；组记录保存状态、到期时间、affiliating p-id及next publishing time。不能把同用户另一client的记录当成本client的记录。

依据：§9.2.2.2.2。

## 控制侧记录层次

适用条件：服务器维护§9.2.2.3.2记录。

层次是group→user→client列表；到期时间在该组的user entry，不是每个client单独保存期限。不要与参与侧user→client→group的逐组期限互换。

依据：§9.2.2.3.2。

## 新增与保留记录

适用条件：收到符合user_publish入口的请求；修改权限及Expires门槛均通过，PIDF entity匹配served用户；candidate间隔非零；tuple id定位served client；只讨论正文列出的组，不讨论遗漏组的撤销。

tuple id定位client。列出的组若无记录或旧记录已过期，候选表新增affiliating记录，到期=当前时间+candidate间隔，保存请求p-id。列出的既有未过期affiliating/affiliated记录复制并延长该组记录期限；该分支不把已有affiliated状态改回affiliating。

依据：§9.2.2.2.3 steps 10–14(a)(i),(iii)。

## N2与逐client替换

适用条件：收到符合user_publish入口的请求；修改权限、Expires与PIDF entity门槛通过；tuple id已定位served client；正期限候选表按§9.2.2.2.3 step14(a)构造。

N2按同一用户当前候选表与其他client记录中的不同组ID合计，只计未过期的affiliating/affiliated组；超限由服务提供方策略减至N2，不保证保留请求中的每一组。随后以候选表替换该client组列表。新建、已过期后重建或重新进入affiliating的指定分支触发向组侧发布；普通保留刷新不在step17(a–c)中。

依据：§9.2.2.2.3 steps 14(b–c), 16–17(a–c)。

## 向组侧发布和刷新

适用条件：按§9.2.2.2.6向某组发起affiliation，或先前发布信息临近到期而续发。

PUBLISH目标为组CF PSI；消息标明目标组及served用户，Expires=4294967295；每次设新的全局唯一p-id。per-group PIDF列出该用户对该组处于未过期affiliating/affiliated的合格client，正文不带affiliation/@expires。本版本不支持一条此类PUBLISH合并多个用户。

依据：§9.2.2.2.6 Note 1 and steps 1–10。

## 控制侧列表与有效期

适用条件：收到符合group_publish入口的请求；Expires、GMS组存在及成员门槛通过，PIDF entity等于served组且tuple id等于handled用户；selected期限非零；已定位served group entry。

定位handled用户的user entry，不存在才新增；根据收到的affiliation/@client设置该用户的client ID列表，并按selected期限设置该user entry到期时间。文本是设置列表，不是只追加本次client。随后识别p-id并调用组侧通知过程。

依据：§9.2.2.3.3 steps 9, 11–13。

## 发布失败清理

适用条件：§9.2.2.2.6发出的该served用户/handled组的(de)affiliation PUBLISH发生timer F超时，或收到3xx/4xx/5xx/6xx。

移除served用户各client下该handled组的记录；文本没有仅删本次新client或仅删affiliating状态的限制。此通用发布失败清理也适用于撤销请求，但不是控制侧成功建立或撤销的证据。

依据：§9.2.2.2.6 final paragraph and step 1。

## 订阅控制侧状态

适用条件：参与侧要确认served用户在handled组的控制侧归属结果。

另按§9.2.2.2.7向组侧订阅，simple-filter按该用户限制；要当前及后续状态则Expires=4294967295，只取当前状态则初始SUBSCRIBE Expires=0。不能把零期限的一次状态读取说成不产生通知，或把PUBLISH 200直接替代NOTIFY结果。

依据：§9.2.2.2.7 initial SUBSCRIBE steps 1–7。

## NOTIFY确认与半寿命发布时间

适用条件：参与侧正在按§9.2.2.2.7确定handled组的归属状态；收到该条规定的SIP NOTIFY及符合§9.3.1的per-group PIDF，且PIDF tuple.id匹配served用户，affiliation/@client匹配served client，affiliation/@expires存在并给出归属期限，且本地user→client→group均匹配该用户、该client及handled组，且group记录仍为affiliating、其本地expiration time尚未到达。

将该记录改为affiliated，并将next publishing time设置在当前时刻与通知中归属到期时刻之间的中点。该正向转换不要求p-id匹配，但不适用于每次已为affiliated的通知；这里也未写用通知expires覆盖本地group记录expiration time。

依据：§9.2.2.2.7 NOTIFY handling step 1。

## 向用户通知状态

适用条件：用户状态订阅已按§9.2.2.2.4建立并仍有效；§9.2.2.2.5为该served用户生成通知。

按user→client→group记录生成per-user PIDF；排除过期及deaffiliated组，若订阅含per-client过滤则应用该过滤；由§9.2.2.2.3调用且已识别p-id时回带该p-id。通知可以反映仍未确认的状态，不能据收到NOTIFY即断言每个目标组都已affiliated。

依据：§9.2.2.2.5;9.2.2.2.3 steps18–19。

## 组侧通知内容

适用条件：组侧状态订阅已按§9.2.2.3.4及其group_subscription入口建立；按§9.2.2.3.5为served组中的handled用户生成通知。

使用served组下handled用户记录生成per-group PIDF，包含affiliation/@expires；若由§9.2.2.3.3触发且已识别p-id，通知回带该p-id。其对象仍是该组中的该用户及其client，不是入会、接听或话权授予结果。

依据：§9.2.2.3.5; 9.3.1.2 per-group affiliation syntax。

## 紧急及重组附加通知

适用条件：正期限建立/刷新处理已到§9.2.2.3.3 steps14–15。

若目标组存在未结束的emergency alert，调用§12.1.3.4；若目标组已被重组，调用§16.2.4.3通知该状态。这两项不是所有归属成功都必然发送的通知。

依据：§9.2.2.3.3 steps 14–15。

## 证据边界

- 未自行选择删减算法、N2缺省值，亦未把本次请求写成逐组追加API。
- 该请求值不是永久归属保证；实际选定期限依赖RFC3903及返回结果。
- 跨域网关寻址仅为该条注释中的可选路由，发现算法未规定，本页不扩成跨域完整链。
- 本过程不明确给出group entry缺失时的创建/错误分支；不借用隐式资格检查§9.2.2.3.8的额外判断改写本条。
- 本次只核调用条件，未验收两个被调用过程。
- 不代替完整RFC3903、SIP事务及业务入呼实现；归属结果不代表呼叫已接受。

## 按需继续

- [explicit-affiliation-publish](explicit-affiliation-publish.md)
- [explicit-affiliation-observation](explicit-affiliation-observation.md)
- [explicit-deaffiliation-state](explicit-deaffiliation-state.md)
- [active-call-entry](active-call-entry.md)
- [explicit-affiliation-server-gates](explicit-affiliation-server-gates.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页211、212、213、214、215、216、217、218、219、228、229、230、231、235；仅本版本。

- [implicit-affiliation-state](implicit-affiliation-state.md)
