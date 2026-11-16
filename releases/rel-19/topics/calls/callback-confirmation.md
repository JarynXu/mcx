# 私呼回呼请求：确认消息不是回呼接通

TS24.379 V19.4.0 §11.1.5的选定客户端、参与功能及控制功能流程。回呼请求者与稍后拨回的目标用户是两个角色；不把SIP事务成功等同业务确认。

## 请求与取消各有权限

适用条件：发起回呼请求或取消请求。

客户端相应allow-request-private-call-call-back或allow-cancel-private-call-call-back缺失/false时通知用户并停止。主叫参与功能另查绑定，无绑定或过期404+141；相应请求无许可分别403+151或403+152。客户端检查不替代服务器检查。

依据：§11.1.5.2.1；11.1.5.3.1 步骤2a–4。

## 发送前记录待确认状态

适用条件：客户端获准发回呼请求或取消请求。

准备MESSAGE：资源列表为目标MCPTT ID，Request-URI为服务自身的参与功能PSI。回呼请求携urgency与time-of-request；请求者按目标ID存记录，先分别进入confirm-pending或cancel-pending，再发送MESSAGE。它还不是confirmed。

依据：§11.1.5.1；11.1.5.2.1。

## 匹配业务消息才改变确认状态

适用条件：请求者有对应目标记录。

只有收到回呼response类型的MESSAGE，mcptt-calling-user-id匹配记录且状态为confirm-pending，才转confirmed。取消response的MESSAGE须匹配记录且处于cancel-pending，才转no-call-back并删记录。发送请求的MESSAGE收到4xx/5xx/6xx，则目标记录转no-call-back并删除；不能用普通MESSAGE的200替代上述业务确认。

依据：§11.1.5.2.1。

## 目标端记录并通知用户

适用条件：目标客户端收到回呼请求MESSAGE。

保存请求者ID、待回呼状态、紧急程度与请求时间并通知用户，再以MESSAGE携回呼response类型回复请求者。回呼本身仍由目标用户随后决定发起，消息确认不等于通话建立。

依据：§11.1.5.2.2。

## 真正回呼走手动起呼

适用条件：目标用户决定履行已记录的回呼请求。

目标客户端用记录中的请求者MCPTT ID，以manual commencement发起私呼，按有/无话权控制入口执行。原请求者发送通话建立的200且记录原为confirmed时删除其请求记录；目标端收到该呼叫INVITE/REFER的2xx且记录为private-call-pending时删除目标记录。

依据：§11.1.5.2.3。

## 控制功能检查并交付MESSAGE

适用条件：控制功能处理回呼请求、取消或response的MESSAGE，后续送至终接参与功能。

缺MCPTT ICSI的Accept-Contact时403；无resource-lists或所有list合计超过一个entry时403+145。控制功能将资源列表用户ID放入mcptt-request-uri，Request-URI指对应终接参与功能PSI。终接参与功能查该用户绑定，无绑定404。下游MESSAGE的2xx使控制功能生成上游200，仍不能替代业务response MESSAGE或真实回呼。

依据：§11.1.5.3.2；11.1.5.4。

## 证据边界

- 目标接收段写PCCB-I2而相邻取消/履行段用PCCB-R2，保留本版标签疑义；本页用语义状态，不据此补全Annex G状态机。
- 未完整收录所有取消竞态、失败重试与媒体步骤；字段说明不是完整报文模板。§11.1.5.3.2步骤5在MESSAGE流程写outgoing INVITE，保留原文疑义。

## 按需继续

- [private-client-acceptance](private-client-acceptance.md)
- [commencement-selection](commencement-selection.md)
- [without-floor-control](without-floor-control.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页465、466、467、468、469、470、471；仅本版本。
