# 按需环境监听：角色、准入、建立反馈与释放责任

固定 TS24.379 V19.4.0，在网、单一目标、按需 MCPTT 环境监听（ambient listening）；两端不采用预建立会话，也不经跨系统网关。不是普通远程发起私呼、组呼或紧急状态变化。

local-init 与 remote-init 是替代类型：前者发起者为被监听方，后者发起者为监听方。建立、接收、响应、用户释放和服务器释放各按实际事件适用，不把全部事件合并为共同前提。

本文说明规范中的角色、许可、信令反馈与释放责任，保留具体回指和顺序疑义。SIP/SDP、安全、话权及媒体只在明确接口处引用，不宣称完整实现或实际音频成功。

## 先确认谁发起、谁被监听及哪项许可适用

适用条件：用户请求新建本地或远程发起的环境监听；客户端按所选类型检查自身配置。

local-init 的发起者请求让目标用户监听自己；remote-init 的发起者请求监听目标用户。对应 allow-request-locally-initiated-ambient-listening 或 allow-request-remote-initiated-ambient-listening 缺失或为false时，客户端告知用户并停止。通过本端检查后，以初始INVITE发往服务自身的PF，session-type=ambient-listening，并携所选类型、目标MCPTT ID的资源列表和Priv-Answer-Mode=Auto。SDP带话权控制媒体；本地类型调用普通隐式话权条件，远程类型调用授予终接客户端话权的隐式请求条件。

规范强度：对应许可缺失/false时的告知和停止、授权后请求构造发送、类型字段及相应隐式请求处理为 SHALL；本页未将可选P-Preferred-Identity头列为必需。

依据：§11.1.6.1；§11.1.6.2.0 (comparison: user indications)；§11.1.6.2.1.1 opening,steps1-15；§6.4 initial INVITE criteria (local/remote comparison)；§11.1.7.1 (comparison: remotely initiated private call roles)。页码：165,471,472,473,474,491。

隐式请求需满足6.4相应SDP属性条件；请求授予终接方话权不等于该方已获话权或音频已被接收。

端到端安全上下文需要建立时，step10调用33.180密钥处理；本页不把可选安全上下文建立条件改成永久无安全，也不展开密钥算法。

11.1.6.2.0有隐藏活动的一般说明；各具体建立和释放条款又按角色列通知动作。本页按各事件保留这些动作，不把一般说明改成全员永远无提示。

## PF 的身份、业务许可和目标许可需分别通过

适用条件：O-PF收到session-type=ambient-listening的初始INVITE。

O-PF可因资源不足或拥塞风险拒绝500并可附Retry-After。它从PAI的公共身份取得发起者MCPTT ID；绑定不存在或过期拒绝404/141。按类型检查对应环境监听许可，缺失或false拒绝403；按发起者身份寻找环境监听CF，找不到拒绝404/142。资源列表正文缺失或所有list合计多于一个entry拒绝403/145；allow-private-call缺失或false拒绝403/107。PrivateCall非空名单存在、目标不匹配且未配置允许名单外呼叫时拒绝403/144。媒体校验中未提供MCPTT speech codec则488。通过后生成送往CF的INVITE，填发起者MCPTT ID、SDP，并将Priv-Answer-Mode设为Auto后转送。

规范强度：资源/拥塞500拒绝及Retry-After为 MAY；身份、许可、目标、codec检查及其规定拒绝，后续字段构造和发送为 SHALL。

依据：§11.1.6.3.1.1 opening,steps1-16。页码：480,481,482。

单目标请求由客户端构造责任限定；PF的step6并未明写“零entry”拒绝，不把缺正文或多于一个entry改成所有非恰好一个均拒绝。

PF的本类型许可、私呼总许可和目标名单是此入口实际检查，不能用客户端已放行替代；CF仍有独立本地策略授权。

step15的位置处理仅在其隐式授予发起者条件及位置许可等条件下适用，本页不将其泛化到所有环境监听；CF定位方法和完整SIP/SDP生成依赖不在此展开。

## CF 决定准入并邀请目标，释放能力按角色给出

适用条件：CF收到环境监听INVITE，前序未拒绝；邀请动作由11.1.6.4.2 step7调用11.1.6.4.1。

CF先核Request-URI的PSI是否分配给环境监听；不符调用6.3.7.1后停止。它验证mcptt-calling-user-id并按本地策略授权，未授权403；SDP没有至少一条媒体流满足可接受参数及至少一种codec/格式时488。随后执行收到INVITE的通用处理、分配会话身份并邀请资源列表中的目标。对目标INVITE的mcptt-request-uri使用目标MCPTT ID，Request-URI使用服务目标的PF PSI，PAI使用CF PSI。local-init时向终接方给出ambient-listening-call-release能力；remote-init时加入空提示Alert-Info。CF发送邀请并启动按用户配置的最长私呼时长计时器；收到目标200后缓存Contact并调用媒体接口。

