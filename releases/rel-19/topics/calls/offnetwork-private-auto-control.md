# 离网MCPTT自动私呼：建立、终接等待与两种控制状态

固定ETSI TS124379 V19.4.0，对应3GPP TS24.379 V19.4.0 Release19 Stage3；仅两个已确定用户之间的普通离网自动应答私呼，类型PRIVATE CALL，发起端关联紧急状态为false。不含手动应答、紧急、组呼或在网SIP。

目标身份、承载及必要配置已具备，发现/授权取得不在此补齐。基本控制每MCPTT user ID一个状态机，并发受MaxCallN10限制。只核成功建立与列明验签失败分支；重传、媒体不可建拒绝、取消及释放完整链未覆盖。

消息按§11.2.1.1.1的MONP传输依赖处理。该条发送写用户local IP、UDP8809及TTL255；接收句却写port TBD和8809 messages，不能用MCVideo或组呼文字静默修复。TS24.380 §7.2仅为接口依赖，不从旧版本组话权页推定私呼内部许可完整。

各角色只在本节条件满足时执行列出的规范动作。

## 自动模式由发起授权和模式配置共同限定

发起MCPTT客户端P0或P1，用户要求普通私呼；Common/PrivateCall/Authorised=true，用户请求自动模式且AutoCommence=true。

发起端均匀随机生成并保存call identifier，原文字面范围为(0,65536)；保存自身caller ID、目标callee ID及AUTOMATIC COMMENCEMENT MODE，并创建独立call-type控制状态机。若需建立端到端安全上下文，先执行本条PCK/PCK-ID、面向被叫UID的封装及签名I_MESSAGE步骤，包含对§6.2.8.3.9确定被叫MCPTT ID/KMS URI的依赖。随后生成并保存offer SDP，SETUP REQUEST携call identifier、双方ID、模式、类型机当前类型及offer，按§11.2.1.1.1发送；CFP1置1、启动TFP1，若原在P1则停止TFP7，再进入P2。

可保存本地位置，但本条发送User location IE的MAY条件限定EMERGENCY PRIVATE CALL；不能将普通私呼也写成可直接携带位置。 不裁定随机区间端点包含性。安全算法、KMS定位及配置默认值未展开，未满足本条自动模式条件不能按本条自动发起。

依据：TS24.379 V19.4.0 §11.2.2.4.2.1，印刷页515,516。

## 终接接受不等于已经进入P4

终接MCPTT客户端P0或P1，收到AUTOMATIC COMMENCEMENT MODE的SETUP REQUEST，call identifier不同于所存值且offer声明的媒体能建立；分别处理无a=key-mgmt属性或含mikey值的MIKEY-SAKKE I_MESSAGE，其他属性格式不覆盖。

终接端保存call identifier，创建call-type状态机，保存请求中的caller ID及自己的callee ID。指定I_MESSAGE路径先提取IDRi中的发起MCPTT ID、转为UID并验证签名；失败时用所存call identifier及双方ID发REJECT，Reason仅在请求限制失败通知且FailRestrict=true时为FAILED，否则为E2E SECURITY CONTEXT FAILURE；释放call-type状态机并保持原状态。验签成功且解封PCK、提取PCK-ID后，或offer完全无a=key-mgmt属性时，生成并保存answer SDP，发送携所存call identifier、双方ID及answer的ACCEPT，按answer建立媒体，CFP4置1、启动TFP4；若原在P1则停止TFP7，再进入P5。

验签失败走REJECT并释放call-type状态机的分支，不进入验签成功或无a=key-mgmt属性的接受路径。 P5概述称等待用户，但此自动分支已发ACCEPT后仍进P5；不推定还须点击接受。媒体不能建立的§11.2.2.4.3.1另有入口，本主题不展开其拒绝链。

依据：TS24.379 V19.4.0 §11.2.2.4.3.2，印刷页519,520,521。

## 两端基本控制分别由ACCEPT和ACK或RTP完成

分别观察发起客户端P2收到回应SETUP REQUEST且call identifier相同的PRIVATE CALL ACCEPT，或已发送ACCEPT的自动终接客户端P5收到发起用户的PRIVATE CALL ACCEPT ACK或RTP媒体。

发起端保存answer SDP，发送携所存call identifier及双方ID的ACCEPT ACK，停止运行中的TFP1和TFP9，按answer建立媒体，以originating floor participant调用TS24.380 §7.2启动floor control，再启动TFP5并进P4。终接端的ACK或RTP是替代触发：停止TFP4，以terminating MCPTT client调用TS24.380 §7.2启动floor control，启动TFP5并进P4。

终接完成入口没有另列call-id相等校验，不擅自补为本条要求；完整分派和鉴权未核，不能据此认定任意ACK有效。 发起侧是originating floor participant，不能搬用MCVideo的角色文字；TFP9也不改成Video的TFP2。调用floor control不证明已获发声许可或声音送达。

依据：TS24.379 V19.4.0 §11.2.2.4.2.8;11.2.2.4.3.4，印刷页517,518,521。

## 普通类型由独立Q状态机保存和确认

分别观察类型机Q0中用户发起普通私呼且关联emergency alert的stored emergency state=false；或空闲客户端Q0收到Call type=PRIVATE CALL的SETUP REQUEST；或Q0收到ACCEPT/ACCEPT ACK且所存类型为PRIVATE CALL。

发起普通分支和接收入站普通分支各自将current call type置PRIVATE CALL，并设置普通离网私呼ProSe per-packet priority。Q0收到ACCEPT或ACCEPT ACK且已存PRIVATE CALL时，进入Q1。类型控制与基本呼叫控制并行存在：基本终接P5可因RTP进入P4，而此Q0完成条款只列ACCEPT或ACCEPT ACK，不列RTP。因此不能仅凭基本控制进P4就断言类型机也已进Q1。

各状态机按自己的事件和条件处理，不造原子转换或跨状态机调度顺序。紧急状态true但未获紧急授权的缺省分支不在此补齐。 ProSe具体数值及配置取得未核；普通类型状态也不等同话权许可。

依据：TS24.379 V19.4.0 §11.2.3.1;11.2.3.4.2;11.2.3.4.3;11.2.3.4.4，印刷页528,529,530,531。

## 范围与来源

传输和状态机背景见§11.2.1.1.1（p513）、§11.2.2.1–.3（pp514–515）。[在网模式选择](commencement-selection.md)与[在网被叫应答](private-client-acceptance.md)是不同场景，不能替换本页MONP和P/Q控制。

来源：[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。内部话权、安全和完整媒体行为未核。
