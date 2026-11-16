# 组媒体与控制保护：发送者上下文和逐跳边界

TS33.180 V19.4.0；已获得并接受组安全上下文的MCPTT/MCVideo RTP组媒体。

在网控制与离网控制分开判断，不能把媒体保护方式套到全部控制消息。

## GMK是派生输入

适用条件：生成组媒体SRTP材料。

GMK作为MIKEY TGK，派生的GUK-ID作为CSB-ID，RAND取自GMK下发消息，CS-ID按表E.1.3-1选择；这些输入生成SRTP master key和master salt，之后再派生会话密钥。GMK本身不是直接使用的SRTP会话密钥。

依据：§7.4.2；7.5.1。

## 安全上下文使用发送者身份

适用条件：接收组媒体并选择安全上下文。

GUK-ID基于发送者的MC service user ID，而非接收者自己的身份。MKI必须存在，建议使用GMK-ID与GUK-ID拼接的64位值；若发送者已由其他方式确定，可仅带32位GMK-ID，由接收方按规则恢复GUK-ID。

依据：§7.4.2。

## 在网控制逐跳保护

适用条件：在网客户端—MCX服务器及MCX服务器之间的RTCP控制。

MCPTT话权、MCVideo发送控制和媒体控制用SRTCP保护；MCX服务器逐跳解密再加密。因此媒体受到保护不意味着控制信令对服务器不可见。

依据：§9.4.1。

## 控制密钥由链路决定

适用条件：在网RTCP控制；相应KFC及标识/随机数已在收发双方建立。

客户端与服务器单播使用CSK作为KFC，服务器到客户端组播使用MuSiK，服务器之间使用SPK。组播也允许Annex H所述MSCCK和legacy MKFC机制；不能概括为所有控制一律使用GMK。

依据：§9.4.2；9.4.3；9.4.5。

## 离网组控制另用GMK

适用条件：离网组控制。

改用GMK派生控制保护；其SRTCP master key、master salt和MKI与组媒体对应材料相同。此离网规则不替代在网逐跳控制规则。

依据：§7.4.2；9.4.4。

## 证据边界

- 未完整核验RFC3830/6043/3711算法实现、Annex F.1.3或Annex H；不提供可直接实现的密码算法或报文配方。
- CS-ID应查询表E.1.3-1；本页不推定未列SPK的专用映射。完整SRTP算法配置与重放处理未覆盖。

## 按需继续

- [group-key-distribution](group-key-distribution.md)
- [private-key-distribution](private-key-distribution.md)
- [ue-key-lifecycle](ue-key-lifecycle.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页 86–88、104–105；仅本版本。

- [group-call-media-boundaries](group-call-media-boundaries.md)
