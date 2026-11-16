# 向另一客户端拉视频：请求角色与双边授权

## 适用范围

- TS24.281 V19.3.0，普通在网one-to-one video pull：用户A要求从指定用户B的MCVideo客户端拉取视频；双方按需会话且使用transmission control。
- 不含one-from-server、离网、功能别名、跨域、预建立、ambient viewing、组呼或紧急扩展。普通私呼被调用程序的身份、服务准入、安全及拒绝后停止条件仍适用，pull只增加明确澄清。
- 本页核信令入口和媒体调用边界，不声称已核pull专属TS24.581媒体状态机、实际首帧或停止播放时刻，也不证明精确跨规范版本组合完整互通。

## 请求方与会话类型

适用条件：A客户端要从另一MCVideo客户端B拉视频，进入pull发起入口。

A须复用§10.2.2.2.1，mcvideo-info的session-type明确改为one-to-one video pull。A是信令呼叫发起方，不能因它发INVITE就认定它是所拉视频的发送方。

- 这是指定字段澄清而非完整INVITE配方；不能使用普通private值替代pull类型，也不套服务器文件URL分支。

依据：3GPP TS24.281 V19.3.0 §12.2.2.1，印刷页 400。

## 两侧PF沿用私呼检查

适用条件：O-PF或T-PF分别收到自己角色的INVITE，session-type为one-to-one video pull。

两侧PF须将其识别为私呼，并分别调用§10.2.2.3.1.1和§10.2.2.3.2。pull类型不取消普通私呼服务器链的前置检查。

- 只确认继承入口，不重建完整PF算法；不要把one-from-server分支的不检查allow-private-call例外移到此处。

依据：3GPP TS24.281 V19.3.0 §12.2.3.1.1;12.2.3.1.2，印刷页 401。

## CF分别检查双方权限

适用条件：CF收到其角色的one-to-one video pull INVITE，调用§10.2.2.4.2并执行pull专属检查。

CF须分别检查`<mcvideo-calling-user-id>`是否获准发起pull、`<mcvideo-called-party-id>`是否获准接收pull呼叫。任一未授权均须返回403及规定Warning，并停止余下步骤。被叫接收pull呼叫的权限不等于请求方已有媒体画面。

- 不从普通私呼获准反推pull双边权限；该段未列具体配置叶或Warning数值，本页不补造。

依据：3GPP TS24.281 V19.3.0 §12.2.3.2.2，印刷页 401、402。

## 证据边界

- 仅所列信令条件与接口，不能替代全部SIP或媒体实现。

## 按需继续

- [MCVideo 私呼服务器链：身份准入、终接设置与逐段应答](private-call-server-admission.md)
- [拉视频的开始与结束：媒体请求、通话成功和释放分开判断](video-pull-start-and-release.md)

[3GPP TS24.281 V19.3.0](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅所列版本和条款。
