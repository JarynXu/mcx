# 排队后授予：T4重发何时停止，达到上限是否撤权

TS24.581 V19.2.0普通在网非广播、非紧急/迫近危险、非临时组。

本次请求已合法排队且已协商queueing，当前已选定participant并进入G: Transmit Taken；不由本页证明先前队列选择规则正确或完整。

只跟踪一个已授予源；不扩展多源重传实例归属、抢占和发送优先级算法。

## 只有排队后授予启动T4

适用条件：G进入Transmit Taken，向此前排队的participant发送Transmission Granted。

启动T4(Transmission Granted)并令C4=1。T4默认1秒且可配置，来自T4-transmission-granted；C4默认3且可配置，来自C4-transmission-granted；未配置counter值时必须采用默认值。启动条件属于排队后授予，不是所有Grant通用条件，也不是客户端T100。

- 表把queueing协商条件写明，程序step2只写was queued，本条保留二者。
- 配置为规范引用，未查询实际部署值；不写死三次或三秒必结束。

依据：§6.3.4.4.1;6.3.4.4.2 step2;11.1.3 Table11.1.3-1 T4 row;11.2.3 Table11.2.3-1 C4 row，印刷页 58、59、219、224。

## T4达到上限不自动撤权

适用条件：G: Transmit Taken中T4到期；分别按C4未到上限及到达上限处理。

C4未到上限时先重发带已授优先级及原音视频SSRC的Granted，再启动T4并将C4加一，仍Taken。T4到期且C4达到上限时，§6.3.4.4.10仍要求保持Taken；不能补成自动撤权、选择下一排队者或挂断通话。

- 达到上限后的额外恢复策略未由此段规定；保持服务器Taken也不证明客户端已收到或使用授予。

依据：§6.3.4.4.9;6.3.4.4.10，印刷页 61、62。

## 媒体到达或结束请求停止T4

适用条件：G: Transmit Taken收到获授客户端RTP到达指示，或收到Transmission End Request。

两条事件都停止运行中的T4。媒体事件继续依本地策略和接收状态分发并保留Taken；结束请求则另按Cx下限及停止转发规则处理。接口可要求Granted的Ack，但该段Ack收取/丢失处理是实现选项，不能用它替代这里明确的媒体/结束停止条件。

- 计时表T4正常停止写Sending of RTP，而procedure以服务器收到获授客户端媒体到达指示描述；两种措辞保留，不擅造新Ack必停事件。
- 此处不重复发送结束主链，详见已发布server-transmission-grant。

依据：§6.3.4.4.5;6.3.4.4.6;6.3.5.3.5;6.3.5.4.9;11.1.3 Table11.1.3-1 T4 row，印刷页 59、60、70、71、78、79、219。

## 证据边界

- 先前Idle入态的排队外层条件异常不在本页修正。
- 没有将本主题扩成所有可靠交付机制或跨系统Track Info处理。

## 按需继续

- [server-transmission-grant](server-transmission-grant.md)
- [participant-transmission-control](participant-transmission-control.md)

[3GPP TS24.581 V19.2.0 / ETSI TS124581 V19.2.0 (2026-08), Release19](https://www.etsi.org/deliver/etsi_ts/124500_124599/124581/19.02.00_60/ts_124581v190200p.pdf)；仅本版本。
