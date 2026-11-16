# 已有私呼升级紧急：呼叫与告警的不同结果

TS24.379 V19.4.0 Stage3在网、带话权控制的已有私呼；升级程序覆盖按需及预建立会话，不扩展为离网或私呼imminent-peril。

## 升级与告警分别授权

适用条件：用户请求升级已有私呼；客户端MEPC=1。

使用re-INVITE并保持当前SDP媒体参数。紧急私呼须allow-emergency-private-call=true，同时目标规则满足二选一：EmergencyCall/MCPTTPrivateRecipient为LocallyDetermined；或为UsePreConfigured且名单包含目标MCPTT ID。获准后emergency-ind=true、MEPC=2，MEPP不为2时设4，尚未设置的整体emergency state亦设置。同步告警另须allow-activate-emergency-alert=true，且OnNetwork/PrivateEmergencyAlert满足对应本地或预配置目标条件，获准后alert-ind=true、MPEA=2并附规定位置；未请求告警置false。请求但未获准告警不是该条明确的false分支。

依据：§6.2.8.3.1.1、6.2.8.3.1.3、6.2.8.3.2；11.1.1.2.1.5。

## 媒体、组合和授权检查

适用条件：控制功能收到emergency-ind=true的升级re-INVITE。

SDP须至少有一条参数及至少一个codec/media format可接受的媒体流，否则488。组合要求不含imminentperil-ind且含alert-ind，不合法则403+Warning150。紧急私呼未授权则403并携emergency-ind=false、alert-ind=false，停止；字段组合合法不是业务授权。

依据：§11.1.1.4.3 步骤1–3；6.3.3.1.17；6.3.3.1.14。

## 转发时保留授权结果

适用条件：控制功能通过前置检查并进入升级转发。

复制mcptt-info并为获准升级置emergency-ind=true。请求告警true且获准才按告警程序填充；转发条款对未提供告警或true但未授权写置false，不能反推前级组合校验允许缺alert-ind。Resource-Priority取紧急配置值，不是固定优先级数字。

依据：§11.1.1.4.5；6.3.3.1.19。

## 接收端不重新选择应答模式

适用条件：既有私呼接收端收到emergency-ind=true的re-INVITE。

将本呼叫MEPP设2，应显示升级与发起人，alert-ind=true时应显示告警。按会话类型处理SDP并接受re-INVITE回200，不改变既有answer-mode；不是一次新人工接听。

依据：§11.1.1.2.1.3 步骤1、5–9及注1。

## 控制侧构造升级成功响应

适用条件：控制侧收到下游升级re-INVITE的200，且尚未回请求方。

构造带当前SDP的上游200并与媒体面交互后发送；请求alert-ind=true但告警未获准时带Warning149。

依据：§11.1.1.4.3 成功响应；6.2.8.3.4；11.1.1.2.1.5。

## 客户端分别确认呼叫和告警

适用条件：请求客户端收到本次升级2xx，且MEPC为2或3。

设MEPP=2、MEPC=3。MPEA原为2且响应不含Warning149才设MPEA=3；不能从升级2xx推断告警一起成功。

依据：§11.1.1.4.3 成功响应；6.2.8.3.4；11.1.1.2.1.5。

## 控制侧在ACK后发INFO

适用条件：带Warning149的升级200收到ACK，原请求告警true但未获准。

控制侧按§6.3.3.1.18发INFO，给emergency-ind=true、alert-ind=false。

依据：§11.1.1.4.3 ACK分支；6.3.3.1.18；6.2.8.3.7。

## 客户端解释特定INFO

适用条件：客户端收到本优先级私呼内Info-Package为g.3gpp.mcptt-info且关联mcptt-info+xml消息体至少设置alert-ind、imminentperil-ind、emergency-ind之一的INFO，且MPEA=2。

据alert-ind=false转MPEA=1、true转MPEA=3。不能把任意INFO当作告警确认。

依据：§11.1.1.4.3 ACK分支；6.3.3.1.18；6.2.8.3.7。

## 升级失败保留既有状态

适用条件：本次升级收到4xx/5xx/6xx，且MEPC为2或3。

MEPC退为1，仅MEPP原为4才退为1；原请求alert-ind=true时MPEA退为1。此分支没有清空既有MEPP=2、挂断原呼叫或清除全部紧急状态的步骤，不套用取消紧急失败的恢复规则。

依据：§6.2.8.3.5；11.1.1.2.1.5。

## 转发前缓存不证明下游成功

适用条件：前置检查通过，且发起人与目标尚非in-progress emergency private call。

控制功能在转发前缓存该用户对的紧急状态；同一条件内告警true且获准再缓存告警。本条没有给出下游失败后的缓存回滚算法，不补造成事务提交/回滚。

依据：§11.1.1.4.3 步骤5及末段。

## 证据边界

- §11.1.1.2.1.5末段将INFO会话写成group，而§6.2.8.3.7明确private；§11.1.1.4.3/4.5授权步骤交叉引用有编号异常，保留疑义。
- 取消授权FFS属于§6.3.3.1.13.4，不扩成升级授权FFS，也不能用升级规则消除取消FFS。
- Annex G、TS24.229/24.380/24.484、INFO完整RFC及位置内容未全部核验；不提供完整状态机、超时重试或媒体算法。

## 按需继续

- [private-downgrade](private-downgrade.md)
- [alert-state](alert-state.md)
- [../calls/control-routing-results](../calls/control-routing-results.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页88、89、90、91、92、137、138、141、142、143、425、426、427、428、458、459、461；仅本版本。
