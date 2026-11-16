# 组呼参与功能的183、PRACK与200分别证明什么

TS24.379 V19.4.0，普通非优先预安排组呼；终接参与功能收到面向自己的初始SIP INVITE。

排除emergency-ind=true、imminentperil-ind=true及任何Priv-Answer-Mode头；不覆盖远程监听、重组扩展。

已通过§10.1.1.3.2的前置检查，并进入本claim指定的接续模式及会话类型。

## 自动分支的早期未确认响应

适用条件：自动按需分支，且无Answer-Mode及Priv-Answer-Mode头且客户端设置auto-answer，或者Answer-Mode=Auto且客户端设置auto-answer。

生成183，P-Answer-State=Unconfirmed，PAI为T-PF；无论可靠或不可靠发送均不带SDP。Priv-Answer-Mode=Auto是原文另一触发，但已排除于本主题。

依据：§6.3.2.2.5.2 steps1–2 NOTE。

## PRACK 的200只确认临时响应

适用条件：自动按需分支的183采用可靠发送，且收到对应PRACK。

必须生成并发送针对PRACK的200；该200不是对INVITE的最终应答。

依据：§6.3.2.2.5.2 PRACK paragraph。

## 不可靠183之后的最终响应

适用条件：自动按需，183以不可靠方式发送，且收到终接客户端对下行INVITE的200。

立即发送上游INVITE200；按同节最终响应构造要求处理。

依据：§6.3.2.2.5.2 response step1。

## 可靠183已确认

适用条件：自动按需，183可靠发送，且已收到PRACK并已发送其200，且收到终接客户端对下行INVITE的200。

立即发送上游INVITE200。

依据：§6.3.2.2.5.2 response step2a。

## 客户端已答复但PRACK尚未到达

适用条件：自动按需，183可靠发送，且收到终接客户端对下行INVITE的200，但尚未收到对应PRACK。

等待PRACK；收到后先生成并发送PRACK200，再发送上游INVITE200。不是收到客户端200即无条件转发。

依据：§6.3.2.2.5.2 response step2b。

## 自动按需最终响应的确认状态

适用条件：自动按需已收到客户端INVITE200；此前183不可靠，或此前可靠183对应的PRACK已收到且PRACK200已发送。

按§6.3.2.2.4.2生成响应，SDP answer基于客户端200的SDP并遵循§6.3.2.2.2.1；PAI为T-PF；若先前183携Unconfirmed，则此200必须带Confirmed；并执行24.380媒体交互。

依据：§6.3.2.2.5.2 final response steps1–5。

## 手动组呼的183另有处理

适用条件：手动按需分支，且收到终接客户端对下行INVITE的183（原文注释指出组呼可有该响应）。

按§6.3.2.2.4.1生成183，PAI为T-PF并转送。§6.3.2.2.4.1还要求：因收到临时响应而生成，且该来件有mcptt-info正文时复制该正文。不能把自动分支的无SDP强制规则搬到本分支；本段也未授权逐字透传全部SDP。

依据：§6.3.2.2.6.2 183 paragraph;6.3.2.2.4.1。

## 手动按需客户端200的后续

适用条件：手动按需分支，且收到客户端对下行INVITE的200。

生成上游200；SDP answer基于客户端200按§6.3.2.2.2.1构建，PAI为T-PF；执行24.380§6.4媒体交互并转送。不要称为群体呼叫最终成功或话权授予。

依据：§6.3.2.2.6.2 200 paragraph。

## 其他无SDP响应

适用条件：自动或手动按需分支，且收到未由相应前述响应处理段处理的其他SIP响应，且响应不含SDP。

沿信令路径转送至主叫网络。无SDP是这一剩余分支的条件，不是覆盖所有手动183的先验门槛。

依据：§6.3.2.2.5.2 final paragraph;6.3.2.2.6.2 final paragraph。

## 普通自动预建立不等待新的INVITE确认

适用条件：自动预建立分支；空闲会话及两个媒体段匹配条件均满足，且INVITE没有Priv-Answer-Mode头，且emergency-ind、imminentperil-ind均不为true。

T-PF生成并发送上游INVITE200，P-Answer-State=Unconfirmed，SDP基于预建立协商及收到的offer；之后按24.380§9交互。该普通分支不等待新客户端INVITE200。若存在任意Priv-Answer-Mode头或上述任一true，则原文转入带Replaces的新INVITE分支，不适用本结论。

依据：§6.3.2.2.5.3 steps1–7。

## 普通手动预建立使用既有对话

适用条件：手动预建立分支；空闲会话及两个媒体段匹配条件均满足，且INVITE没有Priv-Answer-Mode头，且emergency-ind、imminentperil-ind均不为true。

在既有预建立dialog中发reINVITE；其不能带Answer-Mode，手动应答由该场景隐含。收到客户端200后按§6.3.2.2.6.3构建上游200并交互媒体；有codec/media-format改变时更新媒体。注释称MCPC Connect向客户端提供会话身份，具体媒体过程未核。任意Priv-Answer-Mode头/优先标记true走另一个Replaces分支。

依据：§6.3.2.2.6.3。

## 证据边界

- 手动183处理未规定P-Answer-State=Unconfirmed，手动最终200也未给自动分支的Unconfirmed→Confirmed步骤；不得凭收到183就套主控的早期200分支。

- 完整SIP fork/多分支失败合并未由这些条款定义；24.229依赖未核。
- 未核24.380媒体实施，不能将响应等同全组建立或话权授予。
- 显式Answer-Mode入口选择不从10.1.1.3.2无头条件反推。
- 6.3.2.2.6.3以reINVITE调用初始INVITE生成条款，保留原交叉引用，不改写成新dialog。

## 按需继续

- [group-terminating-addressing](group-terminating-addressing.md)
- [group-terminating-mode](group-terminating-mode.md)
- [group-acknowledged-start](group-acknowledged-start.md)

[ETSI官方TS24.379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)，印刷页118、119、120、117、122、123、121、124；仅本版本。

- [客户端接收与应答](../groups/terminating-client-acceptance.md)
