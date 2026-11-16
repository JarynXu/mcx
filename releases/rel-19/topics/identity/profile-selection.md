# 用户配置切换：预选下次生效，活动配置可能断呼

TS23.280 V19.9.0 Stage2；区分CMS中的pre-selected配置与某个MC服务客户端当前selected配置。

## 预选仅改变下次授权的选择

适用条件：用户已认证、UE安全访问CMS、已取得一个或多个用户配置，并触发预选变更。

配置管理客户端将MC service ID和profile index提交CMS，CMS先检查更新授权；之后保存选择与返回确认可任意顺序或并行。接收服务期间改变预选不会改变当前活动配置，变更在下一次MC服务授权时应用。每UE单独指定预选不在此规范范围内。

依据：§10.1.4.6。

## 活动切换针对单个服务客户端

适用条件：用户已认证、UE安全访问MC服务服务器、已取得多个用户配置并完成该服务授权，触发活动配置选择。

MC服务客户端向MC服务服务器提交用户ID和选中index；服务器按需取得用户配置，并保存该客户端的活动index。同一用户不同客户端可以使用不同活动配置，不把它误写成全用户统一切换。

依据：§10.1.4.7。

## 确认不保证组资料已经全部到齐

适用条件：切换选中配置且服务器或客户端缺少所需组配置。

服务器和客户端分别按需取得对应组配置并订阅更新。服务器取得组配置与确认选择可以任意顺序或并行，因此活动配置确认不能单独证明所有组配置下载完成。

依据：§10.1.4.7 steps 4–6。

## 成功协商后清理旧活动状态

适用条件：MC服务服务器和UE成功协商selected用户配置。

在本次单服务客户端选择范围内，双方依据新选中配置清理此前selected或pre-selected配置留下的活动服务状态，包括相关组取消归属和MC服务呼叫断开，并处理新配置所需归属。因此活动配置切换不能作为不中断通话的透明偏好设置。

依据：§10.1.4.7 final paragraph。

## 证据边界

- 只核所列Stage2流程；TS29.283接口、各MC服务呼叫释放与归属报文未核。
- 表10.1.4.2.8-1使用authentication措辞，而过程10.1.4.6明确next service authorization；本页以过程的生效条件表述，不将两者混成同一个过程。

## 按需继续

- [primary-registration](primary-registration.md)
- [service-authorization](service-authorization.md)
- [migration-authorization](migration-authorization.md)
- [../groups/document-access](../groups/document-access.md)

[ETSI官方TS23.280 V19.9.0](https://www.etsi.org/deliver/etsi_ts/123200_123299/123280/19.09.00_60/ts_123280v190900p.pdf)，印刷页87、92、93、94、95；仅本版本。

配置数据另见：[获取](profile-acquisition.md)、[更新](profile-update.md)。
