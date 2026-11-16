# 组呼参与者状态：订阅寻址、权限与通知证据

TS24.379 V19.4.0；在网进行中组呼的conference状态，客户端已参与该会话。

除broadcast-rejection明确列出的广播拒绝分支外，本主题聚焦普通非广播、非临时重组组呼。不将成员表、归属状态和当前通话参与者表混用。

## 会话URI和组ID各放在哪里

适用条件：客户端在进行中的非广播组呼中选择订阅。

在新SIP对话发送SUBSCRIBE：Request-URI为MCPTT session identity，mcptt-info正文的mcptt-request-uri为组ID；P-Preferred-Service为MCPTT ICSI，Accept为application/conference-info+xml，Accept-Contact含相应ICSI特征和require/explicit。需要后续通知时请求Expires=4294967295；仅取当前状态时请求Expires=0。零期限快照不等于退出通话。

依据：§10.1.3.1;10.1.3.2 steps 1–9。

## 参与功能映射会话身份

适用条件：请求来自该参与功能服务的客户端；P-Asserted-Service为MCPTT ICSI，Accept含conference-info+xml，mcptt-info的mcptt-request-uri为组ID。

若Request-URI不能解析为现有会话，拒绝404/Warning137并停止。否则向映射的MCPTT session identity发出SUBSCRIBE，正文加入served用户的mcptt-calling-user-id，并加入指向自身的Record-Route。200响应的Contact也做对应会话身份映射；不能假定两侧URI相同。

依据：§10.1.3.3。

## 参与通话不自动获得状态订阅权限

适用条件：控制功能收到非广播组呼SUBSCRIBE；正文mcptt-request-uri为该会话组ID，mcptt-calling-user-id为参与者MCPTT ID；P-Asserted-Service为MCPTT ICSI且Accept含conference-info+xml。

按组文档on-network-allow-conference-state检查该身份；不允许则403/Warning138并停止。允许后按RFC6665/4575处理、缓存订阅并发送状态通知。归属和呼叫准入不能替代这项权限。

依据：§10.1.3.4.1。

## 广播组呼的单独拒绝

适用条件：控制功能收到针对以broadcast方式发起的组呼的conference状态订阅请求。

返回480并带Warning105。此分支不是普通组呼权限不允许时的403/138。

依据：§10.1.3.4.1 broadcast branch。

## 收到退出BYE或有新参与者加入

适用条件：控制功能按10.1.3.4.2收到订阅、收到prearranged/chat/adhoc参与者BYE，或有新参与者加入；对有效订阅者通知。

按6.3.3.4生成并向订阅者发送NOTIFY；不自动发给所有组成员。参与功能在订阅所建对话中复制NOTIFY内容，并把转送Request-URI设为served用户的public service identity。客户端按RFC6665/4575处理，可显示参与用户ID及可用功能别名；是否展示由客户端选择。

依据：§10.1.3.4.2;10.1.3.3;10.1.3.2。

## 通知表达会话状态，不是授权名单

适用条件：控制功能生成conference状态NOTIFY；此处按普通预安排或chat组呼解释别名。

Event为conference，conference-info的entity为组ID；每个参与者的user.entity为MCPTT ID，其单一endpoint含entity和RFC4575会话status。可选功能别名是用户与本组绑定的别名；可选roles仅供人阅读，不能作为程序授权依据。endpoint状态不能被简化为所有列出用户都已接听。

依据：§6.3.3.4。

## 订阅期限和通话期限分开

适用条件：比较客户端SUBSCRIBE请求与控制功能生成的NOTIFY。

客户端持续订阅请求的Expires为4294967295，而6.3.3.4给NOTIFY写的是默认Expires=3600秒。两者不是同一字段位置或通话最大时长；本页不据此推导协商结果、自动刷新算法或定时释放通话。需要结束订阅时依RFC6665终止并指示终止。

依据：§10.1.3.2;6.3.3.4。

## 证据边界

- RFC4575的全量/增量合并及版本断档按关联页读取；RFC6665完整对话生命周期未展开。不能把每次NOTIFY都当完整名单快照。
- 临时组与非控制功能的聚合路径另有10.1.3.4.3–.5条件，未纳入本页；其中发送侧calling-group-id与接收入口calling-user-id的关系未在本页解决。
- 缺失功能别名不能推导无绑定；通知也不证明话权或媒体已可用。

## 按需继续

- [active-call-entry](active-call-entry.md)
- [rejoin-session](rejoin-session.md)
- [explicit-affiliation-observation](explicit-affiliation-observation.md)
- [../calls/group-acknowledged-start](../calls/group-acknowledged-start.md)
- [conference-state-merge](conference-state-merge.md)

[官方来源](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页151、152、356、357、358、359、360；仅所列版本。

控制侧主动成功移除用户后的通知另属§10.1.1.4.4.3的MAY分支，见[参与者移除](../calls/group-participant-removal.md)。
