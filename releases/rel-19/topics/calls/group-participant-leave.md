# 组呼参与者退出：BYE、REFER与全组释放判断

TS24.379 V19.4.0，普通在网已建立预安排组呼；本条conditions叠加此范围。

## 按需退出

适用条件：用户要求退出已建立的按需组呼。

客户端经10.1.1.2.3.1进入6.2.4.1，先与媒体面交互，再发送BYE，Request-URI为要退出的MCPTT session identity；收到BYE的200后再与媒体面交互。不能套用通用6.2.5中未建立INVITE的CANCEL分支。

依据：§10.1.1.2.3.1;6.2.4.1。

## 预建立会话中的退出

适用条件：用户要求退出预建立会话中的组呼。

客户端发送对话外初始REFER。Request-URI为服务服务器上标识预建立会话的PSI；Refer-To为要退出的MCPTT session identity，method=BYE；Target-Dialog标识预建立会话；Refer-Sub=false、Supported=norefersub。发送前及收到REFER 2xx后分别执行规定媒体交互。此REFER不是拆除预建立对话的BYE。

依据：§10.1.1.2.3.2;6.2.4.2。

## 迁移退出的Reason

适用条件：客户端退出本次已建立按需组呼或预建立承载中的组呼，且该退出由用户迁移触发。

BYE或REFER按对应客户端分支加入Reason，protocol=SIP、cause=200、text=User migration；不能无条件加在普通用户退出上。

依据：§6.2.4.1;6.2.4.2。

## 发起参与功能转发BYE

适用条件：发起参与功能收到所服务客户端退出BYE。

经10.1.1.3.3.1进入6.3.2.1.6：执行媒体交互后生成发向控制功能的BYE；Request-URI使用所收BYE的session identity，P-Asserted-Identity为自身参与功能PSI；原请求含mcptt-info时复制。控制侧200回到后向客户端转送200并执行控制侧会话资源释放交互。

依据：§10.1.1.3.3.1;6.3.2.1.6。

## REFER身份与订阅门槛

适用条件：发起参与功能收到客户端REFER且Refer-To的method=BYE。

用P-Asserted-Identity中的public user identity确定MCPTT ID；无identity binding时返回403及Warning 141并停止。Refer-Sub=false且Supported包含norefersub时不建立隐式订阅。

依据：§10.1.1.3.3.2;6.3.2.1.7。

## REFER确认先于下游BYE

适用条件：收到客户端REFER，Refer-To URI的method=BYE，且PAI中的PUI与MCPTT ID绑定存在。

参与功能先发送REFER 200（Supported=norefersub；请求Refer-Sub=false时响应也带false），之后才生成发往控制功能的BYE：URI为Refer-To中的session identity，PAI为自身PSI，按存在条件复制mcptt-info。下游BYE 200再触发控制侧关联媒体资源释放。因此REFER 200不证明下游BYE已完成。

依据：§6.3.2.1.7。

## 控制侧检查整组释放策略

适用条件：控制功能收到普通组呼参与者退出BYE。

控制功能先执行相应客户端腿媒体资源释放交互并回应200，再检查组呼释放策略6.3.8.1。若需要全组释放，调用6.3.3.1.5并按存在条件传递mcptt-info；若不需要全组释放，必须向仍参与且订阅conference事件的客户端发NOTIFY。单个退出既不必然解散全组，也不保证全组继续。

依据：§10.1.1.4.3;6.3.3.2.4。

## 证据边界

- 只核SIP业务控制链；24.380媒体及话权的具体消息、完成条件未核，不能承诺媒体清理全部完成。
- RFC/24.229通用重试、超时、事务竞争未展开。
- 组呼释放策略及T4/TNG2/TNG3细则继续引用已有group-release-timers，不重复覆盖。
- 排除紧急/迫近危险、远程发起的隐式归属清理、临时组及ad hoc额外规则。
- 本次退出与显式PUBLISH归属撤销分别建模；不能从此处未写撤销推成所有条件下归属永久保留。
- 6.3.2.1.6在发起参与功能语境的200响应段将主体称为terminating MCPTT function。保留该文字错位提示，不据此新造额外终接角色跳转。

## 按需继续

- [group-release-timers](group-release-timers.md)
- [../groups/conference-state](../groups/conference-state.md)
- [../groups/explicit-deaffiliation-state](../groups/explicit-deaffiliation-state.md)
- [group-participant-removal](group-participant-removal.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页73、109、110、149、278、288、289、302；仅本版本。

## 离网独立范围

本页在网条件与claim不适用于离网组呼。离网基本呼叫控制另见：

- [离网组呼的本端退出与忽略窗口](offnetwork-group-local-leave.md)