规范强度：CF所列检查、拒绝、身份填充、条件能力/提示头、邀请发送、定时器启动以及收到200后的缓存/媒体接口调用为 SHALL。

依据：§11.1.6.4.2 opening,steps1-7；§11.1.6.4.1 opening,steps1-9,response and timer paragraphs；§6.3.3.2.2 (actual step5 dependency)。页码：148,486,487,488。

目标用户身份、PF PSI、CF PSI及会话Contact用途不同。PSI定位与跨系统路由方法不在此规范段展开。

6.3.3.2.2仅在收到且支持Contact中的特征标签时缓存；它不是SDP answer生成条款。CF前序PSI不匹配处理在本页仅保留6.3.7.1接口，不推定具体错误码。

终接方只有local-init时为监听方并获该释放能力；不能推成所有终接方都能释放。发起方的能力由后述响应另行提供。

## 自动接续仍有终接准入，且不等于用户人工确认

适用条件：T-PF收到环境监听邀请；本范围不满足使用既有预建立承载条件，进入按需自动接续。终端随后收到初始INVITE。

T-PF可因资源/拥塞拒绝500并可附Retry-After；Contact缺isfocus拒绝403/104，目标MCPTT ID无公共身份绑定拒绝404，被叫配置不允许参加私呼拒绝403/127。通过后调用自动接续。按需helper在Priv-Answer-Mode=Auto等明确条件下生成183/Unconfirmed，再向客户端发INVITE；客户端200返回的发送时机受183可靠性及PRACK处理条件约束。终端可因并发超过MaxCall或资源不足拒绝；有MIKEY-SAKKE I_MESSAGE时需验证，认证失败488/136。未被拒后按6.2.3.1.1自动接受并生成发送200、SDP answer及调用媒体接口。终端在remote-init时缓存被监听角色；local-init时缓存监听角色，宜提示通话进行中，并可显示邀请者ID。

规范强度：PF资源拒绝/Retry-After、终端容量或资源拒绝及显示邀请者ID为 MAY；local-init进行中提示为 SHOULD；其余所列强制准入、认证失败拒绝、自动接续、响应及角色缓存为 SHALL。

依据：§11.1.6.3.2.1 opening,steps1-6；§6.3.2.2.5.1 (actual on-demand/pre-established selector)；§6.3.2.2.5.2 steps1-11,response paragraphs；§11.1.6.2.1.2 steps1-9,NOTE2-4；§6.2.3.1.1 steps1-10。页码：71,118,119,120,474,475,485,486。

终端拒绝后的响应可用相应错误与Warning；若具备隐藏失败原因的许可，则可用不带Warning的480。不得将自动接续理解成绕过容量、鉴权或T-PF私呼许可。

空提示Alert-Info存在时终端不得指示进度；local-init提示与显示分别为SHOULD/MAY，而角色与类型缓存为SHALL。界面是否提示不等于对方人工同意，也不证明媒体可用。

只说明本按需caller选中的自动接续；预建立选择及Replaces替换不属于本文路径。完整SIP头传递、NAT及安全/SDP实现仍为依赖。

## 发起端的200可能仍带 Unconfirmed

适用条件：CF处理邀请响应，O-PF收到对应200，或发起客户端收到183/200；各角色事件分别适用。

若CF收到目标邀请的183/Unconfirmed、支持媒体缓冲且尚未向发起者发最终响应，则生成200并带Unconfirmed、SDP answer及释放能力，调用媒体接口、发送响应并按类型缓存双方身份。另一分支是目标邀请成功且尚未发最终响应，CF生成带释放能力的200并缓存角色；邀请失败则480。O-PF收到200时生成客户端侧200，携SDP、收到的Warning、PF PSI及映射后的会话身份，并在收到P-Answer-State时传递它。发起客户端收到200调用媒体接口；remote-init必须提示建立成功，local-init不得提示成功，并缓存类型。

规范强度：在各响应守卫成立时，CF/PF构造发送、角色/类型缓存以及客户端200处理为 SHALL；remote-init的183进度提示为 MAY，且不得覆盖空提示头的 SHALL NOT。

依据：§11.1.6.4.2 response branches and NOTE1-2；§11.1.6.3.1.1 200 response steps1-8；§11.1.6.2.1.1 183/200 response paragraphs；§6.3.3.2.2 (comparison: actual cited clause)；§6.3.3.2.1 (comparison: SDP answer heading/context)；§6.3.2.2.5.2 final response 3A (comparison: Confirmed at T-PF)。页码：120,147,148,474,482,488,489。

200/Unconfirmed可以早于终接客户端最终响应；不能据发起端“建立成功”提示断言终接已确认、已听到音频或媒体全部成功。183的空提示条件必须保留，remote-init的一般可提示进度条款不能覆盖该禁止提示条件。

