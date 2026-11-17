# 普通离网MCPTT手动私呼：等待、人工应答与控制完成

固定ETSI TS124379 V19.4.0，对应3GPP TS24.379 V19.4.0 Release19 Stage3；仅已知双用户的普通PRIVATE CALL手动应答，不含紧急、自动模式或组呼。发起端关联紧急状态为false；目标、承载及必要配置可用。

每个基本私呼状态机按MCPTT user ID区分，并发受MaxCallN10限制。发起模式资格见本页第一节；终接按实际MANUAL请求进入。后续claims只在已满足本条前序条件及各自事件时适用，不把多角色替代事件当作同时成立。

消息传输依赖§11.2.1.1.1；MONP接收port TBD/8809 messages字面问题未修补。安全、配置取得、完整媒体和TS24.380内部话权未核，不以控制成功证明媒体许可。

以下列明动作是规范要求，位置保存及更新另为可选。

## 先判断手动资格，再进入主叫等待

发起MCPTT客户端P0或P1，用户请求普通私呼，Common/PrivateCall/Authorised=true；“请求自动且AutoCommence=true”不成立，且ManualCommence=true。

均匀随机生成并保存call identifier，字面范围(0,65536)，保存自身caller ID和目标callee ID，所存模式设MANUAL COMMENCEMENT MODE，创建call-type状态机。若需端到端安全上下文，先完成本条PCK/PCK-ID、目标UID封装和签名I_MESSAGE的条件步骤，再生成并保存offer SDP。SETUP REQUEST携所存call identifier、双方ID、模式、类型机当前类型及offer，按§11.2.1.1.1发送；CFP1置1，启动TFP1，原在P1则停止TFP7，再进P2。本地位置可保存；普通类型不满足发送User location IE的紧急限定。

未满足手动选择条件不推定自动回落；不裁定随机区间端点。安全步骤保留为前提和调用边界，不证明密钥算法或配置取得已完成。

依据：TS24.379 V19.4.0 §11.2.2.4.2.1，印刷页515,516。

## RINGING不改变P2，后续等待由各自计时事件决定

分别观察手动发起端P2收到RINGING；P2的TFP1到期且CFP1小于上限；P2的TFP1到期且CFP1等于上限并存有MANUAL模式；或P2的TFP9到期。这些是替代入口。

RINGING入口只保持P2。TFP1到期且CFP1小于上限时，可更新所存本地位置，CFP1加1，用所存call identifier、双方ID、模式、类型及offer重新生成SETUP REQUEST，按§11.2.1.1.1发送，启动TFP1并保持P2。手动模式在CFP1等于上限的TFP1到期事件中启动TFP9并保持P2；P2的TFP9到期则启动TFP7、释放call-type状态机并进入P1。

不把RINGING解释成启动TFP9、停止TFP1或已接受。重传位置字段仍限紧急，普通呼叫不发送。TFP9与被叫TFP2是不同角色的等待，不设共同倒计时。

依据：TS24.379 V19.4.0 §11.2.2.4.2.2;11.2.2.4.2.3;11.2.2.4.2.5;11.2.2.4.2.6，印刷页516,517。

## 终接端发送RINGING后等待用户决定

终接客户端P0或P1收到SETUP REQUEST，模式为MANUAL COMMENCEMENT MODE，call identifier不同于所存值。

保存来话call identifier，创建call-type状态机，保存请求中的caller ID并将自身ID存为callee ID；生成携所存call identifier和双方ID的RINGING，按§11.2.1.1.1回复。原在P1则停止TFP7，启动TFP2，进入P5。P5状态定义描述已经向用户呈现来话通知并等待用户指示。

通知来自P5状态定义，不补未列的UI样式或独立提示动作顺序；进入P5和发RINGING都不是已接受或已获话权。

依据：TS24.379 V19.4.0 §11.2.2.3.6;11.2.2.4.4.1，印刷页515,521,522。

## 用户接受后仍须区分安全验证结果

终接客户端P5收到用户接受指示；分别处理offer完全没有a=key-mgmt属性，或该属性以mikey值携MIKEY-SAKKE I_MESSAGE的验签成功/失败。其他属性格式不覆盖。

