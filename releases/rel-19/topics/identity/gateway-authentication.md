# MC网关接入：网络认证不替代客户端授权

TS33.180 V19.4.0 §5.12.1；non-3GPP设备通过MC gateway UE访问MC服务，MC客户端可驻留在任一侧。

## 两层认证

适用条件：经MC gateway UE接入MC服务。

网关UE先完成3GPP网络设备认证以取得网络连接和路由；无论MC客户端在网关还是non-3GPP设备，每个客户端仍须按§5.1完成MC认证与授权。网络接入成功不能替代MC服务授权。

依据：§5.12.1。

## 本地链路的规范边界

适用条件：建立non-3GPP设备与网关之间的连接。

这段连接可以早于网关网络认证建立；其协议和安全不在此3GPP规范范围内。客户端驻留网关时，设备到客户端的数据传输保护同样不由本条保证。

依据：§5.12.1 steps 1–2。

## 转发和最终权限

适用条件：MC客户端驻留non-3GPP设备。

网关原样转发客户端与MC系统之间的认证授权消息。客户端授权成功后，实际服务访问仍受IdMS取得的access token及CMS用户配置限制，不能从网关身份推导所有下挂设备的无限权限。

依据：§5.12.1 step 3。

## 证据边界

- TS33.501设备认证细节和本地链路实现未核；不据此推荐免认证本地网络。
- MC gateway UE不等于媒体保护中代终端解密的MC Security Gateway，两者角色不能混用。

## 按需继续

- [native-authentication](native-authentication.md)
- [service-authorization](service-authorization.md)
- [../security/access-transport](../security/access-transport.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，§5.12.1，印刷页65–66。
