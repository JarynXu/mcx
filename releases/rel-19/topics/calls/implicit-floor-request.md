# 隐式话权请求：初始INVITE、升级与预建立REFER

TS24.379 V19.4.0 §6.4的选定普通语音与升级入口；这里只判断请求是否携带隐式话权请求，不等于话权已经授予。远程环境监听的授予被叫例外不在本页展开。

## 初始INVITE的联合条件

适用条件：发起MCPTT语音会话，或发起不用于远程环境监听的预建立会话。

关联话权UDP流的SDP带mc_implicit_request fmtp属性时，服务器才将初始INVITE视为主叫的隐式话权请求；不是看到INVITE就自动推断主叫拿到话权。

依据：§6.4 初始INVITE分支。

## 升级re-INVITE也有专门条件

适用条件：组呼升级紧急、私呼升级紧急，或组呼升级imminent peril之一。

只有关联话权UDP流的SDP带mc_implicit_request时，该re-INVITE才被视作隐式话权请求；不满足§6.4任一适用分支的(re-)INVITE按无隐式请求处理。取消紧急不能仅凭沿用re-INVITE就被归入升级分支。

依据：§6.4 re-INVITE分支。

## 预建立REFER没有SDP时

适用条件：使用预建立会话；Refer-To的cid所指resource-lists条目URI headers/body中没有SDP offer。

只有该预建立会话建立时已有隐式话权请求，REFER才继承为隐式请求。不能把缺SDP统一解作无请求。

依据：§6.4 REFER分支条件1。

## 预建立REFER带SDP时

适用条件：使用预建立会话，Refer-To的cid所指resource-lists条目URI headers/body含SDP offer。

无论预建立会话原先是否有隐式请求，本次SDP须在关联话权UDP流中包含mc_implicit_request，才把REFER视为隐式请求；其他情况按无请求处理。原先开启不等于本次带SDP却缺该属性仍自动继承。

依据：§6.4 REFER分支条件2–3。

## 证据边界

- TS24.380规定属性编码、话权状态及是否授予，本页未完整核验；不从请求识别推断实际媒体权限。
- 远程发起环境监听存在向被叫授予话权的独立例外，本页排除该业务，不将普通请求规则泛化。

## 按需继续

- [without-floor-control](without-floor-control.md)
- [../emergency/private-upgrade](../emergency/private-upgrade.md)
- [../security/group-call-media-boundaries](../security/group-call-media-boundaries.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页165、166；仅本版本。

按需核对媒体层指定分支：[floor-participant-entry-request](floor-participant-entry-request.md)。来源版本及条件以该页为准。
