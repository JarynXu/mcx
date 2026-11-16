# First-to-answer：分发目标、选中应答者与清理其他分支

TS24.379 V19.4.0，在网按需、带话权控制的first-to-answer选定服务器步骤；不是群组通话，也不是所有被叫都参与的会议。

## 主叫要有first-to-answer许可

适用条件：originating participating功能处理session-type为first-to-answer。

allow-request-first-to-answer-call缺失或false：403+Warning156。非空PrivateCall名单与全部请求目标均不匹配且不允许名单外拨打：403+153。生成下游请求时，若有该非空名单，仅包含匹配名单的目标entry；不能把至少一项获准理解为整个原始名单都传出。

依据：§11.1.1.3.1.1 步骤11A–12、15a。

## 控制功能发出的邀请指定手动模式

适用条件：控制功能邀请first-to-answer目标。

发出的INVITE带Priv-Answer-Mode=Manual。通常邀请资源列表用户；call-to-functional-alias-ind=true的功能别名分支须先解析激活该别名的ID，未得到任何ID则403+145。解析细节未在本页展开。

依据：§11.1.1.4.1 步骤3；11.1.1.4.2 步骤12。

## 第一条可形成上游最终结果的200带被选用户ID

适用条件：收到相应first-to-answer SIP INVITE的200响应，尚未向主叫发最终响应。

构造上游200和SDP，包含该分支所邀请用户的mcptt-called-party-id；完成规定媒体处理后发送。随后清理其他受邀客户端分支，不把所有200都作为新的主叫成功结果。

依据：§11.1.1.4.2 first-to-answer收到200分支。

## 其他分支按对话是否建立分别清理

适用条件：first-to-answer已进入上述成功响应分支，清理未选中的其余受邀客户端。

已建立对话用BYE并标记not selected for call；尚未建立的用CANCEL。收到CANCEL的200还须等待原INVITE的487；实现决定的等待时间内未收到487时发携带not selected for call的BYE。未成功清理可重发CANCEL/BYE，但本节不给统一秒数或无限重试保证。

依据：§11.1.1.4.2 first-to-answer收到200分支步骤8–9。

## 证据边界

- 仍需主叫一般私呼权限、媒体及其他前置检查，专属许可不是替代条件。
- 步骤15a对非空名单的过滤没有重述名单外许可例外；保留原文过滤条件，不自行补例外。
- 原文步骤8/9的后向编号有不一致，本页按对应行为及条件定位；不扩写精确竞争算法或同时应答排序。

## 按需继续

- [originating-authorization](originating-authorization.md)
- [control-routing-results](control-routing-results.md)
- [private-client-acceptance](private-client-acceptance.md)

[ETSI 官方 TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页438、439、453、455、456、457、458；仅本版本。