指定I_MESSAGE路径从IDRi取发起MCPTT ID、转为UID并验签。失败时发携所存call identifier及双方ID的REJECT：请求限制失败通知且FailRestrict=true时Reason为FAILED，否则为E2E SECURITY CONTEXT FAILURE；按§11.2.1.1.1发送，停止TFP2，TFP7未运行才启动，释放call-type状态机并进入P1。验签成功且已解封PCK、提取PCK-ID后，或offer完全无该属性时，生成并保存answer SDP，以所存身份和answer发送ACCEPT，按私呼SDP建立媒体，停止TFP2，CFP4置1，启动TFP4并保持P5。

失败不走成功或无属性路径，非指定格式不等于无属性。此处媒体SDP写法为private call的SDP body，不静默改写成别节answer字样。已接受后的P5不要求用户再次点击；完整密码算法及媒体内部未核。

依据：TS24.379 V19.4.0 §11.2.2.4.4.3，印刷页522,523,524。

## 用户拒绝与未回应有不同Reason和停止动作

分别观察终接P5的用户拒绝指示或TFP2到期；另观察发起P2收到对SETUP REQUEST的REJECT且call identifier等于所存值。

用户拒绝时，REJECT携所存call identifier及双方ID，Reason通常为REJECT；仅请求限制失败通知且FailRestrict=true时为FAILED。按§11.2.1.1.1发送后停止TFP2、启动TFP7、释放类型机、进入P1。TFP2到期则发送相同身份字段、Reason=FAILED的REJECT，然后启动TFP7、释放类型机、进入P1。发起P2收到满足关联条件的REJECT时，停止运行中的TFP1和TFP9，启动TFP7、释放类型机并进入P1。

不把用户拒绝的显式stop TFP2机械加入已经到期的分支。进入P1不等于立即清call ID或证明对端同步退出。

依据：TS24.379 V19.4.0 §11.2.2.4.4.2;11.2.2.4.4.7;11.2.2.4.2.7，印刷页517,522,524,525。

## 两端基本控制和类型控制分别完成

分别观察发起P2收到回应SETUP REQUEST且call identifier相同的ACCEPT；手动终接P5收到发起用户的ACCEPT ACK或RTP；或类型机Q0收到ACCEPT或ACCEPT ACK且所存类型为PRIVATE CALL。

发起端存answer，发送携所存call identifier与双方ID的ACCEPT ACK，按§11.2.1.1.1发送后停止运行中的TFP1和TFP9，按answer建立媒体，以originating floor participant调用TS24.380 §7.2，启动TFP5并进入P4。终接端收到ACK或RTP时停止TFP4，以terminating MCPTT client调用同一话权接口，启动TFP5并进入P4。Q0自身收到ACCEPT或ACK且存PRIVATE CALL时进入Q1。

Q0完成入口没有RTP；基本机P4不能证明类型机Q1。不造跨机调度。话权调用不是获权或声音交付证明。终接入口未重列call ID校验，不据此认定任意ACK有效。

依据：TS24.379 V19.4.0 §11.2.2.4.2.8;11.2.2.4.4.5;11.2.3.4.4，印刷页517,518,524,530,531。

## 接受后的重传与上限失败保留入口重叠

手动终接端已发送ACCEPT并仍在P5，TFP4到期；CFP4等于上限时另满足失败入口。

一般TFP4到期条款要求按所存call identifier、双方ID及answer SDP生成并回复ACCEPT，发送后CFP4加1，启动TFP4，保持P5。CFP4等于上限的失败条款要求启动TFP7、释放call-type状态机并进入P1。

一般重传没有小于上限守卫，不补优先级或先重传后失败的顺序。失败条款未列媒体终止、REJECT或Q0转换，不能补为完整失败回收算法。

依据：TS24.379 V19.4.0 §11.2.2.4.4.4;11.2.2.4.4.6，印刷页524。

## 范围

覆盖所列手动建立取消、终接收RELEASE及已建正常释放确认；完整报文编码、无ACK重传与竞态调度不在本页范围。 两机并行见§11.2.3.1（p528）；普通类型初始化见§11.2.3.4.2/.3（pp529–530）：Q0普通发起（关联紧急状态false）或空闲Q0收到PRIVATE CALL请求时，各自保存普通类型和相应ProSe优先级，具体配置值未核。

