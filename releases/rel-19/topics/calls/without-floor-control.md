# 无话权控制私呼如何复用既有流程

TS24.379 V19.4.0 §11.1.2的在网private与first-to-answer；保留按需/预建立两类入口，不能直接删除所有媒体控制字段。

## 按需发起与接收

适用条件：按需发起无话权控制私呼或first-to-answer。

复用§11.1.1.2.1.1，但步骤12不提供media-floor control entity媒体级部分，忽略步骤13。

依据：§11.1.2.1–11.1.2.2。

## 接收无话权请求

适用条件：客户端收到私呼或first-to-answer的初始INVITE，且SDP不含media-floor control entity媒体级部分。

识别为无话权控制业务，按§11.1.1.2.1.2或§11.1.1.2.2.2进入对应按需或预建立接收流程；这不意味着跳过接听检查。

依据：§11.1.2.2。

## 参与功能的两种识别入口

适用条件：参与功能收到私呼或first-to-answer请求。

主叫侧按需INVITE的SDP不含media plane control messages媒体级部分时，使用§11.1.1.3.1.1。预建立REFER则检查SDP媒体控制部分fmtp中的mc_no_floor_ctrl，使用§11.1.1.3.1.2。被叫侧INVITE不含media-floor control entity媒体级部分时，使用§11.1.1.3.2；不能把三处检测写成同一个字符串判断。

依据：§11.1.2.3.1–11.1.2.3.2。

## 控制功能继续复用授权和路由

适用条件：控制功能处理无话权控制私呼或first-to-answer。

发起侧沿§11.1.1.4.1。接收对应INVITE且SDP不含media-floor control entity媒体级部分时，识别为无话权控制业务并沿§11.1.1.4.2；无话权控制不等于没有用户授权或目标选择。

依据：§11.1.2.4.1–11.1.2.4.2。

## 证据边界

- 预建立客户端SDP有§11.1.2.2步骤8c(i)/9a的专门改写及端到端安全条件，本页未展开，不能仅套按需SDP差异。
- mc_no_floor_ctrl的具体媒体语义依赖24.380§14，尚未在本页核验。

## 按需继续

- [originating-authorization](originating-authorization.md)
- [terminating-authorization](terminating-authorization.md)
- [control-routing-results](control-routing-results.md)
- [release-signalling](release-signalling.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页462、463；仅本版本。
