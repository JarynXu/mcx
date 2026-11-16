# MCVideo无人接收：通知不等于自动结束

依据ETSI正式发布的3GPP TS22.281 V19.0.0，Release19；仅在网Stage1需求。

## 用户正在向MCVideo组发送

无其他归属成员和无人接收是分别触发通知的条件，服务须通知正在发送的组成员。选择加入型通信启动后，应给其他用户合理选择时间，再发无人接收通知；没有给出统一秒数。 [§5.2.6.2.4 R-002/003 NOTE](https://www.etsi.org/deliver/etsi_ts/122200_122299/122281/19.00.00_60/ts_122281v190000p.pdf)

## 没有用户接收当前通信

服务可中断传输；有已归属/获授权用户希望接收时可恢复。两者是可选能力，不能改写成无人接收必定结束整个通信。 [§5.2.6.2.4 R-004/005](https://www.etsi.org/deliver/etsi_ts/122200_122299/122281/19.00.00_60/ts_122281v190000p.pdf)

## 边界与关联

不提供邀请、媒体建立、暂停或恢复的线级消息和定时器；配置能力不等于任意部署已开启。

[transmission-admission](transmission-admission.md) · [reception](reception.md) · [结构化条件](no-receivers.json)

## 服务器计时与结束证据

- [某个源无人接收：T11到期、停止命令与T3确认](server-stream-idle-termination.md)

这些路径依据TS24.581 V19.2.0指定Stage3程序，不把业务要求、发出命令和完成停止视为同一事件。