成功邀请分支的SDP answer明确回指6.3.3.2.2，但该条实际只缓存特征标签；早响应分支引用6.3.3.2.1。保留这个引用差异，不静默替换。

客户端200的step4将remote-init缓存监听角色写在local-init的4(b)下；CF两种响应分支的角色映射和终接端映射清楚，但本页不将客户端排版改成已无歧义的互斥实现。

CF向发起方200提供释放能力；客户端实际收到能力才满足释放门槛。本页不宣称已逐头闭合全部中间转送实现。

## 用户释放须看实际能力，不能只看监听角色

适用条件：用户请求释放既有按需环境监听，或客户端收到该会话BYE。

客户端若未在该呼叫收到的INVITE或自己INVITE的200中收到ambient-listening-call-release能力，就跳过用户释放后续步骤；收到后调用媒体接口并在会话对话内发BYE。收到该BYE的200后调用媒体接口，清除角色与类型缓存；被监听角色不提示终止，监听角色可提示。收到对端BYE时，先按6.2.6调用媒体接口并回200，再按同样角色规则处理提示和缓存。O-PF通过11.1.6.3.1.2→11.1.3.2.1.1→6.3.2.1.6向CF转BYE；T-PF通过11.1.6.3.2.2→11.1.3.2.2.1→6.3.2.2.8.1转给客户端，并按对应200处理。

规范强度：无能力跳过、BYE/200处理、角色/类型缓存清除及被监听方不提示为 SHALL；监听方终止提示为 MAY。

依据：§11.1.6.1 release roles；§11.1.6.2.1.3；§11.1.6.2.1.4；§6.2.6；§11.1.6.3.1.2；§11.1.6.3.2.2；§11.1.3.2.1.1；§11.1.3.2.2.1；§6.3.2.1.6；§6.3.2.2.8.1；§11.1.6.4.1 step6,NOTE7 (capability comparison)；§11.1.6.4.2 response capability and NOTE1-2 (originator comparison)。页码：74,75,109,124,125,464,472,475,476,482,486,487,488,489。

发起者无论local-init还是remote-init都可由CF响应获得释放能力；local-init的被监听发起者不能被“只有监听方可挂断”规则排除。remote-init的被监听终接方不能仅因已加入就推定有释放能力。

PF helper的媒体释放接口不在本页展开；6.3.2.1.6的200段原文称terminating MCPTT function，保留该角色措辞异常，不把它改成另一个业务caller。

## CF 释放需保留响应次序及原文异常

适用条件：管理员或CF事件触发既有环境监听释放，或者CF收到参与者BYE；两条入口独立。

服务器主动释放用监听者ID、被监听者ID及类型定位会话，先调用媒体接口并向被监听方发BYE；收到200后再构造带release-reason的BYE给监听方。收到监听方BYE的200后清除双方ID与类型缓存。另一入口为CF收到参与者BYE：先调用媒体接口，再按11.1.6.4.4分别列出的动作向other participant及participant的对话发送BYE；收到所发BYE的200后调用媒体释放接口、对原收到的BYE回200并清除缓存。

规范强度：在实际触发与响应事件成立时，会话定位、媒体接口调用、各BYE/200构造发送及缓存清除为 SHALL；本文不补原文未给出的合并、去重或等待规则。

依据：§11.1.6.1 server release circumstances；§11.1.6.4.1 timer expiry paragraph；§11.1.6.4.3 full；§11.1.6.4.4 full。页码：472,487,489,490,491。

计时器caller的原因值写private-call-timer-expiry，而.4.3的计时到期分支写private-call-expiry；不合并为同一个确定值。管理员触发机制不在标准范围内，其他触发事件来源23.379不在本页展开。

11.1.6.4.3在监听方200清缓存后又列一般“收到BYE的200”媒体释放及清缓存段；不自行删除重复段或发明与前段的唯一结合顺序。

11.1.6.4.4对other participant及participant均列BYE，后续200段未在此进一步区分哪一个所发BYE；不简化成只向另一方转发、也不补一个全员确认屏障。

媒体接口被调用、SIP事务响应和双方实际音频停止是不同证据层级；本页没有闭合全部媒体实现。

## 阅读边界与导航

以明确事件和角色读取本页；源文的SDP回指、客户端角色缓存排版、释放原因与重复响应段仍有上述边界，不将本页视作已修正的完整实现。

[远程发起私呼](remotely-initiated-private.md)是另一种三角色业务；[普通隐式话权](implicit-floor-request.md)不替代远程环境监听的终接授予条件。

来源：[TS24.379 V19.4.0 官方原文](https://www.etsi.org/deliver/etsi_ts/124300_124399/124379/19.04.00_60/ts_124379v190400p.pdf)。
