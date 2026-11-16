# 在网按需私呼：被叫客户端的拒绝、应答和取消

TS24.379 V19.4.0 §11.1.1.2.1.2，带话权控制的在网按需私呼及明确标示的 first-to-answer 分支。这里只覆盖被叫客户端，不替代服务器授权和完整 SIP 核心流程。

## 先处理资源和准入拒绝

适用条件：被叫收到初始 SIP INVITE。

占用其他会话且并发超过 MaxCall、资源不足或规范范围外原因时，客户端可拒绝。通常用适当拒绝码及Warning；用户获准限制失败原因时，可用无Warning的480。拒绝后不再执行本节其余步骤。

依据：§11.1.1.2.1.2 步骤1–2。

## 收到MIKEY时先验证，失败不能继续应答

适用条件：SDP的a=key-mgmt携带MIKEY-SAKKE I_MESSAGE。

取发起用户身份、转换UID并验签。认证失败须返回488和Warning136；验签成功才解封PCK并取PCK-ID。共享密钥是保护前提，不等于被叫已接受业务。

依据：§11.1.1.2.1.2 步骤4。

## first-to-answer有单独忙和未答规则

适用条件：session-type为first-to-answer。

通知用户且不得转发此呼叫。用户正忙于其他通话时返回486并停止；在客户端实现决定的时限内未答时返回480并停止，不能捏造统一秒数。

依据：§11.1.1.2.1.2 步骤8。

## 手动应答区分拒绝、转发与振铃

适用条件：已按模式规则进入手动私呼过程。

用户拒绝为480+Warning110；请求手动转发为480+Warning175，随后转入转发流程；这两支均停止本节后续处理。其余生成180；发送最终200时遵循自动模式所用的200构造规则，含会话计时器和SDP等要求。180不证明呼叫已完成。

依据：§6.2.3.2.1; 6.2.3.1.1。

## 最终应答前取消分别响应两个请求

适用条件：已有对话，收到取消该INVITE的CANCEL，且尚未向INVITE发送200。

向CANCEL回复200，向INVITE回复487；若此前保存了临时MEPP状态则恢复并丢弃临时值。不能将CANCEL的200当作INVITE被接受。

依据：§11.1.1.2.1.2 CANCEL分支。

## 证据边界

- Answer-Mode和Priv-Answer-Mode的模式选择另见 commencement-selection；不能从发送方请求自动接听推断任意呼叫均被接受。
- 未核 TS24.229、TS24.380 的完整依赖与全部转发/转接流程；不构造完整消息模板。
- MaxCall及失败原因限制的配置文档未新增核验；first-to-answer的密钥生成特殊分支未完整收录。

## 按需继续

- [commencement-selection](commencement-selection.md)
- [../security/private-key-distribution](../security/private-key-distribution.md)
- [../identity/service-authorization](../identity/service-authorization.md)
- [../interworking/private-manual](../interworking/private-manual.md)

[ETSI 官方 TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页71、72、422、423、424；仅本版本。

前置授权见[主叫参与功能](originating-authorization.md)与[被叫参与功能](terminating-authorization.md)；跨节点200含义见[控制功能响应](control-routing-results.md)。这些是各自角色的条件，不能合并成只看状态码的判断。
