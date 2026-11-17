# MCData组会话状态：订阅权限、通知与结束观察

固定 TS24.282 V19.7.0，普通在网、本地组会话的 conference 状态观察。订阅、PF映射、CF权限、通知与终止依各自角色事件适用，不以全链成功作为共同前提。

正常客户端订阅限其正在参与的非广播组会话；广播拒绝仅在相应CF分支适用。通知的ad hoc成员变化触发另按该条条件，不推广为所有配置组的变化通知。

不覆盖跨域、重组/聚合、优先通信、完整RFC状态合并、可执行XML schema或安全实现。身份绑定、组归属、会话加入、观察权限和数据交付分别判断。

## 参加会话后，选择一次状态或后续通知

适用条件：客户端正在参与一个ongoing、并非以broadcast方式发起的组会话，并选择订阅conference状态。

客户端在新SIP对话中生成SUBSCRIBE。Request-URI为该组的MCData session identity，mcdata-info+xml中的mcdata-request-uri为组ID；P-Preferred-Service使用MCData ICSI，Accept-Contact携相应g.3gpp.icsi-ref及require/explicit，Accept为conference-info+xml。要当前状态及后续通知时请求Expires=4294967295，只取当前状态时请求Expires=0。服务器实际分类还要求请求路由至对应PF或CF的session identity，Event=conference。

- 参加会话是本客户端入口条件，不意味着CF已经允许状态订阅；不能把组ID直接替换为SIP Request-URI的session identity。
- Expires=0在这里表示获取当前状态，不是发BYE、退组或撤销归属；4294967295是请求值，不是已经获授永不过期的观察权限。
- 这里只列24.282的字段和真实分类条件，不展开RFC6665/4575全部对话、刷新或错误恢复。

规范强度：选择订阅为 MAY；一旦选择，所列构造、寻址及按意图设置Expires为 SHALL。

依据：TS24.282 V19.7.0 §25.1;25.2 opening and steps1–9，印刷页572（规范依据）。
依据：TS24.282 V19.7.0 §6.3.1.3 conference subscription classifiers，印刷页95（PF/CF实际命名入口）。

## PF映射已有会话，不用业务组ID代替路由

适用条件：PF收到其服务客户端发出的conference订阅命名请求；P-Asserted-Service为MCData ICSI，Accept为conference-info+xml，mcdata-info含组ID。响应和NOTIFY转送分别由对应实际接收事件触发。

PF尝试把入站Request-URI解析为已有MCData session identity；不能解析时回404/Warning137并停止。继续时生成SUBSCRIBE，以映射的session identity作Request-URI，在info中加入served用户的mcdata-calling-user-id，并加入指向自身的Record-Route后发送。收到SUBSCRIBE响应时复制内容；200的Contact按收到的会话身份作对应映射后转发。收到该订阅对话内、发往served客户端的NOTIFY时复制内容并转发；NOTIFY响应也按本段复制、构造身份并转发。

- 原文在解析失败处写“reject the SIP SUBSCRIBE response”，但当前入口是SUBSCRIBE请求。本页保留此文字差异，不构造向另一个事务拒绝的算法。
- NOTIFY目的地字面是MCData用户的public service identity，不静默改为public user identity。NOTIFY的200响应段要求纳入由收到Contact中的session identity构造的身份，却未像SUBSCRIBE响应段明确输出字段，不能自行指定。
- 两侧session identity可能映射，不能假定相同。SUBSCRIBE的200或NOTIFY的200都不是INVITE成功或数据送达证明。

规范强度：本条匹配、拒绝、映射及转送步骤为 SHALL。

依据：TS24.282 V19.7.0 §25.3 full request/response/NOTIFY procedures，印刷页573,574（规范依据）。
依据：TS24.282 V19.7.0 §6.3.1.3 conference subscription classifiers，印刷页95（命名请求入口）。

## CF另查观察权限，广播请求有独立拒绝

适用条件：正常分支：CF收到对应conference订阅，info中的组ID为该会话组ID，calling-user-id为会话participant的MCData ID，服务ICSI及Accept匹配，且不是broadcast组会话。广播分支：CF实际收到针对以broadcast方式发起的组会话的conference订阅。两分支不同时要求成立。

正常分支中，CF用组文档的on-network-allow-conference-state检查订阅许可；不允许时回403/Warning138并停止。允许后按所引用RFC处理请求，缓存订阅信息并调用§25.4.2发送状态通知。针对broadcast组会话的独立分支生成并发送480/Warning105。参加会话不代替状态订阅许可，403/138和480/105也不是同一种拒绝原因。

- 本页只取participant MCData ID这一入口；权限检查文字还提constituent MCData group ID，但不据此扩展重组或其他身份类别。
- 组文档字段仅按24.282所述检查，不提供配置schema、缺省许可或缓存获取算法。身份、组ID、服务/MIME不满足入口时，本段没有统一错误码，不全部归入138。
- 通过检查后调用通知不保证响应与NOTIFY到达的固定先后，也不保证所有组成员都可观察。

