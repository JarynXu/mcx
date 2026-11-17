# MCPTT注册后的服务授权：PUBLISH、身份绑定与设置结果

TS24.379 V19.4.0，主系统普通在网MCPTT客户端和服务该用户的PF/server，采用授权加设置PUBLISH入口；REGISTER只用于区分SIP注册与业务授权。

排除partner migration、网关UE、跨系统、Resource-Share附加绑定、撤销/注销以及完整REGISTER授权链。客户端与服务器分别按各声明的事件和条件工作，不全局继承成功授权或保护通过。

以下处理按原文SHALL；用户成功提示保留MAY，失败提示保留SHOULD。

## 注册后，用授权加设置PUBLISH提交本业务身份

MCPTT客户端已完成SIP注册；用户认证已成功、有可用access-token，且实现选择PUBLISH执行服务授权。此处建立设置，不是以Expires=0撤销。

客户端调用共同PUBLISH过程：Request-URI为服务该用户的PF PSI，P-Preferred-Service携MCPTT ICSI，Event=poc-settings，Expires=4294967295。mcptt-info+xml携mcptt-access-token和本端mcptt-client-id，poc-settings+xml携当前auto-answer或manual-answer、所选用户profile的user-profile-index作为selected-user-profile-index，以及multiplex-support。SIP注册本身不能证明这次服务授权已成功：§7.2.1AA明确提供不带服务授权的注册入口。

PF PSI的取得、认证和token格式/发行过程不在本链，分别保留外部规范依赖。不是把resource或用户MCPTT ID直接当Request-URI。

授权PUBLISH携token；仅更新设置的§7.2.3另以mcptt-request-uri标目标用户，不能把两者成功/失败含义混用。

Expires是设置发布的值，不是access-token或身份绑定的寿命。共同过程说明client设置计时只适用于匹配Instance Identifier URN的客户端，更新client设置计时也更新user设置计时。

来源：§7.1, §7.2.1AA, §7.2.1A, §7.2.2 opening,steps5-6，印刷页177, 179, 180。

## 缺省开启保护，不能因字段可读就当作已授权

客户端构造该授权PUBLISH，按服务配置中的confidentiality-protection和integrity-protection分别选择保护；服务器处理含token、client-id及poc-settings的该请求。两端动作各有入口，不以服务器处理成功作为客户端发送前提。

两个保护配置各自缺失或为true均表示开启，只有false才关闭。任一保护开启，PUBLISH须带application/mikey，以MIKEY-SAKKE I_MESSAGE携CSK。机密性开启时token和client-id均加密，关闭时均明文；完整性开启时分别保护mcptt-info+xml和poc-settings+xml。服务器先检查各XML正文完整性，检查通过或原本未保护才继续机密性处理：两身份字段都加密则解密，成功后识别MCPTT ID及client ID；只加密一个字段判机密性处理失败；均未加密则从token取得MCPTT ID，从client-id取得client ID。§7.3.3调用该处理未成功时返回403+Warning140并停止。

Warning140原文文字为unable to decrypt XML content；调用者在整个§7.3.1A不成功时使用它，不仅限单一解密失败。 下层§6.6.3.4.2在reference validation或signature validation失败时另列403+Warning139；上层§7.3.3对§7.3.1A不成功写140。保留调用层次差异，不裁定一个唯一最终错误码或补重复响应调度。

CSK取得、MIKEY验证、XML签名与加密算法内部均为明确依赖，不把“识别出身份”当token验证或服务授权完成。

没有要求客户端自行解码token；MCPTT ID的提取属于这里的服务器步骤。

来源：§7.2.2 steps2-5,7, §6.6.2.3.1, §6.6.3.3.1，印刷页168, 174, 180；§7.3.1A token/client-id branch, §7.3.3 steps1-3，印刷页183, 184, 186；§6.6.3.4.2 steps3,5，印刷页175。

## 服务器先查并发上限，授权成功才建立绑定

