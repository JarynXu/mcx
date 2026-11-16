# 组订阅代理：用户、服务器与组成组身份

TS24.481 V19.3.0 Stage3；xcap-diff订阅须区分代理GMS和拥有目标组的GMS。下面只处理所列分支，不是完整SIP状态机。

## 用户路径以令牌中的MCS ID授权

适用条件：初始SUBSCRIBE到代理身份，包含xcap-diff、资源列表、带token的mcptt-info及规定服务标识，PAI不在授权MCS服务器和GMS列表。

代理在规定EncryptedData与CSK条件下解密body，从token取得发起MCS ID用于授权。资源列表中任一资源无订阅权限则403停止；不是仅按SIP传输身份放行，也不是丢掉无权资源后接受其余项。

依据：§6.3.13.3.2.2。

## 跨域订阅传递原始用户身份

适用条件：GMC订阅资源属于其他MCS提供方。

代理针对相应组另建订阅，以自身文档访问身份作PAI，并在mcptt-calling-user-id携带发起用户MCS ID，Request-URI取路由库中的对方文档访问身份。它把收到的NOTIFY信息纳入客户端订阅的通知，不把代理自身身份替换为业务用户。

依据：§6.3.13.3.2.2; 6.3.13.3.2.4。

## 组拥有方仍检查代表谁订阅

适用条件：初始订阅到组拥有方文档访问身份，PAI属于授权GMS，且满足规定事件、MIME和服务标识条件。

若带calling-user-id，按该用户身份检查资源权限；若带calling-group-id，按PAI检查GMS权限并识别其代表的组。任一目标无权限则403；组成组分支若订阅目标不关联该临时组ID，也403停止。信任代理GMS不等于信任任意订阅目标。

依据：§6.3.13.3.3。

## 服务器续订不能照搬用户路径

适用条件：MCS服务器路径，初始PAI在授权MCS服务器列表且满足规定请求条件。

初始请求由代理作为notifier处理；续订时以PAI为认证身份检查所列文档或元素权限，任一无权则403停止。不得从GMC续订条款的简写推导所有类型续订都免授权。

依据：§6.3.13.3.2.3。

## 证据边界

- 未核TS24.229/24.482的身份信任与令牌验证细节；这里的条件不是可绕过认证的头字段模板。
- 跨域GKTP相对URI的base在§6.3.13.3.2.4与组成组订阅§6.3.13.2.3措辞不同；本页不统一改写为相同路由算法。
- RFC5875的状态、过期、合并和失败处理未完整核验。

## 按需继续

- [change-subscription](change-subscription.md)
- [subscription-refresh](subscription-refresh.md)
- [constituent-subscription](constituent-subscription.md)
- [gktp-access](gktp-access.md)
- [document-access](document-access.md)

[ETSI官方TS24.481 V19.3.0](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)，印刷页25、26、27、28；仅本版本。