规范强度：许可拒绝、后续缓存/通知及广播拒绝为 SHALL。

依据：TS24.282 V19.7.0 §25.4.1 full normal and broadcast branches，印刷页574（规范依据）。

## 通知只发给订阅者，成员变化触发按组类型解释

适用条件：CF通过§25.4.1订阅处理后调用§25.4.2；或CF在ad hoc组会话收到participant的BYE，或有新participant加入该ad hoc会话。发送对象是已订阅conference事件的客户端/participants。内容解释另以实际按§6.3.2.3生成或收到该类NOTIFY为条件。

§25.4.2对所列事件要求生成通知包，并向已订阅者发送NOTIFY。它明列的BYE和新participant事件限ad hoc会话，不能推成所有普通配置组增删都保证通知。§6.3.2.3的NOTIFY中PAI是CF PSI，Event=conference，默认Expires=3600；正文把组ID、目标用户ID及conference-info的组entity分别表达。每个participant有user及单一endpoint，endpoint含会话status；功能别名和roles为可选，roles仅供人阅读。客户端收到订阅NOTIFY后按所引RFC处理，可以处理状态并显示参与者ID及可用的组绑定别名。

- §25.4.2字面回指6.3.3.4；本版完整§6.3.3是组文档读取、随后直接进入6.3.4，而§25.2 NOTE2明确将通知内容指向6.3.2.3。这里并列记录实际内容段与异常回指，不把源文改号或声称包构造调用完全无歧义。
- §6.3.2.3对发起/加入/重新加入客户端的user.entity写发出INVITE的用户ID，对被邀请客户端明确写ad hoc情形。不能据此补普通配置组所有被邀请端的完整名单编码，也不能把每个列出的endpoint都解释为已成功加入或媒体就绪。
- NOTIFY内默认Expires=3600与SUBSCRIBE请求的0/4294967295处于不同消息，不是会话最大时长或已验证的订阅协商结果。
- 这里不展开RFC全量/增量合并、版本缺口、丢通知恢复或完整schema验证；不能假定每次通知都是完整最新名单。可选别名缺失不证明无绑定，显示状态也不证明SDS/FD交付。

规范强度：触发后的通知及必需内容为 SHALL；功能别名、roles和客户端状态处理/显示为 MAY；不扩展源文未列出的组类型触发。

依据：TS24.282 V19.7.0 §25.4.2;25.2 NOTIFY paragraph and NOTE2，印刷页573,574,575（规范依据）。
依据：TS24.282 V19.7.0 §6.3.2.3 full procedure，印刷页96,97（实际内容依赖，与错误回指并列）。
依据：TS24.282 V19.7.0 §6.3.3 full procedure and transition to6.3.4，印刷页97（comparison-only：核实6.3.3范围及编号，不作为通知算法）。
依据：TS24.282 V19.7.0 §25.2 Expires steps5–6，印刷页572（不同消息期限对照）。

## 结束订阅只结束状态观察

适用条件：客户端需要结束conference订阅；或CF收到按RFC6665终止该订阅的SUBSCRIBE；或ongoing MCData会话中的该事件订阅到期。各事件分别适用。

客户端按RFC6665终止订阅并指示终止。CF收到终止该订阅的SUBSCRIBE时发送200；订阅到期时按RFC6665终止订阅。这些操作的对象是conference事件订阅，不是组会话、成员归属或已传数据。

- 不能由终止订阅的200推导已发组会话BYE、用户离开、全组释放或历史数据撤回。
- 不展开最后NOTIFY、刷新竞态、超时重试或其他RFC终止状态机；这里的200不保证客户端本地显示已清空。

规范强度：所列订阅终止与CF200为 SHALL。

依据：TS24.282 V19.7.0 §25.2 termination paragraph;25.4.3，印刷页573,575（规范依据）。

## 使用边界与相关主题

- 本页核MCData自身conference业务，不把MCPTT/MCVideo的同名流程、权限和增删触发移植过来。
- 通知内容与接口的字面差异均保留；不提供可运行的SIP/XML实现或全组实时一致性保证。

- [sds-session-responses-and-participants](sds-session-responses-and-participants.md)：对照：INVITE/200和迟加入邀请，不是状态订阅许可。
- [adhoc-criteria-membership-lifecycle](adhoc-criteria-membership-lifecycle.md)：对照：已有ad hoc上下文的动态成员动作；本页仅核其实际成员事件之后的观察条件，不重复选人。
- [adhoc-user-participant-update](adhoc-user-participant-update.md)：对照：用户要求修改成员/criteria的re-INVITE；成功响应不替代本页订阅及通知证据。
