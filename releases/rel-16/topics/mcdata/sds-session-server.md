# 私聊 SDS 会话：服务器准入、目标邀请与响应证据

## 适用范围

- 固定TS24.282 V16.13.0（2026-02），普通在网、直接MCData ID、按需one-to-one SDS session的服务器职责；不含组、功能别名、预建立会话或standalone SDS。
- 按O-PF、CF、T-PF实际请求/响应及其输入分别适用。拒绝检查不继承绑定有效、许可已通过或200已收到的共同前提；构造与后续步骤只在各自前序未停止时继续。
- 适用MIME/XML保护按6.4及6.5.1.1–4，接收验证/解密先于其他处理，失败不得继续；本页不是完整SIP、安全或MSRP实现。

## 主叫参与功能先核绑定、选择 CF，再检查会话资格

条件：主叫参与功能实际收到按6.3.1.2分类的普通one-to-one-sds-session INVITE；绑定、CF选择及许可仍待检查，后续构造仅在前序未停止时适用。

服务器分类同时使用实际路由角色、Accept-Contact中的SDS ICSI、P-Asserted-Service中的SDS ICSI及mcdata-info中的one-to-one-sds-session，不把standalone的one-to-one-sds当作同一入口。O-PF无法处理时可用500拒绝并可携Retry-After，选定拒绝后停止。随后从PAI中的public user identity确定主叫MCData ID并授权；找不到绑定或绑定过期，发404/141并停止。它为主叫选择提供私聊SDS会话服务的CF；无法确定时404/142并停止，然后调用11.1。该helper的私聊发送许可缺失或false会停止；出站One-to-One-Communication名单存在且含一个或多个entry且目标不匹配也会停止。9.2.4.3.3分别为step1的不许可和目标不许可给出403/221与403/229。11.1 step9另要求：为以后通信建立私聊SDS session时，参与功能检查主叫或被叫任一方allow-transmit-data缺失或false，不得建立；客户端在此没有进一步检查不等于参与功能也免检。通过适用检查后，O-PF以选定CF的PSI为Request-URI，写入主叫MCData ID，保留收到的PAI并按专用PF helper生成SDP offer。

强度：角色分类、检查、规定的拒绝和后续构造为SHALL；无法处理时拒绝及Retry-After为MAY；Session-Expires为SHOULD，建议省略refresher，若携则须为uac。

- 11.1 step9的双方资格是独立必要条件；本版9.2.4.3.3的221明确回指step1，没有为仅step9失败另列专用响应映射，本页不替它补码。建会许可也不是以后每条SDS已通过大小或发送检查。
- 9.2.4.3.3 step7b字面回指11.1的1a，而helper实际名单段标为1A；保留这一标记差异。step12A又写incoming SIP MESSAGE，涉及功能别名，本页排除该分支，不把它改写成INVITE算法。

依据：3gpp-ts-24.282-v16.13.0 §6.3.1.2 SDS-session and standalone classifications，印刷页 47,48,49；3gpp-ts-24.282-v16.13.0 §9.2.4.3.3 steps1–16，印刷页 132,133,134；3gpp-ts-24.282-v16.13.0 §11.1 steps1,1A,3,7,9,11–12，印刷页 187,188,189；3gpp-ts-24.282-v16.13.0 §9.2.4.3.1，印刷页 132。

## CF 核媒体与服务条件，再邀请明确的单一目标

条件：CF实际收到本页SDS session INVITE；各拒绝仍可达。只有前序未停止且resource-lists恰有一个entry时，才进入9.2.4.4.3的本页私聊邀请分支。

CF因资源不足或拥塞风险可500拒绝并可携Retry-After，拒绝后停止。媒体参数不可接受或SDP未提供MSRP URI则488并停止；所需SDS功能标签或SDS ICSI标签缺失则403并停止。之后按收到且支持的Contact标签缓存能力、启动SIP Session timer。one-to-one-sds-session缺少resource-lists或其中超过一个entry时403/204并停止；恰有一个entry时邀请该用户，并调用24.582的6.3.2。邀请helper以目标MCData ID填写mcdata-request-uri，以目标关联的T-PF PSI为Request-URI，以CF PSI为PAI，以邀请者public user identity为Referred-By，并携CF会话身份、SDS/isfocus标签及自己的SDP offer。CF offer的message流为sendrecv、自己的MSRP path、两种SDS MIME accept-types及actpass；CF answer按收到协议使用TCP/MSRP或TCP/TLS/MSRP，sendrecv、自己的path，setup为passive。

强度：必要检查、所列拒绝、邀请及媒体调用为SHALL；资源/拥塞拒绝及Retry-After为MAY；出站Session-Expires为SHOULD，其refresher须省略。

- 现有resource-lists为零entry时，不满足原文“缺少body或超过一个”的204条件，也不满足恰好一个的邀请条件；不能擅自补成同一码或选出目标。
- 目标T-PF地址如何发现，9.2.4.4.3 NOTE1明确为本Release范围外。该helper的服务头字面为P-Asserted-Service-Id，而分类用P-Asserted-Service；本页保留差异，不提供自动改名后的完整报文。
- CF构造步骤未逐项明确补出下游分类所需request-type或T-PF名单检查所用mcdata-calling-user-id的传递方法。本页不凭相邻程序补字段；下游职责按实际收到其所需输入分别说明，不声称这组摘要已闭合端到端报文生成。

