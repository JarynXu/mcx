# 在网私呼：PCK 分发完成不等于通话获准

在网（on-network）；TS33.180 V19.4.0；用户已认证，UE已取得与MC service ID关联的KMS密钥材料。

本流程适用单MC系统MCPTT/MCVideo，以及跨MC系统MCPTT；不据此外推跨系统MCVideo。

## 呼叫请求携带封装密钥

发起UE生成PCK；Private Call Request中的SDP offer携带MIKEY-SAKKE I_MESSAGE，将PCK封装给终止用户的UID，同时带PCK-ID，并用发起用户UID关联密钥签名。单系统经发起侧主服务器转发；跨系统MCPTT还经终止侧伙伴服务器。

依据：§7.2.2。

## 验证签名后才解封

适用条件：所选KMS可接受，收到MIKEY-SAKKE I_MESSAGE。

接收实体按发起者身份与时间验证签名，成功后才用KMS下发的身份密钥提取/解密所封装密钥，并取得密钥标识。这里不提供完整重放检查、UID算法或MIKEY解析器。

依据：§5.2.2。

## KMS不匹配不是自动降级成功

适用条件：发起或接收KMS选择不可接受。

可返回KMS Redirect Response提供KMS信息，发起方可重新尝试。此分支不保证存在共同可接受的KMS，也不允许绕过证书/域策略。

依据：§7.2.2。

## 服务器转发与业务许可仍要区分

适用条件：本节密钥分发完成。

后续会话建立信令仍依MCPTT/MCVideo业务规范进行，因此密钥分发成功本身不能证明被叫接受或媒体已成功建立。若安全网关代表终止用户，发起客户端须向用户警示完整端到端安全可能无法保证。

依据：§7.2.2。

## 从PCK到媒体密钥

双方共享PCK及PCK-ID后，PCK作MIKEY TGK，PCK-ID作CSB-ID，RAND来自PCK下发，CS-ID按表E.1.3-1选择，由此生成SRTP master key与master salt。PCK不直接等于SRTP会话密钥。媒体MKI为32位PCK-ID，purpose tag为1。在网控制仍另按§9.4处理，不能推定与媒体相同。

依据：§7.4.1、§7.5.1，印刷页85–88。

派生须支持PRF-HMAC-SHA-256。表E.1.3-1进一步区分发送方向：MCPTT发起方/接收方为0/1，MCVideo为2/3。这里按私呼角色区分流的原始发送方向，不因当前收包端变化而互换。

## 证据边界

- TS23.379/23.281业务准入与完整呼叫状态机、SRTP完整profile、KRR列表选择算法未核，不给确定SIP失败码。
- §7.2.2对TS23.281的参考编号前后不一致；按规范名称定位，不将编号错误当作新依赖。

## 按需继续

- [kms-provisioning](kms-provisioning.md)
- [service-authorization](../identity/service-authorization.md)
- [private-encryption](../interworking/private-encryption.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，所列条款，印刷页 40、68、69、70；仅本版本，不声明与后续版本等同。

- [组媒体与控制边界](group-media-control.md)
- [UE密钥清理](ue-key-lifecycle.md)

- [kms-redirection](kms-redirection.md)

按需续读：[协议步骤](../calls/private-client-acceptance.md)，注意页面所标规范版本及独立适用条件。
