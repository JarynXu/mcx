# 预建立会话：建立、空闲修改与无业务使用时释放

## 适用范围

- 固定 TS24.379 V16.14.0、Rel16 Stage 3。预建立会话在实际 MCPTT 呼叫之前协商媒体参数及 ICE 地址端口；它本身与后来使用它的组呼/私呼不同。仅覆盖建立、无关联业务会话时的修改及无业务使用时的释放。
- 客户端建立、PF接收、修改和BYE按各角色实际事件进入。空闲限制只适用于本页修改/释放范围，不是建立准入的成功前提。资源共享、授权失败、媒体不接受或资源不足仍是可达拒绝分支。
- §8.1要求PF使用资源共享；TS24.229、TS29.214、RFC4028/5245与TS24.380仍是外部接口。本页不实现完整IMS注册、PCC/Rx、ICE、会话刷新、媒体控制或REFER组呼/私呼使用。
- §6.6.1.1通用保护范围明列第9–12章及第7章例外，不能由该段机械套出完整第8章XML保护链，也不能宣布预建立会话免除全部安全。§6.2.1的私呼端到端MIKEY要求明确排除预建立建立；实际SIP/SDP与媒体安全依被调用规范，不从本页推定已配置或完成。

## 客户端先建立媒体容器，不向目标组或被叫发起本次业务呼叫

条件：客户端已SIP注册并按§7.2.2或§7.2.3设置服务设置，决定按§8.2.1建立一个预建立会话。

客户端收集服务接口的ICE候选，按TS24.229生成initial INVITE，Request-URI使用服务用户的PF公共服务身份。Contact带g.3gpp.mcptt；Accept-Contact分别带MCPTT和MCPTT ICSI特征及require/explicit，P-Preferred-Service带MCPTT ICSI；可带P-Preferred-Identity。Supported带timer。Session-Expires建议包含、refresher建议省略，若包含refresher则必须为uac。SDP按§6.2.1包含语音m=audio、speech标识及候选，使用媒体控制时另含对应m=application和fmtp，再发送INVITE。客户端实际收到本INVITE的2xx后按TS24.380与媒体平面交互。

规范强度：指定构造、发送与收到2xx后的交互为SHALL；P-Preferred-Identity为MAY；Session-Expires及省略refresher为SHOULD，包含时uac为SHALL。

限制：
- §8.1允许一个或多个预建立会话，不表示必须预建或替代服务注册。§6.3.1.1还按标识预建立setup的PF PSI分类；不能把任意发往PF的INVITE都视为该入口。
- §6.2.1的组编码偏好、ambient方向与implicit SSRC各有业务条件，本页不将它们无条件放入普通预建立SDP。语音必需、控制段按使用条件；完整端口/fmtp与编解码协商不在本页生成。
- §6.4可把非远程ambient且带mc_implicit_request的初始预建立INVITE识别为隐式话权请求，但“识别为请求”不等于已授予话权。2xx和预建立完成也不证明与另一用户的业务呼叫已建立。
- ICE选出非默认候选对时，§8.2.1注记要求另按§8.3再做offer/answer；不能把收到2xx等同所有连接检查已完成。

依据：
- TS24.379 V16.14.0 §4.9;8.1;8.2.1; 6.3.1.1 pre-established INVITE classification; 6.2.1;6.4 initial pre-established implicit-request conditions；印刷页 48, 49, 56, 57, 77, 136, 137, 161, 162。

## PF逐项准入后分配预建立URI，200发送还有媒体交互顺序

条件：PF实际收到§6.3.1.1分类的预建立setup INVITE，按§8.2.2处理；不预设PSI、授权、绑定或媒体资源均有效。

PSI未分配时按§6.3.7.1回404；识别并按本地政策核验MCPTT ID及授权，不获授权回403/Warning100。PF核资源共享：若由SIP core支持，检查用户与第三方REGISTER的UE registration-token绑定，并与INVITE Feature-Caps中的token匹配；不支持或所述绑定不存在则按step5回403/Warning100并停止。未提供MCPTT语音codec拒绝488，资源不可用拒绝500并停止。通过后分配预建立会话URI，生成200；Contact携该URI，PAI携PF PSI，含norefersub及§6.3.2.1.5.2的timer/Session-Expires、Contact特征与tdialog等要求，SDP应答用PF接受流/控制通道地址端口及ICE候选。SIP core支持资源共享时还附media-sharing、session-initiator、timestamp和按m-line顺序的逐流共享规则。之后与媒体平面交互，注记要求该处理完成后才发送200，再评估ICE候选。

规范强度：逐项拒绝、分配、指定字段和媒体交互/发送为SHALL；本地授权政策与共享外部接口另依实际配置。

