# 组文档变更订阅：订阅者、资源与 SIP 地址

适用：Rel19，TS24.481 V19.3.0，Stage3。这里解释 GMC 初始订阅的资源和地址，不是一份可独立实现的完整 SIP 请求模板。

## 先区分订阅者

GMC 可订阅一个或多个组文档、GKTP 文档的 `<GKTPs>` 元素，或两者。MCS server 的此项流程订阅组文档；拥有临时组组成组的 GMS 还有单独的订阅者流程。不能把 GMC 的所有分支照搬给 MCS server（§6.3.13.1）。

## SIP 目的地与资源条目不是同一地址

GMC 初始 SIP SUBSCRIBE 的 Request-URI 是所配置的 GMS 订阅代理公共服务标识。资源列表使用 `application/resource-lists+xml`，每个资源一个 entry；其 uri 为相对于 GMC 配置的 XCAP root 的路径引用：组文档按组 ID 寻址，GKTP 资源还须以 node selector 指到 `<GKTPs>`（§6.3.13.2.1 a/b）。不能把资源列表里的 HTTP/XCAP 目标直接当作 SIP Request-URI。

GMC 在 mcptt-info MIME body 中带认证取得的 access token；要求身份隐藏时，还必须对 mcptt-info 和 resource-lists 两个 MIME body 执行所引的保密性、完整性保护，并带包含 CSK 的 MIKEY body（同节 c/d）。组管理本身不依赖具体 MC 业务，出现 MCPTT 命名元素是历史原因，不能据此判定只支持 MCPTT（§6.3.13.1）。

资源列表变化采用 SIP re-SUBSCRIBE，带修改后的资源条目；它与最初订阅有各自规定，不应简单复制初始消息全部内容（§6.3.13.2.1）。

## 依赖边界

完整处理还涉及本节服务标识/Contact 要求，以及 TS24.229、RFC5875；access token 获取和身份隐藏保护分别引用 TS24.482、TS24.379，本页未核验这些依赖，不提供认证或加密实现。代理授权和 NOTIFY 内容处理也未在此页展开。

[读取权限](document-access.md) · [跨服务商文档转发](forwarding.md) · [来源](https://www.etsi.org/deliver/etsi_ts/124400_124499/124481/19.03.00_60/ts_124481v190300p.pdf)，印刷页20–22。

后续列表变化和通知处理见[更新订阅](subscription-refresh.md)；若实际调用者是[MCS服务器](server-subscription.md)或[组成组GMS](constituent-subscription.md)，应使用各自请求构造，不照抄GMC身份模板。

进一步核对：[代理和拥有方授权](subscription-proxy.md)、[未知扩展处理](unknown-extensions.md)。
