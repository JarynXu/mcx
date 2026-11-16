# 主 MC 系统：用户认证与 SIP 注册的关系

适用：Release 19，TS23.280 **V19.9.0**，Stage2。此版本独立核对，不替代库内其他版本。

用户认证与 SIP 注册不能画成一条必定先认证、后注册的固定顺序。§10.6.1 的主系统示例允许认证发生在注册之前或之后，也允许将认证并入注册阶段。信令 UA 仍建立安全连接，以进行 SIP 层认证与注册；顺序可变不表示省略 SIP 认证。一次认证可用于多个 MC 服务的授权，各服务仍需相应授权。

SIP 层注册完成时，向 MC 服务服务器的第三方注册是可选的。若位置来自 PLMN 的 LCS，该第三方注册期间需共享 UE IMSI；第三方注册还需按条款携带 UE 的 L4S 能力。此处不是授权任意向第三方披露 IMSI，也不代表所有位置来源都要此字段。

具体认证与令牌机制依赖 TS33.180；此页未核 Stage3 REGISTER 编码。

## 依据与延伸

[ETSI 正式文本](https://www.etsi.org/deliver/etsi_ts/123200_123299/123280/19.09.00_60/ts_123280v190900p.pdf)；精确条款与适用条件见[知识记录](primary-registration.json)。未核完整引用规范或实现。

- [Stage1 应用身份与授权范围](authentication-boundary.md)
- [EPS 接入和信令 QoS](../network-policy/eps-signalling.md)
- [注册器定位与用户绑定](../signalling/registrar-routing.md)

迁往伙伴系统时另读[双方授权与重定向门槛](migration-authorization.md)，不能把主系统注册成功当作伙伴服务已获授权。

TS33.180 V19.4.0补充：[无令牌初始注册与服务授权](service-authorization.md)。本页仍只代表TS23.280 V19.9.0的高层流程。

- [profile-selection](profile-selection.md)
