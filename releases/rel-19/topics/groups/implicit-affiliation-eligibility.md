# 请求触发的隐式归属：资格、状态和呼叫权限分开判断

在网MCPTT，限TS24.379 V19.4.0。

通用资格helper仅在调用方明确要求时适用；具体调用例子限定按需预安排组呼，不推及所有SIP请求、预建立REFER、广播、远程授权或重组流程。

## 哪些请求触发隐式归属

适用条件：O-PF收到符合§10.1.1.3.1.1的prearranged初始INVITE；此前身份绑定、授权、媒体、资源及并发呼叫检查未停止处理，且本claim限定无associated-group-id的普通组寻址，不覆盖重组中的目标组转换。

若按§9.2.2.2.11判定本用户/client未归属目标组且请求已按§6.3.2.1.8.1获优先呼叫授权，调用§9.2.2.2.12；或请求的remotely-initiated-call-request-ind=true时调用该过程。后一分支未重复未归属条件。不能把任意未归属普通INVITE都视为自动建归属。

依据：§10.1.1.3.1.1 steps6(a–b)。

## 资格检查不建记录

适用条件：控制功能收到针对用户尚未归属组的SIP请求，且调用方要求检查隐式归属资格，进入§9.2.2.3.6。

调用§9.2.2.3.8；组ID取mcptt-request-uri，用户ID取mcptt-calling-user-id。GMS中不存在该组、用户不是该组成员，或本地§9.2.2.3.2没有匹配group entry，任一即不合格并停止；均通过才判定可隐式归属。本过程只判资格，不新增user/client记录，也不自行规定SIP拒绝码。

依据：§9.2.2.3.6;9.2.2.3.8 steps1–6。

## 发起与加入权限仍独立

适用条件：控制功能按§10.1.1.4.2处理预安排组呼，前序检查未停止；这里分别讨论其新建step14和已有通话step15。

即使用户满足隐式归属资格，新建仍在step14(b)检查§6.3.5.4发起授权，失败403/119；加入已有通话仍在step15(b)检查§6.3.5.3加入授权，失败403/121。相应隐式记录操作分别位于14(c)、15(e)，不能把资格、记录创建或通知等同呼叫许可。

依据：§10.1.1.4.2 steps14(b–c),15(b,e)。

## N2失败及优先策略例外

适用条件：O-PF在§10.1.1.3.1.1中已执行step6隐式归属；因用户已达到N2而未能使本次归属成功。

step7要求486/102并停止。Note5另限定：请求含true的emergency或imminent-peril指示且已按§6.3.2.1.8.1获优先授权时，本地策略可以允许N2例外，或取消较低优先归属腾出位置。因此既不能写所有优先呼叫必定绕过N2，也不能写一到N2必定无例外失败。

依据：§10.1.1.3.1.1 step7,Notes4–5。

## 两侧状态判断与资格区别

适用条件：需要解释为何PF侧归属判断与CF侧实际记录判断可能不同，且只比较各自调用的已有记录消费过程，不以资格通过证明实际记录存在。

PF的§9.2.2.2.11可把匹配记录的affiliating状态视为已归属；CF的§6.3.6仍检查组、用户、本次client及user entry未到期。隐式资格中的group entry存在也不意味着该user/client已加入该记录。三者分别是参与侧状态判定、控制侧已归属判定和新归属资格。

依据：§9.2.2.2.11;6.3.6;9.2.2.3.8。

## 证据边界

- 不据此重新解释14(a/c)、15(a/e)中混合and/or及远程发起引用的歧义；本claim只确认独立的授权检查与步骤位置。
- 9.2.2.2.11 step1(a)：step1查user entry，失败分支却称group entry；已有页按上下文呈现，不将此文字疑点藏在通用可执行算法中。本小节也未重复expiration检查。
- 10.1.1.4.2 steps14(a/c),15(a/e)：复合and/or、远程发起和资格来源交叉引用仍保留原文边界。本页不生成覆盖所有优先/远程/重组场景的布尔表达式。
- 9.2.2.2.15 配置触发过程：服务授权成功后，profile无OnNetwork/ImplicitAffiliations或无含组ID的entry时停止；有配置时走候选表及§9.2.2.2.6 PUBLISH。这里不展开完整的配置触发过程，也不将业务呼叫的2xx完成规则套用到该路径。
- 6.3.2.1.8.1;6.3.3.1.13.2;6.3.3.1.13.5：本页仅使用调用方已判定的优先授权结果，未重新验收全部配置条件。
- 外部依赖：TS24.229 SIP事务、TS24.481/24.484配置取得与合法性、TS29.283数据库、TS33.180服务授权、RFC实现依赖未在本页完整核验。

## 按需继续

- [../groups/prearranged-admission](../groups/prearranged-admission.md)
- [../groups/join-authorization](../groups/join-authorization.md)
- [../groups/active-call-entry](../groups/active-call-entry.md)
- [../groups/explicit-affiliation-server-state](../groups/explicit-affiliation-server-state.md)
- [../calls/implicit-floor-request](../calls/implicit-floor-request.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页163、164、222、223、232、233、279、280、296、297、298；仅本版本。
