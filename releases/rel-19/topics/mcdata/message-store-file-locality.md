# 对象与文件落点：存入、迁存和重复请求

限Message Store中有关联文件的对象；payloadPart URL/href用于定位文件，objectId用于定位存储对象。

locally在这些条款中指存入MCData Message Store，不是下载到用户终端，也不是FD发送者已收到COMPLETED通知。

每个调用须满足其角色的认证与处理前提；有URL不代表后续获取必然获准或文件始终存在。

## 缺省retrieveFile要求获取

适用条件：MCData server存入带关联文件的对象，Message Store token验证成功。

deposit可带retrieveFile查询参数：No表示这次不要求从内容服务器获取文件，Yes表示要求获取并存入Message Store。参数缺失与Yes等效。对Yes或缺失分支，Message Store须按请求body中对象的payloadPart URL获取文件，存入该用户存储区，并更新对象的payloadPart URL。对象存入与文件落点因这个参数而不同，不能把缺省误写成仅保存远程链接。

- No只限定此次deposit的获取要求，不意味着文件永远不能在后续迁存。
- 存入结果响应依赖OMA过程；本条不编造首次获取失败后的事务回滚、重试或HTTP状态码。

依据：§21.2.5A.1 step1d and NOTE;21.2.5A.2 steps1–3，印刷页 458、459。

## retrieve存入服务器而非终端

适用条件：消息存储客户端要求Message Store取得某objectId关联的文件，发送已认证的对象retrieve POST。

§21.2.24把retrieve定义为已有对象上的自定义POST操作，地址以objects/{objectId}/retrieve结尾，请求使用Empty数据结构。Message Store按objectId找到对象后，只有payloadPart的href指向MCData content server文件时才按§6.7获取；文件确实从内容服务器取得后才本地保存并把href改为本地文件地址。这是在服务端改变对象所指文件的落点，不是用户终端GET文件的动作。

- 不把任意外部URL都纳入这一抓取分支，也不在没有成功取得文件时宣称已更新本地地址。
- 完整URI变量展开、对象/Empty的schema和其他HTTP结果依赖OMA及29.501，未在本页展开。

依据：§21.2.24.1;21.2.24.2 steps1,2，印刷页 470、471。

## 服务器间文件获取也须授权

适用条件：Message Store按§21.2.24.2调用§6.7获取内容服务器文件。

§6.7.2的网络HTTP客户端用文件绝对URL发送GET，并携有效access token。文件服务器验证token；运营者策略不允许下载时返回403，文件不可供下载时返回404。客户端收到包含所请求文件的HTTP200后才保存以供后续处理。因此上游对象操作获准或持有href，都不能替代这次服务器间文件获取。

- 403和404只对应这里明确列出的策略/不可下载条件，不泛化成所有token或网络错误。
- 文件传输的token内部验证、代理、断点续传、解密和完整性实现未核。

依据：§21.2.24.2 step2a(ii);6.7.2.1;6.7.2.2，印刷页 134、135、471。

## 重复200与变更通知条件不同

适用条件：Message Store处理对象retrieve请求；区分href原本已指本地文件与本次获取后href发生变化。

href已经指向Message Store本地文件时，无需再次从内容服务器获取，须返回包含Object的HTTP200；原文说明这样支持重试或重复请求。若对象因href变化而更新，且有客户端订阅了对应事件，才发changedObject通知。由此，200可以是“文件原本已在本地”，并不证明本次重新搬运；未发changedObject也不能单独推出操作失败。

- 本条没有给首次成功迁存统一指定另一个状态码；其一般响应仍按OMA引用。
- 这里的changedObject是存储对象变更事件，不是接收用户下载完成、送达或已读的业务回执。

依据：§21.2.24.2 step3a,3b and NOTE;21.2.12A;21.2.16，印刷页 462、465、471、472。

## 证据边界

- 未覆盖对象删除与文件物理删除联动、存储寿命、配额、并发更新和失败恢复算法。

## 按需继续

- [message-store-access-and-objects](message-store-access-and-objects.md)
- [message-store-notification-sync](message-store-notification-sync.md)
- [fd-http-file-and-signalling-evidence](fd-http-file-and-signalling-evidence.md)
- [../identity/http-sender-identity](../identity/http-sender-identity.md)
- [../identity/http-transport-endpoints](../identity/http-transport-endpoints.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
