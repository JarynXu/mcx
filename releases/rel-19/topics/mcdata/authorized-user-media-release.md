# MCData 授权参与用户释放：媒体请求与服务器准入

TS24.282 V19.7.0 §13.2.5.1/.2，无预告释放已有媒体通信。本文选普通在网直接私聊/预安排组 SDS session；原条款同时列媒体 FD 和 IPCONN，但本页不核其建立与全部媒体行为。

授权释放发起者与原通信发起者是不同角色；本页考察已参与通信的其他授权用户。§13.2.5.1 写用户 SHOULD 属于正在进行的通信，不将其改成服务器必做的硬性成员检查，也不从中推导任意外部管理员均有权释放。

客户端用户请求与 CF 根据配置验证权限分别成立。INFO 入口依赖对应 SIP dialog、Info-Package 与关联 MIME；外部配置和 SIP/媒体实现按依赖定位，不据此补本版未列步骤。

## 参与用户的授权释放请求

适用条件：已参与 ongoing 通信的授权用户要求不预告原发起者而释放；客户端进入 §13.2.5.2.2.1。

客户端在该通信的 SIP dialog 内向 PF 发 INFO，Info-Package 为 g.3gpp.mcdata-com-release，以关联 mcdata-signalling MIME 承载 COMMUNICATION RELEASE，并设 Content-Disposition=Info-Package。Comm Release Information type 必须是 AUTH USER RELEASE REQ；mcdata-info XML 携带授权客户端自己的 mcdata-client-id，Reason 可带。这是请求服务器终止通信，不能用用户自行退出时发送的 BYE 代替，也不能仅凭 client-id 声称自己有权。

- 同对话本身不能替代包、关联 MIME 和 AUTH USER RELEASE REQ 类型条件。
- 权限是后续 CF 依据配置验证的条件；本节未列可据其自行创建的“管理员”默认角色，也未给不参与者如何取得此对话。

依据：§13.2.5.1;13.2.5.2.1/.2.1;15.2.20;13.2.2.2.2.1，印刷页 327、338、339、371。

## CF授权检查与释放调用

适用条件：CF 收到对应通信 dialog 内的 INFO，包为 g.3gpp.mcdata-com-release，关联 mcdata-signalling 中为 COMMUNICATION RELEASE 且类型 AUTH USER RELEASE REQ。

CF 按配置验证发出释放请求的 MCData 用户。验证失败须回403并停止后续步骤；成功则先回200，再调用 §13.2.3.2.4 终止 ongoing 通信。它没有把“用户是参与者”或“客户端已发合法格式”当成授权通过，也没有把原通信发起者的许可自动转给释放发起者。

- §13.2.5.2.4.1 step4b 对200目的地写 toward MCData server，失败分支及 PF 响应过程写向 PF；保留字面差异，不宣称完整响应路由已验证。
- 本节按配置验证授权，但未在这里给出用户身份与客户端ID/对话绑定的完整验证算法；不能把客户端声明的 client-id 当作独立授权凭据。
- 被调 §13.2.3.2.4 对 BYE helper 的调用是 SHOULD，附适当 Reason 是 SHALL；调用强度不能统一改成 SHALL。

依据：§13.2.5.2.4.1;13.2.3.2.4;13.2.2.2.4.4，印刷页 329、331、340。

## 请求接受与BYE收尾不同

适用条件：PF 按 §13.2.5.2.3.1 处理该授权者 INFO，或授权客户端收到其响应；CF 已通过授权后执行媒体释放调用。

PF SHOULD 使用 §13.2.4.3.2 复制包和 MIME 并向 CF 转发，收到 CF200 后才为客户端请求生成200；CF403由本节明确要求生成并回给客户端。客户端收到200或403时 SHOULD 分别告知授权者请求被接受或拒绝。实际收尾仍是 CF 的 BYE/媒体交互，以及各通信段的 BYE200和资源释放；授权请求 INFO200 不是全员已经收尾的聚合证明。

- PF helper 明列包/MIME复制，没有明列 INFO Reason 的复制；CF 最终 BYE 的 Reason 义务不能反推授权者可选原因已逐跳保真。
- 整个组需释放时，被调 helper 向通信的参与者发 BYE；不能替换成所有静态成员、所有 affiliated 用户或 §8 的归属撤销。
- 未规定其他响应/超时在本页的替代成功规则；接收数据或已完成的消息不会仅因 BYE 被自动撤回。

依据：§13.2.5.2.2.1 response paragraphs;13.2.5.2.3.1;13.2.4.3.2;13.2.3.2.2–.4;13.2.2.2.4.4，印刷页 329、331、334、339、340。

## 证据边界

- 不以用户自己离开的 BYE、组归属撤销或紧急状态取消代替授权释放。
- 本页核同版信令和 helper 调用，不声称媒体或跨域验收通过。

## 按需继续

- [session-server-release](session-server-release.md)
- [authorized-user-release-intent-and-decision](authorized-user-release-intent-and-decision.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§13.2.5.2.4.1 step4b;13.2.5.3.4.1 step2c：成功200写发向MCData server，而周边CF/PF流程以PF为对应角色。 不据此重建响应路由；只核授权通过后生成/发送200的行为及后续释放调用。