限制：
- §8.1A允许经SIP core或直接Rx/PCC共享；§8.2.2 step4的token匹配以core支持为条件，step5的无绑定拒绝措辞较宽。本页保留差异，不补直接Rx模式的身份映射或绕过绑定算法。
- §6.3.2.1.5.2规定收到请求未带refresher时200中设uac；不能套普通自动应答的uas。其copy incoming200正文规则本身有实际收到该正文的条件，不为本地生成的200凭空造上游响应。
- 预建立Contact URI、PF PSI、用户身份及以后MCPTT session identity不可混用。PF发200之前媒体交互完成是本调用的顺序要求，不等于全部ICE检查完成、全链路话权或语音成功。

依据：
- TS24.379 V16.14.0 §8.1A;8.2.2; 6.3.7.1; 6.3.2.1.2.2;6.3.2.1.5.2；印刷页 84, 87, 136, 161, 162, 163。

## 修改限于无关联MCPTT会话，旧资源保留到实际200

条件：客户端或PF要在MCPTT业务会话之外修改预建立会话，或接收对现存且无关联MCPTT会话的UPDATE/re-INVITE；只在§8.3对应角色与事件成立时适用。

发起侧生成UPDATE或re-INVITE并提供SDP offer，必要时携ICE候选；客户端offer依§6.2.1，PF offer依TS24.229。接收侧检查至少一个媒体流的参数及至少一个codec可接受，否则回488；通过后生成200及对应SDP answer，必要时含候选，PF响应还含预建立URI的Contact。发起侧收到200后，对参数/codec改变或当前流在answer中被拒绝分别调用TS24.380；PF发起侧还对answer新接受但当前未使用的流调用媒体平面。注记要求发起侧将旧约定资源保留到收到200。

规范强度：所列构造、校验、响应与条件媒体交互为SHALL；旧资源保留到200来自注记。

限制：
- PF发起修改若移除media-floor实体，§8.3.2.2另要求发送前与媒体平面交互；同条注记又要求保留旧实体等资源到200。本页不把发送前交互解释成已彻底释放，也不静默移动动作顺序。
- 客户端作为修改请求接收方生成SDP应答依§6.2.2，PF作为修改请求接收方生成SDP应答依§6.3.2.1.2.2；角色和实际offer条件不同，不将私呼first-to-answer安全条件或新流处理无条件复制到另一角色。
- 这里不是通话中的重协商，也不是完整保持活跃/刷新算法。RFC4028的刷新间隔、失败及重试不由本页补造；保留到200不意味着发生错误或永不响应时无限持有资源。

依据：
- TS24.379 V16.14.0 §8.3.1.1–2;8.3.2.1–2; 6.2.1–2;6.3.2.1.2.2 (SDP dependencies)；印刷页 56, 57, 58, 84, 164, 165。

## 无业务使用时在预建立dialog内释放，业务离开不是同一动作

条件：客户端按§8.4.1.1或PF按§8.4.2.2发起释放；本条只取没有MCPTT业务会话使用该预建立会话的范围。接收BYE时仍实际检查使用情况，发现业务已建立或建立中则退出本条简化路径。

客户端释放时向标识预建立会话的URI发送该预建立dialog内BYE，收到本BYE的200后按TS24.380与媒体平面交互。PF主动释放在其先释放使用该容器的所有呼叫参与者要求之外，再以预建立URI发dialog内BYE，收到200后与媒体平面交互；本页无使用者范围不展开前序参与者释放。客户端或PF实际收到该预建立会话的BYE且检查确认无业务使用时，断开面向对方的媒体资源并生成发送200。

规范强度：对应实际BYE/200事件的构造、资源交互和响应是SHALL；应对core BYE的提示是NOTE。

限制：
- §8.4.1.2对已有MCPTT会话要求逐会话释放；§8.4.2.1还区分业务建立中，先CANCEL，晚到INVITE200仍须释放。它们不能套用本页空闲路径直接宣布所有业务结束。
- 预建立URI用于本容器dialog的BYE；业务清理helper §6.3.2.1.6使用MCPTT session identity，两者不直接等同。本页不提供完整业务清理、CANCEL竞态或等待应答算法。
- 客户端须准备处理SIP core因媒体资源等原因产生的BYE（§8.4.1.1注记）；这不授权把所有BYE都视作PF主动释放。离开一项业务呼叫与拆除预建立容器在§4.9分别指向不同程序，不能互相推定。

依据：
- TS24.379 V16.14.0 §8.4.1.1–2;8.4.2.1–2; 4.9 (call versus container release); 6.3.2.1.6 (identity comparison only)；印刷页 48, 49, 87, 165, 166, 167。

## 条件化关联

[服务设置发布](settings-publication.md)：仅在实际settings-only PUBLISH事件中读取；其200不能代替预建立INVITE、资源共享或媒体准入。
