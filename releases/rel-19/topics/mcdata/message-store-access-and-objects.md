# Message Store 访问：身份、对象查询与结果范围

只适用TS24.282V19.7.0第21章Message Store及其明确引用的操作；不把所有对象等同于一个文件。

message store client、MCData server、message store function、message notification client与notification server是不同功能角色。相同HTTP动词不表示它们用相同身份。

仅按已核条款描述成功前提和响应；未读OMA资源模式、24.482/24.484依赖全文，不补缺失的URI、schema、默认值或错误码。

## 客户端访问先验证令牌

适用条件：消息存储客户端访问message store function，或消息通知客户端访问notification server。

这两类客户端连接使用HTTP over TLS，请求携带MCData access token的Bearer Authorization，服务器须验证token。Message Store主机名来自用户profile，notification server主机名来自服务配置。MCData ID位于token中，也可用于URL的userId变量；在URL中写入一个用户ID本身不替代token验证。

- token获取、验证细节、TLS配置及验证失败码仍依赖外部规范；本条不统一补成403。
- 配置来源的区别不等于客户端可任意指定可信主机，完整配置发现与信任建立不在本页。

依据：§21.1 client interfaces and NOTES1;21.2.1.1/.2;21.2.19.1/.2，印刷页 454、455、456、467。

## 服务器存入与用户存储区分开

适用条件：MCData server向Message Store存入某用户的对象；或Message Store向notification server推送变更。

§21.1把MCData-8和MCData-11的认证/授权交给TS33.180，不能照搬上述客户端接口的全部规则。deposit过程由MCData server充当HTTP客户端：资源URL的boxId取所属用户MCData ID，同时携带按33.180的有效access token；Message Store验证该token后才处理存入。boxId说明对象的用户存储位置，不等于HTTP调用者就是该用户客户端。

- 本页没有重读33.180服务器token规则，不推断token内容、scope或授权获得方式。
- 不会因请求URL含某用户ID，就宣称请求者有权读写该用户全部对象。

依据：§21.1 NOTE1A and MCData-8/MCData-11 security paragraph;21.2.5A.1/.2，印刷页 455、458、459。

## 对象结果不证明文件取得

适用条件：客户端请求单个存储对象或按SelectionCriteria搜索对象；相应token验证成功。

单对象获取使用HTTP GET，Request-URI标识Message Store资源；对象找到时由HTTP响应返回。对象搜索则使用含SelectionCriteria的POST，响应包含符合条件的对象。两种操作都先验证访问token再处理。它们返回的是对象/查询结果；对于payloadPart仍指向内容服务器文件的对象，得到对象不能独立证明文件字节已迁入Message Store，更不能证明已下载到用户设备。

- 对象结构、搜索匹配、分页和一般响应状态由OMA依赖定义，本页不补完整JSON或HTTP状态表。
- 本条没有断言所有对象都只含元数据，或对象响应永远不能包含任何内容；只限制从对象获取推断外部文件取得。

依据：§21.2.1.1/.2;21.2.2.1/.2;21.2.24.2，印刷页 455、456、471。

## 证据边界

- 不涵盖全部对象CRUD、文件夹权限或存储启停授权。

## 按需继续

- [message-store-file-locality](message-store-file-locality.md)
- [message-store-notification-sync](message-store-notification-sync.md)
- [fd-http-file-and-signalling-evidence](fd-http-file-and-signalling-evidence.md)
- [../identity/http-sender-identity](../identity/http-sender-identity.md)
- [../identity/http-transport-endpoints](../identity/http-transport-endpoints.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
