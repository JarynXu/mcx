# 媒体面FD：授权参与用户请求无预告释放

TS24.282 V19.7.0 §13.2.5.2明确包含已建立的媒体面FD，并给出授权客户端、PF和CF过程。用户通过INFO请求CF授权并终止通信，不是凭自己参与通信就能宣布全组已释放。

## 共同条件

- 固定TS24.282 V19.7.0 Rel19 Stage3；已建立的普通在网媒体面FD，直接one-to-one或预安排组，相关SIP对话存在。只取其他已参与的授权用户要求无预告释放的§13.2.5.2入口。
- HTTP FD、SDS、IPCONN、ad hoc、预告延期、紧急和跨域不在本页；不把用户自行离开或服务器主动策略触发替代授权释放请求。
- 各角色与事件分别适用其条件；请求客户端的意图不等于CF授权成功。身份、安全、配置及SIP对话的外部依赖仍须满足，未提供这些依赖的完整实现。

## 授权者请求与PF转送，不是自行离开的BYE

各角色分别判断独立入口，不要求事件同时发生：授权用户要求不预告原发起者而释放已建立媒体FD时，适用客户端发送；PF在本通信dialog内收到带指定Info-Package的客户端INFO时，适用转送；PF收到该INFO的CF200或403、客户端实际收到PF对应响应时，分别适用该响应处理。

§13.2.5.2.1明确包含已用媒体面建立的FD。授权客户端生成dialog内SIP INFO，Info-Package为g.3gpp.mcdata-com-release，关联application/vnd.3gpp.mcdata-signalling承载COMMUNICATION RELEASE，Content-Disposition为Info-Package，Comm Release Information type设AUTH USER RELEASE REQ；另在mcdata-info XML写授权客户端自身mcdata-client-id，可带Reason，发向PF。PF SHOULD调用§13.2.4.3.2；采用该helper时生成INFO、复制Info-Package和MIME并在本通信dialog内向CF发送。PF收到CF200后生成对应200回客户端；收到CF403时，§13.2.5.2.3.1明确要求生成403回客户端。客户端实际收到PF200或403时，SHOULD分别告知授权用户请求被接受或拒绝。

- 用户属于正在通信的参与者在§13.2.5.1为SHOULD；本页选择已参与者，不把它升级为CF必做的成员检查，也不推导外部管理员默认授权。
- PF helper只显式复制包和MIME，没有明确INFO Reason复制；授权者可选Reason不能据此保证逐跳保真。
- INFO200是请求被接受的反馈，不是全部BYE或全部媒体资源释放的证明。未核其它响应、超时与重传替代路径。

规范强度：客户端报文动作SHALL，Reason MAY；PF调用helper及客户端用户提示SHOULD，采用helper后的列明动作SHALL。

依据：§13.2.5.1;13.2.5.2.1;13.2.5.2.2.1;13.2.5.2.3.1;13.2.4.3.2，印刷页338,339,340,334。

## CF验证授权后调用释放，不能借成员身份跳过检查

CF实际收到本通信dialog内INFO，Info-Package为g.3gpp.mcdata-com-release且关联mcdata-signalling MIME；解码后为COMMUNICATION RELEASE、类型AUTH USER RELEASE REQ。授权失败与成功分别判断；BYE及后续响应动作仅在对应helper实际执行和响应实际收到时适用。

CF根据配置验证请求用户是否获授权；失败生成403向PF发送并停止后续步骤。成功生成并发送200，随后SHALL执行§13.2.3.2.4来终止正在进行的通信。这一授权入口明确调用服务器释放过程，不要求再用“服务器主动释放”作为用户请求的替代触发。被调§13.2.3.2.4对§13.2.2.2.4.4的调用为SHOULD，并SHALL附适当Reason文本。采用BYE helper时，CF先与24.582媒体面交互释放，再生成并发送BYE；若整个组通信需要释放，则向该通信全部参与者发送BYE，不能换成全部静态或affiliated成员。CF实际收到对应BYE200后，释放与终止PF段相应的媒体资源。

- §13.2.5.2.4.1成功200目的地字面写MCData server，而失败指向PF且PF过程列CF200接收；保留此差异，不据此宣称响应路由完整验证。
- 用户配置权限与客户端自行声明client-id不同；用户、client-id和dialog间完整身份绑定算法未在本页建立。
- 外层SHALL调用与内层SHOULD调用不可压成无条件SHALL BYE。Reason例子不是必须沿用的统一cause或固定文本。
- 仅核信令入口、条件调用及CF端证据；24.582具体媒体停止动作、所有PF/客户端资源收尾及跨段同步没有因此全部闭合。没有把此过程解释为HTTP FILE DELETED、存储物理删除、已下载副本撤回或文件成功交付。

规范强度：CF授权验证、403/200处理和调用13.2.3.2.4为SHALL；该wrapper调用BYE helper为SHOULD，Reason为SHALL；采用helper时内部动作仍按SHALL。

依据：§13.2.5.2.4.1;13.2.3.2.4;13.2.2.2.4.4，印刷页340,331,329。

## 结果和相邻问题

本页建立媒体FD授权无预告释放的信令责任，不证明完整媒体停止、全员收尾或文件删除。服务器主动触发另见[媒体FD服务器释放](media-fd-server-release.md)；[SDS授权释放](authorized-user-media-release.md)与[HTTP授权释放](authorized-user-http-release.md)各有自己的适用条件，不互相替代。

[官方固定版本](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)。
