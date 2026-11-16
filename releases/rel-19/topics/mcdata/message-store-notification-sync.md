# Message Store 同步：订阅、通知通道与变更结果

限第21章的Message Store变更同步；这里的notification不是第12章SDS/FD disposition。

创建订阅、创建通道和接收通知分别有自己的调用与认证前提。成功完成其中一步不等于其他步骤已完成。

OMA定义的资源结构、通道内部行为、游标和恢复算法未在本页读取；只保留24.282明确规定的选择与结果。

## 通道与订阅分别创建

适用条件：客户端选择经MCData notification server接收Message Store变更，而不是让Message Store直接回调客户端。

消息通知客户端先向notification server创建通道；成功响应含Callback URL，并可能依channelType包含Channel URL。消息存储客户端随后把Callback URL用于向Message Store创建变更订阅，两个POST面向不同服务并分别验证MCData token。Callback URL供Message Store推送变更，Channel URL供通知客户端按通道类型接收，不能将它们互换或把通道创建成功当成订阅已存在。

- 不强制所有通道类型都返回Channel URL；依据创建结果和channelType处理。
- 本页不制定订阅过滤器、期限、续订和通道删除策略。

依据：§21.1 MCData-11 paragraph;21.2.19.1/.2 and NOTES1,2;21.2.12A.1/.2;21.2.22.1，印刷页 455、462、467、469。

## Callback决定通知路径

适用条件：Message Store要通知已订阅的变更，使用对应订阅创建时提供的Callback URL。

Message Store以POST向Callback URL送出通知。URL指向消息存储客户端时，客户端作为HTTP服务器处理该请求，随后采用两种同步方式之一：依据通知内容、restartToken和index更新本地库，或把通知当作随后查询变更的触发。URL指向notification server时，该服务器处理POST，再通过此前创建、按需打开的关联通道让客户端取得通知。这是两条路径，不能假设任何客户端都直接接受服务器HTTP回调。

- 服务器间MCData-11认证/授权见§21.1的33.180引用；不把客户端Bearer流程未经核验复制成此接口全貌。
- “通知可取得”不等于客户端已处理全部变更，也不等于文件内容已下载。

依据：§21.2.16.1;21.2.16.2;21.2.16.3，印刷页 465、466。

## 不同通道分别打开

适用条件：通知通道已创建，客户端按返回的channelType决定是否及如何打开它。

LongPolling使用Channel URL发送含有效MCData token的POST；notification server验证成功并处理后，成功响应包含存储变更通知。WebSocket类型通过Channel URL建立WebSocket连接，这个建立过程不是RESTful。NativeChannel不要求执行本节Open notification channel过程。因此不能把“打开通道”统一实现为一个GET、POST或WebSocket动作。

- WebSocket握手、NativeChannel交付以及LongPolling超时/重试依赖OMA，未在本页核验。
- 创建通道的成功响应与一次LongPolling成功返回通知是不同操作结果。

依据：§21.2.22.1;21.2.22.2，印刷页 469、470。

## 同步对象不等于业务送达

适用条件：客户端已收到存储变更通知，选择用其更新本地对象状态，或另行搜索变更。

直接回调路径及LongPolling接收路径均给出两条同步路径：用通知内容、restartToken和index更新本地库，或再按§21.2.17搜索。搜索分别用CreatedObjects、VanishedObjects或Flag取得新建、消失对象及标志变更；CreatedObjects响应须含creationCursor。变更通知和列表描述的是存储对象状态，不能单凭它们认定对象关联文件已在终端，或原SDS/FD已送达、已读。

- 不要求所有搜索类型都返回creationCursor，也不自行定义restartToken/index与creationCursor的互换规则。
- 本页未核去重、丢通知恢复和全量同步收敛算法，不把一次查询成功当成全库同步完成。

依据：§21.2.16.2;21.2.22.1 PULL response handling;21.2.17.1/.2;21.2.2.1/.2，印刷页 456、465、466、469。

## 证据边界

- 不展开所有订阅更新/删除过程、通道生命周期与OMA完整同步协议。

## 按需继续

- [message-store-access-and-objects](message-store-access-and-objects.md)
- [message-store-file-locality](message-store-file-locality.md)
- [fd-http-file-and-signalling-evidence](fd-http-file-and-signalling-evidence.md)
- [../identity/http-sender-identity](../identity/http-sender-identity.md)
- [../identity/http-transport-endpoints](../identity/http-transport-endpoints.md)

[3GPP TS 24.282 V19.7.0 / ETSI TS 124 282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§21.2.12A.2 opening：服务器段回指21.2.12.1，但现行创建订阅客户端段为21.2.12A.1，21.2.12为Void。 记录回指差异，以明确的创建订阅客户端/服务器过程为本页范围，不凭旧编号补另一流程。
