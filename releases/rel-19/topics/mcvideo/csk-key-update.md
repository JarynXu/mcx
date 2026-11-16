# MCVideo CSK更新：下载条件、来源校验与替换范围

TS24.281 V19.3.0 第7章的普通在网 MCVideo 客户端与服务该用户的 PF/server；第10章仅作普通 on-demand、带 transmission control、直接单用户私呼的准入衔接。排除 partner migration、MCVideo gateway UE 接入、跨系统 gateway、别名/FTA、远程/ambient、优先通信及其例外。

每条 claim 只继承本主题 common_conditions 和自身 conditions。SIP 注册、用户认证、MCVideo 服务授权、CSK 可用、service settings 成功传达、某次呼叫获准及媒体发送/接收许可是不同结果。

外部 TS24.229、TS24.482、TS24.484、TS29.283、TS33.180 及 RFC/XML 算法只按明确调用定位依赖；不以别的服务、版本或既有高层概要补造本版报文、错误码、回滚和寿命。

## 服务器下载入口的双前提

适用条件：按7.3.7，confidentiality protection开启，且PF已在用于服务授权的REGISTER或PUBLISH中收到CSK。

PF MAY决定更新CSK；作出该决定后 SHALL执行key download。它生成SIP MESSAGE，Request-URI取第三方REGISTER的To URI，Accept-Contact带MCVideo ICSI及require/explicit，P-Asserted-Service为MCVideo ICSI；application/mikey包含CSK-ID和封装加密的CSK，再发送给client。这个具体下载入口有机密性开启和此前收到CSK的双前提，不因上传入口允许“完整性单独开启”就自动扩大下载触发条件。

- MAY更新不是每次授权后必轮换。更新算法、定时、失败重试和服务端确认切换时点未在本条给出。
- PUBLISH上传也走该下载段，但寻址仍取第三方REGISTER的To；无该历史时不自行改成PAI或XML用户ID。
- 这里是client-server signalling key，不是PCK/GMK媒体密钥，也不重新授予MCVideo服务或本次通话。

依据：§7.3.7;7.2.1;7.2.2，印刷页 152、153、154、164、165。

## 客户端验证及关联密钥替换

适用条件：client收到SIP MESSAGE，同时含MCVideo ICSI的P-Asserted-Service和application/mikey，且MIKEY CSB-ID内key identifier最高4位为2，即CSK-ID。

client按7.2.5检查原文所称initiator字段IDRi：URI型须与serving PF的PSI一致，再转UID；UID型先将该PF PSI转UID并比较。URI/UID不匹配或I_MESSAGE签名认证失败，均回488/Warning136并停止。验证后按被引安全程序解封装CSK、提取CSK-ID；成功提取时，client SHALL 用新CSK/ID替换与该PF关联的旧CSK/ID，不能替换所有服务器的密钥。

- 本版将initiator字段写成IDRi，并写用participating MCVideo function的KMS-provisioned UID key解密；保留这两项源文，不用33.180的既有摘要静默换身份/密钥归属。
- 本页未重核33.180 MIKEY-SAKKE算法、UID生成和密钥供应，也没有为非CSK-ID、未知ID type、提取失败补原文未列的错误响应。
- 7.2.5没有在成功分支明确写SIP200、旧钥回滚或服务端同步确认，不能从本地替换推出这些结果。

依据：§7.2.5，印刷页 156、157。

## 证据边界

- 普通本系统路径。外部认证、配置schema完整性、MIKEY算法、partner migration、gateway UE、全SIP事务和当前call强制结束未闭合；settings订阅仅有界观察链。

## 按需继续

- [../security/signalling-key-update](../security/signalling-key-update.md)
- [service-authorization](service-authorization.md)

[3GPP TS24.281 V19.3.0 / ETSI TS124281 V19.3.0 (2026-01)](https://www.etsi.org/deliver/etsi_ts/124200_124299/124281/19.03.00_60/ts_124281v190300p.pdf)；仅本版本。
