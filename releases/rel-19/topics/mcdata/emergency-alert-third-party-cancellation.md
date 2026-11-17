# 指定他人的MCData紧急告警怎样取消

## 适用范围

- 限TS24.282 V19.7.0在网普通配置组，已明确目标组及另一个告警原发起者；目标组无正在进行的组通信。排除adhoc、regroup、离网、跨域及未指定告警的批量取消。
- 只处理独立紧急告警的MESSAGE取消，不附带组in-progress emergency状态取消，请求及本页接收通知不含emergency-ind；不是SDS/FD会话升级、降级或释放。
- 请求客户端、CF已授权分支和通知接收者分别按各claim条件进入，不能将客户端许可、CF缓存修改和最终用户状态当成同一个已提交结果。配置schema、完整PF转交及通知关联仍有未核边界。

## 取消他人告警须有专门许可，并指明原发起者

适用条件：用户请求取消一个已指定的、由另一用户发起的告警，客户端执行§16.2.1.2。

客户端要求请求用户及profile对应的ruleset/rule/actions/allow-cancel-emergency-alert-any-user存在且为true；未授权时，提示用户与终止过程均为SHALL。通过后发对话外MESSAGE，mcdata-info携带目标组mcdata-request-uri、alert-ind=false及原告警发起者MCData ID的originated-by，Request-URI指向服务该组的PF。取消者与originated-by不是同一角色。step7仅在请求不带originated-by时置MDEA4，因此不能把自身取消的待确认状态动作套到本请求。

- 允许取消自己的告警不等于具有any-user许可；多告警未指定目标的停止条件在原文限自身告警，不扩大为已验证的第三方消歧算法。
- 第三方生成分支step5没有像自身分支step4c那样列mcdata-client-id；CF反馈又要求复制入站client-id，不能自行补出完整关联字段。可选功能别名及完整报文编码未展开。
- 发出的请求含originated-by，不满足本条自身取消反馈和错误恢复的入口；不能据普通200清取消者自身MDEA或MED。

依据：TS24.282 V19.7.0 §16.2.1.2 opening,steps1–3,5,5A,6–8;notification and error paragraphs;step4c (client-id comparison only)，印刷页378, 379, 380。

## CF授权分支清指定原发起者的告警缓存

适用条件：CF实际收到alert-ind=false、带originated-by且不带emergency-ind的告警取消MESSAGE，并已进入§16.2.3.2 step2明定的按§6.3.7.2.2已授权分支；这不由客户端许可自动推得。

CF清除originated-by所指用户仍有未取消告警的缓存。对已归属但未加入通信的成员生成取消通知，calling-user-id保留收到请求中的实际调用用户，另复制originated-by并写alert-ind=false。随后向原请求回200，再生成独立的成功接收取消请求MESSAGE，写alert-ind=false、alert-ind-rcvd=true，并按step2i复制入站client-id后发送。该列序没有等待全员通知响应的门槛；不能由原请求200证明所有接收者已处理。

- CF helper只按调用用户profile的ruleset/allow-cancel-emergency-alert值true/false判断，未明列客户端的any-user字段，也未说明缺失值。角色间权限和schema路径不能擅自归一。
- §16.2.3.2 step1否定入口却引用发起授权§6.3.7.2.1；本页无emergency-ind时该入口写403、alert-ind=true并停止。不能修成完整一致的取消准入算法。
- step2i依赖入站client-id，而客户端第三方生成分支未明列它；本页不证明独立成功通知的关联链已经闭合。PF转交、通知helper完整编码和最终寻址未在本页展开。
- 清缓存对象是originated-by指定用户，不是取消请求者或全组所有告警；不推导归属撤销、组紧急状态清除或通信释放。

依据：TS24.282 V19.7.0 §6.3.7.2.2;16.2.3.2 opening,step1a,step2a,c,e–i,k and final paragraph，印刷页118, 119, 402, 403, 404。

## 接收者用originated-by识别被取消者

适用条件：客户端实际按§16.2.1.3收到告警通知，alert-ind=false，originated-by存在，且没有emergency-ind；这是独立接收入口，不要求其本人先发取消请求。

客户端SHOULD显示告警取消、组ID及原发起者；原发起者优先取originated-by，而不是把calling-user-id所指取消者当成原发起者。只有originated-by等于接收用户自身MCData ID时，本分支才SHALL将其MDEA置1。此处没有列出清除MED的动作，也不满足另需emergency-ind=false的组状态复位条件。

- 若originated-by指向别人，本分支不要求清接收者自己的MDEA；SHOULD显示也不是人员已读证据。
- 原告警者须实际收到该通知才能应用本条；CF已清缓存或已回取消者200不能替代该接收条件。未证明离线、未归属用户或所有终端均能得到通知。

依据：TS24.282 V19.7.0 §16.2.1.3 opening,step2a–c and NOTE2，印刷页380, 381。

## 整体边界

- 客户端any-user许可与CF普通取消许可的对应、CF否定入口回指及第三方client-id来源未闭合；本页给出条件化动作，不提供完整无歧义的端到端准入实现。
- §16.2.3.2的编辑说明保留紧急组/组通信支持可能缺失、部分或仅用于告警的限制。本页不据告警流程推定完整紧急组通信能力。

## 相关主题

- [emergency-alert-self-cancellation](emergency-alert-self-cancellation.md)
- [emergency-alert-admission-and-results](emergency-alert-admission-and-results.md)
- [group-emergency-client-cancellation](group-emergency-client-cancellation.md)