服务器收到Event=poc-settings、poc-settings+xml，以及含mcptt-access-token和mcptt-client-id的mcptt-info+xml；保护处理成功后进入上限与服务授权检查。各成功/失败子分支独立适用。

服务器从P-Asserted-Identity取得IMS public user identity。用户profile的OnNetwork/anyExt含user-max-simultaneous-authorizations时检查该上限；只有该元素缺失时才检查服务配置OnNetwork/anyExt的max-simultaneous-authorizations。达到适用上限返回486+Warning164并停止；不是两种上限同时取最小值。随后按TS33.180对已识别MCPTT ID执行服务授权；不成功返回403+Warning101并停止。成功则把MCPTT ID和client ID绑定到IMS public user identity；若同用户已在另一个client授权，以client ID比较识别，保留旧绑定并创建新三方绑定。

不为服务配置全局上限缺失编造无限或默认数值；也未规定同client重复授权怎样计数。

外部TS33.180验证内容不在这里展开；并发检查通过不等于token有效。

绑定步骤先于后续RFC3903发布处理；本段没有规定发布处理失败后回滚绑定，也未给绑定寿命。Resource-Share条件下UE身份附加绑定不属于此范围。

来源：§7.3.3 opening,steps1,3a,3b,4-6，印刷页186, 187。

## 200之后的设置与profile处理仍各有条件

服务器服务授权已成功并建立相应绑定，继续§7.3.3 steps7-13。不包括迁移和网关，也不把隐式归属调用结果视为已成功。

服务器按RFC3903处理PUBLISH，不成功就停止余下步骤。成功则缓存设置直到设置到期计时器到期，发送200；该MCPTT ID有多个绑定时在响应携multiple-devices-ind=true。服务器采用收到的Answer-Mode作为本端当前模式；multiplex-support存在且true才表示支持复用，缺失或false表示不支持。需要时从用户数据库取得profile；有selected-user-profile-index时据此识别本端active profile。缺少该元素且存在多个profile时，选择包含Pre-selected-indication的profile；只有一个profile时NOTE说明其默认为pre-selected。profile含非空ImplicitAffiliations组ID条目时，随后调用§9.2.2.2.15。

原文step9发送200列在step10采用Answer-Mode、step11-12处理profile及step13调用隐式归属之前，不把200解释为这些后续依赖都已完成。

客户端本入口要求携selected-user-profile-index，但服务器另保留缺失分支；不据服务器缺省行为改写客户端要求。缺失或多个Pre-selected-indication等异常未在此给出选择算法。

multiple-devices-ind表示多个绑定，不证明每台设备当前在线、允许同时发言或全部业务准入；隐式归属仅列调用，配置下载/归属成功需各自证据。

来源：§7.3.3 steps7-13,NOTES2-5，印刷页187, 188。

## 授权加设置的反馈，不是一次通话许可

客户端收到本次§7.2.2授权加设置PUBLISH的200，或收到3xx、4xx、5xx之一。这些是替代响应分支，不要求同时满足。

收到200时客户端MAY提示MCPTT服务授权与设置成功。收到3xx、4xx或5xx时SHOULD提示失败，可参考Warning原因，并SHALL认为本端未授权。这与仅设置PUBLISH不同：§7.2.3相同错误类别只明确认为尝试的设置没有成功，不能据此互换授权状态结论。

未把6xx、超时或没有响应补入原文列举的失败类别，也不把3xx自动改写为已完成重定向重试。

服务授权成功不替代后续具体私呼/组呼权限、绑定有效期检查、组归属或媒体/话权许可；不由PUBLISH200推导完整业务可用。

来源：§7.2.2 response paragraphs, §7.2.3 response paragraphs，印刷页180, 181。

## 范围边界

用户认证、token校验、密钥供应、配置取得、SIP/RFC3903完整事务及后续隐式归属为独立依赖，不据MCVideo/MCData相似过程补齐MCPTT规则。

授权、绑定、设置缓存、active profile与具体业务许可是不同结果；本链不给端到端原子提交、回滚或统一寿命算法。

来源：[ETSI TS124379 V19.4.0](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