依据：3gpp-ts-24.282-v16.13.0 §6.3.1.2 SDS-session classifications，印刷页 48；3gpp-ts-24.282-v16.13.0 §9.2.4.4.4 definitions;steps1–7;step8 comparison-only，印刷页 138,139；3gpp-ts-24.282-v16.13.0 §9.2.4.4.3 full (private caller and dependency boundary)，印刷页 137,138；3gpp-ts-24.282-v16.13.0 §9.2.4.4.1–2，印刷页 136,137。

## 被叫参与功能按目标绑定和入站名单决定是否继续

条件：T-PF实际收到6.3.1.2所定义的本页SDS session INVITE；应按实际可得目标ID和主叫字段执行，不能继承上游已通过全部准入的假定。

T-PF不能处理时可500拒绝并可携Retry-After，拒绝后停止。它先检查Contact URI中的isfocus，缺失则403/104并停止；再用mcdata-request-uri中的目标MCData ID取public user identity绑定，绑定不存在则404并停止。入站名单拒绝须同时满足：IncomingOne-to-OneCommunicationList存在且含一个或多个One-to-One-CommunicationListEntry；收到的mcdata-calling-user-id与名单任何entry均不匹配；未配置允许接收任意用户的私聊通信。此时403/230并停止。继续时以目标绑定的public user identity为Request-URI，Contact使用映射到收到CF会话身份的本地会话身份并携SDS/isfocus及其他URI参数，复制已有Accept-/Reject-Contact、MIME bodies及PAI，按PF SDP offer helper生成邀请。该helper只保留一个SDS media-level section并保留收到的mikey属性；需要时才替换IP/port，若替换IP则把自己的MSRP URI插在已有path之前。

强度：必要检查、条件拒绝及继续后的构造为SHALL；无法处理时500及Retry-After为MAY；Session-Expires为SHOULD，建议省略refresher，若携则须为uac。

- 空名单或已配置允许任何用户不满足上述完整230守卫；不将三个条件改成OR。配置schema与其他缺省值不在本页核验范围。
- 本段只将“不存在绑定”列为目标404条件，不能照搬O-PF的绑定过期条件或141文字。isfocus拒绝原文回指4.4，本页保留而不另修条款号。
- 同一服务器内PF/CF无专用IP或端口时，SDP helper的NOTE说明省略对应替换；不能从有PF角色推定媒体必经该PF。

依据：3gpp-ts-24.282-v16.13.0 §6.3.1.2 SDS-session classifications，印刷页 48；3gpp-ts-24.282-v16.13.0 §9.2.4.3.4 steps1–14，印刷页 134,135,136；3gpp-ts-24.282-v16.13.0 §9.2.4.3.1–2 (offer/answer dependency)，印刷页 132。

## 各跳响应和媒体调用不等于 SDS 已交付

条件：O-PF或T-PF实际收到其已发INVITE的200或4xx/5xx/6xx；CF实际收到邀请的200，其中向邀请者生成200另须目标MCData ID匹配。各角色/响应是替代事件，不要求同时发生。

T-PF收到200后生成上游200，按PF helper处理SDP answer并映射会话身份，条件复制mcdata-info及收到的PAI，启动会话计时，调用24.582的6.2.2.5，再发送给CF。CF的邀请helper收到200调用6.3.2；9.2.4.4.4向邀请者生成200则明确要求响应中的MCData ID匹配对应INVITE目标ID，随后返回CF会话身份、SDS/isfocus标签、收到的Warning及CF SDP answer，并调用媒体过程。O-PF实际收到200时生成给主叫的200，带映射会话身份、PF SDP answer、收到的Warning，条件复制mcdata-info并保留收到的PSI/PAI，调用6.2.2.4，再发送并启动会话计时。两个PF实际收到4xx/5xx/6xx时各生成响应、带上收到的Warning，并分别转给CF或主叫客户端。以上是信令事件和媒体过程调用，不证明MSRP已连接或任何SDS已发送、交付或读取。

强度：本条各实际响应入口的构造、条件复制、发送、计时及媒体调用为SHALL。

- CF的9.2.4.4.3/.4没有列出与两个PF相同的完整4xx/5xx/6xx回程分支；不能把两个PF的局部规则拼成已经明确闭合的全链失败算法。
- 匹配条件所需响应MCData ID的取值路径没有在此段定义完整；仅有200或仅收到媒体调用不足以代替身份匹配。
- PF的200与CF的200并非所有2xx的通称。T-PF未在INVITE携refresher时200设uas，O-PF收到的请求未携refresher时200设uac，CF上游200设uac，不能统一成客户端规则。
- 这里只核24.282的24.582调用点，不展开媒体连接、首个MSRP事件、逐条发送或会话释放算法；一次会话许可不免除后续消息的实际许可检查。

依据：3gpp-ts-24.282-v16.13.0 §9.2.4.3.3 response events，印刷页 134；3gpp-ts-24.282-v16.13.0 §9.2.4.3.4 response events，印刷页 136；3gpp-ts-24.282-v16.13.0 §9.2.4.3.2，印刷页 132；3gpp-ts-24.282-v16.13.0 §9.2.4.4.2–3 response event/NOTE2，印刷页 137,138；3gpp-ts-24.282-v16.13.0 §9.2.4.4.4 final matched-200 event，印刷页 139,140。

## 条件化关联

- [客户端建立、应答与结束](sds-session-client.md)：仅在该页各客户端事件和共同条件成立时使用；不是服务器每步之后的必经步骤。
- standalone SDS 和 HTTP 文件分发使用不同请求与 caller，不能代替本页会话准入。
