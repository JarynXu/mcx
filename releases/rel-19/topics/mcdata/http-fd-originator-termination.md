# HTTP FD 主叫取消：定位原分发、202与终止结果

TS24.282 V19.7.0，§13.2.2.3主叫用户发起的HTTP FD终止，限直接私聊或普通预安排组；文件已上传成功且分发信令已经发向服务器。原文概述称该信令为SDS message，具体生成过程使用FD HTTP TERMINATION，保留措辞差异。

调用实际PF/CF过程，各自身份绑定、资源、路由与格式检查按条件执行；被明确要求停止的分支不得继续到业务结果。外部配置、SIP/RFC及存储实现仅按已列依赖定位，未据此补充本版缺失步骤。

取消HTTP FD用SIP MESSAGE，不是SIP CANCEL、媒体BYE或接收者FILE DOWNLOAD REQUEST REJECTED；本页不覆盖上传中的HTTP连接中止。

## 定位原文件分发的终止请求

适用条件：主叫进入§13.2.2.3.2.1.1，要求停止既有私聊或组HTTP FD。

客户端按§6.2.4.1向服务自己的PF生成MESSAGE。私聊携带原接收者的resource-list和one-to-one-fd；组携带group-fd、组ID及发起client ID。被调用的§6.2.2.4虽被caller称为standalone FD生成，实际是终止专用helper：生成mcdata-signalling MIME中的FD HTTP TERMINATION，带Conversation ID、Message ID及与原FD相同URL的FILEURL Payload，类型设TERMINATION REQUEST；适用应用标识可带。这里定位的是已分发的文件传输，而非创建新文件发送。

- FD HTTP TERMINATION实际消息定义在§15.1.13，不是若干后续过程仍引用的§15.1.11。这里不因错误回指把它换成DEFERRED DATA REQUEST。
- 消息表把Payload列为可选，但本生成helper明确要求FILEURL Payload；不能用表中O取消具体过程的义务。
- 不从一般UUID规则推导取消应生成全新业务ID；本链识别的是原分发记录，具体生成文字为identifying conversation/message。

依据：§13.2.2.3.1;13.2.2.3.2.1.1;6.2.2.4;6.2.4.1;15.1.13.1，印刷页 59、61、329、330、359。

## 身份、文件和传输记录检查

适用条件：请求按§13.2.2.3.3/.4所指向的§10.2.4.3.1及§10.2.4.4.2处理，前序资源分支未拒绝或排队停止。

O-PF从PAI关联取主叫MCData ID；无绑定或已过期回404/141，找不到CF回404/142并停止。CF对FD HTTP TERMINATION同样要求唯一消息、唯一Payload、FILEURL及文件存在，相关失败为403/209、210、211、212；之后缺Conversation ID或Message ID回403/223，以这两个ID找不到传输回404/224。一步失败不能越过到202。组初发FD的§10.2.4.4.2 step12有FD SIGNALLING PAYLOAD外层条件，不能把其整套组准入/分发步骤直接套在终止消息上。

- §13.2.2.3.3/.4对PF/CF过程的调用用SHOULD；本claim在采用这些过程时说明其内部SHALL检查，不把调用强度改写为SHALL。
- CF先验证URL文件存在，后检查传输记录；文件已不存在可先触发403/212，不能把所有重复取消都归为404/224或默认幂等成功。step11按两个ID查记录；step17另用两个ID加FILEURL查ongoing传输，不能把两次关联条件合并。
- CF此处不因握有三元标识就明定任何用户都可取消；本主题限定原主叫。PF仍执行§11.1，step7拒绝映射带controller-psi缺失守卫，不能从存在controller-psi推定免除身份绑定/全部授权。
- 私聊request-type仍触发step10的resource-list条件；本页使用正确单目标直接ID，不扩别名或零entry错误码。

依据：§13.2.2.3.3/.4;10.2.4.3.1 steps1–7;10.2.4.4.2 steps1–7,10–12;6.7.3.1/.2，印刷页 135、277、278、281、282、283、284、330。

## 202之后的独立终止结果

适用条件：CF通过适用前置步骤，收到类型为TERMINATION REQUEST的FD HTTP TERMINATION。

§10.2.4.4.2先在steps15、16向O-PF回202，再在step17处理终止。它以Conversation ID、Message ID和FILEURL定位ongoing传输；存在时调用§12.4.2.1并把网络通知类型设为FILE DELETED UNAVAILABLE TO DOWNLOAD。随后CF另向请求主叫所属PF发MESSAGE，其业务目标从入站mcdata-calling-user-id取得，使用§6.3.6.1生成TERMINATION RESPONSE，并按本过程成功与否写RELEASE SUCCESS或RELEASE FAILED。原请求的202不是这个独立业务结果。

