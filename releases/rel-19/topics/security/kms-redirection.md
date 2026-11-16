# KMS重定向：政策提示不是新的信任授权

TS33.180 V19.4.0 §5.2.8；为密钥分发选择发起方和接收方KMS。

## 不认识接收KMS或路径政策拒绝时可能重定向

适用条件：KMS选择未知或所选KMS在通信路径上不可接受。

KRR传递可接受KMS的政策信息，可由终止实体或路径中的应用服务器发出。它不配置KMS证书；可能需要多次交互，也可能不存在共同可接受选择并导致通信失败。客户端必须支持接收，但可按政策处理或忽略。

依据：§5.2.8.1.1。

## 列表可以收窄，不能据此扩大信任

适用条件：接收或转发KRR。

KRR分别提供发起方和接收方有序KMS列表，优先项在前，也可用ANY表达该列表不加限制。路径实体可依据政策剔除不接受的KMS，列表变空导致失败；替换KRR嵌入收到的KRR。ANY不等于客户端可以信任任意互联网KMS。

依据：§5.2.8.2.1；5.2.8.2.4。

## 外部域仍必须由Home域许可并配置

适用条件：客户端考虑使用KRR指向的外部安全域。

只接受Home安全域许可且由Home KMS配置的外部域。若政策允许索取未知证书，向Home KMS请求；KRR本身不是证书可信来源。无签名或签名KMS未识别的KRR是否接受依Home KMS政策决定，不可假定一律接受。

依据：§5.2.8.3；5.2.8.5。

## 严格政策会等待Home KMS明确答复

适用条件：Home KMS配置hold communication until KMS acceptance。

客户端在Home KMS通知重定向是否可接受前不对KRR采取行动。若配置不允许KRR，全部忽略。重定向重试与最终业务会话成功是不同事件。

依据：§5.2.8.3；5.2.8.5。

## 证据边界

- §5.2.8.2.5的reduced-list文字使用do not belong，且空列表分支与回退表述存在疑义；本页不擅自修正或生成选择算法。
- §5.2.8.5中Require signed KRRs项的If no与忽略unsigned表述存在疑义；需核对勘误/实现适用规范，不能据本页生成布尔策略。
- 未核完整KRR签名验证、嵌套上限实现、Annex D请求/通知编码；签名在内容表中为可选但推荐，不称为所有KRR都强制签名。

## 按需继续

- [kms-provisioning](kms-provisioning.md)
- [private-key-distribution](private-key-distribution.md)
- [group-key-distribution](group-key-distribution.md)

[ETSI官方TS33.180 V19.4.0](https://www.etsi.org/deliver/etsi_TS/133100_133199/133180/19.04.00_60/ts_133180v190400p.pdf)，印刷页47、48、49、50、51、52、53；仅本版本。
