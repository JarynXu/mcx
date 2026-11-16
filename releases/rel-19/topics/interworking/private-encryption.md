# 互通私呼加密：MC保护与LMR端到端保护

ETSI正式发布的TS23.283 V19.5.0，Release19，Stage2。

适用前提：TS23.283的互通私呼加密范围。

## MC客户端与IWF之间的私呼

可采用MC媒体加密。它独立于LMR端到端加密，也可叠加使用，不能把MC保护段直接等同于跨两端的LMR保护。 [§10.4.5](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 私呼采用LMR声码器；主被叫已预先配置适当LMR端到端加密密钥

可使用LMR端到端加密；仅看声码器相同或MC加密已开启，不能推出此前密钥配置条件已经满足。 [§10.4.5](https://www.etsi.org/deliver/etsi_ts/123200_123299/123283/19.05.00_60/ts_123283v190500p.pdf)

## 边界

TS33.180只作为MC媒体加密依赖引用，本页不描述其密钥协议；LMR密钥格式和配置操作也未核验。

[private-manual](private-manual.md) · [lmr-security-transport](lmr-security-transport.md) · [encrypted-transcoding](encrypted-transcoding.md) · [结构化条件](private-encryption.json)