- “if clause is successful”的判定未在step17细化成存储API结果或全员确认门槛；不能自行把任意202或网络通知发出定义为成功。
- step17a调用的§12.4.2.1是SIP通知生成helper，不提供物理删除API，也未在此调用列出与到期流程相同的目标筛选算法。不要以FILE DELETED文字证明文件字节已物理删除。
- O-PF分别把收到的202或200生成给客户端；这不是要求先202再对同一事务补第二个最终200。排队202/215的停止分支亦不能直接到step17。

依据：§10.2.4.4.2 steps15–17;6.3.6.1;12.4.2.1;13.2.2.3.4，印刷页 98、285、286、323、324、330。

## 业务结果与通知200

适用条件：主叫客户端收到mcdata-signalling MIME中具有FD HTTP TERMINATION消息标识的服务器MESSAGE。

客户端先为该MESSAGE回200；带Application ID或Extended Application ID时将FD HTTP TERMINATION交应用。只有Termination information type为TERMINATION RESPONSE且Release Response Type存在时，才按RELEASE SUCCESS或RELEASE FAILED通知用户成功或失败。这两个业务结果与SIP状态码分属不同字段，不能把回200等同取消成功，也不能将没有结果IE当作成功。

- 交应用和按结果通知用户在原文是分别列出的步骤，没有“交应用后必定跳过用户通知”的otherwise；不自行增加互斥。
- 结果是否到达每个接收者、历史文件副本是否撤销、已完成下载是否回滚不由主叫的RELEASE SUCCESS或对结果MESSAGE的200证明。
- 本接收段未展开三元标识匹配失败的处理；不从服务器预告接收段复制新的错误码或默认动作。

依据：§13.2.2.3.2.1.2;15.1.13.1;15.2.22/.23，印刷页 330、359、372、373。

## 证据边界

- 本页核原主叫取消的实际入口及结果，不借第三方授权释放补权限。
- 所需SIP/RFC和内容存储删除实现未完整核验；明确的业务结果字段不能替代未定义的完成判据。

## 按需继续

- [http-fd-server-stop](http-fd-server-stop.md)

[3GPP TS24.282 V19.7.0 / ETSI TS124282 V19.7.0 (2026-08)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124282/19.07.00_60/ts_124282v190700p.pdf)；仅本版本。

## 原文差异

§13.2.2.3.1/.2.1.1 versus6.2.2.4：概述称上传后发送SDS message，生成caller称standalone FD；被调6.2.2.4实为FD HTTP TERMINATION生成。 按明确helper写终止请求，同时记录caller措辞，不因此新发SDS或普通FD。

§13.2.1.1;13.2.3.3.2.1;13.2.4.5.2.1/.3;15.1.11/.13：服务器生成helper引用15.1.3.1，多处接收过程引用15.1.11；实际FD HTTP TERMINATION在15.1.13，15.1.11是DEFERRED DATA REQUEST。 保留准确实际定义和各处错回指，不把旧编号静默修复成已验证编码。

§13.2.4.5.2.1 step2a(iii);13.2.4.5.4.1 step2：controller-psi由CF放mcdata-info XML，客户端句子却写从mcdata-signalling MIME中的该XML元素读取。 直接暴露两端不一致；依赖成功保存PSI的延期发送保持条件化。

§10.2.4.4.2 step18 versus13.2.4.5.4.2：通用CF入口把非TERMINATION REQUEST引到13.2.5/.6，不是服务器预告的13.2.4.5。通用入口此前还已发送202，而直接延期handler回200。 不修改caller、不拼装同一事务双最终响应；只陈述各自实际入口条件和已核handler行为。

§10.2.4.4.2 step17a;13.2.3.3.4 step1;12.4.2.1：取消/停止要求FILE DELETED，停止caller还明确写删除文件；被调helper仅生成SIP通知，没有删除API和结果判据。 保留删除义务，区分信令意图/声明与物理完成证明，不由通知类型填出实现。

§15.1.13.1;15.2.21;13.2.4.5.4.3：HTTP消息表/专属过程使用Extension response type，但IE用途句只写Comm release Information type=EXTENSION RESPONSE。 按HTTP专属业务分支解释ACCEPTED/REJECTED，记录字段适用措辞的局限。
