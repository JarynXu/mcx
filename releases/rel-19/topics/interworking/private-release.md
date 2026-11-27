# 互通私呼释放：发起方与确认次序

ETSI正式发布的TS23.283 V19.5.0，Release19，Stage2。

适用前提：MC用户已注册且正与经IWF接入的LMR用户私呼；可为自动或手动模式，有或无话权控制。

## MC客户端发起释放

客户端向服务器请求结束，服务器转IWF；收到IWF确认后，服务器再确认客户端请求。客户端和IWF释放媒体资源；若有话权控制，也释放相关资源，客户端不得再请求话权或发送媒体。 [§10.4.4.1](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 服务器因结束条件决定终止

最大通话时长或无收发超时是示例条件，并非本页给定的固定时长。服务器向MC客户端和IWF发结束请求，双方确认并释放媒体及适用的话权资源，用户获得结束通知。 [§10.4.4.2](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## LMR用户或系统发起释放

IWF请求服务器，服务器转MC客户端；收到客户端确认后再确认IWF。双方释放媒体及适用的话权资源。附加应用数据可选，客户端如何反应不在该规范范围。 [§10.4.4.3](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 边界

LMR端如何通知用户不在范围内；不提供超时值、丢包重传或SIP编码。

[private-manual](private-manual.md) · [private-encryption](private-encryption.md) · [结构化条件](private-release.json)

查[IWF 结束请求和应答里的主被叫 ID、应答方 ID 或附加数据](private-call-ringing-and-end-elements.md)，按本腿信息流读，不把它当终端收件或资源已释放。