[自动模式](offnetwork-private-auto-control.md)用于比较，不替代本页手动入口。来源：[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。

## 取消与释放：按当前状态继续

以下分支仍限本页的普通手动私呼，各动作在自己的入口成立时执行。

### 建立等待中的取消与终接撤销

分别观察手动发起端P2收到本用户取消请求，或手动终接端P5或P1收到PRIVATE CALL RELEASE；这些是不同角色的替代入口。

发起端生成携所存call identifier、caller ID、callee ID的PRIVATE CALL RELEASE，按§11.2.1.1.1发送，停止TFP1、停止TFP9，启动TFP3，然后将CFP3置1，进入P3。终接P5或P1收RELEASE时，生成携上述三个所存身份字段的RELEASE ACK并按§11.2.1.1.1回复；仅在P5且TFP7未运行时启动TFP7，随后停止运行中的TFP2和TFP4；仅原在P5时释放call-type状态机并进入P1。

P1收RELEASE仍回复并停止运行中的TFP2/TFP4，但该入口不要求重新启动TFP7或再次释放类型机。终接段未列媒体终止，不补媒体清理。 §11.2.2.4.4.8标题称Caller cancels，入口只写P5/P1收到RELEASE，未另列发送者角色或call ID相等校验；完整分派与鉴权未核，不认定任意消息有效。P2取消也未列if running限定其停止TFP1/TFP9。

依据：TS24.379 V19.4.0 §11.2.2.4.2.9;11.2.2.4.4.8，印刷页518,525。

### 已建立时的请求与接收清理

分别观察手动私呼基本控制P4收到本用户释放指示，或P4收到PRIVATE CALL RELEASE。

用户释放时，生成携所存call identifier及双方ID的RELEASE，按§11.2.1.1.1发送，停止TFP5，先将CFP3置1再启动TFP3，进入P3。P4收RELEASE时，生成携所存call identifier及双方ID的ACK，按§11.2.1.1.1回复后终止私呼媒体、停止TFP5、启动TFP7、释放call-type状态机并进入P1。

P4用户释放的CFP3/TFP3次序不同于P2取消。发出RELEASE不等于本地媒体已经终止；接收端发ACK先于其媒体终止。 本用户不限定为原主叫；收RELEASE入口未另列发送者/ID守卫，不补造也不因此放宽完整鉴权要求。

依据：TS24.379 V19.4.0 §11.2.2.4.5.1;11.2.2.4.5.4，印刷页525,526,527。

### 等待确认与忽略标识阶段分别收尾

手动私呼客户端基本控制P3收到对PRIVATE CALL RELEASE的PRIVATE CALL RELEASE ACK；另一个独立入口是P1的TFP7到期。P3可以来自本页P2取消或P4用户释放。

P3收对应ACK时，停止运行中的TFP3，终止媒体会话，启动TFP7，释放call-type状态机并进入P1。P1的TFP7到期时，清除所存call identifier并进入P0。

§11.2.2.4.5.5按P3及对应ACK进入，没有以此前必须P4作为入口；此处不继承自动已建释放页的共同条件。取消时若尚未建媒体，不由终止媒体这一步推断曾有媒体建立。 无ACK的重传、达上限出口及乱序竞态未在本页闭合；P1不是已立即清除标识。

依据：TS24.379 V19.4.0 §11.2.2.4.5.5;11.2.2.4.5.7，印刷页527。

### 类型控制独立按Q1入口清理

手动普通私呼的类型控制处于Q1，收到本用户释放呼叫指示，或收到PRIVATE CALL RELEASE。P2、P4或P5本身均不能替代Q1条件。

释放所存current call type，停止运行中的TFP6，释放所存ProSe per-packet priority，进入Q0。

不把Q1动作套到Q0的建立等待，也不把RELEASE ACK或计时到期补为该Q1入口。基本控制释放call-type状态机与此处Q转换不同，不设两机先后或原子性；Q0不证明媒体已清理。

依据：TS24.379 V19.4.0 §11.2.3.1;11.2.3.4.7，印刷页528,536。

