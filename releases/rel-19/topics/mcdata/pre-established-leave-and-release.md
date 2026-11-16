# 预建立会话的退出：离开 SDS 业务与销毁会话

## 适用范围

- 同版§9.2.5.4与§18.3.3，普通在网SDS预建立使用。先明确要离开的是内部MCData业务通信，还是要释放客户端—PF的预建立SIP session。
- 本页使用实际REFER/业务BYE/预建立dialog re-INVITE或预建立BYE入口；状态与200按对应事务判断，不代表每条消息成功、文件撤回或组归属撤销。
- 媒体交互只记录24.582调用点；关联判定、转发命名和错引限制随各claim保留，不补隐藏的关联表更新或自动重建策略。

## 离开业务时的两个标识

适用条件：用户要求离开预建立会话中的一个MCData session，客户端进入§9.2.5.4.1.1。

客户端先调用媒体过程，再发送dialog外REFER：Request-URI和Target-Dialog指向预建立会话，Refer-To则指向要离开的MCData session，并在该URI加method=BYE；Refer-Sub=false，Supported=norefersub。客户端在REFER2xx后再调用媒体过程；收到对应预建立dialog中的re-INVITE且state=terminated时，按本段通知业务终止成功。这条路径没有要求客户端用BYE销毁预建立会话本身。

- Refer-To的业务session identity不可替换成Request-URI中的预建立身份；不能把method=BYE误读成客户端已经向PF发送同一个BYE事务。
- 本客户端terminated接收段只列用户通知，没有在此完整列re-INVITE应答/ACK或媒体时序；外部SIP行为未核。

依据：§9.2.5.4.1.1;18.3.3.1.1，印刷页 258、422。

## 离开请求、业务 BYE 与终止反馈

适用条件：PF收到客户端REFER，Refer-To的URI中method=BYE，且本段身份绑定条件满足。

PF从PAI确定用户，找不到所列绑定回404/141停止；按false/norefersub条件不建隐式订阅。PF先回REFER200，再向CF发送以Refer-To中业务session identity为Request-URI的BYE。收到该BYE200后，PF调用媒体过程释放与CF的SIP session相关资源，并向预建立会话发state=terminated的re-INVITE。因此REFER200、业务BYE200和客户端终止状态通知不是同一证据，业务收尾也没有在这里自动撤销组归属。

- 离开PF step2的绑定句写“binding between the public user identity”而缺另一端；本页按字面缺绑定拒绝，不自行增加完整绑定键或失效期限检查。
- 这里没有以REFER200证明CF已释放；也未给BYE失败/超时自动成功或回滚规则。
- 媒体资源释放限定与CF业务SIP session相关的资源；不从该句推导预建立资源全部被清空。

依据：§9.2.5.4.2.1;9.2.5.1.2，印刷页 243、244、259。

## 远端结束业务时的客户端通知

适用条件：PF收到CF针对业务通信的BYE；客户端随后实际满足§9.2.5.4.1.2的接收入口。

PF先调用媒体过程并向CF回200，再在预建立会话内发state=terminate-request的re-INVITE；该请求2xx后又调用媒体过程。客户端接收段写在“预建立会话没有关联MCData session”的条件下，若state=terminate-request则先回200，再释放对应MCData通信资源。该分支仍通过re-INVITE表达业务终止，并非对预建立会话发送BYE。

- 接收入口字面要求without an associated MCData session，却又要求释放业务资源；已核步骤未交代关联何时被清除。不能把without改成with，或假定收到re-INVITE前一定已清表。
- PF小节名为Terminating procedures，但step4写发向originating MCData client；本页不静默确定其应指哪个端点。
- CF得到BYE200早于客户端re-INVITE2xx，不能据CF的200断言客户端已呈现或全部资源已完成收尾。

依据：§9.2.5.4.2.2;9.2.5.4.1.2;9.2.5.1.2，印刷页 243、244、258、259、260。

## 销毁预建立会话及所承载的业务

适用条件：客户端或PF决定释放预建立会话本身，进入§18.3.3，而非仅执行§9.2.5.4业务离开。

客户端主动销毁时按§13.2.2.2.2.1发BYE。PF收到预建立dialog内BYE后区分：已有业务则调用业务释放helper；业务正在建立则先CANCEL，若远端INVITE200仍到达，还要调用业务释放；没有业务则调用媒体断开并回BYE200。远端业务BYE200到达后，PF分别调用面向远端和客户端的资源释放，再向客户端回200。PF主动销毁则先移除使用该预建立会话的所有MCData calls中的本客户端，再向预建立URI发BYE，收到其200后交互媒体面。不能把对一个业务的leave视为整个预建立会话已销毁。

- 客户端收到PF的预建立BYE时，若已有业务则逐业务调用24.582释放；若无业务才调用§13.2.3.2.2。不能把无业务分支的完整BYE处理自动复制成有业务分支已明列的步骤。
- PF主动释放opening误回指“as created in clause8.2.2”，而§8.2.2是组归属变化；实际预建立建立过程在§18.3.2。保留错引，不把组归属视为创建预建立会话。
- SIP core也可能因网络媒体资源释放发BYE，客户端须准备处理；本页不核其完整触发与重建机制。
- 取消在途INVITE后仍可能收到200的分支是明文义务；不能把发送CANCEL当成已确认取消，也不能无根据增加已读/送达状态回滚。
- §18.3.3调用§13.2.2.2.3.1时，没有在本节展开如何为各业务选择BYE目标；后者按所收BYE中的session identity设置Request-URI。本页不自行构造预建立身份到业务身份的替换规则，也不据helper调用声称映射已经验证。

依据：§18.3.3.1.1/.2;18.3.3.2.1/.2;13.2.2.2.2.1;13.2.2.2.3.1;13.2.3.2.2，印刷页 327、328、331、422、423。

## 证据边界

- 预建立会话没有被本离开路径显式BYE，不等于它永久可用；客户端、PF或SIP core仍可按§18.3.3释放。
- 群组业务的全组释放策略另见相应CF过程，本页不把单用户离开推成所有参与者结束。

## 按需继续

- [MCData 会话的服务器释放：无预告 BYE、原因与参与者范围](session-server-release.md)
- [MCData 预建立会话：SDS 范围、共享资源与准入](pre-established-session-admission.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。
